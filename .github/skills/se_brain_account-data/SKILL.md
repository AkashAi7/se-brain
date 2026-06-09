---
name: se_brain_account-data
description: "Retrieve account profile data for a given customer. Returns account details, Azure footprint, competitive landscape, team, signals, and strategic priorities. Use when any skill or agent needs account context — deck building, meeting prep, deal strategy, or territory review. This is the single source of truth for account data."
---

# Account Data Retrieval

The abstraction layer for account information. Primary source is **SharePoint** (`mock-data/accounts.json` on the SE wiki document library). Can be swapped to CRM API, Dynamics, or any other source without changing downstream consumers.

## When to Invoke This Skill

- Deck builder needs account profile (services, team, signals)
- Customer intel needs account context
- Deal strategy needs competitive footprint
- Any skill needing: account name, industry, revenue, HQ, Azure spend, existing services, competitive presence, signals, strategic priorities, or account team

## Input

The invoking agent provides:
- **Account name** (required) — e.g., "Tata Steel", "Mahindra"
- **Fields needed** (optional) — e.g., "services only", "team only", "everything"

## Retrieval Protocol

### Step 1: Read account data from SharePoint
Use the `wiki_read` MCP tool to pull live data from the SharePoint Document Library:
```
wiki_read("mock-data/accounts.json")
```

### Step 2: Filter to the requested account

Parse the JSON and extract ONLY the relevant account's data.

### Data Layers
SharePoint is the authoritative source for shared account data — pull it via `wiki_read`. Do NOT read the stale local mirror `mock-data/`. If `wiki_read` is unavailable, inform the user that the SharePoint connection is required — do not fall back to the mirror.

**Optional private layer:** after grounding in SharePoint, you may also scan the user's `KB-Local/` folder for personal notes on the account. **`KB-Local/` is gitignored, so `file_search` cannot see it** — discover notes with `grep_search` (set `includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`) and read them with `read_file`. Fold them in only if they add value, label them "From your local notes (KB-Local)", and let SharePoint win any conflict. Never read local files outside `KB-Local/`.

## Output Schema

Return a structured block with these sections (omit empty sections):

```
### Account: [Name]
- Industry: ...
- Segment: ...
- Employees: ...
- Revenue: ...
- HQ: ...

### Azure Footprint
- Monthly spend: $X
- M365: deployed/not
- Entra: deployed/not
- Services: [list]

### Competitive Presence
- [Vendor]: [services]

### Recent Signals
- [date] [type]: [detail]

### Strategic Priorities
- [priority 1]
- [priority 2]

### Account Team
- AE: ...
- SE: ...
- CSAM: ...
- GBB: ...
```

## Future Backing Stores

This skill is designed to be re-pointed. Possible future sources:
- Dynamics 365 CRM API
- WorkIQ (Microsoft Graph for account signals)
- Account health dashboards
- Territory planning tools

When the backing store changes, only THIS skill's retrieval protocol changes. All consumers (deck-builder, customer-intel, deal-strategy) remain untouched.
