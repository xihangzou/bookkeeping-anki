# IND-05 Production QA

Issue: **ANKI-028 / #29**  
Chapter: **Industrial 05 — 製造間接費**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/IND-05.tsv`

## Result

- production Notes: **26**
- generated cards: **26**
- Cloze spans: **61**
- included ALPs: **27**
- mapped included ALPs: **27**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **1**
- journal-entry primary Notes: **4**
- formula Notes: **12**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No IND-05 production Note IDs existed before ANKI-028. IDs are allocated deterministically in canonical ALP order as `BK-IND-05-0001`–`BK-IND-05-0026`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The canonical inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

One integration is used because the two propositions form one retrieval frame:

- `BK-IND-05-0006`: definition of planned allocation plus its two operational benefits (`ALP-IND-05-0006`, `ALP-IND-05-0007`). The method label is recalled while the speed and monthly-cost-stability benefits remain active visible context.

All other INCLUDE ALPs map one-to-one to production Notes. Numerical examples 5-1 through 5-3 remain excluded as `DECORATIVE_EXAMPLE` because they substitute numbers into already-active allocation, variance, and flexible-budget relationships rather than adding a distinct decision rule.

## Recall-design review

### Allocation flow and bases

The opening Notes preserve the reason allocation is necessary: manufacturing overhead cannot be directly traced to individual products, so it is accumulated and allocated using an allocation base.

The cost-flow journal keeps debit/credit syntax visible and Clozes only target account names. Indirect material, labor, and expense credits stay visible because the retrieval target is the manufacturing-overhead accumulation account and subsequent transfer to work in process.

The five representative allocation bases are split into separate atomic Cloze spans: direct material cost, direct labor cost, direct labor hours, machine hours, and production quantity. Their category frames remain visible.

### Actual and planned allocation formulas

All formulas keep operators visible and Cloze individual operands only:

- actual allocation rate = actual manufacturing-overhead incidence / total actual allocation-base quantity;
- actual amount allocated to a product = actual rate × that product's actual base quantity;
- planned allocation rate = annual planned manufacturing overhead / annual normal capacity;
- planned allocation amount = planned rate × actual operating level;
- manufacturing-overhead allocation variance = planned allocation amount − actual incidence.

Planned allocation is kept distinct from actual allocation. The default rule for job-order costing is directly retrieved as `予定配賦`.

### Allocation variance direction and accounting

Favorable/adverse direction is tested from the inequality itself:

- planned allocation < actual incidence → adverse / debit variance;
- planned allocation > actual incidence → favorable / credit variance.

Variance-transfer and year-end-disposition entries use account-level Clozes only. At year end the Note explicitly retrieves both the direction (`加算` / `減算`) and the corresponding cost-of-sales / allocation-variance accounts, while keeping debit/credit labels and separators visible.

### Cost control and variance analysis

The batch retrieves the core cost-control and variance-analysis chain:

- `原価管理` as comparison of target and actual cost followed by cause analysis and improvement;
- `予算許容額` as the target manufacturing-overhead amount corresponding to actual operating conditions;
- budget variance = budget allowance − actual incidence;
- volume variance = planned allocation amount − budget allowance;
- total allocation variance = budget variance + volume variance.

The formula-based flexible budget is represented with atomic operands:

`予算許容額 = 変動費率 × 実際操業度 + 固定費予算`

The related fixed-overhead rate, alternate volume-variance formula, and decomposition of the planned allocation rate into variable and fixed rates are separately retrievable because each is a distinct quantitative relationship used in variance analysis.

### Fixed budget and normal capacity

Fixed budget is tested by its defining discriminator: the budget allowance does not change with operating level and uses the manufacturing-overhead budget at normal capacity.

The final Note keeps `基準操業度` visible as the causal subject and retrieves the two quantities it materially affects: `予定配賦率` and `操業度差異`.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/IND-05.tsv`.

## Deterministic validator

`scripts/validate_ind05_production.py` checks:

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
- account-level journal-entry masking / rejection of whole-entry Clozes
- formula/operator atomicity and required precision forms
- core manufacturing-overhead allocation and variance-treatment anchors
- exact canonical exclusion family

Expected output:

```text
IND-05 production validation: PASS
notes=26 cards=26 cloze_spans=61 included_alps=27 mapped=27 unmapped=0
multi_alp_notes=1 journal_entry_notes=4 formula_notes=12 canonical_exclusions=1
account_level_journal_cloze=pass minimal_cloze_scope=pass parallel_atomicity=pass formula_atomicity=pass cost_accounting_treatment=pass visible_answer_leakage=0 deterministic_order=pass
```
