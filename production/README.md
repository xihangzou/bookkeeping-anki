# Production Notes

Canonical production Cloze-note batches live under `production/notes/` as UTF-8 TSV files following the **current** schema in `schema/note_schema.yaml`.

Repository-wide governance is defined in `GOVERNANCE.md`. Current authoring, coverage, active-deck, recall design, wording, and ALP-containment rules are governed by the latest merged `SPEC.md` and `rules/*.md`; v1.0 is a historical baseline rather than permanent authority.

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

An ALP mapping alone is not enough: the material proposition should be recoverable from active Note `Text`; `Extra` is secondary support rather than a substitute for source containment.

## Current Cloze / completeness rules

Current rules include:

- normal Cloze spans should be lexical names or short discriminating chunks;
- arithmetic/formula operators remain visible and formula terms are Clozed separately;
- repeated same-index formula terms may be hidden in every occurrence when structural reuse would otherwise leak the answer;
- parallel terms belonging to one retrieval operation use the same `c1`;
- debit/credit direction uses `{{c1::借}}方` / `{{c1::貸}}方` when direction itself is the target;
- a compact whole journal entry may be one Cloze when the entry itself is the retrieval target;
- method names are stated visibly when an indirect description would make the card ambiguous;
- terminology-definition cards normally leave the definition visible and Cloze the technical name;
- function words such as `のみ` normally remain outside the Cloze;
- the visible text after masking must still identify the retrieval frame;
- a 2+ character Cloze answer must not appear verbatim elsewhere in the visible card;
- source families represented by included ALPs must not be silently truncated during integration.

FND-00 v1.6 is the general style reference for context-rich integrated cards with short answers. COM-01 v1.8 adds chapter evidence for whole-entry recall, explicit method naming, formula-term reuse, and stronger material-proposition containment. COM-02 ANKI-AUDIT-007 applies the same current-rule precision to revenue-recognition, warranty, and service-accounting mechanics.

See `rules/cloze_rules.md`, `rules/coverage_rules.md`, and especially `rules/exam_yield_rules.md` for the authoritative current wording.

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

- `notes/COM-01.tsv` — **38 approved Notes / 38 cards / 99 Cloze spans / 52 included ALPs; v1.8 precision / ALP-containment audit applied**;
- `notes/COM-02.tsv` — **17 approved Notes / 17 cards / 39 Cloze spans / 32 included ALPs; ANKI-AUDIT-007 current living-rule / ALP-containment migration applied**.

COM-02 retains the historical ANKI-009 v1.2 metrics in Git history and issue #10, while its current production state is governed by the explicit migration in issue #77. Stable IDs and the pinned source baseline were preserved.

## Lifecycle

`Status=approved` rows constitute the active deck. `Status=deprecated` rows preserve immutable historical lineage and source traceability but are excluded from active export.

## Current batches

- `notes/FND-00.tsv` — foundations; audited through ANKI-AUDIT-006 (#70);
- `notes/COM-01.tsv` — Commercial chapter 01; v1.8 precision / ALP-containment audit applied;
- `notes/COM-02.tsv` — Commercial chapter 02; ANKI-AUDIT-007 (#77) current-rule precision / ALP-containment migration applied.

Migration/audit records include:

- `scripts/migrate_fnd00_v1_2.py`
- `scripts/migrate_fnd00_v1_3.py`
- `scripts/migrate_fnd00_v1_4.py`
- `scripts/migrate_fnd00_v1_5.py`
- `scripts/migrate_fnd00_v1_6.py`
- issue/PR history and `production/qa/COM-01.md` for COM-01 precision audits;
- issue #77 and `production/qa/COM-02.md` for the explicit COM-02 living-rule migration.

Validation:

- `scripts/validate_fnd00_production.py`
- `scripts/validate_com01_production.py`
- `scripts/validate_com02_production.py`
