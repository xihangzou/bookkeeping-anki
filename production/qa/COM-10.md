# COM-10 Production QA

Issue: **ANKI-017 / #18**  
Chapter: **Commercial 10 — 株式会社会計**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/COM-10.tsv`

## Result

- production Notes: **31**
- generated cards: **31**
- Cloze spans: **89**
- included ALPs: **34**
- mapped included ALPs: **34**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **3**
- journal-entry primary Notes: **9**
- formula Notes: **6**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No COM-10 production Note IDs existed before ANKI-017. IDs are allocated deterministically in primary canonical ALP order as `BK-COM-10-0001`–`BK-COM-10-0031`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The ANKI-003 inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Coherent multi-ALP Notes are used only where one recall frame naturally represents related rules without duplicating review:

- `BK-COM-10-0001`: corporation funding fundamentals and shareholder limited liability (`0001`, `0002`)
- `BK-COM-10-0011`: issuance-cost account selection and the timing-based stock-issuance-cost comparison (`0012`, `0013`)
- `BK-COM-10-0024`: legal-reserve threshold rule and its equivalent minimum formula (`0026`, `0027`)

The canonical numerical worked-example row remains excluded as `DECORATIVE_EXAMPLE` because it adds no retrieval operation beyond the active formulas, conditions, journal mechanics, and classifications.

## Recall-design review

### Minimal lexical scope and visible context

The batch follows the current consolidated recall rules:

- canonical account names, classification labels, short condition discriminators, and atomic formula operands are the recall targets;
- retrieval subjects and treatment-changing conditions remain visible;
- broad answers such as `仕訳を行う`, `仕訳を行わない`, and `処理する` are not used;
- debit/credit syntax and arithmetic operators remain visible;
- formula operands are masked individually rather than hiding whole expressions;
- numerical examples support source evidence rather than generating redundant cards.

### Corporation and equity structure

The opening Notes preserve the hierarchy needed for later corporate accounting: stock issuance and limited liability, the net-assets equation, the split between stockholders' equity and valuation/translation adjustments, the three major stockholders' equity components, and their reserve/subcomponent structure. `その他有価証券評価差額金` is retrieved as `評価・換算差額等`, distinct from `株主資本`.

### Share issuance and capital-increase procedure

The default issuance rule retrieves `資本金` while keeping the receipt account and journal syntax visible. The company-law minimum-capital rule separately retrieves the `1/2以上` threshold and `資本準備金` treatment.

During a capital increase, the application-period entry uses account-level Clozes:

`（借）{{c1::別段預金}}／（貸）{{c1::株式申込証拠金}}`

At the payment date, the Note preserves both required reclassifications: special deposit to an ordinary bank account, and stock-subscription deposits to capital stock / capital reserve.

### Issuance-related costs

Timing remains visible and the canonical accounts are the answers: `創立費` at formation, `開業費` after formation but before operations, and `株式交付費` for a later capital increase. The same Note also preserves the material comparison that a stock-issuance cost changes account according to whether it arises at formation or during a capital increase.

### Stockholders' equity reclassification and deficit

The batch retrieves the `元手` versus `利益剰余金` separation and the general prohibition on crossing those categories, followed by the two source-defined exceptions. Net-loss closing and deficit elimination use account-level journal Clozes with debit/credit syntax visible. The financial-statement Note separately retrieves `借方残高`, `欠損`, and `マイナス` presentation.

### Dividends and legal reserves

The dividend section keeps distribution versus retention distinct, then tests the dividend-total formula with atomic operands. Declaration/payment, profit-source legal-reserve accumulation, voluntary-reserve accumulation/reversal, and other-capital-surplus dividends use account-level Clozes.

The legal-reserve requirement is compressed into the source-equivalent formula:

`必要準備金積立額＝min（{{c1::配当金}}×{{c1::1/10}}, {{c1::資本金}}×{{c1::1/4}}－{{c1::既存準備金合計}}）`

For mixed funding sources, separate atomic operands preserve proportional allocation to `利益準備金` and `資本準備金` without adding number-substitution cards.

### Merger accounting

The merger Notes retain the accounting sequence needed to solve entries: the surviving company receives the disappearing company's assets/liabilities and pays merger consideration; accepted assets/liabilities are recognized at merger-date `時価`; consideration is reflected through `現金` or `資本金` as applicable.

Formula Notes separately retrieve:

`受入純資産額＝{{c1::受入資産時価}}－{{c1::受入負債時価}}`

`のれん＝{{c1::合併対価}}－{{c1::受入純資産額}}`

Goodwill is retrieved as an `無形固定資産`, amortized over at most `20年`, with `のれん償却` as expense. When consideration is below net assets received, the difference is retrieved as `負ののれん発生益` and `収益`.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/COM-10.tsv`.

## Deterministic validator

`scripts/validate_com10_production.py` checks:

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
- exact canonical exclusion family

Expected output:

```text
COM-10 production validation: PASS
notes=31 cards=31 cloze_spans=89 included_alps=34 mapped=34 unmapped=0
multi_alp_notes=3 journal_entry_notes=9 formula_notes=6 canonical_exclusions=1
account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass formula_atomicity=pass visible_answer_leakage=0 deterministic_order=pass
```
