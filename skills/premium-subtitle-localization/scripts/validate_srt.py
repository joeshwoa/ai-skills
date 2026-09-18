#!/usr/bin/env python3
"""
validate_srt.py — the automated "tester" for a subtitle file.

This is a mechanical QA pass: everything here is a checkable rule, not a
judgment call. It catches the class of bug that looks fine in a glance and
then breaks playback or readability — overlapping cues, subtitles that
flash by faster than a human can read, lines too long for the screen, a
cue count that silently dropped lines during translation.

It does NOT check translation quality/meaning — that is a judgment call
for the agent's own review pass (see references/qa_review_checklist.md).
This script and that checklist are two different kinds of test, on
purpose, the same way premium-presentations' validate_deck.py (layout) is
paired with a human-style visual review (content).

Usage:
    python3 validate_srt.py translated.srt --lang ru [--source original.srt]

Exit code is non-zero only on a HARD error (something actually broken).
Reading-speed / length issues are WARNINGS by default (some are
unavoidable for verbose target languages) unless --strict is passed.
"""
from __future__ import annotations

import argparse
import sys

from srt_utils import parse_srt, Cue

# Rough safe reading speeds in characters-per-second. Subtitle convention
# varies by language density; these are deliberately conservative defaults
# used by professional subtitling houses (Netflix-style guidelines land in
# this range). Add more languages here as the skill is used on them.
CPS_BY_LANG = {
    "en": 20, "ar": 18, "ru": 19, "de": 18, "fr": 19, "es": 19,
    "it": 19, "pt": 19, "tr": 19, "ja": 6,  # CJK counted in characters, not phonemes
    "zh": 6, "ko": 7, "default": 18,
}
MIN_DURATION_MS = 700       # a cue on screen for less than this is unreadable
MAX_LINES = 2
MAX_CHARS_PER_LINE = 42     # classic subtitling limit; loosened per-language below
MAX_CHARS_PER_LINE_BY_LANG = {"de": 44, "ru": 44, "ja": 16, "zh": 16, "ko": 18}
MIN_GAP_MS = 80              # minimum gap between consecutive cues (avoid flicker)


def check(cues: list[Cue], lang: str, strict: bool, source_count: int | None):
    errors: list[str] = []
    warnings: list[str] = []

    if not cues:
        errors.append("File has zero cues — nothing parsed.")
        return errors, warnings

    if source_count is not None and len(cues) != source_count:
        errors.append(
            f"Cue count mismatch: source had {source_count}, this file has "
            f"{len(cues)}. Lines were dropped or merged during translation — "
            f"every source cue must produce exactly one translated cue "
            f"(split only the TEXT across lines within a cue, never merge "
            f"two source cues into one, or timing/sync breaks)."
        )

    cps_limit = CPS_BY_LANG.get(lang, CPS_BY_LANG["default"])
    max_chars = MAX_CHARS_PER_LINE_BY_LANG.get(lang, MAX_CHARS_PER_LINE)

    prev = None
    for c in cues:
        loc = f"cue #{c.index} ({c.text[:30]!r}...)" if len(c.text) > 30 else f"cue #{c.index} ({c.text!r})"

        if c.end_ms <= c.start_ms:
            errors.append(f"{loc}: end time is not after start time.")
        elif c.duration_ms < MIN_DURATION_MS:
            warnings.append(
                f"{loc}: on screen for only {c.duration_ms}ms "
                f"(< {MIN_DURATION_MS}ms) — likely unreadable."
            )

        if not c.text.strip():
            errors.append(f"cue #{c.index}: empty text.")

        lines = c.lines
        if len(lines) > MAX_LINES:
            warnings.append(f"{loc}: {len(lines)} lines (max recommended {MAX_LINES}).")
        for li, line in enumerate(lines, start=1):
            if len(line) > max_chars:
                warnings.append(
                    f"{loc}: line {li} is {len(line)} chars "
                    f"(recommended max {max_chars} for lang={lang})."
                )

        char_count = len(c.text.replace("\n", " "))
        if c.duration_ms > 0:
            cps = char_count / (c.duration_ms / 1000)
            if cps > cps_limit:
                msg = (
                    f"{loc}: reading speed {cps:.1f} cps "
                    f"(recommended max {cps_limit} for lang={lang}) — "
                    f"text may be too long for the time available."
                )
                (errors if strict else warnings).append(msg)

        if prev is not None:
            if c.start_ms < prev.end_ms:
                errors.append(
                    f"cue #{c.index} overlaps cue #{prev.index} "
                    f"(starts at {c.start_ms}ms, previous ends at {prev.end_ms}ms)."
                )
            elif c.start_ms - prev.end_ms < MIN_GAP_MS:
                warnings.append(
                    f"cue #{c.index}: only {c.start_ms - prev.end_ms}ms gap "
                    f"after cue #{prev.index} (recommended >= {MIN_GAP_MS}ms)."
                )
        prev = c

    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("srt_path")
    ap.add_argument("--lang", default="default", help="target language code, e.g. ru, ar, en")
    ap.add_argument("--source", help="original-language SRT, to cross-check cue count")
    ap.add_argument("--strict", action="store_true", help="treat reading-speed overruns as errors")
    args = ap.parse_args()

    cues = parse_srt(args.srt_path)
    source_count = len(parse_srt(args.source)) if args.source else None

    errors, warnings = check(cues, args.lang, args.strict, source_count)

    print(f"Checked {len(cues)} cues in {args.srt_path} (lang={args.lang})")
    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  ! {w}")
    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  X {e}")
        print("\nFAILED — fix the errors above before merging into the video.")
        sys.exit(1)

    print("\nPASSED" + (" (with warnings above — review them)" if warnings else " — clean."))
    sys.exit(0)


if __name__ == "__main__":
    main()
