"""builds entries.json and README.md from categories.json, entries/, and
template.md. refuses to build when the data has problems.

usage: build.py [out-dir]   (defaults to the repository root)
"""
import json
import sys
from pathlib import Path

import listing


def anchor(title):
    return "".join(c for c in title.lower().replace(" ", "-") if c.isalnum() or c == "-")


ARCHIVED = {"title": "Archived", "description": "Projects no longer maintained, kept for the record."}


def render_list(categories, entries):
    live = [e for e in entries if not e.get("archived")]
    groups = [(c, [e for e in live if e["category"] == c["id"]]) for c in categories]
    groups.append((ARCHIVED, [e for e in entries if e.get("archived")]))
    toc, sections = [], []
    for c, members in groups:
        if not members:
            continue
        toc.append(f"- [{c['title']}](#{anchor(c['title'])})")
        lines = [f"## {c['title']}", "", f"_{c['description']}_", ""]
        lines += [f"- [{e['name']}]({e['url']}) - {e['description']}" for e in members]
        sections.append("\n".join(lines))
    return "\n".join(toc), "\n\n".join(sections)


def build(root, out):
    categories, entries, problems = listing.load(root)
    if problems:
        raise SystemExit("\n".join(f"error: {p}" for p in problems))
    entries = listing.ordered(categories, entries)

    data = {"categories": categories, "entries": entries}
    (out / "entries.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    toc, body = render_list(categories, entries)
    template = (root / "template.md").read_text(encoding="utf-8")
    readme = template.replace("{{toc}}", toc).replace("{{list}}", body)
    (out / "README.md").write_text(readme, encoding="utf-8")
    return len(entries)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else listing.ROOT
    out.mkdir(parents=True, exist_ok=True)
    print(f"built {build(listing.ROOT, out)} entries into {out}")
