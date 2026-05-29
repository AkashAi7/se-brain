---
title: "SE Onboarding Overview"
type: overview
created: "2026-05-25"
updated: "2026-05-29"
sources: [raw/se-onboarding-flow-reference.md, raw/accounts/se-account-coverage-sample.md, raw/se-onboarding-platform-documentation.md, raw/se-tools-full-reference.md, raw/se-onboarding-staged-ramp-playbook.md, raw/se-day-1-complete-starter-guide.md]
tags: [se-onboarding, onboarding, solution-engineering]
backlinks: [wiki/index.md, wiki/concepts/se-onboarding-journey.md, wiki/concepts/account-coverage-and-pod-map.md, wiki/entities/onboarding-stakeholders.md, wiki/concepts/onboarding-platform-capabilities.md, wiki/concepts/onboarding-tooling-and-resources.md, wiki/sources/se-tools-full-reference.md]
---

# SE Onboarding Overview

This wiki seed frames SE onboarding as a staged journey where the engineer interacts with an agent, and the agent uses skills plus grounded knowledge bases to provide operational account, pod, tooling, and ramp context.

## What We Know So Far

- The onboarding flow is intentionally staged from Day 1 through Ongoing, with Day 1 explicitly focused on profile hydration, access setup, pod discovery, and customer portfolio unlocks.
- The onboarding platform is designed to generate or surface wiki pages at each stage, which aligns well with this repository's raw-to-wiki model.
- A sample account coverage screenshot shows that onboarding should also help a new SE understand account ownership across SSP, SSM, Infrastructure, Data, Apps, Developer, and SEM roles.
- The platform documentation adds a broader capability model: personalized dashboards, live account intelligence, learning guidance, and workflow-driven recommendations.
- The detailed tools reference gives a concrete starter taxonomy of execution systems, onboarding dependencies, learning surfaces, and support links.
- The detailed tools reference clarifies the intended setup model: engineers interact with agents, and agents use skills plus knowledge bases to answer and improve onboarding guidance over time.
- The ramp playbook adds concrete tasks and canonical URLs from Day 1 through Month 3, including 30-60-90 checkpoints.
- The new Day 1 starter guide makes the MCAPS Onboarding Hub the explicit authoritative source and positions the Onboarding Agent as the guided entry point into that knowledge base.
- The new Day 1 starter guide also adds a practical weekly rhythm for Week 1 through Week 6, including live sessions, guided practice, and readiness checks.

## Interaction Model

- The engineer-facing layer should stay simple: ask the onboarding agent for guidance in chat.
- The authoritative content layer should begin with the MCAPS Onboarding Hub, with the agent helping the SE navigate that source of truth.
- The agent layer should orchestrate which skill to use for query, research, ingest, lint, or explainer generation.
- The knowledge-base layer should remain grounded in immutable raw sources, synthesized wiki pages, and optional HTML explainers.
- This means the setup should be understood as `Engineer -> Agent -> Skills + KBs`, not as the engineer navigating raw and wiki layers directly.

## High-Value Onboarding Questions This Wiki Should Answer

- What should a new SE complete on Day 1, Week 1, and later stages?
- Which systems gate onboarding progress?
- Who are the key stakeholder roles around an SE?
- Which accounts belong to the SE's portfolio and who owns each solution area?
- Which tools should a new SE use for onboarding versus day-to-day execution?
- Which platform capabilities are already live and which are planned?
- Where are the gaps in the onboarding source material?

## Reusable Guides Now Available

- A concrete Day 1 onboarding guide has been filed as [Analysis: Day 1 Onboarding Guide](analyses/day-1-onboarding-guide.md).
- A starter first-30-days ramp plan has been filed as [Analysis: First 30 Days Ramp Plan](analyses/first-30-days-ramp-plan.md).
- A day-wise onboarding playbook with sample agent prompts is available as [Analysis: Seamless Onboarding Playbook](analyses/seamless-onboarding-playbook.md).

These are intentionally framed as reusable onboarding outputs that can be refined as stronger internal sources are added.

## Current Gaps

- A canonical internal handbook is still missing, so some staged tasks may remain team-specific.
- The account coverage sample is partial and should be replaced or supplemented with a clean export.
- Pod definitions and role charters need explicit source documents.
- The platform document extraction is text-only and should eventually be replaced with a cleaner authored version.

## Recommended Next Ingests

- A structured onboarding handbook or platform documentation export
- A clean roster of account ownership and team mappings
- Canonical links for any remaining label-only internal systems not captured in the new playbook
- Internal M365 or WorkIQ-based material about pods, managers, and operating rhythm
- Learning plans or milestone checklists for later onboarding stages

## Related Pages

- [SE Onboarding Journey](concepts/se-onboarding-journey.md)
- [Account Coverage And Pod Map](concepts/account-coverage-and-pod-map.md)
- [Onboarding Stakeholders](entities/onboarding-stakeholders.md)
- [Onboarding Platform Capabilities](concepts/onboarding-platform-capabilities.md)
- [Onboarding Tooling And Resources](concepts/onboarding-tooling-and-resources.md)
- [Source Summary: Onboarding Flow](sources/se-onboarding-flow-reference.md)
- [Source Summary: Account Coverage Sample](sources/se-account-coverage-sample.md)
- [Source Summary: SE Tools Full Reference](sources/se-tools-full-reference.md)
- [Source Summary: Staged Ramp Playbook](sources/se-onboarding-staged-ramp-playbook.md)
- [Source Summary: Day 1 Complete Starter Guide](sources/se-day-1-complete-starter-guide.md)