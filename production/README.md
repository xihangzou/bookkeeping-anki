# Production Notes

Canonical production Cloze-note batches live under `production/notes/` as UTF-8 TSV files following the v1.0 field order in `schema/note_schema.yaml`.

The source/schema/stable-ID baseline remains the frozen v1.0 contract. Active-deck selection and generated-card efficiency are additionally governed by the explicit **v1.2 post-freeze exam-yield overlay** in `rules/exam_yield_rules.md`.

## Conventions

- one chapter/part batch per TSV file;
- rows are ordered by canonical ALP source order, even when stable Note IDs were assigned earlier during the representative pilot;
- exact source anchors are recovered through `ALP_IDs` and the canonical inventory rather than duplicated in Note rows;
- stable Note IDs are immutable; retired IDs remain in audit history and are never reused;
- an approved Note may map multiple ALPs when they form one coherent retrieval unit;
- every canonical included ALP must map to at least one **approved** Note;
- chapter-local QA evidence is stored under `production/qa/`.

## Active-card efficiency

An approved Cloze Note can generate more than one Anki review card when it contains multiple distinct Cloze indices. Therefore production QA tracks both **approved Note count** and **generated-card count**.

- default to one generated card (`c1`) for one coherent Note;
- reuse the same Cloze index for tightly coupled comparison members, sequences, paired treatments, formulas, and vocabulary sets that should be recalled together;
- add `c2+` only for a materially independent retrieval operation worth a separate review;
- prefer canonical, standalone accounting terms or short self-contained propositions inside Clozes;
- keep supporting facts visible when hiding them would only create another low-value rotation.

For FND-00 v1.2, 57 approved Notes generate **58 cards**. `BK-FND-00-0091` is the sole approved multi-card Note because financial-statement abbreviations and trial-balance abbreviations are two coherent retrieval families.

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

- `notes/FND-00.tsv` — Part 0 / bookkeeping foundations (ANKI-007; audited by ANKI-AUDIT-001 #56 and ANKI-AUDIT-002 #58)

Run `python scripts/validate_fnd00_production.py` to validate FND-00 source traceability, lifecycle, stable IDs, tags, multi-ALP mappings, 100% active approved ALP coverage, generated-card count, reviewed Cloze-index shape, and Cloze-answer uniqueness checks.

`python scripts/migrate_fnd00_v1_2.py` is the idempotent migration record for the ANKI-AUDIT-002 wording/index changes.
