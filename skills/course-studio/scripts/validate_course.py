#!/usr/bin/env python3
"""validate_course.py — the curriculum QA gate. Run on course_spec.json BEFORE building.

    run.sh validate_course.py course_spec.json

ERRORS (block the build): outcomes nobody teaches or nobody assesses · sessions whose timed plan does
not add up to the session length (±5 min) · assessment weights not summing to 100% · quiz items
without an answer · MCQ answers out of range · sessions with no objectives · placeholder text.
WARNINGS: no practice activity · no check for understanding · lecture segments > 20 min · Bloom
levels never rising above "remember/understand" · objectives without a measurable verb · fewer than
3 quiz items · missing misconceptions / differentiation in a session.
"""
import json
import re
import sys
from pathlib import Path

MEASURABLE = {
    "en": r"^(define|list|name|identify|recall|state|label|explain|describe|summari[sz]e|classify|compare|interpret|give|"
          r"apply|use|solve|write|build|implement|demonstrate|calculate|construct|create|design|develop|debug|trace|fix|"
          r"analy[sz]e|differentiate|organi[sz]e|test|evaluate|justify|critique|choose|assess|predict|convert|draw|plan|present|run|configure|modify|refactor|measure)\b",
    "ar": r"^(يعرّف|يعرف|تعرف|تعرّف|يذكر|تذكر|يحدد|تحدد|يسمّي|تسمي|يشرح|تشرح|يوضح|توضح|يقارن|تقارن|يصنف|تصنف|يلخص|تلخص|يفسر|تفسر|"
          r"يطبق|تطبق|يستخدم|تستخدم|يحل|تحل|يكتب|تكتب|يبني|تبني|ينفذ|تنفذ|يحسب|تحسب|يصمم|تصمم|ينشئ|تنشئ|يطور|تطور|يتتبع|تتتبع|"
          r"يصلح|تصلح|يحلل|تحلل|يختبر|تختبر|يقيّم|يقيم|تقيم|يبرر|تبرر|يختار|تختار|يتنبأ|تتنبأ|يحوّل|تحول|يرسم|ترسم|يخطط|تخطط|يعرض|تعرض|"
          r"يشغّل|تشغل|يعدّل|تعدل|يقيس|تقيس|يستنتج|تستنتج|يميز|تميز|يرتب|ترتب|يجرب|تجرب|يناقش|تناقش)",
}
LOW_BLOOM = {"remember", "understand", "تذكر", "فهم"}
PLACEHOLDER = re.compile(r"lorem ipsum|\bTBD\b|\[insert|XXX|TODO", re.I)


def validate(spec):
    errs, warns = [], []
    c = spec.get("course", {})
    lang = "ar" if str(c.get("language", "")).startswith("ar") else "en"
    outs = {o["id"]: o for o in c.get("outcomes", [])}
    if not outs:
        errs.append("course.outcomes is empty — write 3–8 measurable outcomes first (backward design)")
    taught = {k: [] for k in outs}
    assessed = {k: [] for k in outs}
    for a in c.get("assessment", []):
        for oid in a.get("outcomes", []):
            assessed.setdefault(oid, []).append(a["name"])
    wsum = sum(float(a.get("weight", 0)) for a in c.get("assessment", []))
    if c.get("assessment") and abs(wsum - 1) > 0.001:
        errs.append(f"assessment weights sum to {wsum:.0%}, not 100%")
    blooms = set()
    n = 0
    for m in spec.get("modules", []):
        for s in m.get("sessions", []):
            n += 1
            sid = s.get("id", f"S{n:02d}")
            minutes = int(s.get("minutes", c.get("duration", {}).get("minutes", 90)))
            if not s.get("objectives"):
                errs.append(f"{sid}: no objectives")
            for o in s.get("objectives", []):
                txt = (o.get("verb", "") + " " + o.get("text", "")).strip() if isinstance(o, dict) else str(o)
                if not re.match(MEASURABLE[lang], txt.strip(), re.I) and not re.match(MEASURABLE["en"], txt.strip(), re.I):
                    warns.append(f"{sid}: objective may not be measurable (start with an action verb): “{txt[:60]}”")
            for oid in s.get("outcomes", []) or m.get("outcomes", []):
                if oid not in outs:
                    errs.append(f"{sid}: refers to unknown outcome {oid}")
                taught.setdefault(oid, []).append(sid)
            plan = s.get("plan", [])
            if plan:
                tot = sum(int(p.get("minutes", 0)) for p in plan)
                if abs(tot - minutes) > 5:
                    errs.append(f"{sid}: plan adds up to {tot} min but the session is {minutes} min")
                for p in plan:
                    if int(p.get("minutes", 0)) > 20 and re.search(r"lecture|explain|شرح|محاضرة|direct", (p.get("phase", "") + p.get("title", "")), re.I):
                        warns.append(f"{sid}: a {p['minutes']}-min explanation block — split it with a check or practice (attention drops after ~15 min)")
                if not any(re.search(r"practi|activity|lab|exercise|you do|we do|تطبيق|نشاط|تمرين|معمل|عملي", (p.get("phase", "") + p.get("title", "")), re.I) for p in plan) \
                        and not s.get("activities") and not s.get("lab"):
                    warns.append(f"{sid}: no practice — every session needs students DOING something")
            else:
                warns.append(f"{sid}: no timed plan (instructor guide will have no timing)")
            if not s.get("quiz") and not s.get("exercises"):
                warns.append(f"{sid}: no check for understanding (quiz or exercises)")
            elif len(s.get("quiz", [])) and len(s.get("quiz", [])) < 3:
                warns.append(f"{sid}: only {len(s['quiz'])} quiz item(s) — 3–5 gives a more reliable check")
            for k, q in enumerate(s.get("quiz", []), 1):
                if q.get("answer") is None:
                    errs.append(f"{sid} quiz {k}: no answer (the answer key would be empty)")
                if q.get("options") and isinstance(q.get("answer"), int) and not 0 <= q["answer"] < len(q["options"]):
                    errs.append(f"{sid} quiz {k}: answer index {q['answer']} out of range")
                if q.get("bloom"):
                    blooms.add(str(q["bloom"]).lower())
                for oid in q.get("outcomes", s.get("outcomes", [])):
                    if sid not in assessed.setdefault(oid, []):
                        assessed[oid].append(sid)
            if not s.get("misconceptions"):
                warns.append(f"{sid}: no common mistakes listed (the instructor guide is weaker without them)")
            if not s.get("slides") and not s.get("content"):
                errs.append(f"{sid}: no slides and no content — write the lesson")
    for oid in outs:
        if not taught.get(oid):
            errs.append(f"outcome {oid} is never taught (no session lists it)")
        if not assessed.get(oid):
            errs.append(f"outcome {oid} is never assessed (no quiz item or assessment component)")
    for o in outs.values():
        if o.get("bloom"):
            blooms.add(str(o["bloom"]).lower())
    if blooms and blooms <= LOW_BLOOM:
        warns.append("every outcome/question is remember/understand — add apply/analyze/create work")
    txt = json.dumps(spec, ensure_ascii=False)
    for m in PLACEHOLDER.finditer(txt):
        errs.append(f"placeholder text left: “{txt[max(0, m.start() - 30):m.end() + 20]}”")
        break
    return errs, warns


def main(argv=None):
    a = argv or sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    spec = json.loads(Path(a[0]).read_text(encoding="utf-8"))
    errs, warns = validate(spec)
    for e in errs:
        print("ERROR:", e)
    for w in warns:
        print("WARN: ", w)
    print("✅ course spec OK" if not errs else f"❌ {len(errs)} error(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
