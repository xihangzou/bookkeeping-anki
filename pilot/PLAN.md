> **Historical pilot artifact.** References in this file to a v1.0 freeze describe the original pre-production gate. They do not define current repository governance; current authority is `GOVERNANCE.md` and the latest merged specification/rules/schema.

# Pilot Plan

Purpose: validate Cloze rules v0.9 before generating the full textbook deck.

## Scope

Use representative material from:

- `commercial/chapter00.md` (Part 0 / bookkeeping foundations)
- `commercial/chapter01.md` (commercial bookkeeping / merchandise)

Target: **30–50 Notes**. The count is a validation target only, not a production quota.

## Canonical pilot selection

`pilot/selection.tsv` is the deterministic ALP selection contract for the pilot.

Selection rules:

- every selected row must reference a canonical `INCLUDE` ALP from `inventory/topic_inventory/FND-00.tsv` or `inventory/topic_inventory/COM-01.tsv`;
- source part, chapter, section, and anchor are copied into the selection artifact so every selected ALP remains source-traceable;
- `recall_dimensions` maps each selected ALP to the recall type(s) the pilot must exercise;
- `stress_cases` maps each selected ALP to the stress cases below;
- `planned_note_forms` and `expected_notes` are planning metadata for ANKI-PILOT-002, not a production quota;
- `stress_fixture` may point to an adjacent canonical `EXCLUDE` example when the purpose is to verify that redundant decorative examples do not become independent Notes.

The current selection contains **34 canonical included ALPs** and is designed to support **40 pilot Notes** if ANKI-PILOT-002 follows the planned note forms. This 40-Note estimate exists only to demonstrate that the selection can support the 30–50 validation window.

## Required recall types

Pilot must include at least:

- definition
- classification
- recognition timing
- simple journal entry
- compound journal entry
- formula
- numerical application
- procedure/order
- comparison
- exception/condition
- reasoning / why

## Required stress cases

Include examples that test:

1. same fact appearing in foundation and advanced context;
2. whether two facts should share one cloze number;
3. account names vs amounts in journal-entry cards;
4. formula decomposition;
5. long procedural chains;
6. tables converted to recall units;
7. examples that should be excluded as redundant;
8. cards where visible context might leak the answer;
9. cards with possible synonymous answers;
10. compound entries with multiple debit/credit accounts.

In `pilot/selection.tsv`, these are encoded deterministically as `S1_...` through `S10_...`.

## Review dimensions

For every pilot note mark:

- accounting accuracy
- unambiguous target
- context sufficiency
- atomicity
- answer size
- cloze numbering quality
- duplicate risk
- source traceability
- usefulness after repeated review

## Gate to v1.0

Do not start chapter-wide generation until:

- all pilot accounting errors are fixed;
- all ambiguous prompts are fixed;
- repeated failure patterns are translated into explicit rules;
- `rules/cloze_rules.md` is revised to v1.0;
- v1.0 is frozen.

## Expected artifacts

```text
pilot/
├── PLAN.md
├── selection.tsv
├── notes.tsv
└── review.md
```
