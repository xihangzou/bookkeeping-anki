# Exam-Yield / Active-Deck Rules

Status: **v1.4 post-freeze overlay — ANKI-AUDIT-001/002/003/004 (#56, #58, #62, #66)**

This file is a post-freeze overlay on the frozen v1.0 source/schema/stable-ID contract in `SPEC.md`, `rules/cloze_rules.md`, `rules/coverage_rules.md`, and `schema/note_schema.yaml`.

The frozen source/schema/stable-ID contract remains authoritative. This overlay governs **active-deck selection, lifecycle handling, integration, and recall design**.

## 1. Primary target

The canonical inventory must remain **100% reviewed and traceable**. The active deck should retain the material that materially improves bookkeeping exam performance, problem reading, and later 2級 / CPA reasoning without turning every source proposition into a separate card.

v1.4 deliberately relaxes the aggressive v1.3 importance gate. Card-count control should come first from **coherent integration and same-card Cloze grouping**, and only secondarily from retirement.

Direct recall is favored when omission could plausibly cause:

1. wrong account or five-element classification;
2. wrong debit/credit direction;
3. wrong recognition decision;
4. wrong journal entry or settlement treatment;
5. wrong calculation or formula;
6. failure to distinguish a testable control, voucher, ledger, or source document;
7. failure to apply an important exception;
8. inability to parse recurring bookkeeping terminology, period notation, ledger structure, or workflow;
9. loss of a durable accounting relationship needed later.

Purely decorative wording, exact duplicates, long form-field lists, and facts already fully tested by a stronger integrated card may remain only in historical rows / QA context.

## 2. Source coverage vs active recall

Two metrics remain separate.

### Source-reviewed coverage

Every canonical included ALP must remain represented in production history and must have an auditable include/exclude or retirement decision.

### Active direct-recall coverage

An included ALP does not need an approved mapping merely to preserve traceability. However, v1.4 uses a **moderately permissive** active-recall threshold: useful foundational terminology, period-reading rules, bookkeeping workflow, main/subsidiary book structure, and representative account-selection rules may remain active even when they are not the single highest-yield exam fact.

Do not keep an ALP active solely for numerical coverage; keep it when it contributes meaningful recall or problem comprehension.

## 3. Integration-first card control — v1.4

Before retiring a useful ALP, ask whether it can be integrated into a coherent existing card.

Good integration candidates share a natural retrieval frame, for example:

- `仕訳 / 勘定 / 転記` as the bookkeeping recording process;
- main books plus `元丁 / 仕丁` as one posting-reference system;
- subsidiary-book types plus receivable/payable subledger organization;
- voucher type selection plus the account-field rule;
- source-document identification plus a closely related inference constraint.

Do not integrate merely because two facts are nearby in the textbook. The visible prompt must still define one coherent retrieval operation.

## 4. Cloze lexicality

A Cloze span should normally contain **one lexical accounting unit**, not a compound phrase, list, or explanatory clause.

Preferred targets include:

- `資産`, `負債`, `純資産`, `収益`, `費用`;
- the distinguishing first character in `借方 / 貸方`: `{{c1::借}}方`, `{{c1::貸}}方`;
- `仕訳`, `勘定`, `転記`;
- `試算表`, or the distinguishing prefix in a trial-balance name such as `{{c1::合計}}試算表`;
- account names such as `所得税預り金`, `法定福利費`;
- voucher discriminators such as `{{c1::入金}}伝票`, `{{c1::出金}}伝票`, `{{c1::振替}}伝票`;
- document names such as `納品書`, `請求書`, `領収書`.

Avoid one Cloze that hides:

- `A・B・C` as a single answer;
- an entire journal-entry rule;
- a reason plus conclusion;
- a conjunction-linked procedure;
- an explanatory clause when a canonical noun, account, direction, prefix, or short predicate can be used.

A short predicate such as `ならない` is permitted when a noun substitute would distort the accounting meaning.

## 5. Parallel / conjunction rule

Parallel or conjunction-linked facts that belong to **one coherent retrieval operation** stay on the **same Anki card**, while each answer is masked separately with the same Cloze index.

Use:

`{{c1::A}}・{{c1::B}}`

not:

`{{c1::A・B}}`

and not, merely for parallelism:

`{{c1::A}}・{{c2::B}}`.

Use a new index (`c2+`) only when the second retrieval operation is independently worth rotating as a separate card.

Thus **card count is the number of distinct Cloze indices**, while **Cloze-span count** is tracked separately.

## 6. Visible-context rule — v1.4

After the Cloze answer is hidden, the remaining text must still make the **topic and retrieval frame identifiable**.

Bad:

`現金が増える取引は {{c1::入金伝票}}。現金が減る取引は {{c1::出金伝票}}。現金が増減しない取引は {{c1::振替伝票}}。`

When all answers are hidden, the learner is not explicitly told that the card is about vouchers.

Preferred:

`3伝票制では、現金が増える取引に {{c1::入金}}伝票、現金が減る取引に {{c1::出金}}伝票、現金が増減しない取引に {{c1::振替}}伝票を用いる。`

Likewise, use visible anchors such as `簿記の5要素では`, `試算表の種類では`, `主要簿では`, `補助簿では`, `費用科目の選択では`, or `証ひょうの種類では` when the hidden answers would otherwise erase the domain.

Do not solve context loss by making the Cloze span longer. Keep the answer lexical and improve the visible prompt instead.

## 7. Debit / credit formatting rule

When the intended answer is simply the side `借方` or `貸方`, Cloze only the distinguishing first character:

- `{{c1::借}}方`
- `{{c1::貸}}方`

This leaves `方` visible, preserves the answer class, and reduces unnecessary character recall.

The same rule applies inside compounds when direction is the retrieval target, e.g. `{{c1::借}}方残高` / `{{c1::貸}}方残高`.

Do not use `{{c1::借方}}` or `{{c1::貸方}}` on newly generated/audited active cards unless the full word is materially required for a different retrieval operation.

## 8. Sentence design

Prefer short declarative sentences. Multiple short clauses or sentences may share `c1` when they are parts of one coherent card.

Good:

`給与の源泉徴収では、給与は手取額ではなく {{c1::総額}} を費用計上し、控除した所得税は {{c1::所得税預り金}} で処理する。`

Good:

`主要簿では、取引を発生順に記録する {{c1::仕訳帳}} と、勘定科目別に記録する {{c1::総勘定元帳}} を使う。`

Avoid long prose with one large Cloze spanning several answers.

## 9. Lifecycle

A retired Note remains in `production/notes/` with:

- immutable `ID`;
- historical/source-traceable `ALP_IDs`;
- `Status=deprecated`;
- `QA=pass` once retirement is audited;
- `status::deprecated` tag.

A previously retired stable Note may be reactivated after a reviewed audit when its retrieval value is reassessed. The stable ID is reused only for that same historical Note lineage, never reassigned to unrelated content.

Deprecated Notes are excluded from active export.

## 10. Accuracy override

Conciseness never overrides accounting accuracy. If a one-word prompt would create a false generalization, keep enough visible context or use a short lexical/predicate exception.

Transaction duality must remain expressed through total debit/credit equality, not as though every account in a compound entry changes by the same amount.

## 11. FND-00 audit history

### v1.1 — ANKI-AUDIT-001

- 91 historical rows
- 91 -> 57 approved Notes
- 34 deprecated rows

### v1.2 — ANKI-AUDIT-002

- approved Notes remained 57
- generated cards 110 -> 58
- same-index grouping introduced as a rotation-efficiency tool

### v1.3 — ANKI-AUDIT-003

- approved Notes: **18**
- generated cards: **18**
- active direct-recall ALPs: **36 / 91**
- aggressive low-yield retirement plus lexical same-card spans

### v1.4 — ANKI-AUDIT-004

v1.4 corrects the over-aggressive v1.3 screen and makes **integration**, not retirement, the main compression mechanism:

- historical rows: **91**;
- source-reviewed ALPs: **91 / 91**;
- approved Notes: **29**;
- deprecated rows: **62**;
- active direct-recall ALPs: **61 / 91**;
- generated active cards: **29**;
- active Cloze spans: **70**;
- every approved FND-00 Note uses only `c1`;
- related parallel answers remain same-card lexical spans;
- the visible-context rule is enforced for context-sensitive cards;
- debit/credit direction recall uses first-character Clozes.

The FND-00 counts are audited outcomes, not universal percentage targets. Apply the same v1.4 principles during future generation: use a moderately permissive importance screen, integrate coherent facts before retiring them, preserve visible retrieval context, and keep Cloze answers lexical.