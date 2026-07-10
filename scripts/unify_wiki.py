#!/usr/bin/env python3
"""
unify_wiki.py - Non-destructive, base-preserving unification of two LLM wikis.

Merges an AUGMENT wiki (e.g. wiki_v1) on top of a BASE wiki (e.g. wiki) and
GUARANTEES that BASE content is never deleted or overwritten. Every change to a
base file is append-only, so the original base text is always a prefix of the
result; protected base pages stay byte-identical.

Real wikis are usually NOT disjoint - the augment is incremental content on
similar topics (new accounts, updated info). So instead of blindly creating a
new node + link for every augment page (which bloats the graph), each augment
page is classified by content similarity to the most similar BASE page in the
SAME category (the schema - sources/concepts/entities/comparisons/analyses - is
fixed) and handled by a 4-tier rule:

    Tier 1  EXACT    (sim >= exact-threshold or identical body)
            -> keep the base file; DROP the augment duplicate (no new node).
    Tier 2  CLOSE    (sim >= merge-threshold)
            -> MERGE into a single file: the augment's distinct content is
               appended (append-only) into the base page under a delimited
               "Merged from ..." block. No new slug; the graph stays compact.
               (The se-unify-wiki skill's advanced mode then rewrites this block
               into true synthesized prose.)
    Tier 3  RELATED  (sim >= relate-threshold)
            -> keep BOTH pages and add a bidirectional "Related" link. The skill
               can let the LLM decide whether to upgrade this to a Tier-2 merge.
    Tier 4  DIFFERENT (sim < relate-threshold)
            -> add the augment page as a new standalone node, no link.

This is the deterministic backbone of the hybrid approach (pure standard
library, fully local). The se-unify-wiki Copilot skill wraps it and adds an LLM
synthesis pass on the tier-2/tier-3 pairs.

Exit codes: 0 = success / clean dry-run, 2 = aborted (already unified / bad
paths), 3 = validation failed (base retention < 100% or links broken).
"""

import argparse
import json
import math
import os
import re
import shutil
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

STRUCTURAL = {"index.md", "log.md", "overview.md"}
CATEGORIES = ["sources", "concepts", "entities", "comparisons", "analyses"]

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
LINK_RE = re.compile(r"\]\(([^)]+?\.md)((?:#[^)]*)?)\)")
HEADING_RE = re.compile(r"^(#{1,6})(\s)", re.MULTILINE)
STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "are", "was", "has",
    "have", "not", "but", "all", "any", "its", "via", "per", "into", "than",
    "then", "they", "their", "them", "what", "when", "where", "which", "while",
    "page", "see", "source", "sources", "summary", "type", "tags", "title",
    "related", "concepts", "entities", "points", "key", "contradictions",
    "open", "questions", "appearances", "across", "role", "definition",
}


# --------------------------------------------------------------------------- #
# Frontmatter + page model
# --------------------------------------------------------------------------- #
def split_frontmatter(text):
    m = FM_RE.match(text)
    if not m:
        return {}, "", text
    return parse_fm(m.group(1)), m.group(1), text[m.end():]


def parse_fm(block):
    fm = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        mm = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not mm:
            continue
        key, val = mm.group(1), mm.group(2).strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            items = [s.strip().strip("\"'") for s in inner.split(",")] if inner else []
            fm[key] = [i for i in items if i]
        else:
            fm[key] = val.strip().strip("\"'")
    return fm


class Page:
    def __init__(self, wiki_root, abs_path):
        self.abs_path = Path(abs_path)
        self.relpath = self.abs_path.relative_to(wiki_root).as_posix()
        self.category = self.relpath.split("/")[0] if "/" in self.relpath else "root"
        self.slug = self.abs_path.stem
        self.text = self.abs_path.read_text(encoding="utf-8")
        self.fm, self.fm_block, self.body = split_frontmatter(self.text)
        self.title = self.fm.get("title", self.slug)
        self.type = self.fm.get("type", "")
        self.is_structural = self.relpath in STRUCTURAL

    def norm_body(self):
        return re.sub(r"\s+", " ", self.body).strip().lower()

    def tokens(self):
        text = self.title + "\n" + self.body
        text = re.sub(r"`{1,3}.*?`{1,3}", " ", text, flags=re.DOTALL)
        text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r" \1 ", text)
        text = re.sub(r"[^A-Za-z0-9\s-]", " ", text.lower())
        out = []
        for t in re.split(r"[\s-]+", text):
            if len(t) > 2 and t not in STOPWORDS and not t.isdigit():
                out.append(t)
        return out


def load_wiki(root):
    root = Path(root)
    pages = []
    for md in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in md.relative_to(root).parts):
            continue
        pages.append(Page(root, md))
    return pages


# --------------------------------------------------------------------------- #
# TF-IDF similarity
# --------------------------------------------------------------------------- #
def build_tfidf(docs_tokens):
    n = len(docs_tokens)
    df = defaultdict(int)
    tfs = []
    for toks in docs_tokens:
        tf = defaultdict(int)
        for t in toks:
            tf[t] += 1
        tfs.append(tf)
        for t in tf:
            df[t] += 1
    vecs = []
    for tf in tfs:
        vec = {}
        for t, c in tf.items():
            idf = math.log((1 + n) / (1 + df[t])) + 1.0
            vec[t] = (1 + math.log(c)) * idf
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        vecs.append({t: v / norm for t, v in vec.items()})
    return vecs


def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(t, 0.0) for t, v in a.items())


# --------------------------------------------------------------------------- #
# Path / link helpers
# --------------------------------------------------------------------------- #
def resolve_rel(page_dir, target):
    base = Path(page_dir) if page_dir not in ("", ".") else Path(".")
    parts = []
    for part in (base / target).parts:
        if part == "..":
            if parts:
                parts.pop()
        elif part == ".":
            continue
        else:
            parts.append(part)
    return "/".join(parts)


def make_relative(from_relpath, to_relpath):
    from_dir = os.path.dirname(from_relpath)
    rel = os.path.relpath(to_relpath, from_dir if from_dir else ".")
    return rel.replace("\\", "/")


def normalize_title(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def demote_headings(body):
    return HEADING_RE.sub(lambda m: "#" + m.group(1) + m.group(2), body)


def extract_section(text, heading_substr):
    out, capture = [], False
    for line in text.splitlines():
        if line.startswith("## ") and heading_substr.lower() in line.lower():
            capture = True
            out.append(line)
            continue
        if capture and line.startswith("## "):
            break
        if capture:
            out.append(line)
    return "\n".join(out).strip()


# --------------------------------------------------------------------------- #
# Classification (the 4-tier rule)
# --------------------------------------------------------------------------- #
def classify(aug_pages, base_pages, thresholds, strategy):
    """Return action dicts for each aug content page."""
    base_content = [p for p in base_pages if not p.is_structural]
    base_by_cat = defaultdict(list)
    for p in base_content:
        base_by_cat[p.category].append(p)

    corpus = base_content + [p for p in aug_pages if not p.is_structural]
    vecs = build_tfidf([p.tokens() for p in corpus])
    vec = {id(p): v for p, v in zip(corpus, vecs)}

    actions = []
    for ap in aug_pages:
        if ap.is_structural:
            continue

        # identity signal: same relpath or same normalized title in same category
        same_node = None
        for bp in base_by_cat.get(ap.category, []):
            if bp.relpath == ap.relpath or \
                    normalize_title(bp.title) == normalize_title(ap.title):
                same_node = bp
                break

        # best content match in same category
        best, best_s = None, 0.0
        for bp in base_by_cat.get(ap.category, []):
            s = cosine(vec[id(ap)], vec[id(bp)])
            if s > best_s:
                best, best_s = bp, s

        target = same_node or best
        score = 0.0
        if same_node is not None:
            score = cosine(vec[id(ap)], vec[id(same_node)])
        elif best is not None:
            score = best_s
        score = round(score, 3)

        if strategy == "keep_both":
            tier = "keep_both" if (target is not None and
                                   (same_node is not None or best_s >= thresholds["relate"])) else "new"
        else:  # tiered
            if target is None:
                tier = "new"
            elif same_node is not None:
                # same node (same slug/title): identical body -> exact (keep base);
                # any change -> merge so the updated info is captured, never dropped.
                tier = "exact" if ap.norm_body() == target.norm_body() else "merge"
            elif ap.norm_body() == target.norm_body() or best_s >= thresholds["exact"]:
                tier = "exact"
            elif best_s >= thresholds["merge"]:
                tier = "merge"
            elif best_s >= thresholds["relate"]:
                tier = "relate"
            else:
                tier = "new"

        actions.append({
            "aug": ap, "match": target if tier != "new" else best,
            "tier": tier, "score": score,
            "same_node": same_node is not None,
        })
    return actions


# --------------------------------------------------------------------------- #
# Text rewriting
# --------------------------------------------------------------------------- #
def rewrite_links(text, from_relpath, rename_map):
    """Repoint relative .md links through the rename map (full relative rebuild)."""
    page_dir = Path(from_relpath).parent.as_posix()
    if page_dir == ".":
        page_dir = ""

    def repl(m):
        target, anchor = m.group(1), m.group(2)
        if target.startswith("http"):
            return m.group(0)
        resolved = resolve_rel(page_dir, target)
        final = rename_map.get(resolved, resolved)
        if final != resolved:
            return f"]({make_relative(from_relpath, final)}{anchor})"
        return m.group(0)

    return LINK_RE.sub(repl, text)


def swap_ns(text, rename_map, base_ns, aug_ns):
    def repl(m):
        rel = m.group(1)
        return f"{base_ns}/{rename_map.get(rel, rel)}"
    return re.sub(rf"{re.escape(aug_ns)}/([A-Za-z0-9_./-]+\.md)", repl, text)


def inject_frontmatter_field(text, key, value):
    m = FM_RE.match(text)
    if not m:
        return text
    block = m.group(1)
    if re.search(rf"^{re.escape(key)}:", block, re.MULTILINE):
        return text
    return f"---\n{block}\n{key}: \"{value}\"\n---\n" + text[m.end():]


def prepare_aug_text(aug_page, final_relpath, rename_map, base_ns, aug_ns, extra_note=None):
    text = aug_page.text
    text = rewrite_links(text, final_relpath, rename_map)
    text = swap_ns(text, rename_map, base_ns, aug_ns)
    text = inject_frontmatter_field(text, "source_wiki", aug_ns)
    if extra_note:
        m = FM_RE.match(text)
        if m:
            text = text[:m.end()] + extra_note + text[m.end():]
        else:
            text = extra_note + text
    return text


def append_related_link(base_text, label, link, anchor_title):
    """Append (or extend) a '## Related (unification)' section. Append-only."""
    bullet = f"- Related page from {label}: [{anchor_title}]({link})\n"
    if "## Related (unification)" in base_text:
        return base_text.rstrip() + "\n" + bullet
    return base_text.rstrip() + f"\n\n## Related (unification)\n{bullet}"


def build_merge_block(aug_ns, label, aug_page, base_target, score,
                      rename_map, base_ns):
    body = aug_page.body
    body = re.sub(r"^#\s+.*$", "", body, count=1, flags=re.MULTILINE).strip()
    body = rewrite_links(body, base_target.relpath, rename_map)
    body = swap_ns(body, rename_map, base_ns, aug_ns)
    body = demote_headings(body)
    src = ", ".join(aug_page.fm.get("sources", [])) if aug_page.fm.get("sources") else "-"
    return (
        f"\n\n<!-- BEGIN merged:{aug_ns}:{aug_page.slug} -->\n"
        f"## Merged from {label}: {aug_page.title} (similarity {score})\n"
        f"> Auto-merged augment counterpart (`{aug_ns}/{aug_page.relpath}`, "
        f"sources: {src}). Base content above is authoritative; "
        f"flag any contradictions rather than resolving them.\n\n"
        f"{body}\n"
        f"<!-- END merged:{aug_ns}:{aug_page.slug} -->\n"
    )


# --------------------------------------------------------------------------- #
# Structural merge builders
# --------------------------------------------------------------------------- #
def build_index_block(ns, label, actions, aug_index_text, today, strategy):
    added = [a for a in actions if a["tier"] in ("relate", "new", "keep_both")]
    merged = [a for a in actions if a["tier"] == "merge"]
    exact = [a for a in actions if a["tier"] == "exact"]
    lines = [
        f"<!-- BEGIN unified:{ns} -->",
        f"## Augmented Collection: {label}",
        f"> Merged by unify_wiki.py (strategy={strategy}) on {today}. "
        f"Base entries above are unchanged.",
        "",
    ]
    if added:
        lines += [f"### Added pages ({len(added)})",
                  "| Page | Type | Relation |", "|------|------|----------|"]
        for a in sorted(added, key=lambda x: x["final_rel"]):
            if a["tier"] == "relate":
                rel = f"related to {a['match'].slug}"
            elif a["tier"] == "keep_both":
                rel = f"keep-both (vs {a['match'].slug})"
            else:
                rel = "standalone (new)"
            lines.append(f"| [{a['aug'].title}]({a['final_rel']}) | "
                         f"{a['aug'].type or '-'} | {rel} |")
        lines.append("")
    if merged:
        lines += [f"### Merged into base ({len(merged)})",
                  "| Augment page | Folded into base | Similarity |",
                  "|--------------|------------------|-----------|"]
        for a in merged:
            lines.append(f"| {a['aug'].title} | [{a['match'].title}]"
                         f"({a['match'].relpath}) | {a['score']} |")
        lines.append("")
    if exact:
        lines += [f"### Exact duplicates (base kept, augment dropped) ({len(exact)})", ""]
        for a in exact:
            lines.append(f"- {a['aug'].title} == [{a['match'].title}]({a['match'].relpath})")
        lines.append("")
    carried = extract_section(aug_index_text, "Known Data Inconsistencies")
    if carried:
        carried = carried.split("\n", 1)[1] if "\n" in carried else ""
        lines += [f"### Known Data Inconsistencies ({label})", carried.strip(), ""]
    lines.append(f"<!-- END unified:{ns} -->")
    return "\n".join(lines).strip() + "\n"


def build_overview_block(ns, label, aug_overview_body, rename_map, base_ns, aug_ns):
    body = aug_overview_body
    body = re.sub(r"^#\s+.*$", "", body, count=1, flags=re.MULTILINE).strip()
    body = rewrite_links(body, "overview.md", rename_map)
    body = swap_ns(body, rename_map, base_ns, aug_ns)
    body = demote_headings(body)
    return (f"<!-- BEGIN unified:{ns} -->\n## Augmented Domain: {label}\n\n"
            f"{body}\n<!-- END unified:{ns} -->\n")


def build_log_entry(today, s):
    lines = [
        f"## [{today}] unify | Augmented base wiki with {s['label']}",
        f"- Source: augment `{s['aug_dir']}` -> base `{s['base_dir']}` "
        f"(strategy={s['strategy']}, thresholds exact/merge/relate="
        f"{s['exact']}/{s['merge']}/{s['relate']})",
        f"- Tier 1 exact (base kept, dup dropped): {s['exact_n']}",
        f"- Tier 2 close (merged into base, single file): {s['merge_n']}",
        f"- Tier 3 related (added + Related link): {s['relate_n']}",
        f"- Tier 4 different (added standalone): {s['new_n']}",
        f"- Structural files merged (append-only): index.md, log.md, overview.md",
        f"- Base retention: {s['retention_pct']}% "
        f"({s['base_modified']} appended, {s['base_protected']} protected byte-identical)",
        f"- Broken links after merge: {s['broken_links']}",
        f"- Contradictions carried (flagged, not resolved): {s['contradictions']}",
    ]
    if s["preserve"]:
        lines.append(f"- Preserve rules honored: {', '.join(s['preserve'])}")
    if s["protect"]:
        lines.append(f"- Protected (byte-identical) pages: {', '.join(s['protect'])}")
    if s["downgrades"]:
        lines.append(f"- Downgrades from preserve/protect: {s['downgrades']}")
    if s["backup_path"]:
        lines.append(f"- Base backup: {s['backup_path']}")
    return "\n" + "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #
def find_broken_links(root):
    root = Path(root)
    broken = []
    for md in root.rglob("*.md"):
        if any(part.startswith(".") for part in md.relative_to(root).parts):
            continue
        text = md.read_text(encoding="utf-8")
        for m in LINK_RE.finditer(text):
            target = m.group(1)
            if target.startswith("http"):
                continue
            if not (md.parent / target).resolve().exists():
                broken.append(f"{md.relative_to(root).as_posix()} -> {target}")
    return broken


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Base-preserving wiki unification (tiered).")
    ap.add_argument("--base", default="wiki")
    ap.add_argument("--augment", default="wiki_v1")
    ap.add_argument("--in-place", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--strategy", default="tiered", choices=["tiered", "keep_both"],
                    help="tiered = 4-tier similarity rule (default); keep_both = legacy twins.")
    ap.add_argument("--exact-threshold", type=float, default=0.985,
                    help="Tier 1: keep base, drop augment duplicate (default 0.985; identical body also qualifies).")
    ap.add_argument("--merge-threshold", type=float, default=0.60,
                    help="Tier 2: merge into a single file (default 0.60).")
    ap.add_argument("--relate-threshold", type=float, default=0.25,
                    help="Tier 3: keep both + Related link; the LLM decides in skill mode (default 0.25).")
    ap.add_argument("--threshold", type=float, default=None,
                    help="Legacy alias for --relate-threshold (keep_both match floor).")
    ap.add_argument("--augment-suffix", default="v1",
                    help="Twin suffix for legacy keep_both strategy.")
    ap.add_argument("--augment-label", default=None)
    ap.add_argument("--preserve", action="append", default=[],
                    help="Base relpath/substring to keep SEPARATE (never merged; matches become Related). Repeatable.")
    ap.add_argument("--protect", action="append", default=[],
                    help="Base relpath/substring to keep BYTE-IDENTICAL (no append at all). Repeatable.")
    ap.add_argument("--no-see-also", action="store_true",
                    help="Do not append Related links to base pages.")
    ap.add_argument("--backup-dir", default=None)
    ap.add_argument("--no-backup", action="store_true")
    ap.add_argument("--report", default=None)
    ap.add_argument("--explain", action="store_true",
                    help="Include a per-page similarity/tier table in the report.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    thresholds = {
        "exact": args.exact_threshold,
        "merge": args.merge_threshold,
        "relate": args.threshold if args.threshold is not None else args.relate_threshold,
    }

    base_dir = Path(args.base).resolve()
    aug_dir = Path(args.augment).resolve()
    if not base_dir.is_dir():
        print(f"ERROR: base wiki not found: {base_dir}", file=sys.stderr)
        return 2
    if not aug_dir.is_dir():
        print(f"ERROR: augment wiki not found: {aug_dir}", file=sys.stderr)
        return 2

    aug_ns = aug_dir.name
    label = args.augment_label or aug_ns

    if args.out and not args.in_place:
        out_dir = Path(args.out).resolve()
        if out_dir.exists():
            print(f"ERROR: --out dir already exists: {out_dir}", file=sys.stderr)
            return 2
        shutil.copytree(base_dir, out_dir, ignore=shutil.ignore_patterns(".unify-*"))
        target_dir = out_dir
    else:
        target_dir = base_dir
    base_ns = target_dir.name

    idx_path = target_dir / "index.md"
    if idx_path.exists() and f"<!-- BEGIN unified:{aug_ns} -->" in \
            idx_path.read_text(encoding="utf-8") and not args.force:
        print(f"ABORT: base already unified with '{aug_ns}' (marker in index.md). "
              f"Use --force to re-run.", file=sys.stderr)
        return 2

    orig_base_pages = load_wiki(base_dir)
    base_snapshot = {p.relpath: p.text for p in orig_base_pages}
    target_pages = load_wiki(target_dir)
    aug_pages = load_wiki(aug_dir)

    actions = classify(aug_pages, target_pages, thresholds, args.strategy)

    def hits(patterns, relpath):
        return any(pat and pat in relpath for pat in patterns)

    # Apply preserve/protect downgrades.
    downgrades = []
    for a in actions:
        if a["match"] is None:
            continue
        brel = a["match"].relpath
        if a["tier"] in ("exact", "merge"):
            if hits(args.protect, brel):
                a["tier"] = "new"           # cannot touch a protected base page
                downgrades.append(f"{a['aug'].relpath}: ->new (protect {brel})")
            elif hits(args.preserve, brel):
                a["tier"] = "relate"        # keep separate, just link
                downgrades.append(f"{a['aug'].relpath}: ->relate (preserve {brel})")

    # Build rename map (aug relpath -> final relpath in merged tree).
    rename_map = {}
    for a in actions:
        ap_ = a["aug"]
        if a["tier"] in ("exact", "merge"):
            final = a["match"].relpath           # folds into base; links repoint to base
        elif a["tier"] == "keep_both":
            final = f"{ap_.category}/{ap_.slug}--{args.augment_suffix}.md"
        else:                                    # relate / new
            final = ap_.relpath
        a["final_rel"] = final
        rename_map[ap_.relpath] = final

    today = date.today().isoformat()
    aug_index_text = (aug_dir / "index.md").read_text(encoding="utf-8") \
        if (aug_dir / "index.md").exists() else ""
    contradictions = len(re.findall(
        r"^\d+\.", extract_section(aug_index_text, "Known Data Inconsistencies"),
        flags=re.MULTILINE))

    tier_counts = {t: len([a for a in actions if a["tier"] == t])
                   for t in ("exact", "merge", "relate", "new", "keep_both")}
    base_modified = len({a["match"].relpath for a in actions
                         if a["tier"] in ("merge", "relate") and a["match"]
                         and not hits(args.protect, a["match"].relpath)})
    base_protected = len([p for p in args.protect])

    if args.dry_run:
        _write_report(args, target_dir, label, actions, thresholds, today,
                      base_dir, aug_dir, retention_pct=100.0,
                      base_modified=base_modified, broken_after=None,
                      contradictions=contradictions, backup_path=None,
                      tier_counts=tier_counts, retention_failures=[],
                      downgrades=downgrades, dry_run=True)
        print(_summary(label, tier_counts, 100.0, "(dry-run)", contradictions))
        return 0

    backup_path = None
    if not args.no_backup:
        bdir = Path(args.backup_dir) if args.backup_dir else (base_dir.parent / ".unify-backup")
        bdir.mkdir(parents=True, exist_ok=True)
        backup_path = bdir / f"{base_dir.name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        shutil.copytree(base_dir, backup_path, ignore=shutil.ignore_patterns(".unify-*"))

    links_rewritten = 0
    # Order: do merges/relate (touch base) and adds. Exact = no-op.
    for a in actions:
        ap_ = a["aug"]
        tier = a["tier"]
        final_rel = a["final_rel"]

        if tier == "exact":
            continue  # keep base, drop augment duplicate

        if tier == "merge":
            base_file = target_dir / a["match"].relpath
            btext = base_file.read_text(encoding="utf-8")
            marker = f"<!-- BEGIN merged:{aug_ns}:{ap_.slug} -->"
            if marker not in btext:
                block = build_merge_block(aug_ns, label, ap_, a["match"],
                                          a["score"], rename_map, base_ns)
                base_file.write_text(btext + block, encoding="utf-8")
                links_rewritten += len(LINK_RE.findall(ap_.body))
            continue

        # relate / new / keep_both -> write the augment page as a file
        note = None
        if tier == "relate" and a["match"]:
            back = make_relative(final_rel, a["match"].relpath)
            note = (f"> **Related (unification):** see base page "
                    f"[{a['match'].title}]({back}) (similarity {a['score']}).\n\n")
        elif tier == "keep_both" and a["match"]:
            back = make_relative(final_rel, a["match"].relpath)
            note = (f"> **Unified note:** augmented counterpart from `{aug_ns}` "
                    f"(matched base [{a['match'].title}]({back}), score {a['score']}). "
                    f"Base page is authoritative.\n\n")
        text = prepare_aug_text(ap_, final_rel, rename_map, base_ns, aug_ns, note)
        if a["match"] and tier in ("keep_both",):
            text = inject_frontmatter_field(text, "augments", f"{base_ns}/{a['match'].relpath}")
        dest = target_dir / final_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        links_rewritten += len(LINK_RE.findall(ap_.text))

        # add the back-link on the base page (append-only) for relate/keep_both
        if tier in ("relate", "keep_both") and a["match"] and not args.no_see_also \
                and not hits(args.protect, a["match"].relpath):
            base_file = target_dir / a["match"].relpath
            btext = base_file.read_text(encoding="utf-8")
            fwd = make_relative(a["match"].relpath, final_rel)
            if f"]({fwd})" not in btext:
                base_file.write_text(
                    append_related_link(btext, label, fwd, ap_.title), encoding="utf-8")

    # Structural merges (append-only).
    if idx_path.exists():
        idx_path.write_text(
            idx_path.read_text(encoding="utf-8").rstrip() + "\n\n"
            + build_index_block(aug_ns, label, actions, aug_index_text, today, args.strategy),
            encoding="utf-8")
    ov_path = target_dir / "overview.md"
    aug_ov = aug_dir / "overview.md"
    if ov_path.exists() and aug_ov.exists():
        _, _, aug_ov_body = split_frontmatter(aug_ov.read_text(encoding="utf-8"))
        ov_path.write_text(
            ov_path.read_text(encoding="utf-8").rstrip() + "\n\n"
            + build_overview_block(aug_ns, label, aug_ov_body, rename_map, base_ns, aug_ns),
            encoding="utf-8")

    # Validation.
    retention_failures = []
    for relpath, orig_text in base_snapshot.items():
        merged_file = target_dir / relpath
        if not merged_file.exists():
            retention_failures.append(f"{relpath} (missing!)")
            continue
        merged_text = merged_file.read_text(encoding="utf-8")
        if hits(args.protect, relpath):
            if merged_text != orig_text:
                retention_failures.append(f"{relpath} (protected page changed!)")
        elif not merged_text.startswith(orig_text):
            retention_failures.append(f"{relpath} (base content not preserved as prefix!)")
    retention_pct = round(
        100.0 * (len(base_snapshot) - len(retention_failures)) / max(1, len(base_snapshot)), 2)
    broken_after = find_broken_links(target_dir)

    stats = {
        "label": label, "aug_dir": aug_dir.name, "base_dir": base_dir.name,
        "strategy": args.strategy, "exact": thresholds["exact"],
        "merge": thresholds["merge"], "relate": thresholds["relate"],
        "exact_n": tier_counts["exact"], "merge_n": tier_counts["merge"],
        "relate_n": tier_counts["relate"], "new_n": tier_counts["new"],
        "retention_pct": retention_pct, "base_modified": base_modified,
        "base_protected": base_protected, "broken_links": len(broken_after),
        "contradictions": contradictions, "preserve": args.preserve,
        "protect": args.protect, "downgrades": len(downgrades),
        "backup_path": str(backup_path) if backup_path else None,
    }
    log_path = target_dir / "log.md"
    if log_path.exists():
        log_path.write_text(log_path.read_text(encoding="utf-8").rstrip() + "\n"
                            + build_log_entry(today, stats), encoding="utf-8")

    state = {
        "unified_at": datetime.now().isoformat(timespec="seconds"),
        "augment": aug_ns, "label": label, "strategy": args.strategy,
        "thresholds": thresholds, "tier_counts": tier_counts,
        "actions": [{"aug": a["aug"].relpath, "tier": a["tier"],
                     "match": a["match"].relpath if a["match"] else None,
                     "score": a["score"], "final": a["final_rel"]} for a in actions],
        "retention_pct": retention_pct, "broken_links": len(broken_after),
        "backup": str(backup_path) if backup_path else None,
    }
    (target_dir / ".unify-state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")

    _write_report(args, target_dir, label, actions, thresholds, today,
                  base_dir, aug_dir, retention_pct=retention_pct,
                  base_modified=base_modified, broken_after=broken_after,
                  contradictions=contradictions,
                  backup_path=str(backup_path) if backup_path else None,
                  tier_counts=tier_counts, retention_failures=retention_failures,
                  downgrades=downgrades, dry_run=False)
    print(_summary(label, tier_counts, retention_pct, len(broken_after), contradictions))

    if retention_failures:
        print(f"VALIDATION FAILED: {len(retention_failures)} base-retention violation(s).",
              file=sys.stderr)
        return 3
    if broken_after:
        print(f"VALIDATION WARNING: {len(broken_after)} broken link(s) introduced.",
              file=sys.stderr)
        return 3
    return 0


def _summary(label, tc, retention_pct, broken, contradictions):
    return (
        f"\n=== Wiki Unification Summary (tiered) ===\n"
        f"  Augment label            : {label}\n"
        f"  Tier 1 exact (base kept) : {tc['exact']}\n"
        f"  Tier 2 close (merged)    : {tc['merge']}\n"
        f"  Tier 3 related (linked)  : {tc['relate']}\n"
        f"  Tier 4 different (new)   : {tc['new']}\n"
        + (f"  keep_both twins          : {tc['keep_both']}\n" if tc['keep_both'] else "")
        + f"  Base retention           : {retention_pct}%\n"
        f"  Broken links (after)     : {broken}\n"
        f"  Contradictions carried   : {contradictions}\n"
    )


def _write_report(args, target_dir, label, actions, thresholds, today, base_dir,
                  aug_dir, *, retention_pct, base_modified, broken_after,
                  contradictions, backup_path, tier_counts, retention_failures,
                  downgrades, dry_run):
    report_md = Path(args.report) if args.report else (target_dir.parent / "unify-report.md")
    report_json = report_md.with_suffix(".json")
    by_tier = lambda t: [a for a in actions if a["tier"] == t]

    L = [
        f"# Wiki Unification Report - {today}",
        "",
        ("> **DRY RUN** - no files were written; this is the planned outcome.\n" if dry_run else ""),
        "## Parameters",
        "",
        f"- Base (authoritative): `{base_dir}`",
        f"- Augment: `{aug_dir}` (label: **{label}**)",
        f"- Output: {'in-place on base' if (args.in_place or not args.out) else args.out}",
        f"- Strategy: **{args.strategy}**",
        f"- Thresholds: exact `{thresholds['exact']}` / merge `{thresholds['merge']}` "
        f"/ relate `{thresholds['relate']}`",
        f"- Preserve (kept separate): {args.preserve or '(none)'}",
        f"- Protect (byte-identical): {args.protect or '(none)'}",
        f"- Backup: {backup_path or '(none / dry-run)'}",
        "",
        "## Tier summary",
        "",
        "| Tier | Rule | Count |",
        "|------|------|-------|",
        f"| 1. Exact | keep base, drop augment duplicate | {tier_counts['exact']} |",
        f"| 2. Close | merge into a single file (no new node) | {tier_counts['merge']} |",
        f"| 3. Related | keep both + Related link | {tier_counts['relate']} |",
        f"| 4. Different | add as new standalone node | {tier_counts['new']} |",
        (f"| (legacy) keep_both | twin page | {tier_counts['keep_both']} |"
         if tier_counts['keep_both'] else ""),
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| **Base retention** | **{retention_pct}%** |",
        f"| Base pages appended-to | {base_modified} |",
        f"| Broken links after merge | {0 if dry_run else len(broken_after)} |",
        f"| Contradictions carried (flagged) | {contradictions} |",
        f"| Preserve/Protect downgrades | {len(downgrades)} |",
        "",
    ]

    if by_tier("merge"):
        L += ["## Tier 2 - Merged into base (single file)", "",
              "| Augment page | Folded into base | Similarity |",
              "|--------------|------------------|-----------|"]
        for a in by_tier("merge"):
            L.append(f"| {a['aug'].relpath} | {a['match'].relpath} | {a['score']} |")
        L.append("")
    if by_tier("relate"):
        L += ["## Tier 3 - Related (kept both + link)", "",
              "| Augment page | Related base page | Similarity |",
              "|--------------|-------------------|-----------|"]
        for a in by_tier("relate"):
            L.append(f"| {a['final_rel']} | {a['match'].relpath} | {a['score']} |")
        L.append("")
    if by_tier("exact"):
        L += ["## Tier 1 - Exact duplicates (base kept, augment dropped)", ""]
        for a in by_tier("exact"):
            L.append(f"- {a['aug'].relpath} == {a['match'].relpath} (sim {a['score']})")
        L.append("")
    if by_tier("new"):
        L += ["## Tier 4 - Added standalone (new)", ""]
        for a in sorted(by_tier("new"), key=lambda x: x["final_rel"]):
            near = f" (nearest base {a['match'].slug} @ {a['score']})" if a["match"] else ""
            L.append(f"- `{a['final_rel']}`{near}")
        L.append("")

    if downgrades:
        L += ["## Preserve / Protect downgrades", ""]
        L += [f"- {d}" for d in downgrades] + [""]

    if args.explain:
        L += ["## Similarity explain (all augment pages)", "",
              "| Augment page | Tier | Nearest base | Score | Same-node |",
              "|--------------|------|--------------|-------|-----------|"]
        for a in sorted(actions, key=lambda x: (-x["score"])):
            nb = a["match"].relpath if a["match"] else "-"
            L.append(f"| {a['aug'].relpath} | {a['tier']} | {nb} | "
                     f"{a['score']} | {'yes' if a['same_node'] else ''} |")
        L.append("")

    L += ["## Base-protection check", ""]
    if retention_failures:
        L.append(f"FAILED - {len(retention_failures)} violation(s):")
        L += [f"- {f}" for f in retention_failures]
    else:
        L.append("OK - every base file's original content is an exact prefix of the "
                 "merged file (protected pages byte-identical).")
    L.append("")
    if not dry_run:
        L += ["## Link integrity", ""]
        if broken_after:
            L.append(f"FAILED - {len(broken_after)} broken link(s):")
            L += [f"- {b}" for b in broken_after[:50]]
        else:
            L.append("OK - 0 broken relative links across the unified wiki.")
        L.append("")
    L += [
        "## Notes", "",
        "- Tier-2 merges append a delimited `<!-- BEGIN merged:... -->` block into the base "
        "page (base text stays a prefix). The se-unify-wiki skill's advanced mode rewrites "
        "these into true synthesized prose.",
        "- Contradictions from the augment are carried **flagged, not resolved**.",
        f"- Re-running is guarded by a `<!-- BEGIN unified:{aug_dir.name} -->` marker "
        "(use `--force`). Revert via the backup above or `git checkout -- "
        f"{base_dir.name}`.",
        "",
    ]
    report_md.write_text("\n".join(x for x in L if x is not None), encoding="utf-8")

    report_json.write_text(json.dumps({
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "dry_run": dry_run, "label": label, "base": str(base_dir),
        "augment": str(aug_dir), "strategy": args.strategy, "thresholds": thresholds,
        "tier_counts": tier_counts, "base_retention_pct": retention_pct,
        "base_pages_appended": base_modified,
        "broken_links_after": (None if dry_run else broken_after),
        "contradictions_carried": contradictions,
        "actions": [{"aug": a["aug"].relpath, "tier": a["tier"],
                     "match": a["match"].relpath if a["match"] else None,
                     "score": a["score"], "final": a["final_rel"]} for a in actions],
        "retention_failures": retention_failures,
        "preserve": args.preserve, "protect": args.protect,
        "downgrades": downgrades, "backup": backup_path,
    }, indent=2), encoding="utf-8")
    print(f"Report written: {report_md}")
    print(f"Report JSON   : {report_json}")


if __name__ == "__main__":
    sys.exit(main())
