#!/usr/bin/env python3
"""
srt_utils.py — dependency-free SRT parsing, writing, and batching.

Deliberately pure-stdlib (no `srt`/`pysrt` package): this skill has to run
on whatever machine the agent is on (Cursor/Antigravity/Claude/GPT boxes),
and the third-party `srt` package fails to build in some sandboxed
environments (old setuptools `install_layout` bug). SRT's format is simple
enough that a ~100-line parser is more portable than a dependency.

Core objects:
    Cue(index, start_ms, end_ms, text) — text is the raw multi-line string,
    '\n'-joined, exactly as it should appear on screen (no HTML tags added).

Functions:
    parse_srt(path_or_text) -> list[Cue]
    write_srt(cues, path)
    ms_to_srt_time(ms) / srt_time_to_ms(ts)
    batch_cues(cues, batch_size, context) -> list[Batch]
        Groups cues into translation batches, each carrying a few cues of
        *context* before/after so the translator (a human or an LLM) can
        see setup/payoff across a joke instead of translating lines blind.
"""
from __future__ import annotations

import glob
import json
import os
import re
from dataclasses import dataclass, field, asdict

_TIME_RE = re.compile(
    r"(\d{1,2}):(\d{2}):(\d{2})[,.](\d{1,3})"
)
_BLOCK_SPLIT_RE = re.compile(r"\r?\n\r?\n+")


@dataclass
class Cue:
    index: int
    start_ms: int
    end_ms: int
    text: str  # '\n'-joined lines, as displayed

    @property
    def duration_ms(self) -> int:
        return self.end_ms - self.start_ms

    @property
    def lines(self) -> list[str]:
        return self.text.split("\n")


@dataclass
class Batch:
    batch_id: int
    # cues the translator must actually translate this batch
    target_indices: list[int]
    # cues included only so the translator can see surrounding dialogue —
    # do NOT re-translate these, they belong to the neighboring batch
    context_before_indices: list[int] = field(default_factory=list)
    context_after_indices: list[int] = field(default_factory=list)


def srt_time_to_ms(ts: str) -> int:
    m = _TIME_RE.search(ts)
    if not m:
        raise ValueError(f"Not a valid SRT timestamp: {ts!r}")
    h, mnt, s, frac = m.groups()
    frac = (frac + "000")[:3]  # pad/truncate to milliseconds
    return (
        int(h) * 3_600_000
        + int(mnt) * 60_000
        + int(s) * 1_000
        + int(frac)
    )


def ms_to_srt_time(ms: int) -> str:
    if ms < 0:
        ms = 0
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1_000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def parse_srt(path_or_text: str) -> list[Cue]:
    """Accepts a filesystem path or raw SRT text directly."""
    if os.path.exists(path_or_text):
        with open(path_or_text, "r", encoding="utf-8-sig") as f:
            raw = f.read()
    else:
        raw = path_or_text

    raw = raw.replace("\r\n", "\n").strip("﻿ \n")
    if not raw.strip():
        return []

    cues: list[Cue] = []
    for block in _BLOCK_SPLIT_RE.split(raw):
        block = block.strip()
        if not block:
            continue
        lines = block.split("\n")
        # line 0 is normally the numeric index, but be tolerant of files
        # that are missing it (some export tools drop it) — detect by
        # whether line 0 or line 1 contains the "-->" arrow.
        if "-->" in lines[0]:
            idx_line, time_line, text_lines = None, lines[0], lines[1:]
        elif len(lines) > 1 and "-->" in lines[1]:
            idx_line, time_line, text_lines = lines[0], lines[1], lines[2:]
        else:
            # not a real cue block (stray blank block) — skip
            continue

        start_s, end_s = [p.strip() for p in time_line.split("-->")]
        start_ms = srt_time_to_ms(start_s)
        end_ms = srt_time_to_ms(end_s)
        text = "\n".join(text_lines).strip("\n")

        try:
            index = int(idx_line) if idx_line is not None else len(cues) + 1
        except ValueError:
            index = len(cues) + 1

        cues.append(Cue(index=index, start_ms=start_ms, end_ms=end_ms, text=text))

    # re-number sequentially — guards against gaps/duplicates in the source
    for i, c in enumerate(cues, start=1):
        c.index = i
    return cues


def write_srt(cues: list[Cue], path: str) -> None:
    lines = []
    for c in cues:
        lines.append(str(c.index))
        lines.append(f"{ms_to_srt_time(c.start_ms)} --> {ms_to_srt_time(c.end_ms)}")
        lines.append(c.text)
        lines.append("")  # blank line separator
    content = "\n".join(lines).rstrip("\n") + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def find_subtitle_candidates(video_path: str) -> list[str]:
    """Look in the video's own directory (non-recursive) for .srt/.vtt/.ass
    files — the common places a downloaded/ripped movie already ships one."""
    directory = os.path.dirname(os.path.abspath(video_path)) or "."
    candidates = []
    for ext in ("srt", "vtt", "ass", "ssa"):
        candidates.extend(glob.glob(os.path.join(directory, f"*.{ext}")))
    return sorted(candidates)


def batch_cues(cues: list[Cue], batch_size: int = 25, context: int = 3) -> list[Batch]:
    """Split cues into translation batches with overlap context.

    batch_size=25, context=3 means: translate 25 lines at a time, but show
    the translator the 3 cues before and after so jokes with setup/payoff
    spanning a batch boundary, or a callback to an earlier line, don't get
    mistranslated in isolation.
    """
    n = len(cues)
    batches = []
    bid = 0
    i = 0
    while i < n:
        j = min(i + batch_size, n)
        target = [c.index for c in cues[i:j]]
        before = [c.index for c in cues[max(0, i - context):i]]
        after = [c.index for c in cues[j:min(n, j + context)]]
        batches.append(
            Batch(batch_id=bid, target_indices=target,
                  context_before_indices=before, context_after_indices=after)
        )
        bid += 1
        i = j
    return batches


def cues_to_translation_json(cues: list[Cue], batches: list[Batch]) -> str:
    """Serialize cues + batch plan into the JSON an agent (or a human) reads
    to produce translations. This is what scripts/batch_for_translation.py
    writes to disk."""
    by_index = {c.index: c for c in cues}
    out = {
        "cue_count": len(cues),
        "batches": [],
    }
    for b in batches:
        out["batches"].append({
            "batch_id": b.batch_id,
            "context_before": [
                {"index": i, "text": by_index[i].text} for i in b.context_before_indices
            ],
            "translate": [
                {
                    "index": i,
                    "text": by_index[i].text,
                    "duration_ms": by_index[i].duration_ms,
                }
                for i in b.target_indices
            ],
            "context_after": [
                {"index": i, "text": by_index[i].text} for i in b.context_after_indices
            ],
        })
    return json.dumps(out, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 srt_utils.py <file.srt>  (self-test: parse, re-write, re-parse, diff)")
        sys.exit(1)
    path = sys.argv[1]
    cues = parse_srt(path)
    print(f"Parsed {len(cues)} cues from {path}")
    tmp = path + ".roundtrip.srt"
    write_srt(cues, tmp)
    cues2 = parse_srt(tmp)
    ok = len(cues) == len(cues2) and all(
        (a.start_ms, a.end_ms, a.text) == (b.start_ms, b.end_ms, b.text)
        for a, b in zip(cues, cues2)
    )
    print("Round-trip OK" if ok else "ROUND-TRIP MISMATCH")
    os.remove(tmp)
