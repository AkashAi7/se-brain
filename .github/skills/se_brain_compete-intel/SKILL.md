---
name: se_brain_compete-intel
description: "Retrieve competitive intelligence and positioning data for a given competitor or account context. Returns competitor strengths, our advantages, positioning dimensions, radar scores, and talk tracks. Use when any skill needs compete context — deck building, meeting prep, deal strategy, or positioning exercises."
---

# Competitive Intelligence Retrieval

The abstraction layer for compete positioning data. Currently backed by `wiki-steady-state/concepts/compete-landscape.md` and `raw-steady-state/azure-vs-aws-positioning-guide.md`. Can be swapped to Seismic battlecards, internal compete portals, or live intelligence feeds.

## When to Invoke This Skill

- Deck builder needs radar chart scores (us vs competitor on N dimensions)
- Deck builder needs two-column positioning (our strengths vs their gaps)
- Deal strategy needs counter-positioning
- Meeting prep needs objection handling
- Any skill needing: competitor profile, positioning dimensions, win/loss patterns, or talk tracks

## Input

The invoking agent provides:
- **Competitor** (required) — e.g., "Google Cloud", "AWS", "Snowflake"
- **Account context** (optional) — for account-specific positioning
- **Format needed** (optional) — "radar scores", "strengths vs gaps", "objection handling", "full brief"

## Retrieval Protocol

### Step 1: Read the compete landscape page
Use the `wiki_read` MCP tool:
```
wiki_read("wiki-steady-state/concepts/compete-landscape.md")
```

### Step 2: If a specific positioning guide exists, read it
```
wiki_read("raw-steady-state/azure-vs-aws-positioning-guide.md")
```
(or similar files for other competitors)

### Step 3: If account context is provided, read account data to understand the competitive footprint
```
→ Invoke se_brain_account-data for the account's competitive_footprint field
```

### Step 4: Synthesize positioning specific to the context

### Data Layers
SharePoint is the authoritative source for shared compete data — pull it via `wiki_read`. Do NOT read the stale local mirrors `wiki-steady-state/` or `raw-steady-state/`. If `wiki_read` is unavailable, inform the user that the SharePoint connection is required — do not fall back to the mirrors.

**Optional private layer:** after grounding in SharePoint, you may also scan the user's `KB-Local/` folder for personal compete notes. **`KB-Local/` is gitignored, so `file_search` cannot see it** — discover notes with `grep_search` (set `includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`) and read them with `read_file`. Fold them in only if they add value, label them "From your local notes (KB-Local)", and let SharePoint win any conflict. Never read local files outside `KB-Local/`.

## Output Schema

### For Radar Charts
Return 5-7 dimensions with scores (1-10) for both us and competitor:
```
dimensions: ["Dim1", "Dim2", ...]
our_scores: [N, N, ...]
their_scores: [N, N, ...]
subtitle: "We win on X, Y. They lead on Z."
```

### For Two-Column Positioning
```
our_strengths:
  - [strength 1 with proof point]
  - [strength 2]
their_gaps:
  - [gap 1 with evidence]
  - [gap 2]
```

### For Objection Handling
```
objections:
  - objection: "[what the customer says]"
    response: "[how to counter]"
    proof: "[evidence/reference]"
```

### Full Brief
All of the above combined, plus:
- Competitor overview (what they offer, recent moves)
- Win/loss patterns at this account
- Recommended positioning narrative

## Scoring Guidelines

When generating radar scores, use these calibration anchors:

| Score | Meaning |
|-------|---------|
| 9-10 | Clear market leader, uncontested |
| 7-8 | Strong, recognized advantage |
| 5-6 | Competitive, slight edge |
| 3-4 | Present but weaker |
| 1-2 | Minimal or absent |

Always ground scores in evidence from the wiki. If no evidence exists for a dimension, score conservatively (5-6) and note the gap.

## Future Backing Stores

- Seismic battlecard API (via MCP)
- Internal compete portal (Microsoft Compete Hub)
- Win/loss database
- Real-time news monitoring for competitor moves
