# Recall Precision Rules

Status: **Current authoritative specialization**
Issue: **ANKI-AUDIT-008 / #79**
Governance: `GOVERNANCE.md`

This file specializes `rules/cloze_rules.md` and `rules/exam_yield_rules.md` for answer precision. Where an older generic rule allows a broader form, this more specific reviewed rule takes precedence for new work and explicitly migrated batches.

## 1. Journal entries: Cloze account names, not the tuple

For ordinary journal-entry recall, keep debit/credit labels, separators, and amounts visible. Cloze each account name separately using the same index when the entry is one coherent retrieval unit.

Preferred:

`（借）{{c1::売掛金}}／（貸）{{c1::売上}}`

`（借）{{c1::買掛金}}／（貸）{{c1::仕入}}`

Avoid:

`{{c1::（借）売掛金／（貸）売上}}`

`{{c1::借方：売掛金／貸方：売上}}`

The old compact-whole-entry exception is retired for newly authored or explicitly re-audited production Notes. If the same account occurs twice in one integrated procedure, hide every occurrence with the same `c1` so the visible card does not leak the answer.

Amounts copied directly from the prompt remain visible. Cloze an amount only when calculation or measurement is itself the target.

## 2. Canonical answer precision

Prefer the smallest accounting answer that captures the material proposition:

- account name;
- technical term;
- recognition point;
- method/document name;
- formula operand;
- short discriminator.

Avoid approximate prose such as `果たした時点`, `売上を再計上しない`, `仕入を減額する`, or a whole explanatory clause when a canonical accounting term or exact timing discriminator can be recalled instead.

For recognition rules, keep the accounting subject visible and Cloze the timing concept. Example:

`本業収益は、その約束を{{c1::充足した時点}}に認識する。`

## 3. Essential-recall test

A Note should earn active review time by testing at least one of the following:

- account selection or journal mechanics;
- recognition timing;
- classification that changes accounting treatment;
- formula/measurement relationship;
- method or document discrimination needed to solve questions;
- a material exception that changes the entry or measurement.

Do not create a Cloze merely because a sentence contains terminology. Example-only details, explanatory paraphrases, and obvious consequences should normally remain visible or move to `Extra` unless direct recall has independent exam value.

An included ALP still must remain materially represented in active `Text`; this rule changes what is hidden, not whether source content is silently dropped.

## 4. Reference style

Use FND-00 and COM-01 as the default style reference for short, visible-context, same-card lexical answers. ANKI-AUDIT-008 specifically supersedes legacy compact-entry examples that remain in older chapter history.

Existing chapters are migrated deliberately under `GOVERNANCE.md`; historical audit states remain reproducible through Git history.
