---
name: course-studio
description: A full curriculum and course-production team that designs and writes complete courses — programme/course plans, syllabi, learning outcomes and alignment matrices, session-by-session lesson plans with timing, the full lesson content (not just slides), slide decks with speaker notes, student handouts, worksheets, labs, quizzes and exams with answer keys, rubrics, instructor guides, gradebooks, question banks and schedules — for schools (e.g. Don Bosco technical schools), universities, academies/bootcamps, corporate training and online courses, in Arabic or English. Always asks first what the context is (school subject content vs. a training programme, level, sessions, language, brand). Use for any request to plan, design, write or produce a course, curriculum, programme, lesson series, training, workshop, lesson plans, course materials or exam materials.
---

# Course Studio

A curriculum team on top of premium-presentations, premium-documents, premium-spreadsheets and the
design kit. You write ONE `course_spec.json` (the whole course, with real content); the builder
turns it into every file a teacher, a school and the students need.

## 0. Intake — ALWAYS ask first (short, Arabic if the user writes Arabic)
Never assume the context; the same topic is a different course for a school, a bootcamp or a
company. Ask in one round (offer options, recommend one):
1. **Context** — school subject content (which school/system, grade, age — e.g. Don Bosco
   technical, ministry curriculum?) · university course (credit hours, CLO/PLO) · academy/bootcamp/
   training-centre programme (e.g. Neo AI, LTC, Masartech, Coach Academy) · corporate training ·
   online self-paced · a single workshop.
2. **Scope** — whole programme (several courses) · one course · one unit · one session.
3. **Learners** — level, prior knowledge, group size, devices/lab.
4. **Time** — number of sessions × minutes, weeks, theory/practice ratio.
5. **Language** — of content and of slides (Arabic/English/mixed; Egyptian for school students?).
6. **Assessment** — the school's grading rules/weights, exams, projects, certificates.
7. **Deliverables** — pick from: course plan · syllabus · instructor guide · slides · lesson
   notes · handouts/worksheets · labs · quizzes + keys · exam · gradebook · question bank ·
   schedule (default: all).
8. **Look** — default unbranded (`plain-pro`, or `school-bright` / `royal-academic`); a brand only
   when the user asks (`"brand": "<slug>"` or a theme such as `donbosco-lab`, `neoai-light`).
Use the user's existing curriculum/books/syllabus if they have one — read it before designing.

## The team
| Role | Owns |
|---|---|
| Programme director | scope, context fit, sign-offs, consistency across courses |
| Instructional designer | outcomes (Bloom), backward design, sequencing, session structure, alignment |
| Subject-matter expert | accuracy, current versions/tools, real examples, misconceptions |
| Content writer | the full lesson text in the learners' language, examples, analogies |
| Slide designer | decks per session (premium-presentations), images, diagrams |
| Activity & lab designer | practice, labs with checkpoints, projects, differentiation |
| Assessment designer | quizzes, exams, rubrics, answer keys, question bank, weights |
| Instructor-guide writer | timing, what to say/do, anticipated mistakes, answers |
| Editor & QA | validate_course, language register, accessibility, page/slide checks |

## Workflow (gates)
1. **Intake** (above) → confirm a one-paragraph brief.
2. **Design** (show the user before writing everything): 3–8 measurable outcomes with Bloom
   levels → assessment plan (weights = 100%) → module/session map (titles + 1-line goal each) →
   timing pattern per session. References: `references/instructional-design.md`,
   `references/contexts.md`, `references/assessment.md`.
3. **Pilot session** — write session 1 completely (plan, content, slides, activities, quiz),
   build it with `--only S01`, show it, adjust tone/level/design with the user.
4. **Write the rest** in `course_spec.json` (`references/course-spec.md`; full example
   `examples/python_school_ar.json`). Write the FULL content: explanations, worked examples,
   analogies, code, exercises with answers — the lesson notes must teach on their own.
   Prefer authored `slides` per session (auto-slides are a fallback).
5. **Validate** — `R="bash ../premium-design-kit/scripts/run.sh"`;
   `$R scripts/validate_course.py course_spec.json` → fix every ERROR (unassessed outcomes, timing
   that doesn't add up, quiz items without answers, weights ≠ 100%) and read the WARNINGS.
6. **Build** — `$R scripts/build_course.py course_spec.json out/<Course>` (`--only S03,S04`,
   `--skip slides|docs|sheets`, `--offline`, `--no-pdf`). It validates every deck and workbook.
7. **QA** — LOOK at: the course plan contact sheet, one full session pack (slides, lesson,
   worksheet, quiz + key), the gradebook. `kit.py preview <file>` for each. Fix → rebuild.
8. **Deliver** — the folder (README.md indexes everything + the alignment matrix), the `[NEEDS]`
   list, and what to review (facts, school rules).

## Output folder
`00_Course_Plan` · `00_Syllabus` · `00_Instructor_Guide` (docx + pdf) · `Schedule.xlsx` ·
`Gradebook.xlsx` · `Question_Bank.xlsx` · per session `S01_<title>/`: `Slides.pptx` (speaker
notes) · `Lesson` · `Worksheet` · `Lab` · `Quiz` + `Quiz_Answer_Key` (docx + pdf) · `_specs/`
(editable sources of everything) · `README.md`.

## Quality bar
- Every outcome is taught AND assessed (validator enforces). Objectives start with an action verb.
- Each session: hook → objectives → explain in chunks ≤ 15 min → worked example → guided practice
  → independent practice → check for understanding → recap → homework (I do / We do / You do).
- Practice ≥ 40% of time for skills courses; school students change activity every 10–15 min.
- Examples from the learners' world (Egyptian context, their age, their trade/specialty).
- Questions: one idea each, plausible distractors, no "all of the above", answer + explanation.
- Language: content register matches the learners (Egyptian Arabic for school students is fine;
  formal Arabic for official plans when the school wants it); technical terms in English as used.
- No invented facts about the school, ministry rules or grading — ask.

## Hand-offs
premium-presentations (custom decks) · premium-documents (any extra document) ·
premium-spreadsheets (custom trackers) · reels-studio (course promo or lesson videos) ·
video-post-studio / motion-design-studio (recorded lessons, animated explainers) ·
premium-subtitle-localization (translating material).
