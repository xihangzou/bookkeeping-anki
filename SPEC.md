# Anki Deck Specification

Status: **Current authoritative specification — living document**
Governance: `GOVERNANCE.md`

## 1. Scope

The deck covers the complete content of:

- `xihangzou/bookkeeping-integrated/merged/textbook.md`
- current production source baseline commit `569ed7b82e729334e1472286eaca7c4352e6fbdb`

Scope equals bookkeeping levels 2 and 3 as integrated in that textbook, including:

- Part 0 簿記の基礎
- Part I 商業簿記
- Part II 工業簿記

No chapter is excluded merely because it is advanced relative to level 3.

The source baseline and the authoring-rule baseline are separate. The source commit may remain pinned while specification, Cloze, coverage, schema, and QA rules improve through reviewed repository changes.

## 2. Mastery definition

"100% mastery" means every necessary learning point in the source textbook is represented by enough recall prompts to reproduce the knowledge required for correct reasoning, journal entries, calculations, procedures, comparisons, and exceptions.

It does **not** mean every sentence or example must become a card.

A deck is complete only when:

1. every source section has been reviewed;
2. every included Atomic Learning Point is traceable in production history and materially represented according to current coverage rules;
3. every excluded source unit has an explicit exclusion reason;
4. all journal entries and calculations have passed accounting QA;
5. all approved notes have passed current Cloze QA;
6. there are no unresolved duplicate or conflicting notes;
7. current authoritative rules and validators are internally consistent.

## 3. Unit hierarchy

```text
Source block
  -> Topic
    -> Atomic Learning Point (ALP)
      -> Recall Unit
        -> Cloze Note
          -> one or more Anki cards
```

### Atomic Learning Point

The smallest proposition that can be independently tested and whose omission would create a meaningful knowledge gap.

Typical ALP types:

- definition
- classification
- recognition
- measurement
- journal_entry
- formula
- procedure
- comparison
- exception
- reasoning
- ledger
- financial_statement
- cost_accounting

## 4. Note philosophy

- Primary note type: Anki Cloze.
- One note should represent one coherent recall unit.
- Context must remain visible so the answer is inferable from knowledge, not from guessing what the question is asking.
- Related ALPs should be integrated when they form one coherent retrieval frame.
- Card count is controlled primarily by coherent integration and same-index grouping, not by silently dropping useful source content.
- A note may create several cards only when the masked facts are independently worth recalling.
- Closely coupled or parallel facts that should be recalled together may share the same cloze number.
- `Extra` explains reasoning, common errors, derivation, or source nuance; it must not become a substitute for recalling required knowledge.

The single authoritative current card-design/coverage/recall rule document is `rules/anki_card_rules.md`.

The legacy paths `rules/cloze_rules.md`, `rules/coverage_rules.md`, `rules/exam_yield_rules.md`, and `rules/recall_precision_rules.md` are compatibility/history pointers only.

## 5. Coverage policy

Include information when omission could cause one of the following:

- wrong account classification;
- wrong debit/credit direction;
- wrong recognition timing;
- wrong journal entry;
- wrong calculation;
- wrong procedural order;
- confusion between similar methods;
- failure to apply a condition or exception;
- inability to explain an important accounting relationship;
- inability to read or execute material bookkeeping mechanics represented in the source.

Exclude or merge:

- rhetorical introductions;
- exact repetition;
- paraphrases with no additional condition;
- decorative examples whose only change is arbitrary numbers;
- facts already fully recalled by another note unless a different retrieval context is genuinely useful.

An ALP mapped to an approved integrated Note must remain materially recoverable from that Note; ALP mapping alone is not evidence of active content coverage.

See `rules/anki_card_rules.md`.

## 6. Source traceability

Every note must carry:

- source repository
- source baseline commit
- source path
- Part
- chapter
- section
- topic
- ALP ID(s)

A source update must be auditable by comparing the pinned baseline with a later commit. Updating the source baseline requires an explicit reviewed migration; it is independent from updating authoring or QA rules.

## 7. Pilot baseline and ongoing rule evolution

ANKI-PILOT-001〜006 established the initial v1.0 production baseline using 40 corrected Notes / 62 generated cards with 0 accounting failures, 0 source-traceability failures, 0 major findings, and 0 blocking findings.

That gate authorized Phase C generation, but v1.0 is now treated as a **historical baseline rather than a permanent semantic freeze**.

After full production begins:

1. audit real generated Notes and rendered cards;
2. record ambiguity, omission, overload, leakage, accounting, or efficiency failures;
3. update the authoritative specification, `rules/anki_card_rules.md`, or schema when the policy itself should improve;
4. update validators when the rule can be checked mechanically;
5. explicitly migrate affected production batches when required;
6. preserve historical reproducibility through Git history, issues/PRs, QA records, compatibility paths, and migration scripts.

See `GOVERNANCE.md`. `FREEZE.md` records the historical v1.0 gate only.

## 8. Quality dimensions

Each note is independently assessed for:

- **Accuracy**: accounting content is correct.
- **Coverage**: it maps to necessary ALPs and materially preserves required source content.
- **Atomicity / coherence**: integration does not create unrelated retrieval tasks.
- **Prompt sufficiency**: context makes the retrieval target unambiguous after masking.
- **Recall value**: the cloze tests knowledge rather than trivial completion.
- **Non-leakage**: visible text does not give away the hidden answer.
- **Non-duplication**: it adds a distinct retrieval target.
- **Traceability**: source mapping and lineage are complete.
- **Rule currency**: it satisfies `rules/anki_card_rules.md` for new work, or an explicitly documented earlier audited state for historical batches not yet migrated.

## 9. Persistent lineage invariants

Unless an explicit repository-wide migration changes them:

- stable Note IDs are immutable after assignment;
- deprecated/deleted IDs are not reused for unrelated content;
- canonical ALP/source mappings remain auditable;
- approved production Notes retain deterministic serialization;
- existing batches retain their pinned source fields until an explicit source-baseline migration.

These are lineage/reproducibility invariants, not a freeze on improving deck-design rules.

## 10. Output

Canonical editable data is stored in repository text files. APKG is an export artifact, not the source of truth.

Planned outputs:

- structured topic inventory
- canonical Cloze note dataset
- QA reports
- TSV/CSV import representation
- APKG export

## 11. CPA continuity

The deck should create durable bookkeeping foundations for later CPA study. This affects card quality and terminology, but the current deck remains source-bounded to `textbook.md`. CPA-only content must not be counted as bookkeeping coverage.
