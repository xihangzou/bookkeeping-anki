# IND-07 Production QA

Issue: **ANKI-030 / #31**  
Chapter: **Industrial 07 — 個別原価計算**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/IND-07.tsv`

## Result

- production Notes: **15**
- generated cards: **15**
- Cloze spans: **30**
- included ALPs: **18**
- mapped included ALPs: **18**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **3**
- journal-entry primary Notes: **3**
- formula Notes: **0** (no canonical IND-07 formula ALP)
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No IND-07 production Note IDs existed before ANKI-030. IDs are allocated deterministically in primary canonical ALP order as `BK-IND-07-0001`–`BK-IND-07-0015`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The canonical inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Coherent multi-ALP Notes are used only when one retrieval frame naturally represents related rules without duplicating review:

- `BK-IND-07-0004`: `原価計算票` and the `原価元帳` formed by filing those sheets (`0004`, `0005`)
- `BK-IND-07-0006`: direct assignment `賦課（直課）` versus indirect-cost `配賦計算` (`0007`, `0008`)
- `BK-IND-07-0014`: direct-expense spoilage treatment and the Level-2 exam-scope boundary (`0016`, `0018`)

The worked numerical examples remain excluded as `DECORATIVE_EXAMPLE` because they only instantiate the active job-costing and spoilage rules with concrete numbers.

## Recall-design review

### Minimal lexical scope and visible context

The batch follows the consolidated current rules:

- canonical accounting labels are retrieved directly where label identification is useful;
- journal-entry debit/credit syntax remains visible while target account names are Clozed at account level;
- parallel terms such as simple versus departmental job costing, spoilage terminology, and department allocation elements use separate atomic Cloze spans;
- broad action answers such as `仕訳を行う`, `処理する`, `振り替える`, and `賦課する` are not used as Cloze answers;
- same-index grouping hides tightly coupled answers together where visible siblings would leak the relation;
- each generated card retains enough visible subject/context to identify the required accounting answer class.

### Job-order costing documents and ledgers

The opening Notes retrieve the purpose of `個別原価計算`, the role of the `特定製造指図書`, and the distinction between `単純個別原価計算` and `部門別個別原価計算`.

`原価計算票` is tested as the instruction-specific cost sheet collecting direct materials, direct labour, and manufacturing overhead. Its filed accumulation is retrieved as the `原価元帳`, while the monthly aggregate reconciling to Work in Process is separately retrieved as `原価計算表（総括表）`.

### Assignment, allocation, and job-costing procedures

Direct manufacturing costs are retrieved through `賦課（直課）`; manufacturing overhead that cannot be traced directly is retrieved through `配賦計算`. The simple job-costing Note then tests the operational pair of job-specific direct-cost assignment and a factory-wide `単一配賦率` for overhead.

Departmental job costing remains a separate procedure Note and retrieves the department-specific `配賦率` and `配賦基準` used after overhead is accumulated by department.

### Completion and sale cost flow

Completion of a production order is represented as an account-level journal unit:

`（借）製品／（貸）仕掛品`

while unfinished orders remain in `仕掛品`.

For completed and delivered orders, the second journal unit retrieves:

`（借）売上原価／（貸）製品`

while completed but undelivered orders remain in `製品`. Repeated occurrences of `仕掛品` or `製品` use the same `c1` so visible text cannot leak the target account.

### Spoilage and repair-cost flow

The terminology Note distinguishes `仕損`, `仕損品`, and `仕損費` with separate atomic spans. Repair activity retrieves `補修指図書`, and normal spoilage cost is assigned to the `当初の製造指図書` as manufacturing cost.

The Level-2 scope Note retrieves `直接経費処理` and keeps the two-stage treatment visible: repair-order cost is first transferred to spoilage cost and then directly charged to the original production order.

The dedicated journal Note tests the account flow at account level:

1. `（借）仕損費／（貸）仕掛品`
2. `（借）仕掛品／（貸）仕損費`

No whole-entry Cloze is used.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/IND-07.tsv`.

## Deterministic validator

`scripts/validate_ind07_production.py` checks:

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
- chapter-specific completion, sale, and spoilage cost-flow anchors
- absence of invented formula Notes where the canonical shard has no formula ALP
- exact canonical exclusion family

Expected output:

```text
IND-07 production validation: PASS
notes=15 cards=15 cloze_spans=30 included_alps=18 mapped=18 unmapped=0
multi_alp_notes=3 journal_entry_notes=3 formula_notes=0 canonical_exclusions=1
account_level_journal_cloze=pass minimal_cloze_scope=pass formula_atomicity=not_applicable cost_accounting_treatment=pass visible_answer_leakage=0 deterministic_order=pass
```
