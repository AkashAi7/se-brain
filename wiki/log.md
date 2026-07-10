# Wiki Log

Append-only chronological record of wiki operations. Newest entries at the bottom.

## [2026-06-10] build | Initial wiki build
- Sources ingested: 15 (6 onboarding, 3 steady-state, 1 broadcast, 4 mock-data, 1 KB-Local private)
- Source folders: SharePoint `raw/`, `raw-steady-state/`, `broadcasts/`, `mock-data/` + local `KB-Local/` (wiki/ and wiki-steady-state/ folders deliberately excluded)
- Pages created: 38 total
  - Source summaries: 15
  - Concepts: 11 (se-onboarding-journey, staged-ramp-plan, onboarding-tooling-and-resources, onboarding-platform-capabilities, mcem-deal-execution, technical-win, workshop-and-poc-delivery, active-pipeline, customer-engagement-patterns, account-coverage-and-pod-map, se-skills-and-growth)
  - Entities: 8 (ashish-arora, onboarding-stakeholders, tata-steel, tata-sons, tata-agratas, mahindra, azure-ai-foundry, microsoft-sales-tools)
  - Comparisons: 1 (azure-vs-aws)
  - Analyses: 4 (day-1-onboarding-guide, first-30-days-ramp-plan, pipeline-health-snapshot, seamless-onboarding-playbook)
  - Navigation: overview.md, index.md, log.md
- KB-Local: folded in Tata Steel private call notes (Web IQ developer interest), labeled "From local notes (KB-Local)" with no SharePoint URL
- Contradictions flagged (not resolved): (1) opportunities legacy deal block vs authoritative 7-deal block; (2) skills/HOK placeholder accounts vs real Tata/Mahindra accounts; (3) onboarding coverage sample vs live accounts; (4) AWS-centric compete content vs real Google Cloud incumbent
- Hero products: Azure AI Foundry (cloud + Foundry Local + Web IQ), Voice Live APIs
- Pipeline: 7 deals / $12.65M across Tata Group + Mahindra
- Validated proof point: Voice Live = 22% conversion lift over Google Dialogflow at Mahindra Finance

## [2026-06-17] query | Azure DevOps insights governance model
- Filed as: wiki/analyses/azure-devops-insights-governance-model.md
- Referenced: local wiki operating conventions + onboarding flow/tooling source context
- Key output: landing-zone branch model, context exclusion policy, raw versioning strategy, PR-gated promotion flow

## [2026-07-09] repair | Repoint wiki citations from SharePoint to Azure DevOps
- RCA: all 32 source links pointed at the retired SharePoint dump; the 2026-07-03 raw/ restructure invalidated most cited paths; no post-migration ingest ever ran — so the fetch→ground→file-back growth loop was broken at fetch.
- Repointed wiki/index.md + 14 source-summary pages to Azure DevOps canonical URLs.
- Mapped 4 sources to new raw/ paths (day-1-starter-guide, platform-documentation, tools-full-reference, mcem-process-guide); marked 10 as legacy captures with successor pointers where they exist.
- Updated frontmatter sources: paths (legacy/ prefix for captures no longer in raw/).

## [2026-07-09] ingest | SE Onboarding Overview (Phased Journey)
- Fetched from Azure DevOps via MCP: raw/onboarding/onboarding-overview.md
- Created: wiki/sources/onboarding-overview.md
- Updated: wiki/concepts/se-onboarding-journey.md, wiki/concepts/staged-ramp-plan.md (+1 source, backlinks)
- Updated: wiki/index.md (new source row)
- First ingest from the restructured Azure DevOps raw dump — growth loop verified working. ~325 raw docs remain un-ingested; recommend a batch se-wiki-generator run (sector profiles, se-roles, process-guidelines).
