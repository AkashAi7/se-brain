# KB-Local — Your Private Augmentation Layer

This folder is **your personal, local-only knowledge store**. It is gitignored and never uploaded to SharePoint, so anything you put here stays on your machine.

## How it fits the two-tier model

SE Brain agents use a **two-tier retrieval model**:

| Tier | Source | Role | Always used? |
|------|--------|------|--------------|
| **1. Universal** | SharePoint wiki (`microsoftapc.sharepoint.com/teams/se-brain-wiki`) | Shared source of truth for all SEs | ✅ Always queried |
| **2. Private** | This `KB-Local/` folder | Your personal notes, drafts, private context | ⚙️ Optional — used only if relevant |

The agent **always** grounds in SharePoint first. It then **optionally** checks `KB-Local/` and folds in anything that genuinely adds value to the answer. If nothing here is relevant, it's skipped silently.

## Rules the agent follows

1. SharePoint is authoritative for **shared facts**. Local notes can **add** personal context but never override shared truth. On a conflict, SharePoint wins and the agent flags the discrepancy.
2. Local content is clearly labeled in answers (e.g. *"From your local notes (KB-Local)…"*) so you always know what came from where.
3. The agent reads local files **only from `KB-Local/`** — never from the stale local mirrors of the shared wiki (`mock-data/`, `wiki/`, etc.).

## What to put here

- Private deal notes, customer context you don't want shared
- Personal prep, draft pitches, scratch analysis
- Snippets, links, or reference docs you want the agent to consider
- Anything personal that shouldn't live in the universal wiki

## Format

Plain markdown (`.md`) works best. Add YAML frontmatter if you like, but it's optional:

```markdown
---
title: "Tata Steel — my private notes"
tags: [tata-steel, private]
---

# My notes
- Dinesh prefers architecture-first conversations
- Avoid leading with pricing until the workshop
```

Subfolders are fine (e.g. `KB-Local/accounts/tata-steel.md`).
