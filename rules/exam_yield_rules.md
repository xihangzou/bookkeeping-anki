# Exam-Yield / Active-Deck Rules

Status: **Current authoritative rules — living specification**
Audit lineage: ANKI-AUDIT-001/002/003/004/005/006 (#56, #58, #62, #66, #68, #70), COM-01 v1.7/v1.8 precision audits
Governance: `GOVERNANCE.md`

This file is part of the current rule set. It governs active-deck selection, integration, lifecycle, recall design, audited completeness, wording, and ALP containment. It may be revised when later production evidence supports a better rule; newer merged rules supersede older audit states.

## 1. Primary target

Review and trace **100% of canonical included ALPs**, then compress study cost primarily through **coherent integration**, not aggressive retirement.

For foundational material, useful problem-reading vocabulary, account classification, journal logic, ledger/voucher/document workflows, formulas, and recurring notation may remain active when they can be integrated without making the card ambiguous.

Do not force every proposition into its own card. Conversely, do not retire or silently omit a useful ALP merely to hit an arbitrary card or Cloze-span quota.

## 2. Integration-first card control

Before creating or retaining another card, ask whether the ALP fits an existing retrieval frame.

Good integration families include:

- `仕訳 / 勘定 / 転記 / 複合仕訳 / 諸口`;
- five-element classification plus closely related statement placement;
- accounting-period vocabulary plus the bookkeeping cycle;
- payroll treatments that share one recognition frame;
- subsidiary-book families;
- voucher selection and closely related voucher rules;
- individual/aggregate posting workflow;
- source-document identification and inference;
- abbreviations and symbols used to read bookkeeping questions.

Integration must remain semantically coherent. If adding an ALP changes the card into a second unrelated retrieval task, use another Note rather than overloading the first.

Integration is a **compression mechanism, not a license to drop source content**. If an ALP is mapped to an approved Note, the Note `Text` should retain the material proposition needed to recover that ALP, either as direct recall or explicit visible supporting context. `Extra` may explain or disambiguate, but should not be the only place where a mapped ALP materially survives.

## 3. Cloze span design

A Cloze should normally contain one lexical accounting unit, one account/method/document name, or one short syntactic discriminator.

Preferred forms include:

- `{{c1::資産}}`, `{{c1::負債}}`, `{{c1::純資産}}`;
- `{{c1::仕訳}}`, `{{c1::勘定}}`, `{{c1::転記}}`;
- `{{c1::借}}方`, `{{c1::貸}}方` when side direction itself is the target;
- `{{c1::合計}}試算表`, `{{c1::残高}}試算表`;
- `{{c1::入金}}伝票`, `{{c1::出金}}伝票`, `{{c1::振替}}伝票`;
- account/document/ledger/method names;
- short syntax-sensitive chunks when the particle is part of the distinction, e.g. `{{c1::に終わる}}` and `{{c1::から始まる}}`.

Avoid one Cloze containing a list, several joined conceptual answers, or a whole explanatory clause when shorter answer units are possible.

Function words and limiting particles such as `のみ` should normally stay **outside** the Cloze unless the particle itself is the distinction being tested. Prefer `{{c1::数量}}のみ` to `{{c1::数量のみ}}`.

When a source gives a definition and a technical name, prefer leaving the definition visible and Clozing the **name** when name retrieval is the useful operation. Example: `帳簿上の在庫数量を{{c1::帳簿棚卸数量}}という`.

## 4. Formula itemization

For arithmetic or accounting relationships, keep operators visible and Cloze the **individual terms**, not the whole expression.

Preferred:

`当期純利益＝{{c1::収益}}－{{c1::費用}}`

`純売上高＝{{c1::総売上高}}－{{c1::売上戻り高}}`

Avoid:

`当期純利益＝{{c1::収益－費用}}`

This makes each component independently retrievable while still producing one card because all spans share `c1`.

If the same term is structurally reused within one coherent formula family, the same answer may appear in more than one same-index Cloze when hiding every occurrence is necessary to avoid answer leakage or to preserve the complete relationship. Example:

`{{c1::売上原価}}＝...、売上総利益＝{{c1::売上高}}－{{c1::売上原価}}`

Repeated same-answer spans are an exception for deliberate formula reuse, not a general duplication pattern.

## 5. Same-card parallelism

Parallel facts belonging to one retrieval operation use separate spans with the **same** Cloze index:

`{{c1::A}}・{{c1::B}}`

Do not use `{{c1::A・B}}`, and do not introduce `c2+` merely because the card has another blank. A new index is justified only for a genuinely independent review operation.

Thus card count is the number of distinct Cloze indices; Cloze-span count is tracked separately.

## 6. Visible-context and method-name rule

After all `c1` answers are hidden, the remaining text must still identify the subject and retrieval frame.

Good visible anchors include `3伝票制では`, `試算表の種類では`, `主要簿では`, `補助簿では`, `証ひょうの種類では`, and explicit accounting-method names.

When several methods could plausibly fit the same wording, **name the method visibly** rather than relying on an indirect description. For example, use `売上原価対立法では、...` instead of `販売時に収益と原価を同時記録する方式では、...`.

Do **not** add a cue that contains the answer being tested. A card whose answer includes `簿記` must not begin with `簿記の基本では、` solely as a topic label.

## 7. Visible-answer anti-leak rule

A hidden answer must not be reproduced verbatim elsewhere in the visible portion of the same generated card.

Bad:

`簿記の基本では、… {{c1::簿記}} …`

Bad:

`借方・貸方の合計を集計するのは {{c1::合計}}試算表…`

Prefer paraphrased cues:

`各勘定の借貸それぞれの総額を並べるのが {{c1::合計}}試算表…`

For QA, exact visible repetition of a Cloze answer of two or more characters is treated as leakage. One-character discriminators such as `借` / `貸` are exempt from the generic substring check but remain subject to their dedicated formatting rule. Deliberately repeated same-index formula terms are not leakage because all occurrences are hidden.

## 8. Journal-entry recall

Choose the Cloze target according to the learning objective.

- If the target is only debit/credit **direction**, use `{{c1::借}}方` / `{{c1::貸}}方`.
- If the target is **account selection**, Cloze the account names.
- If the target is the **whole compact journal entry**, it is acceptable to Cloze the structured entry itself, e.g. `{{c1::（借）仕入／（貸）繰越商品}}`, when splitting it would reduce the retrieval task to trivial direction guessing or create visible-answer leakage.

The compact-journal-entry exception may contain standard entry punctuation and exceed the normal lexical-span length. It applies only to a short, conventional journal-entry tuple, not to explanatory prose or a multi-step procedure.

## 9. Completeness inside integrated cards

When several ALPs are compressed into one card, preserve the source distinctions that remain useful for exam reading or mechanics. Do not replace a source family with only one or two examples when the inventory explicitly treats the family as an included learning point.

For each mapped ALP, perform a **material-proposition check** against the inventory summary and source when necessary:

1. identify the proposition that makes the ALP distinct;
2. verify that proposition is recoverable from the active Note `Text`;
3. restore omitted distinctions as direct Clozes or concise visible context;
4. use `Extra` only for secondary explanation, aliases, or rationale.

Examples of distinctions that should not disappear merely for brevity include:

- a method's complete account family;
- both the general rule and the application consequence of FIFO;
- recognition timing plus subsequent settlement treatment;
- a formula and a linked formula that reuses its result;
- the difference between a physical/quantity phenomenon and the expense account used to record it;
- classification conditions such as `帳簿棚卸数量＞実地棚卸数量` or `取得原価＞正味売却価額` when those conditions are part of the mapped ALP.

## 10. Sentence design and style

Use short declarative Japanese. Prefer the terminology used in the source and in bookkeeping questions.

- Put the **accounting subject first**: `三分法では`, `売上原価対立法では`, `商品有高帳は`.
- Prefer direct wording over indirect descriptions such as `〜する方式では` when the method name is known.
- Avoid parenthetical classification when it can be written naturally as visible prose: prefer `資産の{{c1::商品}}` to `{{c1::商品}}（資産）`.
- Avoid overly broad answers such as full explanatory phrases when a short discriminator is enough.
- Do not make brevity the goal by itself. Concision never overrides accounting accuracy, ALP completeness, or answer clarity.
- FND-00 v1.6 is the default style reference for integrated, context-rich, short-answer production Notes unless a chapter-specific accounting mechanic requires a justified exception.

## 11. Lifecycle and stable IDs

Retired Notes remain in production history with immutable IDs and historical ALP mappings. A historical Note may be reactivated only within the same lineage after review; its stable ID is never reassigned to unrelated content.

These are persistent lineage rules under `GOVERNANCE.md`, not consequences of a v1.0 freeze.

## 12. FND-00 audit history

- **v1.1 / #56:** 91 -> 57 approved Notes.
- **v1.2 / #58:** 110 -> 58 generated cards through same-index grouping.
- **v1.3 / #62:** aggressive screening reduced the deck to 18 cards / 36 active ALPs.
- **v1.4 / #66:** screening was relaxed and integration-first compression restored 29 cards / 61 active ALPs.
- **v1.5 / #68:** remaining useful ALPs were re-integrated, answer leakage was removed, and all canonical FND-00 ALPs returned to active coverage.
- **v1.6 / #70:** mapped-but-underrepresented source content was restored, formulas were itemized, and the 32-card integration architecture was retained.

### FND-00 v1.6 result

- historical rows: **91**;
- source-reviewed ALPs: **91 / 91**;
- active direct-recall ALPs: **91 / 91**;
- approved Notes / generated cards: **32**;
- deprecated historical rows: **59**;
- active Cloze spans: **150**;
- every approved Note uses only `c1`;
- exact visible-answer leakage for answers of 2+ characters: **0**;
- arithmetic/formula operators remain visible and formula terms are separately Clozed;
- all ten representative expense-account categories from the source are present;
- `標準式` / `残高式` and material general-ledger mechanics are present;
- `BK-FND-00-0084` states that subsidiary ledgers receive `{{c1::個別転記}}` from each voucher;
- debit/credit directions use first-character Clozes;
- `BK-FND-00-0018` has no answer-leaking `簿記の基本では、` prefix;
- `BK-FND-00-0027` uses `{{c1::に終わる}}` / `{{c1::から始まる}}`.

These counts are chapter outcomes, not universal quotas.

## 13. COM-01 precision audit lineage

COM-01 v1.7 established the FND-style precision baseline: redundant classification Clozes were removed, broad phrase answers shortened, visible method/context cues strengthened, and visible-answer leakage held at zero.

COM-01 v1.8 adds the following generalizable refinements:

- Cloze the three 三分法 account names as well as the `決算整理` timing;
- when the whole closing entry is the retrieval target, Cloze the compact journal-entry tuple instead of merely `借` / `貸`;
- state `売上原価対立法` explicitly on its mechanics and sale-entry cards;
- retain the reused `売上原価` term as a hidden term in the gross-profit formula;
- keep `のみ` outside a quantity Cloze;
- replace broad purchase/sale cost phrases with shorter discriminators (`購入`, `販売`, `未販売在庫`);
- when a definition maps terminology, Cloze the terminology name rather than hiding the descriptive definition;
- restore mapped-but-compressed ALP distinctions such as prepayment timing, the explicit FIFO premise, complete shrinkage formulas, and lower-of-cost valuation formulas.

## 14. Rule evolution

When later chapter work exposes a better active-deck, wording, containment, or recall rule, update this file and related validators explicitly. Do not preserve an inferior rule merely because it was part of v1.0 or an earlier audit version.

For an existing batch, record whether the new rule applies immediately as a repository-wide invariant or only after an explicit chapter migration. Preserve historical audit metrics as history rather than rewriting them to look as though the newer rule always existed.
