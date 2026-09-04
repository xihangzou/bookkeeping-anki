# IND-02 Production QA

Issue: **ANKI-025 / #26**  
Chapter: **Industrial 02 — 材料費**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/IND-02.tsv`

## Result

- production Notes: **24**
- generated cards: **24**
- Cloze spans: **48**
- included ALPs: **29**
- mapped included ALPs: **29**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **5**
- journal-entry primary Notes: **3**
- formula Notes: **5**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No IND-02 production Note IDs existed before ANKI-025. IDs are allocated deterministically in primary canonical ALP order as `BK-IND-02-0001`–`BK-IND-02-0024`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The canonical inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Coherent multi-ALP Notes are used only when one retrieval frame naturally represents related rules without duplicating review:

- `BK-IND-02-0003`: general material journal flow plus direct/indirect consumption entry (`0003`, `0017`)
- `BK-IND-02-0005`: major materials and purchased parts as the two standard direct-material categories (`0005`, `0006`)
- `BK-IND-02-0010`: external and internal material incidental costs (`0011`, `0012`)
- `BK-IND-02-0018`: perpetual/periodic inventory-method difference plus the physical-count requirement (`0021`, `0022`)
- `BK-IND-02-0019`: normal versus abnormal inventory-loss treatment (`0023`, `0024`)

The worked numerical examples remain excluded as `DECORATIVE_EXAMPLE` because they only substitute numbers into active purchase, consumption, inventory, pricing, and variance rules.

## Recall-design review

### Minimal lexical scope and visible context

The batch follows the consolidated current rules:

- canonical accounting labels are retrieved directly where label identification is useful;
- formulas keep arithmetic operators visible and Cloze individual operands only;
- journal-entry debit/credit syntax remains visible while target account names are Clozed at account level;
- broad action answers such as `仕訳を行う`, `仕訳を行わない`, `処理する`, `計上する`, and abstract `あり` / `なし` are not used;
- same-index grouping hides tightly coupled answers together where visible siblings would leak the relation;
- each generated card retains enough visible subject/context to identify the required accounting answer class.

### Material asset-to-cost flow and classification

The opening Notes retrieve the transition from `材料` as an asset to `材料費` on consumption and preserve the stock-flow identity `月初材料＋当月購入＝当月消費＋月末材料` with atomic operands.

Direct versus indirect material cost is tested by the actual decision criterion: whether consumption can be identified by specific product. Major materials and purchased parts are grouped as the standard direct-material categories, while auxiliary materials, factory supplies, and consumable tools/equipment are tested as indirect materials.

### Purchase cost and incidental costs

Purchase cost is represented as `購入代価＋材料副費`. The purchase-entry Note keeps the debit-side material frame visible and retrieves `買掛金` and `現金` as the relevant credit accounts for the stated transaction. Returns/discounts retrieve the reversing `買掛金` account while keeping the material credit visible.

External and internal material incidental costs are distinguished by where they arise in the material flow. The mandatory inclusion of external incidental costs remains visible, while internal-cost inclusion retrieves the three permitted scope choices: exclude, partially include, or fully include.

Planned incidental-cost allocation retrieves the `予定配賦率`, and the resulting difference from actual incidence retrieves the canonical label `材料副費配賦差異`.

### Material consumption, inventory records, and loss

Material consumption preserves the atomic formula `材料消費単価×材料消費数量`. The integrated journal Note retrieves `仕掛品` for direct material and `製造間接費` for indirect material without hiding debit/credit syntax.

The ledger/method Notes distinguish `材料元帳`, `継続記録法`, and the periodic-inventory calculation. The method comparison explicitly retrieves which method can identify inventory shrinkage independently and retains the rule that physical counting is required under both methods.

Normal inventory shrinkage is retrieved as `製造間接費` (indirect expense), while abnormal fire/theft losses are kept outside manufacturing cost and retrieved as `営業外費用` or `特別損失`.

### Consumption pricing and planned price variance

FIFO is retrieved from its cost-flow assumption. Weighted-average pricing keeps division visible and retrieves only `合計原価` and `合計数量` as operands.

The planned-price section retrieves `予定消費単価（予定消費価格）`, preserves `予定材料消費額＝実際消費数量×予定消費単価`, and tests the price-variance relationship `予定消費額－実際消費額` plus year-end allocation to `売上原価`. The favorable/adverse direction remains explanatory context in `Extra` rather than creating a redundant second retrieval operation.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/IND-02.tsv`.

## Deterministic validator

`scripts/validate_ind02_production.py` checks:

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
- account-level journal-entry masking / rejection of whole-entry Clozes
- formula/operator atomicity and required precision forms
- cost-accounting treatment anchors for inventory loss
- exact canonical exclusion family

Expected output:

```text
IND-02 production validation: PASS
notes=24 cards=24 cloze_spans=48 included_alps=29 mapped=29 unmapped=0
multi_alp_notes=5 journal_entry_notes=3 formula_notes=5 canonical_exclusions=1
account_level_journal_cloze=pass minimal_cloze_scope=pass formula_atomicity=pass cost_accounting_treatment=pass visible_answer_leakage=0 deterministic_order=pass
```
