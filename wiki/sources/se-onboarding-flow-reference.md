---
title: "Summary: SE Onboarding Flow & Azure DevOps Wiki Integration"
type: source-summary
created: "2026-06-10"
updated: "2026-06-10"
sources: [legacy/raw/se-onboarding-flow-reference.md]
tags: [se-onboarding, onboarding-flow, wiki, azure-devops]
backlinks: [wiki/concepts/se-onboarding-journey.md]
---

# SE Onboarding Flow & Azure DevOps Wiki Integration

> Source: [akashai7.github.io/se-onboarding-wiki](https://akashai7.github.io/se-onboarding-wiki/) | Legacy capture — not present in the current Azure DevOps raw/ dump | Retrieved: 2026-05-25 | Type: reference

## Key Takeaways

- The onboarding journey is organized into **six stages**: Day 1, Week 1, Week 2, Week 3-4, Month 2, and Ongoing.
- The Day 1 experience focuses on profile hydration, access setup, pod discovery, and unlocking the customer portfolio.
- The platform treats the wiki as both an onboarding **input** (guidance) and an **output** generated during onboarding.
- Concrete Azure DevOps wiki artifacts are shown (e.g. `Onboarding/Day1/Welcome.md`).

## Detailed Summary

First login auto-generates a personalized dashboard with an access checklist, the SE's pod, and assigned customers. The Day 1 onboarding steps are: (1) login and profile hydration, (2) access setup checklist, (3) meet your pod, (4) customer portfolio unlocked after access grants are confirmed. Systems mentioned include Entra ID, IDWeb, MyAccess, and Org Explorer.

Only the Day 1 narrative was directly readable from the fetched page; later stages (Week 1 through Ongoing) were visible as navigation labels with low detail. The implication is that the knowledge base should be organized around **stage-based pages and operational sub-pages** rather than one long document — Day 1 seeds the journey model, and later stages are expanded from internal sources.

## Notable Claims

| Claim | Confidence | Corroborated By | Contradicted By |
|-------|-----------|-----------------|-----------------|
| Onboarding spans six stages | High | [Day 1 Starter Guide](se-day-1-complete-starter-guide.md), [Staged Ramp Playbook](se-onboarding-staged-ramp-playbook.md) | — |
| First login auto-generates a personalized dashboard | Medium (single source) | [Platform Documentation](se-onboarding-platform-documentation.md) | — |

## Entities Mentioned

- Entra ID, IDWeb, MyAccess, Org Explorer — access and org systems.

## Concepts Touched

- [SE Onboarding Journey](../concepts/se-onboarding-journey.md) — the six-stage framework.
- [Onboarding Platform Capabilities](../concepts/onboarding-platform-capabilities.md) — dashboard generation.

## Questions Raised

- What detailed content belongs to Week 1 through Ongoing stages? (Only Day 1 was fully visible.)
