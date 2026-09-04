# COM-04 Production QA

Issue: **ANKI-011 / #12**
Chapter: **Commercial 04 — 債権債務**
Rules: current living `SPEC.md`, `rules/*.md`, and `rules/recall_precision_rules.md`
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`

## Result

- approved Notes: **29**
- generated cards: **29**
- Cloze spans: **94**
- canonical included ALPs: **41**
- mapped included ALPs: **41**
- unmapped included ALPs: **0**
- ALPs mapped more than once: **0**
- coherent multi-ALP Notes: **8**
- journal-entry primary Notes: **14**
- formula Notes: **2**
- decorative-example exclusions: **1**
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No COM-04 pilot Note IDs existed. Production IDs are allocated deterministically in primary canonical ALP order as `BK-COM-04-0001`–`BK-COM-04-0029`.

## Coverage architecture

| Note | Canonical ALPs | Retrieval unit |
|---|---|---|
| 0001 | 0001 | 発生原因による債権債務の勘定選択 |
| 0002 | 0002–0003 | 立替金・仕入原価除外・買掛金との相殺 |
| 0003 | 0004 | 受取商品券の発生と精算 |
| 0004 | 0005–0006 | クレジット売掛金と信販手数料の認識時点 |
| 0005 | 0007 | 商品売買以外の未収入金・未払金 |
| 0006 | 0008–0009 | 貸付・借入元本と利息勘定 |
| 0007 | 0010 | 利息の年額・月割・日割計算 |
| 0008 | 0011 | 利息控除後借入の総額測定 |
| 0009 | 0012 | 役員・従業員との資金貸借勘定 |
| 0010 | 0013 | 手形貸付金・手形借入金と商取引手形の区別 |
| 0011 | 0014 | 約束手形・受取手形・支払手形 |
| 0012 | 0015 | 商品売買での手形発生仕訳 |
| 0013 | 0016 | 手形の満期決済仕訳 |
| 0014 | 0017 | 掛債権債務から手形への振替 |
| 0015 | 0018–0019 | 手形裏書の譲渡側・譲受側処理 |
| 0016 | 0020 | 自己振出手形の裏書受入例外 |
| 0017 | 0021 | 手形割引と手形売却損 |
| 0018 | 0022 | 手形割引料の計算式 |
| 0019 | 0023 | 電子記録債権・債務の発生記録と決済 |
| 0020 | 0024–0026 | 電子記録債権の譲渡・分割・売却損 |
| 0021 | 0027 | 不渡手形の定義 |
| 0022 | 0028 | 手元手形の不渡りと拒絶証書費用 |
| 0023 | 0029 | 不渡手形の回収と延滞利息 |
| 0024 | 0030 | 裏書・割引済手形の不渡りと償還 |
| 0025 | 0031 | 手形更改の定義・承諾 |
| 0026 | 0032 | 更改時の債務者・債権者仕訳 |
| 0027 | 0033–0034 | 商品売買／非商品取引の手形勘定比較 |
| 0028 | 0035–0037, 0040–0041 | 債務保証・対照勘定・偶発債務・表示・裏書割引との関係 |
| 0029 | 0038–0039 | 保証消滅と代位弁済時の求償権 |

The single inventory row with `status=EXCLUDE` is the chapter-wide decorative numerical-example family. No canonical included ALP is excluded from active Text. The canonical ANKI-003 inventory remains unchanged with empty `note_ids` and `qa_status=pending`; production mapping lives in each Note's `ALP_IDs` field.

## Recall-design QA

### Journal entries

COM-04 follows the current account-level rule directly at initial generation:

- debit/credit markers and separators remain visible;
- each account name is Clozed separately with the same `c1` when the entry is one coherent retrieval unit;
- no whole journal-entry tuple is hidden inside a single Cloze span;
- repeated account answers are hidden at every occurrence when leaving one visible would leak the answer;
- copied numerical examples are not used as trivia Clozes.

Representative forms include:

- advance paid for counterparty: `（借）{{c1::立替金}}／（貸）{{c1::現金}}`
- note issuance: `（借）{{c1::仕入}}／（貸）{{c1::支払手形}}`
- receivable conversion: `（借）{{c1::受取手形}}／（貸）{{c1::売掛金}}`
- dishonor: `（借）{{c1::不渡手形}}／（貸）{{c1::受取手形}}`
- guarantee memorandum: `（借）{{c1::保証債務見返}}／（貸）{{c1::保証債務}}`

### Canonical-label priority and minimal scope

Named accounting concepts are targeted directly where label identification is useful, including `約束手形`, `手形の裏書`, `手形の割引`, `不渡手形`, `手形の更改`, `債務の保証`, and `偶発債務`.

Broad action phrases such as `仕訳を行う`, `処理する`, or whole explanatory clauses are not Cloze answers. Procedures and comparisons retain visible context while targeting short discriminators such as `相殺`, `譲渡記録`, `分割`, and `承諾`.

### Formulas and measurement

Operators remain visible and formula operands are itemized on the same `c1` card:

- `利息＝{{c1::元金}}×{{c1::年利率}}`
- month allocation `×{{c1::月数}}/12`
- day allocation `×{{c1::日数}}/365`
- `割引料＝{{c1::手形金額}}×{{c1::割引率}}×{{c1::割引日数}}÷365`

The interest-deducted borrowing Note tests the gross-liability measurement rule rather than memorizing an example amount.

## Deterministic validation

Run:

```text
python scripts/validate_com04_production.py
```

Expected result:

```text
COM-04 production validation: PASS
notes=29 cards=29 cloze_spans=94 included_alps=41 mapped=41 unmapped=0
multi_alp_notes=8 journal_entry_notes=14 formula_notes=2 decorative_exclusions=1
account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass visible_answer_leakage=0 deterministic_order=pass
```

The validator checks stable IDs/order, exact source provenance, deterministic tags/lifecycle, c1-only card generation, exact-once ALP mapping, canonical ANKI-003 inventory immutability, primary source-section consistency, local duplicate rendered text, visible-answer leakage, account-level journal Clozes, canonical-label forms, formula itemization, minimal Cloze scope, and preservation of the decorative exclusion.
