# COM-16 Production QA

Issue: **ANKI-023 / #24**  
Chapter: **Commercial 16 — 製造業会計**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/COM-16.tsv`

## Result

- production Notes: **23**
- generated cards: **23**
- Cloze spans: **62**
- included ALPs: **24**
- mapped included ALPs: **24**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **1**
- journal-entry primary Notes: **3**
- formula Notes: **5**
- cost-accounting primary Notes: **5**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No COM-16 production Note IDs existed before ANKI-023. IDs are allocated deterministically in canonical ALP order as `BK-COM-16-0001`–`BK-COM-16-0023`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The canonical inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

One multi-ALP Note is used:

- `BK-COM-16-0002`: manufacturing closing workflow plus the monthly-costing premise (`ALP-COM-16-0002`, `ALP-COM-16-0003`).

All other ALPs remain separate because they introduce a distinct journal, measurement, formula, cost-flow decision, exception, or financial-statement presentation rule. The worked numerical comprehensive example remains excluded as `DECORATIVE_EXAMPLE` because its numbers only instantiate already-active rules.

## Recall-design review

### Manufacturing closing and monthly boundary

The opening Notes retrieve the canonical `製造業会計` label, the one-month costing period, the monthly sequence of manufacturing cost / cost of goods sold / cost variance determination, and the rule that monthly closing does not perform revenue/expense closing entries.

### Materials, labor, and manufacturing expenses

Material consumption tests the treatment-changing destination: direct material cost goes to `仕掛品`, while indirect material cost goes to `製造間接費`. The material book-inventory formula keeps month/timing modifiers visible and Clozes only the atomic operands.

Normal material loss is retained as a manufacturing-overhead cost-flow rule with account-level journal masking. Wage consumption uses the accrual relationship `当月支払＋月末未払－前月末未払`, with the timing modifiers visible. Direct and indirect labor destinations are separated explicitly.

Retirement-benefit expense retrieves the annual-estimate monthly allocation and the manufacturing-department discriminator. Depreciation retrieves monthly recognition and functional allocation between manufacturing overhead and the selling/general-administrative side.

### Manufacturing overhead and variance

Predetermined overhead allocation retrieves `予定配賦額`, `仕掛品`, and `原価差異` in one coherent cost-flow frame. The variance formula is kept separate from the favorable/unfavorable direction card so no formula operand is leaked by a visible comparison branch.

The variance formula keeps the subtraction operator visible and Clozes only `予定配賦額` and `実際発生額`. A separate classification Note tests unfavorable/borrow-side versus favorable/credit-side direction.

### Work in process, finished goods, and cost of goods sold

The batch preserves the full manufacturing cost chain:

- current-period manufacturing cost = direct materials + direct labor + predetermined manufacturing overhead;
- cost of goods manufactured = beginning WIP + current manufacturing cost − ending WIP;
- completion transfers cost from WIP to finished goods;
- current-period COGS = beginning finished goods + cost of goods manufactured − ending finished goods;
- sale transfers finished-goods cost to COGS;
- month-end cost variance is assigned to COGS, with distinct entries for unfavorable and favorable variance.

Journal syntax remains visible and the account names are individually Clozed with the same `c1`, preventing counterpart leakage.

### Financial statements

The P/L Note retrieves post-variance COGS and the selling/general-administrative presentation of depreciation and retirement-benefit expense that are not manufacturing costs. The B/S Note retrieves materials, WIP, and finished goods as inventory, including aggregate `棚卸資産` presentation.

The final Note preserves the linkage from current net income to retained earnings while leaving the general accounting equation visible to avoid duplicating a foundational formula card.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/COM-16.tsv`.

## Deterministic validator

`scripts/validate_com16_production.py` checks:

- exact field order and deterministic stable IDs
- pinned source provenance
- Part/Chapter/primary Section consistency
- required deterministic tags and lifecycle
- `c1`-only generation
- exact deterministic Note-to-ALP mapping and exact-once INCLUDE-ALP coverage
- canonical inventory immutability
- local duplicate rendered text
- visible-answer leakage
- broad/non-atomic Cloze answers
- account-level journal-entry masking whenever debit/credit syntax appears
- formula/operator atomicity
- manufacturing-cost-flow precision forms
- exact canonical exclusion family

Expected output:

```text
COM-16 production validation: PASS
notes=23 cards=23 cloze_spans=62 included_alps=24 mapped=24 unmapped=0
multi_alp_notes=1 journal_entry_notes=3 formula_notes=5 cost_accounting_notes=5 canonical_exclusions=1
account_level_journal_cloze=pass manufacturing_cost_flow=pass formula_atomicity=pass minimal_cloze_scope=pass visible_answer_leakage=0 deterministic_order=pass
```
