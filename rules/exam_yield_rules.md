# Exam-Yield / Active-Deck Rules

Status: **v1.2 post-freeze overlay — ANKI-AUDIT-001/002 (#56, #58)**

This file is an explicit post-freeze migration layered on top of the frozen v1.0 contract in `SPEC.md`, `rules/cloze_rules.md`, `rules/coverage_rules.md`, and `schema/note_schema.yaml`.

The v1.0 source/schema/stable-ID contract remains authoritative unless this overlay explicitly changes active-deck selection, lifecycle handling, or generated-card efficiency.

## 1. Target

The canonical inventory remains source-complete, but the **active approved deck is exam-weighted and retrieval-efficient**.

A source proposition does not automatically deserve its own direct Cloze card. Direct recall is retained when omission could materially cause:

1. wrong account selection or five-element classification;
2. wrong debit/credit direction;
3. wrong recognition timing;
4. wrong journal entry or settlement treatment;
5. wrong amount, formula, valuation, or calculation;
6. wrong ledger / voucher procedure that can be directly tested;
7. failure to discriminate similar treatments, methods, or documents;
8. failure to apply an exception or condition;
9. inability to parse terminology or notation that is routinely required by bookkeeping exam questions;
10. loss of a causal accounting relationship needed for later 2級 / CPA reasoning.

Note count and generated-card count are not quotas. The target is the smallest active corpus that preserves all necessary exam-relevant retrieval operations and full canonical ALP traceability.

## 2. Low-yield direct recall

Do **not** keep an independent active card merely because a proposition is accurate or present in the source.

Prefer consolidation, visible context, or deprecation when the proposed card mainly tests:

- introductory/background description;
- obvious stakeholder-label association;
- a general rule already tested by a more complete accounting rule;
- pure left/right or label naming already embedded in a debit-credit decision card;
- long lists of form fields or account examples without a decision;
- terminology that is useful only as supporting context and is naturally encountered in a higher-yield card;
- a procedural sequence already subsumed by a more complete sequence;
- a definition duplicated by an application/contrast card with equal or greater retrieval value.

Low exam importance alone is not a reason to delete source traceability. The ALP should normally be mapped to a coherent higher-yield approved Note.

## 3. Consolidation test

Multiple ALPs should map to one approved Note when all of the following hold:

- they form one accounting decision or retrieval unit;
- the combined Note remains understandable with its Clozes hidden;
- the generated cards do not require unrelated simultaneous judgments;
- consolidation removes duplicate or low-yield direct recall;
- every ALP remains individually traceable through `ALP_IDs`.

Examples:

- debit/credit left-right terminology + normal-balance/increase rule -> one five-element debit-credit Note;
- bookkeeping transaction definition + positive/negative boundary cases -> one recognition Note;
- trial-balance definition + purpose + debit-credit equality -> one trial-balance control Note;
- journal/general-ledger definitions -> one time-order vs account-order comparison Note;
- individual/aggregate posting + aggregation tables + subsidiary-ledger exception -> one posting-workflow Note.

## 4. Deprecated lifecycle

A superseded production Note is retained as an auditable row with:

- the same immutable `ID`;
- its historical ALP mapping retained;
- `Status=deprecated`;
- `QA=pass` when the retirement decision itself has passed audit;
- the mechanically corresponding `status::deprecated` tag.

Deprecated Notes:

- are not active-deck coverage;
- are not exported as study cards;
- do not satisfy an ALP's active coverage requirement by themselves;
- must never have their IDs reused.

Every included ALP must map to at least one **approved** Note. For a normalized chapter batch, one approved Note per ALP is preferred; one approved Note may cover several ALPs.

## 5. Exam-yield rewrite preference

When a low-yield Note contains material worth retaining, redesign in this order:

1. accounting decision / classification;
2. contrast between confusable treatments;
3. journal-entry or settlement consequence;
4. recognition condition;
5. calculation or formula application;
6. exam-document interpretation;
7. concise terminology recall only when terminology itself is necessary to parse questions.

Do not turn a low-yield list into a larger memorization list. Keep representative examples and make the selection principle visible.

## 6. Accuracy override

If a source-derived simplification is potentially misleading in a broader bookkeeping context, the production Note must use the most precise source-consistent wording that remains valid for later learning.

In particular, transaction duality must not be phrased as though **each** account in a compound entry changes by the same amount. The durable rule is that a transaction is recorded on debit and credit sides and the total debit amount equals the total credit amount.

## 7. FND-00 v1.1 audit target

For ANKI-AUDIT-001:

- retain all 91 canonical FND-00 ALPs as active-source coverage targets;
- retain all assigned production Note IDs as immutable audit history;
- reduce independent approved Notes where direct recall is redundant or low-yield;
- preserve exactly one approved mapping for every included FND-00 ALP;
- allow approved multi-ALP Notes;
- keep deprecated rows in `production/notes/FND-00.tsv` but exclude them from active export;
- prioritize debit-credit rules, transaction recognition, trial-balance controls, payroll/temporary-account entries, correction entries, ledger reconciliation, voucher decisions, and document-to-entry inference.

The resulting approved-note count is an audit outcome, not a quota.

## 8. Generated-card rotation efficiency — v1.2

ANKI-AUDIT-002 adds a generated-card-level optimization layer. A Cloze Note with `c1`, `c2`, and `c3` creates three review cards even when the three facts belong to one natural retrieval unit. Therefore **distinct Cloze indices are a study-cost decision**.

For every approved Note:

1. start from **one generated card** (`c1`) for one coherent retrieval unit;
2. reuse the same Cloze index for tightly coupled facts that should be recalled together;
3. add `c2+` only when the additional card tests a materially independent retrieval operation worth a separate review;
4. do not create additional cards merely because a sentence contains several blanks;
5. count distinct Cloze indices as part of chapter QA and report the generated-card total.

Same-index grouping is normally preferred for:

- paired debit/credit treatments;
- two sides of one classification contrast;
- parallel formulas that should be reproduced as a set;
- ordered stages whose sequence is the target;
- vocabulary bundles needed together to parse one exam construct;
- paired journal-entry consequences that constitute one accounting decision;
- mutually dependent document or voucher classifications.

Separate indices remain appropriate when hiding everything together would overload recall or when each group supports a genuinely independent exam decision. The reason should be apparent from the Note or QA record.

## 9. Cloze answer uniqueness and standalone form — v1.2

A Cloze span should be a **canonical answer unit**, not a grammatical residue.

Prefer answers such as:

- `資産`, `負債`, `純資産`;
- `借方`, `貸方`;
- `合計試算表`, `残高試算表`;
- `所得税預り金`;
- `補助記入帳`, `補助元帳`;
- a complete formula or short self-contained proposition.

Avoid targets such as:

- `運用形態` when the accounting category itself can be tested;
- `ある調達源泉` / `ない調達源泉`;
- `増減するか`;
- `発見できない` without identifying what cannot detect the error;
- fragments whose grammatical form admits several plausible completions.

When a source proposition is better tested in reverse, keep the condition or definition visible and Cloze the canonical accounting term. The intended semantic answer class must be unique from the visible prompt.

Each exact Cloze answer span should appear at most once within an approved Note. If identical answer text would be hidden twice, redesign the sentence or keep one occurrence visible unless repetition itself is materially necessary.

## 10. Visible-context rule — v1.2

Supporting facts that are useful for understanding but do not deserve another review card should remain visible in the Note or `Extra`.

Visible context should:

- identify the subject, period, transaction direction, and comparison axis needed to determine the answer;
- prevent multiple accounting-equivalent interpretations;
- avoid revealing a hidden answer through a visible sibling fact;
- let the learner know what *kind* of answer is required without making the answer automatic.

The objective is not maximal masking. It is **minimal sufficient masking for durable retrieval**.

## 11. FND-00 v1.2 rotation target

For ANKI-AUDIT-002, after v1.1 active-deck selection:

- historical rows remain **91**;
- approved Notes remain **57** and deprecated rows remain **34**;
- 91/91 included ALPs remain mapped exactly once to an approved Note;
- generated cards are reduced from **110 to 58**;
- all approved Notes use one generated card except `BK-FND-00-0091`, which uses two coherent abbreviation-family cards;
- no approved Note contains a duplicated exact Cloze answer span;
- Cloze wording is revised toward canonical accounting terms, short formulas, directions, or self-contained propositions.

Apply these v1.2 rules during ANKI-008 onward generation so generated-card efficiency is designed in from the start rather than repaired after chapter generation.
