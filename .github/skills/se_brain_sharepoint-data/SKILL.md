---
name: se_brain_sharepoint-data
description: "Unified data retrieval gateway from the SE Brain SharePoint wiki site. Provides wiki_read and wiki_list access to all knowledge: accounts, pipeline, compete intel, wiki concepts, analyses, broadcasts, and raw sources. This is the ONLY authorized path to SE Brain data — the agent must NEVER read local files directly. Use for any data lookup the steady-state or onboarding agent needs."
---

# SharePoint Data Retrieval

The gateway for all SE Brain knowledge retrieval. The universal knowledge lives on SharePoint at `microsoftapc.sharepoint.com/teams/se-brain-wiki` and is accessed through the `wiki_read` and `wiki_list` MCP tools. A separate, optional **private local layer** (`KB-Local/`) can augment answers with personal notes.

## Two-Tier Knowledge Model

| Tier | Source | Role | When used |
|------|--------|------|-----------|
| **1. Universal (authoritative)** | SharePoint wiki via `wiki_read` / `wiki_list` | Shared source of truth for all SEs | **Always** — every answer must be grounded here first |
| **2. Private (augmentation)** | Local `KB-Local/` folder via `file_search` / `read_file` | The user's personal notes, drafts, private deal context | **Optional** — checked after SharePoint, used only if it adds value |

**Order of operations for every data-backed answer:**
1. **Always query SharePoint first** (`wiki_read`) for the universal, authoritative content. This is mandatory and is the backbone of the answer.
2. **Then optionally scan `KB-Local/`** for private notes relevant to the question. `KB-Local/` is gitignored, so `file_search` cannot see it — use `grep_search` (with `includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`) to discover notes, then `read_file` to read them.
3. **Fold in local content only if it genuinely adds value.** If nothing in `KB-Local/` is relevant, skip it silently — never pad the answer with irrelevant local material.
4. **`KB-Local/` never substitutes for SharePoint.** It is additive only. If SharePoint is unreachable, do NOT build an answer from `KB-Local/` alone — tell the user the SharePoint connection is required and stop. A brief missing the shared account/pipeline/compete truth is misleading.

## Grounding Policy

**Universal knowledge = SharePoint only.** For any shared fact (accounts, pipeline, compete, wiki concepts):
- ✅ Use `wiki_read(path)` to retrieve any wiki/data file
- ✅ Use `wiki_list(folder)` to browse directory contents
- ✅ Use `wiki_search(query)` to find files by keyword
- ❌ NEVER use `read_file` on local mirrors of the shared wiki: `mock-data/`, `wiki-steady-state/`, `wiki/`, `raw/`, `raw-steady-state/`, or `broadcasts/` (these are stale copies)
- ❌ NEVER use `grep_search` or `file_search` on those mirror directories
- ❌ NEVER fall back to those local mirrors if SharePoint is unreachable — inform the user instead

**Private augmentation = `KB-Local/` only.** This is the single sanctioned local source:
- ✅ Discover notes with `grep_search` (`includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`), then read with `read_file` — `file_search` cannot see `KB-Local/` because it is gitignored
- ✅ Treat it as additive context, never as a replacement for SharePoint
- ✅ On a conflict over a shared fact, **SharePoint wins** — flag the discrepancy to the user
- ✅ **Label local-sourced content** distinctly in the answer (e.g. "From your local notes (KB-Local)…")
- ❌ NEVER build an answer from `KB-Local/` alone when SharePoint is down — it augments, never substitutes
- ❌ NEVER read local files outside `KB-Local/` for data

## SharePoint Site

- **Site:** microsoftapc.sharepoint.com/teams/se-brain-wiki
- **Library:** Documents
- **MCP Server:** se-graph-wiki (configured in .vscode/mcp.json)

## Directory Structure

```
Documents/
├── wiki/                          ← Onboarding KB
│   ├── index.md                   ← Master catalog
│   ├── log.md, overview.md
│   ├── analyses/                  ← Day 1 guide, 30-day plan, playbook
│   ├── concepts/                  ← Journey, tooling, platform, pod-map
│   ├── entities/                  ← Stakeholders
│   └── sources/                   ← Source summaries
│
├── wiki-steady-state/             ← Execution KB
│   ├── index.md                   ← Master catalog
│   ├── log.md, overview.md
│   ├── analyses/                  ← Pipeline health, Tata strategy
│   ├── comparisons/               ← Foundry vs Vertex, Fabric vs Databricks
│   ├── concepts/                  ← Compete, MCEM, pitch, workshop, learning
│   ├── entities/                  ← Accounts, pipeline, Google Cloud, AWS
│   └── sources/                   ← Source summaries
│
├── mock-data/                     ← Live JSON data
│   ├── accounts.json              ← 4 accounts with full profiles
│   ├── opportunities.json         ← 7 deals, $12.65M pipeline
│   └── skills-and-growth.json     ← Certifications, skill gaps
│
├── raw-steady-state/              ← Immutable source documents
│   ├── azure-vs-aws-positioning-guide.md
│   ├── mcem-deal-execution-framework.md
│   └── workshop-and-poc-delivery-patterns.md
│
├── raw/                           ← Onboarding source documents
│   ├── se-day-1-complete-starter-guide.md
│   ├── se-onboarding-flow-reference.md
│   └── ...
│
└── broadcasts/                    ← Shared SE insights
    ├── index.md
    └── 2026-06-09-voice-live-conversion-pattern.md
```

## How to Use This Skill

### For Account Data
```
wiki_read("mock-data/accounts.json")
```
Parse the JSON, filter to the requested account name, return structured profile.

### For Pipeline / Opportunity Data
```
wiki_read("mock-data/opportunities.json")
```
Parse the JSON, filter by account or return full territory, return structured summary.

### For Compete Intelligence
```
wiki_read("wiki-steady-state/concepts/compete-landscape.md")
```
For specific competitor deep-dives:
```
wiki_read("wiki-steady-state/entities/google-cloud.md")
wiki_read("wiki-steady-state/entities/aws.md")
```
For head-to-head comparisons:
```
wiki_read("wiki-steady-state/comparisons/foundry-vs-vertex-ai.md")
wiki_read("wiki-steady-state/comparisons/fabric-vs-databricks-snowflake.md")
```

### For Deal Methodology
```
wiki_read("wiki-steady-state/concepts/deal-execution-and-mcem.md")
```

### For Customer Engagement Patterns
```
wiki_read("wiki-steady-state/concepts/customer-engagement-patterns.md")
```

### For Pitch & Messaging
```
wiki_read("wiki-steady-state/concepts/pitch-and-messaging.md")
```

### For Workshop / POC Delivery
```
wiki_read("wiki-steady-state/concepts/workshop-and-poc-delivery.md")
```

### For Account Strategy
```
wiki_read("wiki-steady-state/concepts/account-strategy-and-expansion.md")
```

### For Learning Paths
```
wiki_read("wiki-steady-state/concepts/continuous-learning.md")
wiki_read("mock-data/skills-and-growth.json")
```

### For Onboarding Content
```
wiki_read("wiki/index.md")                              ← Find the right page
wiki_read("wiki/analyses/day-1-onboarding-guide.md")    ← Day 1
wiki_read("wiki/analyses/first-30-days-ramp-plan.md")   ← Month 1
wiki_read("wiki/concepts/se-onboarding-journey.md")     ← Full journey
wiki_read("wiki/entities/onboarding-stakeholders.md")   ← People
```

### For Previously Filed Analyses
```
wiki_list("wiki-steady-state/analyses")                 ← See what's been answered
wiki_read("wiki-steady-state/analyses/<specific>.md")   ← Read specific analysis
```

### For Broadcasts
```
wiki_read("broadcasts/index.md")                        ← Catalog of shared insights
wiki_read("broadcasts/<specific>.md")                   ← Read specific broadcast
```

### For Browsing / Discovery
```
wiki_list("wiki-steady-state/concepts")                 ← List all concept pages
wiki_list("wiki-steady-state/entities")                 ← List all entity pages
wiki_list("mock-data")                                  ← List all data files
```

## Retrieval Protocol

### Step 1: Classify the Need

| Need | Primary Path |
|------|-------------|
| Account profile, team, signals | `mock-data/accounts.json` |
| Pipeline, deals, stages, values | `mock-data/opportunities.json` |
| Skills, certifications, growth | `mock-data/skills-and-growth.json` |
| Compete positioning | `wiki-steady-state/concepts/compete-landscape.md` |
| Specific competitor | `wiki-steady-state/entities/<competitor>.md` |
| Head-to-head comparison | `wiki-steady-state/comparisons/<x-vs-y>.md` |
| Deal methodology (MCEM) | `wiki-steady-state/concepts/deal-execution-and-mcem.md` |
| Customer engagement | `wiki-steady-state/concepts/customer-engagement-patterns.md` |
| Pitch frameworks | `wiki-steady-state/concepts/pitch-and-messaging.md` |
| Workshop/POC patterns | `wiki-steady-state/concepts/workshop-and-poc-delivery.md` |
| Learning paths | `wiki-steady-state/concepts/continuous-learning.md` |
| Account strategy | `wiki-steady-state/concepts/account-strategy-and-expansion.md` |
| Onboarding stage guide | `wiki/analyses/` (pick by stage) |
| Onboarding tools | `wiki/concepts/onboarding-tooling-and-resources.md` |
| Stakeholders | `wiki/entities/onboarding-stakeholders.md` |

### Step 2: Read via wiki_read

Call `wiki_read(path)` with the path from Step 1. Maximum 3 reads per question.

### Step 2b: Optionally Augment from KB-Local (Private Layer)

After retrieving the universal content, optionally check the private local layer:
- Use `grep_search` (`includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`) to find personal notes relevant to the question, then `read_file` to read them. `file_search` cannot see `KB-Local/` (it is gitignored).
- Fold in only what adds value. If nothing is relevant, skip silently.
- Never read local files outside `KB-Local/`.

### Step 3: Parse and Filter

- **Parse JSON inline from the `wiki_read` result.** The tool returns the file contents directly in context — read and filter the records yourself.
- **Do NOT** write the tool output to a temp file and re-parse it with an external `python`/`Get-Content` command. That round-trip is brittle (it triggers `JSONDecodeError: Extra data` when the tool-output wrapper isn't pure JSON) and is unnecessary.
- For markdown files: read the synthesized content directly.

### Step 4: Return Structured Data

Return the data as structured markdown (tables, lists, labeled sections). Never return raw JSON to the user.

## Citing Sources (Required)

Every answer grounded in this data MUST cite the central SharePoint wiki pages it used. This makes answers traceable back to the single source of truth.

**Citation URL pattern** — convert any wiki path to a clickable SharePoint link:

```
https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/<path>
```

Replace spaces with `%20`. Examples:
- `wiki/analyses/day-1-onboarding-guide.md` → `https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/wiki/analyses/day-1-onboarding-guide.md`
- `wiki-steady-state/concepts/compete-landscape.md` → `https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/wiki-steady-state/concepts/compete-landscape.md`

**How to present citations:**
- End the answer with a short **Sources** section listing the wiki pages used, as markdown links with the page title as link text.
- Example:
  ```markdown
  **Sources** (SE Brain wiki):
  - [Day 1 Onboarding Guide](https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/wiki/analyses/day-1-onboarding-guide.md)
  - [Onboarding Tooling & Resources](https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/wiki/concepts/onboarding-tooling-and-resources.md)
  ```
- For data files (`mock-data/*.json`), cite them too: `[Account Data](…/mock-data/accounts.json)`.
- Only cite pages you actually read in this turn. Never invent a page or path you didn't retrieve.
- **Private notes:** if you used content from `KB-Local/`, attribute it inline as "From your local notes (KB-Local)" rather than as a SharePoint link — it's local-only and has no shared URL.

## Writing Data Back

When the agent needs to update the wiki (file an analysis, push a broadcast, update data):

```
wiki_write("wiki-steady-state/analyses/<slug>.md", content)
wiki_write("broadcasts/<date>-<slug>.md", content)
wiki_write("mock-data/accounts.json", updated_json)
```

## Error Handling

If `wiki_read` or `wiki_list` returns an error:
1. Check the path is correct (use `wiki_list` to verify folder contents)
2. If 404: the file doesn't exist — inform the user
3. If auth error: tell the user "SharePoint connection required — run `az login` to refresh credentials"
4. NEVER fall back to local file reads

## Performance Rules

1. **Maximum 3 reads per invocation** — if you need more, you're over-reading
2. **Go direct** — if you know the path, read it. Don't browse first.
3. **Cache within conversation** — if you already retrieved data in this conversation, don't re-read
4. **Return only what's asked for** — filter and summarize, don't dump entire files
