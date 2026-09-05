# IND-06 Production QA

Issue: **ANKI-029 / #30**  
Chapter: **Industrial 06 — 部門別計算**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/IND-06.tsv`

## Result

- production Notes: **23**
- generated cards: **23**
- Cloze spans: **44**
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
- visible retrieval context preserved when targets are hidden
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs and coverage

No IND-06 production Note IDs existed before ANKI-029. IDs are allocated deterministically in canonical ALP order as `BK-IND-06-0001`–`BK-IND-06-0023`.

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. This chapter uses a one-ALP-per-Note mapping because each inventory proposition already corresponds to a distinct retrieval operation; no compression was necessary to prevent duplication or answer leakage. The canonical inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

The chapter's worked numerical demonstrations remain excluded as `DECORATIVE_EXAMPLE`. They substitute numbers into the active rules for total allocation, direct allocation, reciprocal allocation, actual departmental rates, and planned allocation without introducing an additional canonical decision rule.

## Recall-design review

### Review-driven Cloze refinements

A post-production learner review identified several spans that technically preserved the proposition but hid more wording than necessary. The affected Notes were tightened without changing ALP mapping or source meaning:

- `BK-IND-06-0002`: `正確な製品原価の計算` was narrowed to the canonical object `製品原価`; `正確な` and `の計算` remain visible.
- `BK-IND-06-0010`: formula modifiers are visible: `各部門の` remains outside the `配賦基準量` span and the denominator is expressed as `その{{c1::合計}}`.
- `BK-IND-06-0013`: the defining facts for direct allocation remain visible and only `直接配賦法` is hidden, so the prompt remains meaningful after Cloze removal.
- `BK-IND-06-0016`: `他の` is visible and only the atomic category label `補助部門` is hidden.
- `BK-IND-06-0020`: timing and department qualifiers remain visible around the actual-rate operands.
- `BK-IND-06-0021`: department/product qualifiers remain visible around `実際配賦率` and `実際配賦基準数値`.
- `BK-IND-06-0023`: long action phrases were replaced with atomic accounting objects (`予定配賦率`, `予定配賦額`, `実際部門費`, `配賦差異`) while the workflow verbs and timing remain visible.

These changes implement the existing minimal lexical scope, context sufficiency, context-qualified atomicity, formula-operand, and parallel-term atomicity rules. No new global rule is required.

### Departmental-costing concepts

The opening Notes retrieve the definition and purposes of departmental costing, distinguish `単純個別原価計算` from `部門別個別原価計算`, and test the core department classifications. Parallel classification labels such as `主経営部門`・`副経営部門` and `補助経営部門`・`工場管理部門` use separate same-index Cloze spans so the answers remain lexically atomic while still generating one coherent card.

### Three-stage cost flow

The batch preserves the complete departmental-costing flow:

1. `第1次集計`: manufacturing overhead is accumulated in cost departments;
2. `第2次集計`: service-department costs are allocated to manufacturing departments;
3. `第3次集計`: manufacturing-department costs are allocated to products.

Department-specific overhead and common departmental overhead are distinguished by whether the originating department can be identified. The common-cost allocation formula keeps arithmetic operators and relational qualifiers visible and Clozes only atomic operands.

### Direct and reciprocal allocation

Direct allocation is now prompted by a fully visible defining sentence: reciprocal service between service departments is ignored and service-department costs are allocated only to manufacturing departments; the learner retrieves the method name `直接配賦法`. The denominator rule remains a separate Note that retrieves the exclusion treatment.

The simplified reciprocal-allocation sequence separately retrieves the first allocation, self-consumption exclusion, and second allocation. In the first allocation, `製造部門` and `補助部門` are separate same-index spans, with the qualifier `他の` left visible. In the second allocation, amounts newly assigned to service departments are reallocated only to manufacturing departments.

### Product allocation and planned allocation

The third-stage Notes retrieve the departmental actual allocation rate and product allocation formulas using atomic operands while keeping timing, department, and product qualifiers visible. Planned allocation retrieves the beginning-of-period planned rate, actual activity base, and the ordered period workflow from rate setting through monthly variance calculation and year-end variance disposition.

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
- visible-context precision for the direct-allocation definition
- direct-versus-reciprocal service-department allocation anchors
- ordered three-stage and planned-allocation cost flow
- exact canonical exclusion family

Expected output:

```text
IND-06 production validation: PASS
notes=23 cards=23 cloze_spans=44 included_alps=23 mapped=23 unmapped=0
procedure_notes=7 formula_notes=3 canonical_exclusions=1
minimal_cloze_scope=pass formula_atomicity=pass parallel_atomicity=pass visible_context=pass cost_accounting_flow=pass journal_entry_check=not_applicable visible_answer_leakage=0 deterministic_order=pass
```
