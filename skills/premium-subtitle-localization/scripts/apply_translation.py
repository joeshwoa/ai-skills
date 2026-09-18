#!/usr/bin/env python3
"""
apply_translation.py — reassemble agent-translated text into a real SRT.

Takes the ORIGINAL srt (for authoritative timing — translation must never
silently shift sync) and a JSON file of translated cues, and writes the
final target-language SRT.

Expected translations JSON — a flat array, one entry per source cue:
    [
      {"index": 1, "text": "Привет, дружище", "note": "informal register kept"},
      {"index": 2, "text": "..."},
      ...
    ]
"note" is optional free text the translator (agent) can leave — e.g. "this
joke was adapted, not literal: source pun on X, target pun on Y". Notes are
never written into the SRT itself; they're collected into a sidecar
`<output>.notes.json` / printed for the human, so a reviewer can see what
was deliberately changed without it leaking onto the screen.

Usage:
    python3 apply_translation.py original.srt translations.json output.srt
"""
from __future__ import annotations

import argparse
import json
import sys

from srt_utils import parse_srt, write_srt, Cue


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("original_srt")
    ap.add_argument("translations_json")
    ap.add_argument("output_srt")
    args = ap.parse_args()

    source_cues = parse_srt(args.original_srt)
    with open(args.translations_json, "r", encoding="utf-8") as f:
        translations = json.load(f)

    by_index = {}
    for t in translations:
        idx = t["index"]
        if idx in by_index:
            raise SystemExit(f"Duplicate translation entry for cue #{idx}.")
        by_index[idx] = t

    missing = [c.index for c in source_cues if c.index not in by_index]
    if missing:
        raise SystemExit(
            f"Missing translations for {len(missing)} cue(s): {missing[:20]}"
            + (" ..." if len(missing) > 20 else "")
            + "\nEvery source cue needs a translated entry — partial output "
              "will desync the rest of the file."
        )

    out_cues = []
    notes = {}
    for c in source_cues:
        t = by_index[c.index]
        text = t["text"].strip()
        if not text:
            raise SystemExit(f"cue #{c.index}: translated text is empty.")
        out_cues.append(Cue(index=c.index, start_ms=c.start_ms, end_ms=c.end_ms, text=text))
        if t.get("note"):
            notes[c.index] = t["note"]

    write_srt(out_cues, args.output_srt)
    print(f"Wrote {len(out_cues)} cues -> {args.output_srt}")

    if notes:
        notes_path = args.output_srt + ".notes.json"
        with open(notes_path, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
        print(f"{len(notes)} adaptation note(s) -> {notes_path} (for review, not shipped in the SRT)")

    print(
        "Next: python3 validate_srt.py "
        f"{args.output_srt} --lang <target> --source {args.original_srt}"
    )


if __name__ == "__main__":
    main()
