#!/usr/bin/env python3
"""Ingest a markdown document and generate a procedure skill draft."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from frontmatter import parse_frontmatter

# Import helpers from run.py (deterministic placeholder implementations)
from run import extract_outline, compose_skill_draft


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", required=True, help="Path to a markdown document")
    ap.add_argument("--out", default=None, help="Output skills directory (default: repo/skills)")
    ap.add_argument("--force", action="store_true", help="Overwrite existing skill folder")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[1]
    doc_path = Path(args.doc)
    if not doc_path.is_absolute():
        doc_path = repo / doc_path

    outline = extract_outline(str(doc_path))
    skill_md = compose_skill_draft(outline)
    fm = parse_frontmatter(skill_md)
    name = fm.frontmatter.get("name")
    if not name:
        print("Failed to parse skill name from generated draft", file=sys.stderr)
        return 2

    skills_root = Path(args.out) if args.out else repo / "skills"
    if not skills_root.is_absolute():
        skills_root = repo / skills_root

    skill_dir = skills_root / name
    if skill_dir.exists() and not args.force:
        print(f"Skill already exists: {skill_dir}. Use --force to overwrite.", file=sys.stderr)
        return 1

    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    print(f"[ingest] wrote {skill_dir / 'SKILL.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
