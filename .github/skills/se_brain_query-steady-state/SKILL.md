---
name: se_brain_query-steady-state
description: 'The ONLY retrieval gateway for the steady-state knowledge base. Use for ALL data lookups: compete intel, deal context, account data, pipeline info, engagement patterns, pitch frameworks, and learning paths. Searches wiki-steady-state/index.md, reads relevant pages, pulls from mock-data/ for account and opportunity context, and synthesizes grounded answers. Replaces direct file reads entirely — the agent must NEVER read wiki-steady-state/ or mock-data/ directly.'
---

# Query Steady-State KB

The single retrieval skill for all steady-state knowledge. Every lookup — compete, deals, accounts, patterns, pitches, learning — goes through this skill.

**Grounding (two-tier):** All *shared* data reads MUST use `wiki_read()` targeting `microsoftapc.sharepoint.com/teams/se-brain-wiki`. The agent MUST NOT read the stale local mirrors `mock-data/`, `wiki-steady-state/`, or `raw-steady-state/`. If the MCP tool is unavailable, inform the user — do not silently fall back to those mirrors.

**Optional private layer:** after grounding in SharePoint, you may also scan the user's `KB-Local/` folder for relevant personal notes. **`KB-Local/` is gitignored, so `file_search` cannot see it** — discover notes with `grep_search` (set `includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`) and read them with `read_file`. Fold them in only if they add value, label them "From your local notes (KB-Local)", and let SharePoint win any conflict. Never read local files outside `KB-Local/`.

## Relationship to Focused Retrieval Skills

For common data retrieval patterns, focused skills exist that wrap this gateway:

| Focused Skill | Use Case | Calls This Skill Internally |
|--------------|----------|----------------------------|
| `se_brain_account-data` | Account profile, footprint, team, signals | Yes — reads mock-data/accounts.json from SharePoint |
| `se_brain_pipeline-data` | Opportunities, stages, values, contacts | Yes — reads mock-data/opportunities.json from SharePoint |
| `se_brain_compete-intel` | Positioning, radar scores, talk tracks | Yes — reads concepts/compete-landscape.md |
| `se_brain_account-research` | Fresh web intelligence | No — uses fetch_webpage directly |

**When to use THIS skill directly:** For cross-domain questions, learning paths, engagement patterns, pitch frameworks, or any query that doesn't cleanly fit one focused skill.

## When to Use This Skill

- **ALWAYS** — whenever the agent needs any data from the steady-state knowledge base
- The agent instructions forbid direct `read_file`, `list_dir`, `file_search`, or `grep_search` on `wiki-steady-state/`, `raw-steady-state/`, or `mock-data/`
- This skill is the ONLY authorized path to that data

## What This Skill Covers

| Data Need | Source |
|-----------|--------|
| Compete intelligence (AWS, GCP, Anthropic) | `wiki-steady-state/concepts/compete-landscape.md` |
| Deal execution & MCEM motion | `wiki-steady-state/concepts/deal-execution-and-mcem.md` |
| Customer engagement patterns | `wiki-steady-state/concepts/customer-engagement-patterns.md` |
| Pitch & messaging frameworks | `wiki-steady-state/concepts/pitch-and-messaging.md` |
| Workshop & POC delivery | `wiki-steady-state/concepts/workshop-and-poc-delivery.md` |
| Account strategy & expansion | `wiki-steady-state/concepts/account-strategy-and-expansion.md` |
| Continuous learning paths | `wiki-steady-state/concepts/continuous-learning.md` |
| Account context (names, teams, segments) | `wiki-steady-state/entities/active-accounts.md` |
| Pipeline & opportunities | `wiki-steady-state/entities/active-pipeline.md` |
| Skills & growth matrix | `mock-data/skills-and-growth.json` |
| Filed analyses | `wiki-steady-state/analyses/` |
| Competitor profiles | `wiki-steady-state/entities/` |
| Comparisons | `wiki-steady-state/comparisons/` |

## Step-by-Step Retrieval Protocol

### Step 1: Classify the Data Need

Before reading anything, determine what type of data is needed:

| Need Type | Primary Source (via `wiki_read`) | Secondary (via `wiki_read`) |
|-----------|---------------|----------|
| Compete positioning | `wiki-steady-state/concepts/compete-landscape.md` | `raw-steady-state/azure-vs-aws-positioning-guide.md` |
| Account-specific context | `mock-data/accounts.json` | `wiki-steady-state/entities/active-accounts.md` |
| Deal/pipeline data | `mock-data/opportunities.json` | `wiki-steady-state/entities/active-pipeline.md` |
| Engagement framework | `wiki-steady-state/concepts/customer-engagement-patterns.md` | None |
| Pitch narrative | `wiki-steady-state/concepts/pitch-and-messaging.md` | None |
| Workshop/POC patterns | `wiki-steady-state/concepts/workshop-and-poc-delivery.md` | `raw-steady-state/workshop-and-poc-delivery-patterns.md` |
| Deal methodology | `wiki-steady-state/concepts/deal-execution-and-mcem.md` | `raw-steady-state/mcem-deal-execution-framework.md` |
| Learning paths | `wiki-steady-state/concepts/continuous-learning.md` | None |
| Account strategy | `wiki-steady-state/concepts/account-strategy-and-expansion.md` | None |
| Skills matrix | `mock-data/skills-and-growth.json` | None |
| Previously answered questions | `wiki-steady-state/analyses/` | None |

**All reads use `wiki_read()` — NEVER `read_file()` on these paths. SharePoint is the sole source.**

### Step 2: Read the Index (Only If Unsure)

If the classification in Step 1 gives you a clear target, go directly to that file. Only read `wiki-steady-state/index.md` if:
- The question spans multiple domains
- You're unsure which page is most relevant
- You need to check if an analysis already exists for this question

### Step 3: Read the Target Page(s)

Read the minimum pages needed to answer. Priority order:

1. **Filed analyses** (`wiki-steady-state/analyses/`) — if this question was answered before, use that
2. **Concept pages** (`wiki-steady-state/concepts/`) — synthesized knowledge on the topic
3. **Entity pages** (`wiki-steady-state/entities/`) — competitor profiles, customer archetypes
4. **Mock data** (`mock-data/`) — account, pipeline, and skills data
5. **Raw sources** (`raw-steady-state/`) — only when wiki pages lack needed detail

### Step 4: Synthesize

Combine the retrieved data into the answer the parent skill or agent needs. Follow these rules:

- **Cite sources** — reference the wiki page that grounded each claim
- **Don't over-read** — if one page answers the question, don't read five
- **Flag gaps** — if the KB doesn't cover something, say so rather than inventing
- **Return structured data** — tables, lists, and labeled sections rather than prose dumps

### Step 5: Account and Pipeline Lookups

For account/deal-specific questions, read the JSON files from **SharePoint** and extract ONLY the relevant records:

**accounts.json** — Use when the question mentions a customer name, account context, or team members:
```
wiki_read("mock-data/accounts.json")
```
- Extract: account name, segment, team (AE, CSAM, SE), active workstreams, key contacts
- Return as a brief structured summary, not raw JSON

**opportunities.json** — Use when the question mentions a deal, pipeline, revenue, stage, or specific opportunity:
```
wiki_read("mock-data/opportunities.json")
```
- Extract: opportunity name, account, value, stage, days in stage, next steps, risk flags
- Return as a brief structured summary

**skills-and-growth.json** — Use when the question is about learning, certifications, skill gaps, or role transitions:
```
wiki_read("mock-data/skills-and-growth.json")
```
- Extract: current skills, target skills, gaps, recommended paths
- Return as a prioritized list

**No Local Fallback:** SharePoint is the single source of truth. Do NOT use `read_file` on local `mock-data/`, `wiki-steady-state/`, or `raw-steady-state/` directories. If `wiki_read` is unavailable, inform the user that the SharePoint connection is required.

## Anti-Patterns (NEVER Do These)

- ❌ Using `read_file` on `mock-data/`, `wiki-steady-state/`, or `raw-steady-state/`
- ❌ Using `grep_search` or `file_search` on data directories
- ❌ Reading `wiki-steady-state/` directory listing to "see what's there"
- ❌ Searching for `**/*.json` or `**/*.md` via file_search
- ❌ Reading ALL concept pages when only one is relevant
- ❌ Reading raw sources when the wiki concept page has the answer
- ❌ Returning raw JSON to the user — always summarize
- ❌ Reading index.md every time — only when classification is ambiguous
- ❌ Falling back to local files when SharePoint is unreachable — report the error instead

## Performance Rules

1. **Maximum 3 file reads per invocation** — if you need more, you're over-reading
2. **Go direct** — if you know the answer is in `compete-landscape.md`, read it. Don't read the index first.
3. **Cache within conversation** — if you already read a page in this conversation, don't re-read it
4. **Return only what's needed** — the parent skill/agent asked for specific data. Return THAT, not the whole page.
