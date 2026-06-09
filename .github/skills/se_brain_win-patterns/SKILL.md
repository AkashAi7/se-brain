---
name: se-win-patterns
description: 'Surface win stories, deal patterns, reference customers, and reusable playbooks from past successes to give SEs confidence and a headstart on complex opportunities. Use when the user says "how have we won deals like this", "find me a reference customer", "win patterns for X", "who has done this before", "give me confidence on this deal", "reference stories for X", "what worked in similar deals", "any wins against [competitor]", "deal confidence kit", or any request for historical win context and reusable patterns.'
---

# SE Win Patterns — Reference Intelligence & Deal Confidence

Surface **win stories, reference customers, proven patterns, and reusable playbooks** from past deals to give an SE confidence and a headstart on complex opportunities. This is the "someone has done this before" skill — it turns the collective field experience into an unfair advantage for every deal.

## Why This Skill Exists

Every SE faces the same moment: a complex new deal, unfamiliar competitor, or a customer objection they haven't handled before. The answer usually exists somewhere — in a win wire email, a Teams thread, a shared deck, or a colleague's experience. This skill finds it.

**The promise**: No SE should ever walk into a deal thinking "I'm the first person to face this." You're not. This skill proves it and gives you the playbook.

## When to Use This Skill

| User Says | This Skill Does |
|-----------|-----------------|
| "how have we won against Databricks" | Mines win stories where Microsoft displaced Databricks |
| "find me a reference customer for Azure AI in banking" | Locates relevant customer success stories |
| "give me confidence on the Zomato deal" | Builds a deal confidence kit with similar wins and patterns |
| "what worked in similar deals" | Pattern-matches current deal to past successes |
| "any displacement wins for Fabric" | Finds migration/displacement success stories |
| "who has done a POC like this before" | Surfaces SEs who've executed similar proof-of-concepts |
| "reference stories for real-time analytics" | Finds customer stories matching the scenario |
| "win patterns for GCP displacement" | Extracts the recurring plays that win against GCP |
| "deal confidence kit for [opportunity]" | Full confidence package tied to a specific deal |

## The 3 Core Functions

### 1. Win Pattern Mining
Search M365 for win wire emails, deal win announcements, and success stories. Extract the recurring patterns — what plays worked, what proof points closed the deal, what objections were overcome.

### 2. Reference Customer Matching
Given a deal scenario (industry + solution area + competitor + scale), find the most relevant customer references that the SE can cite in meetings, proposals, or executive briefings.

### 3. Deal Confidence Kit
For a specific active opportunity, assemble a complete confidence package: similar wins, reference customers, proven objection responses, competitor displacement stories, and reusable technical architectures.

## Execution Steps

### Step 1: Understand the Context

Determine what the SE needs by extracting:
- **Industry**: Banking, E-commerce, Manufacturing, etc.
- **Solution area**: AI, Data, Security, Infrastructure, Modern Work
- **Competitor** (if any): AWS, GCP, Databricks, Snowflake, CrowdStrike, etc.
- **Scenario**: Greenfield, migration, displacement, expansion, consolidation
- **Scale indicators**: User count, data volume, transaction rate, geography
- **Active deal** (if specified): Look up in `mock-data/opportunities.json`

### Step 2: Query WorkIQ for Win Intelligence

Use `mcp_workiq_ask_work_iq` with multiple targeted queries:

#### For Win Stories:
```
Query 1: "What deal wins, win wires, or success announcements have been shared about winning [SOLUTION AREA] deals against [COMPETITOR] in [INDUSTRY]? Include any win stories from emails or Teams messages."

Query 2: "What customer success stories or reference customers do we have for [SCENARIO] in [INDUSTRY]? Look for shared presentations, case studies, or win announcements."
```

#### For Displacement Patterns:
```
Query 1: "How have we successfully displaced [COMPETITOR] in past deals? What were the key technical proof points, commercial angles, or customer objections we overcame? Look for win wire emails and deal retrospectives."

Query 2: "What migration or displacement playbooks have been shared for moving customers from [COMPETITOR] to [MICROSOFT SOLUTION]? Check Teams channels, emails, and shared documents."
```

#### For Reference Customers:
```
Query 1: "What customer references, success stories, or case studies are available for [SOLUTION] in [INDUSTRY]? Include any customer presentations, demo recordings, or shared reference decks."

Query 2: "Which customers have publicly spoken about their [SOLUTION] deployment? Any joint announcements, blog posts, or event presentations shared internally?"
```

#### For Reusable Assets:
```
Query 1: "What demo environments, architecture diagrams, POC templates, or reusable technical assets have been shared by other SEs for [SCENARIO]? Check Teams channels and shared documents."

Query 2: "Has anyone shared a similar workshop or POC plan for [SCENARIO]? Looking for templates, agendas, or success criteria documents."
```

### Step 3: Cross-Reference with Deal Data

If the user has a specific active deal (shared reads via the `wiki_read()` MCP tool — never the stale local mirrors):
1. `wiki_read("mock-data/opportunities.json")` for deal details
2. `wiki_read("mock-data/accounts.json")` for account context
3. Match the deal's characteristics (industry, competitor, solution area, scale) to the win patterns found

You may also scan the user's `KB-Local/` folder for relevant private notes on the deal. **`KB-Local/` is gitignored, so `file_search` cannot see it** — discover notes with `grep_search` (set `includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`) and read them with `read_file`; fold them in only if they add value, labeled "From your local notes (KB-Local)".
4. Identify which patterns are most relevant to THIS specific deal

### Step 4: Extract Actionable Patterns

From the raw win intelligence, synthesize into actionable patterns:

- **What plays worked**: The specific technical demos, commercial angles, or executive narratives that closed similar deals
- **What proof points resonated**: Benchmarks, metrics, or capabilities that convinced similar customers
- **What objections were overcome**: The exact pushback and how it was addressed
- **What timelines looked like**: How long similar deals took from qualification to close
- **Who can help**: SEs or specialists who've done this before and can advise

### Step 5: Produce the Output

---

## Output Formats

### Win Pattern Summary

```markdown
# Win Patterns: [Solution] vs [Competitor] in [Industry]

## Pattern Overview
**Win rate signal**: [How common are wins in this scenario — based on available data]
**Typical deal cycle**: [Duration from qualification to close]
**Key differentiator**: [The #1 thing that consistently wins these deals]

---

## Proven Plays That Work

### Play 1: [Name — e.g., "Total Cost Ownership Reframe"]
**What it is**: [1-2 sentences describing the play]
**When to use it**: [Which stage, which stakeholder, which objection triggers it]
**Evidence**: [Which win story proves this works]
**Example framing**: "[Exact language or positioning angle to use]"

### Play 2: [Name]
...

### Play 3: [Name]
...

---

## Reference Customers You Can Cite

| Customer | Industry | Scenario | Scale | Key Metric | Source |
|----------|----------|----------|-------|------------|--------|
| [Name] | [Industry] | [What they did] | [Users/data/etc.] | [Outcome metric] | [Link to story] |
| ... | ... | ... | ... | ... | ... |

---

## Objections You'll Face (And How to Handle Them)

| They'll Say | Why They Say It | You Say | Proof |
|-------------|-----------------|---------|-------|
| "[Objection]" | [Underlying concern] | "[Response]" | [Reference or data] |
| ... | ... | ... | ... |

---

## Reusable Assets

| Asset | Type | Owner/Source | Link | Notes |
|-------|------|-------------|------|-------|
| [Name] | Architecture diagram | [SE who shared] | [URL] | [When to use it] |
| [Name] | Demo script | ... | ... | ... |
| [Name] | POC template | ... | ... | ... |

---

## Who Has Done This Before

| Person | Role | What They Did | Contact |
|--------|------|---------------|---------|
| [Name] | [SE/GBB/Specialist] | [Brief description of their relevant experience] | [How to reach them] |
```

### Deal Confidence Kit (For a Specific Opportunity)

```markdown
# 💪 Deal Confidence Kit: [Account] — [Opportunity Title]

## Your Situation
**Deal**: [Title] | **Value**: $[X] | **Stage**: [Stage] | **Competitor**: [Name]
**Key blocker**: [The #1 thing you're worried about]

---

## Confidence Builders

### ✅ Similar Deals We've Won
[List 2-4 similar deals with brief details on how they were won]

### ✅ Your Strongest Proof Points
[Specific metrics, benchmarks, or capabilities that matter for THIS deal]

### ✅ References You Can Name-Drop
[Customers in similar industries/scenarios that have deployed successfully]

### ✅ The Play That Works Here
[Based on pattern matching, the specific approach most likely to win this deal]

---

## Risk Mitigators

### ⚠️ Objection: "[The thing you're worried the customer will say]"
**Pattern response**: [How others have handled this successfully]
**Proof**: [Evidence from similar wins]

### ⚠️ Competitor Strength: "[What the competitor does well here]"
**Counter**: [The reframe or alternative narrative]
**Proof**: [Where we've won despite this]

---

## Your Confidence Score: [HIGH / MEDIUM / NEEDS WORK]

**Why**: [1-2 sentences explaining the confidence assessment based on pattern match strength]

**To increase confidence**:
- [ ] [Specific action — e.g., "Get a reference call set up with [similar customer]"]
- [ ] [Specific action — e.g., "Run a benchmark showing [specific capability]"]
- [ ] [Specific action — e.g., "Connect with [SE name] who won a similar deal at [account]"]
```

---

## Integration with Other Skills

This skill connects the dots across the SE toolkit:

- **`se-customer-intel`** → When preparing a brief, pull win patterns to add a "Similar Wins" section
- **`se-deal-strategy`** → When a deal is stuck, win patterns show what unstuck similar deals
- **`se-seismic-intel`** → Win patterns complement battlecards — battlecards say what to say, win patterns prove it works
- **`se-week-ahead`** → When a tough meeting is on the calendar, offer a confidence kit
- **`se-deep-dive`** → When a technical gap is identified, win patterns show what technical proof points mattered

## Suggested Follow-Ups

After delivering win patterns, offer:

1. "Want me to build a full compete strategy for this meeting?" → triggers `se-seismic-intel` + `se-customer-intel`
2. "Should I prep a deep dive on [technical area] that won similar deals?" → triggers `se-deep-dive`
3. "Want me to find the actual shared assets (decks, demos) from these wins?" → deeper WorkIQ query

## Rules

- **Always use WorkIQ** — the value is REAL win stories from your field, not generic case studies.
- **Pattern > Anecdote** — when multiple wins share a pattern, highlight the pattern. One win is an anecdote; three wins is a strategy.
- **Be honest about confidence** — if the pattern match is weak or data is thin, say so. Don't fabricate confidence.
- **Name sources** — win wires, Teams threads, and shared decks should be cited with links when available.
- **Connect to the active deal** — abstract patterns are less useful than "here's exactly how this applies to YOUR deal with [Customer]."
- **Surface people, not just content** — knowing WHO has done this before is as valuable as knowing what they did. SEs learn best from peers.
- **Compound over time** — when a new win wire comes through, suggest filing the pattern into `wiki-steady-state/` for future use.
