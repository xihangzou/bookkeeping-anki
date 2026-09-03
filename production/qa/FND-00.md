# FND-00 Production QA

Issues: ANKI-007 / #8; ANKI-AUDIT-001 / #56; ANKI-AUDIT-002 / #58

Contracts:
- frozen v1.0 source/schema baseline (`FREEZE.md`, `rules/cloze_rules.md`, `rules/coverage_rules.md`, `schema/note_schema.yaml`)
- v1.2 post-freeze active-deck / rotation-efficiency overlay (`rules/exam_yield_rules.md`)

## Final batch state

| Metric | ANKI-007 | v1.1 exam-yield audit | v1.2 rotation audit |
|---|---:|---:|---:|
| historical production rows | 91 | 91 | **91** |
| active `approved` Notes | 91 | 57 | **57** |
| `deprecated` audit rows | 0 | 34 | **34** |
| canonical included FND-00 ALPs | 91 | 91 | **91** |
| ALPs mapped to approved Notes | 91 | 91 | **91** |
| active unmapped ALPs | 0 | 0 | **0** |
| approved multi-ALP Notes | 0 | 25 | **25** |
| generated Cloze cards | 91+ | 110 | **58** |
| approved Notes with >1 generated card | many | 43 | **1** |
| stable IDs reused / renumbered | 0 | 0 | **0** |

`BK-FND-00-0016` remains reserved pilot-only evidence and is not used in production.

## v1.1 active-deck audit

ANKI-AUDIT-001 separated **canonical source coverage** from **active direct recall**. Low-yield introductions, duplicated general rules, mechanical label association, long form-field lists, and semantically duplicated definitions were consolidated into higher-yield approved Notes while preserving all 91 canonical ALP mappings.

The 34 deprecated IDs remain immutable audit history:

`BK-FND-00-0001`, `0006`, `0007`, `0020`, `0021`, `0023`, `0031`, `0033`, `0034`, `0035`, `0036`, `0038`, `0040`, `0041`, `0042`, `0045`, `0046`, `0052`, `0056`, `0057`, `0059`, `0060`, `0061`, `0063`, `0065`, `0066`, `0067`, `0076`, `0077`, `0081`, `0082`, `0083`, `0085`, `0087`.

Material v1.1 corrections included:
- transaction duality now tests total debit = total credit rather than implying each account changes by the same amount;
- expense-account recall is transaction-to-account selection rather than a long account-name list;
- debit/credit direction is consolidated into the five-element rule;
- transaction definition and positive/negative recognition cases are one judgment unit;
- trial-balance definition/purpose/equality are consolidated while its detection limitation remains separate;
- payroll, temporary-account, correction-entry, ledger, voucher, and document fragments are consolidated where they form one accounting decision.

## v1.2 objective: rotation efficiency

ANKI-AUDIT-002 audits **generated cards**, not just Note count. A Note containing `c1`, `c2`, and `c3` creates three review rotations even when all blanks belong to one natural recall unit.

Baseline after v1.1:
- 57 approved Notes;
- **110 generated cards**;
- 43 approved Notes generated more than one card.

Final v1.2 state:
- 57 approved Notes;
- **58 generated cards**;
- only `BK-FND-00-0091` generates two cards;
- every other approved Note uses one Cloze index (`c1`).

`BK-FND-00-0091` deliberately retains two groups because:
1. F/S, B/S, P/L, S/S form one financial-statement abbreviation family; and
2. T/B, 前T/B, 後T/B form a separate trial-balance abbreviation family.

Combining those two families into one large card would reduce rotation count by only one while materially increasing answer load, so two cards are retained.

## v1.2 same-index grouping decisions

Same-index grouping is used when multiple blanks should be recalled together as one decision or set, including:
- `得意先 / 仕入先 / 掛け`;
- `仕訳 / 勘定 / 転記`;
- debit/credit paired directions;
- the bookkeeping cycle sequence;
- three trial-balance types;
- expense-account representative selections;
- employee/employer social-insurance treatment;
- 仮払金 / 仮受金 treatment components;
- journal/general-ledger role contrasts;
- `元丁 / 仕丁`;
- subsidiary-book classification;
- three-voucher selection;
- sales/purchase return treatment;
- document classifications;
- document-to-entry evidence cues.

This reduces low-value sibling-card repetition without removing any source coverage.

## Cloze uniqueness / standalone-answer audit

The v1.2 rewrite prefers canonical accounting answer units over grammatical fragments.

Examples:

### Asset / liability / equity

Old retrieval targets in `BK-FND-00-0032` included vague phrases such as `運用形態`, `ある調達源泉`, and `ない調達源泉`.

The revised Note keeps the definitions visible and asks for the canonical categories:
- `資産`;
- `負債`;
- `純資産`.

### Trial-balance types

`BK-FND-00-0010` now keeps the aggregation criterion visible and asks for:
- `合計試算表`;
- `残高試算表`;
- `合計残高試算表`.

This is more uniquely determined than hiding long description fragments.

### Transaction recognition

`BK-FND-00-0037` keeps the recognition criterion visible and contrasts the canonical conclusions `簿記上の取引` / `簿記上の取引ではない`.

### Subsidiary books

`BK-FND-00-0068` now shows the recording axis and asks for `補助記入帳` / `補助元帳`, rather than hiding generic phrases such as `発生順` / `対象別`.

### Source documents

`BK-FND-00-0086` shows what information a document provides and asks for the canonical document names `納品書`, `請求書`, `領収書`, `当座勘定照合表`.

## Answer-span checks

For every approved Note, QA requires:
- nonempty valid Cloze syntax;
- reviewed Cloze-index shape;
- unique semantic answer class from visible context;
- no duplicated exact Cloze answer span inside the Note;
- no known weak v1.1 fragments (`運用形態`, `ある調達源泉`, `ない調達源泉`, `増減するか`, bare `発見できない`);
- no exact rendered-text duplicate across approved Notes.

The validator mechanically enforces all checks that can be made deterministic. Semantic uniqueness / accounting standalone quality was manually reviewed during ANKI-AUDIT-002.

## Reproducible migration

`scripts/migrate_fnd00_v1_2.py` records the reviewed v1.1 → v1.2 Text/index migration. It is idempotent and verifies the resulting shape:
- approved Notes = 57;
- generated cards = 58;
- every approved Note except `BK-FND-00-0091` uses `{c1}`;
- `BK-FND-00-0091` uses `{c1,c2}`.

## v1.2 mechanical validation

GitHub Actions `Validate production notes` passed on PR #59.

```text
FND-00 v1.2 production validation: PASS
rows=91 approved=57 deprecated=34 included_alps=91 approved_mapped=91 unmapped=0
generated_cards=58 multi_card_approved_notes=1 approved_multi_alp_notes=25 reserved_pilot_only_id=BK-FND-00-0016
approved_journal_entry_notes=8 approved_formula_notes=3
```

The validator now enforces:
- complete 91-row stable Note-ID history;
- exact 57 approved / 34 deprecated lifecycle;
- exact reviewed deprecated-ID set;
- source fields, tags, QA status, and canonical ALP ordering;
- 91/91 ALPs mapped exactly once to an approved Note;
- active rendered-text duplicate control;
- **58 generated cards**;
- exact approved Cloze-index shape;
- one and only one multi-card approved Note (`BK-FND-00-0091`);
- no duplicated exact Cloze answer span within approved Notes;
- no reviewed weak/non-standalone v1.1 answer fragments.

## Downstream requirement

ANKI-008 onward should apply v1.2 during initial generation:
1. establish necessary/sufficient active Notes under the exam-yield rule;
2. treat distinct Cloze indices as review-cost decisions;
3. default one coherent Note to one generated card;
4. group coupled facts under the same index;
5. add another card only for a materially independent retrieval operation;
6. prefer canonical standalone accounting answer units over grammatical fragments.

This preserves 100% source coverage while minimizing unnecessary review rotations.
