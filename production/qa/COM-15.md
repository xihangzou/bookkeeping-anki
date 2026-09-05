# COM-15 Production QA

Issue: **ANKI-022 / #23**  
Chapter: **Commercial 15 — 連結会計**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/COM-15.tsv`

## Result

- production Notes: **44**
- generated cards: **50**
- Cloze spans: **110**
- included ALPs: **46**
- mapped included ALPs: **46**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **2**
- journal-entry primary Notes: **17**
- formula Notes: **9**
- financial-statement primary Notes: **5**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- generated-card visible-answer leakage for 2+ character answers: **0**
- non-atomic parallel-term Clozes: **0**
- hidden arithmetic operators: **0**
- broad/non-atomic targeted action Clozes: **0**
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No COM-15 production Note IDs existed before ANKI-022. IDs are allocated deterministically in canonical ALP order as `BK-COM-15-0001`–`BK-COM-15-0044`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The canonical inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Two coherent multi-ALP Notes are used:

- `BK-COM-15-0003`: consolidation workflow plus the consolidation-work-sheet purpose (`ALP-COM-15-0003`, `ALP-COM-15-0004`).
- `BK-COM-15-0040`: discounted intragroup notes plus the split treatment of bank-discounted and hand-held portions (`ALP-COM-15-0041`, `ALP-COM-15-0042`).

All other INCLUDE ALPs remain separate because they introduce a distinct definition, formula, journal, recognition boundary, carry-forward rule, noncontrolling-interest adjustment, or financial-statement presentation rule. The comprehensive numerical examples remain excluded as `DECORATIVE_EXAMPLE` because they instantiate already-active rules without adding a new retrieval operation.

## Recall-design review

### Consolidation basics and capital consolidation

The opening Notes retrieve the consolidated-financial-statement label, the parent/subsidiary criterion, the simple-sum-plus-consolidation-adjustment workflow, and the consolidation worksheet. Consolidated P/L and B/S presentation rules are kept distinct from the parent-attributable-income relation.

Full-ownership investment/equity elimination uses account-level journal masking: `資本金`, `資本剰余金`, `利益剰余金`, and `子会社株式` are separate same-index Cloze spans. Goodwill measurement is a separate formula card with visible subtraction, while positive investment-elimination difference recognition tests the minimal canonical labels `のれん` and `資産`.

Beginning entries, goodwill amortization, prior-period profit/loss carry-forward, and intragroup dividend elimination remain separate retrieval units so current-period and cumulative consolidation adjustments are not conflated.

### Partial ownership and noncontrolling interests

Noncontrolling-shareholder definition, initial NCI measurement, partial-ownership goodwill, full subsidiary-equity elimination, NCI income attribution, dividend treatment, cumulative NCI carry-forward, and the ending-NCI check are each represented explicitly.

Journal entries keep debit/credit syntax visible and Cloze account names individually. Formula operators remain visible and only atomic operands are hidden.

### Intragroup transactions and unrealized profit

The ordinary intragroup sales/balance Note is split into three generated cards by meaning:

- `c1`: internal sales / cost of sales;
- `c2`: accounts payable / accounts receivable;
- `c3`: notes payable / notes receivable.

The intragroup financing Note is likewise split into principal, interest, and accrual pairs (`c1`/`c2`/`c3`). This avoids forcing six independent account names into one recall event while preserving one coherent ALP-level Note.

The batch separately tests the no-beginning-entry exception, downstream/upstream terminology, the external-sale realization boundary, ending-inventory elimination, both profit-rate and markup-rate unrealized-profit formulas, and beginning-inventory realization.

Land unrealized-profit elimination, land carry-forward, allowance elimination, and next-period allowance carry-forward remain distinct because they differ in persistence and in how prior-period profit effects enter retained earnings.

### Upstream adjustments

Upstream treatment first retrieves the structural distinction: subsidiary profit changes require an NCI-attributable adjustment. Inventory, land, and allowance cases then test the actual direction of the NCI journal entries. The land and allowance directions are kept on one comparison card because the direction reversal is the learning target and separate cards would expose the counterpart relationship.

Discounted intragroup notes keep the bank-discounted portion as external borrowing while hand-held internal notes are eliminated.

### Consolidated statement of changes in equity

The final Notes cover the purpose and components of the consolidated S/S, net presentation of NCI movements, linkage among consolidated P/L, S/S, and B/S, and the S/S-specific adjustment-account suffixes.

`BK-COM-15-0044` generates three cards: opening-balance suffixes (`c1`), dividend adjustment (`c2`), and NCI current-period movement (`c3`). Repeated `当期首残高` occurrences remain same-index because they express one shared naming rule.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/COM-15.tsv`.

## Deterministic validator

`scripts/validate_com15_production.py` checks:

- exact field order and deterministic stable IDs
- pinned source provenance
- Part/Chapter/primary Section consistency
- required deterministic tags and lifecycle
- exact Cloze-group architecture and generated-card count
- exact deterministic Note-to-ALP mapping and exact-once INCLUDE-ALP coverage
- canonical inventory immutability
- local duplicate rendered text
- generated-card visible-answer leakage
- broad/non-atomic Cloze answers
- parallel-term atomicity
- account-level journal-entry masking
- formula/operator atomicity
- critical capital-consolidation, NCI, intragroup, unrealized-profit, upstream, discounted-note, and consolidated-S/S precision forms
- exact canonical exclusion family

Expected output:

```text
COM-15 production validation: PASS
notes=44 cards=50 cloze_spans=110 included_alps=46 mapped=46 unmapped=0
multi_alp_notes=2 journal_entry_notes=17 formula_notes=9 financial_statement_notes=5 canonical_exclusions=1
account_level_journal_cloze=pass formula_atomicity=pass parallel_overload_split=pass minimal_cloze_scope=pass visible_answer_leakage=0 deterministic_order=pass
```
