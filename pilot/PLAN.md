# Pilot Plan

Purpose: validate Cloze rules v0.9 before generating the full textbook deck.

## Scope

Use representative material from:

- `commercial/chapter00.md` (Part 0 / bookkeeping foundations)
- `commercial/chapter01.md` (commercial bookkeeping / merchandise)

Target: **30–50 Notes**. The count is a validation target only, not a production quota.

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
├── notes.tsv
└── review.md
```
