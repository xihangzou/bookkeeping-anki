# Coverage Rules

Status: **v0.9 — pilot validation pending**

## 1. Coverage target

Coverage target is the complete meaning of `bookkeeping-integrated/merged/textbook.md`, not a fixed card count and not only the 3級-derived topic map.

A source passage is covered when every testable and conceptually necessary proposition is either:

- mapped to one or more Cloze Notes; or
- explicitly excluded with a valid reason.

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

A numerical example is retained when it introduces a new decision, calculation step, branch, compound entry, or common error. Mere number substitution is not sufficient.

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

Do not create additional notes once the learner can already retrieve the proposition and apply it in all materially different contexts represented by the textbook.

Thus:

- one proposition repeated in five chapters does not automatically require five notes;
- one rule with three materially different exceptions may require four or more notes;
- one journal-entry pattern with only changed numbers normally requires one note;
- one method that changes treatment under different conditions requires separate condition-sensitive retrieval.

## 7. Source decomposition

Process each section in this order:

1. identify heading path;
2. split prose/tables/examples into semantic blocks;
3. list candidate propositions;
4. merge propositions that form one inseparable rule;
5. assign ALP IDs;
6. classify each as `INCLUDE` or `EXCLUDE`;
7. map included ALPs to notes;
8. record exclusion reason for excluded candidates.

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

## 9. Duplicate policy across chapters

Textbook integration intentionally contains foundational explanations near advanced treatments. Therefore deduplication must be semantic, not purely textual.

Keep separate notes when:

- later chapter adds a condition or exception;
- same concept is used in a materially different decision context;
- advanced treatment requires a distinct retrieval operation;
- the learner must discriminate two similar treatments.

Merge when:

- wording differs but proposition and retrieval target are the same;
- only numerical values differ;
- an advanced section repeats a foundational definition with no added information.

## 10. Journal-entry coverage

For each journal-entry family, verify coverage of all materially distinct textbook cases:

- initial recognition;
- subsequent settlement/collection;
- reversal/cancellation/return where applicable;
- adjustment/closing where applicable;
- compound entry where materially different;
- exception or alternate method explicitly taught by the textbook.

Do not assume one simple entry covers a later compound or conditional entry.

## 11. Calculation coverage

For each quantitative topic, separately inventory:

- formula/relationship;
- required inputs;
- order of operations where meaningful;
- treatment of boundaries/conditions;
- at least one application when application requires more than direct substitution.

## 12. Tables and lists

A table is not automatically one ALP. Decompose by what the learner must discriminate.

Examples:

- account classification table -> rows or logical groups;
- method comparison -> comparison dimensions;
- procedural list -> one ordered ALP if order itself matters;
- list of examples -> exclude examples that add no rule.

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
- 0 unexplained exclusions.

## 14. Source updates

The baseline is pinned. If `bookkeeping-integrated` changes later:

1. compare old and new source commits;
2. identify changed source blocks;
3. re-run ALP decomposition only for affected blocks plus dependent notes;
4. record the new baseline only after QA.
