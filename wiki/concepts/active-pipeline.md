---
title: "Active Pipeline"
type: concept
created: "2026-06-10"
updated: "2026-06-10"
sources: [legacy/mock-data/opportunities.json, legacy/mock-data/accounts.json, legacy/mock-data/hok-log.json, legacy/broadcasts/2026-06-09-voice-live-conversion-pattern.md]
tags: [pipeline, opportunities, deals, tata, mahindra, india-enterprise]
backlinks: [wiki/sources/opportunities-data.md, wiki/sources/accounts-data.md, wiki/concepts/mcem-deal-execution.md, wiki/entities/ashish-arora.md, wiki/overview.md, wiki/analyses/pipeline-health-snapshot.md]
---

# Active Pipeline

## Definition

The live set of opportunities owned by SE [Ashish Arora](../entities/ashish-arora.md) in the **India Enterprise — Tata Group & Mahindra** territory: **7 deals worth $12.65M**, tracked by MCEM stage, value, competitor, and technical-win status (from [Opportunities Data](../sources/opportunities-data.md)).

## Key Points

- **$12.65M across 7 deals**, forecast confidence "high".
- **Stage distribution:** Qualify 1, Develop 1, Solution 3, Proof 2, Close 0.
- **Hot deals:** Industrial Clara (OPP-2026-0306), 3-IQ stack (0301), Voice Live (0303).
- **At-risk:** Google loan-pipeline displacement (OPP-2026-0304).
- **Dominant theme:** AI-platform expansion, edge AI, and **Google Cloud displacement** across a historically GCP-leaning portfolio.

## The Seven Opportunities

| ID | Account | Title | Stage | Value | Competitor | Tech Win |
|----|---------|-------|-------|-------|-----------|----------|
| OPP-2026-0301 | [Tata Steel](../entities/tata-steel.md) | 3-IQ: Foundry IQ + Fabric IQ + Work IQ | Solution | $2.8M | Google Cloud | in_progress |
| OPP-2026-0302 | [Tata Steel](../entities/tata-steel.md) | Foundry Local — Plant AI | Qualify | $0.95M | Google Edge TPU | not_started |
| OPP-2026-0303 | [Mahindra](../entities/mahindra.md) | Voice Live APIs — loan & holiday selling | Proof | $1.2M | Google Dialogflow | likely |
| OPP-2026-0304 | [Mahindra](../entities/mahindra.md) | Loan pipeline — Google displacement | Develop | $2.1M | Google Cloud | not_started |
| OPP-2026-0305 | [Tata Sons](../entities/tata-sons.md) | AI Agents expansion (partner delivery) | Solution | $1.6M | None (greenfield) | in_progress |
| OPP-2026-0306 | [Tata Agratas](../entities/tata-agratas.md) | Industrial Clara — edge agentic AI | Proof | $1.8M | None (greenfield) | likely |
| OPP-2026-0307 | [Tata Agratas](../entities/tata-agratas.md) | Enterprise Clara — cloud AI platform | Solution | $2.2M | None (greenfield) | in_progress |

## How Sources Relate to This Concept

| Source | Perspective | Key Contribution |
|--------|------------|-----------------|
| [Opportunities Data](../sources/opportunities-data.md) | Pipeline of record | Deal stages, values, blockers, contacts |
| [Accounts Data](../sources/accounts-data.md) | Account context | Strategic priorities and competitive footprint |
| [HOK Log Data](../sources/hok-log-data.md) | Effort trail | Hours behind Tata Steel deals |
| [Voice Live Pattern](../sources/voice-live-conversion-pattern.md) | Validated proof | OPP-2026-0303 as a replicable win |
| [Tata Steel private notes](../sources/kb-local-tata-steel-private-notes.md) | Private signal | Bottom-up Web IQ champion (informs OPP-2026-0301) |

## Contradictions and Open Questions

- **⚠ Data contradiction (flagged):** `opportunities.json` contains a **second trailing block** of legacy/placeholder deals (HDFC, BigBasket, Zomato, Bajaj — $9.45M) with mismatched account IDs. Only the **first 7-deal block** is treated as authoritative; the second needs verification. See [Opportunities Data](../sources/opportunities-data.md).

## Related Concepts

- [MCEM Deal Execution](mcem-deal-execution.md) — the methodology these deals follow.
- [Technical Win](technical-win.md) — win status per deal.
- [Customer Engagement Patterns](customer-engagement-patterns.md) — the repeatable plays.
- [Account Coverage and Pod Map](account-coverage-and-pod-map.md) — the territory.

## Related Entities

- [Ashish Arora](../entities/ashish-arora.md), [Tata Steel](../entities/tata-steel.md), [Mahindra](../entities/mahindra.md), [Tata Sons](../entities/tata-sons.md), [Tata Agratas](../entities/tata-agratas.md), [Azure AI Foundry](../entities/azure-ai-foundry.md).
