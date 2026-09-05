# ANKI-040 — Formula / Calculation QA

## Result

**PASS** — the normalized production corpus has no unresolved formula/calculation defects under the current living rules.

- audited production Notes: **395**
- approved `formula` Notes in population: **148**
- approved `measurement` Notes in population: **33**
- canonical formula/measurement ALPs: **225 / 225 mapped and audited**
- calculation-dependent `cost_accounting` ALPs selected by independent signal scan: **6 / 6 mapped and audited**
- Notes containing an explicit equation relation: **178**
- Cloze targets reviewed by the corpus-wide audit: **1,107**
- canonical explicit formula relations checked: **167**
- equivalent source relations explicitly reconciled: **4**
- retained parseable worked numerical equations: **0**
- production Note defects confirmed: **0**
- production Notes corrected: **0**
- unresolved defects: **0**

Validation evidence: GitHub Actions run **#367**, `Validate production notes`, commit `b90618678ead49c52c60520d50ba2ea614cc68d5`.

## Authoritative baseline

The audit uses the normalized ANKI-038 corpus and the pinned source lineage carried by every active Note:

- source repository: `xihangzou/bookkeeping-integrated`
- source commit: `569ed7b82e729334e1472286eaca7c4352e6fbdb`
- source path: `merged/textbook.md`
- canonical ALP inventories under `inventory/topic_inventory/`
- current authority: `rules/anki_card_rules.md`
- chapter production validators plus corpus/journal validators

Historical authoring rules are not used as current acceptance criteria.

## Reproducible population construction

`scripts/validate_formula_production.py` reconstructs the audit population from active (`Status=approved`) Notes as the union of:

1. Notes whose primary `Type` is `formula` or `measurement`;
2. Notes mapped from INCLUDE ALPs whose canonical type is `formula` or `measurement`;
3. Notes mapped from `cost_accounting` ALPs whose canonical summaries contain calculation/allocation/valuation signals; and
4. Notes whose active text independently contains an equation/arithmetic relation or a material calculation/allocation/valuation signal.

The redundant selectors are intentional: a mistyped Note or ALP cannot silently escape the audit merely because one classification field is wrong.

### Audited Note count by batch

| Batch | Notes |
|---|---:|
| FND-00 | 5 |
| COM-01 | 20 |
| COM-02 | 3 |
| COM-03 | 3 |
| COM-04 | 7 |
| COM-05 | 28 |
| COM-06 | 26 |
| COM-07 | 5 |
| COM-08 | 7 |
| COM-09 | 8 |
| COM-10 | 10 |
| COM-11 | 13 |
| COM-12 | 20 |
| COM-13 | 14 |
| COM-14 | 3 |
| COM-15 | 15 |
| COM-16 | 9 |
| IND-01 | 16 |
| IND-02 | 12 |
| IND-03 | 10 |
| IND-04 | 7 |
| IND-05 | 24 |
| IND-06 | 19 |
| IND-07 | 7 |
| IND-08 | 25 |
| IND-09 | 12 |
| IND-10 | 11 |
| IND-11 | 28 |
| IND-12 | 14 |
| IND-13 | 13 |
| IND-14 | 1 |
| **Total** | **395** |

The validator prints the exact Note IDs for every batch, making the population reproducible from CI logs.

## Formula correctness and source reconciliation

The audit checks each selected Note for pinned source lineage and chapter QA status, then cross-checks canonical formula ALPs with explicit equations against the operator/sign relationships recorded in the source-derived ALP summaries. In addition, the existing chapter validators re-run and must continue to pass their chapter-specific formula, measurement, costing-flow, and source-integrity checks.

Four representations require explicit equivalence reconciliation rather than naive operator-order comparison:

| ALP | Production representation | Reconciliation |
|---|---|---|
| `ALP-COM-13-0003` | `当期末繰越利益剰余金＝前期末繰越利益剰余金＋当期純利益` | Same retained-earnings equation as the pinned textbook, with the result moved from the right side to the left. |
| `ALP-FND-00-0058` | correction procedure expressed as `誤仕訳の逆仕訳` plus `正しい仕訳` | Operationally equivalent to the canonical correction relationship `誤仕訳＋訂正仕訳＝正しい仕訳`. |
| `ALP-IND-12-0019` | `全部原価計算営業利益＝直接原価計算営業利益－期首固定費＋期末固定費` | Same fixed-cost adjustment as `直接原価計算営業利益＋期末固定費－期首固定費`; add/subtract terms are reordered. |
| `ALP-IND-13-0006` | component equations for contribution-margin ratio and variable-cost ratio plus visible `合計100%` | One integrated Note carries the two component ratios and their canonical identity `貢献利益率＋変動費率＝100%`. |

These equivalences are enumerated explicitly in the validator so that only reviewed cases are accepted; any new operator/sign mismatch still fails closed.

Pinned textbook spot-checks confirm the relevant relationships, including:

- COM-13: `前期末B/Sの繰越利益剰余金 + P/Lの当期純利益 = 当期末B/Sの繰越利益剰余金`;
- IND-12: the fixed-cost expense and operating-profit reconciliation formulas, including the `－期首` / `＋期末` direction;
- IND-13: `貢献利益率 ＝ 貢献利益 ÷ 売上高`, `変動費率 ＝ 変動費 ÷ 売上高`, and `貢献利益率 ＋ 変動費率 ＝ 100%`.

## Cloze / mathematical-meaning checks

The corpus-wide validator and chapter validators together enforce the current rules relevant to calculations:

- formula operators remain visible when the recall target is an accounting operand;
- formula/measurement Notes do not hide a whole arithmetic expression as one answer;
- accounting operands remain atomic/minimal while retaining context that is part of the canonical concept;
- valid atomic constants such as `1/2`, `1/10`, and statement abbreviations such as `B/S`, `P/L`, `S/S` are not misclassified as hidden division expressions;
- context-qualified atomic terms such as `手付金授受時HR`, `実際配賦率`, or `標準価格` are not mechanically split when the qualifier is part of the accounting variable itself;
- chapter validators continue to report formula atomicity/minimal scope and visible-answer leakage checks as PASS.

This distinction is necessary to apply both the formula-operator rule and the context-qualified atomicity rule without contradiction.

## Worked numerical applications

The active production Notes contain **0 retained parseable worked numerical equations** of the form that can be independently recomputed without reconstructing a source-only example. Therefore the required retained-example recomputation count is **0 (not applicable)**.

Worked numerical examples in the textbook remain source evidence but are commonly inventory-excluded as decorative/example material rather than retained as production recall targets. For example, the IND-12 source contains a complete direct-vs-absorption costing case study, while the inventory excludes its example block from production Notes. Symbolic relationships retained in production are covered by the formula/source checks above.

## Defect triage

The first deliberately over-broad validator pass produced **135 provisional flags**. Manual/source review classified them as:

- **131 detector false positives** caused by treating valid contextual operands, fractions, statement abbreviations, or non-formula targets as formula-scope defects;
- **4 source-equivalent representations** listed above;
- **0 confirmed production Note defects**.

The validator was calibrated to the current living rules and the four reviewed equivalences were made explicit. No production Note text required correction.

## Final recheck

GitHub Actions run #367 re-ran:

- governance validation;
- all 31 chapter production validators;
- ANKI-038 corpus-normalization validation;
- ANKI-039 journal-entry validation; and
- ANKI-040 formula/calculation validation.

All validators passed. ANKI-040 final metrics were:

```text
audited_notes=395
formula_notes=148
measurement_notes=33
mandatory_formula_measurement_alps=225
mapped_mandatory_alps=225
calculation_cost_alps=6
mapped_calculation_cost_alps=6
equations_checked=178
cloze_targets_checked=1107
source_formula_relations_checked=167
source_formula_equivalences_reconciled=4
recalculated_examples=0
defects=0
unresolved=0
ANKI-040 formula/calculation validation: PASS
```

## Final status

**PASS — unresolved formula/calculation defects = 0.**
