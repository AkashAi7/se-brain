# SE Graph Wiki — Setup Guide

## Overview

This MCP server lets SE Brain skills read and write wiki content to a SharePoint document library via Microsoft Graph API, using your authenticated identity.

**Architecture:**
```
Skills → MCP Tools → Graph API → SharePoint Site → Document Library
        (wiki_read,    (auth'd)    (/sites/X)     (wiki/, broadcasts/,
         wiki_write,                                mock-data/)
         wiki_list,
         wiki_search)
```

## Prerequisites

- Azure CLI installed (`az` command available)
- Node.js 18+ installed
- Access to a Microsoft 365 tenant (your @microsoft.com account)
- Permission to create SharePoint sites (or ask your admin)

## Step 1: Create a SharePoint Site

1. Go to https://microsoft.sharepoint.com
2. Click **+ Create site** → **Team site** (or Communication site)
3. Name it: `SE-Brain-Wiki`
4. Note the URL: `https://microsoft.sharepoint.com/sites/SE-Brain-Wiki`

The site comes with a default "Documents" library — that's where your wiki files will live.

## Step 2: Set Up Folder Structure in the Library

In the SharePoint Documents library, create these folders:
```
Documents/
├── wiki/
│   ├── analyses/
│   ├── concepts/
│   ├── entities/
│   └── sources/
├── wiki-steady-state/
│   ├── analyses/
│   ├── concepts/
│   ├── entities/
│   └── sources/
├── broadcasts/
├── mock-data/
└── raw-steady-state/
```

You can create these manually in the SharePoint UI, or the MCP server will auto-create folders when you write files (Graph API creates parent folders on PUT).

## Step 3: Authenticate Locally

For local development, the easiest approach is Azure CLI:

```powershell
az login
```

This gives `DefaultAzureCredential` access to Graph API using your identity.

**Your account needs these permissions:**
- `Files.ReadWrite.All` — to read/write files in SharePoint
- `Sites.ReadWrite.All` — to list sites and drives

These are typically available to Microsoft employees by default through your Microsoft 365 license.

## Step 3.5: Install Dependencies and Build

The MCP server runs from compiled JavaScript in `dist/`. If you see an error like
`Cannot find module '.../dist/index.js'`, the project hasn't been built yet.

From the server folder, install dependencies and compile the TypeScript:

```powershell
cd mcp-servers/se-graph-wiki
npm install
npm run build
```

This produces `dist/index.js`. You only need to rebuild (`npm run build`) after
changing files in `src/`. For continuous rebuilds during development, use `npm run dev`.

## Step 4: Configure the MCP Server

Edit `.vscode/mcp.json` and update the environment variables:

```json
{
  "se-graph-wiki": {
    "command": "node",
    "args": ["${workspaceFolder}/mcp-servers/se-graph-wiki/dist/index.js"],
    "env": {
      "GRAPH_SITE_HOSTNAME": "microsoft.sharepoint.com",
      "GRAPH_SITE_PATH": "/teams/se-brain-wiki",
      "GRAPH_LIBRARY_NAME": "Documents"
    }
  }
}
```

## Step 5: Test

```powershell
# Set env vars for manual testing
$env:GRAPH_SITE_HOSTNAME = "microsoftapc.sharepoint.com"
$env:GRAPH_SITE_PATH = "/teams/se-brain-wiki"
$env:GRAPH_LIBRARY_NAME = "Documents"

# Run the server (it uses stdio, so you'll see startup logs on stderr)
node mcp-servers/se-graph-wiki/dist/index.js
```

Once running in VS Code via MCP, the tools will be available:
- `wiki_read` — read any .md file
- `wiki_write` — write/update any file
- `wiki_list` — browse folder contents
- `wiki_search` — search by keyword
- `wiki_delete` — remove a file (goes to recycle bin)

## Step 6: Migrate Wiki Content

Once the SharePoint site is ready, you can push your local wiki to it:

```powershell
# Example: Push all wiki-steady-state files
Get-ChildItem -Recurse "wiki-steady-state" -Filter "*.md" | ForEach-Object {
    $relativePath = $_.FullName.Replace((Get-Location).Path + "\", "").Replace("\", "/")
    Write-Host "Uploading: $relativePath"
    # The MCP server handles this, or you can use Graph API directly:
    # Invoke-RestMethod -Method PUT -Uri "https://graph.microsoft.com/v1.0/drives/$driveId/root:/$relativePath:/content" ...
}
```

Or simply use the `wiki_write` tool through the agent to push files one at a time.

## Alternative: App Registration (for production/shared use)

If you want a dedicated service identity instead of user-delegated:

1. Go to https://portal.azure.com → Microsoft Entra ID → App registrations
2. Create: `SE-Brain-Graph-Wiki`
3. API Permissions → Add → Microsoft Graph → Application:
   - `Files.ReadWrite.All`
   - `Sites.ReadWrite.All`
4. Grant admin consent
5. Create a client secret
6. Set environment variables:
   ```
   AZURE_TENANT_ID=your-tenant-id
   AZURE_CLIENT_ID=app-client-id
   AZURE_CLIENT_SECRET=app-secret
   ```

This lets the MCP run as a service without requiring `az login`.

## How Skills Use This

Once configured, the data retrieval skills swap their backing store:

| Skill | Before (local) | After (SharePoint) |
|-------|---------------|-------------------|
| `se_brain_account-data` | `read_file("wiki-steady-state/entities/active-accounts.md")` | `wiki_read("wiki-steady-state/entities/active-accounts.md")` |
| `se_brain_pipeline-data` | `read_file("wiki-steady-state/entities/active-pipeline.md")` | `wiki_read("wiki-steady-state/entities/active-pipeline.md")` |
| `se_brain_compete-intel` | `read_file("wiki-steady-state/concepts/compete-landscape.md")` | `wiki_read("wiki-steady-state/concepts/compete-landscape.md")` |
| `se_brain_broadcast-insight` | `create_file("broadcasts/...")` | `wiki_write("broadcasts/...")` |

The folder structure in SharePoint mirrors the local repo structure, so paths stay the same.

## Troubleshooting

### "AADSTS65001: The user or administrator has not consented"
→ Run `az login` again, or ask your admin to grant Graph API permissions.

### "Failed to resolve site: 404"
→ Check `GRAPH_SITE_PATH` matches your SharePoint site URL exactly.

### "Drive 'X' not found"
→ Check `GRAPH_LIBRARY_NAME` matches the document library name in your SharePoint site.

### "403 Forbidden"  
→ Your account may need Sites.ReadWrite.All. Check in Azure Portal → Enterprise Apps → your app → Permissions.
