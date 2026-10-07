#!/usr/bin/env python3
"""build_course.py — one course spec → the complete teaching package.

    run.sh build_course.py course_spec.json out/<course-folder> [--only S01,S02] [--offline] [--no-pdf]
                                                               [--skip slides,docs,sheets]

Output (every file also has its editable source spec next to it in _specs/):
  00_Course_Plan.docx/.pdf        plan for the school/academy: outcomes, map, schedule, assessment, rubrics
  00_Syllabus.docx/.pdf           the student-facing version
  00_Instructor_Guide.docx/.pdf   every session: timing, what to say/do, misconceptions, answers
  Schedule.xlsx · Gradebook.xlsx · Question_Bank.xlsx
  S01_<title>/  Slides.pptx (+ speaker notes) · Lesson.docx/.pdf (full content) · Handout/Worksheet ·
                Lab.docx/.pdf · Quiz.docx/.pdf + Quiz_Answer_Key.docx/.pdf
  README.md                       index of everything, alignment matrix, what to check

Run validate_course.py on the spec FIRST — it refuses to build a course whose outcomes, timing or
assessments do not line up.
"""
from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SK = HERE.parents[1]
for p in (HERE, SK / "premium-design-kit" / "lib", SK / "premium-documents" / "scripts",
          SK / "premium-presentations" / "scripts", SK / "premium-spreadsheets" / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from pdk.text import spec_is_rtl  # noqa: E402

T = {
    "en": {"plan": "Course Plan", "syllabus": "Syllabus", "guide": "Instructor Guide", "overview": "Overview",
           "audience": "Who it is for", "outcomes": "Learning outcomes", "map": "Course map", "schedule": "Schedule",
           "assessment": "Assessment", "rubrics": "Rubrics", "materials": "Materials & tools", "policies": "Policies",
           "session": "Session", "module": "Module", "objectives": "Objectives", "plan_t": "Session plan",
           "time": "Time", "phase": "Phase", "teacher": "Teacher", "students": "Students", "misconceptions": "Common mistakes",
           "support": "Support", "extend": "Stretch", "homework": "Homework", "answers": "Answers", "lesson": "Lesson notes",
           "handout": "Handout", "worksheet": "Worksheet", "lab": "Lab", "quiz": "Quiz", "key": "Answer key",
           "prereq": "Prerequisites", "description": "Description", "outcome": "Outcome", "bloom": "Level",
           "taught": "Taught in", "assessed": "Assessed by", "weight": "Weight", "component": "Component",
           "activity": "Activity", "deliverable": "Deliverable", "solution": "Solution", "setup": "Setup",
           "checkpoints": "Checkpoints", "prep": "Before the session", "recap": "Recap", "agenda": "Today",
           "questions": "Questions?", "min": "min", "minutes": "minutes", "sessions": "sessions", "level": "Level",
           "exercises": "Exercises", "duration": "Duration", "mode": "Delivery", "instructions": "Answer all questions."},
    "ar": {"plan": "خطة الكورس", "syllabus": "دليل الطالب", "guide": "دليل المدرّب", "overview": "نظرة عامة",
           "audience": "الفئة المستهدفة", "outcomes": "نواتج التعلم", "map": "خريطة الكورس", "schedule": "الجدول الزمني",
           "assessment": "التقييم", "rubrics": "معايير التصحيح", "materials": "الأدوات والمواد", "policies": "السياسات",
           "session": "الحصة", "module": "الوحدة", "objectives": "الأهداف", "plan_t": "خطة الحصة",
           "time": "الوقت", "phase": "المرحلة", "teacher": "المدرّب", "students": "الطلاب", "misconceptions": "أخطاء شائعة",
           "support": "للدعم", "extend": "للتميّز", "homework": "الواجب", "answers": "الإجابات", "lesson": "شرح الدرس",
           "handout": "ملزمة", "worksheet": "ورقة عمل", "lab": "معمل", "quiz": "اختبار قصير", "key": "نموذج الإجابة",
           "prereq": "المتطلبات السابقة", "description": "الوصف", "outcome": "الناتج", "bloom": "المستوى",
           "taught": "يُدرّس في", "assessed": "يُقيّم في", "weight": "الوزن", "component": "عنصر التقييم",
           "activity": "نشاط", "deliverable": "التسليم", "solution": "الحل", "setup": "التجهيز",
           "checkpoints": "نقاط التحقق", "prep": "قبل الحصة", "recap": "الخلاصة", "agenda": "النهارده",
           "questions": "أسئلة؟", "min": "د", "minutes": "دقيقة", "sessions": "حصص", "level": "المستوى",
           "exercises": "تمارين", "duration": "المدة", "mode": "طريقة التقديم", "instructions": "أجب عن جميع الأسئلة."},
}


def slug(s, n=34):
    s = re.sub(r"[^\w؀-ۿ]+", "_", str(s)).strip("_")
    return s[:n] or "session"


class CourseBuilder:
    def __init__(self, spec: dict, out: Path, *, offline=False, pdf=True, only=None, skip=()):
        self.spec = spec
        self.c = spec["course"]
        self.out = out
        self.offline = offline
        self.pdf = pdf
        self.only = set(only or [])
        self.skip = set(skip)
        self.rtl = spec_is_rtl({"language": self.c.get("language", ""), "t": self.c.get("title", "")})
        self.L = T["ar" if self.rtl else "en"]
        self.slides_rtl = str(self.c.get("slides_language", self.c.get("language", "ar" if self.rtl else "en"))).startswith("ar")
        self.theme = self.c.get("theme", "plain-pro")
        self.brand = self.c.get("brand")
        self.files = []
        self.warnings = []
        self.specs = out / "_specs"
        self.specs.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------ helpers
    def sessions(self):
        n = 0
        for m in self.spec.get("modules", []):
            for s in m.get("sessions", []):
                n += 1
                s.setdefault("id", f"S{n:02d}")
                s.setdefault("minutes", self.c.get("duration", {}).get("minutes", 90))
                yield m, n, s

    def base(self, **kw):
        d = {"theme": self.theme, "language": "ar" if self.rtl else "en", "project": slug(self.c.get("title", "course"), 40),
             "footer": self.c.get("org", "")}
        if self.brand:
            d["brand"] = self.brand
        d.update(kw)
        return d

    def doc(self, spec, path: Path):
        from build_doc import build as build_doc
        sp = self.specs / (path.stem + ".json")
        sp.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
        rep = build_doc(sp, path, pdf=self.pdf, docx=True, offline=self.offline)
        self.files += rep["files"]
        self.warnings += [f"{path.name}: {w}" for w in rep["warnings"] if "auto-picked" not in w]

    def deck(self, spec, path: Path):
        import build_deck
        sp = self.specs / (path.parent.name + "_" + path.stem + ".json")
        sp.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
        build_deck.build(str(sp), str(path), offline=self.offline)
        self.files.append(str(path))
        import subprocess
        r = subprocess.run([sys.executable, str(SK / "premium-presentations" / "scripts" / "validate_deck.py"), str(path)],
                           capture_output=True, text=True)
        if r.returncode:
            self.warnings.append(f"{path.parent.name}/{path.name}: " + " | ".join(r.stdout.strip().splitlines()[1:5]))

    def sheet(self, spec, path: Path):
        from build_sheet import SheetBuilder
        sp = self.specs / (path.stem + ".json")
        sp.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
        rep = SheetBuilder(spec, self.specs).build(path, recalc=True)
        self.files.append(str(path))
        if rep.get("errors"):
            self.warnings.append(f"{path.name}: formula errors {rep['errors'][:4]}")

    # ------------------------------------------------------------ alignment
    def alignment(self):
        outs = self.c.get("outcomes", [])
        taught = {o["id"]: [] for o in outs}
        assessed = {o["id"]: [] for o in outs}
        for m, n, s in self.sessions():
            for oid in s.get("outcomes", []) or m.get("outcomes", []):
                taught.setdefault(oid, []).append(s["id"])
            for q in s.get("quiz", []):
                for oid in q.get("outcomes", s.get("outcomes", [])):
                    if s["id"] not in assessed.setdefault(oid, []):
                        assessed[oid].append(s["id"])
        for a in self.c.get("assessment", []):
            for oid in a.get("outcomes", []):
                assessed.setdefault(oid, []).append(a["name"])
        return taught, assessed

    # ------------------------------------------------------------ course-level documents
    def course_plan(self):
        c, L = self.c, self.L
        aud = c.get("audience", {})
        dur = c.get("duration", {})
        blocks = [{"type": "heading", "text": L["overview"]},
                  {"type": "paragraph", "style": "lead", "text": c.get("description", "")}]
        facts = [(L["audience"], aud.get("description") or " · ".join(str(v) for v in (aud.get("school"), aud.get("grade"), aud.get("age"), aud.get("level")) if v)),
                 (L["duration"], f"{dur.get('sessions', sum(1 for _ in self.sessions()))} {L['sessions']} × {dur.get('minutes', 90)} {L['minutes']}" + (f" · {dur['weeks']} weeks" if dur.get("weeks") and not self.rtl else (f" · {dur['weeks']} أسابيع" if dur.get("weeks") else ""))),
                 (L["mode"], c.get("mode", "")), (L["prereq"], c.get("prerequisites", ""))]
        blocks.append({"type": "kv", "items": [[k, v] for k, v in facts if v]})
        stats = [{"value": str(dur.get("sessions", sum(1 for _ in self.sessions()))), "label": L["sessions"]},
                 {"value": str(len(c.get("outcomes", []))), "label": L["outcomes"]},
                 {"value": str(sum(len(s.get("quiz", [])) for _, _, s in self.sessions())), "label": L["quiz"]}]
        blocks.append({"type": "stats", "items": stats})
        blocks += [{"type": "heading", "text": L["outcomes"]},
                   {"type": "table", "headers": ["#", L["outcome"], L["bloom"]],
                    "rows": [[o["id"], o["text"], o.get("bloom", "")] for o in c.get("outcomes", [])], "widths": [10, 70, 20]}]
        taught, assessed = self.alignment()
        blocks.append({"type": "table", "headers": ["#", L["taught"], L["assessed"]],
                       "rows": [[o["id"], ", ".join(taught.get(o["id"], [])) or "—", ", ".join(assessed.get(o["id"], [])) or "—"]
                                for o in c.get("outcomes", [])], "caption": "Alignment matrix" if not self.rtl else "مصفوفة المواءمة"})
        blocks.append({"type": "heading", "text": L["map"]})
        for m in self.spec.get("modules", []):
            items = [{"title": f"{s.get('id')} · {s['title']}", "text": "; ".join(o["text"] if isinstance(o, dict) else o for o in s.get("objectives", [])[:3])}
                     for s in m.get("sessions", [])]
            blocks += [{"type": "heading", "level": 2, "text": m["title"]}]
            if m.get("summary"):
                blocks.append({"type": "paragraph", "text": m["summary"]})
            blocks.append({"type": "steps", "items": items})
        blocks += [{"type": "heading", "text": L["schedule"]},
                   {"type": "schedule", "items": [{"time": s["id"], "duration": f"{s['minutes']} {L['min']}", "title": s["title"],
                                                   "text": " → ".join(p.get("phase", p.get("title", "")) for p in s.get("plan", []))}
                                                  for _, _, s in self.sessions()]}]
        if c.get("assessment"):
            blocks += [{"type": "heading", "text": L["assessment"]},
                       {"type": "table", "headers": [L["component"], L["weight"], L["description"], L["outcomes"]],
                        "rows": [[a["name"], f"{round(a.get('weight', 0) * 100)}%", a.get("description", ""), ", ".join(a.get("outcomes", []))]
                                 for a in c["assessment"]], "widths": [22, 10, 50, 18]}]
            blocks.append({"type": "chart", "chart": {"type": "donut", "categories": [a["name"] for a in c["assessment"]],
                                                      "series": [{"values": [round(a.get("weight", 0) * 100) for a in c["assessment"]]}], "unit": "%"},
                           "height_in": 2.8})
        for r in c.get("rubrics", []):
            blocks += [{"type": "heading", "level": 2, "text": r.get("title", L["rubrics"])}, {"type": "rubric", **r}]
        if c.get("materials") or c.get("tools"):
            blocks += [{"type": "heading", "text": L["materials"]}, {"type": "bullets", "items": c.get("materials", []) + c.get("tools", [])}]
        if c.get("policies"):
            blocks += [{"type": "heading", "text": L["policies"]}, {"type": "bullets", "items": c["policies"]}]
        spec = self.base(type="course_plan", meta={"title": c["title"], "subtitle": c.get("subtitle", ""), "kicker": L["plan"],
                                                    "author": c.get("instructor", ""), "prepared_for": aud.get("school", c.get("org", "")),
                                                    "org": c.get("org", ""), "date": c.get("date", "")},
                         cover={"style": c.get("cover_style", "photo" if c.get("cover_image") else "band"), "image": c.get("cover_image")},
                         blocks=blocks)
        self.doc(spec, self.out / "00_Course_Plan")

    def syllabus(self):
        c, L = self.c, self.L
        blocks = [{"type": "paragraph", "style": "lead", "text": c.get("description", "")},
                  {"type": "heading", "text": L["outcomes"], "numbered": False},
                  {"type": "checklist", "items": [o["text"] for o in c.get("outcomes", [])]},
                  {"type": "heading", "text": L["schedule"], "numbered": False},
                  {"type": "table", "headers": ["#", L["session"], L["objectives"]],
                   "rows": [[s["id"], s["title"], "; ".join((o["text"] if isinstance(o, dict) else o) for o in s.get("objectives", [])[:2])]
                            for _, _, s in self.sessions()], "widths": [8, 34, 58]}]
        if c.get("assessment"):
            blocks += [{"type": "heading", "text": L["assessment"], "numbered": False},
                       {"type": "stats", "items": [{"value": f"{round(a.get('weight', 0) * 100)}%", "label": a["name"]} for a in c["assessment"][:4]]}]
        if c.get("policies"):
            blocks += [{"type": "heading", "text": L["policies"], "numbered": False}, {"type": "bullets", "items": c["policies"]}]
        spec = self.base(type="syllabus", numbered=False, meta={"title": c["title"], "subtitle": L["syllabus"], "kicker": c.get("org", ""),
                                                                "author": c.get("instructor", "")},
                         cover={"style": "band", "image": c.get("cover_image")}, blocks=blocks)
        self.doc(spec, self.out / "00_Syllabus")

    def instructor_guide(self):
        L = self.L
        blocks = []
        for m, n, s in self.sessions():
            blocks.append({"type": "section", "title": f"{s['id']} · {s['title']}", "intro": s.get("summary", "")})
            blocks.append({"type": "kv", "items": [[L["duration"], f"{s['minutes']} {L['minutes']}"],
                                                   [L["outcomes"], ", ".join(s.get("outcomes", []))]] +
                           ([[L["materials"], ", ".join(s["materials"])]] if s.get("materials") else [])})
            if s.get("prep"):
                blocks += [{"type": "callout", "kind": "note", "title": L["prep"], "text": s["prep"]}]
            blocks += [{"type": "heading", "level": 2, "text": L["objectives"], "numbered": False},
                       {"type": "bullets", "items": [((o.get("verb", "") + " " + o.get("text", "")).strip() if isinstance(o, dict) else o) for o in s.get("objectives", [])]}]
            if s.get("plan"):
                t = 0
                rows = []
                for p in s["plan"]:
                    rows.append({"time": f"{t:02d}–{t + int(p.get('minutes', 0)):02d}", "duration": f"{p.get('minutes')} {L['min']}",
                                 "title": p.get("phase", "") + (" — " + p["title"] if p.get("title") else ""),
                                 "text": "  \n".join(x for x in ((("**" + L["teacher"] + ":** " + p["teacher"]) if p.get("teacher") else ""),
                                                               (("**" + L["students"] + ":** " + p["students"]) if p.get("students") else ""),
                                                               p.get("notes", "")) if x)})
                    t += int(p.get("minutes", 0))
                blocks += [{"type": "heading", "level": 2, "text": L["plan_t"], "numbered": False}, {"type": "schedule", "items": rows}]
            if s.get("misconceptions"):
                blocks += [{"type": "heading", "level": 2, "text": L["misconceptions"], "numbered": False},
                           {"type": "table", "headers": ["✗", "✓"], "rows": [[x.get("wrong", ""), x.get("fix", "")] for x in s["misconceptions"]]}]
            diff = s.get("differentiation", {})
            if diff:
                blocks.append({"type": "two_column", "left": [{"type": "callout", "kind": "info", "title": L["support"], "text": diff.get("support", "")}],
                               "right": [{"type": "callout", "kind": "success", "title": L["extend"], "text": diff.get("extend", "")}]})
            sols = [a for a in s.get("activities", []) if a.get("solution")]
            if sols or s.get("quiz"):
                blocks.append({"type": "heading", "level": 2, "text": L["answers"], "numbered": False})
                for a in sols:
                    blocks.append({"type": "paragraph", "text": f"**{a['title']}**"})
                    blocks.append({"type": "code", "code": a["solution"], "lang": a.get("lang")} if a.get("solution_is_code", True) and "\n" in a["solution"]
                                  else {"type": "paragraph", "text": a["solution"]})
                if s.get("quiz"):
                    blocks.append({"type": "questions", "items": s["quiz"], "show_answers": True})
        spec = self.base(type="instructor_guide", numbered=False, toc=True,
                         meta={"title": self.c["title"], "subtitle": L["guide"], "kicker": L["guide"], "author": self.c.get("instructor", "")},
                         cover={"style": "band", "image": self.c.get("cover_image")}, blocks=blocks)
        self.doc(spec, self.out / "00_Instructor_Guide")

    # ------------------------------------------------------------ per-session
    def session_pack(self, m, n, s):
        L = self.L
        folder = self.out / f"{s['id']}_{slug(s['title'])}"
        folder.mkdir(parents=True, exist_ok=True)
        meta_course = self.c.get("title", "")
        if "slides" not in self.skip:
            self.deck(self.session_deck(m, n, s), folder / "Slides.pptx")
        if "docs" in self.skip:
            return
        if s.get("content"):
            self.doc(self.base(type="handout", meta={"title": s["title"], "kicker": f"{meta_course} · {L['session']} {n}"},
                               blocks=[{"type": "box", "title": L["objectives"], "blocks": [{"type": "checklist", "items": [
                                   ((o.get("verb", "") + " " + o.get("text", "")).strip() if isinstance(o, dict) else o) for o in s.get("objectives", [])]}]}]
                               + s["content"] + ([{"type": "callout", "kind": "tip", "title": L["homework"], "text": s["homework"]}] if s.get("homework") else [])),
                     folder / "Lesson")
        if s.get("exercises") or s.get("activities"):
            blocks = []
            for a in s.get("activities", []):
                blocks += [{"type": "heading", "text": f"{L['activity']}: {a['title']}", "numbered": False},
                           {"type": "steps", "items": [{"title": st if isinstance(st, str) else st.get("title", ""), "text": "" if isinstance(st, str) else st.get("text", "")} for st in a.get("steps", [])]}]
                if a.get("deliverable"):
                    blocks.append({"type": "callout", "kind": "success", "title": L["deliverable"], "text": a["deliverable"]})
                if a.get("space_lines"):
                    blocks.append({"type": "note_lines", "lines": a["space_lines"]})
            if s.get("exercises"):
                blocks += [{"type": "heading", "text": L["exercises"], "numbered": False}, {"type": "questions", "items": s["exercises"]}]
            self.doc(self.base(type="worksheet", meta={"title": s["title"], "kicker": f"{meta_course} · {L['session']} {n}",
                                                       "instructions": s.get("worksheet_instructions", "")}, blocks=blocks),
                     folder / "Worksheet")
        if s.get("lab"):
            lab = s["lab"]
            blocks = []
            if lab.get("setup"):
                blocks += [{"type": "heading", "text": L["setup"], "numbered": False}, {"type": "checklist", "items": lab["setup"]}]
            for i, st in enumerate(lab.get("steps", []), 1):
                blocks += [{"type": "heading", "level": 2, "text": f"{i}. {st.get('title', '')}", "numbered": False}]
                if st.get("text"):
                    blocks.append({"type": "paragraph", "text": st["text"]})
                if st.get("code"):
                    blocks.append({"type": "code", "code": st["code"], "lang": st.get("lang", lab.get("lang"))})
                if st.get("check"):
                    blocks.append({"type": "callout", "kind": "success", "title": "تحقق" if self.rtl else "Check", "text": st["check"]})
            if lab.get("checkpoints"):
                blocks += [{"type": "heading", "text": L["checkpoints"], "numbered": False}, {"type": "checklist", "items": lab["checkpoints"]}]
            self.doc(self.base(type="lab_sheet", meta={"title": lab.get("title", s["title"]), "kicker": f"{L['lab']} · {L['session']} {n}",
                                                       "instructions": lab.get("goal", "")}, blocks=blocks), folder / "Lab")
        if s.get("quiz"):
            for key, show in (("Quiz", False), ("Quiz_Answer_Key", True)):
                self.doc(self.base(type="answer_key" if show else "exam",
                                   meta={"title": f"{L['quiz']} — {s['title']}" + (f" ({L['key']})" if show else ""),
                                         "course": meta_course, "duration": s.get("quiz_minutes", ""),
                                         "instructions": "" if show else L["instructions"]},
                                   blocks=[{"type": "questions", "items": s["quiz"], "show_answers": show}]), folder / key)

    def session_deck(self, m, n, s):
        L = self.L if self.slides_rtl == self.rtl else T["ar" if self.slides_rtl else "en"]
        deck = {"theme": self.theme, "language": "ar" if self.slides_rtl else "en", "footer": f"{self.c.get('title', '')} · {L['session']} {n}",
                "project": slug(self.c.get("title", "course"), 40), "icon_set": self.c.get("icon_set", "material-symbols")}
        if self.brand:
            deck["brand"] = self.brand
        if s.get("slides"):                       # authored deck — the recommended path
            deck["slides"] = copy.deepcopy(s["slides"])
            return deck
        # auto deck (fallback): good structure, but authored slides are always better
        sl = [{"type": "image_hero" if s.get("image") else "title", "kicker": f"{L['session']} {n} · {m.get('title', '')}",
               "title": s["title"], "subtitle": s.get("summary", ""), **({"image": s["image"]} if s.get("image") else {})}]
        if s.get("objectives"):
            sl.append({"type": "objectives", "title": L["objectives"], "items": [o if isinstance(o, dict) else {"text": o} for o in s["objectives"][:6]]})
        if s.get("plan"):
            sl.append({"type": "agenda", "title": L["agenda"], "items": [p.get("title") or p.get("phase", "") for p in s["plan"]][:7]})
        sec = {"title": None, "texts": [], "bullets": [], "code": None}

        def plain(t):
            return re.sub(r"\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`", lambda m: m.group(1) or m.group(2) or m.group(3), str(t))

        def flush(keep=False):
            title = sec["title"]
            if not title:
                return
            if not (sec["code"] or sec["texts"] or sec["bullets"]):
                return
            if sec["code"]:
                sl.append({"type": "code", "title": sec["title"], "code": sec["code"]["code"], "lang": sec["code"].get("lang"),
                           "caption": plain(sec["texts"][0]) if sec["texts"] else ""})
                rest = sec["texts"][1:] + sec["bullets"]
                if rest:
                    sl.append({"type": "bullets", "title": sec["title"], "bullets": [plain(x) if isinstance(x, str) else x for x in rest][:5]})
            else:
                items = [plain(x) if isinstance(x, str) else x for x in sec["texts"] + sec["bullets"]]
                if len(items) == 1:
                    sl.append({"type": "big_statement", "statement": items[0] if isinstance(items[0], str) else items[0].get("point", ""),
                               "support": sec["title"]})
                elif items:
                    sl.append({"type": "bullets", "title": sec["title"], "bullets": items[:5]})
            sec.update({"title": title if keep else None, "texts": [], "bullets": [], "code": None})

        for b in s.get("content", []):
            t = b.get("type")
            if t in ("heading", "section"):
                flush()
                sec["title"] = b.get("text") or b.get("title")
            elif t == "bullets":
                sec["bullets"] += [i if isinstance(i, (str, dict)) else str(i) for i in b.get("items", [])]
            elif t == "paragraph":
                first = re.split(r"(?<=[.!؟?])\s", b.get("text", ""))[0]
                sec["texts"].append(first[:160])
            elif t == "code":
                if sec["code"]:
                    flush(keep=True)
                sec["code"] = b
            elif t == "callout":
                sec["bullets"].append({"point": b.get("title", ""), "detail": plain(b.get("text", ""))})
            elif t == "steps":
                flush(keep=True)
                sl.append({"type": "process", "title": sec["title"] or "", "steps": [{"label": plain(i.get("title", "")), "detail": plain(i.get("text", ""))} for i in b.get("items", [])[:5]]})
            elif t == "table":
                flush(keep=True)
                sl.append({"type": "table", "title": sec["title"] or b.get("caption", ""), "headers": b.get("headers", []), "rows": [[plain(c) for c in r] for r in b.get("rows", [])[:7]]})
            elif t == "definition":
                flush(keep=True)
                sl.append({"type": "definition", "term": b.get("term", ""), "definition": plain(b.get("text", "")), "example": plain(b.get("example", ""))})
            elif t == "image":
                flush(keep=True)
                sl.append({"type": "image_split", "title": sec["title"] or "", "image": b.get("image"), "text": plain(b.get("caption", ""))})
        flush()
        for a in s.get("activities", [])[:2]:
            sl.append({"type": "activity", "title": a["title"], "minutes": a.get("minutes"), "mode": a.get("mode", ""),
                       "icon": a.get("icon", "group work"), "steps": [x if isinstance(x, str) else x.get("title", "") for x in a.get("steps", [])][:6],
                       "deliverable": a.get("deliverable", "")})
        for q in [q for q in s.get("quiz", []) if q.get("options")][:3]:
            sl.append({"type": "quiz", "question": q["q"], "options": q["options"][:4], "answer": q.get("answer")})
            sl.append({"type": "quiz", "question": q["q"], "options": q["options"][:4], "answer": q.get("answer"), "reveal": True,
                       "explanation": q.get("explanation", "")})
        if s.get("recap"):
            sl.append({"type": "icon_grid", "title": L["recap"], "items": s["recap"][:6]})
        sl.append({"type": "closing", "title": L["questions"], "contact": (L["homework"] + ": " + s["homework"]) if s.get("homework") else ""})
        notes = {i: p for i, p in enumerate(s.get("plan", []))}
        if notes:
            sl[0]["notes"] = [f"{p.get('minutes')}′ {p.get('phase', '')}: {p.get('teacher', '')}" for p in s["plan"]]
        deck["slides"] = sl
        return deck

    # ------------------------------------------------------------ workbooks
    def workbooks(self):
        from presets import gradebook, question_bank, schedule
        lang = "ar" if self.rtl else "en"
        rows = []
        start = self.c.get("start_date")
        import datetime as dt
        step = int(self.c.get("days_between_sessions", 7))
        for i, (m, n, s) in enumerate(self.sessions()):
            date = (dt.date.fromisoformat(start) + dt.timedelta(days=i * step)).isoformat() if start else None
            rows.append({"n": n, "date": date or s.get("date"), "module": m.get("title", ""), "title": s["title"],
                         "outcomes": ", ".join(s.get("outcomes", [])), "activity": ", ".join(a["title"] for a in s.get("activities", [])),
                         "assessment": (self.L["quiz"] if s.get("quiz") else ""), "hours": round(s["minutes"] / 60, 2)})
        sp = schedule(rows, title=f"{self.c['title']} — {self.L['schedule']}", language=lang, theme=self.theme)
        self.sheet(sp, self.out / "Schedule.xlsx")
        comps = self.c.get("assessment") or [{"name": self.L["quiz"], "weight": 1.0}]
        students = self.c.get("students") or [f"{'طالب' if self.rtl else 'Student'} {i + 1}" for i in range(int(self.c.get("audience", {}).get("size", 20)))]
        gb = gradebook(students, [{"name": a["name"], "max": a.get("max", 100), "weight": a.get("weight", 0)} for a in comps],
                       language=lang, theme=self.theme, course=self.c["title"], pass_mark=self.c.get("pass_mark", 50))
        self.sheet(gb, self.out / "Gradebook.xlsx")
        qs = []
        for m, n, s in self.sessions():
            for k, q in enumerate(s.get("quiz", []) + s.get("exercises", []), 1):
                qs.append({"id": f"{s['id']}-Q{k:02d}", "unit": s["id"], "outcome": ", ".join(q.get("outcomes", s.get("outcomes", []))),
                           "bloom": q.get("bloom", ""), "kind": q.get("kind", "mcq" if q.get("options") else "short"), "q": q.get("q", ""),
                           "options": q.get("options"), "answer": q.get("answer"), "points": q.get("points", 1), "difficulty": q.get("difficulty", "")})
        if qs:
            self.sheet(question_bank(qs, title=f"{self.c['title']} — {'بنك الأسئلة' if self.rtl else 'Question bank'}", language=lang,
                                     theme=self.theme), self.out / "Question_Bank.xlsx")

    # ------------------------------------------------------------ run
    def run(self):
        self.out.mkdir(parents=True, exist_ok=True)
        if not self.only:
            if "docs" not in self.skip:
                self.course_plan()
                self.syllabus()
                self.instructor_guide()
            if "sheets" not in self.skip:
                self.workbooks()
        for m, n, s in self.sessions():
            if self.only and s["id"] not in self.only:
                continue
            self.session_pack(m, n, s)
        self.readme()
        return {"files": self.files, "warnings": self.warnings}

    def readme(self):
        taught, assessed = self.alignment()
        lines = [f"# {self.c['title']}", "", self.c.get("description", ""), "", "## Files", ""]
        for f in sorted(set(self.files)):
            lines.append(f"- `{Path(f).relative_to(self.out)}`")
        lines += ["", "## Alignment", "", "| Outcome | Taught | Assessed |", "|---|---|---|"]
        for o in self.c.get("outcomes", []):
            lines.append(f"| {o['id']} {o['text']} | {', '.join(taught.get(o['id'], [])) or '—'} | {', '.join(assessed.get(o['id'], [])) or '—'} |")
        lines += ["", "Editable sources for every file are in `_specs/` (rebuild with the skills' scripts)."]
        (self.out / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv=None):
    a = list(argv or sys.argv[1:])
    only, skip = [], []
    for opt, dest in (("--only", only), ("--skip", skip)):
        if opt in a:
            i = a.index(opt)
            if i + 1 < len(a):
                dest += a[i + 1].split(",")
                del a[i:i + 2]
    flags = [x for x in a if x.startswith("--")]
    args = [x for x in a if not x.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        return 1
    spec = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    from validate_course import validate
    errs, warns = validate(spec)
    if errs:
        print("❌ course spec problems — fix before building:")
        for e in errs:
            print("  -", e)
        return 2
    for w in warns:
        print("WARN:", w)
    rep = CourseBuilder(spec, Path(args[1]), offline="--offline" in flags, pdf="--no-pdf" not in flags, only=only, skip=skip).run()
    print(f"✅ {len(rep['files'])} files in {args[1]}")
    for w in rep["warnings"]:
        print("WARN:", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
