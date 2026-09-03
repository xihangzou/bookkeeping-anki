# FND-00 Production QA

Issues: ANKI-007 / #8; ANKI-AUDIT-001 / #56; ANKI-AUDIT-002 / #58; ANKI-AUDIT-003 / #62

Contracts:
- frozen v1.0 source/schema baseline (`FREEZE.md`, `rules/cloze_rules.md`, `rules/coverage_rules.md`, `schema/note_schema.yaml`)
- current v1.3 post-freeze active-deck / Cloze overlay (`rules/exam_yield_rules.md`)

## Audit history

| Metric | ANKI-007 | v1.1 | v1.2 | v1.3 |
|---|---:|---:|---:|---:|
| historical rows | 91 | 91 | 91 | **91** |
| approved Notes | 91 | 57 | 57 | **18** |
| deprecated rows | 0 | 34 | 34 | **73** |
| source-reviewed ALPs | 91 | 91 | 91 | **91** |
| active direct-recall ALPs | 91 | 91 | 91 | **36** |
| generated active cards | 91+ | 110 | 58 | **18** |
| active Cloze spans | n/a | n/a | n/a | **36** |

`BK-FND-00-0016` remains reserved pilot-only evidence and is unused in production.

## v1.3 objective

ANKI-AUDIT-003 reduces review volume without making individual Cloze answers broader.

Two separate decisions are enforced:

1. **Selection:** low-yield facts are retired from active spaced recall while remaining auditable in production history.
2. **Masking:** retained facts use short lexical Cloze spans. Parallel lexical answers that belong to one coherent retrieval operation remain on the same Anki card by sharing `c1`.

Therefore the preferred form is:

`{{c1::A}}・{{c1::B}}`

rather than either:

- `{{c1::A・B}}` (compound answer span), or
- `{{c1::A}}・{{c2::B}}` (unnecessary extra review card).

## Active selection

The v1.3 active deck contains 18 Notes covering 36 direct-recall ALPs. The retained areas are those most likely to change an accounting answer or support later study:

- own-company perspective;
- five-element classification;
- debit/credit direction;
- debit-credit equality;
- bookkeeping-transaction recognition;
- trial-balance definition/types/limitations;
- payroll withholding and social-insurance treatment;
- temporary accounts;
- correction entries;
- subsidiary-ledger reconciliation;
- three-voucher selection;
- source-document classification and interpretation.

Other included ALPs remain source-reviewed and traceable through historical rows, but no longer create active review cards merely to satisfy an active-mapping quota.

## Lexical Cloze examples

### Five elements

One card contains five separate lexical spans:

`財産や権利は {{c1::資産}}。返済義務は {{c1::負債}}。返済義務のない調達源泉は {{c1::純資産}}。会社の儲けの原因は {{c1::収益}}。収益を得るための消費は {{c1::費用}}。`

This generates one card, not five, while each hidden answer remains a canonical accounting term.

### Debit / credit

`資産・費用の増加は {{c1::借方}}。負債・純資産・収益の増加は {{c1::貸方}}。`

The comparison is one coherent retrieval operation, so both lexical spans use `c1`.

### Trial-balance types

`借方・貸方の合計を集計するのは {{c1::合計試算表}}。残高を集計するのは {{c1::残高試算表}}。合計と残高を集計するのは {{c1::合計残高試算表}}。`

### Payroll

`給与は手取額ではなく {{c1::総額}} を費用計上する。控除した所得税は {{c1::所得税預り金}} で処理する。`

### Vouchers

`現金が増える取引は {{c1::入金伝票}}。現金が減る取引は {{c1::出金伝票}}。現金が増減しない取引は {{c1::振替伝票}}。`

### Source documents

`納品明細は {{c1::納品書}}。請求金額の明細は {{c1::請求書}}。支払の証明は {{c1::領収書}}。当座預金の入出金明細は {{c1::当座勘定照合表}}。`

## Mechanical checks

The v1.3 validator enforces:

- exactly 91 historical rows;
- exactly 18 approved / 73 deprecated rows;
- exactly 91 source-reviewed included ALPs represented in production history;
- exactly 36 ALPs represented by active approved Notes;
- exactly 18 generated active cards;
- exactly 36 active Cloze spans;
- every approved FND-00 Note uses only `c1`;
- compound/list-like answer spans containing `・`, punctuation, formula/list separators, etc. are rejected;
- duplicate exact answer spans within a Note are rejected;
- source commit/path, stable IDs, canonical ALP ordering, lifecycle tags, and QA fields remain valid;
- exact rendered-text duplicates among approved Notes are rejected.

## Validation result

GitHub Actions passed after the user's same-card correction:

```text
FND-00 v1.3 production validation: PASS
rows=91 approved=18 deprecated=73 source_reviewed_alps=91 active_recall_alps=36
generated_cards=18 cloze_spans=36 same_index_parallelism=pass lexical_atomicity=pass reserved_pilot_only_id=BK-FND-00-0016
```

COM-01 and COM-02 validators also passed in the same workflow run, confirming that this FND-00 audit did not break the existing commercial batches.

## Reproducibility

- `scripts/migrate_fnd00_v1_2.py` records the v1.2 migration.
- `scripts/migrate_fnd00_v1_3.py` records the v1.3 active-selection and lexical same-card migration.
- `scripts/validate_fnd00_production.py` fixes the final FND-00 v1.3 metrics and masking shape.

## Downstream rule

For ANKI-008 onward generation/audits:

1. retain only retrieval operations that justify spaced repetition;
2. prefer lexical Cloze spans over phrase/clause answers;
3. when parallel/conjunction facts belong to the same coherent retrieval operation, split their spans but reuse the same index (`c1`);
4. use `c2+` only for a genuinely independent retrieval operation worth another review card;
5. track source-reviewed coverage, active-recall ALPs, generated cards, and Cloze spans separately.
