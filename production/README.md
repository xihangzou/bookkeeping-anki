# Production Notes

Canonical production Cloze-note batches live under `production/notes/` as UTF-8 TSV files following the v1.0 field order in `schema/note_schema.yaml`.

The source/schema/stable-ID baseline remains the frozen v1.0 contract. Active-deck selection is governed by the **v1.3 post-freeze exam-yield overlay** in `rules/exam_yield_rules.md`.

## Conventions

- one chapter/part batch per TSV file;
- rows are ordered by canonical ALP source order;
- exact source anchors are recovered through `ALP_IDs` and the canonical inventory;
- stable Note IDs are immutable; retired IDs remain in audit history and are never reused;
- chapter-local QA evidence is stored under `production/qa/`.

## Source coverage and active recall

v1.3 distinguishes two separate completeness metrics:

- **source-reviewed coverage**: every included ALP has been reviewed and remains traceable in production history;
- **active direct-recall coverage**: only ALPs worth spaced retrieval must remain on `Status=approved` Notes.

A deprecated historical row can therefore preserve source traceability without forcing a low-yield fact into the active deck. Do not create or retain an approved card solely to keep every ALP active-mapped.

## Cloze lexicality and same-card grouping — v1.3

Study cost is reduced primarily by retiring low-yield cards. For facts that remain worth recalling:

- prefer one lexical accounting term / account name / direction per Cloze span;
- split a compound answer into separate spans, e.g. `{{c1::A}}・{{c1::B}}`, rather than `{{c1::A・B}}`;
- parallel or conjunction-linked facts that form one coherent retrieval operation stay on the same card by reusing the same index;
- do not use `c2+` merely because a Note contains another blank or sentence;
- add another index only when a second retrieval operation is independently worth a separate review;
- track **generated-card count** (distinct Cloze indices) separately from **Cloze-span count** (atomic masked answer units).

## FND-00 audit result

FND-00 has three post-production audit stages:

- v1.1: 91 -> 57 approved Notes;
- v1.2: 110 -> 58 generated cards;
- v1.3: **18 approved Notes / 18 generated cards / 36 lexical Cloze spans**.

The 91 historical rows remain. All 91 included ALPs remain source-reviewed/traceable; **36 ALPs** remain active direct-recall targets. Every approved FND-00 Note uses only `c1`; parallel lexical answers are represented by multiple `{{c1::...}}` spans on that same card.

## Existing commercial batches

- COM-01 currently reflects v1.2 generation: 38 approved Notes / 38 cards / 52 included ALPs active-mapped.
- COM-02 currently reflects v1.2 generation: 17 approved Notes / 17 cards / 32 included ALPs active-mapped.

v1.3 is the current target for future generation. Existing v1.2 commercial batches should be migrated only through explicit chapter audits so stable IDs and prior QA evidence remain auditable.

## Lifecycle

### `Status=approved`

Approved rows constitute the active study deck. They use `QA=pass` and `status::approved`.

### `Status=deprecated`

Deprecated rows are retained as production history. They:

- keep immutable Note IDs and historical ALP mappings;
- use `QA=pass` after retirement is audited;
- use `status::deprecated`;
- are excluded from active export;
- never have their IDs reused.

## Current batches

- `notes/FND-00.tsv` — Part 0 / bookkeeping foundations (ANKI-007; audits #56, #58, #62)
- `notes/COM-01.tsv` — Commercial chapter 01 / 商品売買 (ANKI-008; v1.2 generation)
- `notes/COM-02.tsv` — Commercial chapter 02 / 収益認識 (ANKI-009; v1.2 generation)

Run `python scripts/validate_fnd00_production.py` to validate FND-00 historical source coverage, 18/73 lifecycle, 36 active-recall ALPs, **18 generated cards / 36 lexical spans**, same-index parallelism, lexical answer shape, and stable source/tag controls.

Run `python scripts/validate_com01_production.py` and `python scripts/validate_com02_production.py` for the existing v1.2 commercial batches.

Migration records:

- `scripts/migrate_fnd00_v1_2.py` — v1.2 rotation migration;
- `scripts/migrate_fnd00_v1_3.py` — v1.3 minimal/lexical migration.
