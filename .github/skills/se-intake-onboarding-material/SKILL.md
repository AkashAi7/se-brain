---
name: se-intake-onboarding-material
description: 'Normalize user-provided onboarding material into clean raw sources for the SE onboarding knowledge base. Use when the user shares onboarding docs, screenshots, spreadsheets, pasted notes, transcripts, exported tables, meeting notes, or rough markdown and wants them ingested, structured, deduplicated, separated by topic, or turned into canonical raw sources. Prepares material for se-wiki-generator by writing proper frontmatter, confidence notes, file placement, and raw/sources.md updates.'
---

# Intake Onboarding Material

Turn ad hoc onboarding material into clean, durable `raw/` sources so the rest of the onboarding workflow stays reliable and low-friction.

This skill fills the gap between "the user gave me material" and "the wiki is ready to answer from it." It is the intake and normalization layer for the SE onboarding product.

## When to Use This Skill

- The user shares an onboarding document and says "ingest this", "clean this up", or "add this to the knowledge base"
- The user provides a screenshot, spreadsheet, copied notes, transcript, or rough markdown
- The user asks to separate account data from general onboarding content
- The user asks to remove duplication, structure the source set, or make the raw corpus sane
- The agent needs to convert messy user input into a canonical `raw/` source before using `se-wiki-generator`

## What This Skill Owns

- Normalize incoming material into one or more `raw/` markdown files with valid YAML frontmatter
- Place files in the right raw subfolder such as `raw/`, `raw/accounts/`, or `raw/assets/`
- Preserve confidence notes when the material is transcribed, partial, or screenshot-derived
- Keep account-specific data separate from general onboarding guidance when the content calls for it
- Update `raw/sources.md` so the manifest stays aligned with the fact layer
- Flag duplication or source overlap instead of silently blending it away

## What This Skill Does Not Own

- It does not synthesize the wiki pages themselves; hand off to `se-wiki-generator` after intake
- It does not answer onboarding questions from the raw material unless the wiki is still missing and the user explicitly needs an interim answer
- It does not overwrite authoritative raw source content except for `raw/sources.md`

## Intake Workflow

### Step 1 - Classify the Material

Decide which of these buckets the input belongs to:

- general onboarding guidance
- stage-specific guidance such as Day 1, Week 1, Week 2, or Month 2
- tooling and links
- stakeholder or pod mapping
- account coverage or customer ownership data
- platform or workflow documentation
- meeting or transcript material

If the material spans multiple buckets, split it into multiple raw sources instead of forcing one overloaded file.

### Step 2 - Assess Trust and Completeness

Mark the material clearly:

- `source_type: reference` for docs, guides, and structured notes
- `source_type: data` for spreadsheets, screenshots, tables, and account lists
- add caveats in the body when the source is partial, transcribed, lossy, or user-curated

If the source is screenshot-derived or manually transcribed, explicitly state that and capture confidence where needed.

### Step 3 - Choose File Placement

Use the smallest clean placement that preserves structure:

- `raw/` for general onboarding sources
- `raw/accounts/` for account coverage, pod ownership, and customer-specific artifacts
- `raw/assets/` for binary assets referenced by a source file

Avoid mixing account coverage material into the same source file as general onboarding guidance when they can stand on their own.

### Step 4 - Create Canonical Raw Files

Each new raw file must include YAML frontmatter:

```yaml
---
title: "Descriptive Title"
url: "user-provided://descriptive-slug"
date_retrieved: "2026-05-29"
source_type: reference | data
tags: [se-onboarding, ...]
---
```

Then write the clean markdown body:

- preserve headings, lists, and tables where they carry meaning
- remove obvious noise and duplicate boilerplate
- keep the content factual rather than prematurely synthesized
- add short caveat sections when the source is partial or inferred

### Step 5 - Check for Duplication

Before finalizing the source:

- compare it against nearby `raw/` files covering the same stage, tooling set, or stakeholder map
- keep the strongest source as the authoritative one for dense link inventories or detailed stage instructions
- avoid archiving by default unless the user wants history preserved
- if the user wants a lean corpus, delete or replace redundant material after updating references

### Step 6 - Update `raw/sources.md`

The manifest must reflect:

- active sources
- separated account data
- any purposeful substructure that improves maintenance

Use concise tags that distinguish stage guides, platform docs, tooling catalogs, and account data.

### Step 7 - Hand Off Cleanly

After intake is complete, the next step is usually:

- `se-wiki-generator` to ingest the source into the wiki
- `se-lint-wiki` if the intake changed multiple connected pages

## Output Expectations

When this skill finishes, report:

- what raw files were created, moved, split, or removed
- how `raw/sources.md` changed
- what duplication was removed or intentionally retained
- what should be handed next to `se-wiki-generator` or `se-lint-wiki`

## Quality Bar

Good intake should leave the repo in a state where:

- each raw file has a single clear role
- account data is clearly separated when appropriate
- screenshot-derived content is marked with confidence or caveats
- the raw corpus is easier to maintain than what the user originally provided
- the wiki layer can ingest the result without guessing what each source is for