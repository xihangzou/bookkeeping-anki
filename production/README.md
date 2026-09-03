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
- repeated same-index terms may be hidden in every occurrence when structural reuse would otherwise leak the answer;
- parallel terms belonging to one retrieval operation use the same `c1`;
- debit/credit direction uses `{{c1::借}}方` / `{{c1::貸}}方` only when direction itself is the target;
- for newly authored or explicitly re-audited ordinary journal entries, debit/credit labels and separators remain visible while each account name is Clozed separately with the same `c1` when the entry is one coherent retrieval unit;
- historical compact whole-entry forms may remain only in batches not yet explicitly migrated under the newer recall-precision specialization;
- when a visible description maps one-to-one to a named accounting concept, prefer Clozing the canonical label when label identification is the useful retrieval operation;
- terminology-definition cards normally leave the definition visible and Cloze the technical name;
- function words such as `のみ` normally remain outside the Cloze;
- the visible text after masking must still identify the retrieval frame;
- a 2+ character Cloze answer must not appear verbatim elsewhere in the visible card;
- source families represented by included ALPs must not be silently truncated during integration.

FND-00 v1.6 is the general style reference for context-rich integrated cards with short answers. COM-01 v1.8 adds chapter evidence for explicit method naming, formula-term reuse, and stronger material-proposition containment. COM-02 ANKI-AUDIT-008/009 establishes account-level journal Clozes and canonical-label priority. COM-03 applies those current rules directly at initial production generation.

See `rules/cloze_rules.md`, `rules/coverage_rules.md`, `rules/exam_yield_rules.md`, and `rules/recall_precision_rules.md` for the authoritative current wording.

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
- `notes/COM-02.tsv` — **17 approved Notes / 17 cards / 50 Cloze spans / 32 included ALPs; ANKI-AUDIT-008/009 recall-precision and canonical-label audits applied**;
- `notes/COM-03.tsv` — **25 approved Notes / 25 cards / 70 Cloze spans / 38 included ALPs; current living recall rules applied at generation**.

COM-02 retains historical ANKI-009 and ANKI-AUDIT-007 metrics in Git history and their issues; its current production state includes the later ANKI-AUDIT-008/009 precision changes. Stable IDs and the pinned source baseline were preserved.

COM-03 is generated directly under the current account-level journal and canonical-label rules. Its two decorative numerical examples remain excluded by canonical inventory status, while all 38 included ALPs map exactly once to active Text.

## Lifecycle

`Status=approved` rows constitute the active deck. `Status=deprecated` rows preserve immutable historical lineage and source traceability but are excluded from active export.

## Current batches

- `notes/FND-00.tsv` — foundations; audited through ANKI-AUDIT-006 (#70);
- `notes/COM-01.tsv` — Commercial chapter 01; v1.8 precision / ALP-containment audit applied;
- `notes/COM-02.tsv` — Commercial chapter 02; audited through ANKI-AUDIT-009 (#81);
- `notes/COM-03.tsv` — Commercial chapter 03; generated under ANKI-010 (#11) with current living recall rules.

Migration/audit records include:

- `scripts/migrate_fnd00_v1_2.py`
- `scripts/migrate_fnd00_v1_3.py`
- `scripts/migrate_fnd00_v1_4.py`
- `scripts/migrate_fnd00_v1_5.py`
- `scripts/migrate_fnd00_v1_6.py`
- issue/PR history and `production/qa/COM-01.md` for COM-01 precision audits;
- issues #77, #79, #81 and `production/qa/COM-02.md` for COM-02 migrations/audits;
- issue #11 and `production/qa/COM-03.md` for COM-03 initial production generation.

Validation:

- `scripts/validate_fnd00_production.py`
- `scripts/validate_com01_production.py`
- `scripts/validate_com02_production.py`
- `scripts/validate_com03_production.py`
