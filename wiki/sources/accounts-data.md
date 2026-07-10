---
title: "Summary: Account Portfolio Data (accounts.json)"
type: source-summary
created: "2026-06-10"
updated: "2026-06-10"
sources: [mock-data/accounts.json]
tags: [accounts, portfolio, tata, mahindra, india-enterprise, data]
backlinks: [wiki/concepts/account-coverage-and-pod-map.md, wiki/entities/tata-steel.md, wiki/entities/mahindra.md, wiki/entities/tata-sons.md, wiki/entities/tata-agratas.md]
---

# Account Portfolio Data (accounts.json)

> Source: structured mock data | Legacy capture — see [raw/metadata/](https://dev.azure.com/SE-Brain-AzDev/SE-Brain/_git/SE-Brain?path=/raw/metadata) and sector account profiles | Type: data

## Key Takeaways

- Four enterprise accounts in the **India Enterprise — Tata Group & Mahindra** territory, all owned by SE **Ashish Arora**.
- Every account has M365 and Entra deployed and a meaningful Azure consumption run-rate; all carry a **competitive footprint** (predominantly **Google Cloud**, some AWS).
- Strategic theme across the portfolio: **multi-cloud opening, AI-first strategy, and displacement of incumbent Google stacks**.

## Detailed Summary

| Account | Industry | Azure/mo | Primary Compete | Health |
|---------|----------|----------|-----------------|--------|
| [Tata Steel](../entities/tata-steel.md) | Steel & Manufacturing | $120K | Google Cloud (BigQuery, GKE, Vertex, Looker) | strong-and-growing |
| [Mahindra](../entities/mahindra.md) | Financial Services & Hospitality | $85K | Google (loan pipeline, Dialogflow) + some AWS | strong |
| [Tata Sons](../entities/tata-sons.md) | Conglomerate Holding | $65K | Mixed group-company GCP/AWS | excellent |
| [Tata Agratas](../entities/tata-agratas.md) | Battery Manufacturing & Energy | $40K | Some AWS IoT, Siemens MindSphere | excellent |

Each record carries recent signals (engagement, usage, strategic, news), strategic priorities, India context, and the full account team (AE, SE, CSAM, GBB). Recurring account team members: AEs Sneha Kapoor and Arjun Reddy, CSAMs Pooja Sharma and Rahul Mehta, GBB Karthik Raman (AI specialist). Common hero products across the portfolio are **Azure AI Foundry** and **Azure AI Foundry Local**.

## Notable Claims

| Claim | Confidence | Corroborated By | Contradicted By |
|-------|-----------|-----------------|-----------------|
| All four accounts owned by Ashish Arora | High | [Opportunities Data](opportunities-data.md), [HOK Log Data](hok-log-data.md) | — |
| Tata Steel is traditionally a Google account opening to Microsoft | High | [Opportunities Data](opportunities-data.md) (OPP-2026-0301 notes) | — |
| Tata Group success creates a "lighthouse effect" across 30+ companies | Medium (single source) | — | — |

## Entities Mentioned

- [Tata Steel](../entities/tata-steel.md), [Mahindra](../entities/mahindra.md), [Tata Sons](../entities/tata-sons.md), [Tata Agratas](../entities/tata-agratas.md), [Ashish Arora](../entities/ashish-arora.md), [Azure AI Foundry](../entities/azure-ai-foundry.md).

## Concepts Touched

- [Account Coverage and Pod Map](../concepts/account-coverage-and-pod-map.md) — portfolio and team structure.
- [Active Pipeline](../concepts/active-pipeline.md) — opportunities per account.

## Questions Raised

- The onboarding-era [coverage sample](se-account-coverage-sample.md) lists a different (non-Tata) account set — which reflects the current live territory?
