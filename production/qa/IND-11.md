# IND-11 Production QA

Issue: **ANKI-034 / #35**  
Chapter: **Industrial 11 — 標準原価計算**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/IND-11.tsv`

## Result

- production Notes: **29**
- generated cards: **29**
- Cloze spans: **83**
- included ALPs: **31**
- mapped included ALPs: **31**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **1**
- journal-entry primary Notes: **0**
- formula Notes: **17**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- non-atomic parallel-term Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No IND-11 production Note IDs existed before ANKI-034. IDs are allocated deterministically in primary canonical ALP order as `BK-IND-11-0001`–`BK-IND-11-0029`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The canonical inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Most ALPs remain one-to-one with a Note. One coherent comparison Note integrates the three ledger-plan ALPs because they are best recalled on the same comparison axis:

- `BK-IND-11-0029`: single-plan rule, partial-plan rule, and their common/different ledger treatment (`ALP-IND-11-0029`, `ALP-IND-11-0030`, `ALP-IND-11-0031`)

Worked examples 11-1 through 11-5 remain excluded as `DECORATIVE_EXAMPLE` because they substitute specific numbers into active standard-cost, variance-analysis, and ledger rules without adding a new decision branch.

## Recall-design review

### Standard costing, objectives, and workflow

The opening Notes distinguish actual costing from standard costing by the treatment-changing dimension: actual costing may use planned prices while retaining actual quantities, whereas standard costing also establishes quantity/work-time standards. Standard costing is tied directly to variance analysis and cost control rather than testing a generic definition in isolation.

The production-flow Note keeps the standard-costing frame visible and uses separate same-index atomic spans for the sequence-critical stages: setting cost standards, calculating standard and actual cost, calculating/analyzing variances, reporting/improvement, and year-end variance disposal.

`原価標準` and `標準原価` are retrieved on a single comparison axis: per-unit target cost versus the target manufacturing cost applied to the period's actual production.

### Cost standards and WIP measurement

The core formulas keep operators visible and Cloze only individual operands:

- standard cost = cost standard × actual production quantity
- standard direct materials = standard price × standard quantity
- standard direct labor = standard wage rate × standard direct labor time
- standard manufacturing overhead = standard allocation rate × standard operating level
- completed-goods standard cost = per-unit cost standard × completed quantity

For WIP, beginning-point material input retrieves actual physical units for materials and conversion-equivalent units for direct labor/manufacturing overhead. The average-input exception separately retrieves completed-unit equivalents for materials as well.

The standard-setting quality Note retrieves `客観的` and `達成可能` rather than broad explanatory clauses.

### Direct-material and direct-labor variances

Variance classification is one coherent classification card with each independently meaningful variance name in its own atomic Cloze span. Direct-material and direct-labor total, price/rate, quantity/time formulas preserve subtraction and multiplication operators while masking only the formula operands.

The formula frames preserve the economically important evaluation bases: price/rate variances use actual quantity/time, while quantity/time variances use standard price/rate.

### Manufacturing-overhead variances

Flexible-budget overhead variance formulas separately retrieve the operands for budget, volume, and efficiency variances. Variable- and fixed-efficiency variances remain distinct because the applicable rate changes the calculation.

Fixed-budget analysis retains the common standard-allocation-rate basis in both budget allowance and volume variance. The 4-way method retrieves its canonical label from a visible definition; the 3-way Note tests the two distinct consolidation methods without duplicating the underlying variance formulas.

### P&L treatment and ledger plans

Year-end standard-cost variances are retrieved as an adjustment to `売上原価`; adverse variances are `加算` and favorable variances are `減算`.

The single/partial plan Note uses one visible comparison frame. It retrieves:

- single plan: current input at `標準原価`, variance in `各原価要素勘定`;
- partial plan: current input at `実際原価`, variance in `仕掛品勘定`;
- common rule: completed-goods transfer and ending WIP at `標準原価`.

This integration avoids three near-duplicate cards while materially preserving all three mapped ALPs.

### Minimal scope, parallel atomicity, and leakage

The batch applies the current consolidated rules:

- each independently meaningful list/parallel term is a separate Cloze span even when all spans share `c1`;
- formula operators remain visible and formulas mask individual operands;
- broad targets such as `仕訳を行う`, `処理する`, `あり`, and `なし` are not used;
- same-index grouping keeps tightly coupled formula/comparison operands on one generated card;
- each card retains a visible accounting subject and answer class;
- no 2+ character Cloze answer appears verbatim in the visible portion of the same rendered card.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/IND-11.tsv`.

## Deterministic validator

`scripts/validate_ind11_production.py` checks:

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
- parallel-term atomicity
- formula/operator atomicity and required precision forms
- exact canonical exclusion family

Expected output:

```text
IND-11 production validation: PASS
notes=29 cards=29 cloze_spans=83 included_alps=31 mapped=31 unmapped=0
multi_alp_notes=1 journal_entry_notes=0 formula_notes=17 canonical_exclusions=1
minimal_cloze_scope=pass parallel_term_atomicity=pass formula_atomicity=pass cost_accounting_treatment=pass visible_answer_leakage=0 deterministic_order=pass
```
