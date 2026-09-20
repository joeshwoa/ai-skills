#!/usr/bin/env python3
"""
build_manifest.py — scan skills/*/SKILL.md and (re)write skills/manifest.json.

Dependency-free on purpose (no PyYAML) — this needs to run reliably on
whatever machine the agent is on (the user's Mac via Cursor, this repo's
CI, etc.) without assuming a package is installed. It parses only the
two frontmatter shapes actually used in this repo's SKILL.md files:

  ---
  name: foo
  description: A single-line description.
  ---

  ---
  name: foo
  description: >
    A folded block-scalar description that
    wraps across several indented lines.
  ---

Usage:
  python3 skills/skill-router/scripts/build_manifest.py
  (run from the repo root, or pass the repo root as argv[1])
"""
import json
import re
import sys
from pathlib import Path


def parse_frontmatter(text: str) -> dict:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("no frontmatter block (must start with '---')")
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise ValueError("frontmatter block never closes with '---'")

    body = lines[1:end]
    result = {}
    i = 0
    key_re = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")
    while i < len(body):
        line = body[i]
        if not line.strip():
            i += 1
            continue
        m = key_re.match(line)
        if not m:
            i += 1
            continue
        key, rest = m.group(1), m.group(2).strip()
        if rest in (">", "|", ">-", "|-"):
            # Folded/literal block scalar: collect indented continuation lines.
            fold = rest.startswith(">")
            parts = []
            i += 1
            while i < len(body) and (body[i].startswith("  ") or not body[i].strip()):
                parts.append(body[i].strip())
                i += 1
            result[key] = " ".join(p for p in parts if p) if fold else "\n".join(parts)
            continue
        else:
            # Plain scalar — strip a single layer of matching quotes.
            if len(rest) >= 2 and rest[0] == rest[-1] and rest[0] in ("'", '"'):
                rest = rest[1:-1]
            result[key] = rest
            i += 1
    return result


def main():
    repo_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
    skills_dir = repo_root / "skills"
    if not skills_dir.is_dir():
        print(f"error: {skills_dir} not found", file=sys.stderr)
        sys.exit(1)

    entries = []
    errors = []
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        skill_dir = skill_md.parent
        try:
            fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        except ValueError as e:
            errors.append(f"{skill_md.relative_to(repo_root)}: {e}")
            continue
        name = fm.get("name", skill_dir.name)
        description = fm.get("description", "")
        if not description:
            errors.append(f"{skill_md.relative_to(repo_root)}: missing/empty description")
        has_scripts = (skill_dir / "scripts").is_dir()
        has_references = (skill_dir / "references").is_dir()
        entries.append(
            {
                "name": name,
                "path": f"skills/{skill_dir.name}",
                "description": description,
                "has_scripts": has_scripts,
                "has_references": has_references,
            }
        )

    manifest = {
        "generated_by": "skills/skill-router/scripts/build_manifest.py",
        "skill_count": len(entries),
        "skills": entries,
    }
    out_path = skills_dir / "manifest.json"
    out_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out_path} ({len(entries)} skill(s)).")
    if errors:
        print("Warnings:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
