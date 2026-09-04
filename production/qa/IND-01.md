# IND-01 Production QA

Issue: **ANKI-024 / #25**  
Chapter: **Industrial 01 — 工業簿記の基礎**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/IND-01.tsv`

## Result

- production Notes: **23**
- generated cards: **23**
- Cloze spans: **58**
- included ALPs: **30**
- mapped included ALPs: **30**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **4**
- formula Notes: **4**
- cost-accounting primary Notes: **3**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No IND-01 production Note IDs existed before ANKI-024. IDs are allocated deterministically in primary canonical ALP order as `BK-IND-01-0001`–`BK-IND-01-0023`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The ANKI-003 inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Coherent multi-ALP Notes are used only where one retrieval frame naturally represents related propositions without duplicating review:

- `BK-IND-01-0009`:発生形態別3区分と材料費・労務費・経費の定義 (`0009`–`0012`)
- `BK-IND-01-0012`: 直接費の賦課と間接費の配賦 (`0015`, `0016`)
- `BK-IND-01-0015`: 操業度別分類と変動費・固定費の定義 (`0019`–`0021`)
- `BK-IND-01-0018`: 工業簿記の主要勘定体系と一連の原価フロー (`0024`, `0030`)

The worked numerical example remains excluded as `DECORATIVE_EXAMPLE` because it is number substitution for relationships already retrieved by the active classification and formula Notes.

## Recall-design review

### Definitions and classifications

The batch retrieves canonical labels only when the visible description identifies a unique accounting concept. Material/ labor/ expense classification is integrated into one same-card frame, as are variable/fixed cost definitions, so sibling answers do not create separate trivial cards.

Direct and indirect manufacturing cost Notes keep the defining criterion visible and Cloze the canonical category and component names. `賦課` and `配賦` are contrasted in one retrieval frame because the distinction is treatment-changing and the two procedures are inseparable.

### Formula atomicity

Formula Notes keep operators visible and mask individual operands only:

- `総原価＝製造原価＋販売費及び一般管理費`
- `利益＝売上高－総原価`
- `製造原価＝材料費＋労務費＋経費＝製造直接費＋製造間接費`
- `販売価格＝総原価＋利益`

No whole-expression Cloze is used.

### Cost-accounting flow

The end-to-end ledger Note retrieves account names at account level: material/labor/expense cost elements, direct-cost transfer to work in process, overhead collection and allocation to work in process, completion into finished goods, and sale into cost of goods sold.

The three costing stages are then retrieved separately as `費目別計算 → 部門別計算 → 製品別計算`, followed by stage-specific destination rules and the production-form choice between `個別原価計算` and `総合原価計算`.

The canonical IND-01 shard contains no standalone `journal_entry` ALP. Accordingly, no redundant transaction-by-transaction journal-entry Note is invented outside the inventory. The chapter's entry mechanics represented by the canonical shard are covered through the account-level ledger/cost-flow Notes; the validator still rejects compact whole-entry Clozes if debit/credit syntax is introduced later.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/IND-01.tsv`.

## Deterministic validator

`scripts/validate_ind01_production.py` checks:

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
- account-level journal-entry masking if debit/credit syntax appears
- formula/operator atomicity
- required cost-classification and cost-flow precision forms
- exact canonical exclusion family

Expected output:

```text
IND-01 production validation: PASS
notes=23 cards=23 cloze_spans=58 included_alps=30 mapped=30 unmapped=0
multi_alp_notes=4 formula_notes=4 cost_accounting_notes=3 canonical_exclusions=1
cost_flow=pass formula_atomicity=pass account_level_masking=pass minimal_cloze_scope=pass visible_answer_leakage=0 deterministic_order=pass
```

## Initial implementation commits

- `7ae8a64c72c940e99a94eaff2a907ffd20db0306` — add `production/notes/IND-01.tsv`
- `7015f190beac4639278e11cfc5f144107153256e` — add `scripts/validate_ind01_production.py`
