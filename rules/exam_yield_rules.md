# Exam-Yield / Active-Deck Rules

Status: **Current authoritative rules — living specification**
Audit lineage: ANKI-AUDIT-001/002/003/004/005/006 (#56, #58, #62, #66, #68, #70)
Governance: `GOVERNANCE.md`

This file is part of the current rule set. It governs active-deck selection, integration, lifecycle, recall design, and audited completeness. It may be revised when later production evidence supports a better rule; newer merged rules supersede older audit states.

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

Integration is a **compression mechanism, not a license to drop source content**. If an ALP is mapped to an approved Note, the Note text must retain the material proposition needed to recover that ALP, either as direct recall or explicit visible supporting context.

## 3. Cloze span design

A Cloze should normally contain one lexical accounting unit or one short syntactic discriminator.

Preferred forms include:

- `{{c1::資産}}`, `{{c1::負債}}`, `{{c1::純資産}}`;
- `{{c1::仕訳}}`, `{{c1::勘定}}`, `{{c1::転記}}`;
- `{{c1::借}}方`, `{{c1::貸}}方`;
- `{{c1::合計}}試算表`, `{{c1::残高}}試算表`;
- `{{c1::入金}}伝票`, `{{c1::出金}}伝票`, `{{c1::振替}}伝票`;
- account/document/ledger names;
- short syntax-sensitive chunks when the particle is part of the distinction, e.g. `{{c1::に終わる}}` and `{{c1::から始まる}}`.

Avoid one Cloze containing a list, several joined answers, a whole explanatory clause, or an entire journal-entry procedure when shorter answer units are possible.

## 4. Formula itemization

Introduced in FND-00 v1.6 and now part of the current general rule: for arithmetic or accounting relationships, keep the operator visible and Cloze the **individual terms**, not the whole expression.

Preferred:

`当期純利益＝{{c1::収益}}－{{c1::費用}}`

`純売上高＝{{c1::総売上高}}－{{c1::売上戻り高}}`

Avoid:

`当期純利益＝{{c1::収益－費用}}`

This makes each component independently retrievable while still producing one card because all spans share `c1`. The same principle applies to conceptual relationships when the terms themselves are the learning targets.

## 5. Same-card parallelism

Parallel facts belonging to one retrieval operation use separate spans with the **same** Cloze index:

`{{c1::A}}・{{c1::B}}`

Do not use `{{c1::A・B}}`, and do not introduce `c2+` merely because the card has another blank. A new index is justified only for a genuinely independent review operation.

Thus card count is the number of distinct Cloze indices; Cloze-span count is tracked separately.

## 6. Visible-context rule

After all `c1` answers are hidden, the remaining text must still identify the subject and retrieval frame.

Good visible anchors include `3伝票制では`, `試算表の種類では`, `主要簿では`, `補助簿では`, `証ひょうの種類では`, and other domain cues that do not themselves reveal the answer.

Do **not** add a cue that contains the answer being tested. For example, a card whose answer includes `簿記` must not begin with `簿記の基本では、` solely as a topic label.

## 7. Visible-answer anti-leak rule

A hidden answer must not be reproduced verbatim elsewhere in the visible portion of the same generated card.

Bad:

`簿記の基本では、… {{c1::簿記}} …`

Bad:

`借方・貸方の合計を集計するのは {{c1::合計}}試算表…`

Prefer paraphrased cues:

`各勘定の借貸それぞれの総額を並べるのが {{c1::合計}}試算表…`

For QA, exact visible repetition of a Cloze answer of two or more characters is treated as leakage. One-character discriminators such as `借` / `貸` are exempt from the generic substring check but remain subject to their dedicated formatting rule.

## 8. Debit / credit formatting

When the retrieval target is the side `借方` / `貸方`, hide only the first character:

- `{{c1::借}}方`
- `{{c1::貸}}方`

The same form applies in compounds such as `{{c1::貸}}方残高`.

## 9. Completeness inside integrated cards

Strengthened in FND-00 v1.6 and now part of the current general rule: when several ALPs are compressed into one card, preserve the source distinctions that remain useful for exam reading or mechanics. Do not replace a source family with only one or two examples when the inventory explicitly treats the family as an included learning point.

Examples for FND-00:

- the expense-account family retains all representative source categories (`給料`, `水道光熱費`, `旅費交通費`, `広告宣伝費`, `消耗品費`, `通信費`, `保険料`, `保管費`, `諸会費`, `雑費`);
- the general-ledger card retains `標準式` and `残高式` plus their material field differences;
- the subsidiary-book card retains the material mechanics for cash, current-account, petty-cash, bill, receivable/payable subledgers, and human-name accounts;
- the posting card states explicitly that subsidiary ledgers are posted from each voucher by `個別転記`;
- temporary-account cards retain both process and classification (`仮払金` as an asset; `仮受金` as a liability).

Visible supporting detail does not need its own Cloze when masking it would add little retrieval value, but it must not disappear merely for brevity.

## 10. Sentence design

Prefer short declarative clauses. Multiple clauses may share `c1` when they remain one coherent retrieval set. Visible supporting facts may be retained when masking them would create redundant review cost.

Conciseness never overrides accounting accuracy, source completeness, or answer clarity.

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

These counts are chapter outcomes, not universal quotas. Future chapters should use the current rules, and later audits may improve them further.

## 13. Rule evolution

When later chapter work exposes a better active-deck or recall rule, update this file and the related general rules explicitly. Do not preserve an inferior rule merely because it was part of v1.0 or an earlier audit version.

For an existing batch, record whether the new rule applies immediately as a repository-wide invariant or only after an explicit chapter migration. Preserve historical audit metrics as history rather than rewriting them to look as though the newer rule always existed.
