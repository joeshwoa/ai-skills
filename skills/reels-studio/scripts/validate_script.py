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
                      line_text, load_brand, load_json, safe_lines, scene_has_words, spoken_lines, target_range,
                      CONTENT_TYPES, content_type, scene_starts, cut_scene_indices, speech_seconds)

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
    "youtube": {"caption": 5000, "title": 100, "hashtags_warn": 5,
                "hashtag_note": "YouTube shows 3 above the title and ignores all of them past 60"},
    "facebook": {"caption": 63206, "hashtags_warn": 5, "hashtag_note": "Facebook: hashtags matter little"},
    "website": {"caption": 100000, "hashtags_warn": 0, "hashtag_note": "no hashtags on a website/landing page"},
    "tv": {"caption": 100000, "hashtags_warn": 0, "hashtag_note": "no hashtags on TV"},
}

# Ad placements: hard maximum length in seconds where the platform fixes one (verify live).
PLACEMENTS = {
    "youtube_skippable": None, "youtube_non_skippable": 15, "youtube_bumper": 6, "youtube_shorts_ad": None,
    "youtube_infeed": None, "meta_feed": None, "meta_reels": None, "meta_stories": None,
    "tiktok_infeed": None, "tiktok_topview": None, "snapchat_ad": 180, "linkedin_video": None,
    "x_video": None, "tv_spot": None, "ctv": None, "cinema": None, "ooh_digital": None,
}
# Meta's "personal attributes" policy: ads may not assert or imply the viewer's health, finances,
# religion, ethnicity, sexuality, etc. ("Are you overweight?"). Heuristic — the reviewer decides.
PERSONAL_ATTR_RE = re.compile(
    r"(\b(are you|you're|you are) (overweight|fat|broke|in debt|depressed|anxious|diabetic|single|divorced|gay|"
    r"muslim|christian|bald|infertile|unemployed)\b|"
    r"(إنت|انت|إنتي|انتي|حضرتك) (تخين|تخينة|مديون|مديونة|مكتئب|مكتئبة|عندك سكر|عانس|مطلق|مطلقة|أصلع|عاطل|عاطلة|مفلس))", re.I)

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


GREETING_RE = re.compile(r"^\W*(hi|hey|hello)[\s,]+(guys|everyone|all|friends)(?=[\s,.!:]|$)|^\W*welcome back\b|"
                         r"^\W*(أهلا|أهلاً|اهلا|اهلاً|مرحبا|مرحباً|السلام عليكم|إزيكم|ازيكم)(?![\u0621-\u064A])", re.I)


VISIBLE = ("visual", "graphic", "super", "broll", "lower_third", "onscreen_text", "camera")
LOGO_RE = re.compile(r"\blogo\b|لوجو|شعار", re.I)
NO_LOGO_RE = re.compile(r"\bno logo\b|without (the |a )?logo|من غير (ال)?لوجو|بدون (ال)?لوجو", re.I)


def brand_seen_early(scenes, starts, brand, lang, wps, window=5.0) -> bool:
    """Brand said or shown before `window` seconds: visible blocks of scenes that start in the window,
    and spoken lines whose own start time (accumulated inside the scene) is in the window."""
    b = brand.lower()
    for i, sc in enumerate(scenes):
        if starts[i] >= window:
            break
        t = starts[i]
        for bl in sc.get("blocks") or []:
            if not isinstance(bl, dict):
                continue
            if bl.get("type") in VISIBLE:
                for _, text in safe_lines(bl):
                    if b in text.lower() or (LOGO_RE.search(text) and not NO_LOGO_RE.search(text)):
                        return True
        for bl in sc.get("blocks") or []:
            if isinstance(bl, dict) and bl.get("type") in ("dialogue", "voiceover", "question"):
                for kind, text in safe_lines(bl):
                    if t >= window:
                        break
                    if kind == "line" and b in text.lower():
                        return True
                    t += speech_seconds(text, lang, wps) if kind == "line" else (0.6 if kind == "pause" else 0)
    return False


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
    ctype = content_type(spec)
    if ctype not in CONTENT_TYPES:
        add(out, "error", "brief.content_type", f"unknown content_type '{ctype}' (use {', '.join(CONTENT_TYPES)})")
        ctype = "reel"
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
    hook_limit = 10.0 if ctype == "long_form" else 3.0
    if hook_at is None:
        add(out, "error", "hook", "nothing is said or shown as text — the video needs a spoken or on-screen hook")
    elif hook_at > hook_limit:
        add(out, "error", "hook", f"first words/on-screen text arrive at ~{hook_at:.1f}s — the hook must land in the "
                                  f"first {hook_limit:.0f} s")

    first = next(iter(spoken_lines({"scenes": scenes})), None)
    if first and GREETING_RE.search(first[2]):
        add(out, "warning", "hook", f"opens with a greeting — start with the hook, greet later (or never): “{first[2][:50]}”")
    if first and ctype != "long_form":
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
        if ctype == "ad":  # ad slots are fixed: running over is not an option
            if total > hi * 1.05:
                add(out, "error", "runtime", f"estimated {total:.0f}s but the ad slot is {hi:.0f}s — cut lines (ads can't run over)")
            elif total < lo * 0.8:
                add(out, "warning", "runtime", f"estimated {total:.0f}s for a {lo:.0f}–{hi:.0f}s slot — room to land the offer/CTA")
        else:
            err, warn = (0.35, 0.15) if ctype == "long_form" else (0.25, 0.10)
            if total < lo * (1 - err) or total > hi * (1 + err):
                add(out, "error", "runtime", f"estimated {total:.0f}s vs target {lo:.0f}–{hi:.0f}s (>{int(err * 100)}% off) — cut or add")
            elif total < lo * (1 - warn) or total > hi * (1 + warn):
                add(out, "warning", "runtime", f"estimated {total:.0f}s vs target {lo:.0f}–{hi:.0f}s")

    # --- long-form: structure that holds attention for minutes
    starts = scene_starts({"scenes": scenes}, lang, wps)
    ch_idx = [i for i, sc in enumerate(scenes) if sc.get("chapter")]
    if ch_idx and ctype != "long_form":
        add(out, "warning", "chapters", "chapters are set but content_type isn't long_form — they won't be printed")
    if ctype == "long_form":
        if total > 180 and not ch_idx:
            add(out, "warning", "chapters", "over 3 minutes with no chapters — set \"chapter\" on the scenes that start a section")
        for sc in scenes:
            secs = estimate_scene_seconds(sc, lang, wps)
            unscripted = any(isinstance(bl, dict) and bl.get("type") == "question" for bl in sc.get("blocks") or [])
            if secs > 180 and not unscripted:  # interview segments are answers, not a monologue
                add(out, "warning", sc.get("title", ""), f"one scene runs ~{secs:.0f}s — split it or add a re-hook / visual change "
                                                         "every 60–90 s")
        if 0 < len(ch_idx) < 3:
            add(out, "warning", "chapters", f"{len(ch_idx)} chapter(s) — YouTube needs at least 3 (each ≥ 10 s, first at 00:00) to show them")
        times = [0.0 if k == 0 else starts[i] for k, i in enumerate(ch_idx)] + [total]
        for k, i in enumerate(ch_idx):
            if times[k + 1] - times[k] < 10:
                add(out, "warning", "chapters", f"chapter '{scenes[i]['chapter']}' lasts ~{times[k + 1] - times[k]:.0f}s — "
                                                "YouTube needs ≥ 10 s per chapter")
        if ch_idx and ch_idx[0] > 0 and starts[ch_idx[0]] > 75:
            add(out, "warning", "intro", f"the intro runs ~{starts[ch_idx[0]]:.0f}s before the first chapter — keep the cold open + "
                                         "promise under ~45–60 s")

    # --- cutdowns (any content type that defines them)
    cut_fits = {}
    for i, c in enumerate(as_list(spec.get("cutdowns"))):
        where = f"cutdowns[{i}]"
        if not isinstance(c, dict):
            add(out, "error", where, "each cutdown must be an object {name, target_sec, scenes, ratio, placement}")
            continue
        try:
            idx = cut_scene_indices(c, len(scenes))
        except SpecError as e:
            add(out, "error", where, str(e))
            continue
        tgt = c.get("target_sec")
        if isinstance(tgt, bool) or not isinstance(tgt, (int, float)):
            add(out, "error", where, f"cutdown '{c.get('name')}' has no target_sec")
            continue
        for n in idx:
            sc = scenes[n - 1]
            if not isinstance(sc.get("duration_sec"), (int, float)) and estimate_scene_seconds(sc, lang, wps) == 0:
                add(out, "warning", where, f"scene {n} has no words and no duration_sec — time it so the cutdown can be checked")
        est = sum(estimate_scene_seconds(scenes[n - 1], lang, wps) for n in idx) + float(c.get("end_frame_sec") or 0)
        if est > tgt * 1.05:
            add(out, "error", where, f"cutdown '{c.get('name')}' runs ~{est:.1f}s for a {tgt}s slot — drop or trim scenes")
        elif est < tgt * 0.6:
            add(out, "warning", where, f"cutdown '{c.get('name')}' is only ~{est:.1f}s of {tgt}s")
        pl = c.get("placement")
        if pl in PLACEMENTS and PLACEMENTS[pl] and tgt > PLACEMENTS[pl]:
            add(out, "error", where, f"{pl} allows at most {PLACEMENTS[pl]}s, cutdown target is {tgt}s")
        if pl and est <= tgt * 1.05 and (not PLACEMENTS.get(pl) or tgt <= PLACEMENTS[pl]):
            cut_fits[pl] = True
        if not scene_has_words(scenes[idx[0] - 1]):
            add(out, "warning", where, f"cutdown '{c.get('name')}' opens on a scene with no words — its hook must land in 3 s")
        if not scene_has_words(scenes[idx[-1] - 1]) and not c.get("end_frame_sec"):
            add(out, "warning", where, f"cutdown '{c.get('name')}' ends without a spoken/written CTA and has no end_frame_sec")

    # --- ads: brand early, placements, copy, policy
    brand_name = str(brief.get("brand_name") or "").strip()
    if ctype == "ad":
        placements = as_list(brief.get("placements"))
        if not placements:
            add(out, "warning", "brief.placements", "no ad placements — they decide length, ratio and safe zones")
        for p in placements:
            if p not in PLACEMENTS:
                add(out, "warning", "brief.placements", f"unknown placement '{p}' (known: {', '.join(PLACEMENTS)})")
            elif PLACEMENTS[p] and total > PLACEMENTS[p] * 1.05 and not cut_fits.get(p):
                add(out, "error", "brief.placements", f"{p} allows at most {PLACEMENTS[p]}s but the script runs ~{total:.1f}s "
                                                      f"and no cutdown with placement '{p}' fits — add one")
        if not brief.get("ratios"):
            add(out, "warning", "brief.ratios", "no aspect ratios listed (e.g. 9:16, 4:5, 1:1, 16:9) — the director frames for all of them")
        if not brand_name:
            add(out, "warning", "brief.brand_name", "set brief.brand_name so the brand-in-first-seconds check can run")
        elif not brand_seen_early(scenes, starts, brand_name, lang, wps):
            add(out, "warning", "brand", f"'{brand_name}' isn't seen or heard in the first 5 s — skippable viewers leave "
                                         "without knowing who it was (show the logo/product or say the name)")
        for sc in scenes:
            for bl in sc.get("blocks") or []:
                if isinstance(bl, dict):
                    for _, text in safe_lines(bl):
                        if PERSONAL_ATTR_RE.search(text):
                            add(out, "warning", sc.get("title", ""), f"asserts a personal attribute of the viewer — Meta/TikTok "
                                                                     f"ad policy rejects this; reframe: “{text[:60]}”")

    # --- a timed scene must fit its own lines
    for sc in scenes:
        if isinstance(sc.get("duration_sec"), (int, float)):
            spoken = estimate_scene_seconds({"blocks": sc.get("blocks")}, lang, wps)  # words only
            if spoken > sc["duration_sec"] * 1.1 + 0.3:
                add(out, "warning", sc.get("title", ""), f"lines need ~{spoken:.1f}s but the scene is timed at {sc['duration_sec']}s "
                                                         "— cut words or give it more time")

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
    if ctype == "ad" and str(cta or "").strip().lower() in ("", "none"):
        add(out, "error", "cta", "an ad needs a CTA — one action, said and shown")
    elif not cta:
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
    for i, t in enumerate(as_list(posting.get("title_options"))):
        if len(str(t)) > 100:
            add(out, "error", f"posting.title_options[{i}]", f"{len(str(t))} chars > YouTube's 100")
        elif len(str(t)) > 70:
            add(out, "warning", f"posting.title_options[{i}]", f"{len(str(t))} chars — titles get cut around 60–70 in search/feeds")
    ad = posting.get("ad_copy") if isinstance(posting.get("ad_copy"), dict) else {}
    for key, soft, label in (("primary_text", 125, "primary text shows ~125 chars before 'more'"),
                             ("headline", 40, "Meta recommends ~27 chars and cuts headlines around 40"),
                             ("description", 27, "Meta recommends ~27 chars for the link description")):
        if ad.get(key) and len(str(ad[key])) > soft:
            add(out, "warning", f"posting.ad_copy.{key}", f"{len(str(ad[key]))} chars — {label} (verify per placement)")
        if ad.get(key) and (CLAIM_RE.search(str(ad[key])) or PERSONAL_ATTR_RE.search(str(ad[key]))):
            add(out, "warning", f"posting.ad_copy.{key}", "ad copy makes a claim or asserts a personal attribute — check ad policy")
    if not posting:
        add(out, "warning", "posting", "no posting pack (cover text, caption, hashtags, A/B hooks / ad copy / titles)")
    elif ctype == "long_form":
        if not posting.get("title_options"):
            add(out, "warning", "posting.title_options", "long-form needs 3–5 title options — packaging decides the click")
        if not posting.get("thumbnail_concepts"):
            add(out, "warning", "posting.thumbnail_concepts", "no thumbnail concepts — design them with the title, before the shoot")
    elif ctype == "ad":
        if not ad:
            add(out, "warning", "posting.ad_copy", "no ad copy (primary text, headline, CTA button)")
        if not posting.get("alt_hooks"):
            add(out, "warning", "posting.alt_hooks", "no alternative hooks — ads need 3+ hook variants to test")
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
