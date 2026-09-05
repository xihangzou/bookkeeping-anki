# TASKS

Legend: `[x]` complete, `[-]` in progress, `[ ]` pending. Detailed completion evidence lives in the linked GitHub Issues/PRs and chapter QA files.

## Current authoritative contract

- `GOVERNANCE.md` — living-spec governance
- `SPEC.md` — deck/source/mastery specification
- `rules/anki_card_rules.md` — **sole current Anki card-design / coverage / recall rule Markdown**
- `schema/note_schema.yaml` — canonical Note schema/lifecycle
- `FREEZE.md` — historical v1.0 pilot gate only

Legacy rule paths (`cloze_rules.md`, `coverage_rules.md`, `exam_yield_rules.md`, `recall_precision_rules.md`) are compatibility/history pointers after ANKI-GOV-002.

## Phase A — Specification and inventory

- [x] **ANKI-001** Project scope / mastery definition / source baseline
- [x] **ANKI-002** Extract complete textbook structure
- [x] **ANKI-003** Atomic Learning Point inventory
- [x] **ANKI-004** Necessary-sufficient coverage rules (historical precursor; integrated into `rules/anki_card_rules.md`)
- [x] **ANKI-005** Cloze rules v0.9 (historical precursor; integrated into `rules/anki_card_rules.md`)
- [x] **ANKI-006** Canonical Note schema and tag namespaces

## Phase B — Pilot and initial production baseline

- [x] **ANKI-PILOT-001** Select representative ALPs
- [x] **ANKI-PILOT-002** Generate pilot Cloze Notes
- [x] **ANKI-PILOT-003** Validate rendering and recall quality
- [x] **ANKI-PILOT-004** Record failure patterns
- [x] **ANKI-PILOT-005** Revise initial rules to v1.0 candidate
- [x] **ANKI-PILOT-006** Establish historical v1.0 production baseline

Historical pilot evidence remains in `pilot/` and `FREEZE.md`. Current work uses the living consolidated rule set.

## Governance / rule evolution

- [x] **ANKI-GOV-001** Living-spec governance; retire permanent v1.0 freeze authority (#73)
- [x] **ANKI-GOV-002** Consolidate Anki card rules into one authoritative Markdown (#98)
  - integrate Cloze, coverage, exam-yield/active-deck, and recall-precision rules into `rules/anki_card_rules.md`
  - retain old rule paths only as compatibility/history pointers
  - update governance/spec/docs/CI and downstream Issues to the consolidated living contract

Production audit Issues (ANKI-AUDIT-001 onward) remain historical evidence for why current rules evolved. Their generalizable rules are integrated into `rules/anki_card_rules.md`.

## Phase C — Full note generation

### Foundation

- [x] **ANKI-007** Part 0 / FND-00 production generation
- [x] **ANKI-AUDIT-001–006** FND-00 active-deck / completeness / formula / leakage audits

### Commercial bookkeeping

- [x] **ANKI-008** Commercial chapter01
- [x] **ANKI-009** Commercial chapter02
- [x] **ANKI-010** Commercial chapter03
- [x] **ANKI-011** Commercial chapter04
- [x] **ANKI-012** Commercial chapter05
- [x] **ANKI-013** Commercial chapter06
- [x] **ANKI-014** Commercial chapter07
- [x] **ANKI-015** Commercial chapter08
- [x] **ANKI-016** Commercial chapter09
- [x] **ANKI-017** Commercial chapter10
- [x] **ANKI-018** Commercial chapter11
- [x] **ANKI-019** Commercial chapter12
- [ ] **ANKI-020** Commercial chapter13
- [x] **ANKI-021** Commercial chapter14
- [ ] **ANKI-022** Commercial chapter15
- [x] **ANKI-023** Commercial chapter16

### Industrial bookkeeping

- [x] **ANKI-024** Industrial chapter01
- [x] **ANKI-025** Industrial chapter02
- [ ] **ANKI-026** Industrial chapter03
- [ ] **ANKI-027** Industrial chapter04
- [ ] **ANKI-028** Industrial chapter05
- [ ] **ANKI-029** Industrial chapter06
- [x] **ANKI-030** Industrial chapter07
- [ ] **ANKI-031** Industrial chapter08
- [ ] **ANKI-032** Industrial chapter09
- [x] **ANKI-033** Industrial chapter10
- [ ] **ANKI-034** Industrial chapter11
- [ ] **ANKI-035** Industrial chapter12
- [ ] **ANKI-036** Industrial chapter13
- [ ] **ANKI-037** Industrial chapter14

Every pending generation task must use the **latest merged** `rules/anki_card_rules.md` plus the current schema and pinned source/ALP shard. Historical v1.0 wording is not the active authoring contract.

## Phase D — Normalization

- [ ] **ANKI-038** Cross-chapter semantic normalization/deduplication
  - use retrieval-unit-level duplicate control from `rules/anki_card_rules.md`
  - preserve exact-once ALP traceability and stable IDs

## Phase E — Accounting QA

- [ ] **ANKI-039** Journal-entry QA
  - accounts, debit/credit, amounts, recognition timing, compound entries
  - preserve current account-level journal Cloze design during corrections
- [ ] **ANKI-040** Formula/calculation QA
  - formulas, derivations, allocation, inventory/cost flow, industrial calculations
  - preserve visible operators and atomic operand masking

## Phase F — Recall and coverage QA

- [ ] **ANKI-041** Cloze / recall-quality QA
  - ambiguity, visible context, minimal lexical scope, same-index grouping, answer leakage, over-deletion, recall value
- [ ] **ANKI-042** Final semantic coverage QA
  - 100% source sections reviewed
  - 100% included ALPs mapped/materially represented
  - all exclusions justified
  - no unresolved orphan/duplicate/conflict

## Phase G — Export

- [ ] **ANKI-043** Deterministic export
  - canonical TSV
  - import/round-trip validation
  - APKG where supported
  - manifest records source baseline, schema identity, consolidated rule identity, Note/card/span counts

## Completion gate

Project is complete only when all are true:

- source sections reviewed: 100%
- included ALPs traceable in production history: 100%
- mapped active ALPs materially represented in active Note text: 100%
- unexplained exclusions/retirements: 0
- unresolved accounting QA failures: 0
- unresolved formula/calculation failures: 0
- unresolved ambiguous/leaking Clozes: 0
- unresolved semantic duplicates/orphans: 0
- approved Notes with source traceability: 100%
- export reproducible from canonical repository data
