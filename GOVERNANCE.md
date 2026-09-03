# Repository Governance

Status: **Current authoritative governance**
Issue: **ANKI-GOV-001 / #73**

## 1. Living specification

This repository uses a **living specification** model.

The current merged versions of the following artifacts are authoritative for ongoing generation, explicit migrations, QA, and export:

- `SPEC.md`
- `rules/cloze_rules.md`
- `rules/coverage_rules.md`
- `rules/exam_yield_rules.md`
- `schema/note_schema.yaml`
- chapter-local production QA and validators where they define stricter audited requirements

These artifacts may be revised when pilot evidence, production audits, or later chapter work demonstrates a better rule. There is no permanently frozen v1.0 semantic contract.

## 2. Change discipline

Rule, specification, schema, and QA changes must be explicit and reviewable.

A substantive change should normally:

1. identify the observed failure, ambiguity, omission, or efficiency problem;
2. update the relevant authoritative artifact rather than relying on an undocumented local exception;
3. preserve or deliberately migrate affected production data;
4. update deterministic validation when a rule can be checked mechanically;
5. record the change through an issue/PR or equivalent Git history;
6. run affected production validators before merge.

The latest merged rule supersedes an older rule for new work. Existing chapter batches are migrated only when the change is explicitly applied to them or when a repository-wide invariant requires immediate migration.

## 3. Historical versions

Historical versions remain reproducible through Git commits, issues, PRs, migration scripts, and QA reports.

`FREEZE.md` records the historical v1.0 pilot gate. It is evidence of the initial production baseline, not an authority that blocks later evolution.

Version labels such as v1.0, v1.2, or v1.6 identify historical states or audit milestones. They do not create permanent precedence over newer merged rules.

## 4. Persistent invariants

Living rules do not mean arbitrary mutation. The following invariants remain in force unless a separately reviewed repository-wide migration explicitly changes them:

- stable Note IDs are immutable after assignment;
- deprecated or deleted stable IDs are never reused for unrelated content;
- ALP IDs and source mappings remain auditable;
- every production Note remains source-traceable;
- already generated batches retain their pinned `SourceRepo`, `SourceCommit`, and `SourcePath` unless an explicit source-baseline migration is approved;
- deterministic serialization and validation must remain reproducible;
- historical production lineage must not be silently rewritten.

## 5. Source baseline versus rule baseline

The pinned textbook commit is a **source baseline**, not a rule freeze.

A batch may continue to use a pinned source commit while authoring, coverage, Cloze, schema, and QA rules evolve. Updating the textbook source baseline is a separate reviewed migration from updating deck-design rules.

## 6. Conflict resolution

When repository documents conflict:

1. explicit current governance and current rule text take precedence over historical freeze/pilot language;
2. more specific audited chapter requirements take precedence over generic guidance for that chapter;
3. newer merged substantive rules take precedence over older historical rules;
4. stable-ID, source-traceability, and lineage invariants remain mandatory unless explicitly migrated.

Do not preserve a known-bad rule merely because it appeared in v1.0. Do not silently deviate from the current rules either; update the authoritative rule set when the policy itself needs to change.
