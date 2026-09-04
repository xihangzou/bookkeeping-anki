# COM-06 Production QA

Issue: **ANKI-013 / #14**  
Chapter: **Commercial 06 — 有形固定資産**  
Rules: current living `SPEC.md`, `rules/*.md`, and `rules/recall_precision_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/COM-06.tsv`

## Result

- production Notes: **40**
- generated cards: **40**
- Cloze spans: **88**
- included ALPs: **44**
- mapped included ALPs: **44**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **4**
- journal-entry primary Notes: **9**
- formula Notes: **10**
- decorative-example exclusions: **1**
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No COM-06 production Note IDs existed before ANKI-013. IDs are allocated deterministically in primary canonical ALP order as `BK-COM-06-0001`–`BK-COM-06-0040`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The ANKI-003 inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Coherent multi-ALP Notes are used only where the relationship is the recall unit itself or where separate Notes would duplicate the same rule:

- `BK-COM-06-0016`: fixed-asset disposal gain/loss plus the shared carrying-amount formula (`0016`, `0031`)
- `BK-COM-06-0027`: revenue-versus-capital expenditure classification plus mixed-repair allocation (`0027`, `0028`)
- `BK-COM-06-0030`: direct/indirect depreciation methods plus indirect-method presentation (`0032`, `0033`)
- `BK-COM-06-0033`: the shared partial-year month-proration rule for straight-line and declining-balance methods (`0036`, `0038`)

The canonical EXCLUDE row is a numerical worked-example family and remains excluded as `DECORATIVE_EXAMPLE`.

## Recall-design review

### Minimal lexical scope

The batch follows the current recall-precision specializations:

- canonical account, method, and classification labels are targeted directly where identification is exam-useful;
- fixed contextual words remain visible where they already identify the answer class;
- broad action phrases such as `処理する` and `計上する` are not Cloze answers;
- numerical worked examples and explanatory tails remain outside active recall unless they change the accounting rule.

### Journal entries

Debit/credit syntax remains visible and account names are Clozed at account level with the same `c1` for each coherent entry.

Representative forms:

- construction in progress: `（借）{{c1::建設仮勘定}}／（貸）現金等`
- installment interest allocation: `（借）{{c1::支払利息}}／（貸）{{c1::前払利息}}`
- alternative installment closing adjustment: `（借）{{c1::前払利息}}／（貸）{{c1::支払利息}}`
- insurance settlement: `（借）{{c1::未収入金}}／（貸）{{c1::未決算}}`
- inventory casualty: `（借）{{c1::火災損失}}／（貸）{{c1::仕入}}`

Where the counteraccount is generic by source design, it remains visible rather than forcing an ambiguous Cloze. For example, direct-reduction compression uses `（貸）対象固定資産` while the canonical `固定資産圧縮損` account is recalled.

### Formulas and measurement

Formula operators remain visible and operands are itemized:

- acquisition cost = purchase consideration + incidental costs
- installment price = cash price + interest
- per-payment interest = prepaid-interest amount / number of payments
- disposal gain/loss and carrying amount
- retirement and discard losses
- straight-line, declining-balance, and units-of-production depreciation
- 200% declining-balance rate
- depreciation guarantee and revised-depreciation formulas

For `200%定率法の償却率＝（1÷耐用年数）×200%`, the fixed `200%` remains visible because the method name already supplies that multiplier. The independently useful formula operand `耐用年数` is the Cloze target, consistent with minimal lexical scope and visible operator structure.

### Method and exception discrimination

The chapter's high-yield distinctions remain compact same-card recall units:

- removal from use (`除却`) versus physical discard (`廃棄`)
- revenue expenditure / repair expense versus capital expenditure / capitalization
- direct versus indirect depreciation recording
- straight-line versus declining-balance versus units-of-production methods
- month proration for straight-line/declining-balance versus no proration for units-of-production
- 10%-residual declining-balance rule versus 200% declining-balance guarantee/revision mechanics

### Duplicate-control decisions

The carrying-amount formula appears both in the fixed-asset disposal discussion and the depreciation section. It is represented once in active recall through `BK-COM-06-0016`, mapped to both canonical ALPs, instead of creating a duplicate rendered card.

The same principle is applied to the shared partial-year month-proration rule and the direct/indirect-method presentation rule, while preserving exact canonical ALP coverage.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/COM-06.tsv`.

## Deterministic validator

`scripts/validate_com06_production.py` checks:

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
- account-level journal-entry Clozes
- formula/operator atomicity and required precision forms
- decorative exclusion count

Expected output:

```text
COM-06 production validation: PASS
notes=40 cards=40 cloze_spans=88 included_alps=44 mapped=44 unmapped=0
multi_alp_notes=4 journal_entry_notes=9 formula_notes=10 decorative_exclusions=1
account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass formula_atomicity=pass visible_answer_leakage=0 deterministic_order=pass
```
