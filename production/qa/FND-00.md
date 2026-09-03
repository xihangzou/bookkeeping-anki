# FND-00 Production QA

Issues: ANKI-007 / #8; ANKI-AUDIT-001 / #56; ANKI-AUDIT-002 / #58; ANKI-AUDIT-003 / #62; ANKI-AUDIT-004 / #66; ANKI-AUDIT-005 / #68

Contracts:
- frozen v1.0 source/schema/stable-ID baseline;
- current v1.5 post-freeze integration / Cloze overlay: `rules/exam_yield_rules.md`.

## Audit history

| Metric | initial | v1.1 | v1.2 | v1.3 | v1.4 | v1.5 |
|---|---:|---:|---:|---:|---:|---:|
| historical rows | 91 | 91 | 91 | 91 | 91 | **91** |
| approved Notes | 91 | 57 | 57 | 18 | 29 | **32** |
| deprecated rows | 0 | 34 | 34 | 73 | 62 | **59** |
| source-reviewed ALPs | 91 | 91 | 91 | 91 | 91 | **91** |
| active direct-recall ALPs | 91 | 91 | 91 | 36 | 61 | **91** |
| generated cards | 91+ | 110 | 58 | 18 | 29 | **32** |
| active Cloze spans | n/a | n/a | n/a | 36 | 70 | **120** |

`BK-FND-00-0016` remains reserved pilot-only evidence and is unused in production.

## v1.5 objective

ANKI-AUDIT-005 maximizes useful source coverage without returning to one-card-per-ALP design.

- remaining inactive ALPs were re-audited individually;
- coherent facts were folded into existing retrieval frames;
- only three coherent historical Notes were reactivated: `BK-FND-00-0048` (立替金・預り金), `BK-FND-00-0084` (伝票からの転記), and `BK-FND-00-0091` (略語・記号);
- active coverage therefore rises **61/91 -> 91/91 ALPs** while card count rises only **29 -> 32**;
- all approved Notes still use only `c1`.

## User-directed corrections

### BK-FND-00-0018

Removed `簿記の基本では、` because it directly exposed the later `{{c1::簿記}}` answer. The card now begins with a neutral definition cue:

`会社の取引を記録する媒体を {{c1::帳簿}}、そこへ書き込むことを {{c1::記帳}} ...`

### BK-FND-00-0027

Period notation now preserves the particles inside the answer:

`「X年Y月期」はY月{{c1::に終わる}}1年間、「X年度」はX年{{c1::から始まる}}1年間`

## Visible-answer leakage audit

The v1.4 deck had 11 approved Notes where a 2+ character Cloze answer was repeated visibly elsewhere on the same card. v1.5 rewrites those prompts and the validator now rejects this pattern.

Result: **0 visible exact-answer leaks** for 2+ character answers.

This includes corrections to cards involving `簿記`, `仕訳/勘定`, `収益`, `取引`, trial-balance prefixes, expense entries, temporary accounts, main books, vouchers, and document copies.

## Integration examples

- financial-statement purpose is integrated into the basic bookkeeping-definition card;
- B/S and P/L placement is visible supporting context on the five-element debit/credit card;
- compound-entry/posting/`諸口` facts are integrated with `仕訳 / 勘定 / 転記`;
- accounting-period terminology is integrated with the bookkeeping cycle;
- subsidiary-book families are consolidated on one card;
- sales/purchase book returns and net-sales/net-purchases formulas are integrated with subsidiary-ledger reconciliation;
- partial-cash voucher treatment is integrated with the 3-voucher card;
- voucher-to-ledger posting has one dedicated integrated card;
- voucher inference cues are integrated into the document-reasoning card;
- all accounting abbreviations and `△ / @` notation share one notation card.

## Mechanical checks

`scripts/validate_fnd00_production.py` enforces:

- 91 historical rows and immutable stable-ID set;
- 32 approved / 59 deprecated rows;
- 91/91 source-reviewed and 91/91 active ALPs;
- every active ALP maps exactly once;
- 32 generated cards and 120 Cloze spans;
- approved Notes use `c1` only;
- lexical / short-discriminator Cloze shape;
- same-index parallelism;
- visible retrieval context;
- zero exact visible-answer leakage for answers of 2+ characters;
- `{{c1::借}}方 / {{c1::貸}}方` formatting;
- the exact 0018 and 0027 user corrections;
- source commit/path, canonical ALP order, Section alignment, tags, QA, and reserved `BK-FND-00-0016` controls.

## Validation result

```text
FND-00 v1.5 production validation: PASS
rows=91 approved=32 deprecated=59 source_reviewed_alps=91 active_recall_alps=91
generated_cards=32 cloze_spans=120 same_index_parallelism=pass lexical_atomicity=pass visible_context=pass visible_answer_leakage=0 debit_credit_first_character=pass reserved_pilot_only_id=BK-FND-00-0016
```

COM-01 and COM-02 validators pass in the same production workflow.

## Reproducibility

- `scripts/migrate_fnd00_v1_2.py` — v1.2 rotation migration;
- `scripts/migrate_fnd00_v1_3.py` — v1.3 minimal/lexical migration;
- `scripts/migrate_fnd00_v1_4.py` — v1.4 balanced/context migration;
- `scripts/migrate_fnd00_v1_5.py` — v1.5 maximal-integration / anti-leak migration;
- `scripts/validate_fnd00_production.py` — current v1.5 gate.

## Downstream rule

For subsequent chapters, prefer **coverage-preserving integration** over either extreme: do not create one card per ALP, and do not discard useful examinable material merely to minimize the card count. Keep answer spans atomic, the retrieval frame visible, and the answer itself absent from visible context.