#!/usr/bin/env python3
"""
transcribe.py — generate a source-language SRT from a video's audio, when
no existing subtitle file was found (see find_subtitles.py / SKILL.md
Step 1).

READ THIS BEFORE CHANGING DEFAULTS
----------------------------------
ASR on *colloquial dialect* speech in a *feature film* (music under
dialogue, overlapping speakers, shouting, room tone) is much harder than
ASR on clean read speech. Whisper's Arabic training data is dominated by
MSA/news, so on Egyptian/Gulf/Levantine colloquial it does not politely
degrade — it emits confident, fluent, phonetically-plausible NONSENSE:
  heard:  "خلّصني قوام"      ->  emitted: "حصاني قوام"
  heard:  "طلبة الثانوية"   ->  emitted: "طلس التنمية"
That is why the defaults here are the expensive ones (large-v3, dialect
priming, no cross-segment conditioning). A `small` model on this content
does not produce "slightly worse subtitles" — it produces a transcript
that is wrong in a way no downstream step can detect or repair.

Backends, auto-selected:
  mlx_whisper     — Apple Silicon (Metal GPU). Dramatically faster than
                    CPU faster-whisper; this is the right backend on a
                    modern Mac and is tried first there.
  faster_whisper  — CTranslate2, CPU/CUDA. The portable fallback.
Both run fully local: no API key, no audio leaves the machine.

Outputs TWO files:
  <out.srt>            the subtitles
  <out.srt>.asr.json   per-segment confidence + word timings

The sidecar is not optional bookkeeping — asr_confidence.py and
check_transcript_fidelity.py both need it, and the fidelity gate in
SKILL.md Step 1.5 cannot run without it. Never delete it before the
source transcript has been verified.

Usage:
    python3 transcribe.py movie.mp4 source.srt --lang ar --dialect egyptian
    python3 transcribe.py movie.mp4 source.srt --lang ar --model large-v3 \
        --initial-prompt "بعض الأسماء والمصطلحات المتوقعة في الفيلم"
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import subprocess
import sys
import tempfile

from srt_utils import Cue, write_srt

# --------------------------------------------------------------------------
# Dialect priming.
#
# Whisper conditions on `initial_prompt` as if it were the transcript of
# the preceding audio. Feeding it colloquial orthography plus the film's
# own vocabulary measurably pulls output away from MSA normalization and
# toward what was actually said. Domain nouns matter most: a word the
# model has "seen" recently is far likelier to be recognized than guessed.
# --------------------------------------------------------------------------
DIALECT_PROMPTS = {
    "egyptian": (
        "حوار بالعامية المصرية. كلام عادي بين ناس، مش فصحى ولا نشرة أخبار. "
        "إيه، ده، دي، كده، إزاي، عايز، مش، بقى، خلاص، يعني، أهو، دلوقتي، "
        "معلش، يا عم، يا باشا، يا أستاذ، طيب، أصل، علشان، النهاردة."
    ),
    "gulf": (
        "حوار باللهجة الخليجية. كلام عادي بين ناس، مو فصحى. "
        "شنو، وش، كذا، زين، ابغى، ما، يبغى، هسه، الحين، عاد، يا بعد، طيب."
    ),
    "levantine": (
        "حوار باللهجة الشامية. كلام عادي بين ناس، مش فصحى. "
        "شو، هيك، كيف، بدي، مش، هلق، يعني، طيب، منيح، خلص، يا زلمة."
    ),
    "maghrebi": (
        "حوار باللهجة المغاربية. هضرة عادية بين الناس، ماشي فصحى. "
        "شنو، هاكا، كيفاش، بغيت، ماشي، دابا، يعني، واخا، بزاف، صافي."
    ),
}

# Whisper's Arabic/English training data includes a lot of fan-subtitled
# video, so it hallucinates subtitle boilerplate into silence and music.
# These are the recurring ones; extend per-project via --drop-pattern.
HALLUCINATION_PATTERNS = [
    r"المترجم", r"مترجم\s*للقناة", r"ترجمة\s+\S+", r"اشتراك", r"اشتركوا",
    r"شكرا\s+للمشاهدة", r"شكرًا\s+للمشاهدة", r"تمت\s+الترجمة",
    r"subscribe", r"translated\s+by", r"subtitles?\s+by", r"thanks?\s+for\s+watching",
    r"www\.", r"https?://",
]

REPEAT_RE = re.compile(r"(\S+)(?:\s+\1){2,}")

# Cue shaping. Kept here (not in validate_srt.py) because these decide
# where a cue is CUT, which needs word timings that only exist at ASR time.
MAX_CUE_CHARS = 46
MAX_CUE_SECONDS = 6.5
MAX_GAP = 0.7
MIN_CUE_SECONDS = 0.6


def extract_audio(video_path: str, wav_path: str) -> None:
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-ac", "1", "-ar", "16000", "-acodec", "pcm_s16le",
        wav_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg audio extraction failed:\n{result.stderr[-2000:]}")


def pick_backend(requested: str) -> str:
    """Choose an ASR backend. Apple Silicon gets mlx first — it is the
    difference between 'runs in minutes' and 'runs longer than the film'."""
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
    raise SystemExit(
        "No ASR backend available. Install one:\n"
        "  Apple Silicon:  pip install --break-system-packages mlx-whisper\n"
        "  anything else:  pip install --break-system-packages faster-whisper\n"
        "(or: pip install --break-system-packages -r requirements.txt)"
    )


def build_prompt(args) -> str | None:
    parts = []
    if args.dialect:
        key = args.dialect.lower()
        if key not in DIALECT_PROMPTS:
            print(
                f"warning: unknown --dialect {args.dialect!r}; known: "
                f"{', '.join(sorted(DIALECT_PROMPTS))}. Ignoring.",
                file=sys.stderr,
            )
        else:
            parts.append(DIALECT_PROMPTS[key])
    if args.initial_prompt:
        parts.append(args.initial_prompt)
    return " ".join(parts) if parts else None


def is_hallucination(text: str, extra: list[re.Pattern]) -> bool:
    t = " ".join(text.split())
    if not t:
        return True
    for pat in HALLUCINATION_PATTERNS:
        if re.search(pat, t, re.I):
            return True
    return any(p.search(t) for p in extra)


def collapse_repeats(text: str) -> str:
    prev = None
    while prev != text:
        prev = text
        text = REPEAT_RE.sub(lambda m: m.group(1), text)
    return " ".join(text.split())


# --------------------------------------------------------------------------
# Backends. Both normalize to the same shape:
#   {"language", "segments": [{start, end, text, avg_logprob,
#                              no_speech_prob, compression_ratio, words}]}
# so everything downstream is backend-agnostic.
#
# Shared decoding choices, and why:
#   condition_on_previous_text=False
#       Whisper's default (True) feeds its own last output back in as
#       context. On a film that is a drift amplifier: one garbled line
#       biases the next, and the transcript slides into a self-consistent
#       fiction. Off is strictly better for dialogue.
#   temperature fallback (0.0, 0.2, 0.4)
#       Retry a segment with more randomness only when greedy decoding
#       trips the quality thresholds below, instead of accepting junk.
#   compression_ratio_threshold / logprob_threshold / no_speech_threshold
#       The three signals that mark "this segment is probably garbage".
#       Kept slightly stricter than stock so low-confidence spans get
#       FLAGGED rather than silently blessed.
# --------------------------------------------------------------------------
def run_mlx(wav: str, lang: str | None, model: str, prompt: str | None) -> dict:
    import mlx_whisper

    repo = model
    if not os.path.exists(model):
        repo = f"mlx-community/whisper-{model}" if not model.startswith("mlx-community/") else model

    result = mlx_whisper.transcribe(
        wav,
        path_or_hf_repo=repo,
        language=lang,
        word_timestamps=True,
        condition_on_previous_text=False,
        temperature=(0.0, 0.2, 0.4),
        compression_ratio_threshold=2.2,
        logprob_threshold=-0.8,
        no_speech_threshold=0.6,
        initial_prompt=prompt,
        verbose=False,
    )
    return {
        "language": result.get("language"),
        "segments": [
            {
                "start": s.get("start"),
                "end": s.get("end"),
                "text": s.get("text", ""),
                "avg_logprob": s.get("avg_logprob"),
                "no_speech_prob": s.get("no_speech_prob"),
                "compression_ratio": s.get("compression_ratio"),
                "words": s.get("words") or [],
            }
            for s in (result.get("segments") or [])
        ],
    }


def run_faster(wav: str, lang: str | None, model: str, prompt: str | None) -> dict:
    from faster_whisper import WhisperModel

    device, compute = "cpu", "int8"
    try:  # use CUDA when it is actually there
        import torch
        if torch.cuda.is_available():
            device, compute = "cuda", "float16"
    except ImportError:
        pass

    wm = WhisperModel(model, device=device, compute_type=compute)
    segments, info = wm.transcribe(
        wav,
        language=lang,
        word_timestamps=True,
        condition_on_previous_text=False,
        temperature=[0.0, 0.2, 0.4],
        compression_ratio_threshold=2.2,
        log_prob_threshold=-0.8,
        no_speech_threshold=0.6,
        initial_prompt=prompt,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 700},
    )
    out = []
    for s in segments:
        out.append({
            "start": s.start,
            "end": s.end,
            "text": s.text or "",
            "avg_logprob": s.avg_logprob,
            "no_speech_prob": s.no_speech_prob,
            "compression_ratio": s.compression_ratio,
            "words": [
                {"word": w.word, "start": w.start, "end": w.end, "probability": w.probability}
                for w in (s.words or [])
            ],
        })
    return {"language": info.language, "segments": out}


def collect_words(result: dict, extra_drop: list[re.Pattern]) -> list[dict]:
    """Flatten to a word stream, carrying each word's parent-segment
    confidence so cue-level confidence can be computed after splitting."""
    words: list[dict] = []
    for seg in result.get("segments") or []:
        conf = {
            "avg_logprob": seg.get("avg_logprob"),
            "no_speech_prob": seg.get("no_speech_prob"),
            "compression_ratio": seg.get("compression_ratio"),
        }
        seg_words = seg.get("words") or []
        if seg_words:
            for w in seg_words:
                text = (w.get("word") or w.get("text") or "").strip()
                if not text or is_hallucination(text, extra_drop):
                    continue
                start = float(w.get("start", 0.0) or 0.0)
                end = float(w.get("end", start) or start)
                words.append({"text": text, "start": start, "end": max(end, start),
                              "prob": w.get("probability"), **conf})
        else:
            text = collapse_repeats((seg.get("text") or "").strip())
            if not text or is_hallucination(text, extra_drop):
                continue
            words.append({"text": text, "start": float(seg.get("start", 0.0) or 0.0),
                          "end": float(seg.get("end", 0.0) or 0.0), "prob": None, **conf})
    return words


def should_split(current: list[dict], nxt: dict) -> bool:
    if not current:
        return False
    gap = nxt["start"] - current[-1]["end"]
    duration = nxt["end"] - current[0]["start"]
    text = " ".join(w["text"] for w in current)
    punct = current[-1]["text"].endswith((".", "!", "؟", "?", "،", ",", "؛", "…"))
    if gap >= MAX_GAP:
        return True
    if duration >= MAX_CUE_SECONDS and (punct or gap >= 0.2):
        return True
    if len(text) >= MAX_CUE_CHARS and (punct or gap >= 0.15 or len(text) >= MAX_CUE_CHARS + 22):
        return True
    return False


def wrap_cue(text: str) -> str:
    text = collapse_repeats(text)
    if len(text) <= MAX_CUE_CHARS:
        return text
    words, line1 = text.split(" "), []
    for w in words:
        if line1 and len(" ".join(line1 + [w])) > MAX_CUE_CHARS:
            break
        line1.append(w)
    rest = " ".join(words[len(line1):]).strip()
    return f"{' '.join(line1)}\n{rest}" if rest else " ".join(line1)


def build_cues(words: list[dict], extra_drop: list[re.Pattern]) -> tuple[list[Cue], list[dict]]:
    """Group the word stream into cues and compute each cue's confidence.

    Returns (cues, meta) where meta[i] carries the confidence signals for
    cues[i] — this is what lands in the .asr.json sidecar and what
    asr_confidence.py thresholds on.
    """
    groups: list[list[dict]] = []
    bucket: list[dict] = []
    for w in words:
        if should_split(bucket, w):
            groups.append(bucket)
            bucket = [w]
        else:
            bucket.append(w)
    if bucket:
        groups.append(bucket)

    cues: list[Cue] = []
    meta: list[dict] = []
    for i, g in enumerate(groups):
        start, end = g[0]["start"], g[-1]["end"]
        if end - start < MIN_CUE_SECONDS:
            end = start + MIN_CUE_SECONDS
        if i + 1 < len(groups):  # never overlap the next cue
            nxt = groups[i + 1][0]["start"]
            if end > nxt - 0.04:
                end = max(start + 0.12, nxt - 0.04)

        raw_text = " ".join(w["text"] for w in g)
        text = wrap_cue(raw_text)
        if not text.strip() or is_hallucination(text, extra_drop):
            continue

        probs = [w["prob"] for w in g if w.get("prob") is not None]
        logps = [w["avg_logprob"] for w in g if w.get("avg_logprob") is not None]
        nosp = [w["no_speech_prob"] for w in g if w.get("no_speech_prob") is not None]
        comps = [w["compression_ratio"] for w in g if w.get("compression_ratio") is not None]

        idx = len(cues) + 1
        cues.append(Cue(index=idx, start_ms=int(start * 1000),
                        end_ms=int(end * 1000), text=text))
        meta.append({
            "index": idx,
            "start": round(start, 3),
            "end": round(end, 3),
            "text": text.replace("\n", " "),
            "word_prob_mean": round(sum(probs) / len(probs), 4) if probs else None,
            "word_prob_min": round(min(probs), 4) if probs else None,
            "avg_logprob": round(min(logps), 4) if logps else None,
            "no_speech_prob": round(max(nosp), 4) if nosp else None,
            "compression_ratio": round(max(comps), 4) if comps else None,
        })
    return cues, meta


def main():
    ap = argparse.ArgumentParser(
        description="Transcribe a video's audio to SRT, with a confidence sidecar.")
    ap.add_argument("video_path")
    ap.add_argument("out_srt")
    ap.add_argument("--lang", default=None,
                    help="source language code, e.g. ar. Strongly recommended — "
                         "auto-detect mis-fires on films that mix languages or sing.")
    ap.add_argument("--model", default="large-v3",
                    help="default large-v3. Smaller models do not degrade gracefully "
                         "on dialect/film audio — see the module docstring.")
    ap.add_argument("--backend", default="auto", choices=["auto", "mlx", "faster"])
    ap.add_argument("--dialect", default=None,
                    help=f"prime the model for a spoken dialect: {', '.join(sorted(DIALECT_PROMPTS))}")
    ap.add_argument("--initial-prompt", default=None,
                    help="extra priming text: character names, places, recurring "
                         "domain nouns. Raises recognition of exactly those words.")
    ap.add_argument("--drop-pattern", action="append", default=[],
                    help="extra regex for boilerplate to drop (repeatable)")
    ap.add_argument("--keep-wav", help="also save the extracted 16kHz WAV here "
                                       "(retranscribe_spans.py needs it — keep it)")
    args = ap.parse_args()

    extra_drop = [re.compile(p, re.I) for p in args.drop_pattern]
    backend = pick_backend(args.backend)
    prompt = build_prompt(args)

    if args.lang == "ar" and not args.dialect:
        print("note: --lang ar without --dialect. If this is colloquial speech "
              "(most films/TV are), pass e.g. --dialect egyptian — Whisper "
              "normalizes Arabic toward MSA otherwise.", file=sys.stderr)

    with tempfile.TemporaryDirectory() as tmp:
        wav_path = args.keep_wav or os.path.join(tmp, "audio.wav")
        print(f"Extracting audio -> {wav_path} ...")
        extract_audio(args.video_path, wav_path)

        print(f"Transcribing: backend={backend} model={args.model} "
              f"lang={args.lang or 'auto'} dialect={args.dialect or 'none'} ...")
        runner = run_mlx if backend == "mlx" else run_faster
        result = runner(wav_path, args.lang, args.model, prompt)

    words = collect_words(result, extra_drop)
    cues, meta = build_cues(words, extra_drop)
    if not cues:
        raise SystemExit("Transcription produced zero cues — check the audio track/language hint.")

    write_srt(cues, args.out_srt)

    sidecar = args.out_srt + ".asr.json"
    with open(sidecar, "w", encoding="utf-8") as f:
        json.dump({
            "source_video": os.path.abspath(args.video_path),
            "audio_wav": os.path.abspath(args.keep_wav) if args.keep_wav else None,
            "backend": backend,
            "model": args.model,
            "language": result.get("language"),
            "dialect_prompt": args.dialect,
            "initial_prompt": prompt,
            "cue_count": len(cues),
            "cues": meta,
        }, f, ensure_ascii=False, indent=1)

    print(f"{len(cues)} cues -> {args.out_srt}")
    print(f"confidence sidecar -> {sidecar}")
    print()
    print("NEXT STEP IS NOT TRANSLATION. Run the confidence triage first:")
    print(f"    python3 asr_confidence.py {args.out_srt}")
    print("Low-confidence cues must be re-checked AGAINST THE AUDIO "
          "(retranscribe_spans.py), never 'cleaned up' by guessing from "
          "context — see SKILL.md Step 1.5.")


if __name__ == "__main__":
    main()
