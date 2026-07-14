---
title: "Summary: Hours-of-Knowledge Log Data (hok-log.json)"
type: source-summary
created: "2026-06-10"
updated: "2026-06-10"
sources: [legacy/mock-data/hok-log.json]
tags: [activity-log, time-tracking, effort, data]
backlinks: [wiki/entities/ashish-arora.md, wiki/concepts/active-pipeline.md]
---

# Hours-of-Knowledge Log Data (hok-log.json)

> Source: structured mock data | Legacy capture — not present in the current Azure DevOps raw/ dump | Type: data

## Key Takeaways

- An activity log of SE technical effort by account, date, category, and hours.
- Categorized work: prototype, architecture, demo, workshop, research, enablement, blocker.
- Heavily weighted to **Tata Steel** (9 entries, ~37 hrs Apr-Jun 2026), with two **Contoso Financial** entries.

## Detailed Summary

The log captures where hands-on SE time went. For Tata Steel, the trail runs from an AI Companion integration demo (Apr 15) through BigQuery federation research, 3-IQ architecture design, a coexistence narrative pitch to Soummo, an AI strategy workshop, a Foundry Local inference POC (8 hrs, the single largest entry), Edge TPU compete research, and workshop-deck architecture refinement — directly tracing the build-up behind opportunities OPP-2026-0301 and OPP-2026-0302.

| Account | Entries | Approx hours |
|---------|---------|--------------|
| Tata Steel | 9 | ~37 |
| Contoso Financial | 2 | ~9 |

> **⚠ Caveat (flagged):** The two **Contoso Financial** entries reference an account not present in [accounts.json](accounts-data.md) (which covers Tata/Mahindra). Contoso also appears in the [skills & growth data](skills-and-growth-data.md) as a placeholder account. Treat Contoso entries as sample/placeholder data.

## Notable Claims

| Claim | Confidence | Corroborated By | Contradicted By |
|-------|-----------|-----------------|-----------------|
| Tata Steel Foundry Local POC took ~8 hrs of build | High | [Opportunities Data](opportunities-data.md) (OPP-2026-0302) | — |
| Effort traces directly to live opportunities | High | [Active Pipeline](../concepts/active-pipeline.md) | — |
| Contoso Financial is an active account | Low | — | [Accounts Data](accounts-data.md) (not listed) |

## Entities Mentioned

- [Ashish Arora](../entities/ashish-arora.md) (implied owner), [Tata Steel](../entities/tata-steel.md), [Azure AI Foundry](../entities/azure-ai-foundry.md) (Foundry Local).

## Concepts Touched

- [Active Pipeline](../concepts/active-pipeline.md) — effort behind the deals.

## Questions Raised

- Is the HOK log a single-SE log (Ashish Arora) or shared? The schema does not name the contributor.
