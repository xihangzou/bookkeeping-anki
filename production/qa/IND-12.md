# IND-12 Production QA

Issue: **ANKI-035 / #36**  
Chapter: **Industrial 12 — 直接原価計算**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/IND-12.tsv`

## Result

- production Notes: **16**
- generated cards: **16**
- Cloze spans: **51**
- included ALPs: **20**
- mapped included ALPs: **20**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **3**
- formula Notes: **9**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- arithmetic operators hidden inside formula Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No IND-12 production Note IDs existed before ANKI-035. IDs are allocated deterministically in primary canonical ALP order as `BK-IND-12-0001`–`BK-IND-12-0016`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The inventory shard remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Coherent multi-ALP Notes are used only where one retrieval frame avoids semantic duplication:

- `BK-IND-12-0001`: full costing, direct costing, and the fixed-manufacturing-cost distinction (`0001`, `0002`, `0006`)
- `BK-IND-12-0013`: operating-profit reconciliation and the identical fixed-cost-adjustment formula (`0015`, `0019`)
- `BK-IND-12-0015`: fixed-cost-adjustment definition and public-reporting necessity (`0017`, `0018`)

The worked Case Study and Example 12-1 remain excluded as `DECORATIVE_EXAMPLE` because they are numerical applications of relationships already retrieved by the active formula and procedure Notes.

## Recall-design review

### Direct versus full costing

The comparison Note keeps the accounting nouns visible where they already identify the retrieval frame. Following review feedback, `BK-IND-12-0001` masks only `すべての` in the full-costing branch and `のみ` in the direct-costing branch instead of masking the broader phrases `すべての製造原価` and `変動製造原価のみ`. The fixed-manufacturing-cost and period-cost treatment remains actively retrieved. Repeated `期間原価` occurrences share `c1` so visible sibling text cannot reveal the answer.

Product cost and period cost are tested separately through the timing distinction: inventory deferral until sale versus full expense recognition in the period incurred.

### Income-statement structure

The direct-costing sequence retrieves variable/fixed classification, contribution profit, and operating profit without turning broad action clauses into answers. Formula Notes keep arithmetic operators visible and mask individual operands.

The full-costing two-stage profit relation is kept on one same-index card because `売上総利益` is both the output of the first equation and an input to the second; masking every occurrence prevents sibling-answer leakage.

### Fixed manufacturing cost and fixed-cost adjustment

The batch separately retrieves:

- expense timing under full versus direct costing;
- the fixed-manufacturing-cost expense relation;
- operating-profit reconciliation;
- the equivalent operating-profit difference formula;
- why fixed-cost adjustment is required for public reporting; and
- the operational rule to add ending-inventory fixed manufacturing cost and subtract beginning-inventory fixed manufacturing cost.

Following review feedback, formula Notes `BK-IND-12-0012`–`0014` keep shared formula descriptors such as `固定製造費用化額`, `営業利益`, and `に含まれる製造固定費` visible and mask only the discriminating operands: `直接原価計算`, `期首棚卸資産`, and `期末棚卸資産`. This preserves the formula relationship while reducing lexical Cloze scope.

`ALP-IND-12-0015` and `ALP-IND-12-0019` are intentionally mapped to the same Note because they state the same quantitative relationship in different section contexts. Creating separate active Notes would create a semantic duplicate.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/IND-12.tsv`.

## Deterministic validator

`scripts/validate_ind12_production.py` checks:

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
- regression rejection for the reviewed over-broad IND-12 targets
- parallel `・`-joined answer rejection
- formula/operator atomicity
- direct-costing formula precision
- fixed-cost-adjustment direction and reconciliation precision
- exact canonical exclusion family

Expected output:

```text
IND-12 production validation: PASS
notes=16 cards=16 cloze_spans=51 included_alps=20 mapped=20 unmapped=0
multi_alp_notes=3 formula_notes=9 canonical_exclusions=1
direct_costing_logic=pass fixed_cost_adjustment=pass formula_atomicity=pass minimal_cloze_scope=pass visible_answer_leakage=0 deterministic_order=pass
```

## Implementation commits

- `8864b80ed9bc158f8bf2f40b3d1583bf143f4197` — add `production/notes/IND-12.tsv`
- `d2c8cbb4cdb5f6d266702a423917fbc7bde53347` — add `scripts/validate_ind12_production.py`
- `a991e9faf4ff40790b0069d495f8a928728e05b5` — refine reviewed Cloze spans in `IND-12.tsv`
- `6d8510d712b88232d70a3a2d87a29d2fbdd331e7` — tighten chapter validator against regression to the reviewed broad targets
