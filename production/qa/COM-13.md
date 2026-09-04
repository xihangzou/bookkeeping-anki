# COM-13 Production QA

Issue: **ANKI-020 / #21**  
Chapter: **Commercial 13 — 財務諸表**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/COM-13.tsv`

## Result

- production Notes: **39**
- generated cards: **39**
- Cloze spans: **116**
- included ALPs: **41**
- mapped included ALPs: **41**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **1**
- journal-entry primary Notes: **4**
- formula Notes: **7**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No COM-13 production Note IDs existed before ANKI-020. IDs are allocated deterministically in primary canonical ALP order as `BK-COM-13-0001`–`BK-COM-13-0039`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The canonical inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

One coherent multi-ALP Note is used:

- `BK-COM-13-0028`: the one-year display rules for held-to-maturity bonds, borrowings, and long-term prepaid expenses (`ALP-COM-13-0028`–`0030`).

The comprehensive B/S worked example remains excluded as `DECORATIVE_EXAMPLE` because it combines already-covered adjustment and presentation rules without adding a distinct retrieval operation.

## Recall-design review

### Financial-statement foundations

The opening Notes distinguish B/S from P/L by reporting objective, preserve the two core accounting equations, retrieve the retained-earnings linkage, and encode the closing sequence as one ordered recall unit.

The post-closing distinction keeps income-statement accounts and balance-sheet accounts in one visible frame. The pure-profit/pure-loss closing Note uses account-level masking with debit/credit labels and separators visible.

### Accrual and deferral accounts

The four temporal adjustment accounts are retrieved as one canonical set. Deferral versus accrual is tested by the accounting logic rather than by a broad action phrase.

The two adjustment-entry Notes use concrete source-backed rent accounts so the learner retrieves account selection directly:

- prepayment and unearned-revenue entries for deferral;
- accrued-expense and accrued-revenue entries for accrual.

The next-period treatment is retrieved with the canonical label `再振替仕訳`.

### Profit-and-loss presentation

The batch distinguishes ledger account names from P/L presentation names, including `売上→売上高`, `仕入→売上原価`, and the debit/credit presentation of foreign-exchange differences.

Account-form versus report-form P/L is separated by the retrieval dimensions that matter: debit/credit placement versus vertical step-profit presentation.

Step-profit formulas are split into separate Notes where combining them would expose one formula's operand as another formula's visible result. Operators remain visible, while operands are Clozed atomically.

The classification Notes retrieve representative category decisions for SG&A, non-operating income/expense, special gains/losses, inventory-related losses, and allowance expense presentation.

### Balance-sheet presentation

The B/S structure Note retrieves the principal current/fixed and net-asset sections. Current/noncurrent classification is authored as a two-stage process:

1. apply the normal operating-cycle criterion first;
2. apply the one-year criterion only to items outside that cycle.

The operating-cycle Note preserves the important exception that operating-cycle items remain current even when the period exceeds one year.

The one-year presentation Note integrates three tightly related display mappings in one frame: held-to-maturity securities, borrowings, and long-term prepaid expenses.

Contra-asset presentation and the three fixed-asset categories are tested separately to avoid mixing different classification decisions.

### Statement of shareholders' equity

The S/S Notes retrieve the canonical statement name, core row progression, total-equity effects of internal transfers versus dividends/capital increases/net income, and the reconciliation from S/S closing balances to B/S net assets.

### Monthly closing

The monthly-closing section retrieves the definition, monthly depreciation formulas, the reason the cost-of-goods-sold method can accelerate monthly closes, the monthly retirement-benefit provision entry, and the prepaid-expense monthly workflow.

The prepaid-expense workflow uses account-level journal masking and retrieves `不要` for the next-month reversing entry instead of a broad action Cloze such as `仕訳を行わない`.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/COM-13.tsv`.

## Deterministic validator

`scripts/validate_com13_production.py` checks:

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
- formula/operator atomicity and required precision forms
- exact canonical exclusion family

Expected output:

```text
COM-13 production validation: PASS
notes=39 cards=39 cloze_spans=116 included_alps=41 mapped=41 unmapped=0
multi_alp_notes=1 journal_entry_notes=4 formula_notes=7 canonical_exclusions=1
account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass formula_atomicity=pass visible_answer_leakage=0 deterministic_order=pass
```
