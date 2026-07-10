---
title: "Summary: SE Onboarding Overview (Phased Journey)"
type: source-summary
created: "2026-07-09"
updated: "2026-07-09"
sources: [raw/onboarding/onboarding-overview.md]
tags: [onboarding, phased-journey, weekly-rhythm, raw-structure]
backlinks: [wiki/concepts/se-onboarding-journey.md, wiki/concepts/staged-ramp-plan.md]
---

# SE Onboarding Overview (Phased Journey)

> Source: Azure DevOps raw dump | In Azure DevOps: [raw/onboarding/onboarding-overview.md](https://dev.azure.com/SE-Brain-AzDev/SE-Brain/_git/SE-Brain?path=/raw/onboarding/onboarding-overview.md) | Retrieved: 2026-07-09 | Type: reference

## Key Takeaways

- The restructured raw dump organizes onboarding as a **5-phase journey**: Phase 1 Orientation (Day 1-3), Phase 2 Role Fundamentals (Week 1-2), Phase 3 Technical Depth (Week 2-4), Phase 4 Customer Readiness (Month 2), Phase 5 Ongoing Development (Month 3+).
- The onboarding directory is a **path, not a content store** — each phase folder holds a `checklist.json` and `role-track-refs.json` that point into `se-roles/{role}/`, `shared-resources/`, and `sectors/{sector}/` where canonical content lives.
- The **weekly rhythm** carries over from the legacy guides: Monday Onboarding Live (~5 hrs), Tue-Thu Practice Engine (~3-4 hrs), Friday community + scenario assessment (~1-2 hrs), ~10 hrs/week protected time.
- Key systems: MCAPS Onboarding Hub (https://aka.ms/MCAPSOnboarding_RBOHub), MCAPS Onboarding Agent (https://aka.ms/OnboardingAgent), SuccessFactors Learning, MCAPS Academy.

## Detailed Summary

This overview is the entry point to the post-migration `raw/onboarding/` tree. It supersedes the legacy staged-ramp playbook's monolithic structure with a reference-based model: onboarding content is deduplicated, and phase folders link into the canonical role (`se-roles/`), shared-resource, and sector trees. The phased timeline extends the legacy six-week L200 ramp framing into a five-phase model that explicitly continues past Month 3 (Phase 5 — independent ownership, specialization, contribution).

The weekly rhythm section corroborates the Day 1 starter guide's cadence claims (Onboarding Live, Practice Engine, Friday assessment, ~10 protected hours/week).

## Notable Claims

| Claim | Confidence | Corroborated By | Contradicted By |
|-------|-----------|-----------------|-----------------|
| Onboarding is structured as 5 phases from Day 1 to Month 3+ | High | [Staged Ramp Playbook (legacy)](se-onboarding-staged-ramp-playbook.md) — compatible framing | — |
| ~10 hrs/week protected onboarding time | High | [Day 1 Starter Guide](se-day-1-complete-starter-guide.md) | — |
| Content lives canonically in se-roles/, shared-resources/, sectors/; onboarding only references it | High | raw/onboarding directory structure | — |

## Entities Mentioned

- MCAPS Onboarding Hub, MCAPS Onboarding Agent, SuccessFactors Learning, MCAPS Academy

## Related Pages

- [SE Onboarding Journey](../concepts/se-onboarding-journey.md)
- [Staged Ramp Plan](../concepts/staged-ramp-plan.md)
- [Day 1 Complete Starter Guide](se-day-1-complete-starter-guide.md)
