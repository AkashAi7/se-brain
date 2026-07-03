# Azure DevOps Source Store Setup

## Status

SE Brain is transitioning the shared raw source store from the legacy SharePoint Graph MCP server to Azure DevOps.

The authoritative shared source location is now:

```text
https://dev.azure.com/SE-Brain-AzDev/SE-Brain
```

The shared raw source tree is expected under:

```text
raw/
```

Keep raw source paths stable as `raw/...` so existing wiki frontmatter continues to resolve.

## Recommended MCP Server

Use the published Azure DevOps MCP server in VS Code/Copilot:

```jsonc
{
  "servers": {
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
      ],
      "gallery": "https://api.mcp.github.com",
      "version": "1.0.0"
    }
  }
}
```

This workspace already includes that server in `.vscode/mcp.json`.

## Retrieval Model

The wiki remains local. Azure DevOps owns shared raw sources.

```text
Local wiki/  -> read first with local file tools
     |
     v
Azure DevOps raw/ -> fetch only the specific raw files cited by wiki pages
     |
     v
Local wiki/ updates -> write generated summaries, concepts, analyses, index, and log locally
```

Use this order for data-backed answers:

1. Read `wiki/index.md`.
2. Read the relevant local wiki pages.
3. Fetch the specific `raw/...` files those pages cite from Azure DevOps.
4. Synthesize the answer with local wiki links and Azure DevOps raw source links.

Canonical raw source URL pattern:

```text
https://dev.azure.com/SE-Brain-AzDev/SE-Brain/_git/SE-Brain?path=/<path>
```

Example:

```text
https://dev.azure.com/SE-Brain-AzDev/SE-Brain/_git/SE-Brain?path=/raw/onboarding/onboarding-overview.md
```

## Write Model

Shared source updates should follow Git discipline:

1. Add or update source files under `raw/`.
2. Update `raw/sources.md` or the relevant manifest.
3. Commit on a feature branch.
4. Open an Azure DevOps PR unless the user explicitly asks for local-only staging.
5. After acceptance, run the wiki ingest/update flow locally.

Prefer adding new raw source files over rewriting historical source captures.

## Legacy SharePoint Server

The `se-graph-wiki` TypeScript server in this folder is retained as a legacy migration reference. It exposes the old SharePoint-style tools:

- `wiki_read`
- `wiki_write`
- `wiki_list`
- `wiki_search`
- `wiki_delete`

Do not use those tools as the source of truth after the Azure DevOps migration. If SharePoint is used for backfill, move the resulting source document into Azure DevOps `raw/` and cite the Azure DevOps location going forward.

## Troubleshooting

- **Azure DevOps MCP prompts for auth**: complete the interactive sign-in flow.
- **Repo or project not found**: verify the organization is `SE-Brain-AzDev` and the project is `SE-Brain`.
- **Raw path not found**: verify the file path starts with `raw/` and exists in the Azure DevOps repo.
- **MCP unavailable**: use a confirmed-current local checkout only if it is synced with Azure DevOps; otherwise answer from the local wiki and flag that raw verification is blocked.
