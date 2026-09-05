# ANKI-041 — Cloze recall-quality audit

**Final result: PASS**

## Population

- Production batches: 31 / 31
- Approved active Notes audited: 735 / 735
- Generated active cards after corrections: 748
- Active Cloze spans after corrections: 2,008
- Included ALPs actively mapped: 965 / 965
- Unresolved recall-quality defects: 0

The audit was run against the normalized ANKI-038 corpus after ANKI-039 journal-entry QA and ANKI-040 formula/calculation QA. Stable Note IDs, ALP mappings, source provenance, and accounting/formula semantics were preserved.

## Audit method

`scripts/validate_recall_production.py` was added as the corpus-wide generated-card recall gate and wired into production CI. It renders each distinct Cloze index as an Anki card and checks:

- sufficient visible accounting context / retrieval subject;
- broad or placeholder answer targets;
- lexical scope and redundant fixed-head masking;
- independent parallel terms and canonical fixed labels;
- same-index vs different-index grouping;
- visible sibling-answer leakage;
- severe recall load;
- exact active retrieval duplicates;
- the reviewed cross-batch semantic-overlap fingerprint from ANKI-038;
- existence of the relevant chapter validator as the source-semantic backstop.

The corpus-level recall gate runs together with the ANKI-038 normalization validator, ANKI-039 journal-entry validator, and ANKI-040 formula/calculation validator. A full CI run also executes all 31 chapter validators.

## Initial findings and corrections

The first corpus-wide recall scan produced 22 blocker flags before false-positive calibration and correction. Fixed canonical labels and a small number of explicitly justified chapter-specific cues were distinguished from true recall defects.

Confirmed production defects: **6**, all corrected and rechecked.

- visible sibling-answer leakage: **2**
- abstract/broad answer target: **1**
- severe recall overload: **3**
- unresolved after correction: **0**

Six active Notes required production changes:

1. `BK-COM-01-0008` — removed visible wording that leaked `仕入` while keeping the two decision-adjustment entries and debit/credit syntax intact.
2. `BK-COM-01-0009` — removed visible answer leakage from the explanatory frame; the final neutral frame begins `販売時に収益と原価を同時記録する方法では...`.
3. `BK-COM-05-0034` — replaced the abstract answer `なし` with the accounting operation `当期損益に含めない`.
4. `BK-FND-00-0047` — split 10 expense-account targets into two independently recallable groups of 5 (`c1` / `c2`).
5. `BK-FND-00-0068` — split 17 auxiliary-book targets into three coherent groups of 4 / 6 / 7 (`c1` / `c2` / `c3`).
6. `BK-FND-00-0091` — split 9 accounting abbreviations/symbols into three groups of 3 while keeping the T/B family together to avoid sibling leakage.

The three Foundation corrections intentionally increase generated active cards from the ANKI-038 checkpoint of 743 to 748. Active Note count and ALP coverage are unchanged.

## Calibrated non-defects

The corpus gate documents narrowly scoped exceptions rather than weakening the current rule set:

- fixed canonical accounting labels containing `・` or `、` remain whole when punctuation is lexical rather than a list separator;
- `正しい仕訳` in `BK-FND-00-0015` is retained as the canonical operand in the correction-entry relation validated by ANKI-040, not as an ambiguous prompt placeholder;
- `補助部門` in `BK-IND-06-0016` is retained because the chapter QA deliberately keeps the compound visible cue `各補助部門費` while testing the classification label.

## Recall-load review

The validator blocks any generated card with 9 or more hidden targets. After correction, severe recall-load defects = 0.

A finite moderate-load review set of 40 generated cards (6–8 targets, or the configured answer-length criterion) was also enumerated. These were retained because the targets remain within one coherent retrieval frame and continue to pass the relevant chapter validator and corpus-level context/leakage checks.

## Duplicate and semantic consistency recheck

- Exact duplicate active retrieval propositions: 0
- New cross-batch semantic duplicate candidates: 0
- Previously justified ANKI-038 cross-batch semantic overlap pairs rechecked: 4 / 4
- Orphan included ALPs: 0

## Accounting / formula backstops

Final full validation simultaneously confirmed:

- ANKI-039 journal-entry QA: 167 audited Notes, defects = 0, unresolved = 0
- ANKI-040 formula/calculation QA: 395 audited Notes, 178 equations checked, 1,107 Cloze targets checked, 167 canonical source formula relations checked, defects = 0, unresolved = 0

## Final validation

GitHub Actions **Validate production notes #377** (`run_id=33940900977`, commit `6302501c30be8a384d22e64c324c9a5176cba5f2`) completed successfully.

Final recall validator output:

- batches = 31
- audited_notes = 735
- generated_cards = 748
- cloze_spans = 2,008
- multi_index_notes = 7
- retained_semantic_pairs_rechecked = 4
- severe_recall_load_defects = 0
- defects = 0
- unresolved = 0
- `ANKI-041 recall-quality validation: PASS`

## Acceptance result

- every active production Note audited: PASS
- visible context / retrieval subject: PASS
- semantic ambiguity / minimal answer scope: PASS
- canonical-label handling: PASS
- broad actions / redundant fixed heads: PASS
- generated-card leakage / grammar-only guessing: PASS
- Note scope / recall load: PASS
- same-index vs different-index grouping: PASS
- current journal-entry syntax: PASS
- formula operator / operand semantics: PASS
- semantic duplicate control: PASS
- corrections rechecked: PASS
- unresolved Cloze-quality defects: **0**

**ANKI-041 final result: PASS.**