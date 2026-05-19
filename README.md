# 🧠 SE Brain

An **LLM-powered personal wiki system** that turns scattered web research into a structured, interlinked, citation-grounded knowledge base — entirely managed by an AI agent inside VS Code.

## Quick Start

```bash
git clone <this-repo> se-brain
cd se-brain
code .
```

Then just start talking to GitHub Copilot. The repo ships with agent skills (in `.github/skills/`) that Copilot picks up automatically — no extra setup needed.

## What It Does

You point the AI at a topic, it researches it on the internet (or your work email), saves the raw sources, then compiles them into a richly interlinked wiki — complete with concept pages, entity profiles, comparisons, cross-references, and contradiction tracking. Every claim traces back to a source. The wiki grows incrementally as you add more sources or ask more questions.

## The Two-Layer Architecture

| Layer | Path | Ownership | Purpose |
|-------|------|-----------|---------|
| **Raw Sources** | `raw/` | Immutable (user-curated) | Markdown source files fetched from the web or work data |
| **Wiki** | `wiki/` | LLM-owned | Structured, interlinked synthesis generated from raw sources |

This separation ensures you always know what's a raw fact vs. what's a compiled analysis.

## Skills

Skills are modular instruction sets (`.github/skills/*/SKILL.md`) that teach Copilot how to perform each part of the workflow:

| Skill | What It Does | Trigger Phrases |
|-------|-------------|-----------------|
| **open-research** | Fetches sources from the internet → saves to `raw/` | "research X", "gather sources", "find papers on" |
| **wiki-generator** | Compiles raw sources into structured `wiki/` pages | "build the wiki", "ingest sources", "update wiki" |
| **query-wiki** | Answers questions from the wiki with citations | "what does the wiki say about", "compare X and Y" |
| **lint-wiki** | Health-checks the wiki (dead links, gaps, contradictions) | "lint the wiki", "health-check", "find gaps" |
| **work-research** | Gathers sources from M365 (emails, Teams, meetings) | "check work emails about", "find internal context on" |
| **html-explainer** | Converts markdown/responses to visual HTML pages | "visualize this", "make an HTML explainer" |
| **make-skill-template** | Scaffolds new custom skills | "create a skill", "scaffold a skill" |

## Typical Workflow

```
1. Research    → Fetch sources from web/work → raw/
2. Build       → Compile into wiki pages    → wiki/
3. Query       → Ask questions, get cited answers
4. File        → Save answers as analyses   → wiki/analyses/
5. Lint        → Health-check for quality issues
```

Everything compounds: new sources strengthen existing pages, answered questions become referenceable analyses, and lint runs surface gaps that drive new research.

## Core Principles

1. **Never modify `raw/`** — source files are immutable
2. **Every claim traces to a source** — no hallucinated facts
3. **Flag contradictions, don't resolve them** — show both sides, let the user decide
4. **Update incrementally** — don't regenerate the whole wiki
5. **Maintain cross-references** — backlinks, index, and links stay current
6. **Explorations compound** — filed analyses are as valuable as ingested sources

## Project Structure

```
.
├── raw/                        # Immutable source documents
│   ├── sources.md              # Manifest of all collected sources
│   ├── assets/                 # Downloaded images & binaries
│   └── *.md                    # Individual source files (YAML frontmatter)
│
├── wiki/                       # LLM-generated wiki (AI owns entirely)
│   ├── index.md                # Master catalog of all pages
│   ├── log.md                  # Append-only chronological record
│   ├── overview.md             # High-level synthesis
│   ├── sources/                # One summary per raw source
│   ├── concepts/               # Synthesized topic pages
│   ├── entities/               # People, orgs, tools, places
│   ├── comparisons/            # Side-by-side analyses
│   └── analyses/               # Filed query answers
│
├── html-files/                 # Visual HTML explainer pages
│
├── index.html                  # Visual overview of the system
│
└── .github/
    ├── copilot-instructions.md # Schema: rules, conventions, workflows
    └── skills/                 # Modular skill definitions
        ├── open-research/
        ├── work-research/
        ├── wiki-generator/
        ├── query-wiki/
        ├── lint-wiki/
        ├── html-explainer/
        └── make-skill-template/
```

## Requirements

- [VS Code](https://code.visualstudio.com/) with [GitHub Copilot](https://github.com/features/copilot)
- That's it. No dependencies to install, no build step, no runtime.

## License

Internal use.
