# COM-03 Production QA

Issue: **ANKI-010 / #11; ANKI-AUDIT-010 / #84**
Chapter: **Commercial 03 — 現金預金**
Rules: current living `SPEC.md`, `rules/*.md`, and `rules/recall_precision_rules.md`
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`

## Result

- approved Notes: **25**
- generated cards: **25**
- Cloze spans: **66**
- canonical included ALPs: **38**
- mapped included ALPs: **38**
- unmapped included ALPs: **0**
- ALPs mapped more than once: **0**
- coherent multi-ALP Notes: **9**
- journal-entry primary Notes: **7**
- measurement Notes: **2**
- decorative-example exclusions: **2**
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No COM-03 pilot Note IDs existed. Production IDs are allocated deterministically in primary canonical ALP order as `BK-COM-03-0001`–`BK-COM-03-0025`.

## Coverage architecture

| Note | Canonical ALPs | Retrieval unit |
|---|---|---|
| 0001 | 0001–0003 | 現金の範囲・通貨代用証券・郵便切手除外 |
| 0002 | 0004 | 現金過不足の定義 |
| 0003 | 0005–0006 | 期中の不足・超過と原因判明時処理 |
| 0004 | 0007 | 期中発生差額の決算整理 |
| 0005 | 0008–0009 | 決算日新規差額の直接修正 |
| 0006 | 0010 | 現金実査額 |
| 0007 | 0011 | 未使用郵便切手の決算整理 |
| 0008 | 0012 | 当座預金の基礎 |
| 0009 | 0013–0015 | 振出・他人振出受取・自己振出受取の比較 |
| 0010 | 0016 | 普通預金・定期預金の分類 |
| 0011 | 0017 | 銀行手数料・預金利息の勘定選択 |
| 0012 | 0018 | 当座借越契約の定義 |
| 0013 | 0019–0021 | 当座借越の期中・決算・翌期首 |
| 0014 | 0022 | 銀行勘定調整表の定義 |
| 0015 | 0023–0024 | 当社側／銀行側修正と最終残高 |
| 0016 | 0025 | 未渡・未取付・未取立の用語識別 |
| 0017 | 0026 | 未通知・誤記入の当社側修正 |
| 0018 | 0027–0028 | 未渡小切手の仕訳と負債残存 |
| 0019 | 0029–0031 | 時間差項目の銀行側加減 |
| 0020 | 0032 | 未渡小切手と未取付小切手の判別 |
| 0021 | 0033 | 小口現金の定義・分類 |
| 0022 | 0034 | 定額資金前渡制度 |
| 0023 | 0035 | 小口現金の処理順序 |
| 0024 | 0036–0037 | 前渡・報告・補給と複数支払仕訳 |
| 0025 | 0038 | インプレストの補給額 |

The two inventory rows with `status=EXCLUDE` are decorative numerical examples. No canonical included ALP is excluded from active Text.

## Recall-design QA

### Journal entries

New production follows `rules/recall_precision_rules.md`:

- debit/credit markers and separators remain visible;
- account names are Clozed separately with the same `c1` for one coherent entry;
- whole journal-entry tuples are not hidden inside one Cloze span;
- repeated accounts are hidden in every occurrence where leaving one visible would leak the answer;
- copied example amounts are not made into trivia Clozes.

Representative forms include:

- shortage: `（借）{{c1::現金過不足}}／（貸）{{c1::現金}}`
- unused stamps: `（借）{{c1::貯蔵品}}／（貸）{{c1::通信費}}`
- undelivered check: `（借）{{c1::当座預金}}／（貸）{{c1::買掛金}}`
- petty-cash advance/replenishment: `（借）{{c1::小口現金}}／（貸）{{c1::当座預金}}`

### Canonical-label priority

Definitions and named distinctions Cloze the canonical term when label identification is the retrieval target, including:

- 現金過不足
- 銀行勘定調整表
- 未渡小切手 / 未取付小切手 / 未取立小切手
- 定額資金前渡制度

### Minimal Cloze scope

The recall-precision rule now requires the smallest uniquely recoverable answer and rejects broad action phrases when the useful target is the discriminator that determines the treatment.

COM-03 was re-audited accordingly:

- `{{c1::当社側の修正項目}}` / `{{c1::銀行側の修正項目}}` became `{{c1::当社}}側` / `{{c1::銀行}}側`.
- `{{c1::仕訳を行う}}` and `{{c1::仕訳を行わない}}` were removed as Cloze answers; journal treatment remains visible.
- Bank-side timing differences retain the precise operators `{{c1::加算}}` / `{{c1::減算}}`.
- The petty-cash sequence no longer hides four long step phrases. It keeps the procedure frame visible and tests only the short sequence-critical labels `{{c1::報告}}` and `{{c1::補給}}`.

### Measurement and procedures

- `現金実査額＝通貨＋通貨代用証券` keeps the operator visible and masks the operands.
- Bank-side timing differences test `加算` / `減算`; the no-journal treatment remains visible context rather than a broad Cloze answer.
- Petty cash keeps the ordered procedure and the replenishment measurement as separate retrieval units.

## Deterministic validation

Run:

```text
python scripts/validate_com03_production.py
```

Expected result:

```text
COM-03 production validation: PASS
notes=25 cards=25 cloze_spans=66 included_alps=38 mapped=38 unmapped=0
multi_alp_notes=9 journal_entry_notes=7 measurement_notes=2 decorative_exclusions=2
account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass visible_answer_leakage=0 deterministic_order=pass
```

The validator checks stable IDs/order, exact source provenance, required tags/lifecycle, c1-only card generation, exact-once ALP mapping, local duplicate rendered text, visible-answer leakage, account-level journal Clozes, selected canonical-label forms, minimal Cloze scope for the audited patterns, and measurement/procedure precision.
