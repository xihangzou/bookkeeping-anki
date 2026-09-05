# ANKI-042 Final Semantic Coverage Audit

Status: **PASS**

Issue: **ANKI-042 — Final semantic coverage QA**

Audit date: 2026-09-05

## Audited baseline

- source repository: `xihangzou/bookkeeping-integrated`
- source commit: `569ed7b82e729334e1472286eaca7c4352e6fbdb`
- merged source: `merged/textbook.md`
- production audit commit: `28d3ac7b00721e37716efe85143d50a2c9199f09`
- production CI: **Validate production notes #382** (`run_id=33943298560`) — **PASS**
- authoritative rules: `rules/anki_card_rules.md`
- canonical schema: `schema/note_schema.yaml`

The final audit covers the complete source → candidate proposition → canonical ALP → approved production Note chain. It uses the canonical source-structure inventory and topic-inventory completion manifest rather than treating the active Note set itself as the source-coverage denominator.

## Machine-checkable coverage summary

```text
audit=ANKI-042
status=PASS
source_repo=xihangzou/bookkeeping-integrated
source_commit=569ed7b82e729334e1472286eaca7c4352e6fbdb
source_path=merged/textbook.md
source_chapter_files=31
represented_source_chapter_files=31
source_h2_sections=110
source_h3_sections=387
canonical_source_sections=497
candidate_source_anchors=589
source_inventory_coverage_pct=100.00
candidate_propositions=1004
included_alps=965
excluded_candidates=39
excluded_DECORATIVE_EXAMPLE=38
excluded_DUPLICATE_EXACT=1
decision_coverage_pct=100.00
production_rows=811
approved_notes=735
deprecated_notes=76
approved_cards=748
approved_cloze_spans=2008
mapped_included_alps=965
unmapped_included_alps=0
semantic_coverage_pct=100.00
orphan_alps=0
orphan_notes=0
orphan_note_alp_refs=0
multiply_mapped_active_alps=0
unexplained_exclusions=0
unresolved_source_gaps=0
exact_duplicate_active_propositions=0
retained_semantic_similarity_pairs_rechecked=4
unresolved_semantic_duplicate_conflicts=0
rules_sha256=0d9fece4586b900aa775df63525d83668c9fee962f1cd37997f6f59cd1b9c9c9
schema_sha256=a5817abf66e33a37abdb6b9981aab6eb4a1833aee5cc4f8db22aefa0bd1aed8c
workflow_run_id=33943298560
workflow_run_number=382
```

## Coverage interpretation

The canonical structural inventory contains **31 chapter files**, **110 H2 sections**, and **387 H3 sections**, for **497 canonical source sections**. The candidate inventory contains **589 unique source anchors** because extraction anchors are intentionally finer-grained than the H2/H3 hierarchy in places such as `POINT`, examples, and other sub-section anchors. Therefore the 589 anchor count is not a competing denominator; the canonical source-coverage denominator remains the reconciled 497-section structure inventory.

All **1,004** candidate propositions have an explicit canonical decision: **965 INCLUDE** and **39 EXCLUDE**, giving **100.00% decision coverage**. All exclusions are enumerated under the consolidated rule vocabulary: **38 `DECORATIVE_EXAMPLE`** and **1 `DUPLICATE_EXACT`**. Unexplained exclusions are **0**.

Every one of the **965 included ALPs** maps to exactly one active approved production Note after normalization. Unmapped included ALPs, invalid Note→ALP references, orphan approved Notes, and multiply mapped active ALPs are all **0**. This gives **100.00% semantic retrieval coverage** for included ALPs.

The production corpus contains **811 rows**: **735 approved** active Notes and **76 deprecated** lineage rows. The active corpus generates **748 cards** with **2,008 Cloze spans**. Every production row retains the pinned source repository, commit, and merged-source path, and every row has `QA=pass`.

## Duplicate / conflict disposition

The final corpus contains **0 exact duplicate active retrieval propositions**. The corpus-normalization validator still surfaces four similarity candidates at the configured review threshold; ANKI-041 rechecks these retained pairs and reports no recall-quality defect. They remain distinct because they encode different accounting contexts or retrieval goals, so unresolved semantic duplicate conflicts are **0**.

## Validator / CI contract

`script/validate_coverage_production.py` is not used; the canonical executable gate is:

- `scripts/validate_coverage_production.py`

It verifies the pinned source/inventory contract, candidate decisions, exclusions, production lifecycle counts, source provenance, stable IDs, ALP↔Note mapping, active exact-duplicate absence, card/Cloze counts, and current rule/schema fingerprints.

`.github/workflows/validate-production.yml` now includes the coverage gate in full production validation and reruns the corpus/journal/formula/recall/coverage validators when canonical production Note or topic-inventory shards change. Changes to the source-structure inventory, topic-inventory manifest, rules, schema, or coverage validator trigger the full validator suite.

CI run **#382** passed the governance validator, all **31 batch production validators**, corpus normalization, journal-entry QA, formula/calculation QA, recall-quality QA, and the ANKI-042 coverage gate.

## Acceptance criteria disposition

- full canonical source/inventory audited: **PASS**
- all source candidates have INCLUDE/EXCLUDE decision: **PASS (100.00%)**
- all included ALPs have active production retrieval coverage: **PASS (965/965)**
- all approved Notes trace to canonical ALP(s) and pinned provenance: **PASS**
- unexplained exclusions: **0**
- unresolved required source coverage gaps: **0**
- orphan ALPs / orphan approved Notes: **0 / 0**
- unresolved semantic duplicate conflicts: **0**
- current consolidated rules/schema validation: **PASS**
- reproducible machine-checkable report and CI gate committed: **PASS**

## Release handoff

No production-card correction was required by ANKI-042. The canonical production corpus is ready for **ANKI-043 deterministic export/release packaging**.
