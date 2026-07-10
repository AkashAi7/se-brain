---
title: "Summary: Opportunity Pipeline Data (opportunities.json)"
type: source-summary
created: "2026-06-10"
updated: "2026-06-10"
sources: [mock-data/opportunities.json]
tags: [pipeline, opportunities, deals, mcem, data]
backlinks: [wiki/concepts/active-pipeline.md, wiki/concepts/mcem-deal-execution.md]
---

# Opportunity Pipeline Data (opportunities.json)

> Source: structured mock data | Legacy capture — not present in the current Azure DevOps raw/ dump | Type: data

## Key Takeaways

- The **primary pipeline** is 7 deals worth **$12.65M** across Tata Steel, Mahindra, Tata Sons, and Tata Agratas — all SE-owned by Ashish Arora.
- Deals are tracked by MCEM stage, value, close date, competitor, days-in-stage, technical-win status, blockers, and key contacts.
- Stage distribution: Qualify 1, Develop 1, Solution 3, Proof 2, Close 0. Hot deals: OPP-2026-0306 (Industrial Clara), 0301 (3-IQ), 0303 (Voice Live). At-risk: OPP-2026-0304 (Google loan-pipeline displacement).

## Detailed Summary

The seven primary opportunities map cleanly to the [active pipeline](../concepts/active-pipeline.md) concept page. They reflect a consistent strategy: AI-platform expansion (3-IQ, AI Agents, Enterprise Clara), edge AI (Foundry Local, Industrial Clara), and Google displacement (loan pipeline, Voice Live vs Dialogflow). Forecast confidence is "high" for the Tata/Mahindra territory.

> **⚠ Data contradiction (flagged, not resolved):** The `opportunities.json` file contains **two datasets**. After the primary 7-deal Tata/Mahindra block and its `pipeline_summary` (total $12,650,000), the file continues with a **second, trailing block** of legacy/placeholder deals — HDFC, Tata BigBasket, Zomato, Bajaj Finance, plus a Tata Steel security deal — totaling **$9,450,000** with its own `pipeline_summary`. The two blocks reuse account IDs inconsistently (e.g. `ACC-002` = Mahindra in block 1 but Tata BigBasket in block 2; `ACC-003` = Tata Sons vs Tata Steel). **Treat the first block as the authoritative current pipeline**; the second appears to be stale or test data and should be verified before use.

## Notable Claims

| Claim | Confidence | Corroborated By | Contradicted By |
|-------|-----------|-----------------|-----------------|
| Primary pipeline = 7 deals, $12.65M | High | [Accounts Data](accounts-data.md) | Trailing block in same file ($9.45M, different accounts) |
| OPP-2026-0303 Voice Live in Proof, technical win likely | High | [Voice Live Pattern](voice-live-conversion-pattern.md) | — |
| OPP-2026-0304 (Google displacement) is at risk | High | — | — |

## Entities Mentioned

- [Tata Steel](../entities/tata-steel.md), [Mahindra](../entities/mahindra.md), [Tata Sons](../entities/tata-sons.md), [Tata Agratas](../entities/tata-agratas.md), [Azure AI Foundry](../entities/azure-ai-foundry.md).

## Concepts Touched

- [Active Pipeline](../concepts/active-pipeline.md) — deal-by-deal breakdown.
- [MCEM Deal Execution](../concepts/mcem-deal-execution.md) — stage model these deals use.

## Questions Raised

- Is the trailing $9.45M block historical data, another SE's pipeline, or test scaffolding? It needs source verification.
