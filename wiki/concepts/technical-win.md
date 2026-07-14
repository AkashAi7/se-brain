---
title: "Technical Win"
type: concept
created: "2026-06-10"
updated: "2026-06-10"
sources: [raw/process-guidelines/sops/mcem-process-guide.md, legacy/raw-steady-state/workshop-and-poc-delivery-patterns.md, legacy/mock-data/opportunities.json]
tags: [technical-win, mcem, proof, poc, se-execution]
backlinks: [wiki/sources/mcem-deal-execution-framework.md, wiki/sources/workshop-and-poc-delivery-patterns.md, wiki/concepts/mcem-deal-execution.md, wiki/concepts/workshop-and-poc-delivery.md]
---

# Technical Win

## Definition

A **technical win** is explicit customer acknowledgment that the proposed Microsoft solution satisfies the technical evaluation — not merely "the demo went well." It requires the customer to confirm the solution meets requirements, addresses architecture concerns, competes favorably, and has a viable implementation path (from [MCEM Framework](../sources/mcem-deal-execution-framework.md)).

## Key Points

- **Four conditions:** (1) meets stated requirements (functional, performance, security, compliance), (2) addresses architecture concerns (integration, scalability, migration), (3) competes favorably vs alternatives, (4) has a viable implementation path.
- **Earned in Solution/Proof stages** through workshops, POCs, demos, and objection handling.
- **Proof discipline wins** — "a well-scoped POC wins; an unbounded POC fails," and data access is the #1 POC blocker (from [Workshop & POC Patterns](../sources/workshop-and-poc-delivery-patterns.md)).
- **Tracked explicitly** — the [opportunities data](../sources/opportunities-data.md) carries a `technical_win` status (not_started / in_progress / likely) per deal.

## Technical Win Status Across the Live Pipeline

| Status | Deals | Example |
|--------|-------|---------|
| likely | 2 | Industrial Clara (OPP-2026-0306), Voice Live (OPP-2026-0303) |
| in_progress | 3 | 3-IQ (OPP-2026-0301), AI Agents (0305), Enterprise Clara (0307) |
| not_started | 2 | Foundry Local (0302), Google loan displacement (0304) |

## How Sources Relate to This Concept

| Source | Perspective | Key Contribution |
|--------|------------|-----------------|
| [MCEM Framework](../sources/mcem-deal-execution-framework.md) | Definition | The four conditions and explicit-acknowledgment bar |
| [Workshop & POC Patterns](../sources/workshop-and-poc-delivery-patterns.md) | Mechanism | How POCs/workshops produce the win |
| [Opportunities Data](../sources/opportunities-data.md) | Measurement | Per-deal technical-win tracking |

## Contradictions and Open Questions

- For **airgapped/edge** deals (Foundry Local, Industrial Clara), the proof mechanism differs from cloud POCs — how a technical win is demonstrated without cloud environments is an open delivery question (see [Workshop and POC Delivery](workshop-and-poc-delivery.md)).

## Related Concepts

- [MCEM Deal Execution](mcem-deal-execution.md) — the stages where wins are earned.
- [Workshop and POC Delivery](workshop-and-poc-delivery.md) — the proof mechanism.
- [Active Pipeline](active-pipeline.md) — win status per live deal.

## Related Entities

- [Azure AI Foundry](../entities/azure-ai-foundry.md) — the hero product in most technical-win plays.
