# COM-07 Production QA

Issue: **ANKI-014 / #15**  
Chapter: **Commercial 07 — 無形資産**  
Rules: current living `SPEC.md`, `rules/*.md`, and `rules/recall_precision_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/COM-07.tsv`

## Result

- production Notes: **14**
- generated cards: **14**
- Cloze spans: **27**
- included ALPs: **19**
- mapped included ALPs: **19**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **4**
- journal-entry primary Notes: **3**
- formula Notes: **1**
- canonical exclusions: **2** (`DUPLICATE_EXACT` 1, `DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No COM-07 production Note IDs existed before ANKI-014. IDs are allocated deterministically in primary canonical ALP order as `BK-COM-07-0001`–`BK-COM-07-0014`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The ANKI-003 inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Coherent multi-ALP Notes are used only where one recall frame naturally represents the related rules without duplicating review:

- `BK-COM-07-0006`: residual-value / amortization-method rule, rationale, and direct-versus-indirect recording distinction (`0006`, `0010`, `0011`)
- `BK-COM-07-0010`: software purpose classification plus the market-sale scope boundary (`0012`, `0013`)
- `BK-COM-07-0011`: internal-use capitalization condition plus the exam assumption for purchased software (`0014`, `0015`)
- `BK-COM-07-0013`: software-in-progress treatment plus completion/delivery transfer (`0017`, `0018`)

The canonical exclusion rows remain excluded: the repeated R&D POINT is `DUPLICATE_EXACT`, and simple numerical acquisition/amortization examples are `DECORATIVE_EXAMPLE`.

## Recall-design review

### Minimal lexical scope

The batch follows the current recall-precision specializations:

- definitions expose the descriptive cue and Cloze the canonical accounting label;
- recognition cards target exact accounts, conditions, or measurement terms rather than broad action phrases;
- fixed contextual words remain visible when they already identify the answer class;
- explanatory rationale is kept visible where it makes a method choice uniquely recoverable;
- numerical worked examples remain outside active recall.

### Research and development

The chapter opens with two distinct retrieval units:

- the labels `研究開発` and `研究開発費`;
- the recognition rule that R&D expenditure, including assets acquired for R&D purposes, is expensed at occurrence through `研究開発費`.

The repeated POINT is not duplicated as another active card.

### Intangible-asset amortization

The core method/rationale Note keeps the accounting frame visible and targets the short discriminators:

- residual value `ゼロ`;
- `定額法`;
- `直接法`;
- tangible fixed assets: `間接法` in principle.

The annual formula keeps its operator visible:

`無形固定資産の年額償却費＝{{c1::取得原価}}÷{{c1::有効期間}}（残存価額ゼロ）`

Partial-year amortization separately targets `月割`, because timing is an independent exam-useful rule.

### Journal entries

Debit/credit syntax remains visible and account names are Clozed at account level with the same `c1` for each coherent entry.

Representative forms:

- purchased internal-use software: `（借）{{c1::ソフトウェア}}／（貸）現金等`
- commissioned software before completion: `（借）{{c1::ソフトウェア仮勘定}}／（貸）現金等`
- completion transfer: `（借）{{c1::ソフトウェア}}／（貸）{{c1::ソフトウェア仮勘定}}・現金等`
- amortization: `（借）{{c1::ソフトウェア償却}}／（貸）{{c1::ソフトウェア}}`

For the integrated commissioning Note, both occurrences of `ソフトウェア仮勘定` are hidden so the visible card does not leak the answer.

### Software classification and capitalization

Purpose classification remains visible as one accounting frame: research-development, internal-use, and market-sale. The active targets are the treatment-changing results:

- R&D purpose -> `研究開発費`;
- market-sale purpose -> bookkeeping Level 2 `範囲外`.

For internal-use software, `収益獲得` and `費用削減` are the short capitalization-condition discriminators. The exam assumption that purchased software satisfies the condition remains explicit active Text rather than being moved only to `Extra`.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/COM-07.tsv`.

## Deterministic validator

`scripts/validate_com07_production.py` checks:

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
- account-level journal-entry Clozes
- formula/operator atomicity and required precision forms
- exact canonical exclusion families

Expected output:

```text
COM-07 production validation: PASS
notes=14 cards=14 cloze_spans=27 included_alps=19 mapped=19 unmapped=0
multi_alp_notes=4 journal_entry_notes=3 formula_notes=1 canonical_exclusions=2
account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass formula_atomicity=pass visible_answer_leakage=0 deterministic_order=pass
```
