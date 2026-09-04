# COM-12 Production QA

Issue: **ANKI-019 / #20**  
Chapter: **Commercial 12 — 税・税効果会計**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/COM-12.tsv`

## Result

- production Notes: **31**
- generated cards: **31**
- Cloze spans: **71**
- included ALPs: **34**
- mapped included ALPs: **34**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **2**
- journal-entry primary Notes: **11**
- formula Notes: **5**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No COM-12 production Note IDs existed before ANKI-019. IDs are allocated deterministically in primary canonical ALP order as `BK-COM-12-0001`–`BK-COM-12-0031`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The canonical inventory itself remains unchanged: `note_ids` stays empty and `qa_status` stays `pending`.

Coherent multi-ALP Notes are used only where one retrieval frame is materially better than separate cards:

- `BK-COM-12-0001`: taxes/revenue stamps versus postage-stamp account selection (`0001`, `0002`)
- `BK-COM-12-0013`: the four add/deduct tax-adjustment branches (`0014`, `0015`, `0016`)

The numerical examples remain excluded as `DECORATIVE_EXAMPLE`; the active Notes preserve the underlying account selection, journal mechanics, formulas, reversal logic, and exceptions without memorizing arbitrary example numbers.

## Recall-design review

### Basic taxes and consumption tax

The batch retrieves `租税公課` versus `通信費`, the period-end transfer of unused stamps to `貯蔵品`, and the next-period reversal. The paired stamp/revenue-stamp journal entries remain one `c1` retrieval unit because splitting the four account positions would duplicate the same adjustment frame and allow counterpart leakage.

Corporate-tax Notes distinguish interim payment (`仮払法人税等`), year-end recognition of `法人税、住民税及び事業税`, the `未払法人税等` residual formula, and settlement in the following period without a new tax expense.

Consumption-tax Notes distinguish `仮払消費税` from `仮受消費税`, preserve the payable formula with visible subtraction, and test the closing entry that nets both temporary accounts into `未払消費税`.

### Taxable income and tax adjustments

The accounting/tax comparison keeps the two calculation frames parallel: accounting uses `収益－費用`, while tax uses `益金－損金`. The taxable-income reconciliation keeps operators visible and masks the individual operands `税引前当期純利益`, `加算調整`, and `減算調整`.

The four tax-adjustment cases are intentionally grouped under one `c1` so visible sibling answers cannot reveal the direction: 損金不算入→加算、損金算入→減算、益金不算入→減算、益金算入→加算. The later reversal Note similarly hides both sides of the add/deduct reversal pair together.

`一時差異` versus `永久差異`, tax-effect applicability, and typical temporary-difference sources are kept as separate retrieval units because definition, scope, and example classification are distinct judgments.

### Tax-effect accounting

The objective Note retrieves `法人税等調整額` as the mechanism that aligns pretax profit with tax expense by period. A separate Note makes the cash distinction explicit: tax-effect accounting adjusts the income-statement tax amount, not the actual tax payment.

`繰延税金資産` and `繰延税金負債` are tested by future tax effect. The tax-effect formula keeps multiplication visible and masks only `一時差異` and `法定実効税率`.

Recognition and reversal entries keep debit/credit syntax visible and Cloze account names only. The asset-side and liability-side reversal entries stay in one `c1` retrieval unit because showing one account occurrence would otherwise leak the paired reversal pattern.

Balance-sheet presentation is separately tested as `相殺` plus `純額` display while preserving that the two deferred-tax accounts remain separate in the ledger.

### Other securities

The batch distinguishes accounting fair-value treatment from the tax rule that does not fair-value other securities, establishing the temporary difference. The direct-equity exception retrieves `法人税等調整額` as the account that is not used.

For valuation gains, the tax portion is retrieved as `繰延税金負債` and the remainder as `その他有価証券評価差額金`. For valuation losses, the tax portion is `繰延税金資産` and the after-tax remainder reduces `その他有価証券評価差額金`. The security account itself stays visible where it is the retrieval subject, avoiding a contextless self-referential Cloze.

The after-tax formula preserves the relationship `評価差額 × (1－法定実効税率)` with operators visible and also identifies the resulting pure-equity account. The following-period reversal retrieves the canonical `洗替方式` label.

## Accounting / calculation checks

Checked against the pinned chapter source:

- unused stamp/revenue-stamp closing and reopening entries
- interim, year-end, and settlement corporate-tax treatment
- consumption-tax net payable and closing entry
- taxable-income reconciliation and all four adjustment directions
- temporary-difference reversal direction
- deferred-tax asset/liability recognition and reversal entries
- deferred-tax balance-sheet netting
- other-securities gain/loss deferred-tax entries
- after-tax valuation-difference formula
- wash-method reversal

No arithmetic operator is hidden inside a Cloze answer, no prompt-copied arbitrary example amount is made an active recall target, and all journal-entry Clozes preserve visible debit/credit syntax.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/COM-12.tsv`.

## Deterministic validator

`scripts/validate_com12_production.py` checks:

- exact field order and deterministic stable IDs
- pinned source provenance
- Part/Chapter/primary Section consistency
- required deterministic tags and lifecycle
- `c1`-only generation
- exact deterministic Note-to-ALP mapping and exact-once INCLUDE-ALP coverage
- canonical inventory immutability
- local duplicate rendered text
- visible-answer leakage
- broad/non-atomic Cloze answers
- account-level journal-entry masking whenever debit/credit syntax appears
- formula/operator atomicity and required precision forms
- exact canonical exclusion family

Expected output:

```text
COM-12 production validation: PASS
notes=31 cards=31 cloze_spans=71 included_alps=34 mapped=34 unmapped=0
multi_alp_notes=2 journal_entry_notes=11 formula_notes=5 canonical_exclusions=1
account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass formula_atomicity=pass visible_answer_leakage=0 deterministic_order=pass
```
