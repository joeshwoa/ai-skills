#!/usr/bin/env python3
"""Check a reel spec before it is rendered or shown to the user.

    python3 scripts/validate_script.py spec.json [--json] [--today YYYY-MM-DD] [--strict]

Exit 0 = no errors (warnings may exist), 1 = errors, 2 = unreadable spec.
--strict turns warnings into errors (use before final delivery).

ERRORS (must fix): missing scope/audience/goal/platforms, no scenes, unknown block types, no hook
in the first 3 seconds, no CTA (unless brief.cta == "none" for a pure-awareness piece),
runtime more than 25% outside the target, placeholders left in, caption/title over a platform's
hard limit.
WARNINGS (fix or consciously accept): runtime 10–25% off, a long first line, very long sentences,
long on-screen text, Modern-Standard words in an Egyptian-dialect script, script language that
doesn't match the declared language, unprovable claims, engagement bait, stale or undated trend
references, too many hashtags for a platform, trending audio on a business account.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reelspec import (BLOCK_TYPES, CHARS_PER_SEC, RTL_LANGS, WORDS_PER_SEC, DEFAULT_WPS, SpecError,  # noqa: E402
                      as_list, base_lang, count_units, estimate_scene_seconds, has_rtl_chars, is_egyptian,
                      line_text, load_brand, load_json, safe_lines, scene_has_words, spoken_lines, target_range)

PLATFORMS = {
    # caption/title limits are hard; hashtag numbers are guidance (Instagram's 5 is a post limit —
    # verify live). Soft guidance lives in references/platforms.md.
    "instagram_reels": {"caption": 2200, "hashtags_warn": 5,
                        "hashtag_note": "Instagram limits posts to 5 hashtags (late 2025 — verify live)"},
    "tiktok": {"caption": 4000, "hashtags_warn": 6, "hashtag_note": "TikTok: a few specific tags beat many generic ones"},
    "youtube_shorts": {"caption": 5000, "title": 100, "hashtags_warn": 3,
                       "hashtag_note": "YouTube shows only the first 3 above the title"},
    "facebook_reels": {"caption": 63206, "hashtags_warn": 5, "hashtag_note": "Facebook: hashtags matter little"},
    "linkedin": {"caption": 3000, "hashtags_warn": 5, "hashtag_note": "LinkedIn: 3–5 professional tags"},
    "snapchat_spotlight": {"caption": 160, "hashtags_warn": 3, "hashtag_note": "Spotlight captions are tiny"},
    "x": {"caption": 280, "hashtags_warn": 2, "hashtag_note": "X: 1–2 tags"},
    "threads": {"caption": 500, "hashtags_warn": 1, "hashtag_note": "Threads allows one topic tag"},
}

REQUIRED_BRIEF = ["platforms", "audience", "goal"]
PLACEHOLDER_RE = re.compile(r"\{\{|\}\}|\bTODO\b|\bTBD\b|\bFIXME\b|\bXXX\b|(?i:lorem ipsum)|؟؟؟")
SKIP_PLACEHOLDER_KEYS = {"about", "template"}

TASHKEEL = re.compile(r"[ً-ْٰـ]")
# MSA words that rarely belong in natural spoken Egyptian Arabic, with the Egyptian equivalent.
MSA_MARKERS = {
    "سوف": "هـ (هيعمل)", "لماذا": "ليه", "ماذا": "إيه", "هذا": "ده", "هذه": "دي", "هؤلاء": "دول",
    "الذي": "اللي", "التي": "اللي", "الذين": "اللي", "لكي": "عشان", "ليس": "مش", "ليست": "مش",
    "لن": "مش هـ", "أيضا": "كمان / برضه", "جدا": "أوي", "الآن": "دلوقتي", "كيف": "إزاي",
    "متى": "إمتى", "أين": "فين", "يجب": "لازم", "نحن": "إحنا", "أنتم": "إنتو", "لقد": "(drop it)",
    "إنني": "أنا", "لدينا": "عندنا", "لديك": "عندك",
}
PREFIXES = ("و", "ف", "ل", "ب", "ك", "وب", "ول", "فل")

CLAIM_RE = re.compile(r"(guarantee|guaranteed|100\s?%|#1\b|number one|best in the world|risk[- ]free|"
                      r"مضمون|ضمان|١٠٠٪|100٪|الأفضل في العالم|الأول في مصر|رقم ١|رقم 1|أكيد هتكسب|هتكسب آلاف)", re.I)
BAIT_RE = re.compile(r"(comment ['\"]?yes|type ['\"]?yes|tag (3|three|5|five) friends|like if|share if|"
                     r"اكتب تم|اكتب نعم|منشن \d|منشن (تلات|خمس)|لايك لو|شير لو)", re.I)


def add(lst, level, where, msg):
    lst.append({"level": level, "where": where, "msg": msg})


def walk_strings(node, path="spec"):
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for k, v in node.items():
            if k in SKIP_PLACEHOLDER_KEYS:
                continue
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_strings(v, f"{path}[{i}]")


def msa_hits(text: str):
    words = re.findall(r"[؀-ۿ]+", TASHKEEL.sub("", text))
    words = [w.replace("أيضاً", "أيضا").replace("جداً", "جدا") for w in words]
    for w in words:
        cands = [w] + [w[len(p):] for p in PREFIXES if w.startswith(p) and len(w) - len(p) >= 2]
        for c in cands:  # the whole word first, so لماذا is not reported as ماذا
            if c in MSA_MARKERS:
                yield c
                break


def validate(spec: dict, today: dt.date) -> list:
    out = []
    if not isinstance(spec, dict):
        add(out, "error", "spec", "the spec must be a JSON object")
        return out
    lang = spec.get("language")
    if not lang:
        add(out, "error", "language", "set spec.language (e.g. ar-EG, en-US, ar-SA, fr-FR)")
        lang = "en"
    b = base_lang(lang)
    brief = spec.get("brief") if isinstance(spec.get("brief"), dict) else {}
    wps = brief.get("words_per_sec")

    # --- placeholders anywhere (a template is refused until every blank is filled)
    seen = set()
    for path, text in walk_strings(spec):
        if PLACEHOLDER_RE.search(text) and path not in seen:
            seen.add(path)
            add(out, "error", path, f"placeholder left in: {text[:60]}")

    # --- scope & audience: the user asked for these to be settled before writing
    for k in REQUIRED_BRIEF:
        if not brief.get(k):
            add(out, "error", f"brief.{k}", f"brief.{k} is missing — confirm scope and audience with the user first")
    if not brief.get("duration_sec"):
        add(out, "warning", "brief.duration_sec", "no target duration — runtime can't be checked")
    plats = as_list(brief.get("platforms"))
    for p in plats:
        if p not in PLATFORMS:
            add(out, "warning", "brief.platforms", f"unknown platform '{p}' (known: {', '.join(PLATFORMS)})")

    if not spec.get("title"):
        add(out, "error", "title", "missing title")
    scenes = spec.get("scenes") or []
    if not isinstance(scenes, list) or not scenes:
        add(out, "error", "scenes", "no scenes")
        return out

    # --- structure
    good_scenes = []
    for i, sc in enumerate(scenes):
        if not isinstance(sc, dict):
            add(out, "error", f"scenes[{i}]", "a scene must be an object with title and blocks")
            continue
        good_scenes.append(sc)
        where = sc.get("title") or f"scene {i + 1}"
        blocks = sc.get("blocks") or []
        if not blocks:
            add(out, "error", where, "scene has no blocks")
        for bl in blocks:
            if not isinstance(bl, dict):
                add(out, "error", where, f"a block must be an object, got {bl!r:.40}")
                continue
            t = bl.get("type")
            if t not in BLOCK_TYPES:
                add(out, "error", where, f"unknown block type '{t}' (allowed: {', '.join(BLOCK_TYPES)})")
                continue
            if not bl.get("lines"):
                add(out, "error", where, f"{t} block has no lines")
            for item in as_list(bl.get("lines")):
                try:
                    line_text(item)
                except SpecError as e:
                    add(out, "error", where, str(e))
    scenes = good_scenes

    # --- hook in the first ~3 seconds: something said or written on screen
    t, hook_at = 0.0, None
    for i, sc in enumerate(scenes):
        if scene_has_words(sc):
            hook_at = t
            break
        if i == 0 and not isinstance(sc.get("duration_sec"), (int, float)) and not sc.get("duration"):
            add(out, "warning", sc.get("title") or "scene 1",
                "opening scene has no words and no duration — set duration_sec so the hook timing can be checked")
        t += estimate_scene_seconds(sc, lang, wps)
    if hook_at is None:
        add(out, "error", "hook", "nothing is said or shown as text — a reel needs a spoken or on-screen hook")
    elif hook_at > 3.0:
        add(out, "error", "hook", f"first words/on-screen text arrive at ~{hook_at:.1f}s — the hook must land in the first 3 s")

    first = next(iter(spoken_lines({"scenes": scenes})), None)
    if first:
        n = count_units(first[2], lang)
        rate = CHARS_PER_SEC.get(b) or wps or WORDS_PER_SEC.get(b, DEFAULT_WPS)
        limit = int(rate * 6)  # hooks are said briskly; past ~6 s of words the stop-scroll part is buried
        if n > limit:
            add(out, "warning", "hook", f"first spoken line is {n} {'characters' if b in CHARS_PER_SEC else 'words'} "
                                        f"(~{n / rate:.0f} s) — split it so the stop-scrolling words land in the first "
                                        f"~3 s (≈ {int(rate * 3)} words): “{first[2][:60]}”")

    # --- runtime vs target
    total = sum(estimate_scene_seconds(sc, lang, wps) for sc in scenes)
    rng = target_range(spec)
    if rng:
        lo, hi = rng
        if total < lo * 0.75 or total > hi * 1.25:
            add(out, "error", "runtime", f"estimated {total:.0f}s vs target {lo:.0f}–{hi:.0f}s (>25% off) — cut or add lines")
        elif total < lo * 0.9 or total > hi * 1.1:
            add(out, "warning", "runtime", f"estimated {total:.0f}s vs target {lo:.0f}–{hi:.0f}s")

    # --- line-level language checks
    for si, block, text in spoken_lines({"scenes": scenes}):
        where = scenes[si].get("title") or f"scene {si + 1}"
        if b not in CHARS_PER_SEC and count_units(text, lang) > 30:
            add(out, "warning", where, f"long sentence ({count_units(text, lang)} words) — split it so the talent can breathe")
        if b == "ar" and not has_rtl_chars(text) and len(text) > 25:
            add(out, "warning", where, f"Arabic script but this line has no Arabic: “{text[:50]}”")
        if b not in RTL_LANGS and has_rtl_chars(text):
            add(out, "warning", where, f"declared {lang} but the line contains Arabic/Hebrew script: “{text[:50]}”")
        if is_egyptian(lang):
            for m in sorted(set(msa_hits(text))):
                add(out, "warning", where, f"MSA word '{m}' in an Egyptian-dialect line → Egyptian: {MSA_MARKERS[m]}: “{text[:50]}”")
        if CLAIM_RE.search(text):
            add(out, "warning", where, f"claim needs proof or softening: “{text[:60]}”")
        if BAIT_RE.search(text):
            add(out, "warning", where, f"engagement bait — Meta/TikTok demote it; ask a real question instead: “{text[:60]}”")

    for sc in scenes:
        for bl in sc.get("blocks") or []:
            if isinstance(bl, dict) and bl.get("type") == "onscreen_text":
                for _, text in safe_lines(bl):
                    if len(text) > 60:
                        add(out, "warning", sc.get("title", ""), f"on-screen text is {len(text)} chars — keep it ≤ ~60 (≈ 7 words)")

    # --- CTA: declared in the brief AND delivered near the end
    cta = brief.get("cta")
    if not cta:
        add(out, "error", "cta", "no CTA — set brief.cta (or \"none\" for a deliberate no-ask awareness piece) and script it")
    elif str(cta).strip().lower() != "none":
        tail = scenes[-2:]
        delivered = any(scene_has_words(sc) for sc in tail) or bool((spec.get("end_frame") or {}) if isinstance(spec.get("end_frame"), dict) else spec.get("end_frame"))
        if not delivered:
            add(out, "warning", "cta", f"brief.cta is '{cta}' but the last scenes say/show nothing — script the ask")

    # --- trends must be dated and fresh
    for i, tr in enumerate(as_list(brief.get("trend_refs"))):
        if not isinstance(tr, dict):
            add(out, "error", f"brief.trend_refs[{i}]", "each trend ref must be an object {name, kind, source, checked}")
            continue
        name = tr.get("name", "?")
        if tr.get("kind") == "audio" and brief.get("account_type") == "business":
            add(out, "warning", "trend_refs", f"trending sound '{name}' on a business account — usually not licensed for "
                                              "commercial use; use the platform's commercial library or original audio")
        if not tr.get("checked"):
            add(out, "warning", "trend_refs", f"trend '{name}' has no 'checked' date — verify it live before shooting")
            continue
        try:
            age = (today - dt.date.fromisoformat(str(tr["checked"]))).days
        except ValueError:
            add(out, "warning", "trend_refs", f"trend '{name}': bad date '{tr['checked']}' (use YYYY-MM-DD)")
            continue
        if age > 14:
            add(out, "warning", "trend_refs", f"trend '{name}' checked {age} days ago — trends burn out in 1–3 weeks, re-check")

    # --- posting pack
    posting = spec.get("posting") if isinstance(spec.get("posting"), dict) else {}
    cap = str(posting.get("caption") or "")
    tags = as_list(posting.get("hashtags"))
    if len(tags) == 1 and isinstance(tags[0], str) and " " in tags[0].strip():
        tags = tags[0].split()
    for p in plats:
        lim = PLATFORMS.get(p)
        if not lim:
            continue
        if cap and len(cap) > lim["caption"]:
            add(out, "error", "posting.caption", f"{len(cap)} chars > {p} limit {lim['caption']}")
        if lim.get("title") and posting.get("title") and len(str(posting["title"])) > lim["title"]:
            add(out, "error", "posting.title", f"title over {p} limit {lim['title']}")
        if len(tags) > lim["hashtags_warn"]:
            add(out, "warning", "posting.hashtags", f"{len(tags)} hashtags for {p} — {lim['hashtag_note']}")
    if CLAIM_RE.search(cap):
        add(out, "warning", "posting.caption", "caption makes a claim that needs proof")
    if BAIT_RE.search(cap):
        add(out, "warning", "posting.caption", "caption uses engagement bait")
    if not posting:
        add(out, "warning", "posting", "no posting pack (cover text, caption, hashtags, A/B hooks)")
    elif not posting.get("alt_hooks"):
        add(out, "warning", "posting.alt_hooks", "no alternative hooks to A/B test")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--today")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args(argv)
    try:
        spec = load_json(a.spec)
        if spec.get("brand"):
            load_brand(spec["brand"])
    except (OSError, json.JSONDecodeError, SpecError) as e:
        print(f"error: cannot read spec: {e}", file=sys.stderr)
        return 2
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    try:
        issues = validate(spec, today)
    except Exception as e:  # a spec shape nobody anticipated: report it, don't traceback
        issues = [{"level": "error", "where": "spec", "msg": f"could not check the spec ({type(e).__name__}: {e}) — "
                                                            "compare it with references/spec-schema.md"}]
    lang = spec.get("language") or "en"
    brief = spec.get("brief") if isinstance(spec.get("brief"), dict) else {}
    total = sum(estimate_scene_seconds(sc, lang, brief.get("words_per_sec"))
                for sc in (spec.get("scenes") if isinstance(spec.get("scenes"), list) else []))
    errors = [i for i in issues if i["level"] == "error"]
    warns = [i for i in issues if i["level"] == "warning"]
    if a.json:
        print(json.dumps({"ok": not errors and not (a.strict and warns), "estimated_seconds": round(total, 1),
                          "errors": errors, "warnings": warns}, ensure_ascii=False, indent=2))
    else:
        for i in issues:
            print(f"{i['level'].upper():7} [{i['where']}] {i['msg']}")
        print(f"estimated runtime {total:.0f}s — {len(errors)} error(s), {len(warns)} warning(s)")
    return 1 if errors or (a.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
