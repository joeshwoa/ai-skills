#!/usr/bin/env python3
"""
asr_confidence.py — triage an ASR transcript before anyone translates it.

Whisper knows when it is struggling; it just doesn't say so in the SRT.
Each segment carries avg_logprob (how confident the decode was),
no_speech_prob (how likely this was not speech at all) and
compression_ratio (how repetitive the text is — a classic loop/
hallucination tell). transcribe.py stores all three per cue in the
<out.srt>.asr.json sidecar. This reads them back and tells you which
cues you cannot trust.

The point is to make uncertainty VISIBLE and ACTIONABLE before the
transcript is treated as ground truth. A cue that lands in the review
queue must be resolved against the audio (retranscribe_spans.py), not
smoothed over by an agent reading the surrounding dialogue.

USAGE
    python3 asr_confidence.py source.srt
    python3 asr_confidence.py source.srt --queue review_queue.json
    python3 asr_confidence.py source.srt --logprob -0.7 --top 40

EXIT CODES
    0  everything above threshold
    2  low-confidence cues exist -> triage them (not a crash; a to-do)
"""
from __future__ import annotations

import argparse
import json
import os
import sys

# Defaults chosen to surface real trouble without drowning you in noise.
# avg_logprob below ~-0.7 on Whisper is where dialect output starts being
# phonetic guesswork rather than recognition.
DEFAULT_LOGPROB = -0.7
DEFAULT_NO_SPEECH = 0.5
DEFAULT_COMPRESSION = 2.2
DEFAULT_WORD_PROB = 0.5


def load_sidecar(srt_path: str) -> dict:
    path = srt_path + ".asr.json"
    if not os.path.exists(path):
        raise SystemExit(
            f"No confidence sidecar at {path}.\n"
            "It is written by transcribe.py alongside the SRT. Without it there is\n"
            "no way to tell which cues the model was guessing at, so the transcript\n"
            "cannot be triaged — re-run transcribe.py, or if these subtitles came\n"
            "from an external .srt file, treat the whole file as unverified and\n"
            "spot-check it against the audio before translating."
        )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def reasons_for(cue: dict, args) -> list[str]:
    out = []
    lp, ns = cue.get("avg_logprob"), cue.get("no_speech_prob")
    cr, wp = cue.get("compression_ratio"), cue.get("word_prob_mean")
    if lp is not None and lp < args.logprob:
        out.append(f"low avg_logprob {lp}")
    if ns is not None and ns > args.no_speech:
        out.append(f"probably not speech ({ns})")
    if cr is not None and cr > args.compression:
        out.append(f"repetitive/looping (compression {cr})")
    if wp is not None and wp < args.word_prob:
        out.append(f"weak word probs (mean {wp})")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Flag ASR cues that must be checked against audio.")
    ap.add_argument("srt_path")
    ap.add_argument("--queue", help="write the review queue JSON here "
                                    "(input to retranscribe_spans.py)")
    ap.add_argument("--logprob", type=float, default=DEFAULT_LOGPROB)
    ap.add_argument("--no-speech", type=float, default=DEFAULT_NO_SPEECH)
    ap.add_argument("--compression", type=float, default=DEFAULT_COMPRESSION)
    ap.add_argument("--word-prob", type=float, default=DEFAULT_WORD_PROB)
    ap.add_argument("--top", type=int, default=25, help="how many to print (all still go to --queue)")
    args = ap.parse_args()

    data = load_sidecar(args.srt_path)
    cues = data.get("cues") or []
    flagged = []
    for c in cues:
        why = reasons_for(c, args)
        if why:
            flagged.append({**c, "reasons": why})

    total = len(cues) or 1
    print(f"transcript: {args.srt_path}")
    print(f"backend={data.get('backend')} model={data.get('model')} "
          f"language={data.get('language')} dialect={data.get('dialect_prompt') or 'none'}")
    print(f"cues: {len(cues)}   flagged: {len(flagged)} ({len(flagged)/total*100:.1f}%)")

    if not flagged:
        print("\nNo low-confidence cues. Still spot-check a few against the audio "
              "before translating — confidence is a signal, not a guarantee.")
        return 0

    flagged.sort(key=lambda c: (c.get("avg_logprob") if c.get("avg_logprob") is not None else 0))
    print(f"\nWorst {min(args.top, len(flagged))}:")
    for c in flagged[:args.top]:
        ts = f"{c['start']:.1f}-{c['end']:.1f}s"
        print(f"  #{c['index']:<5} {ts:<16} {'; '.join(c['reasons'])}")
        print(f"        {c['text'][:100]}")

    if args.queue:
        with open(args.queue, "w", encoding="utf-8") as f:
            json.dump({
                "srt_path": os.path.abspath(args.srt_path),
                "audio_wav": data.get("audio_wav"),
                "source_video": data.get("source_video"),
                "language": data.get("language"),
                "dialect_prompt": data.get("dialect_prompt"),
                "initial_prompt": data.get("initial_prompt"),
                "flagged_count": len(flagged),
                "cues": flagged,
            }, f, ensure_ascii=False, indent=1)
        print(f"\nreview queue -> {args.queue}")

    pct = len(flagged) / total * 100
    if pct > 25:
        print(f"\n{pct:.0f}% of this transcript is low-confidence. That usually means the "
              f"\nmodel is wrong about the LANGUAGE VARIETY, not just a few lines:")
        print("  - is --dialect set, and set correctly?")
        print("  - is --model large-v3 (not small/medium)?")
        print("  - does --initial-prompt name the characters/places/domain nouns?")
        print("Re-transcribing the whole film with those fixed usually beats "
              "repairing hundreds of cues one at a time.")

    print("\nResolve every flagged cue against the AUDIO:")
    print(f"    python3 retranscribe_spans.py {args.queue or '<queue.json>'} --out candidates.json")
    print("Never resolve one by inferring it from the surrounding dialogue.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
