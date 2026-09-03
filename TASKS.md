# TASKS

Legend: `[x]` complete, `[-]` in progress, `[ ]` pending.

## Phase A — Specification and inventory

- [x] **ANKI-001** Project scope / mastery definition / source baseline
  - `README.md`
  - `SPEC.md`
- [x] **ANKI-002** Extract complete textbook structure
  - `inventory/structure.md`
  - enumerate Part / chapter / section hierarchy from pinned source
- [x] **ANKI-003** Atomic Learning Point inventory
  - decompose every source section
  - assign ALP IDs
  - include/exclude decision for every candidate proposition
  - output canonical coverage inventory
- [x] **ANKI-004** Necessary-sufficient coverage rules
  - `rules/coverage_rules.md`
- [x] **ANKI-005** Cloze rules v0.9
  - `rules/cloze_rules.md`
- [x] **ANKI-006** Canonical Note schema and tag namespaces
  - `schema/note_schema.yaml`

## Phase B — Pilot and initial production baseline

- [x] **ANKI-PILOT-001** Select representative ALPs from Part 0 + Commercial chapter 01
  - `pilot/selection.tsv`
  - 34 canonical included ALPs / 40 planned pilot Notes
  - all required recall types and stress cases mapped
- [x] **ANKI-PILOT-002** Generate 30–50 pilot Cloze Notes
  - `pilot/notes.tsv`
  - 40 pilot Notes / 34 canonical included ALPs
  - `Status=pilot`, `QA=pending` until card-level validation
- [x] **ANKI-PILOT-003** Validate rendering and recall quality
  - `pilot/card_validation.tsv`
  - `pilot/VALIDATION.md`
  - initial 40 Notes / 63 rendered Cloze cards reviewed; findings handed to ANKI-PILOT-004
- [x] **ANKI-PILOT-004** Record ambiguity / overload / duplication failures
  - `pilot/review.md`
  - blocking ambiguity/comparison defects fixed; exact duplicate converted to distinct numeric application
  - corrected pilot: 40 Notes / 62 cards, 0 major, 0 blocking
- [x] **ANKI-PILOT-005** Revise Cloze / coverage rules v0.9 -> v1.0 candidate
  - `rules/cloze_rules.md`: pilot-derived grouping, unique-answer, comparison, formula, journal-entry, answer-equivalence, retrieval-value, and card-level dedup rules
  - `rules/coverage_rules.md`: generated-card / retrieval-unit semantic deduplication
  - `pilot/review.md`: evidence-to-rule matrix and explicit schema/tag/source/TSV no-change rationale
  - corrected pilot preserved: 40 Notes / 62 cards, 0 major, 0 blocking
- [x] **ANKI-PILOT-006** Establish v1.0 initial production baseline
  - `FREEZE.md`: historical gate evidence and original production authorization
  - `SPEC.md`, `rules/cloze_rules.md`, `rules/coverage_rules.md`: v1.0 baseline recorded (later superseded by living-spec governance)
  - `schema/note_schema.yaml`: v1.0 production baseline recorded; semantic schema contract was unchanged at that gate
  - corrected pilot: 40 Notes / 62 cards, 0 accounting failures, 0 source-traceability failures, 0 major, 0 blocking
  - Phase C / ANKI-007 onward unblocked

## Phase C — Full note generation

### Foundation

- [x] **ANKI-007** Part 0 / commercial chapter00 generation
  - `production/notes/FND-00.tsv`: 91 historical production rows / 91 included ALPs
  - `production/qa/FND-00.md`: chapter-local Cloze, duplicate, accounting, formula, and source-traceability QA
  - `scripts/validate_fnd00_production.py` + `validate-production.yml`: deterministic production validation
  - 16 pilot Note IDs promoted without renumbering; `BK-FND-00-0016` remains reserved pilot-only evidence
- [x] **ANKI-AUDIT-001** FND-00 recall-quality / exam-yield audit (#56)
  - 91 historical rows retained; active approved Notes **91 → 57**; deprecated audit rows **34**
  - low-yield terminology/list recall consolidated; transaction-duality wording corrected
  - GitHub Actions v1.1 production validation: **PASS**
- [x] **ANKI-AUDIT-002** FND-00 rotation-efficiency / Cloze-atomicity audit (#58)
  - active approved Notes remain **57**; generated Cloze cards **110 → 58**
  - same-index grouping and standalone-answer rules introduced
  - GitHub Actions v1.2 production validation: **PASS**
- [x] **ANKI-AUDIT-003** FND-00 minimal active deck / lexical same-card Cloze audit (#62)
  - active approved Notes **57 → 18**; active direct-recall ALPs **36/91**
  - generated active cards **58 → 18**; active lexical Cloze spans **36**
  - parallel answers use separate lexical spans on the same `c1`
  - PR #65 CI **PASS**
- [x] **ANKI-AUDIT-004** FND-00 balanced active-deck / visible-context audit (#66)
  - importance screening relaxed; integration-first card control adopted
  - active approved Notes/cards **18 → 29**; active direct-recall ALPs **36 → 61 / 91**
  - active Cloze spans **70**; all approved Notes use only `c1`
  - visible retrieval context enforced; debit/credit uses `{{c1::借}}方` / `{{c1::貸}}方`
  - PR #67 squash merge `26a547ef2e2b48f9c93433e9e25d56e0939a743e`; CI **PASS**
- [x] **ANKI-AUDIT-005** FND-00 maximal ALP integration / answer-leak audit (#68)
  - user correction: remove `簿記の基本では、` from `BK-FND-00-0018`
  - user correction: `BK-FND-00-0027` uses `{{c1::に終わる}}` / `{{c1::から始まる}}`
  - all remaining inactive ALPs re-audited; active coverage **61/91 → 91/91**
  - card count increases only **29 → 32** through three coherent reactivations: `0048`, `0084`, `0091`
  - active Cloze spans **70 → 120** while every approved Note remains one `c1` card
  - exact visible-answer leakage for 2+ character answers **11 Notes → 0**
  - `scripts/migrate_fnd00_v1_5.py` + strengthened v1.5 validator; FND-00 / COM-01 / COM-02 CI **PASS**
- [x] **ANKI-AUDIT-006** FND-00 content-preservation / formula-itemization audit (#70)
  - retain **32 approved Notes / 32 cards / 91 active ALPs** while restoring mapped-but-underrepresented source content
  - active Cloze spans **120 → 150**; increase comes from richer same-card recall, not extra cards
  - formulas use term-level same-index Clozes, e.g. `{{c1::収益}}－{{c1::費用}}` and term-wise net-sales/net-purchases formulas
  - restore all ten representative expense accounts from the pinned source
  - restore general-ledger `標準式` / `残高式`, material field mechanics, and main-book process flow
  - `BK-FND-00-0084` explicitly states `各伝票から{{c1::個別転記}}する` for subsidiary ledgers
  - restore other compressed ALP content including residual definition, period vocabulary, temporary-account classification, correction logic, subsidiary-book mechanics, voucher/document details
  - `scripts/migrate_fnd00_v1_6.py` + strengthened v1.6 validator; visible-answer leakage remains **0**; FND-00 validation **PASS**

- [x] **ANKI-GOV-001** Living-spec governance / retire permanent v1.0 freeze authority (#73)
  - latest merged `SPEC.md`, `rules/*.md`, schema, and applicable QA/validators are the current authority
  - `FREEZE.md` retained as historical v1.0 baseline evidence only
  - stable IDs, source traceability, pinned batch provenance, and deterministic lineage remain persistent invariants
  - schema lifecycle changed from frozen v1.0 metadata to reviewed living-spec governance
  - governance CI prevents reintroduction of active `frozen v1.0` / `post-freeze` authority language

### Commercial bookkeeping

- [x] **ANKI-008** Commercial chapter01
  - `production/notes/COM-01.tsv`: **38 approved Notes / 38 generated cards / 52 included ALPs / 0 unmapped**
  - 52/52 included ALPs map exactly once; **14** coherent multi-ALP Notes remove redundant direct recall
  - **18** reviewed pilot IDs promoted; **5** pilot-only duplicate-application IDs remain reserved
  - `production/qa/COM-01.md` + `scripts/validate_com01_production.py`; CI validation wired into `validate-production.yml`
- [x] **ANKI-009** Commercial chapter02
  - `production/notes/COM-02.tsv`: **17 approved Notes / 17 generated cards / 32 included ALPs / 0 unmapped**
  - 32/32 included ALPs map exactly once; **11** coherent multi-ALP Notes remove redundant direct recall
  - no prior COM-02 pilot IDs; stable production IDs allocated as `BK-COM-02-0001`–`BK-COM-02-0017`
  - `production/qa/COM-02.md` + `scripts/validate_com02_production.py`; CI validation wired into `validate-production.yml`
- [x] **ANKI-AUDIT-007** COM-02 current living-rule / ALP-containment migration (#77)
  - explicitly migrate the historical ANKI-009 v1.2 batch to the latest living authoring and exam-yield rules
  - retain **17 approved Notes / 17 cards / 32 included ALPs / 11 multi-ALP Notes** and all stable IDs
  - Cloze spans **32 → 39** through term-level same-card itemization; every Note remains `c1` only
  - itemize recognition-basis and formula terms; retain compact whole-entry recall only for four reviewed coupled-entry Notes
  - re-audit all 32 ALPs for material proposition containment in active `Text`; exact visible-answer leakage remains **0**
  - strengthen `scripts/validate_com02_production.py` for lexical atomicity, formula itemization, compact-entry exceptions, content requirements, and answer-leak detection
- [x] **ANKI-010** Commercial chapter03
  - `production/notes/COM-03.tsv`: **25 approved Notes / 25 generated cards / 70 Cloze spans / 38 included ALPs / 0 unmapped**
  - 38/38 included ALPs map exactly once; **9** coherent multi-ALP Notes; **2** decorative numerical-example rows remain excluded by canonical inventory status
  - current recall-precision rules applied at initial generation: account-level same-`c1` journal Clozes, canonical-label priority, visible-answer leakage **0**
  - stable production IDs allocated deterministically as `BK-COM-03-0001`–`BK-COM-03-0025`
  - `production/qa/COM-03.md` + `scripts/validate_com03_production.py`; CI validation wired into `validate-production.yml`
- [ ] **ANKI-011** Commercial chapter04
- [ ] **ANKI-012** Commercial chapter05
- [ ] **ANKI-013** Commercial chapter06
- [ ] **ANKI-014** Commercial chapter07
- [ ] **ANKI-015** Commercial chapter08
- [ ] **ANKI-016** Commercial chapter09
- [ ] **ANKI-017** Commercial chapter10
- [ ] **ANKI-018** Commercial chapter11
- [ ] **ANKI-019** Commercial chapter12
- [ ] **ANKI-020** Commercial chapter13
- [ ] **ANKI-021** Commercial chapter14
- [ ] **ANKI-022** Commercial chapter15
- [ ] **ANKI-023** Commercial chapter16

### Industrial bookkeeping

- [ ] **ANKI-024** Industrial chapter01
- [ ] **ANKI-025** Industrial chapter02
- [ ] **ANKI-026** Industrial chapter03
- [ ] **ANKI-027** Industrial chapter04
- [ ] **ANKI-028** Industrial chapter05
- [ ] **ANKI-029** Industrial chapter06
- [ ] **ANKI-030** Industrial chapter07
- [ ] **ANKI-031** Industrial chapter08
- [ ] **ANKI-032** Industrial chapter09
- [ ] **ANKI-033** Industrial chapter10
- [ ] **ANKI-034** Industrial chapter11
- [ ] **ANKI-035** Industrial chapter12
- [ ] **ANKI-036** Industrial chapter13
- [ ] **ANKI-037** Industrial chapter14

## Phase D — Normalization

- [ ] **ANKI-038** Cross-chapter semantic deduplication
  - preserve materially different retrieval contexts
  - merge exact/semantic duplicates
  - verify no source proposition loses traceability

## Phase E — Accounting QA

- [ ] **ANKI-039** Journal-entry QA
  - accounts
  - debit/credit
  - amount
  - recognition timing
  - compound entries
- [ ] **ANKI-040** Formula / calculation QA
  - formulas
  - derivations
  - allocation
  - inventory/cost flow
  - industrial calculations

## Phase F — Recall and coverage QA

- [ ] **ANKI-041** Cloze quality QA
  - ambiguity
  - context sufficiency
  - lexical atomicity
  - same-card grouping quality
  - visible-answer leakage
  - over-deletion
  - trivial clozes
- [ ] **ANKI-042** Coverage QA
  - 100% source sections reviewed
  - 100% included ALPs traceable in production history
  - every retirement/exclusion justified
  - active direct recall justified by exam value and/or coherent integration
  - mapped active Notes preserve the material proposition of each included ALP
  - no unresolved duplicates/conflicts

## Phase G — Export

- [ ] **ANKI-043** Export
  - canonical TSV
  - import validation
  - APKG
  - export manifest with source baseline, source-reviewed coverage, active-recall coverage, Note/card/span counts

## Completion gate

Project is complete only when all are true:

- source sections reviewed: 100%
- included ALPs traceable in production history: 100%
- mapped active ALPs materially represented in active Note text: 100%
- unexplained exclusions/retirements: 0
- unresolved accounting QA failures: 0
- unresolved ambiguous Clozes: 0
- approved notes with source traceability: 100%
- export reproducible from canonical repository data