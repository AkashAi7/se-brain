---
title: "Summary: Workshop and POC Delivery Patterns for Solution Engineers"
type: source-summary
created: "2026-06-10"
updated: "2026-06-10"
sources: [raw-steady-state/workshop-and-poc-delivery-patterns.md]
tags: [workshop, poc, delivery, patterns, success-criteria, environments, technical-win]
backlinks: [wiki/concepts/workshop-and-poc-delivery.md, wiki/concepts/technical-win.md]
---

# Workshop and POC Delivery Patterns for Solution Engineers

> Source: user-provided | On SharePoint: [raw-steady-state/workshop-and-poc-delivery-patterns.md](https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/raw-steady-state/workshop-and-poc-delivery-patterns.md) | Retrieved: 2026-05-31 | Type: reference

## Key Takeaways

- Six workshop types mapped to deal stage and effort: **Art of the Possible, Architecture Design Session, Hackathon/Build-With, Migration Assessment, Security Posture Review, AI/ML Workshop**.
- A three-phase **POC framework**: Scoping (objective, measurable success criteria, boundaries, timeline, data access, decision maker) → Execution (weekly rhythm + daily practices) → Wrap-Up (results doc, readout, next steps, handoff).
- "A well-scoped POC wins. An unbounded POC fails." Data access is the #1 POC blocker.
- Environment guidance, delivery best practices (before/during/after), six common POC failure modes, and MTC engagement criteria.

## Detailed Summary

The source is the SE's playbook for proving value. Workshop selection is stage-aware: Art of the Possible (2-4 hrs, Qualify/Develop) inspires and qualifies; Architecture Design Sessions (1-2 days, Solution) co-design the target architecture; Hackathons and AI/ML workshops (Solution/Proof) deliver hands-on validation; Migration Assessments and Security Posture Reviews quantify scope and gaps.

The POC framework's central discipline is scoping: every POC needs an objective question, measurable pass/fail criteria, explicit IN/OUT boundaries, a fixed timeline with checkpoints, confirmed data access, and a named decision maker. Execution follows a weekly rhythm (setup → core scenario → optimization → readout) with daily async updates and continuous artifact capture. Failure modes ("it worked but they didn't buy", scope creep, momentum death, blocked data access, late engagement, disengaged customer team) each have a prevention. MTC engagement is reserved for strategic, high-value, or competitive situations (2-4 week lead time).

## Notable Claims

| Claim | Confidence | Corroborated By | Contradicted By |
|-------|-----------|-----------------|-----------------|
| Data access is the #1 POC blocker | High | — | — |
| Well-scoped POCs win; unbounded ones fail | High | [MCEM Deal Execution](mcem-deal-execution-framework.md) | — |
| MTC lead time is 2-4 weeks | Medium | [SE Tools Full Reference](se-tools-full-reference.md) | — |

## Entities Mentioned

- [Azure AI Foundry](../entities/azure-ai-foundry.md), Azure Migrate, MTC, FastTrack, Seismic.

## Concepts Touched

- [Workshop and POC Delivery](../concepts/workshop-and-poc-delivery.md) — the delivery model.
- [Technical Win](../concepts/technical-win.md) — POCs as the proof mechanism.

## Questions Raised

- How do these patterns adapt for **airgapped/edge** POCs (e.g. Foundry Local at Tata Steel / Tata Agratas) where cloud environments aren't available?
