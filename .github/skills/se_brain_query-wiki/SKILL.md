---
name: se_brain_query-wiki
description: 'Answer complex questions by searching and synthesizing from the LLM wiki. Use when asked to "query the wiki", "answer from wiki", "what does the wiki say about", "synthesize an answer", "compare X and Y", "analyze X", "summarize what we know about", or any question that should be answered from the knowledge base. Searches wiki/index.md, reads relevant pages, synthesizes answers with citations, and optionally files answers back into wiki/analyses/ so insights compound over time. Supports multiple output formats: markdown, comparison tables, and structured analyses.'
---

# Query Wiki

Answer questions by searching the onboarding wiki, reading relevant pages via SharePoint, and synthesizing a grounded, cited answer. The key insight: **good answers get filed back into the wiki** so your explorations compound in the knowledge base just like ingested sources do.

**Grounding (two-tier):** All *shared* data reads MUST use the `wiki_read()` MCP tool targeting `microsoftapc.sharepoint.com/teams/se-brain-wiki`. The agent MUST NOT use `read_file`, `grep_search`, or `file_search` on the stale local mirrors `wiki/` or `raw/`. If the MCP tool is unavailable, inform the user — do not silently fall back to those mirrors.

**Optional private layer:** after grounding in SharePoint, you may also scan the user's `KB-Local/` folder for relevant personal notes. **`KB-Local/` is gitignored, so `file_search` cannot see it** — discover notes with `grep_search` (`includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`), then read with `read_file`. Fold them in only if they add value, label them "From your local notes (KB-Local)", and let SharePoint win any conflict. It augments, never substitutes — never answer from `KB-Local/` alone when SharePoint is down. Never read local files outside `KB-Local/`.

## When to Use This Skill

- User asks a factual question about a topic the onboarding wiki covers
- User says "what does the wiki say about X", "summarize what we know about X"
- User asks to "compare X and Y", "analyze X", "how does X relate to Y"
- User asks a complex question requiring synthesis across multiple pages
- User asks to "file this answer", "save this to the wiki"
- Any question where the answer should be grounded in collected sources, not general knowledge
- Onboarding questions: stage plans, tooling, platform, journey, stakeholders

## Prerequisites

- The `wiki_read` and `wiki_write` MCP tools (provided by `se-graph-wiki` server)
- Wiki content exists on SharePoint at `wiki/` path
- `wiki/index.md` — the master catalog used to find relevant pages
- For rich answers: `raw/` sources on SharePoint available as fallback

## Core Principle

**The wiki is your first stop, not `raw/`.** The wiki already contains synthesized, cross-referenced knowledge. Read wiki pages first via `wiki_read()`. Only fall back to raw sources when the wiki lacks sufficient detail. This is the whole point of maintaining a compiled wiki — you shouldn't have to re-derive knowledge from raw sources every time.

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

1. Call `wiki_read("wiki/index.md")`.
2. Identify all pages potentially relevant to the question — check:
   - **Source summaries** that cover the topic
   - **Concept pages** that match the subject
   - **Entity pages** for any named entities in the question
   - **Comparison pages** if the question contrasts things
   - **Existing analyses** that may already answer or partially answer the question
3. Rank by relevance. Read the most relevant 3-5 pages first.

### Step 3: Read Relevant Wiki Pages

1. Call `wiki_read("wiki/<path>")` for each relevant page — read fully, don't skim frontmatter alone.
2. Pay attention to:
   - **Key claims** and their source citations
   - **Contradictions** already flagged between sources
   - **Related pages** linked from each page (follow one level deep if needed)
   - **Gaps** noted in the pages ("Questions Raised" sections)
3. If the wiki pages reference concepts or entities you haven't read yet, follow those links via `wiki_read()`.

### Step 4: Fall Back to Raw Sources (If Needed)

If wiki pages lack sufficient detail:
1. Call `wiki_read("raw/sources.md")` for the manifest.
2. Call `wiki_read("raw/<source-file>.md")` for the specific raw source(s).
3. Note any gap: if you needed raw sources to answer, that's a signal the wiki needs updating.

### Step 4b: Optionally Augment from KB-Local (Private Layer)

After grounding in SharePoint, optionally check the user's private notes:
1. Discover relevant notes with `grep_search` (`includeIgnoredFiles: true`, `includePattern: "KB-Local/**"`) — `file_search` cannot see `KB-Local/` because it is gitignored.
2. Read matches with `read_file`.
3. Fold in only what adds value; if nothing is relevant, skip silently. Label any local content "From your local notes (KB-Local)" and let SharePoint win conflicts. Never read local files outside `KB-Local/`.

### Step 5: Synthesize the Answer

Compose the answer following these rules:

1. **Ground every claim in a source.** Cite wiki pages and ultimately raw sources:
   - `(see [Transformer Architecture](wiki/concepts/transformer-architecture.md))`
   - `(from [Attention Is All You Need](raw/attention-is-all-you-need.md))`
   - For private notes, attribute inline as "From your local notes (KB-Local)" — they are local-only and have no SharePoint URL.

2. **Present contradictions honestly.** If sources disagree:
   > Source A claims X (from [Source A](raw/source-a.md)), while Source B claims Y (from [Source B](raw/source-b.md)). The wiki has flagged this contradiction — see [Concept Page](wiki/concepts/concept.md#contradictions).

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

1. Save to SharePoint via `wiki_write("wiki/analyses/<slug>.md", content)` with proper frontmatter:

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

2. Update `wiki/index.md` via `wiki_write()` — add the new analysis to the Analyses table.

3. Update backlinks on all pages the analysis references via `wiki_write()`.

4. Append to `wiki/log.md` via `wiki_write()`:
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

- **Read the index, not everything.** Call `wiki_read("wiki/index.md")` first. Don't read every wiki page — use the index to find the 3-5 most relevant ones.
- **Follow backlinks.** A page's `backlinks` frontmatter tells you what other pages reference it — those are often relevant context for the question.
- **Check existing analyses first.** Someone (or you) may have already asked a similar question. Call `wiki_list("wiki/analyses")` before doing fresh synthesis.
- **Small answers don't need filing.** "When was X founded?" → answer inline. "How does X's approach to Y compare with Z's across these 5 dimensions?" → worth filing.
- **Max 3 reads for simple questions.** Index → relevant page → answer. Don't over-read.
- **NEVER use local file reads.** All paths go through `wiki_read()` and `wiki_write()` MCP tools against SharePoint.
- **Suggest follow-up questions.** After answering, suggest 1-2 natural follow-up questions — these help the user explore further and may lead to new filed analyses.
- **Note when the wiki needs updating.** If you had to fall back to raw sources for detail, mention this: "The wiki's concept page on X could be enriched with this detail — want me to update it?"

## Troubleshooting

| Issue | Solution |
|-------|---------|
| `wiki/index.md` missing | The wiki hasn't been built. Run **se-wiki-generator** first. |
| Index is stale | Run **se-lint-wiki** to check index consistency, then rebuild. |
| Answer requires info not in any source | Say so explicitly. Don't make things up. Offer to research with **se-open-research**. |
| Too many relevant pages | Prioritize: concept pages > entity pages > source summaries. Read the most-linked pages first. |
| User wants a format you can't produce | Stay within markdown. Tables, headings, bullet points, and code blocks handle most needs. Note the limitation if the user wants something like a chart. |
