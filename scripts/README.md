# Wiki Unification — `unify_wiki.py`

Non-destructive unification of two LLM wikis. Merges an **AUGMENT** wiki (e.g. `wiki_v1/`) on
top of a **BASE** wiki (e.g. `wiki/`), treating the base as authoritative and immutable.

> **The one hard invariant:** output = (all of BASE) + (the augment, folded in by tier); BASE
> wins every conflict; **no BASE byte is ever deleted or overwritten — only appended to.** Every
> change to a base file is append-only, so the base text is always an exact **prefix** of the
> result. `--protect` pages stay **byte-identical**. The script *fails the run* (exit 3) if any
> base region is altered.

Real augments are usually **incremental content on similar topics** (new accounts, updated
numbers, extra detail) — not a disjoint wiki. So the engine does **not** blindly add a new page +
link for every augment page (which would bloat the graph). Instead each augment page is compared
to the most similar BASE page **in the same category** (the schema —
`sources/concepts/entities/comparisons/analyses` — is fixed) and handled by a **4-tier rule**.

Pure Python **standard library** (no `pip install`, no build step, fully local). The companion
Copilot skill `.github/skills/se-unify-wiki/` wraps this script (advanced mode) and also offers
an LLM-only "lite" mode.

---

## The 4-tier rule

| Tier | When (similarity to nearest same-category base page) | Action | Graph effect |
|------|------|--------|--------------|
| **1. Exact** | identical body, or sim ≥ `--exact-threshold` | **keep the base file; drop the augment duplicate** | no new node |
| **2. Close** | sim ≥ `--merge-threshold` (or same slug/title with any change) | **merge into a single file** — the augment's content is appended into the base page under a delimited `<!-- BEGIN merged:… -->` block (append-only). No new slug. | no new node |
| **3. Related** | sim ≥ `--relate-threshold` | **keep both pages + add a bidirectional "Related" link** (the skill's LLM can upgrade this to a merge) | +1 node, linked |
| **4. Different** | below `--relate-threshold` | **add the augment page as a new standalone node, no link** | +1 node |

**Same-slug/same-title pages are treated as the same node:** identical body → Tier 1 (keep base);
**any change → Tier 2 merge** (so updated info is captured, never dropped).

> An incremental augment therefore **collapses into the base** — duplicates dropped, updates
> merged in place — and the graph stays about the same size instead of doubling.

## Requirements

- Python 3 (tested on 3.14), standard library only.
- BASE and AUGMENT dirs using the standard schema.

## Quick start

```bash
# 1. Preview the plan + per-page tiers without writing anything (recommended first):
python scripts/unify_wiki.py --base wiki --augment wiki_v1 --in-place --dry-run --explain

# 2. Apply it in place (append-only onto the base):
python scripts/unify_wiki.py --base wiki --augment wiki_v1 --in-place

# OR: produce a brand-new unified dir and leave base + augment untouched:
python scripts/unify_wiki.py --base wiki --augment wiki_v1 --out wiki_unified
```

After a run, read **`unify-report.md`** and confirm **Base retention = 100%** and
**Broken links = 0**.

---

## How it works

1. **Load** every `.md` page from BASE and AUGMENT and parse YAML frontmatter.
2. **Classify** each augment content page against the most similar base page in the **same
   category** using **TF-IDF cosine similarity** (idf naturally discounts shared boilerplate, so
   the score reflects distinctive content overlap). Apply the 4-tier rule above.
3. **Execute:**
   - *Exact* → no-op (base kept, duplicate dropped).
   - *Close* → append a delimited "Merged from …" block to the base page (base stays a prefix);
     the augment page is **not** written as a separate file.
   - *Related* → write the augment page, add a "Related (unification)" link on the base page
     (append-only) and a back-link note on the augment page.
   - *Different* → write the augment page as-is.
   - Links in written pages are repointed through a rename map (so links to merged/dropped pages
     follow them to the base), and `wiki_v1/ → wiki/` frontmatter refs are swapped; a
     `source_wiki:` provenance field is added.
4. **Merge structural files** append-only — `index.md` (per-tier augment catalog + carried-over
   **Known Data Inconsistencies**), `overview.md`, `log.md`.
5. **Back up** the base, **validate** (base-retention prefix check + broken-link scan), and write
   the **report** (`unify-report.md` + `.json`) plus a `.unify-state.json` audit file.

---

## Options

Run `python scripts/unify_wiki.py --help` for the canonical list.

### Inputs & output location

| Option | Default | What it does |
|--------|---------|--------------|
| `--base DIR` | `wiki` | The **authoritative** base wiki. Never deleted/overwritten. |
| `--augment DIR` | `wiki_v1` | The wiki merged **on top** of the base. |
| `--in-place` | (off) | Append the augment onto the base dir itself (append-only). |
| `--out DIR` | — | Instead, copy the base to a **new** `DIR` and unify there (base & augment untouched). `DIR` must not exist. |

### Strategy & tier thresholds

| Option | Default | What it does |
|--------|---------|--------------|
| `--strategy {tiered,keep_both}` | `tiered` | `tiered` = the 4-tier rule above. `keep_both` = legacy: every match becomes a twin `<slug>--v1.md` (use only if you explicitly want duplicate nodes). |
| `--exact-threshold FLOAT` | `0.985` | Tier 1 cut-off. At/above this (or identical body) the augment page is a **duplicate** and is dropped. Lower it (e.g. `0.97`) if real updates are being dropped. |
| `--merge-threshold FLOAT` | `0.60` | Tier 2 cut-off. At/above this the page is **merged** into the base. Raise (e.g. `0.7`) to merge less aggressively. |
| `--relate-threshold FLOAT` | `0.25` | Tier 3 cut-off. At/above this the pages are **related** (kept + linked); below, the page is **new** (no link). Raise (e.g. `0.35`) to link less. |
| `--threshold FLOAT` | — | Legacy alias for `--relate-threshold` (and the match floor for `keep_both`). |

> Calibrate with `--dry-run --explain`: the report's similarity column shows each augment page's
> nearest base page and score, so you can see exactly where the tier boundaries fall. (For
> reference: in a fully *disjoint* pair, cross-topic pages score ≲ 0.15; a near-duplicate scores
> ≈ 0.95+.)

### Preserving / protecting content (honoring constraints)

| Option | Repeatable | What it does |
|--------|------------|--------------|
| `--preserve PAT` | yes | Any base page whose relpath contains `PAT` is **kept separate** — never merged/dropped. A matching augment page is downgraded to a **Related** link instead. |
| `--protect PAT` | yes | Matching base pages are kept **byte-identical** — not even a "Related"/merge block is appended. The augment page is added standalone instead. Use for *"maintain X exactly"*. |
| `--no-see-also` | (off) | Don't append "Related" links to any base page (keeps base pages byte-identical). |

> Map natural instructions: *"keep X separate / don't merge X"* → `--preserve X`;
> *"ensure X is kept / maintain X exactly"* → `--protect X`.

### Output, safety & control

| Option | Default | What it does |
|--------|---------|--------------|
| `--explain` | (off) | Add a per-page **similarity/tier table** (nearest base page + score) to the report. Great for threshold calibration. |
| `--dry-run` | (off) | Plan + write the **report only**; touch **no** wiki files. Always preview first. |
| `--augment-label L` | augment dir name | Friendly label for the augment collection in index/overview/log. |
| `--augment-suffix S` | `v1` | Twin slug suffix — only used by the legacy `keep_both` strategy. |
| `--backup-dir DIR` | `<repo>/.unify-backup` | Where the base is snapshotted before mutation. |
| `--no-backup` | (off) | Skip the pre-flight base backup (not recommended for `--in-place`). |
| `--report PATH` | `<out-or-repo>/unify-report.md` | Markdown report path (a `.json` sibling is written too). |
| `--force` | (off) | Re-run even if the base already has a `<!-- BEGIN unified:<aug> -->` marker (the idempotency guard). |

---

## Recipes

```bash
# Preview with per-page tiers (no writes) — best first step:
python scripts/unify_wiki.py --base wiki --augment wiki_v1 --in-place --dry-run --explain

# Apply in place:
python scripts/unify_wiki.py --base wiki --augment wiki_v1 --in-place

# Keep a page byte-identical (e.g. "maintain the pipeline numbers exactly"):
python scripts/unify_wiki.py --base wiki --augment wiki_v1 --in-place \
    --protect "analyses/pipeline-health-snapshot.md"

# Keep a page as its own node (never merged), and label the augment nicely:
python scripts/unify_wiki.py --base wiki --augment wiki_v1 --in-place \
    --preserve "entities/onboarding-stakeholders.md" --augment-label "Q3 incremental"

# Merge less aggressively / link less:
python scripts/unify_wiki.py --base wiki --augment wiki_v1 --in-place \
    --merge-threshold 0.7 --relate-threshold 0.35

# Safe, reversible experiment in a throwaway dir:
python scripts/unify_wiki.py --base wiki --augment wiki_v1 --out wiki_unified

# Re-run after a previous unification:
python scripts/unify_wiki.py --base wiki --augment wiki_v1 --in-place --force
```

---

## What a run produces

- **Tier-1** duplicates: nothing written (base kept) — recorded in the report.
- **Tier-2** merges: a delimited "Merged from …" block appended to the base page (single file).
- **Tier-3** related: the augment page added + an append-only "Related (unification)" link on the
  base page + a back-link note on the augment page.
- **Tier-4** different: the augment page added as-is (links + `wiki_v1/→wiki/` refs rewritten,
  `source_wiki:` added).
- **`index.md` / `overview.md` / `log.md`** updated append-only (base content preserved as a prefix).
- **`unify-report.md` + `unify-report.json`** — tier breakdown, merged/related/exact/new tables,
  optional `--explain` similarity table, **base-retention %**, broken-link count, contradictions carried.
- **`.unify-backup/<base>-<timestamp>/`** — full base snapshot before mutation.
- **`<base>/.unify-state.json`** — audit record (every page's tier, score, and final location).

## Validation & exit codes

- **Base retention** — every base file's original content must be an exact **prefix** of the
  merged file (protected pages byte-identical). Must be **100%**.
- **Link integrity** — all relative `.md` links across the unified wiki must resolve. Must be **0** broken.

| Exit code | Meaning |
|-----------|---------|
| `0` | Success (or a clean `--dry-run`). |
| `2` | Aborted — base already unified (use `--force`), or bad/missing paths. |
| `3` | **Validation failed** — base retention < 100% or broken links introduced. Treat as failed; restore the base and investigate. |

## Idempotency & reverting

- Re-running is guarded by the `<!-- BEGIN unified:<aug> -->` marker in `index.md` plus
  `.unify-state.json` — a double-merge **aborts** (exit 2) unless `--force`.
- To revert an in-place run: restore from the backup printed in the report, or — if the base is
  git-tracked — `git checkout -- wiki`.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Real updates dropped as Tier-1 exact | Lower `--exact-threshold` (e.g. `0.97`). Same-slug pages with any body change already merge, not drop. |
| Over-merging (Tier-2 firing too often) | Raise `--merge-threshold` (e.g. `0.7`); inspect with `--explain`. |
| Unrelated pages linked as Tier-3 | Raise `--relate-threshold` (e.g. `0.35`). |
| `ABORT: base already unified … --force` | Restore from backup / `git checkout -- wiki`, or pass `--force`. |
| Exit `3` (retention/broken links) | **Don't ship.** Restore base from backup; check the report's checks. |
| Don't want to touch the base | Use `--out wiki_unified`. |
| `.unify-backup/` growing | Safe to delete old snapshots once a run is verified. |

---

## Relationship to the `se-unify-wiki` skill

| | This script (`unify_wiki.py`) | The `se-unify-wiki` skill |
|---|---|---|
| **Mode** | Standalone, deterministic, 100% local | Configurable: **lite** (LLM-only) or **advanced** (wraps this script) |
| **Tiering** | TF-IDF similarity + the 4-tier rule | lite: LLM judgment; advanced: this script |
| **Tier-2 merge** | structural append block (base-preserved) | advanced Phase 2 rewrites it into **true synthesized prose** |
| **Tier-3 related** | adds a Related link | LLM decides merge-vs-link |
| **"preserve / ensure / maintain X"** | `--preserve` / `--protect` | parsed from the instruction → these flags + synthesis directives |

Run the script directly for a fast, fully-local tiered union; use the skill for natural-language
control, LLM-only merging (lite), or true prose synthesis on the merged pages (advanced).
