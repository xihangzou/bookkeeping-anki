# IND-03 Production QA

Issue: **ANKI-026 / #27**  
Chapter: **Industrial 03 — 労務費**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/IND-03.tsv`

## Result

- production Notes: **20**
- generated cards: **20**
- Cloze spans: **51**
- included ALPs: **24**
- mapped included ALPs: **24**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **4**
- journal-entry primary Notes: **4**
- formula Notes: **6**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No IND-03 production Note IDs existed before ANKI-026. IDs are allocated deterministically in primary canonical ALP order as `BK-IND-03-0001`–`BK-IND-03-0020`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The canonical inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Coherent multi-ALP Notes are used only where the source rules form one inseparable retrieval frame:

- `BK-IND-03-0007`: payment wage formula plus the basic-pay formula (`0007`, `0008`)
- `BK-IND-03-0013`: direct-worker direct and indirect labor formulas (`0014`, `0015`)
- `BK-IND-03-0017`: planned direct and indirect labor formulas (`0019`, `0020`)
- `BK-IND-03-0018`: wage-rate variance primary and alternate formulas (`0021`, `0022`)

The worked numerical examples 3-1 through 3-5 remain excluded as `DECORATIVE_EXAMPLE` because they only substitute numbers into active wage-payment, unpaid-wage adjustment, labor allocation, planned-rate, and variance rules.

## Recall-design review

### Labor-cost definition and classification

The opening Notes retrieve `労務費` as the consumption of labor for manufacturing and preserve that it includes factory salaries beyond direct workers' wages.

Direct versus indirect labor cost is tested by the actual decision criterion: whether labor consumption can be identified by specific product. The direct-worker boundary is then tested separately: only direct-work time becomes direct labor cost.

The indirect-labor category Note keeps the underlying items visible and retrieves the common classification `間接労務費`. A separate exception Note retrieves the key boundary that `賃金` alone can be either direct or indirect depending on the worker's activity.

### Wage payment and payroll withholding

The wage formula family preserves visible arithmetic operators:

`支払賃金 = 基本給 + 加給金`

`基本給 = 支払賃率 × 作業時間`

Repeated `基本給` is hidden with the same `c1` index so the second formula cannot leak the first operand.

The payroll-withholding Note keeps debit/credit labels visible and Clozes only account names. It retrieves `賃金`, `現金`, and `預り金` at account level, preserving the rule that employee tax/social-insurance deductions are liabilities until remitted.

The separate account-classification Note distinguishes `賃金` for factory workers from `給料` for factory office staff and supervisors.

### Accrual adjustment and actual labor allocation

The consumption-period formula is represented atomically as:

`当月賃金消費額（要支払額） = 当月支払額 + 当月末未払額 - 前月末未払額`

The unpaid-wage Note retains two journal entries in one same-index retrieval unit because showing either side would otherwise leak the reversal pattern:

- month start: `未払賃金 / 賃金`
- month end: `賃金 / 未払賃金`

Actual consumption rate keeps division visible and hides only the numerator and denominator. Direct-worker labor then reuses the same rate across direct-work and indirect-work time, with both repeated rate occurrences hidden together.

The direct-worker consumption entry retrieves `仕掛品` for direct work and `製造間接費` for indirect work. The indirect-worker Note preserves the cost-accounting exception that the full payable amount is indirect labor cost, no actual consumption rate is needed, and the whole amount goes to `製造間接費`.

### Planned consumption rate and wage-rate variance

`予定消費賃率` is retrieved as the pre-established hourly rate used for direct workers. Planned direct and indirect labor formulas are integrated because they differ only in the corresponding work-time operand.

The wage-rate variance Note integrates the two equivalent formulas while preserving all arithmetic operators:

`予定消費賃金 - 実際消費賃金（要支払額）`

`（予定消費賃率 - 実際消費賃率） × 実際作業時間`

A separate direction Note retrieves adverse debit variance when planned wages are below actual wages and favorable credit variance in the reverse case.

Year-end disposal is tested through account-level journal entries rather than broad action Clozes: adverse variance debits `売上原価`, while favorable variance credits `売上原価`.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/IND-03.tsv`.

## Deterministic validator

`scripts/validate_ind03_production.py` checks:

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
- direct/indirect labor cost-accounting treatment anchors
- exact canonical exclusion family

Expected output:

```text
IND-03 production validation: PASS
notes=20 cards=20 cloze_spans=51 included_alps=24 mapped=24 unmapped=0
multi_alp_notes=4 journal_entry_notes=4 formula_notes=6 canonical_exclusions=1
account_level_journal_cloze=pass minimal_cloze_scope=pass formula_atomicity=pass cost_accounting_treatment=pass visible_answer_leakage=0 deterministic_order=pass
```
