# COM-01 Production QA

Status: **PASS target — v1.7 chapter-local Cloze-precision audit under the current recall-design rules**

## Governance and contract

- repository governance: `GOVERNANCE.md`
- current general specification/rules/schema: latest merged `SPEC.md`, `rules/*.md`, and `schema/note_schema.yaml`
- this chapter's applied audit state: v1.7 chapter-local Cloze-precision audit, using FND-00 v1.6 active cards as the style reference for answer granularity and visible context
- canonical ALP shard: `inventory/topic_inventory/COM-01.tsv`
- source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`, Commercial chapter 01

## Coverage and lifecycle

| Metric | Result |
|---|---:|
| Canonical included ALPs | 52 |
| Approved production Notes | 38 |
| Generated Cloze cards | 38 |
| Active Cloze spans | 87 |
| Included ALPs mapped | 52 |
| Unmapped included ALPs | 0 |
| ALPs mapped more than once | 0 |
| Approved multi-ALP Notes | 14 |
| Promoted pilot Note IDs | 18 |
| Reserved pilot-only duplicate-application IDs | 5 |
| Deprecated production rows | 0 |
| Excluded decorative-example rows | 3 |
| Exact visible-answer leakage (2+ chars) | 0 |

All 52 included ALPs remain represented without changing stable IDs or increasing card count. The reduction from 92 to 87 Cloze spans removes redundant or imprecise masking rather than source content.

## v1.7 precision changes

The chapter was re-audited against the mature FND-00 v1.6 card style:

- explanatory classifications stay visible when the accounting answer is the actual retrieval target;
- timing answers use short, named frames such as `{{c1::商品受入時}}` rather than broad explanatory clauses;
- acquisition-cost wording uses visible `当社負担の` context plus lexical `{{c1::仕入諸掛り}}`;
- process cards mask `{{c1::決算整理}}` rather than the full phrase `決算整理で算定する`;
- parenthetical account classifications such as `商品（資産）` / `商品売買益（収益）` are rewritten as visible syntax: `資産の {{c1::商品}}` / `収益の {{c1::商品売買益}}`;
- method-family cards no longer mask explanatory phrases such as `仮定計算` when the method names are the examinable answers;
- FIFO uses the compact discriminator pair `{{c1::古い原価層}}` / `{{c1::新しい原価層}}`;
- recognition and matching cards prefer named accounting concepts over sentence-length answers;
- bracketed text is forbidden inside active Cloze answers;
- exact visible-answer leakage remains zero.

User-directed corrections are locked into the validator for:

- `BK-COM-01-0024`: no separate `費用` / `収益` Clozes;
- `BK-COM-01-0002`: `{{c1::商品受入時}}` replaces the broader clause;
- `BK-COM-01-0005`: `当社負担の{{c1::仕入諸掛り}}`;
- `BK-COM-01-0026`: `{{c1::決算整理}}`;
- `BK-COM-01-0027`: no parenthetical `(資産)` / `(収益)` construction.

## Source-content preservation

The audit keeps the material proposition for every mapped ALP, including:

- 三分法の仕入・売上、認識時点、返品、仕入諸掛り、決算整理;
- 分記法の商品・商品売買益と利益関係;
- 売上原価対立法の3勘定、仕入時の資産認識、売上時の原価振替;
- 商品有高帳、FIFO・移動平均・総平均の使い分け;
- 月末棚卸高、売上原価、売上総利益;
- 棚卸減耗、低価評価、商品評価損、財務諸表表示.

## Stable IDs and source traceability

- all 38 production Note IDs are unchanged;
- 18 reviewed pilot IDs remain promoted without renumbering;
- 20 production IDs remain `BK-COM-01-0024`–`BK-COM-01-0043`;
- the 5 reserved pilot-only IDs remain absent;
- every `ALP_IDs` list resolves to canonical `INCLUDE` rows and remains source-ordered;
- pinned source repository, commit, path, part, chapter, and section traceability remain unchanged.

These are current lineage/source invariants under `GOVERNANCE.md`, not consequences of a permanently fixed v1.0 contract.

## Deterministic validation

Run:

```text
python scripts/validate_com01_production.py
```

Expected output:

```text
COM-01 v1.7 production validation: PASS
notes=38 included_alps=52 mapped=52 unmapped=0
generated_cards=38 cloze_spans=87 visible_answer_leakage=0 multi_alp_notes=14
promoted_pilot_ids=18 reserved_pilot_only_ids=5
journal_entry_notes=8 formula_notes=10
```
