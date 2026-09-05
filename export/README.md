# Deterministic Anki export

`production/notes/*.tsv` is the canonical editable corpus. Files generated under `export/build/` are downstream build products only and must not be edited back into production Notes.

## Build

From the repository root:

```bash
python -m pip install -r requirements-export.txt
python scripts/validate_corpus_production.py
python scripts/validate_journal_production.py
python scripts/validate_formula_production.py
python scripts/validate_recall_production.py
python scripts/validate_coverage_production.py
python scripts/build_anki_export.py --output-dir export/build
```

The build is pinned to `genanki==0.13.1` and produces:

- `bookkeeping-master.canonical.tsv` — all and only approved Notes, 16 canonical schema fields, UTF-8/LF, schema-defined escaping, canonical source order;
- `bookkeeping-master.apkg` — Anki-compatible Cloze package using a custom 16-field model so stable Note ID, ALP linkage, source fields, lifecycle fields, and tags are preserved;
- `manifest.json` — source baseline, repository/build identity, schema/rule/coverage fingerprints, corpus counts, artifact fingerprints, and round-trip validation result.

The GitHub Actions workflow `.github/workflows/build-export.yml` runs all global prerequisite validators, builds the export twice, requires byte-identical canonical TSV and manifest output, validates both APKG packages by SQLite round-trip, and uploads the first build as a workflow artifact.

## Anki import

Import `bookkeeping-master.apkg` with Anki Desktop (`File -> Import`). The package contains the `Bookkeeping Master` deck and `Bookkeeping Master Cloze` note type. The note type retains every canonical field; the rendered front uses `Text`, and the answer additionally shows `Extra`.

The APKG binary itself is not used as a source of truth. Rebuild it from the repository corpus whenever the approved corpus, schema, or consolidated rules change.
