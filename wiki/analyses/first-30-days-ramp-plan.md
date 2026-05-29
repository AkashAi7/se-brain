---
title: "Analysis: First 30 Days Ramp Plan"
type: analysis
created: "2026-05-26"
updated: "2026-05-29"
sources: [raw/se-onboarding-flow-reference.md, raw/se-onboarding-platform-documentation.md, raw/accounts/se-account-coverage-sample.md, raw/se-tools-full-reference.md, raw/se-onboarding-staged-ramp-playbook.md, raw/se-day-1-complete-starter-guide.md]
tags: [se-onboarding, ramp-plan, first-30-days, week-1]
backlinks: [wiki/index.md, wiki/overview.md, wiki/concepts/se-onboarding-journey.md, wiki/concepts/account-coverage-and-pod-map.md, wiki/concepts/onboarding-platform-capabilities.md, wiki/concepts/onboarding-tooling-and-resources.md, wiki/entities/onboarding-stakeholders.md]
---

# Analysis: First 30 Days Ramp Plan

## Question

Given the current onboarding sources, what is a practical first-30-days ramp plan for a new SE?

## Short Answer

The first 30 days should move in four layers: Day 1 welcome and access readiness, Days 2-5 org and onboarding task completion, Weeks 2-3 technical foundations, and Week 4 customer-execution readiness with shadowing and deal review. The newer Day 1 field guide also makes the Week 1 rhythm explicit, so the first month now has a stronger operational cadence instead of only a staged outline.

## Detailed Analysis

The visible onboarding flow explicitly defines a multi-stage structure: Day 1, Week 1, Week 2, Week 3-4, Month 2, and Ongoing (from [Summary: SE Onboarding Flow & Azure DevOps Wiki Integration](../sources/se-onboarding-flow-reference.md)). The staged ramp playbook now adds concrete staged content through Month 3, which makes the first 30 days much less inferential (from [Summary: SE Onboarding Staged Ramp Playbook](../sources/se-onboarding-staged-ramp-playbook.md)).

The new Day 1 starter guide strengthens the first-week operating model. It names the MCAPS Onboarding Hub as the authoritative source for schedules and resources, positions the Onboarding Agent as the primary navigation layer, and defines a weekly rhythm of Monday live sessions, Tuesday through Thursday guided practice, and Friday readiness checks (from [Summary: Day 1 as a Solution Engineer - Complete Starter Guide](../sources/se-day-1-complete-starter-guide.md)). That turns Week 1 into a more concrete operating cadence instead of a loose transition period.

The platform document suggests a steady transition from setup to active account engagement. It references account insights, dynamic tooling, relationship-building, shadowing, first customer meetings, and a 30-day manager check-in. These are strong signals for how the first 30 days should be structured (from [Summary: SE Onboarding Platform Documentation](../sources/se-onboarding-platform-documentation.md)).

The account coverage sample adds a practical dimension: by the time a new SE is beyond Day 1, they need to understand who owns what around real customer accounts. That turns the ramp plan from abstract enablement into role- and account-specific navigation (from [Summary: SE Account Coverage Snapshot Sample](../sources/se-account-coverage-sample.md)).

## Suggested 30-Day Ramp Structure

### Day 1

- Start with the MCAPS Onboarding Hub and confirm the Onboarding Agent is the default guide for Week 1 content.
- Hold the manager 1:1 and align on role expectations, norms, and success metrics.
- Complete laptop, MFA, VPN, and corporate-app readiness.
- Complete HR basics and get added to team collaboration surfaces.
- Check SuccessFactors and Outlook for live-session enrollment, allowing for the profile propagation delay.
- Confirm buddy or mentor support.

### Days 2-3

- Review Microsoft culture and growth mindset material.
- Understand the org structure, skip-level, and broader business unit.
- Review the prior quarter's team OKRs and current priorities.
- Meet the immediate team in short introduction meetings.
- Use RAIN to understand role expectations, plan details, and compensation context.
- Review MCEM Portal so the deal flow and orchestration model are clear early.

### Days 4-5

- Request MCAPS Azure Subscription and join the Managed Environment.
- Request the external tenant and Azure subscription if needed.
- Complete GitHub Sales onboarding.
- Review the SE charter and understand the sales motion across AE, SSP, CSA, and TSP.
- Open MSX and walk through the opportunity, forecast, close, and milestones guides.
- Use the Onboarding Agent to keep the first-week sequence and skilling plan current.
- Block protected learning time, agree on the initial certification target, and line up job shadowing and Study Circles.

### Weeks 2-3

- Complete core cloud-stack learning across Azure, M365, Entra ID, Purview, Defender, Power Platform, and Copilot Studio.
- Use Seismic, Cloud Academy, Microsoft Learn, and Role Library as the main learning surfaces.
- Run hands-on labs through Azure Portal, sandbox resources, and architecture guidance.

### Week 4

- Get hands-on with MSX, MSXi, Power BI, and Azure Portal.
- Shadow 3-5 customer meetings across discovery, demo, and workshop formats.
- Review 2-3 closed deals in MSX, including architecture and post-mortem material.
- Use Cloud Adoption Framework, Well-Architected, and licensing references to ground customer conversations.

### Day 30 checkpoint

- Hold the manager feedback session.
- Confirm current strengths, skill gaps, and the Month 2 focus areas.

## Sample Prompts For The First 30 Days

- `Create a week-by-week ramp plan from the onboarding knowledge base.`
- `What should I accomplish by the end of week 1 as a new SE?`
- `Turn the account coverage source into a week 2 account-learning plan.`
- `Help me prepare a 30-day check-in summary for my manager.`

## Evidence

| Claim | Supporting Sources | Confidence |
|-------|--------------------|------------|
| The onboarding model is stage-based beyond Day 1. | [Summary: SE Onboarding Flow & Azure DevOps Wiki Integration](../sources/se-onboarding-flow-reference.md) | medium |
| The first 30 days can be mapped into welcome, org setup, access completion, technical foundations, and execution readiness. | [Summary: SE Onboarding Staged Ramp Playbook](../sources/se-onboarding-staged-ramp-playbook.md) | high |
| Week 1 has an explicit operating cadence and protected learning model, not just a set of tasks. | [Summary: Day 1 as a Solution Engineer - Complete Starter Guide](../sources/se-day-1-complete-starter-guide.md) | high |
| The first month should include account insight, relationship-building, shadowing, and a manager check-in. | [Summary: SE Onboarding Platform Documentation](../sources/se-onboarding-platform-documentation.md) | medium |
| Account ownership understanding is necessary for meaningful ramp. | [Summary: SE Account Coverage Snapshot Sample](../sources/se-account-coverage-sample.md) | medium |
| The tooling surface spans onboarding, execution, learning, and support. | [Summary: SE Tools Full Reference](../sources/se-tools-full-reference.md) | high |

## Contradictions And Caveats

- The staged playbook is user-provided and may still need validation against a canonical internal handbook.
- The ownership sample is partial and should not be treated as authoritative.
- Some platform document phrases were extracted from a lossy Office conversion.

## Related Pages

- [SE Onboarding Journey](../concepts/se-onboarding-journey.md)
- [Account Coverage And Pod Map](../concepts/account-coverage-and-pod-map.md)
- [Onboarding Platform Capabilities](../concepts/onboarding-platform-capabilities.md)
- [Onboarding Tooling And Resources](../concepts/onboarding-tooling-and-resources.md)