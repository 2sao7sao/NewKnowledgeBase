#!/usr/bin/env python3
"""Weekly usage review: summarize TBD patterns and promote patterns based on usage events."""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any, Dict

from frontmatter import parse_frontmatter


def load_usage(path: Path) -> Dict[str, Any]:
    doc = parse_frontmatter(path.read_text(encoding="utf-8"))
    fm = doc.frontmatter
    return fm


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    usage_dir = repo / "kb" / "usage"
    report_dir = repo / "outputs" / "reviews"
    report_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc)
    since = now - timedelta(days=7)

    tbd = []
    recent = []
    counts: Dict[str, int] = {}

    # Read usage events
    events = repo / "outputs" / "usage" / "events.log"
    if events.exists():
        for line in events.read_text(encoding="utf-8").splitlines():
            try:
                date_s, intent, _mode = line.split("\t")
                dt = datetime.strptime(date_s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                if dt >= since:
                    counts[intent] = counts.get(intent, 0) + 1
            except Exception:
                continue

    if usage_dir.exists():
        for p in sorted(usage_dir.glob("*.md")):
            if p.name == "index.md":
                continue
            fm = load_usage(p)
            if fm.get("pattern") == "TBD":
                tbd.append(p.stem)
            updated = fm.get("updated_at")
            if isinstance(updated, str):
                try:
                    dt = datetime.strptime(updated, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                    if dt >= since:
                        recent.append(p.stem)
                except Exception:
                    pass

            # Promote pattern if frequently used
            intent = fm.get("intent")
            if fm.get("pattern") == "TBD" and intent in counts and counts[intent] >= 3:
                text = p.read_text(encoding="utf-8")
                text = text.replace("pattern: TBD", "pattern: required")
                p.write_text(text, encoding="utf-8")

    ts = now.strftime("%Y%m%dT%H%M%SZ")
    out = report_dir / f"usage_review_{ts}.md"
    lines = ["# Weekly Usage Review", "", f"Generated: {now.date()} UTC", ""]
    lines.append("## TBD patterns")
    if tbd:
        lines += [f"- {x}" for x in tbd]
    else:
        lines.append("- none")
    lines.append("\n## Updated this week")
    if recent:
        lines += [f"- {x}" for x in recent]
    else:
        lines.append("- none")

    lines.append("\n## Usage frequency (7d)")
    if counts:
        for k, v in sorted(counts.items(), key=lambda x: -x[1]):
            lines.append(f"- {k}: {v}")
    else:
        lines.append("- none")

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[review] {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
