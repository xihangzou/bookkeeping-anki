# Exam-Yield / Active-Deck Rules

Status: **v1.3 post-freeze overlay — ANKI-AUDIT-001/002/003 (#56, #58, #62)**

This file is a post-freeze overlay on the frozen v1.0 source/schema/stable-ID contract in `SPEC.md`, `rules/cloze_rules.md`, `rules/coverage_rules.md`, and `schema/note_schema.yaml`.

The frozen source/schema/stable-ID contract remains authoritative. This overlay governs **active-deck selection, lifecycle handling, and recall design**.

## 1. Primary target

The canonical inventory must remain **100% reviewed and traceable**, but the active deck is not required to directly recall every included ALP.

The active deck should be the **smallest set of high-yield retrieval operations** that supports bookkeeping exam performance and later 2級 / CPA reasoning.

Direct recall is favored when omission could materially cause:

1. wrong account or five-element classification;
2. wrong debit/credit direction;
3. wrong recognition decision;
4. wrong journal entry or settlement treatment;
5. wrong calculation or formula;
6. failure to distinguish a testable control, voucher, ledger, or source document;
7. failure to apply an important exception;
8. loss of a durable accounting relationship needed later.

Introductory wording, obvious labels, long form-field lists, duplicate definitions, and low-yield terminology may remain only in historical rows / QA context.

## 2. Source coverage vs active recall — v1.3

v1.3 explicitly separates two metrics:

### Source-reviewed coverage

Every canonical included ALP must remain represented in production history and must have an auditable include/exclude and retirement decision.

This is the **coverage completeness** metric.

### Active direct-recall coverage

Only ALPs that justify spaced retrieval need to remain mapped to `Status=approved` Notes.

This is the **study-cost / exam-yield** metric.

Therefore, unlike v1.1/v1.2, an included ALP does **not** need an approved mapping merely to preserve source traceability. A low-yield ALP may be represented only by a `deprecated` historical Note plus chapter QA rationale.

Do not create an artificial active card solely to keep an ALP “active-mapped.”

## 3. Active-card selection gate

Keep a card only when all are true:

- the target is independently worth spaced retrieval;
- forgetting it can plausibly change an exam answer or later accounting reasoning;
- it is not already tested by a stronger downstream card;
- it can be asked with a short, unambiguous prompt;
- the expected answer is canonical enough to grade mentally without synonyms proliferating.

When these conditions fail, deprecate rather than bundle the fact into another active Cloze merely for coverage.

## 4. Cloze lexicality — v1.3

A Cloze should normally contain **one lexical accounting unit**, not a phrase or clause.

Preferred targets include:

- `資産`
- `負債`
- `純資産`
- `収益`
- `費用`
- `借方`
- `貸方`
- `試算表`
- `所得税預り金`
- `法定福利費`
- `仮払金`
- `入金伝票`
- `領収書`

Avoid hiding:

- full explanatory clauses;
- `A＋B` expressions when either component can be asked separately;
- phrases containing the reason and conclusion together;
- conjunction-linked procedures;
- long list strings such as `X・Y・Z` as one answer.

A short phrase is permitted only when no natural canonical one-word/one-term target preserves the intended retrieval operation. The exception must remain short and unambiguous.

## 5. Parallel and conjunction splitting — v1.3

v1.2 used repeated Cloze indices to reduce generated-card count. v1.3 **supersedes that strategy**.

If two sibling facts are independently worth remembering, split them into separate cards:

- parallel classifications -> separate indices;
- debit vs credit treatments -> separate indices;
- employee vs employer treatments -> separate indices;
- multiple trial-balance types -> separate indices;
- multiple voucher/document types -> separate indices;
- conjunction-linked steps -> separate sentences/cards when both steps are retrieval targets.

For approved FND-00 Notes:

- one generated card = one Cloze occurrence;
- do not repeat the same `cN` across several blanks;
- one Japanese full-stop-delimited sentence should contain at most one Cloze;
- visible context may contain supporting facts, but should not force simultaneous recall of unrelated answers.

The way to reduce total study cost is **retiring low-yield cards**, not combining multiple answers into one overloaded card.

## 6. Sentence design

Prefer short declarative prompts.

Good:

- `給与は手取額ではなく {{c1::総額}} を費用計上する。`
- `控除した所得税は {{c2::所得税預り金}} で処理する。`

Avoid:

- one long sentence containing several hidden parallel outcomes;
- a single Cloze spanning an entire journal-entry rule;
- a card whose answer cannot be named without reproducing a clause.

## 7. Lifecycle

A retired Note remains in `production/notes/` with:

- immutable `ID`;
- historical `ALP_IDs`;
- `Status=deprecated`;
- `QA=pass` once the retirement is audited;
- `status::deprecated` tag.

Deprecated Notes are excluded from active export and their IDs must never be reused.

## 8. Accuracy override

Conciseness never overrides accounting accuracy. If a one-word prompt would create a false generalization, keep enough visible context or use a short phrase exception.

Transaction duality must remain expressed through total debit/credit equality, not as though every account in a compound entry changes by the same amount.

## 9. FND-00 audit history

### v1.1 — ANKI-AUDIT-001

- 91 historical rows
- 91 -> 57 approved Notes
- 34 deprecated rows
- source ALPs remained 91/91 actively mapped

### v1.2 — ANKI-AUDIT-002

- approved Notes remained 57
- generated cards 110 -> 58
- repeated same-index grouping used to reduce rotations

### v1.3 — ANKI-AUDIT-003

v1.3 replaces same-index bundling with selective recall + atomic cards:

- historical rows: **91**
- source-reviewed ALPs: **91 / 91**
- approved Notes: **18**
- deprecated rows: **73**
- active direct-recall ALPs: **36 / 91**
- generated active cards: **37**
- each generated card has exactly one Cloze occurrence;
- parallel/conjunction facts are split into separate sentences/cards;
- Cloze answers are normally single canonical terms rather than phrases.

The 36 active ALPs are an audited FND-00 outcome, not a universal percentage target. Apply the same decision gate to ANKI-008 onward and let each chapter's active-recall ratio be determined by exam value.
