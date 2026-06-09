---
name: se-customer-intel
description: 'Generate pre-meeting intelligence briefs for customer engagements. Use when the user says "prep me for a meeting", "I have a call with X", "customer brief for X", "what do I need to know about this account", or any meeting preparation request. Pulls from opportunity data, account signals, and recent engagement history to produce actionable talking points.'
---

# Customer Intelligence — Pre-Meeting Briefs

Generate sharp, actionable pre-meeting intelligence that makes the SE walk in knowing more than the customer expects. This is the "I did my homework" skill — it turns scattered data into a focused brief.

## When to Use This Skill

- User mentions an upcoming customer meeting, call, or engagement
- User asks to "prep me for" or "brief me on" an account
- User names a specific account and asks about context or talking points
- User says "what should I know before tomorrow's call"

## Data Sources

**Grounding (two-tier):** All *shared* datastore reads MUST use the `wiki_read()` MCP tool against `microsoftapc.sharepoint.com/teams/se-brain-wiki`. NEVER read the stale local mirrors (`mock-data/`, `wiki/`, `wiki-steady-state/`, `raw/`, `raw-steady-state/`, `broadcasts/`). If `wiki_read` is unavailable, tell the user the SharePoint connection is required — do not fall back to those mirrors.

**Always also check the private layer.** After grounding in SharePoint, scan the user's `KB-Local/` folder for personal notes relevant to this account or meeting. **`KB-Local/` is gitignored, so `file_search` cannot see it** — discover notes with `grep_search` (set `includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`) and read them with `read_file`. Fold them in only if they add value, label them "From your local notes (KB-Local)", and let SharePoint win any conflict on shared facts. Never read local files outside `KB-Local/`.

- `wiki_read("mock-data/opportunities.json")` — active deals, stages, blockers, contacts, deal notes
- `wiki_read("mock-data/accounts.json")` — account profile, industry, competitive footprint, recent signals, strategic priorities

The brief is built from exactly two layers: **SharePoint** (shared truth) and **`KB-Local/`** (your private notes). Do not call any other live data source.

## Execution Steps

### Step 1: Identify the Account

Match the user's request to an account in the datastore. If ambiguous, ask.

### Step 2: Pull Static Context

Read both via `wiki_read("mock-data/opportunities.json")` and `wiki_read("mock-data/accounts.json")` for the matched account. Extract:
- Active opportunity details (stage, value, blockers, competitor)
- Key contacts and their sentiment
- Recent signals (news, hiring, usage changes, pain points)
- Competitive footprint
- Last engagement and next planned step

### Step 3: Generate the Brief

Produce a structured pre-meeting brief in this format:

```markdown
## Pre-Meeting Brief: [Account Name]
**Meeting context**: [Inferred from opportunity stage + next step]
**Your goal walking in**: [1 sentence — what does success look like in this meeting?]

### Account Snapshot
- Industry | Segment | Size
- Azure footprint: [what they already run]
- Competitive presence: [who else is in the picture]
- Relationship health: [strong/developing/at-risk]

### Active Opportunity
- Deal: [title] | Stage: [X] | Value: [$X]
- Competitor: [name] | Days in stage: [N]
- Technical win status: [pending/in_progress/not_started]
- Key blocker: [the #1 thing preventing forward motion]

### � Your Private Notes (from KB-Local — if any)
[Only include this section if relevant notes exist in KB-Local. Bullet the personal context that should shape the meeting, clearly labeled as your own notes.]
- [From your local notes (KB-Local): personal signal, prior conversation, or reminder]

### Recent Signals (from Account Data)
[Bulleted list of signals from accounts.json with SE interpretation — why each matters for this meeting]

### Key Contacts in the Room
| Name | Role | Sentiment | What They Care About | Recent Interaction |
|------|------|-----------|---------------------|-------------------|
| ... | ... | ... | [inferred from deal notes and signals] | [from deal notes or KB-Local] |

### Talking Points
1. [Lead with this — connects to their stated priority or recent signal]
2. [Address the blocker — have a position ready]
3. [Competitive counter — if competitor is in the picture]
4. [Forward motion — propose the next concrete step]
5. [Follow up — address any open commitments FIRST before asking for more]

### Landmines to Avoid
- [Things that could derail based on contact sentiments and blockers]
- [Unfulfilled commitments — if you owe something, acknowledge it upfront]

### Your Ask
- [What you want to walk out with — a commitment, a next meeting, a POC approval, etc.]
```

### Step 4: SE's Game Plan for This Meeting

```markdown
### Your Demo Plan
- **If you get the chance to show something**: [Specific demo — what to show, in what order, tailored to who's in the room]
- **Environment**: [What needs to be ready — Azure portal, custom demo, slides, Seismic deck]
- **Demo narrative**: [The story you tell while demoing — not just clicks, but the "so what" for this customer]

### Your Whiteboard Plan
- **If it goes technical**: [What architecture to draw — the boxes, arrows, and story that makes them say "yes, that's what we need"]
- **Key transitions**: [Where you draw the "today" vs "future state" line to make the gap tangible]

### Technical Landmines
- [Technical questions that could derail you — based on contact sentiments, competitive context, and blockers]
- [Your prepared response for each — technically credible, not hand-wavy]

### Your Ask (as the SE)
- [What technical next step you're driving toward — architecture session, POC, hands-on lab, bake-off]
- [NOT the commercial ask — that's the AE's job]

### Before the Meeting
- [ ] Review last engagement notes
- [ ] Confirm demo/environment is ready
- [ ] Prep the whiteboard narrative (even if you don't use it)
- [ ] Align with AE: "I'll drive toward [technical next step], you drive toward [commercial next step]"
- [ ] Prepare 1-2 "did you see this?" conversation starters from recent Microsoft announcements relevant to their industry
```

## Citations (Required)

Every brief MUST end with a **Sources** section so the SE can trace every claim. Cite only what you actually read this turn.

```markdown
---
**Sources** (SE Brain wiki):
- [Account Data](https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/mock-data/accounts.json)
- [Pipeline Data](https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/mock-data/opportunities.json)
- [Compete Landscape](https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/wiki-steady-state/concepts/compete-landscape.md)

_Plus your local notes (KB-Local) where labeled above._
```

- URL pattern: `https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/<path>` (spaces → `%20`).
- List only the SharePoint pages you read this turn — never invent a path.
- If you used `KB-Local/` notes, acknowledge them with the "_Plus your local notes (KB-Local)_" line — do not give them a SharePoint URL (they're local-only).

## SE Identity Rule

This brief is for the SE, not the AE. Everything must be framed through what the SE controls:
- What to SHOW (demo, architecture, proof)
- What to PROVE (technical differentiation, scalability, integration)
- What to HANDLE (technical objections from engineers in the room)
- What to PROPOSE (next technical engagement: workshop, POC, lab, reference call)

Do NOT include AE-domain items like pricing negotiation, contract urgency, or executive relationship building as primary recommendations.

## Compete Enrichment via Seismic Intel

When the opportunity has an active competitor (check `competitor` field in `wiki_read("mock-data/opportunities.json")`):
- Invoke `se-seismic-intel` to find live battlecard content for that competitor.
- Include the top objection handling points and trap questions in the brief's "Talking Points" and "Competitive Counter" sections.
- Reference specific battlecard assets by name so the SE can pull them up before the meeting.

This enrichment transforms the brief from static data into a live-content-backed preparation tool.

## Win Pattern Enrichment via Win Patterns

When preparing for a complex deal meeting (Solution stage or later, or high deal value):
- Invoke `se-win-patterns` to find similar wins, reference customers, and proven plays for this deal's scenario (industry + competitor + solution area).
- Add a "Similar Wins" section to the brief showing 1-3 relevant reference stories the SE can cite.
- Include "Plays That Worked" from similar deals — specific angles or proof points that closed comparable opportunities.

This gives the SE confidence walking in: "We've done this before, here's how."

## Rules

- **Be specific, not generic** — reference actual deal data, named contacts, concrete signals
- **Opinionated talking points** — don't just list facts; recommend what to SAY and in what order
- **Flag landmines** — if a contact is skeptical or a topic is sensitive, call it out
- **One clear technical ask** — every meeting should have a technical goal the SE drives toward
- **Urgency-aware** — if the meeting is tomorrow, be concise; if it's next week, offer to go deeper on any section
- **Demo-ready** — always include a demo plan even if the meeting isn't a "demo meeting" (opportunistic showing is how SEs win)
