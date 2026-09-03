# Pilot card-level validation

Issues: ANKI-PILOT-003 (#47), post-fix revalidation in ANKI-PILOT-004 (#48)

## Scope

`pilot/card_validation.tsv` is kept synchronized with the current `pilot/notes.tsv` and records one row for every generated Cloze card.

Current state after ANKI-PILOT-004 corrections:

- Pilot Notes reviewed: **40 / 40**
- Generated Cloze cards reviewed: **62 / 62**
- Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`
- Evidence: `pilot/card_validation.tsv`
- Failure-pattern audit trail: `pilot/review.md`

A card is treated as Anki-style rendered by hiding every occurrence of its active `cN` group while leaving all other Cloze groups visible. `targets` records the hidden answer(s), and `visible_other_answers` records answers that remain visible on that card.

## Check contract

Each card row records all required review dimensions using `P` = pass, `W` = warning, `F` = fail:

- `acct`: accounting accuracy
- `amb`: unambiguous target / answer form
- `ctx`: context sufficiency
- `atom`: atomicity / coherent recall unit
- `ans`: answer size
- `num`: Cloze numbering/grouping quality
- `dup`: duplicate or near-duplicate retrieval risk
- `src`: source traceability
- `repeat`: usefulness after repeated review
- `leak`: rendered-card leakage

Every non-pass row has a stable `defect_codes` value and severity (`minor`, `major`, or `blocking`).

## Historical ANKI-PILOT-003 result

Before corrective edits, ANKI-PILOT-003 reviewed **40 Notes / 63 cards**:

| Severity | Cards |
|---|---:|
| none | 38 |
| minor | 19 |
| major | 2 |
| blocking | 4 |
| **total** | **63** |

The blocking findings were:

- `BK-FND-00-0014 c2` — `ANSWER_FORM_AMBIGUITY`
- `BK-COM-01-0010 c1-c3` — `COMPARISON_AXIS_MISMATCH`

The major duplicate pair was:

- `BK-FND-00-0017 c2`
- `BK-COM-01-0004 c1`

All original defect codes, affected cards, severities, root causes, and dispositions are preserved in `pilot/review.md`.

## ANKI-PILOT-004 corrections

Three authoring corrections were applied:

1. `BK-FND-00-0014`: replace generic `本来の勘定科目` recall with the determinate operation `貸方に計上して取り崩す`.
2. `BK-COM-01-0004`: convert the duplicate pure-purchase formula card into numeric application (`480,000円`).
3. `BK-COM-01-0010`: use timing as the single comparison axis and group the two `売上時` methods into one Cloze target.

The third change reduces the generated-card count by one, from 63 to 62.

## Current post-fix result

| Severity | Cards |
|---|---:|
| none | 42 |
| minor | 20 |
| major | 0 |
| blocking | 0 |
| **total** | **62** |

Accounting and source-traceability checks remain clean: **0 accounting failures** and **0 source-traceability failures**.

The remaining minor findings are deliberate rule-design evidence:

- `LOW_RETRIEVAL_VALUE`
- `POSITIONAL_SEQUENCE_CUE`
- `LARGE_COUPLED_ANSWER`
- `PARALLEL_RELATION_CUE`
- `PARALLEL_FORMULA_CUE`
- `SYNONYM_VARIANT`
- `ANSWER_OVERSPECIFIED`

No current card carries `ANSWER_FORM_AMBIGUITY`, `COMPARISON_AXIS_MISMATCH`, `SEMANTIC_DUPLICATE`, or `NOTE_PARTIAL_DUPLICATE`.

## Gate result

**Current pilot validation has zero major and zero blocking findings.**

`Status=pilot` / `QA=pending` remain unchanged because approval and production freeze belong to the subsequent v1.0 revision/freeze tasks. ANKI-PILOT-005 should use `pilot/review.md` to translate the remaining warning families into explicit v1.0 rules or documented no-change decisions.
