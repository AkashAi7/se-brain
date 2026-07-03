---
name: se-directory-manager
description: 'Manage the raw/ knowledge base — CRUD operations on accounts, roles, sectors, onboarding checklists, and metadata. Use when asked to "add an account", "update account profile", "add a new SE", "assign account", "update sector", "check directory", "validate directory", "add to onboarding", "update role content", "directory status", "who covers X", or any content management for the structured SE directory. Routes content to the correct subdirectory based on type and validates against metadata/system-config.json.'
---

# SE Directory Manager

Skill for managing the structured `raw/` knowledge base. Handles CRUD operations, validation, content routing, and consistency maintenance.

## When to Use This Skill

- User asks to add, update, or remove an account profile
- User asks to add a new SE to the directory
- User asks to update sector or role content
- User asks to modify onboarding checklists or phases
- User asks who covers a specific account
- User asks for directory status or validation
- User asks to update metadata mappings
- Any content management operation targeting `raw/`

## Directory Structure Reference

```
raw/
├── se-roles/             # {infra,data,software,ai}/{knowledge-base,playbooks,certifications,learning-resources}/
├── sectors/              # {bfsi,dn,ites,major-growth,manufacturing,ps}/{accounts/,sector-profile.md}
├── onboarding/           # phases/{1-5}/{checklist.json,role-track-refs.json}, mentorship/, tracker
├── product-updates/      # by-product/, filtered-views/, announcements/, impact-analysis/
├── process-guidelines/   # sops/, playbooks/scenario-playbooks/, best-practices/, quality-standards/, governance/
├── shared-resources/     # tools-and-utilities/, microsoft-101/, glossary/, templates/, competitive-intelligence/
└── metadata/             # system-config.json, role-mappings.json, sector-mappings.json, pod-mappings.json, se-directory.json, account-sector-mapping.json
```

## Operations

### 1. Add Account

**Trigger**: "add account X", "new account", "create account profile"

**Steps**:
1. Read `metadata/account-sector-mapping.json` to check if account already exists
2. Determine sector from user input or infer from context
3. Create `sectors/{sector}/accounts/{account-slug}/account-profile.md` with frontmatter
4. Update `metadata/account-sector-mapping.json` with new entry
5. Update `sectors/{sector}/sector-profile.md` account table if needed

**Template for account-profile.md**:
```yaml
---
title: "{Account Name} — Account Profile"
type: account-profile
sector: {sector}
created: "{date}"
updated: "{date}"
tags: [account, {slug}, {industry}]
---
```

### 2. Add SE to Directory

**Trigger**: "add SE", "new team member", "update SE directory"

**Steps**:
1. Read `metadata/se-directory.json`
2. Add new SE entry with alias, name, role, pod, sector
3. Update `metadata/pod-mappings.json` if pod assignment provided
4. Optionally create onboarding tracker entry in `onboarding/onboarding-tracker.json`

### 3. Update Account Team

**Trigger**: "update team for X", "assign SE to account", "change account ownership"

**Steps**:
1. Locate account profile in `sectors/{sector}/accounts/{account}/account-profile.md`
2. Update the Account Team table
3. Update `metadata/account-sector-mapping.json` if sector/pod changes

### 4. Lookup Coverage

**Trigger**: "who covers X", "account team for X", "find account"

**Steps**:
1. Search `metadata/account-sector-mapping.json` for account name
2. Read the account profile at the resolved path
3. Return team assignments and context

### 5. Validate Directory

**Trigger**: "validate directory", "check consistency", "directory health"

**Steps**:
1. Read `metadata/system-config.json` for conventions
2. Check all account-profile files have required frontmatter
3. Verify `metadata/account-sector-mapping.json` entries match actual folder structure
4. Verify `metadata/se-directory.json` entries are consistent with pod-mappings
5. Report any inconsistencies

### 6. Update Role Content

**Trigger**: "update role X", "add certification", "add playbook"

**Steps**:
1. Determine role from {infra, data, software, ai}
2. Route to correct subdirectory: knowledge-base/, playbooks/, certifications/, learning-resources/
3. Create or update the file
4. Update `metadata/role-mappings.json` if focus areas change

### 7. Update Onboarding

**Trigger**: "add to checklist", "update phase", "new onboarding task"

**Steps**:
1. Determine which phase (1-5) the task belongs to
2. Read the appropriate `phases/phase-{n}/checklist.json`
3. Add the new task with a unique ID following the `p{n}-XX` pattern
4. Update role-track-refs.json if the task is role-specific

## Conventions (from metadata/system-config.json)

- **File naming**: lowercase, hyphens, max 60 chars
- **Frontmatter**: YAML with title, type, created, updated, tags
- **Account slugs**: lowercase company name, hyphens for spaces, remove "Ltd/Pvt/Inc"
- **Dates**: ISO format (YYYY-MM-DD)
- **Cross-references**: relative paths from raw/ root

## Validation Rules

1. Every account in `metadata/account-sector-mapping.json` MUST have a corresponding folder in `sectors/{sector}/accounts/{slug}/`
2. Every SE in `metadata/se-directory.json` MUST appear in exactly one pod in `metadata/pod-mappings.json`
3. Every `checklist.json` task ID must be unique within its phase
4. All role-track-refs.json paths must point to existing directories
5. Sector profile account tables must stay in sync with actual account folders

## Error Handling

- If account already exists: inform user, offer to update instead
- If sector is ambiguous: ask user to specify from {bfsi, dn, ites, major-growth, manufacturing, ps}
- If metadata conflicts detected: flag and ask for resolution before proceeding
