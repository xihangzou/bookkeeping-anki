# Anki Card Rules

Status: **Sole authoritative Anki card-design, coverage, active-deck, and recall rule set — living specification**  
Governance: `GOVERNANCE.md`  
Migration: **ANKI-GOV-002 / #98**

This document consolidates and supersedes the current-rule content previously distributed across:

- `rules/cloze_rules.md`
- `rules/coverage_rules.md`
- `rules/exam_yield_rules.md`
- `rules/recall_precision_rules.md`

Those paths are retained only as compatibility/history pointers. They are not independent current authorities.

Historical audit and pilot states remain reproducible through Git history, issues, PRs, QA reports, and `FREEZE.md`. The current merged version of this file governs all newly authored Notes and every batch explicitly migrated to current rules.

---

## 1. Objective and precedence

Anki Cloze Notes are retrieval prompts for accurate accounting knowledge, not generic fill-in-the-blank exercises.

Priorities, in order:

1. the learner can tell exactly what must be recalled;
2. the correct answer is unique or materially unique;
3. the target has accounting/exam value;
4. the prompt preserves understanding needed for later bookkeeping/CPA study;
5. the answer is no broader than necessary;
6. review cost is compressed without losing source coverage;
7. repeated review still requires meaningful retrieval rather than mechanical cue association.

This file must be applied together with:

- `SPEC.md`;
- `schema/note_schema.yaml`;
- the pinned source baseline and canonical ALP inventory;
- chapter-local QA/validators where an explicitly migrated batch has stricter audited requirements.

When a historical rule conflicts with this document, this document wins for current work. Stable-ID, source-traceability, deterministic-serialization, and lineage invariants remain governed by `GOVERNANCE.md`.

---

## 2. Coverage target

Coverage target is the complete meaning of `bookkeeping-integrated/merged/textbook.md`, not a target card count.

### 2.1 Inventory-stage coverage

A source passage is inventory-covered when every testable or conceptually necessary candidate proposition is classified as either:

- `INCLUDE`: assigned a stable ALP ID, canonical primary type, inclusion reason, and source traceability; or
- `EXCLUDE`: assigned one canonical exclusion reason.

At inventory stage, included ALPs may have empty `note_ids` and `qa_status=pending`.

### 2.2 Final-deck coverage

Final coverage requires:

- every included ALP mapped to one or more valid approved production Notes; and
- every excluded candidate retaining a defensible canonical exclusion.

Coverage does **not** require one Note/card per ALP. Multiple ALPs may map to one coherent retrieval unit.

### 2.3 Mandatory inclusion test

Include an ALP if omitting it could reasonably cause:

1. wrong account selection;
2. wrong debit/credit side;
3. wrong recognition timing;
4. wrong amount/valuation;
5. wrong journal entry;
6. wrong cost flow/allocation;
7. wrong ledger/closing procedure;
8. wrong financial-statement presentation;
9. confusion between materially different methods;
10. a missed condition/exception;
11. inability to reconstruct a core accounting relationship.

### 2.4 Conditional inclusion

Include only when it adds retrieval value:

- examples;
- alternative wording;
- background/history;
- implementation detail;
- long numerical demonstrations;
- form/layout details.

A numerical example deserves active recall only if it introduces a new decision, branch, calculation step, compound entry, boundary condition, common error, or materially different application. Mere number substitution is normally excluded.

### 2.5 Canonical exclusion reasons

Use only:

- `DUPLICATE_EXACT`
- `DUPLICATE_SEMANTIC`
- `PARAPHRASE_ONLY`
- `RHETORICAL_CONTEXT`
- `DECORATIVE_EXAMPLE`
- `DERIVABLE_TRIVIAL`
- `OUTSIDE_RECALL_GOAL`

Never use vague reasons such as `not important`.

---

## 3. Canonical ALP types

Every included ALP receives one primary type from the schema:

| Type | Primary retrieval target |
|---|---|
| `definition` | distinct accounting meaning/name |
| `classification` | category, five-element classification, statement placement |
| `recognition` | timing or recognition condition |
| `measurement` | valuation/amount determination |
| `journal_entry` | debit/credit accounting treatment |
| `formula` | quantitative relationship |
| `procedure` | ordered process/workflow |
| `comparison` | distinction between methods/accounts/treatments |
| `exception` | condition changing the general rule |
| `reasoning` | causal understanding needed to prevent confusion |
| `ledger` | posting/bookkeeping mechanics |
| `financial_statement` | presentation/statement relationship |
| `cost_accounting` | industrial-bookkeeping cost-flow logic |

Secondary characteristics belong in tags. Do not create ad-hoc primary types.

---

## 4. Integration-first architecture

Default: **1 Note = 1 coherent recall unit**.

A coherent unit may contain multiple ALPs only when they belong to the same retrieval frame and separating them would either:

- destroy the accounting relationship;
- create sibling answer leakage;
- duplicate the same retrieval operation;
- split an inseparable comparison, procedure, formula family, or journal unit.

Integration is a compression mechanism, not permission to drop source meaning.

For every mapped ALP, active `Text` must materially preserve the proposition that makes that ALP distinct. `Extra` may explain or disambiguate, but may not be the only place where a mapped ALP survives.

If adding an ALP creates a second unrelated judgment task, split the Note.

---

## 5. Essential-recall test

A production Note should earn review time by testing at least one of:

- account selection or journal mechanics;
- recognition timing;
- treatment-changing classification;
- formula/measurement relationship;
- method/document discrimination needed to solve questions;
- material exception/condition;
- ledger/process mechanics that must be reproduced;
- cost-flow logic.

Do not create a Cloze merely because a sentence contains terminology. Move nonessential examples, explanatory tails, and repeated teaching prose to `Extra` or exclude them when they add no retrieval operation.

---

## 6. Cloze semantics and numbering

Different Cloze indices normally generate different cards. Repeated occurrences of the same index are hidden together.

### 6.1 Default card count

Prefer **1–3 Cloze groups per Note**. More groups are justified only when the retrieval unit itself requires them, such as an ordered sequence or tightly coupled structure.

Do not introduce `c2+` merely to create more cards.

### 6.2 Same-index grouping

Use the same index when facts should be recalled as one unit, especially when:

- showing one member would substantially reveal another;
- paired relations are inseparable;
- one coherent journal entry contains multiple target accounts;
- comparison branches share a relation and separate cards would leak sibling answers;
- parallel formulas would expose each other's operands/operations;
- repeated occurrences of the same answer must all be hidden to prevent leakage.

### 6.3 Different indices

Use different indices only if each generated card independently satisfies all of:

1. sibling visible answers do not make the target trivial;
2. the hidden member has independent retrieval value;
3. grammar/layout/parallel position does not determine the answer;
4. the proposition is not already duplicated elsewhere.

### 6.4 Retrieval-load and semantic chunking

Same-index grouping prevents leakage; it does **not** justify bulk recall. A generated card should not require the learner to reproduce a long, weakly structured list or nearly every step of a workflow merely because all spans share one index.

When several independently meaningful items must be covered:

- keep a semantic cue, category, condition, or role visible for each answer where possible;
- chunk the items into coherent subgroups with different Cloze indices or separate Notes/cards when the subgroups have independent retrieval value;
- for long workflows, keep routine steps visible and test only sequence-critical transitions, named stages, exceptions, or outputs unless reproducing the full sequence is itself essential.

Prefer cue-based discrimination over raw “name all items” recitation. If simultaneous recall of all items is structurally necessary, document that rationale in chapter QA.

---

## 7. Context sufficiency and retrieval-subject visibility

After all target spans on a generated card are hidden, the learner must still know exactly what accounting subject and answer class are being tested.

Bad:

`{{c1::買掛金}}`

Preferred:

`商品を掛けで仕入れたとき、代金の支払義務は{{c1::買掛金}}として処理する。`

Do not mechanically Cloze every accounting term. If a term is the subject/object/frame needed to identify the question, keep it visible.

Before approval, hide all target spans and ask:

> Can the learner still identify exactly what must be recalled?

If not, restore the retrieval subject to visible context.

Placeholder answers such as `適切な勘定科目`, `本来の科目`, or `正しい処理` are unacceptable unless visible facts uniquely determine their semantic answer.

---

## 8. Canonical answer precision and minimal lexical scope

A Cloze answer must be the **smallest uniquely recoverable accounting unit**.

Preferred targets:

- account name;
- technical term;
- recognition point;
- method/document name;
- formula operand;
- short treatment discriminator;
- short operator/direction where that itself is tested.

Avoid whole explanatory clauses, broad actions, or compound labels when a shorter discriminator is uniquely recoverable.

Preferred:

- `手形の{{c1::裏書}}`
- `不一致原因が{{c1::当社}}側にある場合…`
- `改定償却額＝切替時の{{c1::期首帳簿価額}}×{{c1::改定償却率}}`

Avoid:

- `{{c1::手形の裏書}}` when `手形の` is already visible and redundant;
- `{{c1::当社側の修正項目}}`;
- `{{c1::切替時の期首帳簿価額}}` when `切替時の` can remain visible.

Broad action answers are normally forbidden:

- `{{c1::仕訳を行う}}`
- `{{c1::仕訳を行わない}}`
- `{{c1::処理する}}`
- long action clauses.

If operation/direction itself has independent value, use a short exact target such as `{{c1::加算}}`, `{{c1::減算}}`, `{{c1::借方}}`, or `{{c1::貸方}}`.

### 8.1 Context-qualified atomicity

Minimal lexical scope does **not** mean reducing an answer to a context-free fragment. A short Cloze is unacceptable when its meaning depends on a treatment-changing qualifier that is neither inside the answer nor uniquely supplied by visible text.

In particular:

- avoid abstract presence/absence answers such as `{{c1::あり}}` or `{{c1::なし}}` when the useful knowledge is the accounting treatment itself;
- avoid a bare rate, method, or shorthand such as `{{c1::HR}}`, `{{c1::FR}}`, or `{{c1::CR}}` when the actual retrieval target is **which timing/role uses that rate** and sibling contexts could use the same abbreviation;
- when timing, source, destination, or role is the discriminating accounting fact, include that qualifier in the answer or make it explicitly visible in the prompt;
- a short consequence such as `{{c1::不要}}` is acceptable only when the visible frame uniquely specifies what is unnecessary and under what condition.

Preferred:

- `手付金外貨額×{{c1::手付金授受時HR}}＋残額外貨額×{{c1::商品受渡時HR}}`
- `取引後に為替予約した場合、取引発生時の換算レート＝{{c1::HR}}、予約時の換算レート＝{{c1::FR}}。`

Avoid:

- two bare `{{c1::HR}}` answers where the learner must distinguish different applicable dates;
- `為替差損益は{{c1::あり}}／{{c1::なし}}` when the treatment can be stated and tested more precisely elsewhere.

The governing test is semantic: the answer must be atomic **and** self-identifying within its visible retrieval frame.

### 8.2 Canonical-label priority

When visible facts map one-to-one to a named accounting concept, prefer the canonical label when identifying that label is the useful retrieval operation.

Example:

`売上認識が出荷時なら{{c1::出荷基準}}、到着時なら{{c1::着荷基準}}、検収時なら{{c1::検収基準}}。`

Do not reverse every definition mechanically. If timing, amount, or treatment is more exam-useful than the label, test that instead.

### 8.3 Parallel-term atomicity

When two or more **independently meaningful parallel terms** appear in one list or compound phrase, put each term in its own Cloze span rather than hiding the whole parallel phrase as one answer. This applies especially to terms joined by `・`, `／`, `、`, `and`, or `or`.

If the terms belong to one coherent retrieval unit, they may use the same Cloze index so they are hidden together; separate spans enforce lexical atomicity and do **not** by themselves require separate cards.

Preferred:

`{{c1::利益管理}}・{{c1::原価管理}}`

Avoid:

`{{c1::利益管理・原価管理}}`

Do not split a fixed canonical technical term merely because it contains a conjunction or separator. For example, `販売費及び一般管理費` remains one answer when that full canonical account/category label is the retrieval target.

---

## 9. Journal-entry rules

### 9.1 Current production rule: Cloze account names, not the whole tuple

For ordinary newly authored or explicitly re-audited journal entries:

- keep debit/credit labels visible;
- keep separators visible;
- keep prompt-copied amounts visible;
- Cloze each target account name separately;
- use the same `c1` when the entry is one coherent retrieval unit.

Preferred:

`（借）{{c1::売掛金}}／（貸）{{c1::売上}}`

`（借）{{c1::買掛金}}／（貸）{{c1::仕入}}`

Avoid:

`{{c1::（借）売掛金／（貸）売上}}`

The older compact-whole-entry exception is historical and is **retired** for new/re-audited production Notes.

If the same target account appears multiple times in one integrated procedure, hide every occurrence with the same index so visible text cannot leak it.

### 9.2 Debit/credit direction

Cloze `借方`/`貸方` only when direction itself is the learning target. Otherwise leave the labels visible and test account selection.

### 9.3 Amounts

Do not Cloze amounts copied directly from the prompt. Cloze an amount only when calculation, allocation, measurement, difference, tax, interest, depreciation, or another quantitative relation is itself the target.

### 9.4 Compound entries

A large entry may remain one same-index retrieval unit when splitting it would create counterpart leakage or destroy the accounting pattern. If four or more account positions are involved, explicitly verify that safe decomposition is impossible or inferior.

---

## 10. Formula and calculation rules

Keep arithmetic operators visible and Cloze **individual operands**, not a whole expression.

Preferred:

`当期純利益＝{{c1::収益}}－{{c1::費用}}`

`純売上高＝{{c1::総売上高}}－{{c1::売上戻り高}}`

Avoid:

`当期純利益＝{{c1::収益－費用}}`

When a timing/relational modifier already uniquely fixes an operand's role, keep the modifier visible:

`改定償却額＝切替時の{{c1::期首帳簿価額}}×{{c1::改定償却率}}`

Repeated same-answer same-index spans are permitted where a formula family structurally reuses the same term and every occurrence must be hidden to prevent leakage.

### 10.1 Selective operand recall

Do not Cloze every operand mechanically. Hide only operands whose identity, role, basis, timing, or direction carries useful retrieval value. An obvious or repeated base amount may remain visible when the nontrivial target is the allocation basis, denominator, timing, or another discriminator.

Preferred:

`月末仕掛品直接材料費＝当月直接材料費×{{c1::月末仕掛品数量}}÷{{c1::当月投入数量}}`

Avoid:

`月末仕掛品直接材料費＝{{c1::当月直接材料費}}×{{c1::月末仕掛品数量}}÷{{c1::当月投入数量}}`

when `当月直接材料費` is not a decision and hiding it only adds recall load.

“Cloze individual operands” means that selected formula targets should be atomic operands rather than a whole expression; it does **not** require every operand to be hidden.

### 10.2 Formula recall vs application

A second card using the same formula needs a materially different retrieval operation, such as:

- numeric calculation;
- condition selection;
- exception;
- multi-step computation;
- method-selection decision;
- boundary case.

Rewording the same formula or changing only numbers is not new coverage.

---

## 11. Type-specific authoring rules

### 11.1 Definition

Leave the descriptive definition visible and Cloze the technical name when name retrieval is useful. Do not hide the entire definition.

### 11.2 Classification

Test distinctions that change accounting understanding/treatment. Avoid mass-producing trivial account-to-five-element association cards when the classification is already materially retrieved in stronger contexts.

### 11.3 Recognition/timing

Keep the accounting subject visible and Cloze the exact timing concept when timing is the target.

### 11.4 Measurement

Test the valuation/amount rule or adopted amount, not mere number substitution.

### 11.5 Procedure

Keep the overall process frame visible. Hide only short sequence-critical labels/discriminators. Do not Cloze a whole long arrow-separated process.

Example:

`前渡→日々の少額支払い→支払内容の{{c1::報告}}→費用仕訳→支払額と同額の{{c1::補給}}`

If multiple steps each require independent recall, split the procedure into accounting-mechanic Notes.

### 11.6 Comparison

Name one comparison axis and keep all branches in the same answer category.

For compound comparison cells, split independent dimensions into separate short spans, normally retaining the same index when the relationship should remain one card.

Preferred:

`売買目的有価証券＝{{c1::時価}}・差額は{{c1::当期損益}}`

Avoid:

`売買目的有価証券＝{{c1::時価・差額は当期損益}}`

### 11.7 Exception/condition

Keep the condition visible and Cloze the consequence/discriminator. Do not hide both condition and result so the learner cannot identify the branch.

### 11.8 Reasoning

Use reasoning Clozes only where causal understanding materially prevents rote confusion or supports later topics.

### 11.9 Ledger

Use for posting, account entry, balance determination, and mechanical bookkeeping processes. If the main target is the journal itself, use `journal_entry`.

### 11.10 Financial statement

Use for statement placement, structure, item relationships, and reporting purpose. Group or split indices based on leakage/retrieval-value rules.

### 11.11 Cost accounting

Use when industrial-bookkeeping cost flow or allocation relationships are the primary retrieval target. Prefer `formula`, `measurement`, or `journal_entry` when one of those more precisely describes the actual target.

---

## 12. Tables, lists, and parallel structures

Do not turn a table mechanically into one Note or one card per cell.

- decompose by the distinctions the learner must retrieve;
- keep column/axis cues visible when they identify the answer class;
- integrate rows that form one comparison;
- split rows that require independent judgments;
- exclude example rows that add no rule.

For parallel classification/comparison cells with multiple meaningful dimensions, Cloze each dimension separately rather than hiding a whole cell. Independently meaningful parallel terms within one dimension must also follow the parallel-term atomicity rule in §8.3.

Long enumerations are additionally subject to retrieval-load chunking in §6.4; parallel-term atomicity alone does not make a many-item list a good card.

---

## 13. Visible-answer leakage and ambiguity QA

A hidden answer must not appear verbatim in visible text on the same generated card.

For generic automated QA, exact visible repetition of an answer of two or more characters is leakage. One-character discriminators remain subject to dedicated contextual review.

For every generated card, check:

- unique semantic answer class;
- sufficient visible subject/context;
- no visible sibling answer that substantially reveals the target;
- no grammar/layout-only guessing;
- no excessively broad or fragmentary answer;
- no context-free boolean/shorthand answer whose meaning depends on an omitted timing, role, method, source, or destination qualifier;
- no same-index group that degenerates into unstructured bulk-list or whole-workflow recitation when semantic chunking is available;
- no cross-Note or sibling-card semantic duplicate;
- no cue that becomes mechanically sufficient after repeated review.

If leakage exists, resolve it by same-index grouping, text redesign, Note split, or removal of a redundant card.

---

## 14. Duplicate control at retrieval-unit level

Deduplicate at **generated-card / retrieval-unit level**, not only Note level.

Process duplicate candidates in this order:

1. exact same retrieval proposition → merge to one retrieval unit;
2. same fact in another context → retain only if the second context changes the retrieval operation;
3. materially different condition/application/exception/decision → keep separate;
4. different wording but same proposition → merge/remove or redesign as a distinct application.

A partial duplicate generated by one Cloze group inside a larger Note is still a duplicate candidate.

ALP coverage does not require duplicated cards. Multiple ALPs may map to one coherent Note.

---

## 15. Active-deck sufficiency and integration

Review/trace **100% of included ALPs**, then reduce review cost primarily by coherent integration rather than aggressive retirement.

Useful foundational vocabulary, classification, journal logic, ledger/document workflow, formulas, notation, and problem-reading concepts may remain active when they integrate cleanly.

Do not retire a useful ALP solely to reach an arbitrary card/span quota.

Conversely, once the learner can retrieve a proposition and apply it across all materially distinct textbook contexts, additional redundant retrieval units are not sufficient/necessary coverage.

---

## 16. Extra field and answer equivalence

`Extra` may contain:

- reasoning;
- calculation derivation;
- journal decomposition;
- common errors;
- related textbook sections;
- short CPA bridge;
- acceptable semantic answer variants.

`Extra` may not substitute for material active-text coverage of mapped ALPs.

Canonical Cloze wording identifies the intended semantic target; it does not automatically require one literal string. Accounting-equivalent answers are acceptable unless exact terminology itself is explicitly the learning target.

---

## 17. Sentence style

Use short declarative Japanese and source/bookkeeping terminology.

- put the accounting subject first;
- explicitly name a method when several methods could fit the same wording;
- keep retrieval-frame terms visible;
- avoid unnecessary parenthetical clutter;
- prefer short canonical answer units;
- do not sacrifice accounting accuracy or ALP completeness for brevity.

FND-00 and COM-01 remain default style references for context-rich, same-card, short-answer production Notes. Later audited chapters provide additional examples but do not create separate rule authority.

---

## 18. Source decomposition and mapping workflow

Process each source section in this order:

1. identify heading path;
2. split prose/tables/examples into semantic blocks;
3. list candidate propositions;
4. merge propositions that form one inseparable rule;
5. classify every candidate as `INCLUDE` or `EXCLUDE`;
6. assign included ALPs stable IDs/types/source traceability;
7. record canonical exclusion reasons for excluded candidates;
8. design coherent production Notes;
9. map each included ALP to Note `ALP_IDs`;
10. validate active-text material proposition, source provenance, duplicates, ambiguity, leakage, and relevant accounting mechanics.

The canonical ANKI-003 inventory is not rewritten merely to record production Note IDs when repository policy keeps that inventory immutable; production mappings may live in Note `ALP_IDs` as established by current chapter workflows.

---

## 19. Coverage and QA metrics

Final/project-level reporting should include at minimum:

```text
source sections reviewed / total
candidate propositions
included ALPs
excluded candidates by reason
ALPs mapped to notes / total ALPs
unmapped ALPs
approved Note count
generated card count
notes with source traceability / total notes
journal-entry QA result
formula/calculation QA result
Cloze/recall QA result
semantic duplicate/orphan counts
```

Completion requires:

- 100% source sections reviewed;
- 100% included ALPs mapped;
- 0 unresolved accounting errors;
- 0 unresolved ambiguous/leaking Clozes;
- 0 unexplained exclusions;
- 0 unresolved exact/semantic retrieval-unit duplicates unless a materially distinct retrieval rationale is recorded;
- deterministic validation and source traceability.

---

## 20. Stable IDs, lifecycle, and lineage

Stable Note IDs are immutable after assignment and are never reused for unrelated content.

Deprecated Notes remain auditable in production history with historical IDs and ALP mappings. Reactivation, if appropriate, stays within the same lineage.

Pinned `SourceRepo`, `SourceCommit`, and `SourcePath` remain stable unless an explicit source-baseline migration is approved.

Current rule changes do not silently rewrite historical metrics or pilot/audit states.

---

## 21. Source updates

The textbook commit is a pinned source baseline. If the source changes:

1. compare old/new source commits;
2. identify changed source blocks;
3. re-run decomposition for affected blocks and dependent Notes;
4. update mappings/QA deterministically;
5. adopt the new source baseline only after review and validation.

Rule evolution and source-baseline evolution are separate migrations.

---

## 22. Historical lineage and resolved supersessions

### 22.1 Historical v1.0 pilot gate

ANKI-PILOT-006 established the initial v1.0 production baseline after the corrected pilot reached:

- 40 Notes / 62 generated cards;
- 0 accounting failures;
- 0 source-traceability failures;
- 0 major findings;
- 0 blocking findings.

`FREEZE.md` records that milestone. Under living-spec governance it is historical evidence, not a permanent semantic freeze.

### 22.2 Production-audit lineage

FND-00 and COM-01 audits established integration-first compression, formula itemization, visible-context rules, and material-proposition containment.

ANKI-AUDIT-008 through ANKI-AUDIT-013 established the current precision rules integrated above, including:

- account-level journal Clozes with debit/credit syntax visible;
- canonical-label priority;
- minimal lexical Cloze scope;
- broad-action-answer prohibition;
- procedure-step precision;
- fixed-head visibility for compound terms;
- decomposition of compound comparison cells;
- minimal formula-operand scope with visible timing/relational modifiers.

Later chapter review generalized additional precision rules:

- context-qualified atomicity: shorthand, boolean, rate, or method answers must remain semantically self-identifying within the visible retrieval frame; treatment-changing timing/role qualifiers cannot be dropped merely to shorten a Cloze;
- parallel-term atomicity: independently meaningful coordinate terms are separate Cloze spans even when they retain the same Cloze index and remain one generated card;
- retrieval-load chunking: same-index grouping does not license unstructured multi-item recall; long lists/workflows should expose semantic cues and test coherent subgroups or key transitions;
- selective formula-operand recall: only operands with useful retrieval value need be hidden; obvious base amounts may remain visible when another basis, role, or timing distinction is the actual target.

### 22.3 Explicit supersession decisions

The following legacy allowances are no longer current for new/re-audited production:

- compact whole-journal-entry Clozes as a normal exception;
- broad explanatory action clauses as answers;
- hiding redundant fixed heads/modifiers inside technical labels/formula operands;
- whole-cell Clozes that combine multiple accounting dimensions;
- treating Note-level uniqueness as sufficient duplicate control;
- treating historical v1.0 as permanently frozen.

Historical examples remain reproducible through Git history and old QA reports.

---

## 23. Rule evolution

When later chapter work or QA reveals a better coverage, integration, wording, Cloze, or recall rule:

1. update this file rather than creating another independent rule overlay;
2. state whether the new rule is repository-wide immediately or applies through explicit chapter migration;
3. update deterministic validators where mechanically checkable;
4. preserve historical metrics as history;
5. validate affected production before merge.

**Do not create a new current rule Markdown that competes with this file.** Extend this document instead.