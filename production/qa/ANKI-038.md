# ANKI-038 — Cross-chapter semantic normalization report

## Result

**PASS** — canonical production corpus normalized across foundation, commercial, and industrial batches under the current living rule contract.

- Issue: #39 `ANKI-038 Normalize cross-chapter topics and duplicates`
- Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`
- Rule authority: latest merged `rules/anki_card_rules.md`
- Schema: `schema/note_schema.yaml` v1.1
- Corpus: 31 production TSV batches (`FND-00`, `COM-01..16`, `IND-01..14`)
- Normalization validator: `scripts/validate_corpus_production.py`

## Before / after

| Metric | Before normalization | After normalization | Delta |
|---|---:|---:|---:|
| Production rows | 811 | 811 | 0 |
| Approved active Notes | 738 | 735 | -3 |
| Deprecated lineage Notes | 73 | 76 | +3 |
| Generated active cards | 746 | 743 | -3 |
| Active Cloze spans | 2,011 | 2,004 | -7 |
| Included ALPs | 965 | 965 | 0 |
| Active mapped ALPs | 965 | 965 | 0 |
| Canonical excluded candidates | 39 | 39 | 0 |
| Orphan included ALPs | 0 | 0 | 0 |
| Active Note references to non-INCLUDE ALPs | 0 | 0 | 0 |
| Multiply mapped active ALPs | 0 | 0 | 0 |
| Duplicate stable Note IDs | 0 | 0 | 0 |
| Exact duplicate active retrieval propositions | 1 pair | 0 | -1 pair |

The normalization changed lifecycle/mapping only where required. No stable Note ID or ALP ID was renumbered or reused.

## Deterministic migrations

### 1. Official variable-budget capacity variance formula

The following active Notes had an exactly identical generated retrieval proposition:

- `BK-IND-05-0023` — manufacturing-overhead variance analysis
- `BK-IND-11-0021` — standard-costing manufacturing-overhead variance analysis

Decision:

- keep `BK-IND-05-0023` as the canonical active formula because IND-05 is the primary chapter introducing manufacturing-overhead allocation and variance analysis;
- extend its active mapping to `ALP-IND-05-0024 ALP-IND-11-0021`;
- deprecate `BK-IND-11-0021` with auditable replacement `BK-IND-05-0023`;
- preserve the original IND-11 row and source mapping as lineage evidence.

This removes the exact duplicate while preserving the standard-costing bridge to the shared formula.

### 2. Report-form P/L gross-profit and operating-profit stages

The commercial financial-statement corpus and manufacturing financial-statement corpus repeated the same accounting relationships without a manufacturing-specific change in retrieval operation:

- `BK-COM-13-0017` — gross profit
- `BK-COM-13-0018` — operating profit
- `BK-IND-10-0010` — the same gross-profit → operating-profit sequence

Decision:

- keep `BK-COM-13-0018` as the canonical active report-form P/L retrieval frame;
- integrate gross profit and operating profit in one coherent sequence;
- map it to `ALP-COM-13-0017 ALP-COM-13-0018 ALP-IND-10-0010`;
- deprecate `BK-COM-13-0017` and `BK-IND-10-0010`, each with replacement `BK-COM-13-0018`;
- retain the manufacturing-specific P/L Notes in IND-10 where manufacturing changes the retrieval operation, such as product-cost flow, cost-variance adjustment, manufacturing cost report, and manufacturing inventories.

## Retained semantic overlaps

The post-normalization similarity scan reports four cross-batch candidates at the review threshold. They are intentionally retained because their retrieval operations are materially distinct.

| Pair | Decision | Retrieval-context reason |
|---|---|---|
| `BK-IND-10-0008` ↔ `BK-IND-12-0005` | Retain | IND-10 asks for manufacturing financial-statement COGS before cost-variance adjustment; IND-12 asks specifically for **absorption-costing** COGS as the comparator to direct/variable costing. The equation is similar but the method condition is part of the learning target. |
| `BK-IND-05-0005` ↔ `BK-IND-06-0021` | Retain | IND-05 is plant-wide manufacturing-overhead actual allocation; IND-06 applies actual allocation **within each manufacturing department after departmental cost allocation**. The departmental application changes the relevant allocation base and decision context. |
| `BK-COM-13-0018` ↔ `BK-IND-12-0006` | Retain | COM-13 is the generic report-form P/L profit-stage relationship; IND-12 identifies those stages specifically as **absorption costing**, contrasted with contribution margin / fixed-cost presentation under direct costing. |
| `BK-IND-03-0003` ↔ `BK-IND-04-0002` | Retain | Both use traceability as the direct/indirect criterion, but one classifies **labor cost** and the other **expenses**. The answer labels and cost-element classification target differ. |

No retained pair is an exact duplicate generated card.

## Terminology normalization

- `操業度差異` uses the IND-05 manufacturing-overhead formula as the canonical shared formula; the IND-11 occurrence is a cross-chapter bridge rather than a duplicate card.
- `売上総利益`, `営業利益`, and `販売費及び一般管理費` use the COM-13 report-form P/L terminology as the canonical generic profit-stage vocabulary.
- Method qualifiers such as `全部原価計算`, departmental qualifiers such as `当該部門`, and cost-element qualifiers such as `労務費` / `経費` are preserved when they change the retrieval operation.
- Existing COM-16 ↔ industrial-chapter overlap normalization is preserved; ANKI-038 does not reintroduce chapter-level duplicates previously removed during COM-16 review.

## ALP and lineage integrity

Post-normalization corpus validation establishes:

- 965 / 965 included ALPs materially represented by active Notes;
- orphan included ALPs = 0;
- active Note references to invalid/non-INCLUDE ALPs = 0;
- multiply mapped active ALPs = 0;
- duplicate stable Note IDs = 0;
- all 76 deprecated rows contain lineage/replacement evidence recognized by the corpus validator;
- production row count remains 811, so deprecated history is retained rather than deleted.

Inventory shards remain canonical source evidence and were not renumbered or opportunistically rewritten.

## Validation

Primary corpus command:

```bash
python scripts/validate_corpus_production.py
```

Expected normalized result:

```text
batches=31 production_rows=811 approved_notes=735 deprecated_notes=76
approved_cards=743 approved_cloze_spans=2004
included_alps=965 excluded_candidates=39 active_mapped_alps=965
orphan_alps=0 orphan_note_refs=0 multiply_mapped_alps=0
duplicate_note_ids=0 exact_duplicate_active_propositions=0
deprecated_lineage_hints=76/76
semantic_similarity_candidates_ge_0.50=4
ANKI-038 corpus normalization validation: PASS
```

The consolidated `.github/workflows/validate-production.yml` now includes every chapter validator plus `scripts/validate_corpus_production.py`; production-note changes also invoke the corpus-level validator.

## Completion gate

ANKI-038 acceptance criteria are satisfied when the consolidated production workflow passes on this normalized corpus. Downstream ANKI-039 and ANKI-040 may then audit journal entries and formulas/calculations against this canonical normalized state.
