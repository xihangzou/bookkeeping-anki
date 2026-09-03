# COM-01 Production QA

Status: **PASS target — v1.8 precision / ALP-containment audit**

## Governance and contract

- repository governance: `GOVERNANCE.md`
- current general specification/rules/schema: latest merged `SPEC.md`, `rules/*.md`, and `schema/note_schema.yaml`
- chapter style reference: FND-00 v1.6 active cards for short answer spans, visible context, and integrated completeness
- canonical ALP shard: `inventory/topic_inventory/COM-01.tsv`
- source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`, Commercial chapter 01

## Coverage and lifecycle

| Metric | Result |
|---|---:|
| Canonical included ALPs | 52 |
| Approved production Notes | 38 |
| Generated Cloze cards | 38 |
| Active Cloze spans | 99 |
| Included ALPs mapped | 52 |
| Unmapped included ALPs | 0 |
| ALPs mapped more than once | 0 |
| Approved multi-ALP Notes | 14 |
| Promoted pilot Note IDs | 18 |
| Reserved pilot-only duplicate-application IDs | 5 |
| Deprecated production rows | 0 |
| Excluded decorative-example rows | 3 |
| Exact visible-answer leakage (2+ chars) | 0 |

The increase from 87 to 99 Cloze spans restores mapped ALP detail and fully hides reused formula terms without adding cards.

## v1.8 user-directed corrections

- `BK-COM-01-0026`: Cloze `仕入`・`売上`・`繰越商品` as well as `決算整理`.
- `BK-COM-01-0008`: Cloze the two compact closing entries themselves rather than only debit/credit direction.
- `BK-COM-01-0028` and `BK-COM-01-0009`: state `売上原価対立法` visibly.
- `BK-COM-01-0035`: hide the `売上原価` term in the gross-profit formula; both reused occurrences are same-index Clozes.
- `BK-COM-01-0036`: use `{{c1::数量}}のみ`, keeping `のみ` outside the Cloze.
- `BK-COM-01-0016`: replace broad sentence-length cost descriptions with short discriminators `購入`・`販売`・`未販売在庫`.
- `BK-COM-01-0038`: leave definitions visible and Cloze the names `帳簿棚卸数量`・`実地棚卸数量`.

## 52-ALP material-proposition audit

All 52 canonical included ALPs were re-read against the inventory summaries, with source checks where necessary. Material propositions are now recoverable from active Note `Text`, rather than being left only in `Extra`.

Additional restorations beyond the explicit user list:

- `ALP-COM-01-0002`: `費用` / `収益` classification remains visible around the `仕入` / `売上` account Clozes.
- `ALP-COM-01-0004`: the pre-delivery rule explicitly states no `仕入`, asset recognition as `前払金`, and the receipt-time transfer.
- `ALP-COM-01-0005`: purchase returns explicitly use the reverse purchase entry and reduce both accounts.
- `ALP-COM-01-0007` / `0008`: transport, insurance, packing and other company-borne ancillary costs remain visible, together with the complete purchase-cost formula.
- `ALP-COM-01-0010`: all three 三分法 accounts are direct recall targets.
- `ALP-COM-01-0011` / `0044`: both beginning- and end-inventory closing entries plus their add/remove logic are present on one card.
- `ALP-COM-01-0014` / `0015`: 売上原価対立法 is named and its three account classes plus purchase-time inventory recognition remain present.
- `ALP-COM-01-0019` / `0020`: 商品有高帳 directly recalls quantity, cost, subsidiary-ledger status, and cost-basis issue recording.
- `ALP-COM-01-0023` / `0024`: FIFO contains both the explicit first-in premise and old/new cost-layer consequence.
- `ALP-COM-01-0032` / `0033`: both COGS and gross-profit formulas are complete; reused `売上原価` is hidden in both positions.
- `ALP-COM-01-0035` / `0036`: purchase scope, sale scope, unsold-inventory difference, and matching logic are all in `Text`.
- `ALP-COM-01-0040` / `0042`: physical shrinkage, shrinkage expense, and value loss are distinguished with their triggering conditions.
- `ALP-COM-01-0046` / `0047`: the shrinkage quantity formula and fully expanded shrinkage-loss formula are both retained.
- `ALP-COM-01-0049` / `0052`: the lower-of-cost condition and complete evaluated-ending-inventory formula are both retained.

## Style and recall-design checks

- all approved Notes use only `c1`, so 38 Notes = 38 generated cards;
- method names are visible when otherwise ambiguous;
- definitions normally remain visible while technical names are Clozed;
- parenthetical classification is avoided when natural visible prose works better;
- function words such as `のみ` remain outside the Cloze unless they are the actual distinction;
- normal Clozes remain lexical or short discriminators;
- compact whole-journal-entry Clozes are allowed only where the whole entry is the retrieval target;
- repeated same-answer spans are limited to deliberate formula reuse and all occurrences remain hidden;
- exact visible-answer leakage remains zero.

## Stable IDs and source traceability

- all 38 production Note IDs are unchanged;
- 18 reviewed pilot IDs remain promoted without renumbering;
- 20 production IDs remain `BK-COM-01-0024`–`BK-COM-01-0043`;
- the 5 reserved pilot-only IDs remain absent;
- every `ALP_IDs` list resolves to canonical `INCLUDE` rows and remains source-ordered;
- pinned source repository, commit, path, part, chapter, and section traceability remain unchanged.

## Deterministic validation

Run:

```text
python scripts/validate_com01_production.py
```

Expected output:

```text
COM-01 v1.8 production validation: PASS
notes=38 included_alps=52 mapped=52 unmapped=0
generated_cards=38 cloze_spans=99 visible_answer_leakage=0 multi_alp_notes=14
promoted_pilot_ids=18 reserved_pilot_only_ids=5
journal_entry_notes=8 formula_notes=10
```
