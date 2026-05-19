---
name: open-research
description: 'Research a topic on the internet and build a curated collection of raw source documents. Use when asked to "research a topic", "gather sources", "collect articles", "find papers on", "build a source collection", "populate raw sources", "open research on", or "curate sources for". Fetches web articles, papers, and data, converts them to markdown, and saves them as immutable files in a raw/ directory. Supports the LLM Wiki pattern by populating the raw source layer.'
---

# Open Research

Gather raw sources from the internet on a given topic and organize them into an immutable `raw/` collection. This skill populates the **Raw sources** layer of the LLM Wiki pattern — a curated set of source documents that the LLM reads from but never modifies.

## When to Use This Skill

- User wants to research a new topic and collect source material
- User says "research X", "gather sources on X", "find articles about X"
- User wants to populate or expand the `raw/` directory with new sources
- User is bootstrapping a new LLM Wiki and needs initial source material

## Prerequisites

- Internet access via `fetch_webpage` tool (or equivalent browser/fetch tool)
- File creation tools to write sources to disk
- The workspace should have (or will get) a `raw/` directory at the project root

## Directory Structure

The skill creates and populates the following structure:

```
raw/
├── sources.md              # Manifest of all collected sources
├── assets/                 # Downloaded images and binary files
│   └── ...
├── <source-1-slug>.md      # Individual source documents
├── <source-2-slug>.md
└── ...
```

### File Naming Convention

Each source file is named with a URL-safe slug derived from the article title:
- Lowercase, hyphens instead of spaces, no special characters
- Max 60 characters for the slug portion
- Example: `attention-is-all-you-need.md`

### Source File Format

Every source markdown file MUST include YAML frontmatter:

```yaml
---
title: "The Original Article Title"
url: "https://example.com/article"
date_retrieved: "2026-04-05"
source_type: article | paper | report | data | reference | blog | forum
tags: [topic-tag-1, topic-tag-2]
---
```

After the frontmatter, include the full content converted to clean markdown. Preserve:
- All headings, lists, tables, and code blocks
- Image references (download images to `raw/assets/` and update paths)
- Author attribution and publication dates when available
- Any data tables or structured information

## Step-by-Step Workflow

### Step 1: Clarify the Research Topic

Ask the user (if not already clear):
- **What topic** to research
- **Scope**: broad survey vs. focused deep-dive
- **Source preferences**: academic papers, news articles, blog posts, documentation, data sets
- **Approximate number of sources** desired (default: 5-10 for a starting collection)

### Step 2: Create the `raw/` Directory Structure

Ensure the following exists:
```
raw/
raw/assets/
```

If `raw/sources.md` already exists, read it to understand what's already been collected — avoid duplicating existing sources.

### Step 3: Search and Discover Sources

Use available web search and fetch tools to find relevant sources. Strategy:

1. **Start broad**: Search for the main topic to find survey articles, Wikipedia entries, and overview pieces
2. **Follow references**: Good articles cite other good articles — note references worth fetching
3. **Go specific**: Search for subtopics, key entities, and specific claims that emerged
4. **Diversify source types**: Mix articles, papers, official docs, blog posts, and data where available
5. **Prioritize quality**: Prefer primary sources, peer-reviewed work, and authoritative references over aggregators

For each promising URL:
- Fetch the page content using `fetch_webpage`
- Evaluate whether the content is substantive enough to keep
- Skip paywalled, empty, or low-quality pages

### Step 4: Convert and Save Each Source

For each accepted source:

1. Extract the main content (strip navigation, ads, sidebars — `fetch_webpage` typically handles this)
2. Convert to clean markdown preserving structure
3. Add YAML frontmatter with metadata (title, url, date_retrieved, source_type, tags)
4. Save to `raw/<slug>.md`
5. If the source has important images:
   - Note image URLs in the markdown (use standard markdown image syntax)
   - Optionally download key images to `raw/assets/` and update references

### Step 5: Build the Source Manifest

Create or update `raw/sources.md` — a master catalog of all collected sources:

```markdown
# Source Manifest

> Auto-generated catalog of raw sources. Do not edit manually.
> Last updated: 2026-04-05

## Summary

- **Topic**: [Research Topic]
- **Total sources**: [N]
- **Date range**: [earliest retrieval] – [latest retrieval]

## Sources

| # | Title | Type | Tags | File |
|---|-------|------|------|------|
| 1 | [Article Title](url) | article | tag1, tag2 | [slug.md](slug.md) |
| 2 | ... | ... | ... | ... |
```

### Step 6: Report Results to the User

Provide a summary:
- How many sources were collected
- Brief description of each source (1 line)
- Any notable gaps or areas where more sources would help
- Suggestions for follow-up research directions

## Immutability Rule

**Files in `raw/` are IMMUTABLE once written.** The LLM must never modify an existing source file. If a source needs to be updated (e.g., a newer version of a paper is found), save it as a new file with a version suffix (e.g., `attention-is-all-you-need-v2.md`) and update the manifest.

The only exception is `raw/sources.md`, which is updated whenever new sources are added.

## Tips

- **Batch vs. interactive**: For broad topics, collect 5-10 sources in one pass. For focused research, collect 2-3 and discuss with the user before continuing.
- **Rate yourself**: After collecting sources, assess coverage. Are there obvious gaps? Conflicting viewpoints missing? Let the user know.
- **Tag consistently**: Use lowercase, hyphenated tags. Reuse existing tags from `sources.md` when possible.
- **Respect robots.txt and rate limits**: Don't hammer a single domain. Spread fetches across sources.
- **Prefer markdown-friendly sources**: Text-heavy articles convert well. Interactive apps, videos, and heavily scripted pages don't — note them in the manifest with a link but don't try to force-convert them.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `fetch_webpage` returns empty content | The page may be paywalled or JS-rendered. Note the URL in the manifest as "unfetched" and move on. |
| Source is a PDF | If the tool can't parse PDFs, save the URL in the manifest with `source_type: paper` and a note that manual download is needed. |
| Duplicate source found | Check `sources.md` before saving. If a source with the same URL exists, skip it. |
| Too many sources on a subtopic | Prioritize the most authoritative 2-3 and note the rest as "see also" in the manifest. |
| Images can't be downloaded | Leave the original URL in the markdown. Note in frontmatter: `images_local: false`. |
