# v1.0 Production Contract Freeze

Status: **FROZEN**
Gate: **ANKI-PILOT-006 / #50**
Freeze basis: ANKI-PILOT-005 merge `8d114f936565519fb37fd39d3d91ed299f5e5f72`
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`

## Decision

The representative pilot passes the final gate. The production authoring/data contract is frozen as **v1.0**, and Phase C chapter-wide Note generation is explicitly authorized beginning with ANKI-007.

## Frozen artifacts

| Artifact | Frozen identity | Semantic decision |
|---|---|---|
| `SPEC.md` | v1.0 frozen | pilot gate completed; Phase C authorized |
| `rules/cloze_rules.md` | v1.0 frozen | ANKI-PILOT-005 candidate rules accepted without further semantic change |
| `rules/coverage_rules.md` | v1.0 frozen | retrieval-unit duplicate policy accepted without further semantic change |
| `schema/note_schema.yaml` | version 1.0 / `frozen: true` | field set, values, tags, source fields, TSV serialization unchanged from v0.9 semantics |

Branch-time content blob identities for the freeze change:

- `SPEC.md`: `ddcc2b14fb83d7175184421925d442cb1528bd35`
- `rules/cloze_rules.md`: `d86137c84329286fa2f490bab4062b91463a8fe9`
- `rules/coverage_rules.md`: `2909eece63882714e57de04ffebfbe668adaaf62`
- `schema/note_schema.yaml`: `49910c06aa5a9eed404d88bc0afe50eb91dd4712`

## Gate evidence

The corrected representative pilot remains:

- Notes: **40**
- generated Cloze cards: **62**
- accounting failures: **0**
- source-traceability failures: **0**
- major findings: **0**
- blocking findings: **0**

All recurring/minor pilot finding families are governed by explicit v1.0 authoring rules or documented no-change decisions. No unresolved answer-leakage blocker remains. Canonical ALP IDs and source mappings remain valid and unchanged.

## Schema no-change decision

ANKI-PILOT-005 found no evidence requiring semantic changes to:

- Note fields or allowed values;
- tag namespaces;
- `Status` / `QA` semantics;
- deterministic TSV field order, escaping, or list serialization;
- pinned `SourceRepo`, `SourceCommit`, or `SourcePath`;
- canonical ALP IDs or source mappings.

ANKI-PILOT-006 therefore changes only schema version/lifecycle metadata (`0.9 → 1.0`, production phase, frozen state) and does not introduce an evidence-free data-contract revision.

## Production authorization

ANKI-007 onward is **UNBLOCKED**.

All production Notes must:

1. use the frozen v1.0 specification, Cloze rules, coverage rules, and schema;
2. preserve stable Note IDs and canonical ALP mappings;
3. satisfy source traceability and deterministic serialization requirements;
4. pass local duplicate/ambiguity checks and relevant accounting/calculation QA;
5. avoid silent semantic deviations from the frozen contract.

Pilot Notes remain pilot evidence. They may be reused in production only after they satisfy the frozen production contract, stable ID/mapping requirements, and production QA.

Any future semantic contract change requires a separately reviewed post-freeze migration.
