#!/usr/bin/env python3
"""
Helper utilities for the open-research skill.
Generates slugs, frontmatter, and source manifest entries.
"""

import re
import sys
import json
from datetime import date


def slugify(title: str, max_length: int = 60) -> str:
    """Convert a title to a URL-safe filename slug."""
    slug = title.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    if len(slug) > max_length:
        slug = slug[:max_length].rsplit('-', 1)[0]
    return slug


def generate_frontmatter(
    title: str,
    url: str,
    source_type: str = "article",
    tags: list[str] | None = None,
) -> str:
    """Generate YAML frontmatter for a source file."""
    tags = tags or []
    tag_str = ", ".join(tags)
    return (
        f"---\n"
        f'title: "{title}"\n'
        f'url: "{url}"\n'
        f'date_retrieved: "{date.today().isoformat()}"\n'
        f"source_type: {source_type}\n"
        f"tags: [{tag_str}]\n"
        f"---\n"
    )


def manifest_row(index: int, title: str, url: str, source_type: str, tags: list[str], filename: str) -> str:
    """Generate a single markdown table row for sources.md."""
    tag_str = ", ".join(tags)
    return f"| {index} | [{title}]({url}) | {source_type} | {tag_str} | [{filename}]({filename}) |"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python helpers.py <command> [args...]")
        print("Commands:")
        print("  slugify <title>            - Generate a filename slug")
        print("  frontmatter <json>         - Generate YAML frontmatter from JSON")
        sys.exit(1)

    command = sys.argv[1]

    if command == "slugify" and len(sys.argv) >= 3:
        title = " ".join(sys.argv[2:])
        print(slugify(title))

    elif command == "frontmatter" and len(sys.argv) >= 3:
        data = json.loads(sys.argv[2])
        print(generate_frontmatter(
            title=data["title"],
            url=data["url"],
            source_type=data.get("source_type", "article"),
            tags=data.get("tags", []),
        ))

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)
