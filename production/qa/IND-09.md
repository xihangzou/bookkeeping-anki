# IND-09 Production QA

Issue: **ANKI-032 / #33**  
Chapter: **Industrial 09 — その他の総合原価計算**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/IND-09.tsv`

## Result

- production Notes: **14**
- generated cards: **14**
- Cloze spans: **27**
- included ALPs: **19**
- mapped included ALPs: **19**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **4**
- journal-entry primary Notes: **0**
- formula Notes: **3**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No IND-09 production Note IDs existed before ANKI-032. IDs are allocated deterministically in primary canonical ALP order as `BK-IND-09-0001`–`BK-IND-09-0014`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The canonical inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Coherent multi-ALP Notes are used only when the propositions belong to one retrieval frame:

- `BK-IND-09-0002`: cumulative method and prior-process-cost terminology (`0002`, `0003`)
- `BK-IND-09-0003`: cumulative two-stage cost flow plus prior-process-cost allocation basis (`0004`, `0005`)
- `BK-IND-09-0006`: group-direct/group-indirect classification plus the resulting group-costing procedure (`0008`, `0009`, `0010`)
- `BK-IND-09-0008`: conceptual contrast between the debit-side focus of group costing and credit-side focus of grade costing (`0012`, `0019`)

The worked numerical examples 9-1 through 9-3 remain excluded as `DECORATIVE_EXAMPLE`. Their numerical substitutions do not add a retrieval operation beyond the active method, allocation, and formula Notes.

## Recall-design review

### Process-stage costing

The first four Notes distinguish process-stage costing, cumulative costing, and prior-process cost. The cumulative-flow Note retrieves the transferred `前工程費`, the second-stage `加工費`, and the `実在量` allocation basis in one cost-flow frame. All repeated occurrences of `前工程費` are hidden together to prevent visible-answer leakage.

The per-process WIP-method Note uses separate same-index spans for `先入先出法` and `平均法`, satisfying the current parallel-term atomicity rule while keeping them on one coherent card.

### Group process costing

The group-costing definition is separate from the treatment mechanics. The integrated treatment Note distinguishes `組直接費` from `組間接費` using the actual traceability criterion and keeps direct assignment / indirect allocation visible. It then retrieves the resulting `当月投入原価` before each group proceeds to ordinary process costing.

The classification exception is preserved separately: direct/indirect grouping is not fixed by the account label itself, but by whether the cost can be directly traced to each group product.

### Group versus grade costing

`BK-IND-09-0008` directly compares the two conceptual locations in the Work in Process account: group costing focuses on the `借方` side because it aggregates current-period input cost by product group, while grade costing focuses on the `貸方` side because it allocates aggregate completed-product cost across grades. Same-index grouping prevents one side from revealing the other.

### Grade costing and formulas

The grade-costing definition and `等価係数` definition remain separate retrieval units. Formula Notes keep operators visible and Cloze individual operands only:

- `積数＝生産量×等価係数`
- each grade's completed cost uses `完成品総合原価`, its `積数`, and `積数合計`
- unit cost uses the grade's `完成品原価` and `生産量`

The procedure Note is distinct from the formula Notes because it tests ordered method execution: determine aggregate completed cost, calculate weighted units, allocate by weighted-unit ratio, then derive unit cost.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/IND-09.tsv`.

## Deterministic validator

`scripts/validate_ind09_production.py` checks:

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
- formula/operator atomicity and required precision forms
- parallel-term atomicity for the process-method pair
- process/group/grade cost-accounting anchors
- exact canonical exclusion family

Expected output:

```text
IND-09 production validation: PASS
notes=14 cards=14 cloze_spans=27 included_alps=19 mapped=19 unmapped=0
multi_alp_notes=4 journal_entry_notes=0 formula_notes=3 canonical_exclusions=1
minimal_cloze_scope=pass formula_atomicity=pass cost_accounting_flow=pass visible_answer_leakage=0 deterministic_order=pass
```
