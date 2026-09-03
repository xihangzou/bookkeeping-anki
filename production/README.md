# Production Notes

Canonical production Cloze-note batches live under `production/notes/` as UTF-8 TSV files following the frozen v1.0 schema in `schema/note_schema.yaml`.

The source/schema/stable-ID baseline remains frozen. Active-deck and recall design are governed by the **v1.6 post-freeze overlay** in `rules/exam_yield_rules.md`.

## Conventions

- one chapter/part batch per TSV file;
- stable Note IDs are immutable; deprecated IDs are never reassigned;
- source anchors are recovered through canonical `ALP_IDs`;
- chapter QA lives under `production/qa/`;
- active card count is the number of distinct Cloze indices, while Cloze-span count tracks masked answer units.

## Integration-first, content-preserving design — v1.6

Card-count control should come primarily from coherent integration:

1. preserve useful examinable ALPs and the material source propositions they contain;
2. combine facts that belong to one retrieval frame;
3. use separate `{{c1::...}}` spans for parallel answers on the same card;
4. add another Note only when integration would make the retrieval task incoherent or overloaded.

An ALP mapping alone is not enough: material source content must remain recoverable from the active Note text. For FND-00, this yields **91/91 active ALPs in 32 cards** while restoring source details that v1.5 had compressed too aggressively.

## Cloze context, formula, and anti-leak rules

- Cloze spans should normally be lexical or short discriminating chunks;
- arithmetic/formula operators remain visible and each term is Clozed separately, e.g. `{{c1::収益}}－{{c1::費用}}`;
- parallel terms use the same `c1`, not extra generated cards;
- debit/credit direction uses `{{c1::借}}方` / `{{c1::貸}}方`;
- the visible text after masking must still identify the topic;
- a 2+ character Cloze answer must not appear verbatim elsewhere in the same card;
- do not use a topic label that reveals the answer;
- syntax-sensitive answers may include particles where needed, e.g. `{{c1::に終わる}}` / `{{c1::から始まる}}`.

## Completeness examples

When one inventory ALP represents a source family, integration must not silently truncate that family. FND-00 v1.6 therefore retains:

- all ten representative expense categories from the source;
- general-ledger `標準式` / `残高式` and material field mechanics;
- subsidiary-book mechanics and the explicit rule that subsidiary ledgers are posted from each voucher by `{{c1::個別転記}}`;
- temporary-account classifications and later reclassification;
- source-required formula terms, period vocabulary, correction logic, and document/voucher mechanics.

COM-01 applies the same rules to commercial bookkeeping, including acquisition-cost details, cost-flow method families, journal-entry mechanics, inventory valuation, and term-level formula recall. Its chapter-local precision audit also uses FND-00 as the style reference for short, unique answer spans and visible explanatory context.

## FND-00 audit result

Audit progression:

- v1.1: 91 -> 57 approved Notes;
- v1.2: 110 -> 58 generated cards;
- v1.3: 18 cards / 36 active ALPs;
- v1.4: 29 cards / 61 active ALPs;
- v1.5: 32 cards / 120 Cloze spans / 91 active ALPs;
- v1.6: **32 approved Notes / 32 cards / 150 Cloze spans / 91 active ALPs**.

FND-00 retains all 91 historical rows; 59 are deprecated history rows. `BK-FND-00-0016` remains reserved pilot-only evidence.

Run:

`python scripts/validate_fnd00_production.py`

Current expected output includes:

`rows=91 approved=32 deprecated=59 source_reviewed_alps=91 active_recall_alps=91`

and

`generated_cards=32 cloze_spans=150 ... visible_answer_leakage=0 ...`

## Existing commercial batches

- `notes/COM-01.tsv` — **38 approved Notes / 38 cards / 87 Cloze spans / 52 included ALPs; v1.7 chapter precision audit under v1.6 overlay**;
- `notes/COM-02.tsv` — 17 approved Notes / 17 cards / 32 included ALPs.

COM-01 follows the v1.6 recall-design overlay and has additionally been normalized to FND-00-style answer precision. COM-02 retains its audited generation state until an explicit chapter audit migrates it to the newer recall-design rules.

## Lifecycle

`Status=approved` rows constitute the active deck. `Status=deprecated` rows preserve immutable historical lineage and source traceability but are excluded from active export.

## Current batches

- `notes/FND-00.tsv` — foundations; current overlay v1.6 / ANKI-AUDIT-006 (#70);
- `notes/COM-01.tsv` — Commercial chapter 01; v1.7 chapter precision audit under current v1.6 overlay;
- `notes/COM-02.tsv` — Commercial chapter 02.

Migration records:

- `scripts/migrate_fnd00_v1_2.py`
- `scripts/migrate_fnd00_v1_3.py`
- `scripts/migrate_fnd00_v1_4.py`
- `scripts/migrate_fnd00_v1_5.py`
- `scripts/migrate_fnd00_v1_6.py`

Validation:

- `scripts/validate_fnd00_production.py`
- `scripts/validate_com01_production.py`
- `scripts/validate_com02_production.py`
