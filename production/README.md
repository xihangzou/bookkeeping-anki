# Production Notes

Canonical production Cloze-note batches live under `production/notes/` as UTF-8 TSV files following the v1.0 field order in `schema/note_schema.yaml`.

The source/schema/stable-ID baseline remains the frozen v1.0 contract. Active-deck selection is additionally governed by the explicit **v1.1 post-freeze exam-yield overlay** in `rules/exam_yield_rules.md`.

## Conventions

- one chapter/part batch per TSV file;
- rows are ordered by canonical ALP source order, even when stable Note IDs were assigned earlier during the representative pilot;
- exact source anchors are recovered through `ALP_IDs` and the canonical inventory rather than duplicated in Note rows;
- stable Note IDs are immutable; retired IDs remain in audit history and are never reused;
- an approved Note may map multiple ALPs when they form one coherent retrieval unit;
- every canonical included ALP must map to at least one **approved** Note;
- chapter-local QA evidence is stored under `production/qa/`.

## Lifecycle

### `Status=approved`

Approved rows constitute the **active study deck**. They must use `QA=pass` and the corresponding `status::approved` tag.

### `Status=deprecated`

Deprecated rows are retained only as auditable production history after consolidation or retirement. They:

- keep their immutable Note ID and historical ALP mapping;
- use `QA=pass` after the retirement decision is audited;
- use the corresponding `status::deprecated` tag;
- do **not** satisfy active ALP coverage by themselves;
- are excluded from downstream active-deck export;
- must never have their IDs reused.

## Current batches

- `notes/FND-00.tsv` — Part 0 / bookkeeping foundations (ANKI-007, audited by ANKI-AUDIT-001 #56)

Run `python scripts/validate_fnd00_production.py` to validate FND-00 source traceability, approved/deprecated lifecycle, stable IDs, tags, multi-ALP mappings, and 100% active approved ALP coverage.
