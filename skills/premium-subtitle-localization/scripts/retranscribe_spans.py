#!/usr/bin/env python3
"""
retranscribe_spans.py — the legitimate way to fix a garbled cue.

A cue flagged by asr_confidence.py has exactly three honest resolutions
(SKILL.md Step 1.5): re-transcribe it from audio, mark it unclear, or ask
the user. This script implements the first and best one.

For each flagged cue it cuts that span out of the audio WITH PADDING
(context matters: Whisper decodes a 1.5s fragment far worse than the same
words inside a 6s window), then decodes it several times under different
conditions — greedy vs. sampled, with and without the dialect prompt.
Readings that AGREE across independent decodes are probably what was
said. Readings that scatter mean the audio genuinely doesn't support a
confident transcript, and the honest output is "unclear", not a guess.

This is the key distinction the skill got wrong before: a second opinion
from the AUDIO is evidence. A second opinion from an LLM reading the
surrounding subtitles is not — it is the same guess with more confidence.

WORKFLOW
    1. python3 asr_confidence.py source.srt --queue review_queue.json
    2. python3 retranscribe_spans.py review_queue.json --out candidates.json
    3. Read candidates.json. For each cue set "chosen" to the candidate
       text you are adopting (copy it exactly), or "" to mark it unclear.
    4. python3 retranscribe_spans.py --finalize candidates.json source.srt \
           --evidence evidence.json
    5. python3 check_transcript_fidelity.py raw.srt source.srt --evidence evidence.json

Step 4 is what makes an edit legitimate: it writes only text that came
out of a decode, and records the cue index as audio-verified so the
fidelity gate accepts it.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import tempfile

from srt_utils import parse_srt, write_srt, Cue

PAD_SECONDS = 1.2
UNCLEAR_MARKER = "[غير واضح]"


def cut_span(wav: str, start: float, end: float, out_wav: str) -> None:
    s = max(0.0, start - PAD_SECONDS)
    dur = (end + PAD_SECONDS) - s
    cmd = ["ffmpeg", "-y", "-ss", f"{s:.3f}", "-t", f"{dur:.3f}",
           "-i", wav, "-ac", "1", "-ar", "16000", "-acodec", "pcm_s16le", out_wav]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg span cut failed:\n{r.stderr[-1500:]}")


def pick_backend(requested: str) -> str:
    if requested != "auto":
        return requested
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        try:
            import mlx_whisper  # noqa: F401
            return "mlx"
        except ImportError:
            pass
    try:
        import faster_whisper  # noqa: F401
        return "faster"
    except ImportError:
        pass
    raise SystemExit("No ASR backend installed — see requirements.txt.")


def decode(backend: str, wav: str, lang: str, model: str,
           prompt: str | None, temperature: float) -> str:
    """One decode pass. Returns the plain text heard in this span."""
    if backend == "mlx":
        import mlx_whisper
        repo = model if os.path.exists(model) or model.startswith("mlx-community/") \
            else f"mlx-community/whisper-{model}"
        res = mlx_whisper.transcribe(
            wav, path_or_hf_repo=repo, language=lang,
            temperature=temperature, condition_on_previous_text=False,
            initial_prompt=prompt, word_timestamps=False, verbose=False,
        )
        return " ".join((s.get("text") or "").strip() for s in (res.get("segments") or [])).strip()

    from faster_whisper import WhisperModel
    global _FW_CACHE
    try:
        _FW_CACHE
    except NameError:
        _FW_CACHE = {}
    if model not in _FW_CACHE:
        _FW_CACHE[model] = WhisperModel(model, device="cpu", compute_type="int8")
    segs, _ = _FW_CACHE[model].transcribe(
        wav, language=lang, temperature=temperature,
        condition_on_previous_text=False, initial_prompt=prompt,
        word_timestamps=False,
    )
    return " ".join((s.text or "").strip() for s in segs).strip()


def gather(args) -> int:
    with open(args.queue, encoding="utf-8") as f:
        q = json.load(f)

    wav = args.audio or q.get("audio_wav")
    if not wav or not os.path.exists(wav):
        raise SystemExit(
            "Need the extracted audio WAV to re-listen.\n"
            f"  queue says: {wav!r}\n"
            "Pass --audio /path/to/audio.wav, or re-run transcribe.py with\n"
            "--keep-wav so the audio is preserved for exactly this step."
        )

    backend = pick_backend(args.backend)
    lang = args.lang or q.get("language") or "ar"
    prompt = q.get("initial_prompt")
    cues = q.get("cues") or []
    if args.limit:
        cues = cues[:args.limit]

    # Independent conditions. Dropping the prompt on one pass matters:
    # a prompt raises recall of its own vocabulary, so a reading that
    # survives WITHOUT it is better evidence than one that only appears
    # with it.
    conditions = [
        ("greedy+prompt", 0.0, prompt),
        ("sampled+prompt", 0.4, prompt),
        ("greedy+noprompt", 0.0, None),
    ]

    results = []
    print(f"Re-transcribing {len(cues)} spans (backend={backend}, model={args.model}) ...")
    with tempfile.TemporaryDirectory() as tmp:
        for n, c in enumerate(cues, 1):
            span_wav = os.path.join(tmp, f"span_{c['index']}.wav")
            try:
                cut_span(wav, float(c["start"]), float(c["end"]), span_wav)
            except Exception as e:
                print(f"  #{c['index']}: span cut failed: {e}", file=sys.stderr)
                continue

            cands = []
            for label, temp, pr in conditions:
                try:
                    text = decode(backend, span_wav, lang, args.model, pr, temp)
                except Exception as e:
                    text = f"<decode failed: {e}>"
                cands.append({"condition": label, "text": text})

            texts = [c2["text"] for c2 in cands if not c2["text"].startswith("<")]
            agree = len(texts) > 1 and len(set(" ".join(t.split()) for t in texts)) == 1

            results.append({
                "index": c["index"],
                "start": c["start"],
                "end": c["end"],
                "original_asr": c.get("text", ""),
                "reasons": c.get("reasons", []),
                "candidates": cands,
                "unanimous": agree,
                # The agent fills this in: copy one candidate's text
                # verbatim, or "" to mark the cue unclear.
                "chosen": None,
            })
            if n % 10 == 0 or n == len(cues):
                print(f"  {n}/{len(cues)}")

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"srt_path": q.get("srt_path"), "audio_wav": wav,
                   "backend": backend, "model": args.model,
                   "spans": results}, f, ensure_ascii=False, indent=1)

    unan = sum(1 for r in results if r["unanimous"])
    print(f"\n{len(results)} spans -> {args.out}")
    print(f"  {unan} decoded identically under every condition (strong evidence)")
    print(f"  {len(results) - unan} disagree between decodes — if the readings scatter,")
    print(f"     the honest answer is \"{UNCLEAR_MARKER}\", not the nicest-sounding option.")
    print("\nNow set \"chosen\" for each span, then:")
    print(f"    python3 retranscribe_spans.py --finalize {args.out} <source.srt> --evidence evidence.json")
    return 0


def finalize(args) -> int:
    with open(args.finalize, encoding="utf-8") as f:
        data = json.load(f)
    spans = data.get("spans") or []
    cues = parse_srt(args.srt_path)
    by_index = {c.index: c for c in cues}

    applied, unclear, skipped, bad = [], [], [], []
    for s in spans:
        chosen = s.get("chosen")
        if chosen is None:
            skipped.append(s["index"])
            continue
        cue = by_index.get(s["index"])
        if cue is None:
            bad.append(s["index"])
            continue
        if chosen == "":
            cue.text = UNCLEAR_MARKER
            unclear.append(s["index"])
            continue
        # An adopted reading must be one the audio actually produced.
        offered = {" ".join(c["text"].split()) for c in s.get("candidates", [])}
        if " ".join(chosen.split()) not in offered:
            bad.append(s["index"])
            continue
        cue.text = chosen
        applied.append(s["index"])

    if bad:
        print("REFUSED — these spans have a \"chosen\" value that no decode produced:")
        for i in bad[:20]:
            print(f"  #{i}")
        print("\nA chosen reading must be copied verbatim from that span's candidates.")
        print("Writing text the audio never produced is the exact failure this")
        print("script exists to prevent. Use \"\" to mark a cue unclear instead.")
        return 1

    write_srt(cues, args.srt_path)
    evidence = {"verified_indices": sorted(applied + unclear),
                "applied": sorted(applied), "marked_unclear": sorted(unclear),
                "source": os.path.abspath(args.finalize)}
    with open(args.evidence, "w", encoding="utf-8") as f:
        json.dump(evidence, f, ensure_ascii=False, indent=1)

    print(f"applied from audio: {len(applied)}")
    print(f"marked unclear:     {len(unclear)}")
    print(f"left untouched:     {len(skipped)}")
    print(f"updated -> {args.srt_path}")
    print(f"evidence -> {args.evidence}")
    print("\nNow re-run the fidelity gate:")
    print(f"    python3 check_transcript_fidelity.py <raw.srt> {args.srt_path} --evidence {args.evidence}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Re-transcribe low-confidence spans from audio.")
    ap.add_argument("queue", nargs="?", help="review_queue.json from asr_confidence.py")
    ap.add_argument("--out", default="candidates.json")
    ap.add_argument("--audio", help="extracted WAV (defaults to the path recorded in the queue)")
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--backend", default="auto", choices=["auto", "mlx", "faster"])
    ap.add_argument("--lang", default=None)
    ap.add_argument("--limit", type=int, help="only process the first N flagged spans")
    ap.add_argument("--finalize", metavar="CANDIDATES_JSON",
                    help="apply chosen readings to an SRT and write the evidence file")
    ap.add_argument("srt_path", nargs="?", help="SRT to update (with --finalize)")
    ap.add_argument("--evidence", default="evidence.json")
    args = ap.parse_args()

    if args.finalize:
        # Two optional positionals: argparse hands a lone trailing path to
        # `queue`, so accept it as the SRT and keep the documented
        # `--finalize candidates.json source.srt` form working.
        if not args.srt_path and args.queue:
            args.srt_path, args.queue = args.queue, None
        if not args.srt_path:
            raise SystemExit("--finalize needs the SRT to update: "
                             "retranscribe_spans.py --finalize candidates.json source.srt")
        return finalize(args)
    if not args.queue:
        raise SystemExit("Give a review queue JSON, or use --finalize. See --help.")
    return gather(args)


if __name__ == "__main__":
    sys.exit(main())
