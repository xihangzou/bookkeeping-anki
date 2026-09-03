# Historical v1.0 Production Baseline Record

Status: **HISTORICAL — not current authority**
Original gate: **ANKI-PILOT-006 / #50**
Baseline basis: ANKI-PILOT-005 merge `8d114f936565519fb37fd39d3d91ed299f5e5f72`
Source baseline at the gate: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`

## Current governance note

This file records the repository state that originally authorized Phase C production generation. It no longer freezes future semantic evolution.

Current authority is defined by `GOVERNANCE.md` and the latest merged `SPEC.md`, `rules/*.md`, `schema/note_schema.yaml`, and applicable production QA/validators.

The v1.0 gate remains important historical evidence, but newer reviewed rules supersede older v1.0 rules for new work and for production batches that are explicitly migrated.

## Historical decision

At ANKI-PILOT-006, the representative pilot passed the final pre-production gate and the then-current authoring/data contract was recorded as **v1.0**. This authorized Phase C chapter-wide Note generation beginning with ANKI-007.

## Historical baseline artifacts

| Artifact | v1.0 identity at the gate | Historical decision |
|---|---|---|
| `SPEC.md` | v1.0 baseline | pilot gate completed; Phase C authorized |
| `rules/cloze_rules.md` | v1.0 baseline | pilot-derived rules accepted for initial production |
| `rules/coverage_rules.md` | v1.0 baseline | pilot-derived coverage/duplicate policy accepted |
| `schema/note_schema.yaml` | version 1.0 | field set, values, tags, source fields, and TSV serialization accepted for initial production |

Branch-time content blob identities from the original baseline change:

- `SPEC.md`: `ddcc2b14fb83d7175184421925d442cb1528bd35`
- `rules/cloze_rules.md`: `d86137c84329286fa2f490bab4062b91463a8fe9`
- `rules/coverage_rules.md`: `2909eece63882714e57de04ffebfbe668adaaf62`
- `schema/note_schema.yaml`: `49910c06aa5a9eed404d88bc0afe50eb91dd4712`

These identities allow exact reconstruction of the historical v1.0 state through Git; they are not immutable current specifications.

## Gate evidence

The corrected representative pilot was:

- Notes: **40**
- generated Cloze cards: **62**
- accounting failures: **0**
- source-traceability failures: **0**
- major findings: **0**
- blocking findings: **0**

All recurring/minor pilot finding families had explicit v1.0 rule treatment or documented no-change decisions at the time. Canonical ALP IDs and source mappings remained valid.

## Historical schema decision

ANKI-PILOT-005 found no evidence at that time requiring semantic changes to:

- Note fields or allowed values;
- tag namespaces;
- `Status` / `QA` semantics;
- deterministic TSV field order, escaping, or list serialization;
- pinned `SourceRepo`, `SourceCommit`, or `SourcePath`;
- canonical ALP IDs or source mappings.

That no-change decision applies to the historical v1.0 gate only. Later reviewed evidence may revise schema or authoring rules under the living-spec process.

## Invariants that survived the v1.0 baseline

Some constraints remain current because they protect lineage and reproducibility rather than because v1.0 is frozen:

1. stable Note IDs remain immutable after assignment;
2. deprecated/deleted IDs are not reused for unrelated content;
3. source and ALP mappings remain auditable;
4. production serialization remains deterministic;
5. existing batches retain pinned source provenance unless an explicit source-baseline migration changes it.

The exact current form of these invariants is governed by `GOVERNANCE.md`, `SPEC.md`, and `schema/note_schema.yaml`.

## Evolution after v1.0

Production audits after the initial gate have already changed active-deck, Cloze, integration, completeness, and formula rules. Those changes are evidence that the repository operates more effectively as a reviewed living specification.

Future semantic changes should therefore be made explicitly in the current authoritative files, with affected validators/migrations updated and relevant production tests passing. No special "post-freeze" exception mechanism is required.
