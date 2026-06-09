---
name: se_brain_pipeline-data
description: "Retrieve pipeline and opportunity data for a given account or the full territory. Returns deal details, stages, values, blockers, contacts, and next steps. Use when any skill or agent needs pipeline context — deck building, deal strategy, pipeline reviews, or forecasting. Single source of truth for opportunity data."
---

# Pipeline Data Retrieval

The abstraction layer for pipeline and opportunity information. Primary source is **SharePoint** (`mock-data/opportunities.json` on the SE wiki document library). Can be swapped to CRM API without changing downstream consumers.

## When to Invoke This Skill

- Deck builder needs deal values, stages, and timelines for charts (funnel, gantt, waterfall)
- Deal strategy needs blockers and next steps
- Pipeline review needs territory-wide summary
- Any skill needing: opportunity title, stage, value, close date, competitor, blockers, contacts, or deal notes

## Input

The invoking agent provides:
- **Account name** (optional) — filter to one account. If omitted, return full territory.
- **Fields needed** (optional) — e.g., "summary only", "contacts only", "everything"

## Retrieval Protocol

### Step 1: Read opportunity data from SharePoint
Use the `wiki_read` MCP tool to pull live data from the SharePoint Document Library:
```
wiki_read("mock-data/opportunities.json")
```

### Step 2: Filter by account (if specified)

Parse the JSON and filter to the requested account, or return full territory if no account specified.

### Data Layers
SharePoint is the authoritative source for shared pipeline data — pull it via `wiki_read`. Do NOT read the stale local mirror `mock-data/`. If `wiki_read` is unavailable, inform the user that the SharePoint connection is required — do not fall back to the mirror.

**Optional private layer:** after grounding in SharePoint, you may also scan the user's `KB-Local/` folder for personal notes on the deal. **`KB-Local/` is gitignored, so `file_search` cannot see it** — discover notes with `grep_search` (set `includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`) and read them with `read_file`. Fold them in only if they add value, label them "From your local notes (KB-Local)", and let SharePoint win any conflict. Never read local files outside `KB-Local/`.

## Output Schema

Return structured data:

```
### Pipeline Summary
- Total value: $X.XM
- Deal count: N
- Stage distribution: [Qualify: N, Solution: N, Proof: N, ...]

### Opportunities

#### [Opportunity Title]
- Account: ...
- Stage: ...
- Value: $X
- Close date: YYYY-MM-DD
- Competitor: ...
- Technical win: [status]
- Blockers: [list]
- Key contacts: [name (role, sentiment)]
- Last engagement: [date — detail]
- Next step: [action]
```

## Data for Specific Chart Types

When the deck-builder requests pipeline data for charts, format accordingly:

### For Funnel Charts
Return stage names and deal counts descending:
```
categories: ["Total Leads", "Qualified", "Solution", "Proof", "Closed"]
values: [count_at_each_stage]
```

### For Gantt Charts
Return tasks with start week and duration:
```
tasks: [
  {name: "Deal Name — Phase", start: N, duration: N}
]
```
Calculate `start` as weeks from today. Calculate `duration` from stage velocity or (close_date - today) / remaining_stages.

### For Waterfall Charts
Return current ACR + each deal's projected monthly increment:
```
categories: ["Current ACR", "Deal 1", "Deal 2", ..., "Projected Total"]
values: [current, +increment1, +increment2, ..., +remainder]
```

## Future Backing Stores

- Dynamics 365 Opportunity API
- Partner Center deal registration
- Custom pipeline tracker
- WorkIQ (email signals about deal movement)
