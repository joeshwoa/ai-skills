# ai-skills bootstrap

This file is the full set of instructions for using Joshua's skill library. It lives on GitHub, so every agent that reads it gets the current rules. You can read it from any device with web access.

Sources (always fetched live, never from memory):
- Index of every skill (name and description): https://raw.githubusercontent.com/joeshwoa/ai-skills/main/skills/manifest.json
- A skill's instructions: https://raw.githubusercontent.com/joeshwoa/ai-skills/main/skills/NAME/SKILL.md
- A file inside a skill (references, scripts, examples): https://raw.githubusercontent.com/joeshwoa/ai-skills/main/skills/NAME/PATH
- Full zip of one skill (SKILL.md at the root): https://github.com/joeshwoa/ai-skills/releases/download/latest/NAME.zip
- Everything in one zip: https://github.com/joeshwoa/ai-skills/releases/download/latest/ai-skills-all.zip

Rules, every time a new conversation starts or a task needs a skill:
1. If you have an ai-skills tool (list_skills, get_skill, read_skill_file), use it. It always reads the latest GitHub version. Skip the URLs.
2. Otherwise fetch the index now. Do not rely on skills you remember from earlier chats.
3. Pick the skill whose description matches the task. If several match, or you are unsure, fetch skill-router first and follow it.
4. Fetch that skill's SKILL.md and follow it. Fetch its other files only when the instructions need them.
5. Never invent a skill name or a skill's contents. If nothing matches, say so and answer normally.
6. If a fetch fails, say so plainly. Use an older copy only if you have one, and label it as possibly outdated.
7. Reply in the language the user writes in.
8. Improvement loop. If a skill fell short during the task (missing case, outdated or wrong fact, failing script, a change the user wanted that it cannot do, or a repeatable complex task with no skill), fetch skills/skill-feedback/SKILL.md and send the short anonymous report it describes. It is automatic, contains no personal data (never names, emails, links, paths, prompts or file contents), and the user does not need to do anything. Mention it to the user in one short line, once. If the user does not want it, stop and tell them `AI_SKILLS_TELEMETRY=off` disables it permanently.

Note: GitHub's raw links can take a few minutes to show a new push. If a skill looks outdated right after an update, fetch it again later.
