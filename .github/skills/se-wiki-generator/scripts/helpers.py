#!/usr/bin/env python3
"""
Helper utilities for the se-wiki-generator skill.
Generates slugs, frontmatter, backlink maps, and index tables.
"""

import os
import re
import sys
import json
import yaml
from datetime import date
from pathlib import Path
from collections import defaultdict


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


def parse_frontmatter(filepath: str) -> dict:
    """Parse YAML frontmatter from a markdown file. Returns empty dict if none."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (OSError, IOError):
        return {}

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def scan_wiki_pages(wiki_dir: str) -> list[dict]:
    """Scan all .md files under wiki_dir and return their paths + frontmatter."""
    pages = []
    wiki_path = Path(wiki_dir)
    if not wiki_path.exists():
        return pages
    for md_file in wiki_path.rglob('*.md'):
        fm = parse_frontmatter(str(md_file))
        pages.append({
            'path': str(md_file.relative_to(wiki_path.parent)),
            'absolute': str(md_file),
            'frontmatter': fm,
        })
    return pages


def extract_links(filepath: str) -> list[str]:
    """Extract all markdown links and wikilinks from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (OSError, IOError):
        return []

    # Standard markdown links: [text](path.md)
    md_links = re.findall(r'\[.*?\]\(([^)]+\.md(?:#[^)]*)?)\)', content)
    # Wikilinks: [[page-name]]
    wiki_links = re.findall(r'\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]', content)
    return md_links + wiki_links


def build_backlink_map(wiki_dir: str) -> dict[str, list[str]]:
    """Build a map of page -> list of pages that link to it."""
    backlinks = defaultdict(list)
    wiki_path = Path(wiki_dir)
    if not wiki_path.exists():
        return dict(backlinks)

    for md_file in wiki_path.rglob('*.md'):
        source = str(md_file.relative_to(wiki_path.parent))
        links = extract_links(str(md_file))
        for link in links:
            # Normalize the link target
            link_clean = link.split('#')[0]  # strip anchors
            if not link_clean.endswith('.md'):
                link_clean += '.md'
            # Resolve relative to the source file's directory
            resolved = str((md_file.parent / link_clean).resolve())
            try:
                target = str(Path(resolved).relative_to(wiki_path.parent))
            except ValueError:
                target = link_clean
            if source != target:
                backlinks[target].append(source)

    return dict(backlinks)


def find_orphans(wiki_dir: str) -> list[str]:
    """Find wiki pages with zero inbound links (excluding index.md and log.md)."""
    backlinks = build_backlink_map(wiki_dir)
    wiki_path = Path(wiki_dir)
    orphans = []

    skip = {'wiki/index.md', 'wiki/log.md', 'wiki/overview.md'}

    for md_file in wiki_path.rglob('*.md'):
        rel = str(md_file.relative_to(wiki_path.parent))
        if rel in skip:
            continue
        if rel not in backlinks or len(backlinks[rel]) == 0:
            orphans.append(rel)

    return orphans


def generate_log_entry(operation: str, title: str, details: list[str]) -> str:
    """Generate a log.md entry."""
    today = date.today().isoformat()
    lines = [f"\n## [{today}] {operation} | {title}"]
    for detail in details:
        lines.append(f"- {detail}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python helpers.py <command> [args...]")
        print("Commands:")
        print("  slugify <title>          - Generate a filename slug")
        print("  scan <wiki_dir>          - List all wiki pages with frontmatter")
        print("  backlinks <wiki_dir>     - Show backlink map")
        print("  orphans <wiki_dir>       - Find orphan pages")
        print("  log-entry <json>         - Generate a log entry")
        sys.exit(1)

    command = sys.argv[1]

    if command == "slugify" and len(sys.argv) >= 3:
        title = " ".join(sys.argv[2:])
        print(slugify(title))

    elif command == "scan" and len(sys.argv) >= 3:
        pages = scan_wiki_pages(sys.argv[2])
        print(json.dumps(pages, indent=2))

    elif command == "backlinks" and len(sys.argv) >= 3:
        bmap = build_backlink_map(sys.argv[2])
        print(json.dumps(bmap, indent=2))

    elif command == "orphans" and len(sys.argv) >= 3:
        orphans = find_orphans(sys.argv[2])
        for o in orphans:
            print(o)

    elif command == "log-entry" and len(sys.argv) >= 3:
        data = json.loads(sys.argv[2])
        print(generate_log_entry(
            operation=data["operation"],
            title=data["title"],
            details=data.get("details", []),
        ))

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)
