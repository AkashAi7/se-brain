---
title: "Analysis: Day 1 Onboarding Guide"
type: analysis
created: "2026-05-26"
updated: "2026-05-29"
sources: [raw/se-onboarding-flow-reference.md, raw/se-onboarding-platform-documentation.md, raw/se-tools-full-reference.md, raw/se-onboarding-staged-ramp-playbook.md, raw/se-day-1-complete-starter-guide.md]
tags: [se-onboarding, day-1, access-setup, onboarding-guide]
backlinks: [wiki/index.md, wiki/overview.md, wiki/concepts/se-onboarding-journey.md, wiki/concepts/onboarding-platform-capabilities.md, wiki/concepts/onboarding-tooling-and-resources.md, wiki/entities/onboarding-stakeholders.md]
---

# Analysis: Day 1 Onboarding Guide

## Question

What should a new solution engineer do on Day 1, based on the onboarding sources currently in the wiki?

## Short Answer

Day 1 is primarily about becoming operationally reachable and context-aware: start from the authoritative MCAPS Onboarding Hub, use the Onboarding Agent to navigate the program, align with the manager, finish IT and HR readiness, get added to the team operating surfaces, confirm access dependencies, and make sure the SE has a named support network, the right insight surfaces, and a clear picture of the Week 1 rhythm.

## Detailed Analysis

The onboarding flow reference makes Day 1 explicit. It starts with login and profile hydration, then moves into an access checklist, pod discovery, and customer portfolio unlocks (from [Summary: SE Onboarding Flow & Azure DevOps Wiki Integration](../sources/se-onboarding-flow-reference.md)). This means Day 1 is not a generic welcome; it is a dependency-clearing stage.

The staged ramp playbook sharpens that guidance. It adds concrete Day 1 expectations: manager 1:1, IT setup, HR orientation, team distribution list and Teams access, and buddy or mentor assignment (from [Summary: SE Onboarding Staged Ramp Playbook](../sources/se-onboarding-staged-ramp-playbook.md)). Those details turn Day 1 into a practical checklist rather than a high-level readiness theme.

The new Day 1 starter guide makes the entry point more explicit. It says the MCAPS Onboarding Hub is the real-time authoritative source for program materials and that the MCAPS Onboarding Agent in Teams and Microsoft 365 should be used to navigate it (from [Summary: Day 1 as a Solution Engineer - Complete Starter Guide](../sources/se-day-1-complete-starter-guide.md)). That materially improves the knowledge-base model because it answers a Day 1 question the earlier sources only implied: where should the new SE trust the latest guidance to live?

The platform documentation broadens that model. It suggests the first-login experience should already be personalized around role, domain, and account context, and that the system should surface access tasks, tools, and learning recommendations rather than leaving the new SE to assemble them manually (from [Summary: SE Onboarding Platform Documentation](../sources/se-onboarding-platform-documentation.md)).

The tooling sources make the Day 1 and Week 1 operational surface more concrete. A new SE still needs to establish access or visibility for onboarding systems such as MCAPS Subscription, Managed Environment, and External Subscription, but the detailed tools reference now makes it clearer which systems deserve immediate orientation even before deep execution work starts. In particular, RAIN explains the role and incentive structure, MCEM Portal explains how deals flow, MSX is the execution surface to learn next, and the Onboarding Agent gives a weekly guide for staying on track (from [Summary: SE Tools Full Reference](../sources/se-tools-full-reference.md)). The new starter guide strengthens the insight layer around those tools by explicitly naming MSXi as the business-performance dashboard, Power BI as the reporting surface, Mint as the quota and earnings tracker, and FastTrack as a post-deal support path (from [Summary: Day 1 as a Solution Engineer - Complete Starter Guide](../sources/se-day-1-complete-starter-guide.md)). The staged ramp playbook still confirms that some setup systems such as GitHub Sales belong slightly later in the first week rather than being universal Day 1 blockers (from [Summary: SE Onboarding Staged Ramp Playbook](../sources/se-onboarding-staged-ramp-playbook.md)).

The same starter guide also fills a scheduling gap. It frames the onboarding program as a six-week, outcomes-based ramp with a stable weekly rhythm: Monday live onboarding, Tuesday through Thursday guided practice, and Friday readiness checks and community sessions. It also adds operational caveats such as 24 to 72 hour SuccessFactors propagation for training visibility and the importance of agreeing early on a fundamentals certification, study blocks, job shadowing, and study circles (from [Summary: Day 1 as a Solution Engineer - Complete Starter Guide](../sources/se-day-1-complete-starter-guide.md)).

## Recommended Day 1 Checklist

1. Meet the manager to align on role expectations, team norms, and success metrics.
2. Open the MCAPS Onboarding Hub and verify the Onboarding Agent is your default navigation surface for the program.
3. Finish laptop, MFA, VPN, and corporate app setup for Outlook, Teams, OneDrive, and SharePoint.
4. Complete HR orientation items covering benefits, payroll, leave policy, and code of conduct.
5. Check SuccessFactors Learning and Outlook calendar invites for Week 1 live sessions, while accounting for the 24 to 72 hour profile propagation window.
6. Get added to the team distribution lists, Teams channels, and SharePoint sites.
7. Confirm your buddy or mentor assignment and set a recurring cadence.
8. Confirm profile, role, and domain context in the onboarding experience.
9. Complete or verify access setup dependencies and note any blocked systems.
10. Identify pod stakeholders: manager, peers, CSA, GBB, and TSP.
11. Verify visibility into the initial customer or account portfolio.
12. Capture open blockers, missing permissions, and unknown owners in the onboarding tracker.
13. Block protected learning time for Tuesday to Thursday and agree on a Week 1 certification direction.

## Suggested Day 1 Sequence

| Time Block | Focus | Expected output |
|-----------|-------|-----------------|
| First hour | MCAPS Hub review, manager 1:1, and onboarding context | Clear understanding of the authoritative source, assigned domain, norms, and immediate setup needs |
| Midday | IT, HR, SuccessFactors, and team-surface setup | Corporate readiness, Week 1 session visibility, and access to the core collaboration surfaces |
| Early afternoon | Access, tooling, and stakeholder visibility | Submitted requests, named support network, and visibility into execution, insight, and knowledge-base tools |
| Late afternoon | Weekly rhythm setup and blocker capture | Protected study blocks, first certification direction, shadowing plan, and a short list of missing access |

## Sample Prompts For Day 1

- `Give me a simple Day 1 checklist from the onboarding wiki.`
- `What should I verify first: access, tools, or account context?`
- `Summarize Day 1 blockers I should watch for.`
- `Who are the stakeholders I should understand on Day 1?`

## Day 1 Tooling Map

| Need | Likely systems or resources |
|------|-----------------------------|
| Program source of truth | MCAPS Onboarding Hub, Onboarding Agent |
| Manager and team alignment | Manager 1:1, team channels, distribution lists, SharePoint |
| Profile and access readiness | Entra ID, IDWeb, MyAccess |
| Environment readiness | MCAPS Subscription, Managed Environment, External Subscription |
| Role and incentives orientation | RAIN, Incentive Compensation Guide, MSX Earnings |
| Deal-methodology orientation | MCEM Portal, customer-planning guidance, orchestration guidance |
| Initial execution and insight context | MSX, MSXi, Power BI, Azure Portal |
| Role ramp support | Onboarding Agent, Seismic, Role Library, Cloud Academy, Microsoft Learn |
| Week 1 rhythm and practice | SuccessFactors Learning, Experience MCAPS, Study Circles, MCAPS job shadowing |
| Support and escalation | TechWeb, GetHelp |

## Evidence

| Claim | Supporting Sources | Confidence |
|-------|--------------------|------------|
| Day 1 includes profile hydration, access setup, pod discovery, and customer portfolio unlocks. | [Summary: SE Onboarding Flow & Azure DevOps Wiki Integration](../sources/se-onboarding-flow-reference.md) | high |
| Day 1 should also include manager alignment, IT and HR readiness, collaboration-surface access, and mentor assignment. | [Summary: SE Onboarding Staged Ramp Playbook](../sources/se-onboarding-staged-ramp-playbook.md) | high |
| The MCAPS Onboarding Hub should act as the authoritative knowledge base and the Onboarding Agent should be used to navigate it. | [Summary: Day 1 as a Solution Engineer - Complete Starter Guide](../sources/se-day-1-complete-starter-guide.md) | medium |
| Day 1 should be personalized by role and assignment context. | [Summary: SE Onboarding Platform Documentation](../sources/se-onboarding-platform-documentation.md) | medium |
| A Day 1 guide should include environment, execution, learning, and support resources. | [Summary: SE Tools Full Reference](../sources/se-tools-full-reference.md) | high |
| Day 1 and Week 1 should establish the weekly onboarding rhythm, learning blocks, and certification/shadowing setup. | [Summary: Day 1 as a Solution Engineer - Complete Starter Guide](../sources/se-day-1-complete-starter-guide.md) | high |
| Week 1 should begin with role orientation, then deal methodology, then execution familiarity. | [Summary: SE Tools Full Reference](../sources/se-tools-full-reference.md) | high |

## Contradictions And Caveats

- The exact Day 1 completion criteria are still not formally sourced from a canonical internal handbook.
- Some tasks may be team-specific, especially around HR orientation sequencing and buddy assignment.
- Some platform features described in the documentation may be aspirational or only partially implemented.

## Related Pages

- [SE Onboarding Journey](../concepts/se-onboarding-journey.md)
- [Onboarding Platform Capabilities](../concepts/onboarding-platform-capabilities.md)
- [Onboarding Tooling And Resources](../concepts/onboarding-tooling-and-resources.md)
- [Onboarding Stakeholders](../entities/onboarding-stakeholders.md)