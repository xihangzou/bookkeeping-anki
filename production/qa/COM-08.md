# COM-08 Production QA

Issue: **ANKI-015 / #16**  
Chapter: **Commercial 08 — リース取引**  
Rules: current living `SPEC.md`, `rules/*.md`, and `rules/recall_precision_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/COM-08.tsv`

## Result

- production Notes: **15**
- generated cards: **15**
- Cloze spans: **36**
- included ALPs: **21**
- mapped included ALPs: **21**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **4**
- journal-entry primary Notes: **4**
- formula Notes: **3**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No COM-08 production Note IDs existed before ANKI-015. IDs are allocated deterministically in primary canonical ALP order as `BK-COM-08-0001`–`BK-COM-08-0015`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The ANKI-003 inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Coherent multi-ALP Notes are used only where one recall frame naturally represents related rules without duplicating review:

- `BK-COM-08-0003`: lease definition plus finance/operating taxonomy (`0003`, `0004`)
- `BK-COM-08-0004`: finance-lease economic substance, operating-lease contrast, and the two practical classification requirements (`0005`, `0006`, `0007`)
- `BK-COM-08-0011`: lease-asset depreciation rule plus interest-included / interest-excluded consequence comparison (`0014`, `0015`, `0016`)
- `BK-COM-08-0013`: general accrual principle plus the finance-lease interest-excluded accrued-interest entry (`0018`, `0019`)

The canonical numerical worked-example row remains excluded as `DECORATIVE_EXAMPLE`.

## Recall-design review

### Minimal lexical scope

The batch follows the current recall-precision specializations:

- account names, method names, classifications, and short formula operands are the primary recall targets;
- debit/credit syntax and arithmetic operators remain visible;
- fixed contextual modifiers remain outside the Cloze when they already determine the role of an operand;
- broad phrases such as “仕訳を行う” or “計上する” are not used as answers;
- numerical worked examples remain outside active recall.

### Ordinary rental groundwork

The first two Notes preserve the accounting distinctions required before lease accounting:

- building rent / land rent: borrower expense accounts versus lessor revenue accounts;
- refundable deposit: `差入保証金` (asset);
- nonrefundable brokerage fee: `支払手数料` (expense).

### Lease classification

The definition/taxonomy Note tests the short core terms `使用権`, `リース料`, `ファイナンス・リース`, and `オペレーティング・リース`.

The classification Note keeps the economic cues visible and asks for the canonical labels. It also tests the two practical finance-lease requirements separately:

- `フルペイアウト`
- `解約不能`

### Finance-lease recognition and methods

The commencement journal entry is account-level:

`（借）{{c1::リース資産}}／（貸）{{c1::リース債務}}`

Method cards use the visible accounting consequences to retrieve the method labels:

- gross carrying amount / all payment against the liability -> `利子込み法`;
- estimated cash purchase price / separate interest -> `利子抜き法`.

### Formula atomicity

All formula operators remain visible and each accounting quantity is a separate same-`c1` answer:

`リース料総額＝{{c1::見積現金購入価額}}＋{{c1::利息相当額}}`

`利子抜き法の年額支払利息＝（{{c1::リース料総額}}－{{c1::見積現金購入価額}}）÷{{c1::リース期間}}`

`利子抜き法のリース債務元本減少額＝{{c1::リース料支払額}}－{{c1::支払利息}}`

### Depreciation and method consequences

The integrated comparison Note tests:

- useful life -> `リース期間`;
- residual value -> `ゼロ`;
- total lease payments capitalized, no separately recognized interest -> `利子込み法`;
- estimated cash purchase price capitalized, interest allocated separately -> `利子抜き法`.

This avoids duplicating the same method contrast across several active cards while preserving all three canonical ALPs.

### Operating lease and accruals

Operating-lease payment treatment is recalled through the expense account:

`（借）{{c1::支払リース料}}／（貸）現金等`

When payment date and reporting date differ:

- finance lease, interest-excluded method: `（借）{{c1::支払利息}}／（貸）{{c1::未払利息}}`;
- finance lease, interest-included method: no accrued interest is recognized;
- operating lease: `（借）{{c1::支払リース料}}／（貸）{{c1::未払リース料}}`.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/COM-08.tsv`.

## Deterministic validator

`scripts/validate_com08_production.py` checks:

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
COM-08 production validation: PASS
notes=15 cards=15 cloze_spans=36 included_alps=21 mapped=21 unmapped=0
multi_alp_notes=4 journal_entry_notes=4 formula_notes=3 canonical_exclusions=1
account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass formula_atomicity=pass visible_answer_leakage=0 deterministic_order=pass
```
