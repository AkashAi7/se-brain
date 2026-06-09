---
name: se-deal-strategy
description: 'Provide deal strategy and unblock recommendations for stuck or active opportunities. Use when the user says "this deal is stuck", "how do I move this forward", "deal strategy for X", "help me with this opportunity", "pipeline review", or asks about moving an opportunity through stages. Reads from opportunity and account data to give specific, grounded recommendations.'
---

# Deal Strategy — Move Deals Forward

Help SEs unstick deals, accelerate pipeline, and make smart priority decisions. This skill turns pipeline data into strategic action — not generic advice, but specific recommendations grounded in the actual deal context.

## When to Use This Skill

- User mentions a stuck deal or stalled opportunity
- User asks for help moving a deal forward
- User requests pipeline review or prioritization
- User asks about a specific opportunity by name or account
- User says "what should I focus on this week" (deal-context version)
- **User asks "help me compete with X at Y"** — this is a compete-strategy request that MUST be grounded in the specific account context, not generic compete advice

## Data Sources

**Grounding (two-tier):** All *shared* reads MUST use the `wiki_read()` MCP tool against `microsoftapc.sharepoint.com/teams/se-brain-wiki`. NEVER read the stale local mirrors (`mock-data/`, `wiki/`, `wiki-steady-state/`, `raw/`, `raw-steady-state/`, `broadcasts/`). If `wiki_read` is unavailable, tell the user the SharePoint connection is required — do not fall back to those mirrors.

**Always also check the private layer.** After grounding in SharePoint, scan the user's `KB-Local/` folder for personal notes relevant to this deal. **`KB-Local/` is gitignored, so `file_search` cannot see it** — discover notes with `grep_search` (set `includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`) and read them with `read_file`. Fold them in only if they add value, label them "From your local notes (KB-Local)", and let SharePoint win any conflict on shared facts. Never read local files outside `KB-Local/`.

- `wiki_read("mock-data/opportunities.json")` — deals with stages, blockers, competitors, contacts, history
- `wiki_read("mock-data/accounts.json")` — account context, signals, competitive footprint
- `wiki_read("wiki-steady-state/concepts/deal-execution-and-mcem.md")` — MCEM framework and SE activities by stage
- `wiki_read("wiki-steady-state/concepts/compete-landscape.md")` — competitive positioning frameworks and battleground tables
- `wiki_read("raw-steady-state/azure-vs-aws-positioning-guide.md")` — detailed AWS compete guide (use as template for other competitors)

## Execution Steps

### Step 1: Identify the Opportunity

Match the user's request to an opportunity. If they ask about pipeline broadly, analyze all opportunities.

### Step 2: Diagnose the Situation

For each relevant opportunity, analyze:
- **Stage health**: Is it progressing normally or stalling? (use `days_in_stage` vs. typical benchmarks)
- **Blocker analysis**: What's actually preventing forward motion? Is it technical, political, competitive, or commercial?
- **Competitive position**: Who else is in the deal? What's their strength? Where are we differentiated?
- **Stakeholder alignment**: Who's a champion? Who's skeptical? Who's missing from the conversation?
- **Momentum signals**: Is there energy (recent engagement, signals) or drift (aging, no engagement)?

### Step 3: Generate Strategy

#### For a Single Deal — Unblock Strategy

```markdown
## Deal Strategy: [Opportunity Title]
**Account**: [name] | **Stage**: [X] | **Value**: [$X] | **Close date**: [date]
**Days in stage**: [N] | **Health**: [on-track / at-risk / stalled]

### Diagnosis
[2-3 sentences: what's really happening here — the underlying dynamic, not just the surface blocker]

### The Blocker
**Primary**: [the #1 thing holding this back]
**Secondary**: [other friction points]
**Root cause**: [why this blocker exists — technical, political, risk aversion, competitive momentum]

### Recommended Plays (in priority order)

#### Play 1: [Name] — [Expected impact: high/medium]
- **What**: [specific action — not "build relationship" but "schedule a 30-min with David Park to address interpretability concerns directly"]
- **Why**: [connects to the blocker diagnosis]
- **Who to involve**: [GBB, MTC, executive sponsor, partner — be specific]
- **Timeline**: [this week / next 2 weeks / before close date]

#### Play 2: [Name]
[Same structure]

#### Play 3: [Name]
[Same structure]

### Competitive Counter
- **Competitor strength in this deal**: [what they're winning on]
- **Your angle**: [specific differentiation for THIS customer's context]
- **Proof point needed**: [what evidence would tip the balance]

### Stakeholder Play
| Contact | Current State | Action Needed |
|---------|--------------|---------------|
| [name] | Champion | Arm with internal business case material |
| [name] | Skeptical | Direct technical engagement to address concerns |
| [name] | Missing | Need to get introduced — ask champion |

### Risk Assessment
- **Win probability**: [%] — [reasoning]
- **Biggest risk**: [what could kill this deal]
- **De-risk action**: [the one thing that most reduces the risk]

### Next 7 Days
1. [Immediate action — do this first]
2. [Follow-up action]
3. [Prep action for upcoming engagement]
```

#### For Pipeline Review — Portfolio View

```markdown
## Pipeline Review: [Date]
**Total pipeline**: [$X] across [N] deals
**Forecast confidence**: [high/medium/low] — [why]

### Priority Stack (Where to spend your time)

| Priority | Deal | Why Now | Action This Week |
|----------|------|---------|-----------------|
| 🔴 1 | [deal] | [urgent reason] | [specific action] |
| 🟡 2 | [deal] | [reason] | [action] |
| 🟢 3 | [deal] | [reason] | [action] |

### Pipeline Health Check
- **Stage distribution**: [is it balanced or top/bottom heavy?]
- **Aging deals**: [which are stalling — days in stage vs. benchmark]
- **Coverage gap**: [e.g., "nothing in Close — you'll have a revenue gap in 4 weeks"]
- **Competitive pressure**: [which deals have active competitors]

### Recommendation
[1-2 sentences: the strategic insight about where to invest time this week]
```

#### For "Help Me Compete with X at Y" — Account-Specific Compete Plan

When the user asks "help me compete with [Competitor] at [Account]", generate a PRESCRIPTIVE plan, not a generic compete summary. This is the most important distinction — the plan must be tailored to THIS account's specific context, tech stack, decision makers, and deal dynamics.

```markdown
## Compete Plan: [Competitor] at [Account]
**Account**: [name] | **Active Deal(s)**: [title(s)] | **Total Value**: [$X]
**Competitor's Current Footprint**: [what they already own in this account — from accounts.json]
**Your Footprint**: [what Microsoft already has — from accounts.json]

### The Competitive Dynamic
[3-4 sentences explaining the REAL situation — not "Google is strong in data" but "Google owns the BigQuery data warehouse and Vertex AI for 3 ML models at Tata Steel. Their engineers are GCP-certified and comfortable. Your angle is the AI layer (Azure AI Foundry + OpenAI models) which is already winning hearts, and the unification play (3-IQ) which Google can't match."]

### Where We Win (In THIS Account)
| Battleground | Our Strength | Their Weakness | Evidence/Proof Point |
|-------------|-------------|----------------|---------------------|
| [specific capability] | [what we do better HERE] | [where they fall short HERE] | [what to show/reference] |

### Where They're Entrenched (Don't Fight Here... Yet)
| Their Stronghold | Why | Our Play (Long-Term) |
|-----------------|-----|---------------------|
| [what they own] | [why it's sticky] | [how to displace over time — NOT a frontal assault] |

### Your 4-Week SE Compete Plan
**Week 1**: [specific actions — demo X to Y person, build POC showing Z]
**Week 2**: [expand — bring GBB for architecture session, run hands-on lab]
**Week 3**: [prove — deliver bake-off results, reference call with similar customer who displaced competitor]
**Week 4**: [close — present unified architecture vision, help champion build internal business case]

### Narrative to Build
[The 3-sentence story you tell in every meeting that positions against the competitor without badmouthing them. Should sound like: "You've built great capabilities on [competitor]. What we're seeing is that the AI layer needs to integrate with your productivity tools, your identity, and your data — and that's where the 3-IQ approach creates value [competitor] can't match because they don't own the productivity and identity layers."]

### What to Read / Study Before You Engage
| Content | Why | Where to Find It |
|---------|-----|-----------------|
| [specific doc/battlecard/blog] | [what it teaches you] | [URL or internal location] |
| [reference architecture] | [how it helps your pitch] | [URL or internal location] |
| [customer case study] | [similar displacement story] | [URL or internal location] |
| [competitor's own blog/docs] | [know their latest moves] | [URL — know your enemy] |

### Stakeholder-Specific Angles
| Person | Their Current Bias | Your Angle With Them |
|--------|-------------------|---------------------|
| [name from accounts.json] | [leans toward competitor because...] | [specific argument for this person] |
| [name] | [already champion] | [how to arm them for internal advocacy] |

### The Ask to Your AE/CSAM
[What you need from the sales team to execute this plan — exec connect, pricing, partner resources, MTC session, etc.]
```

## SE-Specific Framing — MANDATORY

Every deal strategy response MUST include the SE's technical plays, not just sales strategy. The SE is not a strategist — the SE is the person who builds, demos, proves, and wins technically.

### For Every Deal, Include:

1. **Your technical win plan** — What does "winning technically" look like for this deal? What must be proven? What demo, POC, or architecture session makes this undeniable?

2. **What to demo** — Specific scenario and flow. Not "show Azure AI" but "build a 15-min demo showing RAG over their actual menu data with sub-200ms responses, side-by-side with their current Vertex AI latency."

3. **What to whiteboard** — The architecture story to draw in the room when the technical decision maker is present. Boxes, arrows, and the narrative: "Here's where you are today → here's where we take you → here's why this is better than what [competitor] showed you."

4. **POC/Bake-off design** — If the deal needs proof, design the evaluation criteria so your platform wins. Pick the scenarios that expose the competitor's weakness. Define success metrics that align with YOUR strengths (e.g., "time to first insight" favors Fabric over Databricks glue-code).

5. **Engineer-to-engineer handling** — The customer's technical lead (CTO, VP Eng, Lead Data Engineer) will push back. Anticipate their exact objection based on their tech stack and sentiment, and provide a technically credible response (not a marketing deflection).

6. **Your SE moves (not AE moves)** — What YOU personally do this week. Schedule the architecture session. Build the custom demo with their data schema. Run the bake-off. Bring the GBB for depth. Get hands-on time with their engineers.

### What is NOT an SE move (don't include these):
- "Drive urgency on close date" → that's the AE
- "Negotiate pricing" → that's the AE
- "Build executive relationship" → that's the AE + CSAM
- "Send the proposal" → that's the AE

### What IS an SE move (always include at least 3):
- "Schedule a whiteboard session with their VP Eng on [topic]"
- "Build a custom demo using their [specific data/scenario]"
- "Design the POC success criteria that expose [competitor weakness]"
- "Run a hands-on lab with their engineering team on [platform]"
- "Bring [GBB name] to go deep on [specific architecture pattern]"
- "Deliver an Art of the Possible session covering [3 scenarios]"
- "Create a reference architecture doc tailored to their [industry/scale]"
- "Set up a customer reference call with [similar logo] who displaced [competitor]"

## Rules

- **Be specific** — name people, reference data, propose exact actions
- **Opinionated** — recommend a strategy, don't just list options
- **Time-bound** — every recommendation has a "do this by when"
- **Resource-aware** — suggest who to pull in (GBB, MTC, executive) and why
- **Honest about risk** — if a deal is unlikely, say so and recommend where to redirect energy
- **Portfolio thinking** — when reviewing pipeline, always consider opportunity cost (time spent on low-probability deals = time not spent on high-probability ones)
- **ALWAYS sound like an SE** — if you read your response and it could be written by a management consultant, rewrite it. The SE's value is technical depth, hands-on credibility, and the ability to make the customer's engineers believe.

## Output Length & Progressive Disclosure

**Every response starts with a TL;DR** (5-7 lines): The diagnosis, the #1 play, and the expected outcome.

**Then the detailed strategy** — but disciplined:
- For single deals: ONE primary play expanded fully, then 2-3 secondary plays in compact form (2-3 lines each, not full sections)
- For pipeline reviews: The priority table is the main artifact. Only expand the top 1-2 deals.
- Objection tables: MAX 5 rows. Pick the objections this specific customer will actually raise based on their tech stack and sentiment — don't enumerate every possible objection.
- Stakeholder tables: Only include people who are in the deal data or account contacts. Don't invent "the CFO" if the data doesn't mention one.

**End with 2-3 specific drill-down offers.**

## Honesty About Content & Resources

- **Internal content (battlecards, playbooks):** Say "search Seismic for '[query]'" or "check the Compete channel in Teams" — NEVER assert a specific document exists unless you read it from the KB or a tool confirmed it.
- **Reference customers:** Say "ask your GBB [name] for a [industry] reference who displaced [competitor]" — don't invent a customer name.
- **External links:** Only include URLs from the raw sources or confirmed web fetches. Otherwise say "search [platform] for [topic]".
- **Competitor claims:** Only state competitor capabilities you can ground in KB sources (raw-steady-state files) or confirmed web content. Don't guess at competitor feature gaps.
