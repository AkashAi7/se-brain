---
title: "Summary: Tata Steel — Private Call Notes (KB-Local)"
type: source-summary
created: "2026-06-10"
updated: "2026-06-10"
sources: [KB-Local/accounts/tata-steel.md]
tags: [tata-steel, private, call-notes, foundry, web-iq, kb-local]
backlinks: [wiki/entities/tata-steel.md, wiki/entities/azure-ai-foundry.md]
---

# Tata Steel — Private Call Notes (KB-Local)

> **From local notes (KB-Local)** — personal, local-only source; not on SharePoint. Path: `KB-Local/accounts/tata-steel.md` | Date: 2026-06-09 | Type: private call notes
>
> This is private, additive context. It never overrides shared SharePoint facts; on any conflict, shared sources win.

## Key Takeaways

- A casual ~25 min call with **Aaryan**, a backend developer on Tata Steel's internal platform team (reports up through Dinesh's data org). **Not logged in CRM — background only.**
- Aaryan is experimenting with **Azure AI Foundry's new Web IQ capabilities** and is genuinely excited — the first thing that made the team rethink their "build it all in-house" stance.
- This is a **bottom-up champion signal**: a developer is advocating Foundry + Web IQ before procurement is involved.

## Detailed Summary

What caught Aaryan's attention with **Web IQ**:
- **Live web grounding** — agents pull current public web data into Foundry workflows without a custom scraper stack; replaced ~200 lines of brittle glue code.
- **Citation trace-back** — every retrieved fact carries a source link, which matters for their compliance/audit folks.
- **Freshness** — tested against commodity/steel pricing pages and got same-day numbers, not stale cache.

His concerns / open questions (useful prep):
- **Rate limits and cost** at production scale under heavy agent fan-out.
- Whether Web IQ results can be **scoped to a domain allow-list** for governance.
- How Web IQ grounding **blends with private data in OneLake** — wants a clean hybrid public/private story.

Follow-ups noted: bring a **Web IQ governance one-pager** (domain allow-listing + cost controls); offer a **hands-on Web IQ + OneLake grounding demo**; loop Aaryan into the architecture workshop invite as the internal feasibility validator.

> **Caveat:** Private, unlogged background note. Aaryan is hands-on, not a decision maker, but builds the prototypes leadership sees. Treat as a relationship/signal input, not a formal opportunity fact.

## Notable Claims

| Claim | Confidence | Corroborated By | Contradicted By |
|-------|-----------|-----------------|-----------------|
| Developer-led enthusiasm for Foundry Web IQ at Tata Steel | Medium (single private call) | [Accounts Data](accounts-data.md) (AI Companion usage growing), [Opportunities Data](opportunities-data.md) (OPP-2026-0301) | — |
| Web IQ replaced ~200 lines of custom scraping glue | Low (anecdotal) | — | — |

## Entities Mentioned

- [Tata Steel](../entities/tata-steel.md) — account; Aaryan ties to the existing 3-IQ team (Dinesh, Soummo).
- [Azure AI Foundry](../entities/azure-ai-foundry.md) — Web IQ capability.

## Concepts Touched

- [Active Pipeline](../concepts/active-pipeline.md) — informs OPP-2026-0301 (3-IQ stack) prep.
- [Customer Engagement Patterns](../concepts/customer-engagement-patterns.md) — bottom-up champion nurture.

## Questions Raised

- What are the actual Web IQ pricing/rate-limit behaviors under agent fan-out, and does it support domain allow-listing + OneLake hybrid grounding? (Aaryan's blockers to answer before the workshop.)
