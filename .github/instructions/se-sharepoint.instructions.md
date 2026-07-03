---
applyTo: "**"
---

# SE Azure DevOps Wiki Source Guidelines

## Knowledge Architecture: Local Wiki over Azure DevOps Raw Sources

SE Brain separates the synthesized wiki layer from the raw source dump, and the order you touch them matters. There is one wiki, and it is local. Azure DevOps now holds the shared raw source dump.

| Layer | Where | Role | Access |
|-------|-------|------|--------|
| **Wiki (synthesized)** | **Local `wiki/`** | Compiled overview/context; the first stop for every answer | local `read_file` |
| **Raw dump - shared** | Azure DevOps project `SE-Brain-AzDev/SE-Brain`, repo path `raw/` | Authoritative source documents | Azure DevOps MCP tools or a confirmed-current local checkout |
| **Raw dump - private** | Local `KB-Local/` (gitignored) | The user's personal source notes | `grep_search` -> `read_file` |

Canonical project URL: `https://dev.azure.com/SE-Brain-AzDev/SE-Brain`

Canonical raw source URL pattern:

```text
https://dev.azure.com/SE-Brain-AzDev/SE-Brain/_git/SE-Brain?path=/<path>
```

Example:

```text
https://dev.azure.com/SE-Brain-AzDev/SE-Brain/_git/SE-Brain?path=/raw/onboarding/onboarding-overview.md
```

## Retrieval Flow

1. **Read the local wiki first.** Read `wiki/index.md` and then the relevant `wiki/` pages for overview, context, and source paths.
2. **Fetch only the specific raw documents the wiki points to.** Use Azure DevOps MCP tools when available. A local `raw/` file may be read only when the workspace is the current Azure DevOps checkout or the user explicitly confirms it is current.
3. **Do not blanket-dump the raw source store.** Target the cited `raw/...` paths from the wiki; do not browse or paste large raw folders.
4. **Keep `wiki/` local.** The local wiki is the compiled knowledge layer. Do not store generated wiki pages in the Azure DevOps raw source area unless the user explicitly asks to publish them.
5. **Treat `raw/` as immutable.** Prefer adding new raw source files and updating manifests over rewriting historical source captures.
6. **Use `KB-Local/` only as an additive private layer.** Private notes never override shared Azure DevOps raw sources. On conflict, shared Azure DevOps sources win and the conflict should be flagged.
7. **Label private content clearly.** Attribute local-only content as "From your local notes (KB-Local)".

## Architecture

```text
Local wiki/  <- read first with local file tools      The synthesized layer
     | cites specific raw docs
     v
Skills -> Azure DevOps MCP / Git checkout -> Azure DevOps repo raw/
                                      + local KB-Local/ for private notes
```

The Azure DevOps MCP server is configured with:

```jsonc
"microsoft/azure-devops-mcp": {
  "type": "stdio",
  "command": "npx",
  "args": [
    "-y",
    "@azure-devops/mcp@latest",
    "SE-Brain-AzDev",
    "-d",
    "all",
    "-a",
    "interactive"
  ]
}
```

## Available Source Access Modes

Prefer these in order:

1. **Azure DevOps MCP** for reading, listing, searching, creating branches, committing, or opening PRs against the Azure DevOps project.
2. **Confirmed-current local checkout** for direct local reads from `raw/` and local file edits before a Git commit/PR.
3. **KB-Local** for private notes only.

Do not use the old SharePoint MCP (`wiki_read`, `wiki_write`, `wiki_list`, `wiki_search`) as the source of truth after this transition. If legacy SharePoint access is needed for backfill, label it as migration-only and move the resulting source into Azure DevOps `raw/`.

## Write Workflow for Shared Sources

When adding or updating shared raw source material:

1. Create or update the file under `raw/` in the Azure DevOps repo path.
2. Preserve YAML frontmatter and existing naming conventions.
3. Update the relevant manifest, usually `raw/sources.md`, if present for that source family.
4. Commit on a feature branch and open an Azure DevOps PR unless the user explicitly asks for a direct local-only change.
5. After merge or local acceptance, update the local `wiki/` through the wiki generator flow.
6. Update `wiki/index.md`, `wiki/log.md`, and backlinks when generated wiki content changes.

## Reading Data Efficiently

When fetching from Azure DevOps raw sources:

- Read only the few source files needed for the current answer, normally no more than three unless the task truly requires more.
- Parse structured source data directly from the fetched content.
- Return structured markdown, not raw JSON dumps.
- Cache within the conversation; do not re-read the same source repeatedly.

## Error Handling

If Azure DevOps source access fails:

1. **Not found** - verify the `raw/...` path against the Azure DevOps repo or the current local checkout.
2. **Auth error** - tell the user the Azure DevOps MCP interactive authentication or repo permissions need attention.
3. **MCP unavailable** - use the local `raw/` checkout only if it is known current; otherwise answer from the local wiki and flag that raw source verification is blocked.
4. **Legacy SharePoint mismatch** - do not silently fall back to SharePoint. Treat SharePoint as migration-only.

## How to Present Results

When returning results grounded in the wiki and raw dump:

1. Summarize the response clearly with headings and bullet points.
2. Cite local wiki pages with relative links.
3. Cite raw sources with Azure DevOps URLs using the canonical pattern above.
4. If a raw file cannot be verified, say so explicitly and separate wiki-derived context from source-verified claims.
