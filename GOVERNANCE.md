# Repository Governance

Status: **Current authoritative governance**
Issue: **ANKI-GOV-001 / #73; ANKI-GOV-002 / #98**

## 1. Living specification

This repository uses a **living specification** model.

The current merged versions of the following artifacts are authoritative for ongoing generation, explicit migrations, QA, and export:

- `SPEC.md`
- `rules/anki_card_rules.md`
- `schema/note_schema.yaml`
- chapter-local production QA and validators where they define stricter explicitly migrated requirements

`rules/anki_card_rules.md` is the **sole current Markdown authority** for Anki card design, Cloze behavior, coverage, integration/active-deck policy, duplicate control, and recall precision.

The legacy paths below are compatibility/history pointers only and must not contain independent current rules:

- `rules/cloze_rules.md`
- `rules/coverage_rules.md`
- `rules/exam_yield_rules.md`
- `rules/recall_precision_rules.md`

These artifacts may be revised when pilot evidence, production audits, or later chapter work demonstrates a better rule. There is no permanently frozen v1.0 semantic contract.

## 2. Change discipline

Rule, specification, schema, and QA changes must be explicit and reviewable.

A substantive change should normally:

1. identify the observed failure, ambiguity, omission, or efficiency problem;
2. update the relevant authoritative artifact rather than relying on an undocumented local exception;
3. for card-design/coverage/recall policy, update `rules/anki_card_rules.md` rather than creating another competing rule overlay;
4. preserve or deliberately migrate affected production data;
5. update deterministic validation when a rule can be checked mechanically;
6. record the change through an issue/PR or equivalent Git history;
7. run affected production validators before merge.

The latest merged rule supersedes an older rule for new work. Existing chapter batches are migrated only when the change is explicitly applied to them or when a repository-wide invariant requires immediate migration.

## 3. Historical versions

Historical versions remain reproducible through Git commits, issues, PRs, migration scripts, compatibility rule paths, and QA reports.

`FREEZE.md` records the historical v1.0 pilot gate. It is evidence of the initial production baseline, not an authority that blocks later evolution.

Version labels such as v1.0, v1.2, or v1.6 identify historical states or audit milestones. They do not create permanent precedence over newer merged rules.

The pre-ANKI-GOV-002 rule documents remain available through Git history. Their current working-tree forms intentionally point to `rules/anki_card_rules.md` so historical links remain interpretable without creating competing current authority.

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

1. explicit current governance and `rules/anki_card_rules.md` take precedence over historical freeze/pilot/rule language;
2. chapter-local stricter requirements apply only where that batch was explicitly migrated/audited to them and do not create a new repository-wide rule authority;
3. newer merged substantive rules take precedence over older historical rules;
4. stable-ID, source-traceability, and lineage invariants remain mandatory unless explicitly migrated.

Do not preserve a known-bad rule merely because it appeared in v1.0. Do not silently deviate from current rules either; update `rules/anki_card_rules.md` when repository-wide card policy itself needs to change.
