# ANKI-043 — Deterministic Anki export validation

Status: **PASS / complete**

## Scope

Build the final deterministic Anki import/export artifacts from the fully normalized, QA-passed, 100%-coverage-validated production Note corpus. Export artifacts remain downstream build products; `production/notes/*.tsv` remains the editable canonical source of truth.

## Authoritative baseline

- source repository: `xihangzou/bookkeeping-integrated`
- source path: `merged/textbook.md`
- pinned source commit: `569ed7b82e729334e1472286eaca7c4352e6fbdb`
- ANKI-043 validated repository revision: `59a300ffb38e34acfdb70db7236631dd079f87de`
- schema: `schema/note_schema.yaml`
  - Git blob: `78ffbe9a1497907281b714b9b7a443705d9580a3`
  - SHA-256: `a5817abf66e33a37abdb6b9981aab6eb4a1833aee5cc4f8db22aefa0bd1aed8c`
- consolidated rules: `rules/anki_card_rules.md`
  - Git blob: `0a150f025e246c1580e50e72ec3e37301ea6a323`
  - SHA-256: `0d9fece4586b900aa775df63525d83668c9fee962f1cd37997f6f59cd1b9c9c9`
- final coverage report: `production/qa/ANKI-042.md`
  - Git blob: `3913459a104d963b4abdaed7b1875fdab486bdf3`
  - SHA-256: `5339a17938ddf03c5d48d5578623a155af89d1b4081447e7123975e6ea0d063c`
- canonical production Note corpus SHA-256: `0cb1148cc20b2017feb73209ff770a9ba1bcbbad14258125dd78c12c831be3a5`

Historical `FREEZE.md` / v1.0 remains lineage evidence only.

## Final corpus / export counts

| Metric | Result |
|---|---:|
| production rows | 811 |
| approved Notes exported | 735 |
| deprecated lineage Notes excluded | 76 |
| generated Cloze cards | 748 |
| Cloze spans | 2,008 |
| included ALPs mapped by exported Notes | 965 / 965 |
| duplicate stable Note IDs | 0 |
| Anki GUID collisions | 0 |

All and only `Status=approved`, `QA=pass` Notes are exported. No export step writes to or silently mutates the canonical production Note shards.

## Deliverables

The build produces the following under the selected output directory (CI: `export/build-a/`):

- `bookkeeping-master.canonical.tsv`
  - 16 canonical schema fields
  - UTF-8, LF row delimiters
  - schema-defined escaping for backslash, tab, CR, and LF
  - canonical source ordering
  - SHA-256: `557ac69951b8962378415096dd5d9f840ec6b51a93960015c3534e4042a32a7d`
- `bookkeeping-master.apkg`
  - deck: `Bookkeeping Master`
  - note type: `Bookkeeping Master Cloze`
  - all 16 canonical fields retained in the Anki note model
  - deterministic GUID derived from stable Note ID via `genanki.guid_for(ID)`
  - semantic export SHA-256: `8db5b10b82bd5814920f8f68b0e0605301209321b3267da33169591e47d79dd6`
- `manifest.json`
  - source baseline
  - repository/build revision
  - production corpus identity
  - schema/rule/coverage identities
  - toolchain identity
  - Note/card/span/ALP counts
  - canonical TSV hash and APKG semantic hash
  - round-trip validation result

Build implementation and documentation:

- builder: `scripts/build_anki_export.py`
- Unicode/control-character fixture: `scripts/validate_export_serialization.py`
- pinned tooling: `requirements-export.txt`
- instructions: `export/README.md`
- workflow: `.github/workflows/build-export.yml`

## Tooling assumptions

CI validated with:

- Python `3.12.14`
- `genanki==0.13.1`

The APKG is generated through genanki's standard Anki package writer. The workflow validates the package ZIP and reads the generated Anki SQLite collection back; it does not automate the Anki Desktop GUI. `export/README.md` documents desktop import/review via `File -> Import`.

## Round-trip / import validation

The builder opens the generated APKG, locates its Anki collection database, and validates every exported Note against the expected canonical corpus:

- exported Notes: 735 / 735
- generated cards: 748 / 748
- all 16 fields survive serialization/import representation
- `ID`, `ALP_IDs`, `Text`, `Extra`, source metadata, lifecycle fields, and other schema fields round-trip exactly
- tags survive and match canonical tag sets
- Cloze card ordinals match the distinct `cN` groups for every Note
- stable Note IDs are unique
- Anki GUIDs are unique; collisions = 0
- Japanese Unicode survives UTF-8 + APKG round-trip
- round-trip result: **PASS**

The current production corpus happens to contain zero fields with serialized physical line breaks. Therefore `scripts/validate_export_serialization.py` separately exercises Japanese text plus LF, CR, TAB, and backslash through the schema escape encoder/decoder. Result: **PASS**.

## Determinism validation

GitHub Actions performs two independent builds from the same checkout:

1. `export/build-a`
2. `export/build-b`

It requires:

- byte-identical canonical TSV (`cmp`)
- byte-identical `manifest.json` (`cmp`)
- both APKGs independently pass full SQLite round-trip validation
- both APKGs produce the same semantic fingerprint

Final semantic fingerprint from both builds:

`8db5b10b82bd5814920f8f68b0e0605301209321b3267da33169591e47d79dd6`

The APKG ZIP binary itself is not used as the determinism identity because archive/database packaging metadata may vary; deterministic semantic contents are validated instead.

## CI evidence

Final workflow: **Build Anki export**

- run ID: `33945371171`
- head revision: `59a300ffb38e34acfdb70db7236631dd079f87de`
- result: **SUCCESS**
- uploaded artifact ID: `9963148353`
- uploaded artifact ZIP SHA-256: `3e173741dca8bdaa70f3bd4cc2a27a2f41d7b2bc84f62a16000e7520658c2455`

The same run re-executed the global ANKI-038–042 gates before export. ANKI-042 again reported `semantic_coverage_pct=100.00`, with no unmapped ALPs, orphan Notes, unexplained exclusions, source gaps, or exact duplicate active propositions.

## Build command

```bash
python -m pip install -r requirements-export.txt
python scripts/validate_corpus_production.py
python scripts/validate_journal_production.py
python scripts/validate_formula_production.py
python scripts/validate_recall_production.py
python scripts/validate_coverage_production.py
python scripts/validate_export_serialization.py
python scripts/build_anki_export.py --output-dir export/build
```

## Acceptance criteria

- [x] ANKI-042 PASS with semantic coverage = 100%
- [x] all and only approved final Notes are exported
- [x] exported Note/card count matches the final validated corpus exactly
- [x] Cloze syntax maps to the expected Anki Cloze cards
- [x] fields, tags, stable Note IDs, and ALP linkage survive deterministic export/import representation validation
- [x] no duplicate stable Note IDs or Anki GUID collisions
- [x] Unicode/Japanese and line-break/control-character serialization survive validation
- [x] deterministic rebuild from the same canonical source produces equivalent canonical output and manifest, with identical APKG semantic identity
- [x] manifest identifies source baseline, schema, consolidated rules, corpus, and build identity
- [x] resulting standard genanki APKG is Anki-compatible and desktop import/review instructions are documented
- [x] export does not mutate canonical source data

## Conclusion

**PASS. ANKI-043 is complete.** Phase G is complete and the master-deck project Definition of Done is satisfied at this validated repository revision.
