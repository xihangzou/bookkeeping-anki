# IND-10 Production QA

Issue: **ANKI-033 / #34**  
Chapter: **Industrial 10 — 決算と財務諸表**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/IND-10.tsv`

## Result

- production Notes: **18**
- generated cards: **18**
- Cloze spans: **49**
- included ALPs: **18**
- mapped included ALPs: **18**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **0**
- journal-entry primary Notes: **0**
- formula Notes: **4**
- financial-statement Notes: **5**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No IND-10 production Note IDs existed before ANKI-033. IDs are allocated deterministically in canonical ALP order as `BK-IND-10-0001`–`BK-IND-10-0018`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`; this chapter does not require multi-ALP integration because each canonical learning point already forms a distinct coherent retrieval frame. The canonical inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

The worked numerical example remains excluded as `DECORATIVE_EXAMPLE`: it substitutes concrete figures into formulas and cost-flow relationships that are already active recall targets and introduces no additional decision branch or accounting treatment.

## Recall-design review

### Closing structure

The batch distinguishes annual and monthly closing directly, then tests the monthly transfer sequence from sales / cost of sales / selling and administrative expenses to monthly profit and from monthly operating profit to annual profit. The monthly profit ledger keeps debit/credit labels visible and retrieves the accounts that populate each side.

Annual closing tests the aggregation of twelve months of operating profit together with non-operating and extraordinary profit/loss items to arrive at net income. The annual-only exception is separately retrieved for entities that do not perform monthly closing.

### Selling and administrative expenses

Selling expenses and general administrative expenses are masked as separate same-index spans. This preserves parallel-term atomicity while recalling the classification pair together from visible functional definitions.

### Manufacturing financial statements

The production set retrieves the additional manufacturing statement, `製造原価報告書`, without duplicating the visible definition. Balance-sheet inventory presentation separately tests the three manufacturing inventories and the corresponding period-end balance used for each.

### Formula atomicity

All formulas keep arithmetic operators visible and mask individual operands only:

- adjusted-before-variance cost of sales: beginning finished goods + current cost of goods manufactured − ending finished goods;
- gross and operating profit relationships;
- cost of goods manufactured: current manufacturing costs + beginning work in process − ending work in process;
- material cost: beginning materials + current purchases − ending materials.

Repeated operands are left visible where masking them again would create leakage rather than a new retrieval operation.

### Cost variance and statement linkage

The P&L adjustment tests the direction only: unfavorable variance is added and favorable variance is deducted. The cost report versus P&L comparison retrieves `予定価格` versus `実際価格` with the treatment-changing variance context left visible.

The final procedure Note tests the manufacturing cost flow through `仕掛品` → `製品` → `売上原価`, with every repeated `売上原価` occurrence hidden under the same index so no sibling occurrence leaks the answer.

### Presentation-method atomicity

The manufacturing cost report presentation alternatives are represented as separate parallel spans: `材料費`・`労務費`・`経費` and `製造直接費`・`製造間接費`. Fixed canonical labels such as `販売費及び一般管理費` remain intact rather than being split artificially.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/IND-10.tsv`.

## Deterministic validator

`scripts/validate_ind10_production.py` checks:

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
- parallel-term lexical atomicity
- formula/operator atomicity and required formula forms
- closing, variance, balance-sheet, manufacturing-report, and cost-flow anchors
- exact canonical exclusion family

Expected output:

```text
IND-10 production validation: PASS
notes=18 cards=18 cloze_spans=49 included_alps=18 mapped=18 unmapped=0
multi_alp_notes=0 journal_entry_notes=0 formula_notes=4 financial_statement_notes=5 canonical_exclusions=1
minimal_cloze_scope=pass parallel_atomicity=pass formula_atomicity=pass closing_cost_flow=pass visible_answer_leakage=0 deterministic_order=pass
```
