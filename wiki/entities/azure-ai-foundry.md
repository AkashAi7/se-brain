---
title: "Azure AI Foundry"
type: entity
created: "2026-06-10"
updated: "2026-06-10"
sources: [mock-data/accounts.json, mock-data/opportunities.json, raw-steady-state/azure-vs-aws-positioning-guide.md, raw-steady-state/workshop-and-poc-delivery-patterns.md, kb-local/accounts/tata-steel.md]
tags: [tool, azure, ai-platform, foundry, foundry-local, web-iq, hero-product]
backlinks: [wiki/concepts/active-pipeline.md, wiki/concepts/customer-engagement-patterns.md, wiki/comparisons/azure-vs-aws.md, wiki/entities/tata-steel.md, wiki/entities/tata-agratas.md]
---

# Azure AI Foundry

## Description

Microsoft's end-to-end AI platform for building, evaluating, deploying, and monitoring AI applications — positioned against AWS SageMaker/Bedrock as offering the full AI lifecycle with prompt flow, evaluations, and grounding (from [Azure vs AWS Guide](../sources/azure-vs-aws-positioning-guide.md)). It is the **hero product** across this portfolio, in both cloud and **Foundry Local** (edge) forms, plus the newer **Web IQ** web-grounding capability.

## Role and Significance

- **Cloud Foundry** underpins the AI Companion at [Tata Steel](tata-steel.md), the 3-IQ "Foundry IQ" layer (OPP-2026-0301), AI agents at [Tata Sons](tata-sons.md) (OPP-2026-0305), and Enterprise Clara at [Tata Agratas](tata-agratas.md) (OPP-2026-0307).
- **Foundry Local** (edge/airgapped) is the hero for plant-floor AI: Tata Steel's Foundry Local plant POC (OPP-2026-0302) and Tata Agratas's Industrial Clara (OPP-2026-0306) — a first-of-kind airgapped industrial reference.
- **Web IQ** (live web grounding with citation trace-back and freshness) is generating bottom-up developer enthusiasm at Tata Steel. *From local notes (KB-Local).*

## Appearances Across Sources

| Source | How it appears |
|--------|----------------|
| [Accounts Data](../sources/accounts-data.md) | Deployed/POC across all four accounts |
| [Opportunities Data](../sources/opportunities-data.md) | Core to 5 of 7 deals |
| [Azure vs AWS Guide](../sources/azure-vs-aws-positioning-guide.md) | Positioned vs SageMaker/Bedrock |
| [Workshop & POC Patterns](../sources/workshop-and-poc-delivery-patterns.md) | Central to AI/ML workshops |
| [Tata Steel private notes](../sources/kb-local-tata-steel-private-notes.md) | Web IQ developer enthusiasm *(KB-Local)* |

## Capabilities Referenced

- End-to-end AI lifecycle (build, evaluate, deploy, monitor), prompt flow, grounding.
- **Foundry Local** — local/edge inference for airgapped environments.
- **Web IQ** — live web grounding, source-cited retrieval, same-day freshness; open questions on cost/rate-limits, domain allow-listing, and OneLake hybrid grounding.
- Access to OpenAI models (GPT-4o, GPT-5) plus Microsoft Phi models and a 1600+ model catalog.

## Relationships to Other Entities

- Used by [Ashish Arora](ashish-arora.md) across the portfolio.
- Central to [Customer Engagement Patterns](../concepts/customer-engagement-patterns.md) and the [Azure vs AWS](../comparisons/azure-vs-aws.md) compete story.

## Contradictions and Open Questions

- Web IQ production economics (cost under agent fan-out), governance (domain allow-listing), and OneLake hybrid grounding are **unanswered** — the key blockers to convert Tata Steel's bottom-up interest. *From local notes (KB-Local).*

## Related Pages

- [Active Pipeline](../concepts/active-pipeline.md), [Technical Win](../concepts/technical-win.md), [Workshop and POC Delivery](../concepts/workshop-and-poc-delivery.md).
