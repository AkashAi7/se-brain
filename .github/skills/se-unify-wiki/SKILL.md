---
name: se-unify-wiki
description: 'Unify two LLM wikis into one, non-destructively, using a similarity-tiered merge. Use when asked to "unify the wiki", "unify the wikis", "merge wiki_v1 into wiki", "augment the wiki with wiki_v1", "combine the two wikis", "fold one wiki into another", or "wiki unification". The base wiki is authoritative and immutable — its content is never deleted or overwritten (append-only). Because real augments are incremental content on similar topics, each augment page is classified against the most similar base page in the same category and handled by a 4-tier rule (exact = keep base / close = merge into one file / related = keep both + link / different = add new) so the graph does not bloat with duplicate nodes. CONFIGURABLE: "lite" mode integrates the two wikis with the LLM only (no script); "advanced" mode runs the local deterministic script then adds an LLM synthesis + deep-linking pass. Honors free-form instructions like "preserve X", "ensure Y is kept", or "maintain Z".'
---

# Unify Wiki

Merge two wikis that share the standard schema (`index.md`, `log.md`, `overview.md` +
`sources/ concepts/ entities/ comparisons/ analyses/`) into one unified wiki — **without ever
losing base content**, and **without bloating the graph** with duplicate nodes.

Real augments (e.g. `wiki_v1`) are usually **incremental content on similar topics** — new
accounts, updated numbers, extra detail — not a disjoint wiki. So unification is **not** "add a
new page + link for everything." Each augment page is compared to the most similar base page in
the **same category** (the schema is fixed) and handled by a **4-tier similarity rule**.

## The one hard invariant

`BASE` (default `wiki/`) is **authoritative and immutable**. Every change to a base file is
append-only, so the original base text is always an exact **prefix** of the result; `--protect`
pages stay **byte-identical**. Output = (all of BASE) + (the augment, folded in by tier), with
BASE winning every conflict and **no base content ever deleted or overwritten**.

## The 4-tier rule (core)

Classify each augment page against the most similar base page **in the same category**:

| Tier | When | Action | Graph effect |
|------|------|--------|--------------|
| **1. Exact** | identical / near-identical content (no meaningful new info) | **Keep the base file; drop the augment duplicate.** | no new node |
| **2. Close** | clearly the same topic with new/updated detail | **Merge into a single file** — fold the augment's new content into the base page. No new slug. | no new node |
| **3. Related** | meaningfully related but distinct | **Keep both pages + add a bidirectional "Related" link.** The LLM decides whether it should instead be a Tier-2 merge. | +1 node, linked |
| **4. Different** | unrelated | **Add the augment page as a new standalone node, no link.** | +1 node |

The point of tiers 1–2 is to **avoid duplicate nodes**: an incremental augment collapses into
the base (duplicates dropped, updates merged in place) instead of doubling the graph.

## Two modes (configurable)

| | **lite** (LLM-only) | **advanced** (script + LLM) |
|---|---|---|
| **What runs** | The LLM reads both wikis and integrates them directly — no script. | Runs `scripts/unify_wiki.py` (deterministic tiered union), then an LLM synthesis + deep-linking pass. |
| **Tiering** | LLM judges similarity and applies the 4 rules. | Script computes TF-IDF similarity and applies the 4 rules; LLM refines tier-2/tier-3. |
| **Best for** | Smaller wikis, maximum prose quality, no local Python, quick exploratory merges. | Larger wikis, deterministic + repeatable structural safety, a full report, then true prose synthesis. |
| **Base safety** | LLM must preserve all base content (verify before saving). | Guaranteed by the script (prefix/byte-identical checks + report); LLM re-verifies in Phase 2. |
| **Output** | Merged pages + updated index/log/overview. | All of the script's output (report, backup, state) + synthesized tier-2 pages. |

**Default to `advanced`** unless the user asks for a quick/lite/LLM-only merge or there's no local
Python. If the mode is ambiguous, ask the user which they want.

## When to Use This Skill

- "unify the wiki", "merge wiki_v1 into wiki", "augment wiki with wiki_v1", "combine the two wikis".
- "do a quick/lite unify" → **lite** mode. "deep/advanced unify with linking" → **advanced** mode.
- Unification with constraints — "merge them but **preserve** the stakeholders page", "**ensure**
  the Day 1 guide is kept exactly", "**maintain** the pipeline numbers". Honor these (below).

## Prerequisites

- A BASE wiki dir and an AUGMENT wiki dir using the standard schema.
- For **advanced** mode: Python 3 and the engine at `scripts/unify_wiki.py` (pure stdlib, local).

---

## Mode A — `lite` (LLM-only integration)

No script. You (the LLM) do the whole thing, preserving base content:

1. **Enumerate** both wikis: read each `index.md` and list pages per category.
2. **Match per category.** For each augment page, find the most similar base page in the **same**
   category (compare titles + content). Estimate similarity.
3. **Apply the 4-tier rule with judgment:**
   - **Exact** → keep the base page; skip the augment duplicate (note it).
   - **Close** → write a single merged page **at the base path**: keep every base claim and
     citation, fold in the augment's new detail and citations, put any disagreement in a
     **"Contradictions and Caveats"** block (**flag, never resolve** — base is authoritative),
     union `tags`/`sources`/`backlinks`, keep base `title`/`created`, bump `updated`. No new slug.
   - **Related** → keep both pages; add a bidirectional **"Related"** link. Only upgrade to a
     merge if they are genuinely close.
   - **Different** → add the augment page as a new page; no link.
4. **Base-retention guard:** never drop a base claim. If a merge would lose base content, keep
   both instead.
5. **Update** `index.md` (add new pages, note merges), append a `unify` entry to `log.md`, and
   refresh `overview.md` if the big picture changed. Maintain backlinks.
6. Respect every preserve/ensure/maintain instruction (below).

## Mode B — `advanced` (script + LLM synthesis + deep linking)

### Phase 1 — run the deterministic engine

```bash
python scripts/unify_wiki.py --base wiki --augment wiki_v1 --in-place --dry-run   # preview
python scripts/unify_wiki.py --base wiki --augment wiki_v1 --in-place             # apply
```

The script applies the 4-tier rule deterministically (TF-IDF similarity), folds tier-2 merges in
as delimited `<!-- BEGIN merged:... -->` blocks, adds tier-3 "Related" links, backs up the base,
validates (base-retention + broken links), and writes `unify-report.md` (+ `.json`). Key flags
(full reference in `scripts/README.md`):

| Flag | Purpose |
|------|---------|
| `--base` / `--augment` | base (authoritative) / augment dir |
| `--in-place` / `--out DIR` | append onto base / write a new unified dir |
| `--exact-threshold` / `--merge-threshold` / `--relate-threshold` | tier cut-offs (defaults `0.985` / `0.60` / `0.25`) |
| `--preserve PAT` | keep a base page **separate** (never merged → becomes a Related link) |
| `--protect PAT` | keep a base page **byte-identical** (no append at all) |
| `--explain` | add a per-page similarity/tier table to the report |
| `--dry-run` / `--force` / `--backup-dir` / `--report` | preview / re-run / backup / report path |

### Phase 2 — LLM synthesis + deep linking (only where it adds value)

1. Read `unify-report.md`. Confirm **base retention = 100%** and **broken links = 0**. If either
   fails (script exit 3), **stop and surface the report** — do not claim success.
2. **Tier-2 merges:** for each `<!-- BEGIN merged:<aug>:<slug> -->` block the script appended to a
   base page, rewrite the base page into **one coherent synthesized page** — fold the merged
   content into the right sections, keep all base claims, flag contradictions (never resolve),
   union frontmatter, then **remove the merge markers/block**. Verify no base claim was dropped.
3. **Tier-3 related:** for each related pair, decide — upgrade to a true merge (if actually close)
   or keep the two pages with the Related link. Add deep cross-links (Related Concepts/Entities).
4. **Re-verify** base retention per edited page and refresh `index.md` / `overview.md` / backlinks.

If the user only wants the safe structural union, Phase 1 alone is a complete, valid result.

---

## Honoring User Instructions (important)

Translate constraints into flags (advanced) **and** synthesis directives (both modes). Echo back
your interpretation.

| User says | Interpretation | Action |
|-----------|----------------|--------|
| "**preserve** the X page", "keep X separate", "don't merge X" | X must stay its own node | `--preserve "X"`; in lite mode never fold X into another page (Related link at most) |
| "**ensure** X is kept", "**maintain** X exactly", "X must not change" | X must be byte-identical | `--protect "X"`; never edit X in any synthesis |
| "don't lose anything" / "keep all base" | default — reaffirm | none; point to 100% base-retention in the report |
| "merge duplicates / combine overlapping pages" | allow tier-2 synthesis | run Phase 2 (advanced) or merge in lite |
| "do a quick / LLM-only / lite merge" | mode | use **lite** |
| "deep merge with linking" / "full unification" | mode | use **advanced** |

Rules: a preserve/ensure/maintain instruction is a **hard constraint** that overrides defaults.
Prefer `--protect` when content must not change at all; `--preserve` when it just must stay a
separate node. After the run, **verify** the constraint held and state it back. Never silently
override a user instruction.

## Full Workflow

1. Identify BASE and AUGMENT dirs (default `wiki` + `wiki_v1`; confirm if ambiguous).
2. Pick the **mode** (default advanced; ask if unclear) and parse any preserve/protect constraints.
3. **lite** → do Mode A. **advanced** → Phase 1 **dry-run first**, show planned tier counts, then
   apply, then Phase 2 where it helps.
4. Confirm **base retention 100%** and **0 broken links** (advanced: from the report). If not, stop.
5. Present the final report: tier breakdown (exact/close/related/different), what merged, what was
   added, contradictions carried, retention, link integrity, backup location, how to revert.
6. Offer **se-lint-wiki** on the result to recompute backlinks and catch any orphans.

## Verification checklist (every run)

- [ ] Mode chosen and confirmed; constraints parsed and echoed back.
- [ ] (advanced) Dry-run reviewed before any in-place write.
- [ ] **Base retention 100%** and **0 broken links** (else investigate — don't claim success).
- [ ] Every "preserve/ensure/maintain" constraint verified in the output.
- [ ] Tier-1 duplicates did **not** create new nodes; tier-2 updates folded into the base.
- [ ] `log.md` has the new `unify` entry; `index.md` / `overview.md` updated; backlinks current.
- [ ] (Phase 2) merged pages keep all base claims and **flag** (not resolve) contradictions.

## Troubleshooting

| Issue | Cause / Fix |
|-------|-------------|
| Too many tier-2 merges (over-merging) | Raise `--merge-threshold` (e.g. `0.7`); inspect with `--explain`. |
| Genuine updates classified as tier-1 exact (new info dropped) | Lower `--exact-threshold` (e.g. `0.97`); same-slug pages with any body change already merge, not drop. |
| Unrelated pages linked as tier-3 | Raise `--relate-threshold` (e.g. `0.35`). |
| `ABORT: base already unified … --force` | Restore from backup / `git checkout -- wiki`, or pass `--force`. |
| Exit `3` (retention or broken links) | **Do not ship.** Restore base from backup; surface the report. |
| Want a reversible experiment | `--out wiki_unified` instead of `--in-place`. |

## Tips

- **Incremental augment ⇒ mostly tier-1/tier-2.** Expect the graph to *stay about the same size*,
  not double — that's the whole point.
- **`--explain` calibrates thresholds.** Run a dry-run with `--explain` and read the score column.
- **The report is the source of truth** — lead the user with its tier breakdown and metrics.
- **Base safety is the whole point.** If you can't confirm 100% retention, treat the run as failed.
- See `scripts/README.md` for the full flag reference, recipes, and exit codes.
