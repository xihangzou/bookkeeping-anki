# Production Notes

Canonical production Cloze-note batches live under `production/notes/` as UTF-8 TSV files following the frozen v1.0 field order in `schema/note_schema.yaml`.

## Conventions

- one chapter/part batch per TSV file;
- rows are ordered by canonical ALP source order, even when stable Note IDs were assigned earlier during the representative pilot;
- production-approved Notes use `Status=approved`, `QA=pass`, and the corresponding required tags;
- exact source anchors are recovered through `ALP_IDs` and the canonical inventory rather than duplicated in Note rows;
- stable Note IDs assigned during the pilot are preserved when promoted; retired pilot-only IDs remain reserved and are never reused;
- chapter-local QA evidence is stored under `production/qa/`.

## Current batches

- `notes/FND-00.tsv` — Part 0 / bookkeeping foundations (ANKI-007)

Run `python scripts/validate_fnd00_production.py` to validate the ANKI-007 batch against the canonical FND-00 inventory and frozen schema invariants.
