---
title: "Summary: Skills and Growth Data (skills-and-growth.json)"
type: source-summary
created: "2026-06-10"
updated: "2026-06-10"
sources: [mock-data/skills-and-growth.json]
tags: [skills, certifications, growth, role-transition, data]
backlinks: [wiki/concepts/se-skills-and-growth.md, wiki/entities/ashish-arora.md]
---

# Skills and Growth Data (skills-and-growth.json)

> Source: structured mock data | Legacy capture — not present in the current Azure DevOps raw/ dump | Type: data

## Key Takeaways

- A single SE profile: **AI & Machine Learning SE**, 18 months tenure, transitioned from an **Infrastructure SE** role.
- A detailed **skills matrix** across AI/ML, Infrastructure, Data & Analytics, Security, and Soft Skills, each with proficiency, last-practiced date, and notes.
- Certifications: AZ-104, AZ-500, AZ-305, AI-900 completed; AI-102 in progress (45%); recommended next: AI-102, DP-600, SC-200, AI-050.
- Three structured **role-transition paths** (Infra→AI, Data→AI, Security→AI), each with phased foundations/depth/execution and "what transfers".

## Detailed Summary

The profile shows an SE strongest in Infrastructure (expert compute/networking, advanced Arc/migration/Terraform) who is ramping AI/ML (intermediate Azure OpenAI and RAG; beginner AI Foundry, MLOps, Responsible AI, AI Agents). This maps to the [SE Skills and Growth Model](../concepts/se-skills-and-growth.md) and explains the [account portfolio](accounts-data.md)'s AI-heavy deal mix.

The role-transition paths are reusable playbooks: Infra→AI (4-6 months), Data→AI (3-4 months), Security→AI (3-5 months), each detailing what existing skills transfer, quick wins, key labs, customer-engagement milestones, and execution milestones (e.g. "first independent AI technical win").

> **⚠ Contradiction (flagged, not resolved):** The `learning_history` and skills notes reference **placeholder accounts** — Contoso, WingTip, Adventure Works, Northwind, Fabrikam — that do **not** match the real Tata/Mahindra portfolio in [accounts.json](accounts-data.md). The skills *structure* is reliable; the **account names in the notes are sample/placeholder data** and should not be treated as live engagements.

## Notable Claims

| Claim | Confidence | Corroborated By | Contradicted By |
|-------|-----------|-----------------|-----------------|
| SE is AI/ML, 18mo tenure, ex-Infrastructure | High | — | — |
| AI-102 in progress at 45%, target 2026-07-15 | High | — | — |
| Three documented role-transition paths | High | [Staged Ramp Playbook](se-onboarding-staged-ramp-playbook.md) | — |
| Learning history accounts (Contoso, WingTip, etc.) are live | Low | — | [Accounts Data](accounts-data.md) |

## Entities Mentioned

- [Ashish Arora](../entities/ashish-arora.md) (the profiled SE), [Azure AI Foundry](../entities/azure-ai-foundry.md).

## Concepts Touched

- [SE Skills and Growth Model](../concepts/se-skills-and-growth.md) — the growth framework.
- [Staged Ramp Plan](../concepts/staged-ramp-plan.md) — onboarding analog of role transition.

## Questions Raised

- Is the profile specifically Ashish Arora's, or a generic exemplar? Tenure and AI focus match Ashish, but the placeholder account notes blur this.
