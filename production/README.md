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

A deprecated historical row can therefore preserve source traceability without forcing a low-yield fact into the active deck.

Do not create or retain an approved card solely to keep every ALP active-mapped.

## Cloze atomicity — v1.3

Study cost is reduced by retiring low-yield cards, not by hiding several answers on one card.

For newly generated or v1.3-audited material:

- prefer one lexical accounting term / account name / direction per Cloze;
- one generated card should contain one Cloze occurrence;
- do not repeat the same `cN` across parallel blanks;
- split parallel classifications and conjunction-linked judgments into separate sentences/cards when both deserve recall;
- one Japanese full-stop-delimited sentence should contain at most one Cloze;
- use a short phrase only when no canonical lexical target preserves the intended retrieval operation.

## FND-00 audit result

FND-00 has three post-production audit stages:

- v1.1: 91 -> 57 approved Notes;
- v1.2: 110 -> 58 generated cards through same-index grouping;
- v1.3: **18 approved Notes / 37 generated cards**, with lexical Clozes and parallel/conjunction splitting.

The 91 historical rows remain. All 91 included ALPs remain source-reviewed/traceable; **36 ALPs** remain active direct-recall targets.

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

Run `python scripts/validate_fnd00_production.py` to validate FND-00 historical source coverage, 18/73 lifecycle, 36 active-recall ALPs, 37 generated cards, lexical Cloze shape, one-Cloze-per-card, and sentence splitting.

Run `python scripts/validate_com01_production.py` and `python scripts/validate_com02_production.py` for the existing v1.2 commercial batches.

Migration records:

- `scripts/migrate_fnd00_v1_2.py` — v1.2 rotation migration;
- `scripts/migrate_fnd00_v1_3.py` — v1.3 minimal/atomic migration.
