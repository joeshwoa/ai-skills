"""Ready-made workbook specs for common jobs (fill with REAL data, then build_sheet.py).

    from presets import gradebook
    spec = gradebook(["Mariam", "Youssef"], [{"name": "Quiz 1", "max": 10, "weight": 0.1}, …], language="ar")

Each returns a spec dict; save it as JSON and build, or tweak it first. All of them are formula-driven:
change a score or a weight and every total, grade and chart updates."""
from __future__ import annotations


def _ar(lang):
    return str(lang).startswith("ar")


def gradebook(students, assessments, *, title=None, language="en", theme="school-bright", pass_mark=50,
              grade_bands=None, course=""):
    """students: names (or dicts with name/id/class); assessments: [{"name","max","weight"}] — weights sum to 1."""
    ar = _ar(language)
    names = [s["name"] if isinstance(s, dict) else s for s in students]
    cols = [{"name": "الطالب" if ar else "Student", "width": 26}]
    for a in assessments:
        cols.append({"name": a["name"], "type": "score", "input": True, "width": 11})
    total_terms = "+".join(f"[{a['name']}]/{a['max']}*{a['weight']}" for a in assessments)
    first_a, last_a = assessments[0]["name"], assessments[-1]["name"]
    cols.append({"name": "النسبة" if ar else "Percent", "type": "pct", "bold": True,
                 "formula": f'=IF(COUNT([{first_a}]:[{last_a}])=0,"",ROUND(({total_terms}),4))'})
    bands = grade_bands or ([(0.85, "ممتاز"), (0.75, "جيد جداً"), (0.65, "جيد"), (pass_mark / 100, "مقبول"), (0, "راسب")] if ar else
                            [(0.85, "A"), (0.75, "B"), (0.65, "C"), (pass_mark / 100, "D"), (0, "F")])
    pct_col = "النسبة" if ar else "Percent"
    ifs = "".join(f'IF([{pct_col}]>={b},"{g}",' for b, g in bands[:-1]) + f'"{bands[-1][1]}"' + ")" * (len(bands) - 1)
    cols.append({"name": "التقدير" if ar else "Grade", "formula": f'=IF([{pct_col}]="","",' + ifs + ")", "align": "center", "bold": True})
    rows = [[n] + [None] * len(assessments) for n in names]
    sheet = {"name": "الدرجات" if ar else "Grades", "title": title or ((("كشف درجات " + course) if ar else ("Gradebook — " + course)).strip(" —")),
             "subtitle": ("الأوزان: " if ar else "Weights: ") + ", ".join(f"{a['name']} {int(a['weight'] * 100)}%" for a in assessments),
             "columns": cols, "rows": rows, "freeze_cols": 1,
             "validation": {a["name"]: {"type": "decimal", "min": 0, "max": a["max"], "error": f"0 – {a['max']}"} for a in assessments},
             "conditional": [{"column": pct_col, "type": "data_bar"},
                             {"column": pct_col, "type": "rule", "formula": f'=AND(ISNUMBER([{pct_col}]),[{pct_col}]<{pass_mark / 100})', "style": "bad"}],
             "description": "درجات كل طالب والنسبة والتقدير" if ar else "Scores, weighted percent and grade per student"}
    stats = {"name": "ملخص" if ar else "Summary", "kind": "dashboard", "title": "ملخص الفصل" if ar else "Class summary",
             "kpis": [{"label": "متوسط الفصل" if ar else "Class average", "formula": f'=IFERROR(AVERAGE({{{sheet["name"]}.{pct_col}}}),"—")', "type": "pct"},
                      {"label": "نسبة النجاح" if ar else "Pass rate", "formula": f'=IFERROR(COUNTIF({{{sheet["name"]}.{pct_col}}},">={pass_mark / 100}")/COUNT({{{sheet["name"]}.{pct_col}}}),"—")', "type": "pct"},
                      {"label": "أعلى نسبة" if ar else "Top score", "formula": f'=IF(COUNT({{{sheet["name"]}.{pct_col}}})=0,"—",MAX({{{sheet["name"]}.{pct_col}}}))', "type": "pct"},
                      {"label": "عدد الطلاب" if ar else "Students", "formula": f"=COUNTA({{{sheet['name']}.{'الطالب' if ar else 'Student'}}})", "type": "int"}],
             "charts": [{"type": "bar", "title": "نسبة كل طالب" if ar else "Percent by student", "data_sheet": sheet["name"],
                         "categories": "الطالب" if ar else "Student", "values": [pct_col]}],
             "description": "متوسطات ونسبة النجاح" if ar else "Averages, pass rate, chart"}
    return {"title": sheet["title"], "language": language, "theme": theme, "sheets": [sheet, stats], "contents": False}


def attendance(students, sessions, *, title=None, language="en", theme="school-bright"):
    ar = _ar(language)
    cols = [{"name": "الطالب" if ar else "Student", "width": 24}] + [{"name": s, "width": 7, "align": "center", "input": True} for s in sessions]
    first, last = sessions[0], sessions[-1]
    cols.append({"name": "الحضور" if ar else "Attendance", "type": "pct", "formula": f'=COUNTIF([{first}]:[{last}],"✓")/{len(sessions)}', "bold": True})
    return {"title": title or ("كشف الحضور" if ar else "Attendance"), "language": language, "theme": theme, "contents": False,
            "sheets": [{"name": "الحضور" if ar else "Attendance", "columns": cols, "rows": [[s] + [None] * len(sessions) for s in students],
                        "validation": {s: ["✓", "✗", "E"] for s in sessions}, "freeze_cols": 1,
                        "conditional": [{"column": cols[-1]["name"], "type": "rule", "operator": "lessThan", "value": 0.75, "style": "bad"}],
                        "note": "✓ حاضر · ✗ غائب · E بعذر" if ar else "✓ present · ✗ absent · E excused"}]}


def question_bank(questions, *, title=None, language="en", theme="plain-pro"):
    """questions: [{"id","unit","outcome","bloom","kind","q","options":[…],"answer","points","difficulty"}]"""
    ar = _ar(language)
    H = (["رقم", "الوحدة", "الهدف", "مستوى بلوم", "النوع", "السؤال", "أ", "ب", "ج", "د", "الإجابة", "الدرجة", "الصعوبة"] if ar else
         ["ID", "Unit", "Outcome", "Bloom", "Type", "Question", "A", "B", "C", "D", "Answer", "Points", "Difficulty"])
    rows = []
    for i, q in enumerate(questions, 1):
        o = (q.get("options") or []) + [""] * 4
        ans = q.get("answer")
        if isinstance(ans, int) and q.get("options"):
            ans = ("أبجد" if ar else "ABCD")[ans]
        rows.append([q.get("id", f"Q{i:03d}"), q.get("unit", ""), q.get("outcome", ""), q.get("bloom", ""), q.get("kind", "mcq"), q.get("q", ""),
                     o[0], o[1], o[2], o[3], ans, q.get("points", 1), q.get("difficulty", "")])
    widths = [8, 10, 10, 12, 8, 50, 18, 18, 18, 18, 10, 8, 10]
    cols = [{"name": h, "width": w, "wrap": w >= 18} for h, w in zip(H, widths)]
    cols[11]["type"] = "int"
    return {"title": title or ("بنك الأسئلة" if ar else "Question bank"), "language": language, "theme": theme, "contents": False,
            "sheets": [{"name": "الأسئلة" if ar else "Questions", "columns": cols, "rows": rows, "freeze_cols": 1,
                        "validation": {H[3]: (["تذكر", "فهم", "تطبيق", "تحليل", "تقييم", "إبداع"] if ar else
                                              ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]),
                                       H[12]: (["سهل", "متوسط", "صعب"] if ar else ["Easy", "Medium", "Hard"])}}]}


def tracker(tasks, *, title=None, language="en", theme="plain-pro"):
    """tasks: [{"task","owner","start","due","status","priority","notes"}]"""
    ar = _ar(language)
    H = ["المهمة", "المسؤول", "البداية", "الموعد", "الحالة", "الأولوية", "متأخرة؟", "ملاحظات"] if ar else \
        ["Task", "Owner", "Start", "Due", "Status", "Priority", "Late?", "Notes"]
    st = ["لم تبدأ", "جارية", "منتهية", "متوقفة"] if ar else ["Not started", "In progress", "Done", "Blocked"]
    cols = [{"name": H[0], "width": 40}, {"name": H[1], "width": 16}, {"name": H[2], "type": "date"}, {"name": H[3], "type": "date"},
            {"name": H[4], "width": 14}, {"name": H[5], "width": 10},
            {"name": H[6], "formula": f'=IF(AND([{H[3]}]<TODAY(),[{H[4]}]<>"{st[2]}"),"⚠","")', "align": "center"}, {"name": H[7], "width": 36}]
    rows = [[t.get("task"), t.get("owner"), t.get("start"), t.get("due"), t.get("status", st[0]), t.get("priority", ""), None, t.get("notes", "")] for t in tasks]
    return {"title": title or ("متابعة المهام" if ar else "Task tracker"), "language": language, "theme": theme, "contents": False,
            "sheets": [{"name": "المهام" if ar else "Tasks", "columns": cols, "rows": rows,
                        "validation": {H[4]: st, H[5]: ["P1", "P2", "P3"]},
                        "conditional": [{"column": H[4], "type": "rule", "formula": f'=[{H[4]}]="{st[2]}"', "style": "good", "whole_row": True},
                                        {"column": H[6], "type": "rule", "formula": f'=[{H[6]}]="⚠"', "style": "bad"}]}]}


def schedule(sessions, *, title=None, language="en", theme="plain-pro"):
    """sessions: [{"n","date","module","title","outcomes","activity","assessment","hours"}] — a course calendar."""
    ar = _ar(language)
    H = ["#", "التاريخ", "الوحدة", "عنوان السيشن", "الأهداف", "النشاط", "التقييم", "الساعات"] if ar else \
        ["#", "Date", "Module", "Session", "Outcomes", "Activity", "Assessment", "Hours"]
    cols = [{"name": H[0], "width": 5, "type": "int"}, {"name": H[1], "type": "date"}, {"name": H[2], "width": 18}, {"name": H[3], "width": 34},
            {"name": H[4], "width": 30, "wrap": True}, {"name": H[5], "width": 28, "wrap": True}, {"name": H[6], "width": 18}, {"name": H[7], "type": "decimal"}]
    rows = [[s.get("n", i + 1), s.get("date"), s.get("module", ""), s.get("title", ""), s.get("outcomes", ""), s.get("activity", ""),
             s.get("assessment", ""), s.get("hours", 0)] for i, s in enumerate(sessions)]
    return {"title": title or ("الجدول الزمني للكورس" if ar else "Course schedule"), "language": language, "theme": theme, "contents": False,
            "sheets": [{"name": "الجدول" if ar else "Schedule", "columns": cols, "rows": rows, "totals": {H[7]: "sum"}}]}
