# SE Onboarding Assistant

An onboarding assistant for Solution Engineers that answers stage-based ramp questions like Day 1, Week 2, Month 2, tooling setup, stakeholder mapping, and manager check-ins from the knowledge captured in this repo.

The intended experience is a proper end-customer-facing onboarding product: concise, grounded answers in chat; durable knowledge in the wiki; and optional visual explainers when the user wants a portal-style walkthrough.

If a user opens this project in GitHub Copilot Desktop and types `it's my day one as an SE`, the expected response is the Day 1 roadmap, checklist, stakeholders, and links from the onboarding knowledge base in this repository.

## Quick Start

```bash
git clone <this-repo> se-brain
cd se-brain
code .
```

Then open GitHub Copilot in VS Code or GitHub Copilot Desktop and ask onboarding questions in natural language. The intended interaction is onboarding guidance first, not repo exploration.

This workspace includes a dedicated custom agent for onboarding at `.github/agents/se-onboarding.agent.md` and a seeded onboarding knowledge base in `raw/` and `wiki/`.

The root `index.html` is now an interactive SE Onboarding OS with staged guidance, linked resources, local checklist tracking, blocker notes, and wiki shortcuts.

## Recommended Usage

Treat the repo as an onboarding assistant where the engineer interacts with agents, and the agents use skills plus knowledge bases behind the scenes:

1. Open the repo in GitHub Copilot Desktop or VS Code.
2. Ask onboarding questions directly in chat, such as `it's my day one as an SE`, `help me with week 2`, or `who are the stakeholders around me`.
3. Drop onboarding docs, screenshots, spreadsheets, or work-sourced context into the workspace when you want to expand the knowledge base.
4. Let the agent use the relevant skills and update the knowledge bases for you.

The engineer-facing layer is chat with the agent. The agent-facing layers are skills and knowledge bases. The portal in `index.html` is optional and should not be required for the user to get onboarding guidance.

## Expected First-Chat Behavior

The project should interpret natural onboarding prompts directly.

- `it's my day one as an SE` -> return the Day 1 roadmap and checklist
- `help me with week 2` -> return the Week 2 technical foundations plan
- `what tools do I need first` -> return the onboarding and execution tooling map
- `who should I meet` -> return the stakeholder and pod-context guidance

It should **not** start by saying the repo is a wiki system, a research tool, or an empty canvas unless the user explicitly asks about the project structure.

It also should not narrate the retrieval mechanics with messages like `I'm pulling files` or `reviewed 4 files` when the user asked for onboarding help. The retrieval layer is internal; the answer should feel like a polished product response.

## Sample Prompts

Try these with the `SE Onboarding` agent:

- `Give me a Day 1 onboarding checklist from the current knowledge base.`
- `Create a seamless first-week plan for a new SE.`
- `Summarize the current tooling I need across onboarding, execution, learning, and support.`
- `Explain the stakeholder roles around me: manager, peers, CSA, GBB, and TSP.`
- `Turn the account coverage sample into an easy owner map.`
- `Prepare a first 30 days ramp plan and a manager check-in summary.`

For a fuller prompt pack, see [PROMPTS.md](PROMPTS.md).

## What It Does

The assistant answers onboarding questions from an existing SE onboarding knowledge base and can expand that knowledge base when new material is added. It already contains Day 1 guidance, a first-30-days ramp plan, stakeholder context, onboarding tooling, and a staged ramp playbook.

Under the hood, the setup is agent-centric: the engineer interacts with an agent, the agent invokes the right skills, and those skills read or update the knowledge bases so answers stay grounded in captured material.

## Interaction Setup

| Layer | Main Artifact | Role |
|-------|---------------|------|
| **Engineer** | Chat, prompts, uploaded context | Asks onboarding questions and provides new material |
| **Agent** | `.github/agents/` | Interprets the request, coordinates the workflow, and chooses the right skill path |
| **Skills** | `.github/skills/` | Perform research, wiki generation, querying, linting, work-data ingest, and HTML generation |
| **Knowledge Bases** | `raw/`, `wiki/`, `html-files/` | Store immutable source material, synthesized wiki pages, and derived explainers |

This keeps the engineer-facing experience simple while preserving a grounded backend knowledge layer.

## Knowledge Base Layers

| KB Layer | Path | Ownership | Purpose |
|----------|------|-----------|---------|
| **Raw Sources** | `raw/` | Immutable (user-curated) | Markdown source files fetched from the web or work data |
| **Wiki** | `wiki/` | LLM-owned | Structured, interlinked synthesis generated from raw sources |
| **HTML Explainers** | `html-files/` | LLM-owned | Visual derivatives generated from wiki pages, raw sources, or filed answers |

This separation ensures you always know what's a raw fact, what's compiled analysis, and what's a presentation layer.

## Skills

Skills are modular instruction sets (`.github/skills/*/SKILL.md`) that agents use to perform each part of the workflow:

| Skill | What It Does | Trigger Phrases |
|-------|-------------|-----------------|
| **se-open-research** | Fetches sources from the internet → saves to `raw/` | "research X", "gather sources", "find papers on" |
| **se-wiki-generator** | Compiles raw sources into structured `wiki/` pages | "build the wiki", "ingest sources", "update wiki" |
| **se-query-wiki** | Answers questions from the wiki with citations | "what does the wiki say about", "compare X and Y" |
| **se-lint-wiki** | Health-checks the wiki (dead links, gaps, contradictions) | "lint the wiki", "health-check", "find gaps" |
| **se-work-research** | Gathers sources from M365 (emails, Teams, meetings) | "check work emails about", "find internal context on" |
| **se-html-explainer** | Converts markdown/responses to visual HTML pages | "visualize this", "make an HTML explainer" |
| **se-make-skill-template** | Scaffolds new custom skills | "create a skill", "scaffold a skill" |

The customer-facing agent should know this skill surface already and choose the right path without making the user understand the underlying workflow.

## Custom Agents

The repo can also ship custom task-focused agents in `.github/agents/`.

| Agent | What It Does |
|-------|--------------|
| **SE Onboarding** | Builds and answers from a source-grounded onboarding knowledge base for solution engineers, including stages, access setup, pod mapping, account context, tooling, and onboarding Q&A. |

Use this agent when you want the engineer-to-agent interaction layer to stay simple while the agent handles skills and knowledge bases behind the scenes.

## Included Starter Knowledge Bases

This repo now includes an initial SE onboarding knowledge base to make the pattern concrete instead of purely conceptual.

- `raw/` contains onboarding source captures from the reference flow, account coverage sample, platform documentation, and tooling links.
- `wiki/` contains synthesized onboarding concepts, source summaries, stakeholder context, and reusable analyses.
- `wiki/analyses/day-1-onboarding-guide.md` and `wiki/analyses/first-30-days-ramp-plan.md` provide concrete onboarding outputs the agent can serve immediately.
- `wiki/concepts/onboarding-platform-capabilities.md`, `wiki/concepts/onboarding-tooling-and-resources.md`, and `wiki/entities/onboarding-stakeholders.md` give the agent reusable grounding for systems, tools, and people questions.
- `html-files/` can hold visual explainers derived from the wiki.
- `index.html` now acts as the end-to-end onboarding portal from Day 1 through Month 3.

## Typical Workflow

```
1. Engineer asks an agent for onboarding help
2. Agent chooses the right skill path
3. Skills read or update raw/wiki/html knowledge bases
4. Agent returns a grounded answer or creates reusable outputs
5. The knowledge bases improve for future interactions
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
├── index.html                  # Interactive onboarding portal
│
└── .github/
    ├── copilot-instructions.md # Schema: rules, conventions, workflows
    ├── agents/                 # Engineer-facing agents that orchestrate work
    └── skills/                 # Skill modules agents invoke
        ├── se-onboarding.agent.md
        ├── se-open-research/
        ├── se-work-research/
        ├── se-wiki-generator/
        ├── se-query-wiki/
        ├── se-lint-wiki/
        ├── se-html-explainer/
        └── se-make-skill-template/
```

## Requirements

- [VS Code](https://code.visualstudio.com/) with [GitHub Copilot](https://github.com/features/copilot)
- That's it. No dependencies to install, no build step, no runtime.

## Open The Portal

Open `index.html` in a browser or VS Code preview to use the onboarding system. It includes:

- stage navigation from Day 1 through Month 3
- local checklist progress tracking
- blocker notes saved in browser localStorage
- direct onboarding, execution, learning, support, and certification links
- prompt starters and links back to the repo wiki

## License

Internal use.
