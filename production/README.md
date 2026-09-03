# Production Notes

Canonical production Cloze-note batches live under `production/notes/` as UTF-8 TSV files following the frozen v1.0 schema in `schema/note_schema.yaml`.

The source/schema/stable-ID baseline remains frozen. Active-deck and recall design are governed by the **v1.5 post-freeze overlay** in `rules/exam_yield_rules.md`.

## Conventions

- one chapter/part batch per TSV file;
- stable Note IDs are immutable; deprecated IDs are never reassigned;
- source anchors are recovered through canonical `ALP_IDs`;
- chapter QA lives under `production/qa/`;
- active card count is the number of distinct Cloze indices, while Cloze-span count tracks masked answer units.

## Integration-first design — v1.5

Card-count control should come primarily from coherent integration:

1. preserve useful examinable ALPs;
2. combine facts that belong to one retrieval frame;
3. use separate `{{c1::...}}` spans for parallel answers on the same card;
4. add another Note only when integration would make the retrieval task incoherent or overloaded.

For FND-00, this produces **91/91 active ALPs in 32 cards**, rather than either 91 separate cards or an aggressively filtered deck.

## Cloze context and anti-leak rules

- Cloze spans should normally be lexical or short discriminating chunks;
- debit/credit direction uses `{{c1::借}}方` / `{{c1::貸}}方`;
- the visible text after masking must still identify the topic;
- a 2+ character Cloze answer must not appear verbatim elsewhere in the same card;
- do not use a topic label that reveals the answer, e.g. avoid `簿記の基本では、` on a card testing `{{c1::簿記}}`;
- syntax-sensitive answers may include particles where needed, e.g. `{{c1::に終わる}}` / `{{c1::から始まる}}`.

## FND-00 audit result

Audit progression:

- v1.1: 91 -> 57 approved Notes;
- v1.2: 110 -> 58 generated cards;
- v1.3: 18 cards / 36 active ALPs;
- v1.4: 29 cards / 61 active ALPs;
- v1.5: **32 approved Notes / 32 cards / 120 Cloze spans / 91 active ALPs**.

FND-00 retains all 91 historical rows; 59 are deprecated history rows. `BK-FND-00-0016` remains reserved pilot-only evidence.

Run:

`python scripts/validate_fnd00_production.py`

Current expected output includes:

`rows=91 approved=32 deprecated=59 source_reviewed_alps=91 active_recall_alps=91`

and

`generated_cards=32 cloze_spans=120 ... visible_answer_leakage=0 ...`

## Existing commercial batches

- `notes/COM-01.tsv` — 38 approved Notes / 38 cards / 52 included ALPs;
- `notes/COM-02.tsv` — 17 approved Notes / 17 cards / 32 included ALPs.

Existing commercial batches retain their audited generation state until an explicit chapter audit migrates them to newer recall-design rules.

## Lifecycle

`Status=approved` rows constitute the active deck. `Status=deprecated` rows preserve immutable historical lineage and source traceability but are excluded from active export.

## Current batches

- `notes/FND-00.tsv` — foundations; current overlay v1.5 / ANKI-AUDIT-005 (#68);
- `notes/COM-01.tsv` — Commercial chapter 01;
- `notes/COM-02.tsv` — Commercial chapter 02.

Migration records:

- `scripts/migrate_fnd00_v1_2.py`
- `scripts/migrate_fnd00_v1_3.py`
- `scripts/migrate_fnd00_v1_4.py`
- `scripts/migrate_fnd00_v1_5.py`

Validation:

- `scripts/validate_fnd00_production.py`
- `scripts/validate_com01_production.py`
- `scripts/validate_com02_production.py`