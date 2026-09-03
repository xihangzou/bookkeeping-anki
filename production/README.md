# Production Notes

Canonical production Cloze-note batches live under `production/notes/` as UTF-8 TSV files following the **current** schema in `schema/note_schema.yaml`.

Repository-wide governance is defined in `GOVERNANCE.md`. Current authoring, coverage, active-deck, and recall design are governed by the latest merged `SPEC.md` and `rules/*.md`; v1.0 is a historical baseline rather than permanent authority.

## Conventions

- one chapter/part batch per TSV file;
- stable Note IDs are immutable; deprecated IDs are never reassigned to unrelated content;
- source anchors are recovered through canonical `ALP_IDs`;
- existing batches retain their pinned source provenance until an explicit source-baseline migration;
- chapter QA lives under `production/qa/`;
- active card count is the number of distinct Cloze indices, while Cloze-span count tracks masked answer units.

## Living-rule application

The latest merged rules are authoritative for new generation. Existing batches have an explicit audited state and are migrated deliberately when a newer rule is applied to them.

This means:

1. rule improvements are written into the current authoritative files;
2. validators are updated when the rule is mechanically enforceable;
3. affected chapter batches are migrated explicitly rather than silently rewritten;
4. historical audit metrics remain historical evidence;
5. stable-ID/source-lineage invariants remain intact.

`FREEZE.md` is the historical v1.0 pilot-baseline record only.

## Integration-first, content-preserving design

Card-count control should come primarily from coherent integration:

1. preserve useful examinable ALPs and the material source propositions they contain;
2. combine facts that belong to one retrieval frame;
3. use separate `{{c1::...}}` spans for parallel answers on the same card;
4. add another Note only when integration would make the retrieval task incoherent or overloaded.

An ALP mapping alone is not enough: material source content must remain recoverable from the active Note text.

## Current Cloze / completeness rules

Current rules include:

- Cloze spans should normally be lexical or short discriminating chunks;
- arithmetic/formula operators remain visible and each term is Clozed separately, e.g. `{{c1::収益}}－{{c1::費用}}`;
- parallel terms belonging to one retrieval operation use the same `c1`;
- debit/credit direction uses `{{c1::借}}方` / `{{c1::貸}}方`;
- the visible text after masking must still identify the topic;
- a 2+ character Cloze answer must not appear verbatim elsewhere in the same card;
- source families represented by included ALPs must not be silently truncated during integration.

COM-01 additionally applies the FND-00 style reference for short, unique answer spans and visible explanatory context.

See `rules/cloze_rules.md`, `rules/coverage_rules.md`, and `rules/exam_yield_rules.md` for the authoritative current wording.

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

- `notes/COM-01.tsv` — **38 approved Notes / 38 cards / 87 Cloze spans / 52 included ALPs; v1.7 chapter-local precision audit applied**;
- `notes/COM-02.tsv` — 17 approved Notes / 17 cards / 32 included ALPs; retains its current audited state until an explicit migration applies newer rules.

A newer repository rule does not erase the historical chapter audit. It becomes mandatory for an existing batch when the rule is declared a repository-wide invariant or when that batch is explicitly migrated.

## Lifecycle

`Status=approved` rows constitute the active deck. `Status=deprecated` rows preserve immutable historical lineage and source traceability but are excluded from active export.

## Current batches

- `notes/FND-00.tsv` — foundations; audited through ANKI-AUDIT-006 (#70);
- `notes/COM-01.tsv` — Commercial chapter 01; v1.7 chapter-local Cloze-precision audit applied on top of its current recall-design rules;
- `notes/COM-02.tsv` — Commercial chapter 02; original chapter audit state retained pending explicit migration.

Migration records include:

- `scripts/migrate_fnd00_v1_2.py`
- `scripts/migrate_fnd00_v1_3.py`
- `scripts/migrate_fnd00_v1_4.py`
- `scripts/migrate_fnd00_v1_5.py`
- `scripts/migrate_fnd00_v1_6.py`

Validation:

- `scripts/validate_fnd00_production.py`
- `scripts/validate_com01_production.py`
- `scripts/validate_com02_production.py`
