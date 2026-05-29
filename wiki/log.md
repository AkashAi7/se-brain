# Wiki Log

## [2026-05-25] build | Initial SE onboarding seed
- Created: wiki/index.md
- Created: wiki/overview.md
- Created: wiki/sources/se-onboarding-flow-reference.md
- Created: wiki/sources/se-account-coverage-sample.md
- Created: wiki/concepts/se-onboarding-journey.md
- Created: wiki/concepts/account-coverage-and-pod-map.md
- Created: wiki/entities/onboarding-stakeholders.md
- Sources ingested: 2
- Pages created: 7

## [2026-05-26] ingest | Additional onboarding sources
- Created: raw/se-onboarding-platform-documentation.md
- Created: raw/se-tooling-links.md
- Created: wiki/sources/se-onboarding-platform-documentation.md
- Created: wiki/sources/se-tooling-links.md
- Created: wiki/concepts/onboarding-platform-capabilities.md
- Created: wiki/concepts/onboarding-tooling-and-resources.md
- Updated: wiki/index.md, wiki/overview.md
- Sources ingested: 2
- Pages created: 4

## [2026-05-26] query | Day 1 and first 30 days onboarding plans
- Filed as: wiki/analyses/day-1-onboarding-guide.md
- Filed as: wiki/analyses/first-30-days-ramp-plan.md
- Pages referenced: wiki/concepts/se-onboarding-journey.md, wiki/concepts/account-coverage-and-pod-map.md, wiki/concepts/onboarding-platform-capabilities.md, wiki/concepts/onboarding-tooling-and-resources.md, wiki/entities/onboarding-stakeholders.md

## [2026-05-26] query | Seamless day-wise onboarding playbook
- Filed as: wiki/analyses/seamless-onboarding-playbook.md
- Updated: wiki/analyses/day-1-onboarding-guide.md, wiki/analyses/first-30-days-ramp-plan.md
- Pages referenced: wiki/concepts/se-onboarding-journey.md, wiki/concepts/account-coverage-and-pod-map.md, wiki/concepts/onboarding-platform-capabilities.md, wiki/concepts/onboarding-tooling-and-resources.md, wiki/entities/onboarding-stakeholders.md

## [2026-05-26] ingest | SE onboarding ramp playbook and links
- Created: raw/se-onboarding-ramp-playbook.md
- Created: wiki/sources/se-onboarding-ramp-playbook.md
- Updated: wiki/concepts/se-onboarding-journey.md, wiki/concepts/onboarding-tooling-and-resources.md, wiki/entities/onboarding-stakeholders.md
- Updated: wiki/analyses/day-1-onboarding-guide.md, wiki/analyses/first-30-days-ramp-plan.md
- Updated: wiki/index.md, wiki/overview.md, raw/sources.md
- Pages touched: 9

## [2026-05-29] ingest | Expanded SE tools and expertise materials
- Created: raw/se-tools-full-reference.md
- Created: wiki/sources/se-tools-full-reference.md
- Updated: wiki/sources/se-tooling-links.md
- Updated: wiki/concepts/onboarding-tooling-and-resources.md
- Updated: wiki/analyses/day-1-onboarding-guide.md, wiki/analyses/first-30-days-ramp-plan.md
- Updated: wiki/index.md, raw/sources.md
- Pages touched: 8

## [2026-05-29] ingest | Day 1 complete starter guide
- Created: raw/se-day-1-complete-starter-guide.md
- Created: wiki/sources/se-day-1-complete-starter-guide.md
- Updated: wiki/concepts/onboarding-tooling-and-resources.md
- Updated: wiki/analyses/day-1-onboarding-guide.md
- Updated: wiki/index.md, raw/sources.md
- Pages touched: 6

## [2026-05-29] query | Propagated Day 1 starter guide into onboarding syntheses
- Updated: wiki/analyses/day-1-onboarding-guide.md, wiki/analyses/seamless-onboarding-playbook.md
- Cross-referenced: wiki/concepts/onboarding-tooling-and-resources.md

## [2026-05-29] maintenance | Repository cleanup and quality fixes
- Deleted 7 empty junk skill folders: html-explainer/, lint-wiki/, make-skill-template/, open-research/, query-wiki/, wiki-generator/, work-research/
- Created: raw/assets/ (missing folder referenced in docs)
- Created: html-files/index.html (catalog page for HTML explainers)
- Issues identified: instruction duplication across AGENTS.md, copilot-instructions.md, and se-onboarding.agent.md (noted for future consolidation)
- Updated: wiki/overview.md
- Updated: wiki/analyses/first-30-days-ramp-plan.md
- Updated: wiki/concepts/se-onboarding-journey.md
- Updated: wiki/entities/onboarding-stakeholders.md
- Updated: wiki/concepts/onboarding-tooling-and-resources.md
- Pages touched: 5

## [2026-05-29] lint | Raw source sanity check and restructure
- **Duplication analysis completed across 7 raw sources**
- Created: raw/accounts/ subfolder for account-specific data
- Moved: se-account-coverage-sample.md → raw/accounts/ (account data separated as requested)
- Created: raw/archive/ subfolder for deprecated sources
- Archived: se-tooling-links.md → raw/archive/ (superseded by se-tools-full-reference.md)
- Updated: raw/sources.md manifest with new structure
- **Findings:**
  - Tool URLs appeared in 4 files; se-tools-full-reference.md is the authoritative source (50+ links vs 13)
  - Day 1 content appeared in 3 files; se-day-1-complete-starter-guide.md is the most comprehensive
  - Account coverage data now isolated for separate maintenance
- Active sources reduced from 7 to 5 + 1 account data + 1 archived

## [2026-05-29] maintenance | Removed deprecated tooling source
- Deleted: raw/archive/se-tooling-links.md
- Deleted: wiki/sources/archive/se-tooling-links.md
- Updated: raw/sources.md, wiki/index.md
- Updated references: wiki/overview.md, wiki/concepts/onboarding-tooling-and-resources.md, wiki/analyses/day-1-onboarding-guide.md, wiki/analyses/first-30-days-ramp-plan.md, wiki/analyses/seamless-onboarding-playbook.md
- Fixed source paths to raw/accounts/se-account-coverage-sample.md across dependent wiki pages

## [2026-05-29] maintenance | Reduced overlap across active raw sources
- Tightened: raw/se-onboarding-platform-documentation.md to focus on platform capability model instead of duplicating task lists
- Tightened: raw/se-onboarding-ramp-playbook.md to keep staged ramp content only
- Tightened: raw/se-day-1-complete-starter-guide.md to keep Day 1 operational guidance only
- Updated: raw/sources.md tags to reflect the clarified roles of the active sources

## [2026-05-29] maintenance | Renamed staged ramp source for clarity
- Renamed: raw/se-onboarding-ramp-playbook.md -> raw/se-onboarding-staged-ramp-playbook.md
- Renamed: wiki/sources/se-onboarding-ramp-playbook.md -> wiki/sources/se-onboarding-staged-ramp-playbook.md
- Updated references across raw manifest, wiki index, overview, concepts, entities, and analyses