---
applyTo: "**"
---

# SE SharePoint Wiki — Usage Guidelines

## Grounding Policy: SharePoint-First, with Optional Private Local Layer

SE Brain uses a **two-tier knowledge model**:

| Tier | Source | Role | When |
|------|--------|------|------|
| **1. Universal (authoritative)** | SharePoint wiki (`microsoftapc.sharepoint.com/teams/se-brain-wiki`) | Shared source of truth for all SEs | **Always** queried first via `wiki_read` |
| **2. Private (augmentation)** | Local `KB-Local/` folder (gitignored) | The user's personal notes and private context | **Optional** — used only if it adds value |

**ALL universal knowledge retrieval MUST go through the SharePoint wiki site.** The agent must NEVER read the stale local mirrors (`mock-data/`, `wiki/`, `wiki-steady-state/`, `raw/`, `raw-steady-state/`, `broadcasts/`) for data. The **only** sanctioned local read location is `KB-Local/`.

This ensures:
- **Single source of truth** — shared data is centrally managed on SharePoint
- **Access control** — SharePoint permissions govern who sees what
- **Live updates** — changes on SharePoint are immediately reflected without git operations
- **Domain restriction** — SE Brain's universal knowledge is scoped exclusively to `microsoftapc.sharepoint.com/teams/se-brain-wiki`
- **Private augmentation** — users keep personal notes locally in `KB-Local/` without polluting the shared wiki

### Enforcement Rules

1. **Always query SharePoint first** via `wiki_read` for any account, pipeline, compete, or wiki content. It is the authoritative backbone of every answer.
2. **Do NOT use `read_file` on the stale mirrors**: `mock-data/`, `wiki/`, `wiki-steady-state/`, `raw/`, `raw-steady-state/`, or `broadcasts/`.
3. **Do NOT use `grep_search` or `file_search`** to find data in those mirror directories.
4. **If `wiki_read` fails**, inform the user the SharePoint connection is required — do not silently fall back to the local mirrors.
5. **Optional private layer**: after grounding in SharePoint, you MAY scan `KB-Local/` for the user's personal notes. `KB-Local/` is gitignored, so `file_search` cannot see it — discover notes with `grep_search` (`includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`), then read with `read_file`. Fold in only if relevant; skip silently otherwise.
6. **Precedence**: SharePoint is authoritative for shared facts. `KB-Local/` notes are additive — they never override shared truth and never substitute for it. On a conflict, SharePoint wins and the agent flags it. If SharePoint is unreachable, do NOT build an answer from `KB-Local/` alone — inform the user the connection is required.
7. **Labeling**: clearly attribute any local-sourced content as "From your local notes (KB-Local)" so the user always knows the origin.

## Architecture

The wiki is stored in a SharePoint Document Library at **microsoftapc.sharepoint.com/teams/se-brain-wiki** and accessed directly via Microsoft Graph API through the `se-graph-wiki` MCP server.

```
Skills → MCP Tools → Graph API → SharePoint Document Library
        (wiki_read,    (auth'd)    (wiki-steady-state/, broadcasts/, mock-data/)
         wiki_write,
         wiki_list,
         wiki_search,
         wiki_delete)
```

## Available Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `wiki_read` | Read a file from SharePoint | `wiki_read("wiki-steady-state/concepts/compete-landscape.md")` |
| `wiki_write` | Write/update a file | `wiki_write("broadcasts/2026-06-08-deck-gen.md", content)` |
| `wiki_list` | List folder contents | `wiki_list("wiki-steady-state/concepts")` |
| `wiki_search` | Search by keyword | `wiki_search("compete Google")` |
| `wiki_delete` | Delete a file (recycle bin) | `wiki_delete("broadcasts/old-file.md")` |

## When to Use These Tools

**Use `wiki_read` when:**
- Any skill needs to read wiki content (accounts, pipeline, compete, concepts)
- Loading index files to find relevant pages
- Fetching raw data files (mock-data/*.json)

**Use `wiki_write` when:**
- Broadcasting insights to the universal repo
- Updating wiki pages after new analysis
- Pushing new data (accounts, pipeline updates)
- Filing analyses back into the knowledge base

**Use `wiki_list` when:**
- Discovering what pages exist in a directory
- Checking for new content that hasn't been indexed
- Browsing folder structure

**Use `wiki_search` when:**
- Finding relevant wiki pages by keyword
- Locating files when the exact path is unknown
- Cross-referencing topics across the wiki

**Do NOT use these tools for:**
- General knowledge questions unrelated to SE internal content
- Code generation or debugging tasks
- External/public information lookups (use `fetch_webpage` instead)

## Path Convention

Paths in SharePoint mirror the local repo structure:
```
wiki/                         → Onboarding wiki
wiki-steady-state/            → Execution-phase wiki
broadcasts/                   → Shared insights
mock-data/                    → Account and pipeline data
raw-steady-state/             → Immutable source documents
```

## How to Present Results

When returning results from the SharePoint wiki:
1. Summarize the response clearly with headings and bullet points
2. Note that the answer is grounded in **SE SharePoint wiki content**
3. If a file is not found (404), check the path with `wiki_list` and retry
