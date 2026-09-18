#!/usr/bin/env python3
"""
batch_for_translation.py — turn a source SRT into a translation work order.

This writes a JSON file listing the dialogue in batches (with a little
surrounding context per batch — see srt_utils.batch_cues) for the AGENT
itself to translate, one batch at a time, following
references/translation_workflow.md. This script does NOT translate
anything — deliberately: a mechanical translation library is exactly what
produces the flat, literal output the skill exists to avoid.

Usage:
    python3 batch_for_translation.py source.srt work_order.json \
        --batch-size 25 --context 3

The agent then reads work_order.json, and for each batch, writes back a
sibling file (or a growing list) of {"index": N, "translated": "..."}
objects — see apply_translation.py for the exact shape it expects.
"""
from __future__ import annotations

import argparse
import json

from srt_utils import parse_srt, batch_cues, cues_to_translation_json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source_srt")
    ap.add_argument("out_json")
    ap.add_argument("--batch-size", type=int, default=25)
    ap.add_argument("--context", type=int, default=3)
    args = ap.parse_args()

    cues = parse_srt(args.source_srt)
    if not cues:
        raise SystemExit(f"No cues parsed from {args.source_srt} — is it a valid SRT?")

    batches = batch_cues(cues, batch_size=args.batch_size, context=args.context)
    payload = cues_to_translation_json(cues, batches)

    with open(args.out_json, "w", encoding="utf-8") as f:
        f.write(payload)

    data = json.loads(payload)
    print(f"{len(cues)} cues -> {len(data['batches'])} batches -> {args.out_json}")
    print(
        "Next: translate each batch's \"translate\" list following "
        "references/translation_workflow.md (four passes: literal draft -> "
        "meaning-preserving rewrite -> cultural adaptation -> fluency/timing "
        "polish), collect {\"index\": N, \"translated\": \"...\"} for every "
        "cue, then run apply_translation.py."
    )


if __name__ == "__main__":
    main()
