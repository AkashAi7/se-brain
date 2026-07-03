---
name: se-lint-wiki
description: 'Health-check and maintain quality of an LLM-generated wiki. Use when asked to "lint the wiki", "health-check wiki", "check wiki quality", "find broken links", "find orphan pages", "check for contradictions", "find gaps in the wiki", "validate wiki", or "audit wiki". Scans wiki/ for orphan pages, dead links, stale content, contradictions, missing backlinks, coverage gaps, and index inconsistencies. Produces a structured report and offers to auto-fix safe issues.'
---

# Lint Wiki

Periodically health-check the wiki to keep it accurate, well-linked, and complete as it grows. This skill finds problems — orphans, dead links, contradictions, staleness, missing coverage — and either fixes them automatically or presents them to the user for decision.

## When to Use This Skill

- User says "lint the wiki", "health-check", "audit wiki", "check wiki quality"
- User says "find orphan pages", "find broken links", "check for contradictions"
- User says "what's missing in the wiki", "find gaps", "suggest new pages"
- After a large batch ingest to verify consistency
- Periodically as the wiki matures (every 10-20 ingests is a good cadence)

## Prerequisites

- A local `wiki/` directory with existing pages (produced by the **se-wiki-generator** skill) — the lint operates on this local wiki
- The Azure DevOps **raw dump** for cross-checking coverage (enumerate through Azure DevOps MCP tools or a confirmed-current local checkout); `KB-Local/` for private sources
- `wiki/index.md` for index consistency checks

> **Architecture note:** the wiki is **local** (read/edit with local file tools); the shared raw dump lives in **Azure DevOps**. Coverage checks compare the local `wiki/sources/` against Azure DevOps `raw/` plus any private `KB-Local/` notes.

## Lint Checks

The lint runs **7 checks** in order. Each produces findings that are categorized by severity.

### Severity Levels

| Level | Meaning | Auto-fix? |
|-------|---------|-----------|
| **error** | Broken — dead links, missing files referenced in index | Yes (safe fixes) |
| **warning** | Degraded quality — orphans, stale pages, missing backlinks | Yes (with user confirmation) |
| **info** | Improvement opportunity — coverage gaps, suggested pages | No (user decides) |

---

### Check 1: Orphan Pages

Find wiki pages with **zero inbound links** from other wiki pages.

**How:**
1. Scan every `.md` file under `wiki/`.
2. Extract all markdown links and wikilinks from each file.
3. Build an inbound-link map (page → list of pages linking to it).
4. Pages with zero inbound links are orphans.
5. Exclude `wiki/index.md`, `wiki/log.md`, and `wiki/overview.md` (these are root-level pages).

**Report format:**
```
ORPHAN PAGES (warning) — 3 found
  - wiki/entities/obscure-person.md — 0 inbound links
  - wiki/concepts/minor-concept.md — 0 inbound links
  - wiki/sources/old-article.md — 0 inbound links
Suggested fix: Add links from related pages, or remove if no longer relevant.
```

---

### Check 2: Dead Links

Find links in wiki pages that point to **files that don't exist**.

**How:**
1. Scan every `.md` file under `wiki/`.
2. Extract all relative markdown links (`[text](../path/file.md)`).
3. Resolve each link relative to the source file's directory.
4. Check if the target file exists on disk.
5. Also check wikilinks `[[slug]]` against known page slugs.

**Report format:**
```
DEAD LINKS (error) — 5 found
  - wiki/concepts/transformers.md → ../entities/missing-person.md (file not found)
  - wiki/sources/paper-summary.md → ../concepts/nonexistent.md (file not found)
Suggested fix: Create the missing page, or correct the link target.
```

**Auto-fix options:**
- If the target slug is close to an existing page (typo), offer to fix the link.
- If the target should exist but doesn't, offer to create a stub page.

---

### Check 3: Stale Content

Find pages whose `updated` date is **significantly older** than newer sources that cover the same topics.

**How:**
1. Read `updated` from each wiki page's frontmatter.
2. Read `date_retrieved` from each raw source's frontmatter.
3. For each wiki page, check if any of its listed `sources` have a newer date than the page's `updated` date.
4. Also flag concept/entity pages that haven't been updated since relevant new sources were ingested (cross-reference via tags).

**Report format:**
```
STALE PAGES (warning) — 2 found
  - wiki/concepts/attention-mechanisms.md — last updated 2026-03-15, but raw/new-attention-paper.md was ingested 2026-04-01
  - wiki/entities/openai.md — last updated 2026-02-20, 3 newer sources reference this entity
Suggested fix: Re-read the newer sources and update these pages.
```

---

### Check 4: Contradiction Scan

Find **conflicting claims** across wiki pages about the same topic.

**How:**
1. Identify pages that share overlapping `sources` or `tags`.
2. Read the "Notable Claims" tables and key assertions from each page.
3. Compare claims that address the same fact — different numbers, dates, attributions, or conclusions.
4. Also check if source summary pages flag contradictions that haven't been reflected in the relevant concept/entity pages.

**Report format:**
```
CONTRADICTIONS (warning) — 1 found
  - Claim: "Transformer model introduced in 2017"
    wiki/sources/attention-paper.md says: 2017 (from raw/attention-paper.md)
    wiki/sources/ml-history.md says: 2018 (from raw/ml-history.md)
    Status: Not yet flagged in wiki/concepts/transformer-architecture.md
Suggested fix: Add a "Contradictions" section to the concept page citing both sources.
```

**Important:** Never resolve contradictions. Only flag them. The user decides which source is correct.

---

### Check 5: Coverage Gaps

Find concepts and entities **mentioned in sources but lacking their own wiki page**.

**How:**
1. Scan all `wiki/sources/*.md` files for "Entities Mentioned" and "Concepts Touched" sections.
2. Extract all entity and concept names referenced.
3. Check if each has a corresponding page in `wiki/entities/` or `wiki/concepts/`.
4. Flag any that appear in **2 or more source summaries** but have no dedicated page.
5. Also scan for raw sources not yet ingested — enumerate Azure DevOps `raw/` (plus any `KB-Local/` notes) and flag any missing from the local `wiki/sources/`.

**Report format:**
```
COVERAGE GAPS (info) — 4 found
  Concepts without pages:
  - "self-attention" — mentioned in 3 source summaries, no wiki/concepts/ page
  - "positional encoding" — mentioned in 2 source summaries, no wiki/concepts/ page
  Entities without pages:
  - "Ashish Vaswani" — mentioned in 2 source summaries, no wiki/entities/ page
  Unprocessed sources:
  - raw/new-article.md — present in raw/ but not yet ingested into wiki
Suggested fix: Create pages for high-frequency concepts/entities. Ingest unprocessed sources.
```

---

### Check 6: Missing Backlinks

Find pages where the `backlinks` frontmatter is **out of date** — pages link to them but aren't listed.

**How:**
1. Build the full inbound-link map (same as Check 1).
2. For each page, compare the actual inbound links against the `backlinks` array in frontmatter.
3. Flag any discrepancies (missing entries or entries for links that no longer exist).

**Report format:**
```
MISSING BACKLINKS (error) — 8 found
  - wiki/concepts/attention.md — backlinks missing: wiki/sources/paper-a.md, wiki/entities/researcher.md
  - wiki/entities/google.md — backlinks missing: wiki/comparisons/google-vs-openai.md
  - wiki/sources/old-paper.md — stale backlink: wiki/concepts/deleted-concept.md (page no longer exists)
Auto-fix: Update backlinks frontmatter to match actual inbound links.
```

**Auto-fix:** This is always safe to auto-fix — just update the `backlinks` array to reflect reality.

---

### Check 7: Index Consistency

Verify that `wiki/index.md` is **in sync** with the actual files on disk.

**How:**
1. Parse `wiki/index.md` and extract all page links from the tables.
2. Scan all `.md` files under `wiki/` (recursively).
3. Flag files on disk that are NOT listed in the index.
4. Flag index entries that point to files that don't exist.

**Report format:**
```
INDEX INCONSISTENCIES (error) — 3 found
  Missing from index:
  - wiki/concepts/new-concept.md (exists on disk, not in index.md)
  - wiki/entities/new-entity.md (exists on disk, not in index.md)
  Phantom entries:
  - wiki/comparisons/deleted-comparison.md (in index.md, file not found)
Auto-fix: Add missing pages to index, remove phantom entries.
```

**Auto-fix:** Safe to auto-fix — add real files to index, remove phantom entries.

---

## Full Lint Workflow

1. **Run all 7 checks** in sequence, collecting findings.
2. **Compile the lint report** in the format below.
3. **Present to user** with summary counts.
4. **Offer auto-fixes** for safe issues (backlinks, index). Ask before fixing warnings.
5. **Log the lint** — append an entry to `wiki/log.md`:
   ```markdown
   ## [2026-04-05] lint | Health check
   - Orphan pages: 3
   - Dead links: 5
   - Stale pages: 2
   - Contradictions: 1
   - Coverage gaps: 4
   - Missing backlinks: 8
   - Index inconsistencies: 3
   - Auto-fixed: backlinks (8), index (3)
   ```

## Lint Report Format

```markdown
# Wiki Lint Report — 2026-04-05

## Summary

| Check | Errors | Warnings | Info |
|-------|--------|----------|------|
| Orphan pages | — | 3 | — |
| Dead links | 5 | — | — |
| Stale content | — | 2 | — |
| Contradictions | — | 1 | — |
| Coverage gaps | — | — | 4 |
| Missing backlinks | 8 | — | — |
| Index consistency | 3 | — | — |
| **Total** | **16** | **6** | **4** |

## Errors (auto-fixable)

[details for each error finding]

## Warnings (fix with confirmation)

[details for each warning finding]

## Info (user decides)

[details for each info finding]

## Suggested Next Steps

- [ ] Fix N dead links (auto-fix available)
- [ ] Update N backlinks (auto-fix available)
- [ ] Sync index.md (auto-fix available)
- [ ] Review N stale pages and update from newer sources
- [ ] Address N contradictions in concept pages
- [ ] Consider creating N new concept/entity pages
- [ ] Ingest N unprocessed raw sources
```

## Tips

- **Run lint after large batch ingests.** A batch of 5+ sources often introduces orphans and backlink drift.
- **Don't fix everything at once.** Focus on errors first, then warnings. Info items are suggestions, not problems.
- **Coverage gaps are research leads.** When the lint finds a concept mentioned in 3+ sources but lacking a page, that's a signal it's important enough to deserve one.
- **Contradictions are the most valuable findings.** They tell the user where to dig deeper or re-evaluate sources.
- **Run the helpers script for quick checks.** Use `python .github/skills/se-wiki-generator/scripts/helpers.py orphans wiki/` for a fast orphan scan without a full lint.

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Too many orphans after first build | Normal — run a cross-reference pass to link them in. Focus on pages with 2+ sources first. |
| Stale check flags everything | Happens when `updated` dates are missing from frontmatter. Fix the frontmatter first, then re-lint. |
| Contradiction scan too noisy | Narrow scope by running it on a single concept or tag at a time. |
| Index rebuild takes too long | Scan files first, generate index in one pass rather than reading each page fully. |
| Lint finds issues in raw/ | `raw/` is out of scope — only `wiki/` is linted. Source quality issues should be noted in the source summary page. |
