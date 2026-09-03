# FND-00 Production QA

Issues: ANKI-007 / #8; ANKI-AUDIT-001 / #56; ANKI-AUDIT-002 / #58; ANKI-AUDIT-003 / #62; ANKI-AUDIT-004 / #66; ANKI-AUDIT-005 / #68; ANKI-AUDIT-006 / #70

Contracts:
- frozen v1.0 source/schema/stable-ID baseline;
- current v1.6 post-freeze integration / completeness / Cloze overlay: `rules/exam_yield_rules.md`.

## Audit history

| Metric | initial | v1.1 | v1.2 | v1.3 | v1.4 | v1.5 | v1.6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| historical rows | 91 | 91 | 91 | 91 | 91 | 91 | **91** |
| approved Notes | 91 | 57 | 57 | 18 | 29 | 32 | **32** |
| deprecated rows | 0 | 34 | 34 | 73 | 62 | 59 | **59** |
| source-reviewed ALPs | 91 | 91 | 91 | 91 | 91 | 91 | **91** |
| active direct-recall ALPs | 91 | 91 | 91 | 36 | 61 | 91 | **91** |
| generated cards | 91+ | 110 | 58 | 18 | 29 | 32 | **32** |
| active Cloze spans | n/a | n/a | n/a | 36 | 70 | 120 | **150** |

`BK-FND-00-0016` remains reserved pilot-only evidence and is unused in production.

## v1.6 objective

ANKI-AUDIT-006 keeps the v1.5 **32-card integration architecture** but corrects a new failure mode: an ALP could be mapped to an approved Note while material source detail had been compressed out of the Note text.

The v1.6 audit therefore checks **content preservation inside integrated cards**, not only ALP mapping coverage.

Key outcomes:

- card count remains **32**;
- active ALP coverage remains **91/91**;
- Cloze spans rise **120 -> 150** because omitted examinable content is restored inside existing cards;
- formula operators remain visible while each term is Clozed separately;
- source families that are one included ALP are retained as complete families rather than truncated examples;
- visible-answer leakage remains **0**.

## User-directed corrections

### Formula itemization

Whole-expression Clozes were replaced by term-level Clozes.

Preferred production shape:

`当期純利益＝{{c1::収益}}－{{c1::費用}}`

`純売上高＝{{c1::総売上高}}－{{c1::売上戻り高}}`

`純仕入高＝{{c1::総仕入高}}－{{c1::仕入戻り高}}`

The validator rejects arithmetic operators inside an approved Cloze answer.

### BK-FND-00-0084

The subsidiary-ledger exception is now explicit:

`補助元帳は相手先別明細を保つため、各伝票から{{c1::個別転記}}する。`

### Expense-account completeness

`BK-FND-00-0047` now restores all ten representative source categories:

- 給料
- 水道光熱費
- 旅費交通費
- 広告宣伝費
- 消耗品費
- 通信費
- 保険料
- 保管費
- 諸会費
- 雑費

The source explicitly includes all ten in one classification ALP, so retaining only three examples was undercoverage. The source table confirms these categories. 

### Main-book / general-ledger completeness

`BK-FND-00-0062` now restores:

- the full `取引 → 仕訳帳 → 総勘定元帳 → 試算表・財務諸表` flow;
- journal-book field roles including `元丁`;
- general-ledger `標準式` and `残高式`;
- `仕丁`, debit/credit amount fields, and the additional balance information in the balance-format ledger.

The pinned source terminology is **標準式 / 残高式**.

## Other mapped-but-underrepresented ALPs restored

The full 91-ALP audit also restored or strengthened:

- residual = debit-total / credit-total **difference**;
- the relationship between `勘定科目` and the five elements;
- left side = debit / right side = credit;
- double-entry dual recording plus total debit/credit equality;
- accounting-period purpose and `前期 / 翌期`;
- trial-balance whole-ledger overview purpose;
- the general expense debit-recognition rule;
- `従業員預り金` and the asset/liability basis of temporary employee amounts;
- employee income-tax burden, withholding, and remittance mechanics;
- compound payroll treatment;
- `仮払金 = 資産`, `仮受金 = 負債` plus later reclassification;
- the correction-entry relationship and exception;
- subsidiary-book purpose and detailed mechanics for cash, current account, petty cash, bills, receivable/payable ledgers, and human-name accounts;
- voucher definition / `起票`;
- source-document definition, settlement-method limitation, and advance-receipt treatment.

## Visible-answer leakage audit

v1.6 preserves the v1.5 rule: a 2+ character Cloze answer must not remain visible elsewhere on the same card.

During the v1.6 rewrite, validator feedback caught five context collisions before finalization. They were corrected by paraphrasing visible context rather than weakening the anti-leak rule.

Result: **0 visible exact-answer leaks** for 2+ character answers.

## Mechanical checks

`scripts/validate_fnd00_production.py` enforces:

- 91 historical rows and immutable stable-ID set;
- 32 approved / 59 deprecated rows;
- 91/91 source-reviewed and 91/91 active ALPs;
- every active ALP maps exactly once;
- 32 generated cards and 150 Cloze spans;
- approved Notes use `c1` only;
- lexical / short-discriminator Cloze shape;
- same-index parallelism;
- arithmetic/formula operators are not hidden inside one Cloze span;
- required term-level formula forms;
- all ten source expense-account categories;
- `標準式` / `残高式` and material general-ledger fields;
- explicit `{{c1::個別転記}}` for subsidiary ledgers;
- visible retrieval context;
- zero exact visible-answer leakage for answers of 2+ characters;
- `{{c1::借}}方 / {{c1::貸}}方` formatting;
- the 0018 and 0027 user corrections from v1.5;
- source commit/path, canonical ALP order, Section alignment, tags, QA, and reserved `BK-FND-00-0016` controls.

## Validation result

```text
FND-00 v1.6 production validation: PASS
rows=91 approved=32 deprecated=59 source_reviewed_alps=91 active_recall_alps=91
generated_cards=32 cloze_spans=150 same_index_parallelism=pass lexical_atomicity=pass visible_context=pass visible_answer_leakage=0 debit_credit_first_character=pass reserved_pilot_only_id=BK-FND-00-0016
```

COM-01 and COM-02 remain covered by the same production workflow and must pass before merge.

## Reproducibility

- `scripts/migrate_fnd00_v1_2.py` — v1.2 rotation migration;
- `scripts/migrate_fnd00_v1_3.py` — v1.3 minimal/lexical migration;
- `scripts/migrate_fnd00_v1_4.py` — v1.4 balanced/context migration;
- `scripts/migrate_fnd00_v1_5.py` — v1.5 maximal-integration / anti-leak migration;
- `scripts/migrate_fnd00_v1_6.py` — v1.6 completeness / formula-itemization migration;
- `scripts/validate_fnd00_production.py` — current v1.6 gate.

## Downstream rule

For subsequent chapters, use **coverage-preserving, content-preserving integration**. Mapping an ALP to a Note is not sufficient if the material proposition is absent from the Note text. Keep formulas term-wise, preserve complete included source families, keep the retrieval frame visible, and add cards only when coherent integration is no longer possible.