# Coverage Rules

Status: **v1.0 — frozen after representative pilot (ANKI-PILOT-006)**

## 1. Coverage target

Coverage target is the complete meaning of `bookkeeping-integrated/merged/textbook.md`, not a fixed card count and not only the 3級-derived topic map.

Coverage is evaluated at two distinct stages.

### Inventory-stage coverage

A source passage is inventory-covered when every testable and conceptually necessary candidate proposition is explicitly classified as `INCLUDE` or `EXCLUDE`:

- every included proposition receives a stable ALP ID, one canonical primary type, and full source traceability; and
- every excluded proposition records one valid canonical exclusion reason.

At this stage, included ALPs do not need to be mapped to Cloze Notes yet; empty `note_ids` and `qa_status=pending` are valid.

### Final deck coverage

A source passage is finally covered when every inventory decision has been resolved into either:

- one or more approved Cloze Notes mapped to each included ALP; or
- an explicit valid exclusion for each excluded candidate.

Coverage does not require one distinct Note or generated card per ALP. Multiple ALPs may map to one coherent Note/retrieval unit when the canonical schema rules are satisfied.

## 2. Atomic Learning Point categories

Every included learning point receives one primary category.

| Type | Include when |
|---|---|
| `definition` | a term has a distinct accounting meaning |
| `classification` | category/5-element/statement placement matters |
| `recognition` | timing or recognition condition matters |
| `measurement` | valuation or amount determination matters |
| `journal_entry` | debit/credit treatment must be reproduced |
| `formula` | a quantitative relationship must be recalled |
| `procedure` | order/process is important |
| `comparison` | distinction between methods/accounts matters |
| `exception` | a condition changes the general treatment |
| `reasoning` | causal understanding prevents rote confusion |
| `ledger` | posting/bookkeeping mechanics matter |
| `financial_statement` | presentation or statement relationship matters |
| `cost_accounting` | industrial bookkeeping cost-flow logic matters |

Secondary types may be recorded in tags.

## 3. Mandatory inclusion test

Include an ALP if omitting it could reasonably cause any of the following:

1. wrong account selection;
2. wrong debit/credit side;
3. wrong recognition timing;
4. wrong amount or valuation;
5. wrong journal entry;
6. wrong cost flow or allocation;
7. wrong ledger/closing procedure;
8. wrong financial statement presentation;
9. confusion between similar accounting methods;
10. missed exception or condition;
11. inability to reconstruct a core accounting relationship.

## 4. Conditional inclusion

Include only when it adds retrieval value:

- explanatory examples;
- alternative wording;
- historical/background remarks;
- implementation details;
- long numerical demonstrations;
- bookkeeping form layout details.

A numerical example is retained when it introduces a new decision, calculation step, branch, compound entry, common error, or a materially distinct application of a canonical formula. Mere number substitution is not sufficient unless the application card deliberately replaces an otherwise duplicated formula-recall card.

## 5. Exclusion reasons

Every excluded source unit must use one of these reasons:

- `DUPLICATE_EXACT`
- `DUPLICATE_SEMANTIC`
- `PARAPHRASE_ONLY`
- `RHETORICAL_CONTEXT`
- `DECORATIVE_EXAMPLE`
- `DERIVABLE_TRIVIAL`
- `OUTSIDE_RECALL_GOAL`

No exclusion may use a vague reason such as `not important`.

## 6. Necessary vs sufficient

### Necessary

No meaningful learning point from the source may be absent.

### Sufficient

Do not create additional notes or generated cards once the learner can already retrieve the proposition and apply it in all materially different contexts represented by the textbook.

Thus:

- one proposition repeated in five chapters does not automatically require five notes;
- one rule with three materially different exceptions may require four or more notes;
- one journal-entry pattern with only changed numbers normally requires one note;
- one method that changes treatment under different conditions requires separate condition-sensitive retrieval;
- two Notes may both be necessary at ALP level while one generated retrieval unit is still redundant; deduplication is therefore evaluated below the Note level as well.

## 7. Source decomposition

Process each section in this order:

1. identify heading path;
2. split prose/tables/examples into semantic blocks;
3. list candidate propositions;
4. merge propositions that form one inseparable rule;
5. classify each candidate as `INCLUDE` or `EXCLUDE`;
6. for every included candidate, assign a stable ALP ID, one canonical primary type, and an inclusion reason;
7. for every excluded candidate, record one canonical exclusion reason and leave ALP ID/type empty;
8. map included ALPs to notes when note generation begins.

At the ANKI-003 inventory stage, step 8 may remain pending; `note_ids` may be empty and `qa_status=pending` is valid.

## 8. Coverage inventory fields

Minimum inventory fields:

```text
alp_id
source_part
source_chapter
source_section
source_anchor
summary
type
status
include_reason
exclude_reason
note_ids
qa_status
```

## 9. Duplicate policy across chapters and generated cards

Textbook integration intentionally contains foundational explanations near advanced treatments. Therefore deduplication must be semantic, not purely textual.

Keep separate notes/cards when:

- later chapter adds a condition or exception;
- same concept is used in a materially different decision context;
- advanced treatment requires a distinct retrieval operation;
- the learner must discriminate two similar treatments;
- a second card converts a canonical formula into a materially distinct application, boundary case, or method-selection decision.

Merge, remove, or redesign when:

- wording differs but proposition and retrieval target are the same;
- only numerical values differ without a new decision;
- an advanced section repeats a foundational definition with no added information;
- a generated card from one multi-Cloze Note duplicates a card generated from another Note;
- a sibling card is only a partial duplicate of another Note's retrieval unit.

### Retrieval-unit level requirement

Duplicate QA is performed at **generated-card / retrieval-unit level**, not only at Note level.

For each generated `cN` card, compare the semantic proposition being recalled against existing generated cards. Cross-context repetition is permitted only if the later card adds a materially different:

- retrieval operation;
- condition;
- application;
- exception;
- decision;
- discrimination task.

If two ALPs require coverage but their optimal retrieval proposition is the same, preserve both ALP mappings while using one coherent Note/retrieval unit where allowed by `schema/note_schema.yaml`.

## 10. Journal-entry coverage

For each journal-entry family, verify coverage of all materially distinct textbook cases:

- initial recognition;
- subsequent settlement/collection;
- reversal/cancellation/return where applicable;
- adjustment/closing where applicable;
- compound entry where materially different;
- exception or alternate method explicitly taught by the textbook.

Do not assume one simple entry covers a later compound or conditional entry.

Coverage does not require splitting an inseparable compound entry into multiple cards. Cloze grouping is governed by `rules/cloze_rules.md`; if same-index grouping is required to prevent counterpart leakage, the grouped entry still fully covers its mapped ALP(s).

## 11. Calculation coverage

For each quantitative topic, separately inventory:

- formula/relationship;
- required inputs;
- order of operations where meaningful;
- treatment of boundaries/conditions;
- at least one application when application requires more than direct substitution or when a distinct application is needed to avoid duplicating a canonical formula-recall card.

Formula recall and numeric application are different retrieval operations only when the application actually requires calculation or judgment rather than paraphrasing the formula.

## 12. Tables and lists

A table is not automatically one ALP. Decompose by what the learner must discriminate.

Examples:

- account classification table -> rows or logical groups;
- method comparison -> comparison dimensions;
- procedural list -> one ordered ALP if order itself matters;
- list of examples -> exclude examples that add no rule.

A table-derived proposition may be necessary for coverage but still produce a low-value card if headings make the answer automatic. In that case retain the ALP while redesigning the Cloze toward a condition, contrast, or decision rather than generating redundant label-association cards.

## 13. Coverage metrics

Final report must include at minimum:

```text
source sections reviewed / total
candidate propositions
included ALPs
excluded candidates by reason
ALPs mapped to notes / total ALPs
unmapped ALPs
notes with source traceability / total notes
journal-entry QA pass rate
calculation QA pass rate
Cloze QA pass rate
```

Completion requires:

- 100% source sections reviewed;
- 100% included ALPs mapped;
- 0 unresolved accounting errors;
- 0 unresolved ambiguous Clozes;
- 0 unexplained exclusions;
- 0 unresolved exact/semantic generated-card duplicates unless a materially distinct retrieval rationale is recorded.

## 14. Source updates

The baseline is pinned. If `bookkeeping-integrated` changes later:

1. compare old and new source commits;
2. identify changed source blocks;
3. re-run ALP decomposition only for affected blocks plus dependent notes;
4. record the new baseline only after QA.

## 15. ANKI-PILOT-005 revision scope

The representative pilot justified one coverage-rule change: semantic duplicate control must operate at generated-card / retrieval-unit level, because `BK-FND-00-0017 c2` and `BK-COM-01-0004 c1` were semantically identical despite belonging to different Notes/contexts.

The pilot did **not** justify changing:

- canonical ALP IDs;
- include/exclude reason vocabulary;
- source decomposition fields;
- pinned source baseline;
- source-traceability requirements.

Those contracts remain unchanged for the v1.0 freeze gate.

## 16. ANKI-PILOT-006 freeze decision

The v1.0 candidate passed the final pilot gate and is frozen for Phase C production.

Freeze evidence:

- corrected pilot: **40 Notes / 62 generated cards**;
- accounting failures: **0**;
- source-traceability failures: **0**;
- major findings: **0**;
- blocking findings: **0**;
- recurring/minor finding families are governed by explicit v1.0 rules or documented no-change decisions;
- canonical ALP IDs and source mappings remain unchanged.

Chapter-wide generation from ANKI-007 onward must use this frozen v1.0 coverage contract unless a separately reviewed post-freeze migration is explicitly approved.
