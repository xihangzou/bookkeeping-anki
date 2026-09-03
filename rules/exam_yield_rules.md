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

v1.3 explicitly separates two metrics.

### Source-reviewed coverage

Every canonical included ALP must remain represented in production history and must have an auditable include/exclude or retirement decision.

### Active direct-recall coverage

Only ALPs that justify spaced retrieval need to remain mapped to `Status=approved` Notes.

Unlike v1.1/v1.2, an included ALP does **not** need an approved mapping merely to preserve source traceability. Do not create an artificial active card solely to keep an ALP active-mapped.

## 3. Active-card selection gate

Keep an active Note only when all are true:

- the target is independently worth spaced retrieval;
- forgetting it can plausibly change an exam answer or later accounting reasoning;
- it is not already tested by a stronger downstream card;
- it can be asked with short, unambiguous visible context;
- the expected answer class is canonical enough to grade mentally.

When these conditions fail, deprecate rather than retain a low-yield card.

## 4. Cloze lexicality — v1.3

A Cloze span should normally contain **one lexical accounting unit**, not a compound phrase, list, or explanatory clause.

Preferred targets include:

- `資産`, `負債`, `純資産`, `収益`, `費用`;
- `借方`, `貸方`;
- `試算表`, `合計試算表`, `残高試算表`;
- `所得税預り金`, `法定福利費`;
- `仮払金`, `仮受金`;
- `入金伝票`, `出金伝票`, `振替伝票`;
- `納品書`, `請求書`, `領収書`.

Avoid one Cloze that hides:

- `A・B・C` as a single answer;
- an entire journal-entry rule;
- a reason plus conclusion;
- a conjunction-linked procedure;
- an explanatory clause when a canonical noun, account, direction, or short predicate can be used.

If a source phrase contains multiple independently meaningful lexical targets, split the **Cloze spans**, not necessarily the card. Example:

`資産・費用の増加は {{c1::借方}}。負債・純資産・収益の増加は {{c1::貸方}}。`

A short predicate such as `ならない` is permitted when a noun substitute would distort the accounting meaning.

## 5. Parallel / conjunction rule — v1.3

Parallel or conjunction-linked facts that belong to **one coherent retrieval operation** should stay on the **same Anki card**, while each answer is masked separately with the same Cloze index.

Use:

`{{c1::A}}・{{c1::B}}`

not:

`{{c1::A・B}}`

and not, merely for parallelism:

`{{c1::A}}・{{c2::B}}`.

Examples that normally use the same index within one Note:

- five accounting elements;
- debit/credit sides of one classification rule;
- employee/employer treatments in one payroll comparison;
- trial-balance types;
- voucher types;
- source-document types;
- paired recognition/settlement outcomes that are naturally recalled together.

Use a new index (`c2+`) only when the second retrieval operation is independently worth rotating as a separate card, not merely because it is another blank or another sentence.

Thus **card count is the number of distinct Cloze indices**, while **Cloze-span count** is tracked separately as an atomicity metric.

## 6. Sentence design

Prefer short declarative sentences. Multiple short sentences may share the same `c1` when they are parts of one coherent card.

Good:

`給与は手取額ではなく {{c1::総額}} を費用計上する。控除した所得税は {{c1::所得税預り金}} で処理する。`

Good:

`現金が増える取引は {{c1::入金伝票}}。現金が減る取引は {{c1::出金伝票}}。現金が増減しない取引は {{c1::振替伝票}}。`

Avoid long prose with one large Cloze spanning several answers.

## 7. Lifecycle

A retired Note remains in `production/notes/` with:

- immutable `ID`;
- historical `ALP_IDs`;
- `Status=deprecated`;
- `QA=pass` once retirement is audited;
- `status::deprecated` tag.

Deprecated Notes are excluded from active export and their IDs must never be reused.

## 8. Accuracy override

Conciseness never overrides accounting accuracy. If a one-word prompt would create a false generalization, keep enough visible context or use a short lexical/predicate exception.

Transaction duality must remain expressed through total debit/credit equality, not as though every account in a compound entry changes by the same amount.

## 9. FND-00 audit history

### v1.1 — ANKI-AUDIT-001

- 91 historical rows
- 91 -> 57 approved Notes
- 34 deprecated rows

### v1.2 — ANKI-AUDIT-002

- approved Notes remained 57
- generated cards 110 -> 58
- same-index grouping introduced as a rotation-efficiency tool

### v1.3 — ANKI-AUDIT-003

v1.3 combines aggressive low-yield retirement with **lexical span splitting inside the same coherent card**:

- historical rows: **91**;
- source-reviewed ALPs: **91 / 91**;
- approved Notes: **18**;
- deprecated rows: **73**;
- active direct-recall ALPs: **36 / 91**;
- generated active cards: **18**;
- active Cloze spans: **36**;
- every approved FND-00 Note uses only `c1`;
- parallel/conjunction answers are separate `{{c1::...}}` spans on that same card;
- Cloze answers are normally single canonical terms rather than compound phrases.

The 36 active ALPs are an audited FND-00 outcome, not a universal percentage target. Apply the same selection and lexical-splitting principles during ANKI-008 onward generation; let each chapter's active-recall ratio and card count be determined by exam value.
