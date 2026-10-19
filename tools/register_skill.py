#!/usr/bin/env python3
"""register_skill.py — the one command to run after adding or changing a skill.

  python3 tools/register_skill.py NAME [NAME ...]    register these skills
  python3 tools/register_skill.py --all-missing      register every skills/*/SKILL.md that has no adapter yet

For each skill it (idempotently):
  1. rebuilds skills/manifest.json (what skill-router and the MCP server read),
  2. creates adapters/cursor/NAME.mdc and copies it to .cursor/rules/,
  3. adds a bullet to AGENTS.md and adapters/generic/AGENTS.md (Antigravity, Gemini, Codex...),
  4. adds a bullet to README.md.
It never rewrites an existing entry. Commit and push afterwards (the Mac auto-push does the push).
"""
import re
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def frontmatter(skill):
    text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        raise SystemExit(f"{skill}: SKILL.md has no frontmatter")
    fm = m.group(1)
    name = re.search(r"^name:\s*(.+)$", fm, re.M).group(1).strip()
    d = re.search(r"^description:\s*(>[-+]?|\|[-+]?)?\s*(.*?)(?=^\S|\Z)", fm, re.S | re.M)
    desc = " ".join(l.strip() for l in d.group(2).splitlines() if l.strip()).strip('"\'')
    return name, desc


def first_sentences(desc, limit=520):
    out = ""
    for s in re.split(r"(?<=[.!?])\s+", desc):
        if len(out) + len(s) > limit and out:
            break
        out += (" " if out else "") + s
    return out


def insert_after_last_bullet(path, pattern, bullet_lines, name):
    lines = path.read_text(encoding="utf-8").split("\n")
    if any(name in l and re.match(pattern, l) for l in lines):
        return False
    last = max((i for i, l in enumerate(lines) if re.match(pattern, l)), default=None)
    if last is None:
        lines += [""] + bullet_lines
    else:
        j = last + 1
        while j < len(lines) and lines[j].startswith("  "):
            j += 1
        lines[j:j] = bullet_lines
    path.write_text("\n".join(lines), encoding="utf-8")
    return True


def register(skill):
    name, desc = frontmatter(skill)
    changed = []
    mdc = ROOT / "adapters" / "cursor" / f"{name}.mdc"
    if not mdc.exists():
        title = name.replace("-", " ").title()
        mdc.write_text(
            f"---\ndescription: {desc}\nglobs:\nalwaysApply: false\n---\n# {title}\n\n"
            f"Read `skills/{name}/SKILL.md` in full first, then any `references/` file it points to for the task at hand.\n"
            f"Run scripts from `skills/{name}/scripts/` as the skill describes.\n",
            encoding="utf-8")
        changed.append(str(mdc.relative_to(ROOT)))
    rules = ROOT / ".cursor" / "rules"
    rules.mkdir(parents=True, exist_ok=True)
    if not (rules / f"{name}.mdc").exists():
        (rules / f"{name}.mdc").write_text(mdc.read_text(encoding="utf-8"), encoding="utf-8")
        changed.append(f".cursor/rules/{name}.mdc")
    short = first_sentences(desc)
    body = textwrap.wrap(f"— {short}", width=76)
    ag = [f"- **{name}** (`skills/{name}/SKILL.md`) " + body[0]] + ["  " + l for l in body[1:]]
    for rel in ("AGENTS.md", "adapters/generic/AGENTS.md"):
        p = ROOT / rel
        if p.exists() and insert_after_last_bullet(p, r"^- \*\*[a-z0-9-]+\*\*", ag, f"**{name}**"):
            changed.append(rel)
    rd = textwrap.wrap(f"— {short}", width=76)
    rm = [f"- **[{name}](skills/{name}/SKILL.md)** " + rd[0]] + ["  " + l for l in rd[1:]]
    p = ROOT / "README.md"
    if p.exists() and insert_after_last_bullet(p, r"^- \*\*\[[a-z0-9-]+\]", rm, f"[{name}]"):
        changed.append("README.md")
    return changed


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    if args == ["--all-missing"]:
        args = [d.name for d in sorted((ROOT / "skills").iterdir())
                if (d / "SKILL.md").is_file() and not (ROOT / "adapters" / "cursor" / f"{d.name}.mdc").exists()]
    for s in args:
        if not (ROOT / "skills" / s / "SKILL.md").is_file():
            raise SystemExit(f"no such skill: {s}")
        ch = register(s)
        print(f"{s}: " + (", ".join(ch) if ch else "already registered"))
    subprocess.run([sys.executable, str(ROOT / "skills/skill-router/scripts/build_manifest.py"), str(ROOT)], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
