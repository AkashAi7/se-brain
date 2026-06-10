---
name: se-wiki-generator
description: 'Incrementally build and maintain an LLM-generated wiki from raw source documents. Use when asked to "build the wiki", "generate wiki", "ingest sources", "update wiki", "compile wiki", "create wiki pages", "synthesize sources", "link concepts", "lint wiki", or "health-check wiki". Reads raw sources from the SharePoint raw dump (via wiki_read/wiki_list) plus the optional local KB-Local/ folder, and produces a structured, interlinked collection of markdown files in the LOCAL wiki/ — summaries, entity pages, concept pages, comparisons, an overview, and a synthesis. Source references point to the SharePoint wiki site. Maintains cross-references, backlinks, index, and changelog automatically.'
---

# Wiki Generator

Incrementally compile and maintain a structured, interlinked wiki from the raw source documents. This skill implements the **Wiki layer** of the LLM Wiki pattern — an LLM-owned directory of markdown files that the user reads and the LLM writes.

## Knowledge Architecture (read this first)

The raw dump no longer lives on your local disk. It lives on SharePoint, with an optional private local layer. The wiki you build is the **local** synthesized layer on top of it.

| Layer | Where it lives | Role | How to access |
|-------|----------------|------|---------------|
| **Raw dump — shared** | SharePoint at `microsoftapc.sharepoint.com/teams/se-brain-wiki` under `raw/` | Authoritative source documents | `wiki_read(path)`, `wiki_list(folder)`, `wiki_search(query)` MCP tools |
| **Raw dump — private** | Local `KB-Local/` folder (gitignored) | The user's personal source notes | `grep_search` (`includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`) to discover, `read_file` to read |
| **Wiki (this skill's output)** | **Local `wiki/` folder** | Synthesized, interlinked knowledge | `read_file` / `create_file` / `edit` — you own this directory entirely |

**Direction of work:** read raw from SharePoint (`wiki_read`) **+ KB-Local** → write the compiled wiki **locally** in `wiki/`.

- **NEVER** use `wiki_read`/`wiki_write` against the `wiki/` path — the wiki is a local artifact, not a SharePoint mirror. Read and write it with the local file tools.
- **NEVER** read a stale local `raw/` mirror if one exists — the authoritative raw dump is on SharePoint. If `wiki_read` is unavailable, tell the user the SharePoint connection is required; do not silently fall back to a local `raw/` copy. `KB-Local/` is the only sanctioned local *source* read.
- **Source references in wiki pages point to SharePoint.** Convert any raw path to a clickable SharePoint URL:
  `https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/<path>` (spaces → `%20`). KB-Local-derived material is labeled "From local notes (KB-Local)" and has no SharePoint URL.

## When to Use This Skill

- User says "build the wiki", "generate wiki from sources", "compile wiki"
- User drops a new source in `raw/` and says "ingest this"
- User says "update wiki", "refresh wiki", "sync wiki with sources"
- User asks to "lint the wiki", "health-check", or "find gaps"
- User wants new concept pages, entity pages, comparisons, or summaries generated
- User asks to file an answer or analysis back into the wiki

## Prerequisites

- The `wiki_read` / `wiki_list` / `wiki_search` MCP tools (provided by the `se-graph-wiki` server) connected to the SharePoint raw dump
- At least one source file in the SharePoint `raw/` folder (or in local `KB-Local/`)
- Each shared source on SharePoint should have YAML frontmatter with `title`, `url`, `date_retrieved`, `source_type`, and `tags`
- `raw/sources.md` manifest on SharePoint (recommended but not required — the skill can list `raw/` via `wiki_list("raw")` directly)

## Directory Structure

The skill creates and maintains the following structure **locally** (the SharePoint side only holds the `raw/` sources):

```
wiki/
├── index.md                    # Master catalog of all wiki pages
├── log.md                      # Chronological record of operations
├── overview.md                 # High-level synthesis of the entire topic
├── sources/                    # One summary page per raw source
│   ├── <source-slug>.md
│   └── ...
├── concepts/                   # Concept and topic pages
│   ├── <concept-slug>.md
│   └── ...
├── entities/                   # Entity pages (people, orgs, tools, etc.)
│   ├── <entity-slug>.md
│   └── ...
├── comparisons/                # Side-by-side analyses
│   ├── <comparison-slug>.md
│   └── ...
└── analyses/                   # Filed query answers and deep-dives
    ├── <analysis-slug>.md
    └── ...
```

## Page Formats

### Common Frontmatter

Every wiki page MUST include YAML frontmatter:

```yaml
---
title: "Page Title"
type: source-summary | concept | entity | comparison | analysis | overview
created: "2026-04-05"
updated: "2026-04-05"
sources: [raw/source-slug.md, raw/another-source.md]
tags: [tag1, tag2]
backlinks: [wiki/concepts/related-concept.md]
---
```

> **`sources:` paths are SharePoint raw paths.** Entries like `raw/source-slug.md` identify documents in the SharePoint raw dump. When you render them as clickable links in page bodies, expand them to the SharePoint URL: `https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/raw/source-slug.md`. A source that came from `KB-Local/` instead gets a `kb-local/<file>.md` entry and is attributed inline as "From local notes (KB-Local)" — it has no SharePoint URL. `backlinks:` paths stay as local `wiki/` relative paths.

### Source Summary Page (`wiki/sources/`)

One page per raw source. Contains:

```markdown
---
title: "Summary: <Source Title>"
type: source-summary
created: "2026-04-05"
updated: "2026-04-05"
sources: [raw/<source-slug>.md]
tags: [tag1, tag2]
backlinks: []
---

# <Source Title>

> Source: [Original Title](original-url) | On SharePoint: [raw/<source-slug>.md](https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/raw/<source-slug>.md) | Retrieved: YYYY-MM-DD | Type: article

## Key Takeaways

- Bullet-point summary of the most important claims, findings, or arguments.

## Detailed Summary

Multi-paragraph summary preserving the source's structure and nuance.

## Notable Claims

| Claim | Confidence | Corroborated By | Contradicted By |
|-------|-----------|-----------------|-----------------|
| ...   | ...       | [[link]]        | [[link]]        |

## Entities Mentioned

- [[Entity Name]] — brief context of how this entity appears in the source.

## Concepts Touched

- [[Concept Name]] — brief context.

## Questions Raised

- Open questions this source raises that could be investigated further.
```

### Concept Page (`wiki/concepts/`)

```markdown
---
title: "Concept Name"
type: concept
created: "2026-04-05"
updated: "2026-04-05"
sources: [raw/source1.md, raw/source2.md]
tags: [tag1, tag2]
backlinks: [wiki/sources/source1.md, wiki/entities/entity1.md]
---

# Concept Name

## Definition

Clear, synthesized definition drawing from all relevant sources.

## Key Points

- Synthesized from multiple sources. Each point cites its source(s).

## How Sources Relate to This Concept

| Source | Perspective | Key Contribution |
|--------|------------|-----------------|
| [[Source 1]] | ... | ... |
| [[Source 2]] | ... | ... |

## Contradictions and Open Questions

- Where sources disagree or where gaps remain.

## Related Concepts

- [[Other Concept]] — how they connect.

## Related Entities

- [[Entity]] — relationship to this concept.
```

### Entity Page (`wiki/entities/`)

Follows the same pattern as concept pages but focused on a specific person, organization, tool, place, or other named entity. Include: description, role/significance, appearances across sources, relationships to other entities and concepts.

### Comparison Page (`wiki/comparisons/`)

Side-by-side analysis of two or more entities or concepts. Include a comparison table, a narrative synthesis, and source citations.

### Analysis Page (`wiki/analyses/`)

For query answers and deep-dives that get filed back into the wiki. Include the original question, the synthesized answer, citations, and how this analysis connects to existing pages.

### Overview Page (`wiki/overview.md`)

A single page that synthesizes the entire wiki into a coherent narrative. Updated after every ingest. Serves as the "front page" — anyone reading this page should get the gist of the entire knowledge base.

## Core Operations

### Operation 1: Ingest

Triggered when new source(s) land in the SharePoint `raw/` dump (or in local `KB-Local/`) and the user asks the LLM to process them. This is the most common operation.

**Workflow:**

1. **Identify new sources.**
   - Shared: `wiki_read("raw/sources.md")` for the manifest, or `wiki_list("raw")` to enumerate. Compare against the local `wiki/index.md` to find sources not yet ingested.
   - Private: discover any relevant `KB-Local/` notes with `grep_search` (`includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`). `file_search` cannot see `KB-Local/` because it is gitignored.

2. **Read each new source.**
   - Shared sources: `wiki_read("raw/<file>.md")` — parse the frontmatter and full content directly from the tool result. Do NOT write the result to a temp file and re-parse it.
   - Private sources: `read_file` on the `KB-Local/` path. Never read local files outside `KB-Local/` as sources.

3. **Create source summary page.** Write `wiki/sources/<slug>.md` with the source summary format above. Extract key takeaways, notable claims, entities, and concepts.

4. **Extract entities and concepts.** For each entity and concept mentioned in the source:
   - If a wiki page already exists → **update it**: add the new source to the `sources` list, update the narrative to incorporate new information, add rows to tables, note contradictions if any.
   - If no wiki page exists → **create it**: write a new page in `wiki/concepts/` or `wiki/entities/` using the templates above.

5. **Update cross-references.** For every page touched in this ingest:
   - Ensure `backlinks` frontmatter lists all pages that link TO this page.
   - Ensure inline `[[wikilinks]]` or markdown links connect related pages.
   - Use relative paths: `[Concept](../concepts/concept-slug.md)`.

6. **Update overview.md.** Revise the overview to reflect the new source's contribution. What changed in the big picture?

7. **Update index.md.** Add new pages to the index table. Update one-line summaries if existing pages changed significantly.

8. **Append to log.md.** Add a timestamped entry:
   ```markdown
   ## [2026-04-05] ingest | Source Title
   - Created: wiki/sources/source-slug.md
   - Updated: wiki/concepts/concept-a.md, wiki/entities/entity-b.md
   - Created: wiki/entities/new-entity.md
   - Pages touched: 7
   ```

9. **Report to user.** Summarize what was created/updated, highlight interesting findings, note contradictions with existing wiki content, suggest follow-up questions.

### Operation 2: Full Build

For bootstrapping — when there's no local wiki yet but the SharePoint `raw/` dump (and/or `KB-Local/`) has multiple sources. Runs Ingest on every source, then does a final cross-referencing pass.

**Workflow:**

1. Create the local `wiki/` directory structure (all subdirectories).
2. Initialize `wiki/index.md`, `wiki/log.md`, `wiki/overview.md` as stubs.
3. Enumerate every source via `wiki_list("raw")` (shared) and the `KB-Local/` scan (private), then ingest each one by one (follow Ingest workflow above).
4. After all sources are ingested, do a **cross-reference pass**:
   - Scan all concept and entity pages for potential links that were missed.
   - Identify concepts that appear across 3+ sources — these deserve dedicated pages if they don't have them.
   - Generate comparison pages for entities/concepts that are frequently contrasted.
5. Update `wiki/overview.md` with a comprehensive synthesis.
6. Final update of `wiki/index.md`.
7. Log the full build event.

### Operation 3: Query & File

When the user asks a question and the answer is worth preserving.

**Workflow:**

1. Read the local `wiki/index.md` to find relevant pages.
2. Read the relevant local wiki pages — the wiki should already hold the synthesized knowledge and overview/context.
3. Only if a wiki page lacks a specific detail, fetch the *specific* raw document it references from the dump — `wiki_read("raw/<that-file>.md")` (or `read_file` on the `KB-Local/` note). Don't blanket-scan the raw dump.
4. Synthesize an answer with citations to local wiki pages and ultimately to the SharePoint raw URLs.
5. If the user wants to keep the answer: save it as `wiki/analyses/<slug>.md` (local).
6. Update `wiki/index.md` and `wiki/log.md` (local).

For full query behavior, defer to the **se-query-wiki** skill — this operation is just the "file it back" tail of that flow.

### Operation 4: Lint

Health-check the wiki for quality and completeness.

**Workflow:**

1. **Orphan check.** Find pages with zero inbound backlinks (no other page links to them). Flag them.
2. **Dead link check.** Find links that point to pages that don't exist. Either create the missing page or fix the link.
3. **Contradiction scan.** Read pairs of pages that reference the same claim and check for conflicting statements. Flag contradictions with source citations.
4. **Staleness check.** Compare `updated` dates in frontmatter. Flag pages not updated since significantly newer sources were ingested.
5. **Coverage gaps.** Look for entities or concepts mentioned in 2+ source summaries but lacking their own dedicated page.
6. **Missing backlinks.** Scan page bodies for references to other pages and ensure the `backlinks` frontmatter is up to date.
7. **Index consistency.** Verify every file in `wiki/` is listed in `index.md` and every entry in `index.md` points to an existing file.
8. **Report findings.** Present a structured lint report to the user with suggested fixes. Offer to auto-fix what's safe (e.g., creating missing pages, adding backlinks).

## Index Format (`wiki/index.md`)

```markdown
---
title: "Wiki Index"
type: index
updated: "2026-04-05"
---

# Wiki Index

> Auto-maintained catalog of all wiki pages. Updated on every ingest.

## Overview

- [Overview](overview.md) — High-level synthesis of the entire knowledge base.

## Source Summaries

| Source | Type | Tags | Page |
|--------|------|------|------|
| [Title](raw-url) | article | tag1, tag2 | [Summary](sources/slug.md) |

## Concepts

| Concept | Sources | Page |
|---------|---------|------|
| Concept Name | 3 | [Page](concepts/slug.md) |

## Entities

| Entity | Type | Sources | Page |
|--------|------|---------|------|
| Entity Name | person | 2 | [Page](entities/slug.md) |

## Comparisons

| Comparison | Page |
|-----------|------|
| X vs Y | [Page](comparisons/x-vs-y.md) |

## Analyses

| Question | Date | Page |
|----------|------|------|
| How does X relate to Y? | 2026-04-05 | [Page](analyses/slug.md) |
```

## Log Format (`wiki/log.md`)

```markdown
---
title: "Wiki Log"
type: log
---

# Wiki Log

> Append-only chronological record. Newest entries at the bottom.

## [2026-04-05] build | Initial wiki build
- Sources ingested: 8
- Pages created: 24
- Concepts: 6, Entities: 10, Comparisons: 2

## [2026-04-05] ingest | New Article Title
- Created: wiki/sources/new-article.md
- Updated: wiki/concepts/concept-a.md (+1 source)
- Created: wiki/entities/new-person.md
- Pages touched: 5

## [2026-04-05] lint | Health check
- Orphan pages found: 2
- Missing backlinks fixed: 4
- Coverage gaps: 1 new concept page suggested
```

## Cross-Referencing Rules

1. **Every source summary** must link to the concept and entity pages it references.
2. **Every concept/entity page** must link back to the source summaries it draws from.
3. **Backlinks frontmatter** must list all pages that link TO the current page. Update this whenever a linking page is created or modified.
4. **Use relative markdown links**: `[Concept Name](../concepts/concept-slug.md)` — not absolute paths, not bare wikilinks (unless the user's tooling supports them, in which case `[[concept-slug]]` is acceptable).
5. **The overview** should link to the most important concept and entity pages.
6. **When updating a page**, check if any new links should be added to other pages that reference the same entities/concepts.

## Incremental Updates

The wiki is designed to grow incrementally. Key principle: **never regenerate from scratch** when you can update in place.

- When a new source corroborates an existing claim → update the claim's confidence and add the source citation.
- When a new source contradicts an existing claim → add a "Contradictions" section or row, cite both sources.
- When a new source introduces a new entity/concept → create a new page and link it into the existing graph.
- When a new source significantly changes the big picture → update `overview.md`.

## Tips

- **Start small.** On first build, don't try to create pages for every minor entity. Focus on concepts and entities that appear in 2+ sources. Single-mention entities can be noted in the source summary.
- **Let the user guide emphasis.** After presenting ingest results, ask the user what to dig into further. They may want more detail on one concept and less on another.
- **Prefer updating over creating.** A rich, well-sourced concept page is more valuable than many thin pages. Only create a new page when a topic has enough substance to justify it.
- **Keep summaries honest.** Don't hallucinate claims. Every statement in the wiki should trace back to a raw source. If you're uncertain, say so in the page.
- **Flag contradictions explicitly.** Contradictions between sources are extremely valuable — they tell the user where to dig deeper. Never silently resolve a contradiction by picking one side.

## Troubleshooting

| Issue | Solution |
|-------|---------|
| `wiki_list("raw")` empty and no `KB-Local/` notes | No sources to ingest. Run the **se-open-research** / **se-work-research** skill to populate the SharePoint raw dump first. |
| `wiki_read`/`wiki_list` unavailable or auth error | Tell the user the SharePoint connection is required (e.g. "run `az login` to refresh credentials"). Do NOT fall back to a stale local `raw/` mirror. |
| Source has no frontmatter | Parse what you can from the filename and content. Note the missing metadata in the source summary. |
| Wiki pages are getting too long | Split into sub-pages (e.g., `concepts/machine-learning/supervised.md`) and link from the parent. |
| Backlinks are stale | Run the **lint** operation to detect and fix stale backlinks. |
| `index.md` out of sync | Scan all files in `wiki/` and regenerate the index tables. |
| Conflicting information | Never silently resolve — always flag in a "Contradictions" section with citations to both sources. |
