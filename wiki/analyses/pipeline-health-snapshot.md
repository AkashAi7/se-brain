---
title: "Analysis: Pipeline Health Snapshot"
type: analysis
created: "2026-06-10"
updated: "2026-06-10"
sources: [mock-data/opportunities.json, mock-data/accounts.json, broadcasts/2026-06-09-voice-live-conversion-pattern.md, kb-local/accounts/tata-steel.md]
tags: [pipeline, deals, mcem, at-risk, forecast]
backlinks: [wiki/concepts/active-pipeline.md, wiki/concepts/mcem-deal-execution.md, wiki/index.md]
---

# Analysis: Pipeline Health Snapshot

## Question

What is the health of the active pipeline, and where is attention needed?

## Short Answer

Seven live opportunities total **$12.65M** across Tata Group and Mahindra. Momentum is strong — multiple deals in Proof with technical wins likely — but **two deals are at-risk** and the **biggest gap is Google Cloud compete content**.

## Pipeline at a Glance

| Opp | Account | Solution | Stage | Value | Status |
|-----|---------|----------|-------|-------|--------|
| OPP-2026-0301 | [Tata Steel](../entities/tata-steel.md) | Foundry IQ (3-IQ layer) | Solution | $1.55M | On track |
| OPP-2026-0302 | [Tata Steel](../entities/tata-steel.md) | Foundry Local plant POC | Proof | $0.95M | Win likely |
| OPP-2026-0303 | [Mahindra](../entities/mahindra.md) | Voice Live APIs | Proof | $1.2M | Win likely |
| OPP-2026-0304 | [Mahindra](../entities/mahindra.md) | Loan pipeline (vs Google) | Develop | $2.1M | **At-risk** |
| OPP-2026-0305 | [Tata Sons](../entities/tata-sons.md) | AI Agents expansion | Solution | $1.6M | On track |
| OPP-2026-0306 | [Tata Agratas](../entities/tata-agratas.md) | Industrial Clara (edge) | Proof | $1.8M | Win likely |
| OPP-2026-0307 | [Tata Agratas](../entities/tata-agratas.md) | Enterprise Clara (cloud) | Solution | $2.2M | Hot/greenfield |

Total: **$12.65M**.

## Where Attention Is Needed

- **OPP-2026-0304 (Mahindra loan pipeline)** — at-risk. Google Cloud incumbent; needs accuracy/throughput parity proof and a GCP compete asset.
- **OPP-2026-0302 / 0306 (Foundry Local edge)** — no standard cloud-POC pattern for airgapped [technical wins](../concepts/technical-win.md); delivery approach is the open question.
- **OPP-2026-0301 (Tata Steel Foundry IQ)** — bottom-up developer interest in **Web IQ**, but production cost/governance/OneLake grounding questions are unanswered. *From local notes (KB-Local).*

## Strengths

- Validated proof point: [Voice Live = 22% conversion lift](../sources/voice-live-conversion-pattern.md) over Google Dialogflow at Mahindra Finance, in production — directly reusable for OPP-2026-0303/0304.
- Strong champions across Tata Agratas (PV Mahendran, Pravin Swaminathan) and Tata Sons (Tanushree, Ravi Arora).

## Contradictions and Caveats

- The opportunities source contains a **second, legacy block** of deals (HDFC, Tata BigBasket, Zomato, Bajaj Finance, ~$9.45M) with account IDs that conflict with the live accounts (e.g., ACC-002/ACC-003 map differently). The **first 7-deal block is authoritative**; the legacy block is treated as stale sample data and excluded from the $12.65M total. Flagged, not resolved.
- Compete library is AWS-centric while the live competition is **Google Cloud** — the highest-value missing asset.

## Evidence Table

| Claim | Source | Confidence |
|-------|--------|-----------|
| 7 deals / $12.65M | [Opportunities Data](../sources/opportunities-data.md) | High |
| Voice Live 22% lift | [Voice Live Pattern](../sources/voice-live-conversion-pattern.md) | High (validated) |
| Web IQ open questions | [Tata Steel private notes](../sources/kb-local-tata-steel-private-notes.md) | Medium *(KB-Local)* |
| Legacy deal block is stale | [Opportunities Data](../sources/opportunities-data.md) | Medium |

## Related Pages

- [Active Pipeline](../concepts/active-pipeline.md), [MCEM Deal Execution](../concepts/mcem-deal-execution.md), [Azure vs AWS](../comparisons/azure-vs-aws.md), [Customer Engagement Patterns](../concepts/customer-engagement-patterns.md).

## Follow-ups

- What's the play to de-risk the Mahindra loan-pipeline deal against Google Cloud?
- How do we demonstrate a technical win for airgapped Foundry Local deployments?
