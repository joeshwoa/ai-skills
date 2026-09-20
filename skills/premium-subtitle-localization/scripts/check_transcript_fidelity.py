#!/usr/bin/env python3
"""
check_transcript_fidelity.py — the anti-fabrication gate.

WHY THIS EXISTS
---------------
This skill once shipped an Arabic transcript in which 81% of cues had
been altered away from what the ASR actually heard, and 101 cues had
silently vanished. Nothing caught it. Every existing check passed:
validate_srt.py saw well-formed cues with legal timings, verify_output.py
saw a playable file with the right duration, and the translation QA pass
compared the Russian against the Arabic — which was itself already wrong.

The mechanism was not malice or a bug. ASR on dialect film audio returns
garbled text; an agent handed garbled text will, absent a rule against
it, "repair" it into fluent plausible prose. That reads BETTER and is
far WORSE: a reviewer without the audio cannot tell invented dialogue
from real dialogue, because invention is exactly what fluency looks like.

So: any edit to the source transcript must be justified by evidence from
the AUDIO, not by context. This script measures how far an edited
transcript has drifted from the raw ASR and fails when drift is large
and undocumented.

USAGE
    # after editing source.srt, before translating anything:
    python3 check_transcript_fidelity.py source.raw.srt source.srt

    # with an evidence file recording which cues were re-transcribed:
    python3 check_transcript_fidelity.py source.raw.srt source.srt \
        --evidence retranscribe_evidence.json

    python3 check_transcript_fidelity.py raw.srt edited.srt --report drift.json

EXIT CODES
    0  drift is within limits, or fully covered by evidence
    1  undocumented drift over threshold, or silent cue drops -> STOP
"""
from __future__ import annotations

import argparse
import difflib
import json
import sys

from srt_utils import parse_srt


def norm(text: str) -> str:
    """Compare on content, not layout: line wrapping and whitespace are
    formatting decisions and are not drift."""
    return " ".join(text.replace("\n", " ").split())


def similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def load_evidence(path: str | None) -> set[int]:
    """Cue indices whose edit is backed by a re-transcription from audio.
    Written by retranscribe_spans.py; may also be maintained by hand as
    a JSON list of indices or {"verified_indices": [...]}"""
    if not path:
        return set()
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = data.get("verified_indices") or data.get("indices") or []
    out = set()
    for item in data:
        if isinstance(item, int):
            out.add(item)
        elif isinstance(item, dict) and "index" in item:
            out.add(int(item["index"]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Detect fabricated/undocumented edits to an ASR transcript.")
    ap.add_argument("raw_srt", help="the untouched ASR output")
    ap.add_argument("edited_srt", help="the transcript as it stands now")
    ap.add_argument("--evidence", help="JSON listing cue indices re-checked against audio")
    ap.add_argument("--max-rewritten-pct", type=float, default=5.0,
                    help="max %% of cues allowed to be HEAVILY rewritten without "
                         "evidence (default 5)")
    ap.add_argument("--max-dropped", type=int, default=0,
                    help="max cues allowed to disappear silently (default 0)")
    ap.add_argument("--rewrite-threshold", type=float, default=0.6,
                    help="similarity below this counts as a rewrite (default 0.6)")
    ap.add_argument("--report", help="write the full per-cue drift report here")
    args = ap.parse_args()

    raw = {c.start_ms: c for c in parse_srt(args.raw_srt)}
    edited = {c.start_ms: c for c in parse_srt(args.edited_srt)}
    verified = load_evidence(args.evidence)

    # Align by start time: translation/QA must never retime the source, so
    # start_ms is a stable key. A cue whose timing moved reads as dropped
    # + added, which is itself worth surfacing.
    dropped = sorted(set(raw) - set(edited))
    added = sorted(set(edited) - set(raw))
    common = sorted(set(raw) & set(edited))

    unchanged, light, rewritten = [], [], []
    for t in common:
        s = similarity(raw[t].text, edited[t].text)
        rec = {
            "index": edited[t].index,
            "start_ms": t,
            "similarity": round(s, 3),
            "raw": norm(raw[t].text),
            "edited": norm(edited[t].text),
            "evidence": edited[t].index in verified,
        }
        if s > 0.95:
            unchanged.append(rec)
        elif s >= args.rewrite_threshold:
            light.append(rec)
        else:
            rewritten.append(rec)

    total = len(common) or 1
    undocumented = [r for r in rewritten if not r["evidence"]]
    pct_rewritten = len(rewritten) / total * 100
    pct_undocumented = len(undocumented) / total * 100

    print(f"raw cues:    {len(raw)}")
    print(f"edited cues: {len(edited)}")
    print(f"aligned:     {len(common)}")
    print()
    print(f"  unchanged (sim > 0.95):              {len(unchanged):5d}  ({len(unchanged)/total*100:5.1f}%)")
    print(f"  lightly edited ({args.rewrite_threshold}-0.95):          {len(light):5d}  ({len(light)/total*100:5.1f}%)")
    print(f"  REWRITTEN (sim < {args.rewrite_threshold}):              {len(rewritten):5d}  ({pct_rewritten:5.1f}%)")
    print(f"    of which undocumented:             {len(undocumented):5d}  ({pct_undocumented:5.1f}%)")
    print(f"  dropped (vanished from edited):      {len(dropped):5d}")
    print(f"  added (not in raw):                  {len(added):5d}")

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump({
                "raw_srt": args.raw_srt,
                "edited_srt": args.edited_srt,
                "counts": {
                    "raw": len(raw), "edited": len(edited), "aligned": len(common),
                    "unchanged": len(unchanged), "light": len(light),
                    "rewritten": len(rewritten), "undocumented_rewrites": len(undocumented),
                    "dropped": len(dropped), "added": len(added),
                },
                "rewritten": rewritten,
                "lightly_edited": light,
                "dropped_cues": [{"start_ms": t, "text": norm(raw[t].text)} for t in dropped],
            }, f, ensure_ascii=False, indent=1)
        print(f"\nfull report -> {args.report}")

    errors = []
    if pct_undocumented > args.max_rewritten_pct:
        errors.append(
            f"{pct_undocumented:.1f}% of cues were heavily rewritten with no audio evidence "
            f"(limit {args.max_rewritten_pct}%). These edits are guesses unless a "
            f"re-transcription says otherwise."
        )
    if len(dropped) > args.max_dropped:
        errors.append(
            f"{len(dropped)} cues disappeared (limit {args.max_dropped}). Dialogue that was "
            f"heard must not silently vanish — drop it explicitly or keep it."
        )

    if errors:
        print("\nFAILED — the transcript has drifted from what was actually heard:")
        for e in errors:
            print(f"  X {e}")
        print("\nFix by doing ONE of these for each flagged cue:")
        print("  1. Re-transcribe that span from audio (retranscribe_spans.py) and")
        print("     record it in the --evidence file. This is the preferred move.")
        print("  2. Restore the raw ASR text and mark the cue unclear for review.")
        print("  3. Ask the user what is said there.")
        print("Do NOT resolve it by writing what the line 'probably' was.")
        if undocumented:
            print(f"\nFirst undocumented rewrites (of {len(undocumented)}):")
            for r in undocumented[:10]:
                print(f"  #{r['index']} sim={r['similarity']}")
                print(f"     heard:   {r['raw'][:90]}")
                print(f"     written: {r['edited'][:90]}")
        return 1

    print("\nPASSED — edits are within limits or backed by audio evidence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
