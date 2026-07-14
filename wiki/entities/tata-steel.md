---
title: "Tata Steel"
type: entity
created: "2026-06-10"
updated: "2026-06-10"
sources: [legacy/mock-data/accounts.json, legacy/mock-data/opportunities.json, legacy/mock-data/hok-log.json, KB-Local/accounts/tata-steel.md]
tags: [account, tata-group, manufacturing, steel, gcp-displacement, edge-ai]
backlinks: [wiki/concepts/active-pipeline.md, wiki/concepts/account-coverage-and-pod-map.md, wiki/entities/azure-ai-foundry.md, wiki/comparisons/azure-vs-aws.md]
---

# Tata Steel

## Description

India's largest steel producer ($30B revenue, 78,000 employees, HQ Jamshedpur), a **Tata Group** enterprise account. Traditionally a **Google Cloud** account (BigQuery, GKE, Vertex AI, Looker) that is rapidly opening to Microsoft after a successful AI Companion project built on [Azure AI Foundry](azure-ai-foundry.md) + Azure AI Search. Azure consumption ~$120K/month; M365 and Entra deployed. Health: **strong-and-growing**.

## Role and Significance

- The portfolio's **flagship Google-displacement opportunity**: a landmark chance to grow Microsoft footprint in a GCP-dominated account.
- Two live opportunities in the [active pipeline](../concepts/active-pipeline.md):
  - **OPP-2026-0301 — 3-IQ stack** (Foundry IQ + Fabric IQ + Work IQ), Solution stage, $2.8M, vs Google Cloud. Champions: Dinesh (Data Lead), Soummo Bose (AI Lead).
  - **OPP-2026-0302 — Foundry Local** plant-level AI, Qualify stage, $0.95M, vs Google Edge TPU. Sponsor: Dr HD Singh (Plant Head).
- The account with the **deepest effort trail** in the [HOK log](../sources/hok-log-data.md) (~37 hrs: architecture, prototypes, a Foundry Local POC, compete research).
- Strategic priorities: unify AI/Data/Productivity with the 3-IQ stack, bring AI to the plant floor, reduce single-cloud dependency, scale AI Companion.

## Appearances Across Sources

| Source | How it appears |
|--------|----------------|
| [Accounts Data](../sources/accounts-data.md) | ACC-001, full profile and signals |
| [Opportunities Data](../sources/opportunities-data.md) | OPP-2026-0301, OPP-2026-0302 |
| [HOK Log Data](../sources/hok-log-data.md) | 9 activity entries (~37 hrs) |
| [Tata Steel private notes](../sources/kb-local-tata-steel-private-notes.md) | Private Aaryan/Web IQ call *(KB-Local)* |

## Key Contacts

| Name | Role | Sentiment |
|------|------|-----------|
| Dinesh | Data Lead | champion |
| Soummo Bose | AI Lead | champion |
| Dr HD Singh | Plant Head | curious-positive |
| Aaryan | Developer (platform team) | bottom-up Web IQ enthusiast *(KB-Local)* |

> **From local notes (KB-Local):** developer **Aaryan** is privately championing **Foundry Web IQ** (live web grounding, citation trace-back, freshness) ahead of procurement — a bottom-up signal to nurture. His blockers: Web IQ cost/rate-limits at scale, domain allow-listing, and OneLake hybrid grounding. Bring a governance one-pager and a Web IQ + OneLake demo to the next session. *(Private background; not CRM-logged.)*

## Relationships to Other Entities

- Account team: AE Sneha Kapoor, CSAM Pooja Sharma, GBB Karthik Raman; SE [Ashish Arora](ashish-arora.md).
- Hero products: [Azure AI Foundry](azure-ai-foundry.md) and Foundry Local.
- Competes against [Google Cloud](../comparisons/azure-vs-aws.md) (see compete note re GCP gap).

## Contradictions and Open Questions

- This live Tata Steel record differs from the onboarding-era [coverage sample](../sources/se-account-coverage-sample.md), which lists a different account set — see [Account Coverage and Pod Map](../concepts/account-coverage-and-pod-map.md).

## Related Pages

- [Active Pipeline](../concepts/active-pipeline.md), [Customer Engagement Patterns](../concepts/customer-engagement-patterns.md), [Azure AI Foundry](azure-ai-foundry.md).
