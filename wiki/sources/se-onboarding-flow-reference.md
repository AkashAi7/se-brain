---
title: "Summary: SE Onboarding Flow & Azure DevOps Wiki Integration"
type: source-summary
created: "2026-05-25"
updated: "2026-05-25"
sources: [raw/se-onboarding-flow-reference.md]
tags: [se-onboarding, onboarding-flow, wiki, azure-devops]
backlinks: [wiki/index.md, wiki/overview.md, wiki/concepts/se-onboarding-journey.md, wiki/entities/onboarding-stakeholders.md]
---

# SE Onboarding Flow & Azure DevOps Wiki Integration

> Source: [SE Onboarding Flow & Azure DevOps Wiki Integration](https://akashai7.github.io/se-onboarding-wiki/) | Retrieved: 2026-05-25 | Type: reference

## Key Takeaways

- The onboarding framework is organized as a six-stage journey.
- Day 1 is centered on profile, access, pod discovery, and customer readiness.
- The wiki is presented as a live onboarding artifact, not just static documentation.
- The visible Day 1 flow references concrete operational systems and wiki pages.

## Detailed Summary

The reference site presents SE onboarding as a staged experience with the wiki integrated into the operating model. The strongest visible detail is on Day 1, where the platform hydrates the user profile, checks access prerequisites, reveals pod context, and only then unlocks the customer portfolio. This indicates that onboarding content should be sequenced around readiness gates instead of a flat checklist.

The page also shows the expected wiki shape for onboarding content. Day 1 appears to rely on `Welcome.md`, `Access-Setup-Checklist.md`, and `IDWeb-Requests.md`, which suggests onboarding knowledge should mix user-facing guidance with operational request documentation.

## Notable Claims

| Claim | Confidence | Corroborated By | Contradicted By |
|-------|-----------|-----------------|-----------------|
| The onboarding journey has six stages. | high | [SE Onboarding Journey](../concepts/se-onboarding-journey.md) | none |
| Day 1 depends on Entra ID, IDWeb, MyAccess, and Org Explorer. | high | [SE Onboarding Journey](../concepts/se-onboarding-journey.md) | none |
| Wiki pages are generated or used at each onboarding stage. | medium | [SE Onboarding Journey](../concepts/se-onboarding-journey.md) | none |

## Entities Mentioned

- [Onboarding Stakeholders](../entities/onboarding-stakeholders.md) - Stakeholder roles include manager, peers, CSA, GBB, and TSP.

## Concepts Touched

- [SE Onboarding Journey](../concepts/se-onboarding-journey.md) - stage-based onboarding model
- [Account Coverage And Pod Map](../concepts/account-coverage-and-pod-map.md) - downstream context that becomes useful after access is established

## Questions Raised

- What are the exact Week 1 to Ongoing deliverables for a new SE?
- Which systems remain the source of truth for access status and ownership?
- Which onboarding pages should be auto-generated versus manually curated?