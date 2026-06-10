---
name: se-query-wiki
description: 'Answer complex questions by navigating the local LLM wiki and fetching the actual data from the SharePoint raw dump. Use when asked to "query the wiki", "answer from wiki", "what does the wiki say about", "synthesize an answer", "compare X and Y", "analyze X", "summarize what we know about", or any question that should be answered from the knowledge base. Uses wiki/index.md and pages as the navigational map to identify the relevant source documents, then fetches those documents from SharePoint (wiki_read) for the real details, synthesizes a cited answer, and optionally files it back into wiki/analyses/. Always returns proper links and references. Supports markdown, comparison tables, and structured analyses.'
---

# Query Wiki

Answer questions by navigating the local wiki to find what's relevant, fetching the actual data from the SharePoint source documents it points to, and synthesizing a grounded, cited answer. The key insight: **good answers get filed back into the wiki** so your explorations compound in the knowledge base just like ingested sources do.

## Knowledge Architecture & Retrieval Discipline (read this first)

Two layers with two distinct jobs. **The wiki is the map; SharePoint is the territory.** You navigate with the wiki, then pull the actual data from SharePoint. Both steps happen on essentially every substantive answer.

| Layer | Where | Role | Access |
|-------|-------|------|--------|
| **Wiki** | **Local `wiki/`** | The **navigational layer** — overview, structure, and which source documents hold the details. Your first stop, but **not** the final source of the data you surface. | `read_file` / search local files |
| **Raw dump — shared** | SharePoint `raw/` (`microsoftapc.sharepoint.com/teams/se-brain-wiki`) | The **authoritative data layer** — the real source documents the answer's specifics come from | `wiki_read(path)` MCP tool |
| **Raw dump — private** | Local `KB-Local/` (gitignored) | The user's personal source notes (private data layer) | `grep_search` (`includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`) → `read_file` |

**The standard flow — both halves are required, not optional:**

1. **Read the local wiki first for navigation and context.** Use it to understand the topic's shape, how things connect, and — crucially — *which specific source documents on SharePoint hold the relevant details*. Treat the wiki's summaries as a guide, not as the final word on the data.
2. **Fetch the actual data from SharePoint.** For each relevant source the wiki pointed you to, `wiki_read("raw/<file>.md")` and pull the real details from the source document (plus `read_file` any cited `KB-Local/` note). **This is a normal, expected step on every data-backed answer — not a fallback.** The substantive content you surface should be grounded in these source documents, not just the wiki's compressed summary.
3. **Synthesize and cite** — combine the wiki's framing with the SharePoint source data; cite SharePoint URLs for raw sources and local relative links for wiki pages.

**Two guardrails (this is about *targeting*, not avoidance):**
- **Don't bypass the wiki.** It tells you *what* is relevant and *where* the data lives. Reaching into SharePoint blind — without first navigating via the wiki — is wrong.
- **Don't blanket-dump SharePoint.** Use the wiki's cues to fetch the *specific* documents that matter; never `wiki_search`/`wiki_list` the whole dump and return its contents wholesale. Fetch with purpose, then synthesize — don't paste raw files at the user.

## When to Use This Skill

- User asks a factual question about a topic the wiki covers
- User says "what does the wiki say about X", "summarize what we know about X"
- User asks to "compare X and Y", "analyze X", "how does X relate to Y"
- User asks a complex question requiring synthesis across multiple pages
- User asks to "file this answer", "save this to the wiki"
- Any question where the answer should be grounded in collected sources, not general knowledge

## Prerequisites

- A local `wiki/` directory with pages (produced by the **se-wiki-generator** skill)
- `wiki/index.md` — the master catalog used to find relevant pages
- The `wiki_read` MCP tool (provided by `se-graph-wiki`) for fetching specific raw documents from SharePoint when the wiki points to them
- Optionally, `KB-Local/` for the user's private source notes

## Core Principle

**The wiki navigates; SharePoint supplies the data.** The wiki is your first stop because it tells you what's relevant, how it connects, and which source documents hold the details — but the actual specifics you surface come from the SharePoint source documents the wiki points to. Read the wiki for the map and context, then fetch the relevant SharePoint raw documents for the real data, then synthesize. Fetching from SharePoint is a routine part of answering, not a last resort. The discipline is in *targeting* (let the wiki tell you which docs to pull) and *synthesizing* (never paste raw files at the user) — not in avoiding SharePoint.

## Step-by-Step Workflow

### Step 1: Understand the Question

Classify the question to determine the best answer format:

| Question Type | Example | Output Format |
|--------------|---------|---------------|
| **Factual** | "When was X introduced?" | Inline answer with citation |
| **Summary** | "What do we know about X?" | Narrative markdown with citations |
| **Comparison** | "How does X differ from Y?" | Comparison table + narrative |
| **Analysis** | "Why did X happen?" | Structured analysis page |
| **Connection** | "How does X relate to Y?" | Relationship diagram or narrative |
| **Gap** | "What don't we know about X?" | Gap analysis with suggested sources |

### Step 2: Search the Wiki Index

1. Read the local `wiki/index.md`.
2. Identify all pages potentially relevant to the question — check:
   - **Source summaries** that cover the topic
   - **Concept pages** that match the subject
   - **Entity pages** for any named entities in the question
   - **Comparison pages** if the question contrasts things
   - **Existing analyses** that may already answer or partially answer the question
3. Rank by relevance. Read the most relevant 3-5 pages first.

### Step 3: Read Relevant Wiki Pages

1. Read each relevant page fully — don't skim frontmatter alone.
2. Pay attention to:
   - **Key claims** and their source citations
   - **Contradictions** already flagged between sources
   - **Related pages** linked from each page (follow one level deep if needed)
   - **Gaps** noted in the pages ("Questions Raised" sections)
3. If the wiki pages reference concepts or entities you haven't read yet, follow those links.

### Step 4: Fetch the Relevant Data from SharePoint

Now pull the actual data. The wiki told you *which* sources matter; go read them. This is a standard step on every substantive answer — the details you surface should be grounded in the source documents, not just the wiki's summary.

1. From the relevant wiki pages' `sources:` frontmatter and inline citations, collect the source paths that hold the data the question needs (e.g. `raw/se-day-1-complete-starter-guide.md`).
2. Fetch each one:
   - Shared: `wiki_read("raw/<file>.md")` from SharePoint. Parse the returned content directly and pull the specifics (numbers, names, links, exact wording) the answer needs.
   - Private: if the wiki attributes a detail to a `KB-Local/` note, `read_file` that specific note. Never read local files outside `KB-Local/`.
3. Fetch with purpose: pull the documents the wiki pointed to, not the whole dump. If you find the wiki under-cited a relevant area, it's fine to `wiki_read` an obviously-related source — but you're still *targeting*, never list-and-dumping the entire raw folder.
4. If `wiki_read` is unavailable, tell the user the SharePoint connection is required — do not fall back to a stale local `raw/` mirror, and don't pass off the wiki's summary as the sourced answer.
5. If the wiki pointed at nothing for a needed area, note the gap and offer to enrich the wiki via **se-wiki-generator**.

### Step 5: Synthesize the Answer

Compose the answer following these rules:

1. **Ground every claim in a source.** Cite local wiki pages with relative links and raw sources with SharePoint URLs:
   - `(see [Transformer Architecture](../concepts/transformer-architecture.md))` — local wiki page
   - `(from [Attention Is All You Need](https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/raw/attention-is-all-you-need.md))` — SharePoint raw source
   - For private notes, attribute inline as "From your local notes (KB-Local)" — they are local-only and have no SharePoint URL.

2. **Present contradictions honestly.** If sources disagree:
   > Source A claims X (from [Source A](https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/raw/source-a.md)), while Source B claims Y (from [Source B](https://microsoftapc.sharepoint.com/teams/se-brain-wiki/Shared%20Documents/raw/source-b.md)). The wiki has flagged this contradiction — see [Concept Page](../concepts/concept.md#contradictions).

3. **Acknowledge gaps.** If the wiki doesn't fully cover the question:
   > The wiki doesn't currently have a dedicated page on this subtopic. Based on available sources, here's what we know: [...]. I can create a new concept page if you'd like.

4. **Don't hallucinate.** If the wiki and raw sources don't contain the answer, say so. Offer to research the topic using the **se-open-research** skill.

### Step 6: Choose the Output Format

Based on the question type from Step 1:

#### Inline Answer
For simple factual questions. Answer directly in the chat with a citation.

#### Narrative Markdown
For summaries and explanations. Structured with headings, bullet points, and citations throughout.

#### Comparison Table
For "X vs Y" questions:

```markdown
| Dimension | X | Y | Sources |
|-----------|---|---|---------|
| Feature A | ... | ... | [Source 1], [Source 2] |
| Feature B | ... | ... | [Source 3] |
| ... | ... | ... | ... |

**Summary:** Narrative comparison synthesizing the table.
```

#### Structured Analysis
For deeper "why" and "how" questions:

```markdown
## Question
[The original question]

## Short Answer
[1-2 sentence answer]

## Detailed Analysis
[Multi-paragraph analysis with citations]

## Evidence
| Claim | Supporting Sources | Confidence |
|-------|-------------------|------------|
| ... | ... | high/medium/low |

## Contradictions and Caveats
[Where sources disagree or where confidence is low]

## Related Pages
- [[link]] — how it connects
```

### Step 7: Offer to File the Answer

If the answer is **substantial and worth preserving** (more than a quick factual lookup), offer to file it:

> This analysis touches on several wiki pages. Would you like me to save it as `wiki/analyses/<slug>.md` so it becomes part of the knowledge base?

**Criteria for filing:**
- Answer required synthesizing 3+ wiki pages
- Answer reveals a new connection, pattern, or insight
- Answer is a comparison the user might want to reference later
- User explicitly asks to save it

### Step 8: File the Answer (If Accepted)

1. Save locally to `wiki/analyses/<slug>.md` with proper frontmatter (`sources:` lists the SharePoint raw paths, e.g. `raw/source1.md`, that the analysis draws on):

```yaml
---
title: "Analysis: <Question Summary>"
type: analysis
created: "2026-04-05"
updated: "2026-04-05"
sources: [raw/source1.md, raw/source2.md]
tags: [tag1, tag2]
backlinks: []
---
```

2. Update `wiki/index.md` — add the new analysis to the Analyses table.

3. Update backlinks on all pages the analysis references.

4. Append to `wiki/log.md`:
```markdown
## [2026-04-05] query | How does X relate to Y?
- Filed as: wiki/analyses/x-relates-to-y.md
- Pages referenced: wiki/concepts/x.md, wiki/concepts/y.md, wiki/entities/z.md
```

5. If the analysis revealed a gap (missing concept page, outdated entity page), note it and offer to fix it.

## Handling Edge Cases

### Question outside wiki scope
> The wiki doesn't cover this topic yet. I can research it using the **se-open-research** skill to gather sources, then build wiki pages on it. Want me to proceed?

### Wiki is empty or doesn't exist
> The wiki hasn't been built yet. Run the **se-wiki-generator** skill first to compile the wiki from raw sources, then I can answer questions against it.

### Answer contradicts itself
Never hide contradictions. Present both sides:
> There's a known contradiction in the sources on this point. [Source A] says X, [Source B] says Y. Neither has been confirmed as authoritative. See the contradiction note in [Concept Page](wiki/concepts/concept.md).

### Answer is speculative
If the sources don't directly answer but you can infer:
> The wiki sources don't directly address this, but based on [related claims], a reasonable inference is [...]. This is my synthesis, not a directly sourced claim. Confidence: low.

Mark speculative claims clearly so the user knows the difference.

## Tips

- **Navigate with the wiki, get the data from SharePoint.** Read the local wiki first for the map and context, then fetch the actual details from the SharePoint source docs it points to. Both halves run on every substantive answer — the wiki is not the final source of the data you surface.
- **Never reach into SharePoint blind, never dump it.** Don't query the raw dump without navigating via the wiki first, and don't `wiki_list`/`wiki_search` the whole dump and paste its contents. Fetch the *specific* docs the wiki cited, then synthesize.
- **Read the index, not everything.** The index is your table of contents. Don't read every wiki page for every question — use the index to find the 3-5 most relevant ones.
- **Follow backlinks.** A page's `backlinks` frontmatter tells you what other pages reference it — those are often relevant context for the question.
- **Check existing analyses first.** Someone (or you) may have already asked a similar question. Check `wiki/analyses/` before doing fresh synthesis.
- **Small answers don't need filing.** "When was X founded?" → answer inline. "How does X's approach to Y compare with Z's across these 5 dimensions?" → worth filing.
- **Always link your sources.** Every answer ends grounded: SharePoint URLs for the source docs you fetched, page titles/relative links for the wiki pages you used. No sourced answer ships without references.
- **Suggest follow-up questions.** After answering, suggest 1-2 natural follow-up questions — these help the user explore further and may lead to new filed analyses.
- **Note when the wiki needs updating.** If the wiki under-pointed for a relevant area, mention it: "The wiki's concept page on X could be enriched — want me to update it?"

## Troubleshooting

| Issue | Solution |
|-------|---------|
| `wiki/index.md` missing | The local wiki hasn't been built. Run **se-wiki-generator** first (it reads the SharePoint raw dump + KB-Local). |
| Index is stale | Run **se-lint-wiki** to check index consistency, then rebuild. |
| `wiki_read` on a raw doc fails / auth error | Tell the user the SharePoint connection is required (e.g. "run `az login`"). Answer from the wiki alone and flag the missing detail — do not fall back to a stale local `raw/` mirror. |
| Answer requires info not in any source | Say so explicitly. Don't make things up. Offer to research with **se-open-research**. |
| Too many relevant pages | Prioritize: concept pages > entity pages > source summaries. Read the most-linked pages first. |
| User wants a format you can't produce | Stay within markdown. Tables, headings, bullet points, and code blocks handle most needs. Note the limitation if the user wants something like a chart. |
