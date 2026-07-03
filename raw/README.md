# Raw SE Directory

> Structured knowledge base for Microsoft Solution Engineers.

## Purpose

This directory organizes SE operational knowledge into a discoverable, role-aware, sector-aware structure that supports onboarding, daily execution, and continuous learning.

## Structure

```
raw/
├── se-roles/             # Role-specific knowledge (infra, data, software, ai)
├── sectors/              # Sector-specific content (bfsi, dn, ites, major-growth, manufacturing, ps)
├── onboarding/           # Phased onboarding journey with checklists
├── product-updates/      # Product changes and SE impact analysis
├── process-guidelines/   # SOPs, playbooks, best practices, governance
├── shared-resources/     # Tools, glossary, templates, Microsoft 101
└── metadata/             # System config, mappings, directory data
```

## Quick Start

| I need... | Go to... |
|-----------|----------|
| Day 1 guide | `onboarding/phases/phase-1-orientation/day-1-starter-guide.md` |
| Tool URLs | `shared-resources/tools-and-utilities/se-tools-full-reference.md` |
| My role track | `se-roles/{your-role}/knowledge-base/README.md` |
| Account info | `sectors/{your-sector}/accounts/{account-name}/` |
| Certifications | `se-roles/{your-role}/certifications/` |
| Glossary | `shared-resources/glossary/glossary.md` |
| Process/SOP | `process-guidelines/` |

## Conventions

- **File naming**: lowercase, hyphens, max 60 chars (e.g., `day-1-starter-guide.md`)
- **Frontmatter**: YAML with title, type, created, updated, tags
- **Cross-references**: relative paths from this directory root
- **Metadata**: JSON files in `metadata/` for machine-readable mappings

## Maintenance

Content is maintained by the SE Brain agent system. The `se-directory-manager` skill handles CRUD operations, validation, and content routing.
