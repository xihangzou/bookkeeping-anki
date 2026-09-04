# COM-05 Production QA

Issue: **ANKI-012 / #13**  
Chapter: **Commercial 05 — 有価証券**  
Rules: current living `SPEC.md`, `rules/*.md`, and `rules/recall_precision_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/COM-05.tsv`

## Result

- production Notes: **38**
- generated cards: **38**
- Cloze spans: **101**
- included ALPs: **48**
- mapped included ALPs: **48**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **9**
- journal-entry primary Notes: **4**
- formula Notes: **7**
- decorative-example exclusions: **2**
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No COM-05 production Note IDs existed before ANKI-012. IDs are allocated deterministically in primary canonical ALP order as `BK-COM-05-0001`–`BK-COM-05-0038`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The ANKI-003 inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Coherent multi-ALP Notes are used only where the relationship is the recall unit itself:

- `BK-COM-05-0001`: stock/bond economic-character and recovery comparison (`0001`–`0002`)
- `BK-COM-05-0018`: investment-income account and cash-equivalent treatment (`0019`–`0020`)
- `BK-COM-05-0020`: accrued-interest definition and buyer-to-seller allocation (`0022`–`0023`)
- `BK-COM-05-0026`: trading-security valuation gain/loss formulas (`0029`–`0030`)
- `BK-COM-05-0027`: netting plus profit-to-equity linkage (`0031`–`0032`)
- `BK-COM-05-0028`: held-to-maturity valuation plus amortized-cost condition (`0033`–`0034`)
- `BK-COM-05-0030`: amortization entry plus carrying amount (`0036`–`0037`)
- `BK-COM-05-0036`: next-period trading-security methods and mechanics (`0043`–`0045`)
- `BK-COM-05-0038`: other-securities wash-only rule and rationale (`0047`–`0048`)

The two canonical EXCLUDE rows are numerical worked examples and remain excluded as `DECORATIVE_EXAMPLE`.

## Recall-design review

### Minimal lexical scope

The batch applies the current ANKI-AUDIT-011 specialization from initial generation:

- canonical account names and method names are targeted directly where identification is exam-useful;
- fixed contextual words remain visible where they already identify the answer class;
- broad action phrases such as `仕訳を行う`, `仕訳を行わない`, and `処理する` are not Cloze answers;
- explanatory tails and numerical examples are kept out of active recall unless they change the accounting rule.

### Journal entries

Journal syntax remains visible and account names are individually Clozed with the same `c1`.

Representative forms:

- seller accrued interest: `（貸）{{c1::有価証券利息}}`
- buyer accrued interest: `（借）{{c1::有価証券利息}}` and `（貸）{{c1::有価証券利息}}`
- amortized-cost adjustment: `（借）{{c1::満期保有目的の債券}}／（貸）{{c1::有価証券利息}}`
- other-securities valuation: `（借）{{c1::その他有価証券}}／（貸）{{c1::その他有価証券評価差額金}}` and the reverse entry for a decline

### Formulas and measurement

Formula operators remain visible and operands are itemized:

- acquisition cost = purchase price + incidental costs
- average unit cost = aggregate acquisition cost / aggregate shares
- sale cost = shares sold × average unit cost
- bond price = face amount / 100 × price per ¥100
- coupon interest = face amount × annual rate × months / 12
- trading-security valuation gain/loss formulas
- straight-line amortized-cost adjustment formula

### High-yield classification structure

The chapter-wide holding-purpose and year-end valuation matrices are retained as coherent same-card recall units because splitting them would remove the comparison relationship the source is testing.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact source anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/COM-05.tsv`.

## Deterministic validator

`scripts/validate_com05_production.py` checks:

- exact field order and deterministic stable IDs
- pinned source provenance
- Part/Chapter/primary Section consistency
- required deterministic tags and lifecycle
- c1-only generation
- exact-once INCLUDE-ALP mapping
- canonical inventory immutability
- local duplicate rendered text
- visible-answer leakage
- broad/non-atomic Cloze answers
- account-level journal-entry Clozes
- required formula, valuation, amortized-cost, and next-period precision forms
- decorative exclusion count

Expected output:

```text
COM-05 production validation: PASS
notes=38 cards=38 cloze_spans=101 included_alps=48 mapped=48 unmapped=0
multi_alp_notes=9 journal_entry_notes=4 formula_notes=7 decorative_exclusions=2
account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass visible_answer_leakage=0 deterministic_order=pass
```
