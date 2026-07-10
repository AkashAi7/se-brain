---
title: "How we unify two wikis without bloating the graph"
date: 2026-07-02
category: Engineering
description: "Folding an incremental wiki onto a base one, non-destructively — a 4-tier similarity rule that dedupes instead of duplicating, with a base-safety contract you can actually prove."
tags: [wiki-unification, knowledge-management, entity-resolution, agents, se-brain]
---

SE Brain started with one wiki. Then there were two.

It happens the moment the idea works. An SE builds a base wiki; a quarter later
there's a second collection — a teammate's version, a new set of accounts, an
updated pipeline, a fresh batch of notes. Same shape (`concepts`, `entities`,
`sources`, …), overlapping topics, newer facts. Now you don't want two wikis.
You want one brain.

So the question is narrow and sharp: **how do you fold `wiki_v1` into `wiki`
without (1) losing anything the base already knew, or (2) drowning the graph in
near-duplicate pages?** This post is about the answer we landed on — and the
naive version we threw away first.

> ▶ **Watch the walkthrough** — a short video tour of wiki unification in SE Brain:
> [open the video](https://microsoftapc-my.sharepoint.com/:v:/g/personal/abpatra_microsoft_com/IQCDFJ63sXjYTZsdSzaKMTwMAcWnRcQzrfp4lzUzq5U8-jI?e=A38QJq&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)

## Concatenation is not unification

The obvious merge is: copy every augment page in; where two pages collide, keep
both and add a cross-link. It's safe. It's also wrong.

Real augments aren't disjoint. `wiki_v1` is **incremental content on similar
topics** — the same accounts with new deals, the same concepts with sharper
detail. Blindly keeping both turns one `tata-steel.md` into `tata-steel.md` *and*
`tata-steel--v1.md`, doubles your entity list, and every "Related" link you sprinkle
in makes the graph noisier, not smarter. Within two merges nobody trusts it —
which is exactly the [rot an LLM-managed wiki was supposed to prevent](post.html?slug=llm-managed-wikis).

Unification, it turns out, is a **deduplication / entity-resolution** problem
wearing a merge costume. (This is the part we changed our minds about: our first
cut was precisely that keep-both merger. It passed every safety check and still
produced a worse wiki.)

## The non-negotiable: the base is sacred

One rule sits above everything else: the **base wiki is authoritative and
immutable**. Merging is an *additive, left-biased union* — output = everything in
base **+** everything in augment, base wins every conflict, and **no base byte is
ever deleted or overwritten.**

We don't just promise that; we make it structural. Every change to a base file is
**append-only**, so the original base text is always an exact *prefix* of the
result. Pages you mark `--protect` stay *byte-identical*. After the merge a
validator re-reads every base page and **fails the whole run** if any base
content isn't preserved as a prefix.

> Base safety isn't a feature we tested once. It's an invariant the tool asserts
> on every run — and refuses to finish if it can't.

## The 4-tier rule

So for each augment page we ask one question: *how similar is it to the most
similar base page in the same category?* (The schema is fixed, so "same kind
compares to same kind" — entities to entities, concepts to concepts.) The answer
picks one of four actions:

| Tier | If it's… | We… | New node? |
|------|----------|-----|-----------|
| **1 · Exact** | identical (or nearly) to a base page | keep the base page, **drop** the copy | no |
| **2 · Close** | the same thing, with new detail | **merge** it into that one page | no |
| **3 · Related** | a cousin, not a copy | keep both, add a **Related** link | yes |
| **4 · Different** | genuinely new | add it as its own page | yes |

The whole point of tiers 1–2 is to **not create a node**. An incremental augment
should *collapse into* the base — duplicates dropped, updates folded in — not
double it.

## A tiny example

Say the base has `entities/tata-steel.md`, `entities/mahindra.md`, and
`concepts/technical-win.md`. The augment brings four pages:

| Augment page | Nearest base page | Similarity | → Tier |
|--------------|-------------------|:----------:|--------|
| `concepts/technical-win.md` *(identical)* | `technical-win.md` | 1.00 | **1 · Exact** |
| `entities/tata-steel.md` *(POC now in prod, new deal)* | `tata-steel.md` | 0.94 | **2 · Close** |
| `entities/jsw-steel.md` *(a different steel account)* | `tata-steel.md` | 0.28 | **3 · Related** |
| `entities/orsted.md` *(offshore wind, unrelated)* | `mahindra.md` | 0.08 | **4 · Different** |

Four pages in — and the graph grows by **two**. `technical-win` is a duplicate,
dropped. `tata-steel` gets *richer in place*: the new deal and updated pipeline
are folded into the one page, base text untouched at the top. `jsw-steel` joins
as its own node with a Related link to Tata Steel. `orsted` lands standalone. The
old keep-both approach would have added four new pages plus a tangle of links.

## Same slug, new facts: the bug worth naming

Here's the subtle one. `entities/tata-steel.md` exists in *both* wikis — same
node. Our first tiered version saw 94% similarity, called it "exact," and dropped
the augment copy… silently throwing away the new deal and the updated pipeline.
That's the exact opposite of what you want from an *update*.

The fix is a rule, not a threshold: **a same-node page is "exact" only if its
body is byte-identical; any change means merge.** Similarity thresholds are for
deciding things about *different* pages. Identity is decided by the slug and
title, and an updated page is still the same node — so it merges, and the new
facts survive.

## How "similar" gets a number

The score is plain **TF-IDF cosine** between the two pages' text, compared only
within a category. TF-IDF matters here: these pages share a lot of scaffolding
(`## Key Points`, `## Related`, boilerplate headings), but `idf` down-weights
anything common across the corpus, so the score reflects *distinctive* overlap,
not shared structure.

Calibrated on real data, the bands separate cleanly: genuinely unrelated pages
score **≲ 0.15**, a near-duplicate scores **≈ 0.95+**. So the defaults are
`exact ≥ 0.985`, `merge ≥ 0.60`, `relate ≥ 0.25` — and the fuzzy middle (a
JSW Steel at 0.28) is exactly where a deterministic script should stop guessing
and **let the LLM decide** whether it's a merge or just a link.

## Deterministic core, optional brain

We ship it two ways, because they're good at different things.

- A **local Python script** (`unify_wiki.py`, standard library, no installs) does
  the whole tiered union deterministically: classify every page, merge, link,
  back up the base, validate, and write a report. Same input → same safe output,
  every time. It never needs a model.
- The **`se-unify-wiki` skill** wraps it with two modes. **Lite** is LLM-only: the
  agent reads both wikis and does the merge in prose, no script. **Advanced** runs
  the script, then lets the LLM rewrite each tier-2 "merged" block into one truly
  synthesized page and adjudicate the tier-3 middle band.

Both honor plain-English guardrails. *"Keep the pipeline numbers exactly"* becomes
byte-level `--protect`. *"Keep the stakeholders page separate"* forces it to stay
its own node. You say the intent; the tool maps it to a constraint and then
**verifies the constraint held**.

Why both? The deterministic core is what makes it *trustworthy* — a repeatable,
auditable, base-safe union with a report you can read. The LLM is what makes it
*smart* — collapsing two overlapping pages into one clean narrative instead of two
stacked halves. You choose how much of each you want.

## The payoff

The test that convinced us: take the base wiki, make an augment that's a full copy
with a few pages updated (the real "incremental" case), and unify.

```
Tier 1 exact (base kept, dup dropped) : 36
Tier 2 close (merged in place)        :  3
Tier 3 related / Tier 4 new           :  0
New nodes created                     :  0
Broken links after merge              :  0
Base retention                        : 100%
```

The graph didn't grow. It just got **more current** — three pages absorbed their
updates, thirty-six duplicates evaporated, and not a single base fact was lost.
That's the difference between concatenating two wikis and actually unifying them.

## The takeaway

Unifying two wikis is entity resolution with a safety contract. The base is
sacred, the graph shouldn't bloat, and every merge either preserves a byte or
explains itself in the report. A deterministic core keeps it honest; an LLM makes
it fluent.

Two wikis go in. One brain comes out — a little more current, and no bigger than
it needs to be. The rest, as always, is just files.
