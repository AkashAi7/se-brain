---
title: "Workshop and POC Delivery"
type: concept
created: "2026-06-10"
updated: "2026-06-10"
sources: [raw-steady-state/workshop-and-poc-delivery-patterns.md, mock-data/hok-log.json]
tags: [workshop, poc, delivery, patterns, success-criteria, environments]
backlinks: [wiki/sources/workshop-and-poc-delivery-patterns.md, wiki/concepts/technical-win.md, wiki/concepts/mcem-deal-execution.md]
---

# Workshop and POC Delivery

## Definition

The SE's repeatable patterns for proving value to a customer through **workshops** (stage-aware engagement formats) and **proofs of concept** (scoped, time-boxed validations), each tied to earning a [technical win](technical-win.md) (from [Workshop & POC Patterns](../sources/workshop-and-poc-delivery-patterns.md)).

## Key Points

- **Six workshop types**, mapped to deal stage and effort: Art of the Possible (Qualify/Develop), Architecture Design Session (Solution), Hackathon/Build-With (Solution/Proof), Migration Assessment, Security Posture Review, AI/ML Workshop.
- **Three-phase POC framework:** Scoping → Execution → Wrap-Up.
- **Scoping is the discipline:** define an objective question, measurable success criteria, IN/OUT boundaries, fixed timeline with checkpoints, confirmed data access, and a named decision maker.
- **Data access is the #1 POC blocker** — make it a prerequisite, not a Phase 1 task.
- **Six failure modes** each have a prevention (no decision maker, scope creep, momentum death, blocked data, late engagement, disengaged customer team).
- **MTC engagement** for strategic/high-value/competitive situations, with a 2-4 week lead time.

## Workshop Selection Quick Reference

| Workshop | Stage | Duration | SE Effort |
|----------|-------|----------|-----------|
| Art of the Possible | Qualify/Develop | 2-4 hrs | Low-medium |
| Architecture Design Session | Solution | 1-2 days | Medium-high |
| Hackathon / Build-With | Solution/Proof | 1-3 days | High |
| Migration Assessment | Develop/Solution | 1-2 days | Medium |
| Security Posture Review | Develop/Solution | 0.5-1 day | Medium |
| AI/ML Workshop | Solution/Proof | 1-2 days | High |

## How Sources Relate to This Concept

| Source | Perspective | Key Contribution |
|--------|------------|-----------------|
| [Workshop & POC Patterns](../sources/workshop-and-poc-delivery-patterns.md) | Playbook | Workshop types, POC framework, failure modes, environments |
| [HOK Log Data](../sources/hok-log-data.md) | Evidence | Real delivery effort (workshops, prototypes, POCs) at Tata Steel |

## Contradictions and Open Questions

- The patterns assume cloud-based POC environments; **airgapped/edge** delivery (Foundry Local at Tata Steel/Agratas) needs an adapted pattern — flagged as an open question in the source.

## Related Concepts

- [Technical Win](technical-win.md) — the outcome of good delivery.
- [MCEM Deal Execution](mcem-deal-execution.md) — stages that call for each workshop.
- [Active Pipeline](active-pipeline.md) — deals currently in workshop/POC.

## Related Entities

- [Azure AI Foundry](../entities/azure-ai-foundry.md) — central to AI/ML workshops and edge POCs.
- [Microsoft Sales & Execution Tools](../entities/microsoft-sales-tools.md) — MTC, FastTrack, Seismic, Azure Migrate.
