# Anki Deck Specification

Status: **v0.9 (pilot validation pending)**

## 1. Scope

The deck covers the complete content of:

- `xihangzou/bookkeeping-integrated/merged/textbook.md`
- baseline commit `569ed7b82e729334e1472286eaca7c4352e6fbdb`

Scope equals bookkeeping levels 2 and 3 as integrated in that textbook, including:

- Part 0 簿記の基礎
- Part I 商業簿記
- Part II 工業簿記

No chapter is excluded merely because it is advanced relative to level 3.

## 2. Mastery definition

"100% mastery" means every necessary learning point in the source textbook is represented by enough recall prompts to reproduce the knowledge required for correct reasoning, journal entries, calculations, procedures, comparisons, and exceptions.

It does **not** mean every sentence or example must become a card.

A deck is complete only when:

1. every source section has been reviewed;
2. every included Atomic Learning Point has one or more mapped notes;
3. every excluded source unit has an explicit exclusion reason;
4. all journal entries and calculations have passed accounting QA;
5. all notes have passed Cloze QA;
6. there are no unresolved duplicate or conflicting notes.

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
- Default target: 1-3 cloze groups per note.
- A note may create several cards only when the masked facts are independently worth recalling.
- Closely coupled facts that should be recalled together may share the same cloze number.
- `Extra` explains reasoning, common errors, derivation, or source nuance; it must not become a substitute for recalling the answer.

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
- inability to explain an important accounting relationship.

Exclude or merge:

- rhetorical introductions;
- exact repetition;
- paraphrases with no additional condition;
- decorative examples whose only change is arbitrary numbers;
- facts already fully recalled by another note unless a different retrieval context is genuinely useful.

See `rules/coverage_rules.md`.

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

A source update must be auditable by comparing the pinned baseline with a later commit.

## 7. Pilot gate

Before full production:

1. generate 30-50 representative notes from Part 0 and early commercial bookkeeping;
2. include definitions, classifications, journal entries, formula/procedure, comparison, and reasoning cards;
3. review actual Anki rendering and recall quality;
4. record failure patterns;
5. revise rules from v0.9 to v1.0 once;
6. freeze v1.0 before chapter-wide generation.

## 8. Quality dimensions

Each note is independently assessed for:

- **Accuracy**: accounting content is correct.
- **Coverage**: it maps to a necessary ALP.
- **Atomicity**: it is not overloaded.
- **Prompt sufficiency**: context makes the retrieval target unambiguous.
- **Recall value**: the cloze tests knowledge rather than reading comprehension or trivial completion.
- **Non-duplication**: it adds a distinct retrieval target.
- **Traceability**: source mapping is complete.

## 9. Output

Canonical editable data is stored in repository text files. APKG is an export artifact, not the source of truth.

Planned outputs:

- structured topic inventory
- canonical Cloze note dataset
- QA reports
- TSV/CSV import representation
- APKG export

## 10. CPA continuity

The deck should create durable bookkeeping foundations for later CPA study. This affects card quality and terminology, but the current deck remains source-bounded to `textbook.md`. CPA-only content must not be counted as bookkeeping coverage.
