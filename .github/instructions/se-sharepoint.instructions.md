---
applyTo: "**"
---

# SE SharePoint Wiki — Usage Guidelines

## Knowledge Architecture: Local Wiki over SharePoint Raw Dump

SE Brain separates the **synthesized wiki layer** from the **raw source dump**, and the order you touch them matters. There is **one wiki, and it is local.** SharePoint holds only the raw dumps.

| Layer | Where | Role | Access |
|-------|-------|------|--------|
| **Wiki (synthesized)** | **Local `wiki/`** | Compiled overview/context — the first stop for every answer | local `read_file` |
| **Raw dump — shared** | SharePoint (`microsoftapc.sharepoint.com/teams/se-brain-wiki`) | Authoritative source documents | `wiki_read` / `wiki_list` / `wiki_search` |
| **Raw dump — private** | Local `KB-Local/` (gitignored) | The user's personal source notes | `grep_search` → `read_file` |

**The non-negotiable retrieval flow:** consult the **local wiki first** for overview and context, then fetch **only the specific raw documents** the wiki points to. Never bypass the wiki to scan or dump the raw source dump.

This ensures:
- **Wiki as the lens** — the compiled local wiki gives the overview; the raw dump is consulted *through* it, one referenced doc at a time
- **Single source of truth for raw sources** — the shared raw dump is centrally managed on SharePoint
- **Live updates** — changes to the raw dump on SharePoint are immediately reflected without git operations
- **Private augmentation** — users keep personal source notes locally in `KB-Local/` without polluting the shared dump

### Enforcement Rules

1. **Read the local wiki first.** `read_file` the relevant `wiki/` pages for overview and context. This is the backbone of every answer.
2. **Then fetch the actual data from SharePoint.** Using the wiki's cues, `wiki_read` the *specific* raw files it points to (and `read_file` any cited `KB-Local/` note), and ground the answer's specifics in them. This runs on every data-backed answer — it is not a fallback for when the wiki "lacks detail." Target the cited docs; never blanket-`wiki_search`/`wiki_list` the raw dump and return its contents directly.
3. **The `wiki/` is LOCAL — read it with `read_file`, not `wiki_read`.** It is the compiled knowledge base, not a SharePoint mirror. SharePoint does not store the wiki.
4. **Do NOT use `read_file` on a stale local `raw/` mirror.** The authoritative raw dump is on SharePoint; `KB-Local/` is the only sanctioned local *source* read.
5. **If `wiki_read` fails**, inform the user the SharePoint connection is required — answer from the wiki alone and flag the missing detail; do not silently fall back to a stale local raw mirror.
6. **Optional private layer**: after grounding in the wiki, you MAY scan `KB-Local/` for the user's personal notes. `KB-Local/` is gitignored, so `file_search` cannot see it — discover with `grep_search` (`includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`), then `read_file`. Fold in only if relevant; skip silently otherwise.
7. **Precedence**: SharePoint shared sources are authoritative for shared facts. `KB-Local/` notes are additive — they never override shared truth and never substitute for it. On a conflict, SharePoint wins and the agent flags it.
8. **Labeling**: clearly attribute any local-sourced content as "From your local notes (KB-Local)" so the user always knows the origin.

## Architecture

The **raw source dump** is stored in a SharePoint Document Library at **microsoftapc.sharepoint.com/teams/se-brain-wiki** and accessed via Microsoft Graph API through the `se-graph-wiki` MCP server. The **wiki is built locally** from that dump and is **not** stored on SharePoint.

```
Local wiki/  ← read first (read_file)         The synthesized layer
     │  cites specific raw docs
     ▼
Skills → MCP Tools → Graph API → SharePoint Document Library
        (wiki_read,    (auth'd)    (the raw dump — source documents)
         wiki_write,                + local KB-Local/ for private sources
         wiki_list,
         wiki_search,
         wiki_delete)
```

## Available Tools

These tools operate on the **SharePoint raw dump**. The local `wiki/` is read/written with the ordinary local file tools (`read_file` / `create_file` / `edit`), never these.

| Tool | Purpose | Example |
|------|---------|---------|
| `wiki_read` | Read a raw doc from SharePoint | `wiki_read("raw/se-day-1-complete-starter-guide.md")` |
| `wiki_write` | Write/update a raw doc or the manifest | `wiki_write("raw/sources.md", content)` |
| `wiki_list` | List folder contents | `wiki_list("raw")` |
| `wiki_search` | Locate a raw file by keyword | `wiki_search("day 1 access")` |
| `wiki_delete` | Delete a file (recycle bin) | `wiki_delete("raw/old-file.md")` |

## When to Use These Tools

**Use `wiki_read` when:**
- A wiki page points to a specific raw source document you need a detail from
- Ingesting raw sources to build the local wiki (via **se-wiki-generator**)

**Use `wiki_write` when:**
- Adding a new shared source to the raw dump (or updating `raw/sources.md`)

**Use `wiki_list` when:**
- Enumerating the raw dump to find sources not yet ingested into the wiki

**Use `wiki_search` when:**
- Locating a specific raw file when the exact path is unknown — to then read *that* file, not to bulk-dump the raw content

**Do NOT use these tools for:**
- Reading the wiki — that is local (`read_file`)
- General knowledge questions unrelated to SE internal content
- Code generation or debugging tasks
- External/public information lookups (use `fetch_webpage` instead)

## Path Convention

```
LOCAL                              SHAREPOINT (microsoftapc.sharepoint.com/teams/se-brain-wiki)
wiki/         → the one wiki       raw/            → raw source dump (read via wiki_read)
KB-Local/     → private sources    raw/sources.md  → manifest of collected sources
```

## Reading Data Efficiently

When fetching from SharePoint (raw docs, or any structured `mock-data/*.json` if present):

- **Parse JSON inline from the `wiki_read` result.** The tool returns the file contents directly in context — read and filter the records yourself. **Do NOT** write the tool output to a temp file and re-parse it with an external `python`/`Get-Content` command; that round-trip is brittle (it triggers `JSONDecodeError: Extra data` when the tool-output wrapper isn't pure JSON) and is unnecessary.
- **Return structured markdown, never raw JSON.** Surface tables, lists, and labeled sections to the user — never dump the raw file contents.
- **Max ~3 reads per question.** If you need more, you're over-reading. Go direct (read the path the wiki cited; don't browse first), cache within the conversation (don't re-read what you already pulled), and return only what's asked for.

## Error Handling

If `wiki_read` / `wiki_list` errors:
1. **404** — verify the path with `wiki_list`, then retry; if it genuinely doesn't exist, tell the user.
2. **Auth error** — tell the user the SharePoint connection is required (e.g. "run `az login` to refresh credentials").
3. **Never** fall back to a stale local `raw/` mirror — answer from the local wiki and flag the missing raw detail.

## How to Present Results

When returning results grounded in the wiki and raw dump:
1. Summarize the response clearly with headings and bullet points
2. Cite local wiki pages (relative links) and raw sources (SharePoint URLs: `https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/<path>`, spaces → `%20`)
3. If a raw file is not found (404), check the path with `wiki_list` and retry
