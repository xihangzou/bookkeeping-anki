# IND-06 Production QA

Issue: **ANKI-029 / #30**  
Chapter: **Industrial 06 — 部門別計算**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/IND-06.tsv`

## Result

- production Notes: **23**
- generated cards: **23**
- Cloze spans: **46**
- included ALPs: **23**
- mapped included ALPs: **23**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- procedure Notes: **7**
- formula Notes: **3**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- parallel compound answers split into atomic Cloze spans
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs and coverage

No IND-06 production Note IDs existed before ANKI-029. IDs are allocated deterministically in canonical ALP order as `BK-IND-06-0001`–`BK-IND-06-0023`.

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. This chapter uses a one-ALP-per-Note mapping because each inventory proposition already corresponds to a distinct retrieval operation; no compression was necessary to prevent duplication or answer leakage. The canonical inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

The chapter's worked numerical demonstrations remain excluded as `DECORATIVE_EXAMPLE`. They substitute numbers into the active rules for total allocation, direct allocation, reciprocal allocation, actual departmental rates, and planned allocation without introducing an additional canonical decision rule.

## Recall-design review

### Departmental-costing concepts

The opening Notes retrieve the definition and purposes of departmental costing, distinguish `単純個別原価計算` from `部門別個別原価計算`, and test the core department classifications. Parallel classification labels such as `主経営部門`・`副経営部門` and `補助経営部門`・`工場管理部門` use separate same-index Cloze spans so the answers remain lexically atomic while still generating one coherent card.

### Three-stage cost flow

The batch preserves the complete departmental-costing flow:

1. `第1次集計`: manufacturing overhead is accumulated in cost departments;
2. `第2次集計`: service-department costs are allocated to manufacturing departments;
3. `第3次集計`: manufacturing-department costs are allocated to products.

Department-specific overhead and common departmental overhead are distinguished by whether the originating department can be identified. The common-cost allocation formula keeps arithmetic operators visible and Clozes only the individual operands.

### Direct and reciprocal allocation

Direct allocation retrieves the defining rule that reciprocal service between service departments is ignored and the denominator excludes service provided to other service departments.

The simplified reciprocal-allocation sequence separately retrieves the first allocation, self-consumption exclusion, and second allocation. In the first allocation, `製造部門` and `他の補助部門` are separate same-index spans rather than one compound answer. In the second allocation, amounts newly assigned to service departments are reallocated only to manufacturing departments.

### Product allocation and planned allocation

The third-stage Notes retrieve the departmental actual allocation rate and product allocation formulas using atomic operands. Planned allocation retrieves the beginning-of-period planned rate, actual activity base, and the ordered period workflow from rate setting through monthly variance calculation and year-end variance disposition.

### Journal-entry applicability

The canonical IND-06 INCLUDE shard contains no `journal_entry` ALPs. The chapter source includes illustrative entries inside worked procedures, but the canonical inventory does not classify those entries as independent active-recall propositions for this batch. Accordingly, the production batch does not create journal-entry Notes beyond the included ALP scope; the validator explicitly asserts that no unexpected journal-entry primary Note is introduced.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/IND-06.tsv`.

## Deterministic validator

`scripts/validate_ind06_production.py` checks:

- exact field order and deterministic stable IDs
- pinned source provenance
- Part/Chapter/primary Section consistency
- required deterministic tags and lifecycle
- `c1`-only generation
- exact one-to-one Note-to-ALP mapping and exact-once INCLUDE-ALP coverage
- canonical inventory immutability
- local duplicate rendered text
- visible-answer leakage
- broad/non-atomic Cloze answers
- atomic parallel-term Cloze spans
- formula/operator atomicity and required precision forms
- direct-versus-reciprocal service-department allocation anchors
- ordered three-stage and planned-allocation cost flow
- exact canonical exclusion family

Validated output:

```text
IND-06 production validation: PASS
notes=23 cards=23 cloze_spans=46 included_alps=23 mapped=23 unmapped=0
procedure_notes=7 formula_notes=3 canonical_exclusions=1
minimal_cloze_scope=pass formula_atomicity=pass parallel_atomicity=pass cost_accounting_flow=pass journal_entry_check=not_applicable visible_answer_leakage=0 deterministic_order=pass
```
