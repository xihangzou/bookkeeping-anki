# IND-04 Production QA

Issue: **ANKI-027 / #28**  
Chapter: **Industrial 04 — 経費**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/IND-04.tsv`

## Result

- production Notes: **17**
- generated cards: **17**
- Cloze spans: **47**
- included ALPs: **17**
- mapped included ALPs: **17**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **0**
- journal-entry primary Notes: **1**
- formula Notes: **2**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs and coverage

No IND-04 production Note IDs existed before ANKI-027. IDs are allocated deterministically in canonical ALP order as `BK-IND-04-0001`–`BK-IND-04-0017`.

Each included ALP maps exactly once to the correspondingly numbered production Note. The canonical inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

The worked examples 4-1 through 4-4 remain excluded as `DECORATIVE_EXAMPLE` because they only substitute numbers into the active rules for paid, monthly, measured, and incurred expenses.

## Recall-design review

### Expense definition and classification

The opening Notes retrieve the definition of `経費`, distinguish `直接経費` from `間接経費` by product traceability, and actively recall the seven representative expense categories with separate atomic Cloze spans.

`外注加工賃` and `特許権使用料` are separately recalled as representative direct expenses. Direct versus indirect cost flow is tested through the debit-side destination accounts: `仕掛品` for direct expenses and `製造間接費` for indirect expenses.

### Expense-consumption measurement

The four measurement classes are recalled as `支払経費`, `月割経費`, `測定経費`, and `発生経費`.

Paid-expense formulas keep arithmetic operators visible and Cloze only the operands:

- unpaid adjustment: 当月支払額 − 前月未払額 + 当月未払額
- prepaid adjustment: 当月支払額 + 前月前払額 − 当月前払額

The month-opening/month-end adjustment Note keeps debit/credit syntax visible and retrieves only `未払経費` and `前払経費` as the period-adjustment accounts.

Monthly, measured, and incurred expenses each retain the source measurement rule in active `Text`: annual monthly allocation uses 12 months, measured expenses include fixed/basic charges when applicable, and incurred expenses use the actual amount incurred in the month.

### Three bookkeeping methods

The batch recalls all three canonical bookkeeping methods and then tests each method's distinct posting route:

1. individual expense accounts: record each expense in its own account, then transfer direct/indirect amounts to `仕掛品` / `製造間接費`;
2. single expense account: aggregate occurrence amounts in `経費勘定`, then split consumption to `仕掛品` / `製造間接費`;
3. no expense account: bypass expense accounts and directly post direct/indirect amounts to `仕掛品` / `製造間接費`.

The final comparison Note tests that the methods differ in the `経費勘定の経由方法`, while the final cost amounts accumulated in work in process and manufacturing overhead are the same.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact source anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/IND-04.tsv`.

## Deterministic validator

`scripts/validate_ind04_production.py` checks:

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
- account-level journal-entry masking / rejection of whole-entry Clozes
- formula/operator atomicity and required precision forms
- exact canonical exclusion family

Expected output:

```text
IND-04 production validation: PASS
notes=17 cards=17 cloze_spans=47 included_alps=17 mapped=17 unmapped=0
multi_alp_notes=0 journal_entry_notes=1 formula_notes=2 canonical_exclusions=1
account_level_journal_cloze=pass minimal_cloze_scope=pass formula_atomicity=pass cost_accounting_treatment=pass visible_answer_leakage=0 deterministic_order=pass
```
