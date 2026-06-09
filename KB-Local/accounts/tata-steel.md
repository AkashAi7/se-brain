---
title: "Tata Steel — private call notes"
tags: [tata-steel, private, call-notes, foundry, web-iq]
date: "2026-06-09"
---

# Tata Steel — private call notes (local only)

## Phone call with Aaryan (Developer, Tata Steel) — 2026-06-09

Casual ~25 min call, his initiative. Not logged in CRM. Treat as background only.

- **Aaryan** is a backend developer on Tata Steel's internal platform team (reports up through Dinesh's data org). Hands-on, not a decision maker, but builds the prototypes leadership actually sees.
- He's been experimenting with **Foundry's new Web IQ capabilities** over the last couple of weeks and is genuinely excited — said it's the first thing that made the team rethink their "build it all in-house" stance.

### What caught his attention with Web IQ
- **Live web grounding** — agents can pull current public web data into Foundry workflows without a custom scraper stack. He'd hand-rolled something brittle before; Web IQ replaced ~200 lines of glue code.
- **Citation trace-back** — every retrieved fact carries a source link, which he said would matter a lot for their compliance/audit folks.
- **Freshness** — he tested it against commodity/steel pricing pages and was impressed it returned same-day numbers, not stale cache.

### His concerns / open questions (use these to prep)
- Worried about **rate limits and cost** at production scale — wants to know how Web IQ pricing behaves under heavy agent fan-out.
- Asked whether Web IQ results can be **scoped to an allow-list of domains** for governance (he wants to restrict to approved sources).
- Unsure how Web IQ grounding interacts with their **private data in OneLake** — wants a clean story for blending public web + internal data in one agent.

### My takeaways / follow-ups
- This is a **bottom-up signal** — a developer is championing Foundry + Web IQ before procurement is even involved. Worth nurturing.
- Bring a **Web IQ governance one-pager** (domain allow-listing + cost controls) to the next technical session.
- Offer Aaryan a **hands-on Web IQ + OneLake grounding demo** — that hybrid public/private story is exactly his blocker.
- Personal reminder: loop Aaryan into the architecture workshop invite; he'll be the one who validates feasibility internally.
