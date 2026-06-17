---
title: "Why we let an LLM manage the wiki"
date: 2026-06-17
category: Concept
description: "The idea behind SE Brain — a self-maintained, source-cited wiki an agent navigates, instead of a vector store it gropes around in."
tags: [llm-wiki, knowledge-management, agents, se-brain]
---

Every Solutions Engineer is sitting on a pile of knowledge: a shared SharePoint
dump, scattered personal notes, half-remembered answers from a deal six months
ago, and whatever the last enablement session covered. The problem was never a
lack of information. It was that nothing **connected** it.

SE Brain's answer is a little unusual: instead of indexing everything into a
vector store and hoping similarity search does the rest, we let an LLM
**maintain a wiki** — a synthesized, interlinked, source-cited layer that sits
on top of the raw sources. This post is about why.

## Recall is not navigation

The default move for "agent memory" is a vector database. Embeddings are easy to
add and genuinely good at fuzzy recall. But recall is not the same as
**navigation**.

A vector store answers *"what looks similar to this query?"* What an SE actually
needs, mid-deal, is *"what is connected to this, and how?"* Those are different
questions.

- **Recall** returns a bag of nearby chunks.
- **Navigation** returns a path: this account → owns → this opportunity →
  competes against → this rival → countered by → this proof point.

A wiki is built for the second question. The links *are* the reasoning.

## The wiki is the map; the raw dump is the data

SE Brain keeps two layers deliberately separate:

1. A **raw source dump** on SharePoint — the authoritative, immutable
   documents. Plus an optional private `KB-Local/` layer for your own notes.
2. A **local wiki** — the compiled, synthesized knowledge the agent (and you)
   actually browse.

The agent always reads the wiki *first* to get oriented, then fetches the
specific raw documents the wiki points to for the real details. The wiki is the
index; the sources are the source of truth.

> The graph of links is the index. The raw documents are the ground truth.
> Synthesis lives in between, and it always cites both.

## A page is just Markdown

Every node in the wiki is a plain Markdown file with YAML frontmatter:

```yaml
---
title: "MCEM Deal Execution"
type: concept
sources: [raw/mcem-deal-execution-framework.md]
tags: [sales-process, qualification]
backlinks: [wiki/concepts/technical-win.md]
---
The MCEM framework structures a deal across five stages. Links to the
technical-win motion and the active-pipeline view.
```

That single choice buys a lot:

- It is **human-readable** — you can audit every claim and link by eye.
- It is **diffable** — every change shows up in a pull request.
- It is **portable** — it is just files; no runtime, no SDK, no lock-in.

## Why an LLM should be the one maintaining it

Wikis rot. People stop updating them, links break, two pages quietly start
contradicting each other, and within a quarter nobody trusts it. The reason SE
Brain works is that the **upkeep is the agent's job**, not yours:

- When new sources land, it **ingests incrementally** — updating existing pages
  in place instead of rebuilding from scratch.
- It maintains **cross-references and backlinks** so the graph stays connected.
- It **flags contradictions instead of silently resolving them** — when two
  sources disagree, it shows both sides with citations and lets you decide.
- It **lints** the wiki for orphan pages, dead links, stale content, and
  coverage gaps.

## The rules that keep it trustworthy

An LLM-maintained wiki is only useful if you can trust it. So the agent works
under a few hard constraints:

1. **Every claim traces to a source.** No source, no claim.
2. **Navigate the wiki, then fetch the real data.** Never answer from the
   compressed summary alone.
3. **Shared truth wins conflicts**, and local notes are always labelled as
   yours.
4. **Explorations compound** — a good answer gets filed back as an analysis, so
   the next question starts further ahead.

That last point is the quiet superpower. Every question you ask doesn't just get
answered — it makes the brain a little bigger. A vector store forgets the moment
the context window closes. A wiki remembers, because the answer becomes a page.

## The takeaway

SE Brain isn't trying to be a smarter search box. It's trying to be a **brain** —
a navigable, source-cited, self-maintaining knowledge layer that spans the whole
SE journey and gets sharper every time you use it. An LLM manages the wiki so you
don't have to, and so it never goes stale.

That's the whole idea. The rest is just files.
