# FND-00 Production QA

Issues: ANKI-007 / #8; ANKI-AUDIT-001 / #56; ANKI-AUDIT-002 / #58; ANKI-AUDIT-003 / #62; ANKI-AUDIT-004 / #66

Contracts:
- frozen v1.0 source/schema baseline (`FREEZE.md`, `rules/cloze_rules.md`, `rules/coverage_rules.md`, `schema/note_schema.yaml`)
- current v1.4 post-freeze active-deck / Cloze overlay (`rules/exam_yield_rules.md`)

## Audit history

| Metric | ANKI-007 | v1.1 | v1.2 | v1.3 | v1.4 |
|---|---:|---:|---:|---:|---:|
| historical rows | 91 | 91 | 91 | 91 | **91** |
| approved Notes | 91 | 57 | 57 | 18 | **29** |
| deprecated rows | 0 | 34 | 34 | 73 | **62** |
| source-reviewed ALPs | 91 | 91 | 91 | 91 | **91** |
| active direct-recall ALPs | 91 | 91 | 91 | 36 | **61** |
| generated active cards | 91+ | 110 | 58 | 18 | **29** |
| active Cloze spans | n/a | n/a | n/a | 36 | **70** |

`BK-FND-00-0016` remains reserved pilot-only evidence and is unused in production.

## v1.4 objective

ANKI-AUDIT-004 corrects the over-aggressive v1.3 importance screen.

The new balance is:

1. **Moderately permissive selection:** restore useful foundational terminology, period reading, bookkeeping workflow, ledger structure, and representative account-selection rules.
2. **Integration-first compression:** keep card count down by combining facts that share one natural retrieval frame instead of retiring them merely to hit a low count.
3. **Lexical masking:** keep individual Cloze spans short and canonical.
4. **Visible context:** after all Cloze answers are hidden, the learner must still know what topic/decision the card is asking about.
5. **Direction shorthand:** when `借方 / 貸方` itself is the answer, hide only the first character.

## Restored / integrated active areas

Compared with v1.3, v1.4 restores or strengthens direct recall for:

- `簿記 / 帳簿 / 記帳`;
- `出資 / 借入 / 貸付`;
- `得意先 / 仕入先 / 掛け`;
- `仕訳 / 勘定 / 転記`;
- debit/credit balance direction;
- period notation;
- bookkeeping cycle;
- basic expense journal-entry selection;
- representative expense-account selection;
- main books plus `元丁 / 仕丁`;
- subsidiary-book types plus receivable/payable subledger organization.

Existing high-yield cards for trial balance, payroll, temporary accounts, corrections, vouchers, and source documents remain active.

The active deck therefore increases from **18 to 29 cards**, while active ALP recall increases from **36 to 61**. The increase is controlled by integration rather than one-card-per-ALP generation.

## Cloze shape examples

### Debit / credit

Use the visible suffix `方` and hide only the discriminating character:

`5要素の増加の定位置は、資産・費用が {{c1::借}}方、負債・純資産・収益が {{c1::貸}}方である。`

The same rule is used for `{{c1::借}}方残高` / `{{c1::貸}}方残高`.

### Trial-balance types

Keep `試算表` visible and hide the distinguishing prefix:

`試算表の種類では、借方・貸方の合計を集計するのは {{c1::合計}}試算表、残高を集計するのは {{c1::残高}}試算表、合計と残高を集計するのは {{c1::合計残高}}試算表である。`

### Vouchers

v1.3 had a context-loss problem because all voucher names could disappear simultaneously.

v1.4 uses:

`3伝票制では、現金が増える取引に {{c1::入金}}伝票、現金が減る取引に {{c1::出金}}伝票、現金が増減しない取引に {{c1::振替}}伝票を用いる。`

`3伝票制` and `伝票` remain visible even when the answers are hidden.

The same card also integrates the closely related field rule:

`入金・出金伝票の科目欄には現金の {{c1::相手科目}} を記入する。`

### Main books

One card integrates the two main books and their posting-reference fields:

`主要簿では、取引を発生順に記録する {{c1::仕訳帳}} と、勘定科目別に記録する {{c1::総勘定元帳}} を使う。転記の参照欄は、仕訳帳の {{c1::元丁}} が転記先、総勘定元帳の {{c1::仕丁}} が転記元を示す。`

### Subsidiary books

`補助簿では、取引を発生順に記録する {{c1::補助記入帳}} と、対象別に記録する {{c1::補助元帳}} を使う。売掛金元帳は {{c1::得意先}} 別、買掛金元帳は {{c1::仕入先}} 別に管理する。`

This is one coherent bookkeeping-organization card rather than four separate low-load cards.

## Mechanical checks

The v1.4 validator enforces:

- exactly 91 historical rows;
- exactly **29 approved / 62 deprecated** rows;
- all 91 included ALPs represented in production history;
- exactly **61 active direct-recall ALPs**;
- no ALP mapped to multiple active Notes;
- exactly **29 generated active cards**;
- exactly **70 active Cloze spans**;
- every approved FND-00 Note uses only `c1`;
- compound/list-like Cloze answer spans are rejected;
- duplicate exact Cloze answers within a Note are rejected;
- full-word `{{c1::借方}}` / `{{c1::貸方}}` direction Clozes are rejected;
- reviewed context-sensitive Notes must retain a visible topic cue after Cloze masking;
- source commit/path, stable IDs, canonical ALP order, lifecycle tags, and QA fields remain valid;
- exact rendered-text duplicates among approved Notes are rejected.

## Validation result

GitHub Actions branch validation passed:

```text
FND-00 v1.4 production validation: PASS
rows=91 approved=29 deprecated=62 source_reviewed_alps=91 active_recall_alps=61
generated_cards=29 cloze_spans=70 same_index_parallelism=pass lexical_atomicity=pass visible_context=pass debit_credit_first_character=pass reserved_pilot_only_id=BK-FND-00-0016
```

COM-01 and COM-02 validators also passed in the same workflow run.

## Reproducibility

- `scripts/migrate_fnd00_v1_2.py` records the v1.2 migration.
- `scripts/migrate_fnd00_v1_3.py` records the v1.3 minimal/lexical migration.
- `scripts/migrate_fnd00_v1_4.py` records the v1.4 balanced/context-preserving migration.
- `scripts/validate_fnd00_production.py` fixes the v1.4 metrics and masking rules.

## Downstream rule

For future generation/audits:

1. use a moderately permissive importance screen rather than aggressively minimizing active ALPs;
2. control card count primarily through coherent integration;
3. keep parallel lexical answers on the same card with the same Cloze index;
4. preserve an explicit visible topic/retrieval frame after masking;
5. use first-character Clozes for debit/credit direction;
6. track source-reviewed ALPs, active-recall ALPs, cards, and Cloze spans separately.