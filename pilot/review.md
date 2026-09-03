> **Historical pilot artifact.** References in this file to a v1.0 freeze describe the original pre-production gate. They do not define current repository governance; current authority is `GOVERNANCE.md` and the latest merged specification/rules/schema.

# Pilot failure-pattern review

Issue: ANKI-PILOT-004 (#48)

## Purpose

This review consolidates the ANKI-PILOT-003 card-level findings into the auditable evidence used to revise the v0.9 authoring/schema contract to v1.0.

Authoritative input reviewed here:

- `pilot/card_validation.tsv` as produced by ANKI-PILOT-003: 40 Notes / 63 generated Cloze cards
- `pilot/VALIDATION.md`
- `pilot/notes.tsv`
- `rules/cloze_rules.md` v0.9
- `schema/note_schema.yaml` v0.9

The original ANKI-PILOT-003 result was 38 cards with no finding, 19 minor, 2 major, and 4 blocking. Accounting failures and source-traceability failures were both zero.

## Defect inventory and disposition

Every defect code emitted by ANKI-PILOT-003 is represented below. Counts refer to the original 63-card review.

| Defect code | Affected cards | Original severity | Recurrence classification | Root cause | Pilot disposition | Proposed v1.0 rule/schema action |
|---|---|---|---|---|---|---|
| `LOW_RETRIEVAL_VALUE` | `BK-FND-00-0001 c1-c3` (3) | minor | one Note / repeated across 3 sibling cards | labels such as 投資家・銀行・取引先 strongly cue the associated decision purpose | retained; accurate and coverage-relevant | add a utility check: do not create a Cloze whose visible cue makes retrieval effectively automatic after repetition unless it is needed for explicit coverage; prefer a higher-value contrast or decision condition |
| `POSITIONAL_SEQUENCE_CUE` | `BK-FND-00-0009 c1-c4`; `BK-COM-01-0017 c1-c3` (7) | minor | recurring across 2 procedure Notes | separate Cloze numbers leave neighboring sequence stages visible, exposing the missing stage's position | retained as acceptable warnings because exact stage wording still requires recall | procedure rule: if order itself is the target, visible neighbors are permitted only when the missing stage still requires substantive recall; use same-index grouping or whole-sequence recall when neighbors reveal the answer rather than merely position |
| `LARGE_COUPLED_ANSWER` | `BK-FND-00-0013 c1`; `BK-COM-01-0003 c1`; `BK-COM-01-0008 c1`; `BK-COM-01-0009 c1` (4) | minor | recurring across 4 journal-entry Notes | answer units contain 3-4 account names/positions because splitting would leak the coupled entry | retained; no accounting error and coupling is pedagogically coherent | journal-entry rule: multi-field same-index answers are allowed when the fields form one inseparable entry/paired-entry unit; require explicit justification when the answer contains more than 3 account positions and split only when leakage can be avoided |
| `ANSWER_FORM_AMBIGUITY` | `BK-FND-00-0014 c2` (1) | blocking | one-off authoring mistake | generic target `本来の勘定科目` has multiple semantically valid realizations without a concrete transaction | **fixed** in `pilot/notes.tsv`: target changed to the uniquely testable operation of crediting/removing 仮払金 after the amount/purpose is determined | ambiguity rule: a Cloze must specify a unique semantic answer class; never Cloze a placeholder such as “appropriate/original account” unless the transaction facts uniquely determine that account |
| `PARALLEL_RELATION_CUE` | `BK-FND-00-0015 c1-c2` (2) | minor | one Note / rule-level risk | leaving the counterpart relation visible materially narrows the hidden half | retained; the relation still requires recall and is compact | same/different-index rule: when paired relation members are mutually revealing, prefer same-index masking if independent recall adds little; separate cards are allowed only when each hidden member remains non-trivial with its counterpart visible |
| `PARALLEL_FORMULA_CUE` | `BK-FND-00-0017 c1-c2` (2) | minor after deduplication | one Note / rule-level risk | visible sibling formula exposes the algebraic template of the hidden formula | retained as warning after duplicate removal | formula rule: parallel formulas may remain separate cards only when the visible formula does not disclose the hidden operands/operation; otherwise group them or add discriminating context |
| `NOTE_PARTIAL_DUPLICATE` | `BK-FND-00-0017 c1` (1) | minor | one-off pair-level symptom | one sibling card shared a retrieval proposition with another Note | **fixed** by changing `BK-COM-01-0004` to numeric application, so the sibling Note no longer contains a duplicated retrieval unit | duplicate rule: evaluate duplication at generated-card/retrieval-unit level, not only Note level |
| `SEMANTIC_DUPLICATE` | `BK-FND-00-0017 c2`; `BK-COM-01-0004 c1` (2) | major | one exact cross-context pair | both cards asked for `純仕入高 = 総仕入高 - 仕入戻し高`; the commercial wording added no new judgment | **fixed**: keep the canonical formula in `BK-FND-00-0017`; convert `BK-COM-01-0004` to a numeric application (`500,000 - 20,000 = 480,000円`) | dedup rule: cross-context repetition is allowed only if the second card adds a materially different retrieval operation, condition, application, exception, or decision; otherwise merge/remove it |
| `SYNONYM_VARIANT` | `BK-COM-01-0001 c1` (1) | minor | answer-equivalence family; see also `ANSWER_OVERSPECIFIED` | canonical wording `販売目的` has natural equivalents such as `販売する目的` | retained; canonical text remains concise | answer-form rule: canonical answers define intended meaning, not an exclusive literal string, unless terminology must be exact; Extra or authoring guidance should identify common acceptable equivalents when useful |
| `COMPARISON_AXIS_MISMATCH` | `BK-COM-01-0010 c1-c3` (3) | blocking | one-off authoring mistake with multi-card blast radius | lead-in asked when 売上原価 is recognized, while the 分記法 branch asked for the object `商品売買益`; cards therefore mixed timing and object dimensions | **fixed**: comparison now asks one axis only: timing. 三分法=`決算時`; 分記法の商品売買益 and 売上原価対立法の売上原価=`売上時`, with the latter two represented by one shared Cloze group | comparison rule: every branch in a comparison Note must answer the same named dimension and use the same answer category; if two branches share the same answer, mask the shared proposition together when separate cards would leak it |
| `ANSWER_OVERSPECIFIED` | `BK-COM-01-0016 c1` (1) | minor | answer-equivalence family; see `SYNONYM_VARIANT` | `販売済商品の売上原価` is pedagogically precise, but `売上原価` carries the core semantic answer | retained | same answer-form rule as `SYNONYM_VARIANT`: do not imply that a longer canonical phrase invalidates an accounting-equivalent shorter answer unless the modifier is itself the tested distinction |

## Required review dimensions with no defect

The pilot also explicitly checked failure classes that did not produce a defect code.

| Review class | Result | Disposition / v1.0 implication |
|---|---|---|
| accounting errors | 0 failures | no accounting-rule change from this pilot; retain mandatory journal-entry/formula QA gates |
| insufficient context | no standalone recurring defect; only the `COMPARISON_AXIS_MISMATCH` context failure | address through unique-answer and same-axis comparison rules rather than a schema change |
| excessively fragmented Notes | no standalone defect | no change; continue to evaluate at generated-card level |
| answer leakage | no blocking direct-answer leakage; warning-level positional/parallel cues recorded above | strengthen grouping guidance; do not add schema fields |
| poor Cloze numbering/grouping | warnings captured by positional/parallel cue codes | revise same-index vs different-index guidance in v1.0 |
| weak source traceability | 0 failures | no source-field/schema change required; keep pinned repo/commit/path + ALP mapping mandatory |
| schema/tag friction | none observed | no schema change justified by the pilot |
| deterministic TSV serialization friction | none observed | no serialization change justified by the pilot |

## Pilot Note corrections

### `BK-FND-00-0014` — remove generic answer-form ambiguity

Before:

`支払内容・金額が未確定のときはまず {{c1::仮払金}} で記録し、内容が確定した後に {{c2::本来の勘定科目}} へ振り替える。`

After:

`支払内容・金額が未確定のときはまず {{c1::仮払金}} で記録し、内容が確定した後は仮払金を {{c2::貸方に計上して取り崩す}}。`

The corrected target tests a determinate operation on the temporary asset account rather than an unspecified downstream account name.

### `BK-COM-01-0004` — resolve exact semantic duplicate

Before:

`商品売買における純仕入高は、{{c1::総仕入高－仕入戻し高}} で求める。`

After:

`商品売買で総仕入高500,000円、仕入戻し高20,000円なら、純仕入高は {{c1::480,000円}} である。`

The foundation Note remains the formula recall. The commercial Note now tests application, preserving ALP coverage without duplicating the same retrieval proposition.

### `BK-COM-01-0010` — restore one comparison axis and prevent sibling leakage

Before, the Note mixed timing (`決算時`, `売上時`) with an object (`商品売買益`).

After:

`利益・売上原価を把握する時点は、三分法では {{c1::決算時}}。分記法の商品売買益と売上原価対立法の売上原価はいずれも {{c2::売上時}} に把握する。`

The corrected Note uses timing as the single axis. The two methods that share the same timing are grouped into one Cloze target, preventing one branch from simply revealing the other's answer.

## Post-fix verification state

After applying the three Note corrections and revalidating all generated cards:

| Severity | Cards |
|---|---:|
| none | 42 |
| minor | 20 |
| major | 0 |
| blocking | 0 |
| **total** | **62** |

The card count falls from 63 to 62 because `BK-COM-01-0010` now uses two coherent Cloze groups rather than three mismatched groups.

Remaining minor warnings are intentionally retained as evidence for ANKI-PILOT-005. They are not accounting errors, ambiguous prompts, or direct answer leakage. No unresolved blocking finding remains.

## Recurring patterns requiring v1.0 treatment

ANKI-PILOT-005 must make an explicit rule decision for these recurring/systemic families:

1. **Sequence cueing** — positional information from visible neighboring stages.
2. **Parallel cueing** — visible paired relations/formulas narrowing the hidden answer.
3. **Coupled answer size** — coherent journal entries approaching the useful recall-load ceiling.
4. **Answer equivalence** — synonyms and pedagogically overspecified canonical wording.
5. **Retrieval-unit deduplication** — generated-card semantic duplicates across contexts.
6. **Comparison-axis discipline** — all branches must answer one named dimension and one answer category.
7. **Unique answer form** — generic placeholders are invalid unless context determines one semantic target.
8. **Retrieval value** — accurate cards should still require meaningful recall after repetition.

No schema/tag/source/serialization change is justified solely by this pilot. If ANKI-PILOT-005 nevertheless changes those contracts, it must document evidence beyond this review.

## Gate result

**ANKI-PILOT-004 passes.**

- every ANKI-PILOT-003 defect is represented above
- recurring patterns are separated from one-off authoring mistakes
- accounting failures remain zero
- both blocking ambiguity families are fixed in the pilot Notes
- the semantic duplicate pair is resolved
- every recurring/systemic pattern has a concrete v1.0 rule proposal or an explicit no-schema-change rationale
- unresolved blocking findings: **0**

ANKI-PILOT-005 may proceed with the v0.9 → v1.0 revision using this review as its evidence base.

## ANKI-PILOT-005 v1.0 implementation record

Issue: ANKI-PILOT-005 (#49)

The v1.0 candidate translates each pilot finding into an explicit production rule while preserving stable contracts that passed the pilot.

| Pilot evidence | Implemented v1.0 location | Decision |
|---|---|---|
| `LOW_RETRIEVAL_VALUE` | `rules/cloze_rules.md` §24 | add retrieval-utility check; prefer condition/contrast/decision over mechanically cued association when possible |
| `POSITIONAL_SEQUENCE_CUE` | `rules/cloze_rules.md` §13 | visible neighbors may reveal position only; if they effectively reveal the answer, use whole-sequence/same-index/redesign |
| `PARALLEL_RELATION_CUE` | `rules/cloze_rules.md` §4 | mutually revealing paired members default toward same-index unless each card remains independently non-trivial |
| `PARALLEL_FORMULA_CUE` | `rules/cloze_rules.md` §12 | separate formula cards allowed only when visible sibling formula does not disclose hidden operands/operation |
| `LARGE_COUPLED_ANSWER` | `rules/cloze_rules.md` §7 | inseparable multi-field entries may stay same-index; 4+ account positions require an explicit split-vs-leakage check |
| `ANSWER_FORM_AMBIGUITY` | `rules/cloze_rules.md` §5 | every Cloze must have a unique semantic answer class; generic placeholders are invalid without determining facts |
| `SYNONYM_VARIANT` / `ANSWER_OVERSPECIFIED` | `rules/cloze_rules.md` §22 | canonical wording represents semantic meaning unless exact terminology itself is the target |
| `NOTE_PARTIAL_DUPLICATE` / `SEMANTIC_DUPLICATE` | `rules/cloze_rules.md` §23; `rules/coverage_rules.md` §9 | deduplicate at generated-card/retrieval-unit level; second context must add a materially different retrieval operation |
| `COMPARISON_AXIS_MISMATCH` | `rules/cloze_rules.md` §14 | every branch answers one named comparison axis and one answer category; identical branch answers may share one Cloze group |
| multi-ALP coherence/source preservation | `rules/cloze_rules.md` §2 | multiple ALPs may share one Note only as one coherent recall unit; canonical inventory mappings remain authoritative |

### No-change decisions

The pilot produced no evidence requiring changes to the following contracts:

- `schema/note_schema.yaml` field set, allowed values, tag namespaces, `Status`, or `QA`
- deterministic TSV field order / escaping / list serialization
- pinned `SourceRepo`, `SourceCommit`, `SourcePath`
- canonical ALP IDs or source mappings

Therefore `schema/note_schema.yaml` remains semantically unchanged in ANKI-PILOT-005. Its version metadata is intentionally left for the ANKI-PILOT-006 freeze step rather than creating an evidence-free schema revision.

### Coverage-rule change rationale

A coverage-rule change **was** justified. The pilot's exact duplicate crossed Note boundaries and affected only one generated sibling retrieval unit. `rules/coverage_rules.md` is therefore revised to v1.0 candidate so semantic duplication is evaluated at generated-card/retrieval-unit level while ALP coverage remains independently preserved.

### Corrected pilot compatibility

No `pilot/notes.tsv` row, canonical ALP ID, source mapping, tag, `Status`, `QA`, or TSV serialization is changed by ANKI-PILOT-005. The corrected corpus remains the ANKI-PILOT-004 state: **40 Notes / 62 generated cards, 0 major, 0 blocking, 0 accounting failures, 0 source-traceability failures**.

The retained 20 minor warnings are now governed by explicit v1.0 rules rather than unresolved contract ambiguity. They do not require further pilot Note edits before the freeze review.

## ANKI-PILOT-005 gate result

**v1.0 candidate revision passes ANKI-PILOT-005.**

- every recurring pilot failure has an implemented rule change or explicit no-change rationale
- generated-card semantic deduplication is now a coverage requirement
- no existing canonical ALP ID or source mapping is changed
- corrected pilot Notes remain structurally compatible with the unchanged schema/TSV contract
- unresolved blocking accounting/ambiguity/direct-leakage findings remain **0**
- affected rule artifacts consistently identify themselves as **v1.0 candidate**

ANKI-PILOT-006 may now perform the final freeze decision and production authorization.
