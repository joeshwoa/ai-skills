#!/usr/bin/env python3
"""
script_breakdown.py — read a client's script the way a first AD and a
script supervisor would, before anyone designs a shot.

A video made from a misread script cannot be fixed by better prompts. So
the very first thing that happens to a client script is a mechanical
breakdown: every scene, location, time of day, character, line of
dialogue, voice-over, sound cue, on-screen text and transition — with
timings and the problems a reader would catch. The agent then does the
interpretive half (intent, tone, subtext — references/script-analysis.md)
on top of facts instead of impressions.

Reads: .txt .md .fountain (plain text), .docx (no dependencies), .pdf
(needs `pdftotext`). Arabic and English, mixed allowed. Understands:
  - screenplay format   (INT./EXT. headings, CHARACTER cue in caps, dialogue)
  - inline format       (Name: line)  /  (هنا: جملة)
  - Arabic headings     (مشهد 1 - داخلي - مطبخ - ليل)
  - extensions          (V.O.) (O.S.) (صوت) (راوي)…  parentheticals (بهمس)
  - labelled cues       SFX: / MUSIC: / TEXT: / VO:  and Arabic equivalents
  - transitions         CUT TO: / DISSOLVE TO: / FADE IN: / قطع إلى / مزج

USAGE
    python3 script_breakdown.py client_script.docx --out breakdown/ \
        --target-seconds 60 --ratio 9:16
Writes breakdown/breakdown.json, breakdown/breakdown.md (the report to
read and to show the client), breakdown/plan_skeleton.json (a first shot
list the agent must then route properly — never generate from it as-is).

EXIT CODES: 0 read cleanly · 3 read with issues/questions · 1 cannot read
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
import unicodedata
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
try:
    from shot_plan import PACE, count_words
except Exception:  # keep usable standalone
    PACE = {"ar": {"target": (2.0, 2.6), "max": 3.0}, "en": {"target": (2.3, 3.0), "max": 3.5},
            "default": {"target": (2.0, 2.8), "max": 3.2}}

    def count_words(t: str) -> int:
        t = re.sub(r"\[[^\]]*\]", " ", t)
        return len([w for w in t.split() if w])

AR = r"؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿"
TASHKEEL = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭ]")

MAX_CLIP = 10.0          # longest single generation (Omni) in seconds
LEAD, TAIL, GAP = 0.7, 0.8, 0.4   # air before first line, after last, between lines
MAX_SPEAKERS_PER_CLIP = 2

HEADING = re.compile(
    r"^\s*(?:#{1,3}\s*)?(?:(?:scene|sc\.?)\s*\d+[\s:.\-–—]*|المشهد|مشهد\s*[\d٠-٩]*[\s:.\-–—]*)?"
    r"(?P<ie>INT\.?/EXT\.?|EXT\.?/INT\.?|I/E|INT\.?|EXT\.?|داخلي\s*/\s*خارجي|داخلي|خارجي)\b",
    re.I)
HEADING_LOOSE = re.compile(r"^\s*(?:#{1,3}\s+.+|(?:scene|sc\.)\s*\d+\b.*|المشهد\s*.*|مشهد\s*[\d٠-٩]+.*)$", re.I)
TIME_WORDS = {
    "day": "day", "night": "night", "morning": "morning", "evening": "evening", "dawn": "dawn",
    "dusk": "dusk", "sunset": "sunset", "afternoon": "afternoon", "continuous": "continuous",
    "later": "later", "نهار": "day", "النهار": "day", "ليل": "night", "الليل": "night", "ليلا": "night",
    "صباح": "morning", "الصبح": "morning", "صباحا": "morning", "مساء": "evening", "بالليل": "night",
    "فجر": "dawn", "الفجر": "dawn", "غروب": "sunset", "الغروب": "sunset", "ظهر": "afternoon",
    "العصر": "afternoon", "مستمر": "continuous", "لاحقا": "later",
}
TRANSITION = re.compile(
    r"^\s*(?P<t>fade in|fade out|fade to black|fade to white|cut to|smash cut to|match cut to|"
    r"jump cut to|dissolve to|wipe to|whip pan to|cross ?fade|l-cut|j-cut|"
    r"قطع إلى|قطع الى|قطع|مزج إلى|مزج الى|مزج|ظهور تدريجي|اختفاء تدريجي|إظلام|اظلام|انتقال إلى|انتقال)\s*:?\s*\.?\s*$",
    re.I)
TRANSITION_MAP = {
    "fade in": "fade_black", "fade out": "fade_black", "fade to black": "fade_black",
    "fade to white": "fade_white", "cut to": "cut", "smash cut to": "cut", "jump cut to": "cut",
    "match cut to": "match_cut", "dissolve to": "dissolve", "cross fade": "dissolve",
    "crossfade": "dissolve", "wipe to": "wipe", "whip pan to": "whip_pan", "l-cut": "l_cut",
    "j-cut": "j_cut", "قطع إلى": "cut", "قطع الى": "cut", "قطع": "cut", "مزج إلى": "dissolve",
    "مزج الى": "dissolve", "مزج": "dissolve", "ظهور تدريجي": "fade_black",
    "اختفاء تدريجي": "fade_black", "إظلام": "fade_black", "اظلام": "fade_black",
    "انتقال إلى": "cut", "انتقال": "cut",
}
INLINE = re.compile(
    r"^\s*(?P<name>[^\s:：()\[\]][^:：()\[\]]{0,30}?)\s*(?:\((?P<ext>[^)]{1,24})\))?\s*[:：]\s*(?P<text>.*)$")
CAPS_CUE = re.compile(r"^\s*(?P<name>[A-Z][A-Z0-9 .'\-]{1,28})\s*(?:\((?P<ext>[^)]{1,24})\))?\s*$")
PAREN = re.compile(r"^\s*[(（](?P<p>[^)）]{1,80})[)）]\s*(?P<rest>.*)$")
AR_CUE = re.compile(rf"^\s*(?P<name>[{AR}]+(?:\s+[{AR}]+){{0,2}})\s*(?:[(（](?P<ext>[^)）]{{1,24}})[)）])?\s*$")
# timecodes at the start of a line: "0:00-0:03:", "00:05 –", "[0:03]"
TIMECODE = re.compile(r"^\s*\[?(?P<tc>\d{1,2}:\d{2}(?:[.:]\d{1,2})?(?:\s*[-–—]\s*\d{1,2}:\d{2}(?:[.:]\d{1,2})?)?)\]?\s*[:：\-–—|]?\s*(?P<rest>.*)$")
ORDINALS = (r"\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|first|second|third|"
            r"fourth|fifth|sixth|seventh|eighth|ninth|tenth|[IVX]{1,5}|"
            r"الأول|الاول|الثاني|التاني|الثالث|التالت|الرابع|الخامس|السادس|السابع|الثامن|التامن|التاسع|العاشر|"
            r"الأخير|الاخير|واحد|اثنين|اتنين|ثلاثة|تلاتة|أربعة|اربعة|خمسة")
SCENE_HEAD = re.compile(rf"^\s*(?:#{{1,3}}\s*)?(?:scene|sc\.?|المشهد|مشهد)\s*(?:{ORDINALS})?\s*(?:[:：.\-–—]|$)", re.I)
# screenplay words that look like cues/names but are not characters
NOT_CHARACTERS = {"montage", "series of shots", "intercut", "flashback", "flash back", "back to", "end",
                  "the end", "end montage", "end flashback", "continued", "cont'd", "begin", "title",
                  "super", "insert", "later", "moments later", "black", "credits", "mos", "pov",
                  "مونتاج", "فلاش باك", "فلاشباك", "نهاية", "النهاية", "تتر", "لاحقا", "لقطات", "عودة"}

LABELS = {
    "sfx": "sfx", "sound": "sfx", "fx": "sfx", "مؤثرات": "sfx", "مؤثر": "sfx", "صوت": "sfx", "مؤثرات صوتية": "sfx",
    "music": "music", "موسيقى": "music", "موسيقي": "music", "مزيكا": "music",
    "text": "onscreen", "on screen": "onscreen", "on-screen": "onscreen", "on-screen text": "onscreen",
    "super": "onscreen", "title": "onscreen", "caption": "onscreen", "نص": "onscreen",
    "كتابة": "onscreen", "نص على الشاشة": "onscreen", "عنوان": "onscreen", "تتر": "onscreen",
    "vo": "vo", "v.o.": "vo", "v.o": "vo", "voice over": "vo", "voiceover": "vo", "narrator": "vo",
    "narration": "vo", "الراوي": "vo", "راوي": "vo", "الراوى": "vo", "المعلق": "vo",
    "تعليق صوتي": "vo", "تعليق": "vo", "فويس اوفر": "vo", "فويس أوفر": "vo",
    "note": "note", "notes": "note", "ad": "note", "إعلان": "note", "اعلان": "note", "project": "note",
    "المشروع": "note", "العنوان": "note", "brief": "note", "client": "note", "العميل": "note",
    "duration": "note", "المدة": "note", "platform": "note", "المنصة": "note", "format": "note",
    "concept": "note", "الفكرة": "note", "target": "note", "الجمهور": "note", "ملاحظة": "note", "ملحوظة": "note", "ملاحظات": "note",
    "location": "note", "المكان": "note", "time": "note", "الوقت": "note", "hook": "note",
    "cta": "onscreen", "visual": "action", "action": "action", "وصف": "action", "المشهد": "action",
    "shot": "action", "لقطة": "action", "camera": "action", "كاميرا": "action", "الكاميرا": "action",
}
VO_EXT = {"v.o.", "vo", "v.o", "voice over", "narrator", "صوت", "راوي", "تعليق", "تعليق صوتي", "صوت فقط"}
OS_EXT = {"o.s.", "o.s", "os", "o.c.", "o.c", "off", "off screen", "خارج الكادر", "من بره", "من برا"}

EGY = set("ده دي دا إيه ايه مش عايز عايزه عاوز ازاي إزاي كده كدا بتاع دلوقتي اوي أوي خالص بقى يلا يعني امبارح بكره النهارده النهاردة فين ليه إمتى امتى حاجة حاجه مفيش فيه برضه".split())
MSA = set("هذا هذه ماذا ليس لماذا كيف سوف الذي التي لقد لن أين متى الآن جدا لكن إنني إنه أيضا".split())

RISKS = [
    (r"\b(crowd|audience|stadium|protest)\b|جمهور|زحمة|زحام|حشد|مظاهرة", "crowd scenes: AI video struggles with many consistent people — keep crowds soft/background"),
    (r"\b(fight|punch|chase|run|dance|jump)\w*|خناقة|معركة|ضرب|جري|يجري|رقص|يرقص|قفز", "fast action: limbs melt in fast motion — slow it, cut on action, or split into short beats"),
    (r"\b(sign|poster|screen shows|banner|logo|label)\b|لافتة|يافطة|بوستر|شاشة|لوجو|شعار|مكتوب", "text in frame: video models garble text — make it in the keyframe (Nano Banana Pro) or add in post"),
    (r"\b(hands?|fingers?|typing|writing)\b|إيده|ايده|يده|أصابع|صوابع|يكتب|بيكتب", "close hand action: check fingers every take; favour wider framing"),
    (r"\b(water|rain|fire|smoke|pour)\w*|مية|مياه|ماء|مطر|نار|دخان|يصب", "fluids/fire: fine as texture, poor as precise action"),
    (r"\b(dog|cat|horse|bird|animal)s?\b|كلب|قطة|قطه|حصان|عصفور|حيوان", "animals: consistency across shots is hard — add a reference image"),
    (r"\b(mirror|reflection)\b|مراية|مرآة|انعكاس", "mirrors/reflections: frequent physics errors"),
    (r"\b(phone screen|laptop screen|tv)\b|موبايل|تليفون|لابتوب|تلفزيون", "device screens: content on screens is usually wrong — insert in post"),
]


# ------------------------------------------------------------------ reading
def read_any(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        import xml.etree.ElementTree as ET
        W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        with zipfile.ZipFile(path) as z:
            root = ET.fromstring(z.read("word/document.xml"))
        paras = []
        for p in root.iter(W + "p"):          # document order, tables included
            buf = []
            # only run content: <w:tabs> in paragraph properties are tab STOPS, not tabs
            for el in (x for r in p.iter(W + "r") for x in r):
                if el.tag == W + "t" and el.text:
                    buf.append(el.text)
                elif el.tag == W + "tab":
                    buf.append("\t")
                elif el.tag in (W + "br", W + "cr"):
                    buf.append("\n")
            paras.append("".join(buf))
        return "\n".join(paras)
    if ext == ".pdf":
        r = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit("cannot read PDF (pdftotext missing?) — ask for a .docx or .txt copy")
        return r.stdout
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def to_ascii_digits(s: str) -> str:
    return s.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789"))


def norm_name(n: str) -> str:
    n = TASHKEEL.sub("", unicodedata.normalize("NFKC", n)).strip().lower()
    n = re.sub("[أإآ]", "ا", n).replace("ة", "ه").replace("ى", "ي")
    return re.sub(r"\s+", " ", n)


def is_arabic(s: str) -> bool:
    letters = [c for c in s if c.isalpha()]
    return bool(letters) and sum(1 for c in letters if re.match(f"[{AR}]", c)) / len(letters) > 0.5


def lev(a: str, b: str) -> int:
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def label_of(name: str) -> str | None:
    n = norm_name(name).rstrip(".")
    for k, v in LABELS.items():
        if n == norm_name(k):
            return v
    return None


def is_scene_heading(s: str) -> bool:
    if HEADING.match(s) or SCENE_HEAD.match(s):
        return True
    return bool(HEADING_LOOSE.match(s) and len(s) < 90 and not INLINE.match(s))


def not_character(name: str) -> bool:
    n = norm_name(name).rstrip(".:")
    return n in {norm_name(x) for x in NOT_CHARACTERS} or bool(re.search(r"\d", name))


def cue_candidates(lines: list[str]) -> set[str]:
    """Short Arabic lines that stand alone and are followed by text at least
    twice are speaker cues ("سلمى" on its own line, the line below it)."""
    seen: dict[str, int] = {}
    for i, raw in enumerate(lines[:-1]):
        s, nxt = raw.strip(), lines[i + 1].strip()
        m = AR_CUE.match(s)
        if not m or not nxt or is_scene_heading(s) or TRANSITION.match(s) or label_of(m.group("name")):
            continue
        if not_character(m.group("name")):
            continue
        seen[norm_name(m.group("name"))] = seen.get(norm_name(m.group("name")), 0) + 1
    return {k for k, v in seen.items() if v >= 2}


def clean_spoken(t: str) -> tuple[str, str | None]:
    """Remove a leading (parenthetical) and [bracketed] directions; return text + delivery note."""
    note = None
    m = PAREN.match(t)
    if m:
        note, t = m.group("p").strip(), m.group("rest")
    t = re.sub(r"\[[^\]]*\]", " ", t)
    return " ".join(t.split()), note


# ------------------------------------------------------------------ parsing
def speech_event(name, ext, lab, rest, note, i, timecode) -> dict:
    """A spoken line. A NAMED character in V.O. keeps the name: it is that
    character's voice (inner voice / narration by her) and must be cast with
    her voice. Only an unnamed narrator ("VO:", "الراوي:") is narration."""
    ext_n = norm_name(ext or "")
    is_vo = lab == "vo" or ext_n in {norm_name(x) for x in VO_EXT}
    spoken, n2 = clean_spoken(rest)
    ev = {"type": "vo" if is_vo else "dialogue",
          "character": None if lab == "vo" else name,
          "offscreen": is_vo or ext_n in {norm_name(x) for x in OS_EXT},
          "delivery": note or n2 or (ext if ext and not is_vo and ext_n not in
                                     {norm_name(x) for x in OS_EXT} else None),
          "text": spoken, "line": i + 1}
    if timecode:
        ev["timecode"] = timecode
    return ev


def parse(text: str) -> dict:
    lines = to_ascii_digits(text).replace("\r\n", "\n").replace("\r", "\n").split("\n")
    ar_cues = cue_candidates(lines)
    scenes: list[dict] = []
    cur: dict | None = None
    pending_transition = None

    def new_scene(heading: str | None, idx: int) -> dict:
        nonlocal pending_transition
        sc = {"n": len(scenes) + 1, "heading": heading, "int_ext": None, "location": None,
              "time": None, "line": idx + 1, "events": [],
              "transition_in": pending_transition}
        pending_transition = None
        if heading:
            m = HEADING.match(heading)
            if m:
                ie = m.group("ie").upper().replace("داخلي", "INT").replace("خارجي", "EXT")
                sc["int_ext"] = "INT" if "INT" in ie and "EXT" not in ie else ("EXT" if "EXT" in ie and "INT" not in ie else "INT/EXT")
            rest = HEADING.sub("", heading) if m else SCENE_HEAD.sub("", re.sub(r"^\s*#{1,3}\s*", "", heading))
            parts = [p.strip(" .:") for p in re.split(r"\s[-–—|/]\s|\s[-–—]|[-–—]\s|,|،|\.\s|:\s", rest)
                     if p.strip(" .:")]
            for p in list(parts):
                w = norm_name(p)
                for tw, tv in TIME_WORDS.items():
                    if w == norm_name(tw) or w.endswith(" " + norm_name(tw)):
                        sc["time"] = tv
                        parts.remove(p)
                        break
            parts = [p for p in parts if not re.fullmatch(r"(scene|مشهد|المشهد)?\s*\d+", p, re.I)]
            sc["location"] = " — ".join(parts) or None
        scenes.append(sc)
        return sc

    i = 0
    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        if not s:
            i += 1
            continue
        if TRANSITION.match(s):
            t = TRANSITION_MAP.get(TRANSITION.match(s).group("t").lower(), "cut")
            if cur and cur["events"] and t == "fade_black" and "out" in s.lower() + ("اختفاء" if "اختفاء" in s else ""):
                cur["transition_out"] = "fade_black"
            else:
                pending_transition = t
            i += 1
            continue
        if is_scene_heading(s):
            # "مشهد ٣" on one line, "خارجي. محطة. مساء" on the next = one heading
            if cur is not None and not cur["events"] and cur["heading"] and not cur["int_ext"] \
                    and not cur["location"] and scenes[-1] is cur:
                scenes.pop()
                pending_transition = pending_transition or cur.get("transition_in")
                cur = new_scene(cur["heading"] + " - " + s, cur["line"] - 1)
            else:
                cur = new_scene(s, i)
            i += 1
            continue
        if cur is None:
            cur = new_scene(None, i)

        tc = TIMECODE.match(s)
        timecode = None
        if tc and tc.group("rest") is not None:
            timecode, s = tc.group("tc"), tc.group("rest").strip()
            if not s:
                i += 1
                continue

        # labelled / inline dialogue
        m = INLINE.match(s)
        if m and len(m.group("name").split()) <= 4 and not re.search(r"[.!?؟،]$", m.group("name")) \
                and not re.search(r"\d", m.group("name")):
            name, ext, rest = m.group("name").strip(), (m.group("ext") or "").strip(), m.group("text").strip()
            lab = label_of(name)
            first = norm_name(name.split()[0]) if name.split() else ""
            if not lab and len(name.split()) > 1 and first in {norm_name(x) for x in
                                                              ("note", "notes", "ملاحظة", "ملحوظة", "ملاحظات")}:
                lab = "note"                                   # "NOTE TO CLIENT:"
            if not lab and not_character(name):
                lab = "action"                                 # "MONTAGE:", "FLASHBACK:"
                rest = f"{name}: {rest}".strip(": ")
            if not rest:  # name alone, dialogue on following lines
                j, block = i + 1, []
                while j < len(lines) and lines[j].strip() and not INLINE.match(lines[j]) \
                        and not HEADING.match(lines[j].strip()) and not TRANSITION.match(lines[j].strip()):
                    block.append(lines[j].strip())
                    j += 1
                rest, i = " ".join(block), j - 1
            if lab in ("sfx", "music", "onscreen", "note", "action"):
                cur["events"].append({"type": lab, "text": rest, "line": i + 1,
                                      **({"timecode": timecode} if timecode else {})})
            elif rest:
                cur["events"].append(speech_event(name, ext, lab, rest, None, i, timecode))
            i += 1
            continue

        # screenplay cue: NAME (Latin caps) or an Arabic name seen as a cue elsewhere
        c = CAPS_CUE.match(s)
        if c and not_character(c.group("name")):
            cur["events"].append({"type": "action", "text": s, "line": i + 1})
            i += 1
            continue
        if not c:
            ac = AR_CUE.match(s)
            if ac and (norm_name(ac.group("name")) in ar_cues or
                       (ac.group("ext") and norm_name(ac.group("ext")) in
                        {norm_name(x) for x in VO_EXT | OS_EXT})):
                c = ac
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if c and nxt and not HEADING.match(s) and not TRANSITION.match(nxt) and not is_scene_heading(nxt):
            name, ext = c.group("name").strip(), (c.group("ext") or "").strip()
            j, block, note = i + 1, [], None
            while j < len(lines) and lines[j].strip():
                ln = lines[j].strip()
                cm = CAPS_CUE.match(ln)
                if is_scene_heading(ln) or TRANSITION.match(ln) or (cm and not_character(cm.group("name"))):
                    break
                pm = PAREN.match(ln)
                if pm and not pm.group("rest"):
                    note = pm.group("p")
                else:
                    block.append(ln)
                j += 1
            lab = label_of(name)
            if lab in ("sfx", "music", "onscreen", "note", "action"):
                cur["events"].append({"type": lab, "text": " ".join(block), "line": i + 1})
            else:
                cur["events"].append(speech_event(name if is_arabic(name) else name.title(), ext, lab,
                                                  " ".join(block), note, i, timecode))
            i = j
            continue

        cur["events"].append({"type": "action", "text": s, "line": i + 1,
                              **({"timecode": timecode} if timecode else {})})
        i += 1

    # Lines before the first real scene heading are the client's cover info
    # (title, format, duration, notes) — not a scene, and not characters.
    preamble = []
    if len(scenes) > 1 and scenes[0]["heading"] is None and any(sc["heading"] for sc in scenes[1:]):
        first = scenes.pop(0)
        preamble = [(e.get("character") + ": " if e.get("character") else "") + e.get("text", "")
                    for e in first["events"]]
        if first.get("transition_in") and not scenes[0].get("transition_in"):
            scenes[0]["transition_in"] = first["transition_in"]
        for k, sc in enumerate(scenes, 1):
            sc["n"] = k
    return {"scenes": scenes, "preamble": preamble}


# ------------------------------------------------------------------ analysis
def analyse(parsed: dict, target: float | None, lang_hint: str | None,
            aliases: dict[str, str] | None = None) -> dict:
    scenes = parsed["scenes"]
    all_text = " ".join(e.get("text", "") for sc in scenes for e in sc["events"])
    lang = lang_hint or ("ar" if is_arabic(all_text) else "en")
    lk = lang.split("-")[0] if lang.split("-")[0] in PACE else "default"
    lo, hi = PACE[lk]["target"]
    wps = (lo + hi) / 2
    issues, questions = [], []

    # characters, with spelling-variant detection
    # Names are never merged on a guess (هند and هنا are different people).
    # Near-identical spellings become a question; the client's answer comes
    # back as --alias "كرين=كريم" and only then are they joined.
    alias = {norm_name(a): b for a, b in (aliases or {}).items()}
    raw_names: dict[str, list[str]] = {}
    for sc in scenes:
        for e in sc["events"]:
            if e["type"] in ("dialogue", "vo") and e.get("character"):
                nm = alias.get(norm_name(e["character"]), e["character"])
                raw_names.setdefault(norm_name(nm), []).append(nm)
    canon = {k: max(set(v), key=v.count) for k, v in raw_names.items()}
    keys = sorted(canon)
    for a_i, a in enumerate(keys):
        for b in keys[a_i + 1:]:
            if len(a) >= 3 and len(b) >= 3 and lev(a, b) == 1:
                na, nb = len(raw_names[a]), len(raw_names[b])
                questions.append(f"\"{canon[a]}\" ({na} line(s)) and \"{canon[b]}\" ({nb} line(s)) — the same "
                                 f"character (a typo) or two people? Kept SEPARATE until you answer; if the "
                                 f"same, re-run with --alias \"{canon[a] if na < nb else canon[b]}="
                                 f"{canon[b] if na < nb else canon[a]}\".")
                issues.append(f"Possible name typo: \"{canon[a]}\" / \"{canon[b]}\" — the cast cannot be locked "
                              f"until this is answered.")

    def cname(n: str | None) -> str | None:
        if not n:
            return None
        n = alias.get(norm_name(n), n)
        return canon.get(norm_name(n), n)

    chars: dict[str, dict] = {}
    total_speech = 0.0
    for sc in scenes:
        sc["characters"] = []
        sc_speech = 0.0
        action_words = 0
        for e in sc["events"]:
            if e["type"] in ("dialogue", "vo"):
                e["character"] = cname(e.get("character"))
                w = count_words(e["text"])
                e["words"] = w
                e["seconds"] = round(w / wps, 1)
                sc_speech += e["seconds"]
                if e.get("character"):
                    c = chars.setdefault(e["character"], {"name": e["character"], "lines": 0, "words": 0,
                                                           "scenes": [], "offscreen_lines": 0,
                                                           "vo_lines": 0, "speaks": True,
                                                           "egy": 0, "msa": 0})
                    c["lines"] += 1
                    if e["type"] == "vo":
                        c["vo_lines"] += 1
                    c["words"] += w
                    if sc["n"] not in c["scenes"]:
                        c["scenes"].append(sc["n"])
                    if e.get("offscreen"):
                        c["offscreen_lines"] += 1
                    toks = [norm_name(t) for t in re.findall(f"[{AR}]+", e["text"])]
                    c["egy"] += sum(t in {norm_name(x) for x in EGY} for t in toks)
                    c["msa"] += sum(t in {norm_name(x) for x in MSA} for t in toks)
                    if e["type"] == "dialogue" and not e.get("offscreen") \
                            and e["character"] not in sc["characters"]:
                        sc["characters"].append(e["character"])
                if e["seconds"] > MAX_CLIP - LEAD - TAIL:
                    issues.append(f"Scene {sc['n']} line {e['line']}: {w} words ≈ {e['seconds']}s — longer "
                                  f"than one clip can hold; will be split across shots at a pause.")
            elif e["type"] == "action":
                action_words += count_words(e["text"])
        # mentions of known characters in action lines
        for e in sc["events"]:
            if e["type"] == "action":
                for c in list(chars):
                    if re.search(rf"(?<![{AR}\w]){re.escape(norm_name(c))}", norm_name(e["text"])) \
                            and c not in sc["characters"]:
                        sc["characters"].append(c)
                        if sc["n"] not in chars[c]["scenes"]:
                            chars[c]["scenes"].append(sc["n"])
        if re.search(r"\b(both|together|they|the two|everyone)\b|الاتنين|الاثنين|الإتنين|هما|سوا|مع بعض|الكل|الجميع",
                     " ".join(e["text"] for e in sc["events"] if e["type"] == "action"), re.I):
            prev = scenes[scenes.index(sc) - 1]["characters"] if scenes.index(sc) > 0 else []
            for c in prev:
                if c not in sc["characters"]:
                    sc["characters"].append(c)
        sc["speech_seconds"] = round(sc_speech, 1)
        sc["est_seconds"] = round(max(sc_speech * 1.25 + 1.5, action_words / 6 + 2, 4), 1)
        total_speech += sc_speech

        if not sc.get("location"):
            questions.append(f"Scene {sc['n']}: where does it take place? (no location given)")
        if not sc.get("time"):
            questions.append(f"Scene {sc['n']}: time of day / light? (day, night, golden hour…)")
        speakers = {e["character"] for e in sc["events"] if e["type"] == "dialogue"}
        if len(speakers) > MAX_SPEAKERS_PER_CLIP:
            issues.append(f"Scene {sc['n']}: {len(speakers)} speakers — coverage must be split so no clip "
                          f"has more than {MAX_SPEAKERS_PER_CLIP} (voices get swapped otherwise).")
        for e in sc["events"]:
            if e["type"] == "dialogue" and e.get("offscreen"):
                issues.append(f"Scene {sc['n']} line {e['line']}: {e['character']} speaks off-screen (O.S.) — "
                              f"decide: keep them in frame, or treat as narration.")
            if e["type"] == "onscreen":
                issues.append(f"Scene {sc['n']} line {e['line']}: on-screen text \"{e['text'][:40]}\" — add "
                              f"in post or render in a keyframe; never ask the video model to write it.")
        risks = []
        blob = " ".join(e["text"] for e in sc["events"] if e["type"] in ("action", "onscreen"))
        for pat, msg in RISKS:
            if re.search(pat, blob, re.I):
                risks.append(msg)
        sc["risks"] = risks

    # silent on-screen people introduced in action: "SARA (30s)", "Omar (40)", "عم حسن (60)"
    TITLES = r"(?:عم|أم|ام|أبو|ابو|دكتور|الدكتور|الحاج|الحاجة|أستاذ|استاذ|الأستاذ|مدام|الست)"
    intro_re = re.compile(rf"(?P<n>[A-Z]{{2,}}(?:\s[A-Z]{{2,}})?|[A-Z][a-z'\-]+|(?:{TITLES}\s+)?[{AR}]+)"
                          r"\s*[(（][^)）]*?\d{1,3}[^)）]*[)）]")
    for sc in scenes:
        for e in sc["events"]:
            if e["type"] != "action":
                continue
            for m in intro_re.finditer(e["text"]):
                nm = cname(m.group("n").strip())
                if len(nm) < 2 or not_character(nm) or label_of(nm):
                    continue
                if nm.isupper() and not is_arabic(nm):
                    nm = nm.title()
                if not any(norm_name(nm) == norm_name(k) for k in chars):
                    chars[nm] = {"name": nm, "lines": 0, "words": 0, "scenes": [sc["n"]],
                                 "offscreen_lines": 0, "vo_lines": 0, "speaks": False, "egy": 0, "msa": 0}
                    if nm not in sc["characters"]:
                        sc["characters"].append(nm)
    for sc in scenes:
        for e in sc["events"]:
            if e["type"] == "action":
                for c in list(chars):
                    if re.search(rf"(?<![{AR}\w]){re.escape(norm_name(c))}", norm_name(e["text"])) \
                            and c not in sc["characters"]:
                        sc["characters"].append(c)
                        if sc["n"] not in chars[c]["scenes"]:
                            chars[c]["scenes"].append(sc["n"])

    # first description of each character in action lines: "Salma (28) stands…"
    for c in chars.values():
        c["intro"], c["age"] = None, None
        for sc in scenes:
            for e in sc["events"]:
                if e["type"] == "action" and norm_name(c["name"]) in norm_name(e["text"]):
                    c["intro"] = e["text"]
                    m = re.search(re.escape(c["name"]) + r"\s*[(（][^)）]*?(\d{1,3})[^)）]*[)）]", e["text"], re.I)
                    if m:
                        c["age"] = int(m.group(1))
                    break
            if c["intro"]:
                break
    for c in chars.values():
        if c["egy"] and c["msa"] and min(c["egy"], c["msa"]) / max(c["egy"], c["msa"]) > 0.3:
            questions.append(f"{c['name']} mixes Egyptian dialect and MSA — intentional (e.g. reading a "
                             f"question aloud) or should it be all dialect?")
        known = f" (script gives: {c['intro'][:70]})" if c.get("intro") else ""
        need = "look and wardrobe" if c.get("age") else "age, look and wardrobe"
        questions.append(f"{c['name']}: {need}?{known} — needed to build the character before any "
                         f"shot, or approve the proposal we'll draw")
        if c.get("vo_lines"):
            questions.append(f"{c['name']} has {c['vo_lines']} voice-over line(s) in her/his own voice — record "
                             f"them with the character's Flow voice (audio from a short Omni clip) so it "
                             f"matches the on-screen voice, or with a matching TTS voice?")
        if not c.get("speaks"):
            questions.append(f"{c['name']} appears on screen without lines — confirm this person is needed "
                             f"on camera (they will be cast like everyone else).")
        if c["lines"] == 1 and c["words"] <= 3:
            issues.append(f"{c['name']} has a single short line — check it isn't a typo of another name.")

    questions.append("Anyone else on camera who doesn't speak (a barista, a child, passers-by)? "
                     "Every recognisable person is cast before any shot.")
    vo = [e for sc in scenes for e in sc["events"] if e["type"] == "vo" and not e.get("character")]
    if vo:
        questions.append("There is narration (V.O.): which voice-over provider — Gemini TTS (free, same "
                         "voices as Flow) or ElevenLabs (natural; free tier non-commercial)? Male/female, tone?")
    if any(e["type"] == "music" for sc in scenes for e in sc["events"]):
        questions.append("Music cues are in the script: do you supply the track, or should we brief/license one?")

    est_total = round(sum(sc["est_seconds"] for sc in scenes), 1)
    if target:
        if est_total > target * 1.15:
            issues.append(f"Estimated runtime {est_total}s is longer than the {target:g}s target — "
                          f"trim lines or scenes (suggestions in the report).")
        elif est_total < target * 0.7:
            issues.append(f"Estimated runtime {est_total}s is well under the {target:g}s target — "
                          f"confirm, or add beats/B-roll.")
    for c in chars.values():
        c.pop("egy"), c.pop("msa")
    return {"language": lang, "pace_wps": round(wps, 2), "scenes": scenes,
            "characters": list(chars.values()), "voiceover_lines": len(vo),
            "speech_seconds": round(total_speech, 1), "estimated_seconds": est_total,
            "target_seconds": target, "issues": issues, "questions": questions}


# ------------------------------------------------------------------ skeleton plan
def split_line(text: str, max_words: int) -> list[str]:
    words = text.split()
    if len(words) <= max_words:
        return [text]
    out, buf = [], []
    for w in words:
        buf.append(w)
        if len(buf) >= max_words * 0.55 and re.search(r"[،,.!?؟؛;…:]$", w):
            out.append(" ".join(buf)); buf = []
        elif len(buf) >= max_words:
            out.append(" ".join(buf)); buf = []
    if buf:
        out.append(" ".join(buf))
    return out


def pick_duration(need: float) -> int:
    for d in (4, 6, 8, 10):
        if need <= d:
            return d
    return 10


def slug(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", unicodedata.normalize("NFKD", name)).strip("_").upper()
    return s or "CHAR" + str(abs(hash(name)) % 1000)


def skeleton(an: dict, ratio: str, project: str) -> dict:
    wps = an["pace_wps"]
    max_words = int((MAX_CLIP - LEAD - TAIL) * wps)
    ids = {}
    characters = []
    for c in an["characters"]:
        cid = slug(c["name"])
        if cid.startswith("CHAR") or not re.match(r"[A-Z]", cid):
            cid = f"C{len(ids) + 1:02d}"
        ids[c["name"]] = cid
        speaks = bool(c.get("speaks", True))
        characters.append({"id": cid, "name": c["name"], "speaks": speaks, "status": "planned",
                           "flow_character": None, "voice": f"{cid}_VOICE" if speaks else None,
                           "sheet": None})
    shots, vo_lines, n = [], [], 0

    def add_shot(sc, beat, cast, dialogue, dur, transition, onscreen=None):
        nonlocal n
        n += 1
        shots.append({
            "id": f"S{n:02d}", "scene": sc["n"], "beat": beat[:90], "duration": dur,
            "model": "omni-1.1-flash", "mode": "ingredients" if cast else "text",
            "resolution": "720p", "outputs": 1, "cast": cast,
            "onscreen_seconds": round(onscreen or dur, 1),
            "keyframes": {"start": bool(cast), "end": False, "model": "nano-banana-2"},
            "ingredients": [f"{ids[c]}_REF" for c in cast] + [f"{ids[c]}_VOICE" for c in
                                                                 {d["character"] for d in dialogue}],
            "characters_recurring": bool(cast), "dialogue": dialogue,
            "continuation": "first_shot" if n == 1 else ("hard_cut" if transition else "ingredients"),
            "transition_in": {"type": transition or "cut"},
            "routing_reviewed": False})

    for sc in an["scenes"]:
        first_in_scene = True
        actions = [e["text"] for e in sc["events"] if e["type"] == "action"]
        lead_action = []
        for e in sc["events"]:
            if e["type"] in ("dialogue", "vo"):
                break
            if e["type"] == "action":
                lead_action.append(e["text"])
        if lead_action or not any(e["type"] == "dialogue" for e in sc["events"]):
            beat = " ".join(lead_action or actions)[:200] or (sc.get("location") or f"scene {sc['n']}")
            add_shot(sc, "ESTABLISH: " + beat, [c for c in sc["characters"] if c in ids][:2], [],
                     6 if len(beat.split()) > 12 else 4, sc.get("transition_in"),
                     onscreen=3.5 if len(beat.split()) > 12 else 2.5)
            first_in_scene = False
        group, speakers, t = [], set(), LEAD
        def flush():
            nonlocal group, speakers, t, first_in_scene
            if not group:
                return
            dur = pick_duration(t - GAP + TAIL)
            onscreen = {d["character"] for d in group if not d.get("offscreen")}
            cast = sorted(onscreen) or [c for c in sc["characters"] if c in ids and c not in speakers][:1]
            beat = " / ".join(f"{d['character']}: {d['text']}" for d in group)
            add_shot(sc, beat, cast, group, dur, sc.get("transition_in") if first_in_scene else None,
                     onscreen=t - GAP + 0.5)
            first_in_scene = False
            group, speakers, t = [], set(), LEAD
        for e in sc["events"]:
            if e["type"] == "vo":
                vo_lines.append({"scene": sc["n"], "text": e["text"], "seconds": e["seconds"],
                                 "after_shot": f"S{n:02d}" if n else None,
                                 **({"speaker": ids.get(e["character"]), "speaker_name": e["character"]}
                                    if e.get("character") else {})})
                continue
            if e["type"] != "dialogue":
                continue
            if e.get("offscreen"):
                flush()
            for part in split_line(e["text"], max_words):
                secs = round(max(1.2, count_words(part) / wps), 2)
                if group and (t + secs + TAIL > MAX_CLIP or
                              (e["character"] not in speakers and len(speakers) >= MAX_SPEAKERS_PER_CLIP)):
                    flush()
                group.append({"character": e["character"], "text": part,
                              "start": round(t, 2), "end": round(t + secs, 2),
                              **({"offscreen": True} if e.get("offscreen") else {}),
                              **({"delivery": e["delivery"]} if e.get("delivery") else {})})
                speakers.add(e["character"])
                t += secs + GAP
            if e.get("offscreen"):
                flush()
        flush()
    return {"project": project, "platform": "google-flow", "aspect_ratio": ratio,
            "language": an["language"], "budget_credits": None, "skeleton": True,
            "target_seconds": an.get("target_seconds"),
            "characters": characters, "voiceover_lines": vo_lines, "shots": shots}


# ------------------------------------------------------------------ report
def report_md(an: dict, src: str) -> str:
    L = [f"# Script breakdown — {os.path.basename(src)}", ""]
    L.append(f"Language: **{an['language']}** · scenes: **{len(an['scenes'])}** · characters: "
             f"**{len(an['characters'])}** · narration lines: **{an['voiceover_lines']}** · spoken "
             f"≈ **{an['speech_seconds']}s** · estimated runtime ≈ **{an['estimated_seconds']}s**"
             + (f" (target {an['target_seconds']:g}s)" if an['target_seconds'] else ""))
    if an.get("preamble"):
        L += ["", "## Header / cover notes", ""] + [f"- {x}" for x in an["preamble"]]
    L += ["", "## Characters", "", "| Character | Speaks | Lines | Words | Scenes | Off-screen | Age | First description |",
          "|---|---|---|---|---|---|---|---|"]
    for c in sorted(an["characters"], key=lambda c: -c["words"]):
        L.append(f"| {c['name']} | {'yes' if c.get('speaks', True) else 'silent'} | {c['lines']} | {c['words']} | "
                 f"{', '.join(map(str, c['scenes']))} | "
                 f"{c['offscreen_lines']} | {c.get('age') or '?'} | {(c.get('intro') or '—')[:80]} |")
    L += ["", "## Scenes", ""]
    for sc in an["scenes"]:
        L.append(f"### Scene {sc['n']} — {sc.get('int_ext') or '?'} · {sc.get('location') or '? location'} · "
                 f"{sc.get('time') or '? time'}  (≈{sc['est_seconds']}s)")
        if sc.get("transition_in"):
            L.append(f"_in: {sc['transition_in']}_")
        L.append(f"Characters: {', '.join(sc['characters']) or '—'}")
        for e in sc["events"]:
            if e["type"] == "dialogue":
                d = f" _({e['delivery']})_" if e.get("delivery") else ""
                o = " **[O.S.]**" if e.get("offscreen") else ""
                L.append(f"- **{e['character']}**{o}{d}: {e['text']}  `{e['words']}w ≈{e['seconds']}s`")
            elif e["type"] == "vo":
                who = f"{e['character']} (V.O.)" if e.get("character") else "NARRATION"
                L.append(f"- 🎙 **{who}**: {e['text']}  `{e['words']}w ≈{e['seconds']}s`")
            elif e["type"] in ("sfx", "music", "onscreen", "note"):
                L.append(f"- *{e['type'].upper()}*: {e['text']}")
            else:
                L.append(f"- {e['text']}")
        if sc["risks"]:
            L.append("")
            L.append("Production risks: " + "; ".join(sc["risks"]))
        L.append("")
    if an["issues"]:
        L += ["## Issues found", ""] + [f"- {x}" for x in an["issues"]] + [""]
    if an["questions"]:
        L += ["## Questions for the client", ""] + [f"{i}. {q}" for i, q in enumerate(an["questions"], 1)] + [""]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="Break a client script down before planning shots.")
    ap.add_argument("script")
    ap.add_argument("--out", default="breakdown")
    ap.add_argument("--target-seconds", type=float)
    ap.add_argument("--ratio", default="9:16", choices=["9:16", "16:9"])
    ap.add_argument("--language", help="override detection, e.g. ar-EG")
    ap.add_argument("--project", default=None)
    ap.add_argument("--alias", action="append", default=[],
                    help='client-confirmed same person: --alias "كرين=كريم" (repeatable)')
    args = ap.parse_args()
    aliases = {}
    for a_ in args.alias:
        if "=" not in a_:
            raise SystemExit(f"--alias needs OLD=NEW, got {a_}")
        k, v = a_.split("=", 1)
        aliases[k.strip()] = v.strip()

    try:
        text = read_any(args.script)
    except Exception as e:
        print(f"cannot read {args.script}: {e}")
        return 1
    if not text.strip():
        print("script is empty")
        return 1
    parsed = parse(text)
    an = analyse(parsed, args.target_seconds, args.language, aliases)
    an["preamble"] = parsed.get("preamble", [])
    if not any(c.get("speaks", True) for c in an["characters"]) and not an["voiceover_lines"]:
        an["issues"].append("No dialogue or narration found — either it's a silent/visual piece, or the "
                            "format wasn't recognised (use 'Name: line' per line).")
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "breakdown.json"), "w", encoding="utf-8") as f:
        json.dump(an, f, ensure_ascii=False, indent=1)
    with open(os.path.join(args.out, "breakdown.md"), "w", encoding="utf-8") as f:
        f.write(report_md(an, args.script))
    sk = skeleton(an, args.ratio, args.project or os.path.splitext(os.path.basename(args.script))[0])
    with open(os.path.join(args.out, "plan_skeleton.json"), "w", encoding="utf-8") as f:
        json.dump(sk, f, ensure_ascii=False, indent=1)

    print(f"{len(an['scenes'])} scenes · {len(an['characters'])} characters "
          f"({', '.join(c['name'] for c in an['characters'])}) · {an['voiceover_lines']} narration lines · "
          f"≈{an['estimated_seconds']}s · skeleton {len(sk['shots'])} shots")
    for x in an["issues"]:
        print(f"  ! {x}")
    print(f"  {len(an['questions'])} question(s) for the client")
    print(f"-> {args.out}/breakdown.md  breakdown.json  plan_skeleton.json")
    return 3 if an["issues"] or an["questions"] else 0


if __name__ == "__main__":
    sys.exit(main())
