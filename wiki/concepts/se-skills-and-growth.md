---
title: "SE Skills and Growth Model"
type: concept
created: "2026-06-10"
updated: "2026-06-10"
sources: [mock-data/skills-and-growth.json, raw/se-onboarding-staged-ramp-playbook.md, raw/se-onboarding-platform-documentation.md]
tags: [skills, certifications, growth, role-transition, learning]
backlinks: [wiki/sources/skills-and-growth-data.md, wiki/sources/se-onboarding-staged-ramp-playbook.md, wiki/entities/ashish-arora.md, wiki/concepts/staged-ramp-plan.md]
---

# SE Skills and Growth Model

## Definition

The framework for how an SE builds and tracks capability — a **skills matrix** across solution areas, a **certification roadmap**, and structured **role-transition paths** for SEs moving between specialties (from [Skills & Growth Data](../sources/skills-and-growth-data.md)).

## Key Points

- **Skills matrix** spans AI/ML, Infrastructure, Data & Analytics, Security, and Soft Skills, each capability rated by proficiency (beginner → expert) with last-practiced date and notes.
- **Certification roadmap:** completed (AZ-104, AZ-500, AZ-305, AI-900); in progress (AI-102, 45%); recommended next (AI-102, DP-600, SC-200, AI-050).
- **Three role-transition paths**, each with phased foundations/depth/execution and "what transfers":
  - **Infra → AI** (4-6 months)
  - **Data → AI** (3-4 months)
  - **Security → AI** (3-5 months)
- **What transfers** is explicit — e.g. an Infra SE's networking, security, and cost-optimization skills carry directly into AI service architecture.
- This is the **execution-phase analog** of the onboarding [staged ramp plan](staged-ramp-plan.md): the ramp builds a new hire; transition paths re-skill an existing SE.

## Role Transition Paths

| From → To | Duration | Phase 1 | Phase 3 milestone |
|-----------|----------|---------|-------------------|
| Infrastructure → AI | 4-6 mo | AI-900, OpenAI basics, RAG overview | First independent AI technical win |
| Data & Analytics → AI | 3-4 mo | LLM fundamentals, embeddings, RAG | First AI deal closed (not just data) |
| Security → AI | 3-5 mo | LLM with security lens, Responsible AI | Compete win vs pure-play AI vendor |

## How Sources Relate to This Concept

| Source | Perspective | Key Contribution |
|--------|------------|-----------------|
| [Skills & Growth Data](../sources/skills-and-growth-data.md) | Profile + paths | Skills matrix, certifications, role-transition playbooks |
| [Staged Ramp Playbook](../sources/se-onboarding-staged-ramp-playbook.md) | Onboarding analog | Certification targets and ramp milestones |
| [Platform Documentation](../sources/se-onboarding-platform-documentation.md) | Platform view | Skilling/certification integrated into the platform |

## Contradictions and Open Questions

- **⚠ Placeholder accounts (flagged):** the skills data's `learning_history` references Contoso, WingTip, Adventure Works, Northwind, and Fabrikam — none in the live [accounts data](../sources/accounts-data.md). The skills *structure* is reliable; the account names are sample data. See [Skills & Growth Data](../sources/skills-and-growth-data.md).
- Whether the profile is specifically [Ashish Arora](../entities/ashish-arora.md)'s or a generic exemplar is ambiguous (tenure and AI focus match, but placeholder notes blur it).

## Related Concepts

- [Staged Ramp Plan](staged-ramp-plan.md) — onboarding analog.
- [SE Onboarding Journey](se-onboarding-journey.md) — where skilling begins.
- [Customer Engagement Patterns](customer-engagement-patterns.md) — compete skills applied.

## Related Entities

- [Ashish Arora](../entities/ashish-arora.md) — the profiled AI/ML SE (ex-Infrastructure).
- [Azure AI Foundry](../entities/azure-ai-foundry.md) — focus of current upskilling.
