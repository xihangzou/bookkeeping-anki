# COM-09 Production QA

Issue: **ANKI-016 / #17**  
Chapter: **Commercial 09 — 引当金**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/COM-09.tsv`

## Result

- production Notes: **22**
- generated cards: **22**
- Cloze spans: **55**
- included ALPs: **30**
- mapped included ALPs: **30**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **8**
- journal-entry primary Notes: **9**
- formula Notes: **4**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No COM-09 production Note IDs existed before ANKI-016. IDs are allocated deterministically in primary canonical ALP order as `BK-COM-09-0001`–`BK-COM-09-0022`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The ANKI-003 inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Coherent multi-ALP Notes are used only where one recall frame naturally represents related rules without duplicating review:

- `BK-COM-09-0001`: provision recognition principle and later utilization (`0001`, `0002`)
- `BK-COM-09-0002`: provision taxonomy and the chapter's concrete classification (`0003`, `0004`)
- `BK-COM-09-0012`: pooled/individual evaluation selection plus exclusion-and-combination workflow (`0014`, `0016`)
- `BK-COM-09-0014`: nontrade-receivable allowance scope and exam scope-selection rule (`0017`, `0018`)
- `BK-COM-09-0015`: repair-provision recognition and utilization (`0019`, `0020`)
- `BK-COM-09-0016`: employee-bonus provision recognition and utilization (`0021`, `0023`)
- `BK-COM-09-0020`: retirement-benefit matching rationale and utilization (`0026`, `0027`)
- `BK-COM-09-0021`: product-warranty provision recognition and utilization (`0028`, `0029`)

The canonical numerical worked-example row remains excluded as `DECORATIVE_EXAMPLE` because it adds no retrieval operation beyond the active formulas, conditions, and journal mechanics.

## Recall-design review

### Minimal lexical scope and visible context

The batch follows the current consolidated recall rules:

- canonical account names, classification labels, method labels, short process discriminators, and atomic formula operands are the recall targets;
- retrieval subjects and treatment-changing conditions remain visible;
- broad answers such as `仕訳を行う`, `仕訳を行わない`, and `処理する` are not used;
- debit/credit syntax and arithmetic operators remain visible;
- fixed timing/relational modifiers such as `期末の`, `決算整理前の`, `担保の`, `保証による`, `当期の`, and `賞与計算期間の` remain outside the Cloze where they identify an operand role;
- numerical examples are supporting source evidence rather than separate active cards.

### General provision principle and classification

The opening Notes retain the two decisions needed for the rest of the chapter:

- a future expense whose cause belongs to the current/prior period is recognized in the current period and the provision is later utilized;
- an `評価性引当金` is an asset contra item, while a `負債性引当金` is a liability;
- `貸倒引当金` is the chapter's evaluation allowance, while repair, bonus, director bonus, retirement benefit, and product warranty provisions are liability provisions.

### Bad-debt timing and journal mechanics

Current-period and prior-period receivables are separated because the available allowance differs:

- current-period credit-sale receivable bad debt: `（借）{{c1::貸倒損失}}／（貸）{{c1::売掛金}}`;
- prior-period credit-sale receivable bad debt: first `（借）{{c1::貸倒引当金}}／（貸）{{c1::売掛金}}`, with only the excess charged to `{{c1::貸倒損失}}`;
- recovery of a previously written-off receivable credits `{{c1::償却債権取立益}}`.

Debit/credit syntax remains visible and no whole-entry Cloze is used.

### Allowance formulas and difference method

Operators remain visible and accounting quantities are separately masked:

`貸倒見積高＝期末の{{c1::対象債権残高}}×{{c1::貸倒実績率}}`

`貸倒引当金繰入＝{{c1::貸倒見積高}}－決算整理前の{{c1::貸倒引当金残高}}`

The estimate-versus-realized-loss distinction is separately tested through the expense account `貸倒引当金繰入`. If the pre-adjustment allowance exceeds the required estimate, the account-level reversal is:

`（借）{{c1::貸倒引当金}}／（貸）{{c1::貸倒引当金戻入}}`

The financial-statement distinction remains explicit: the income statement reports the period's allowance expense, while the balance sheet deducts the post-adjustment allowance balance; the two normally differ under the difference method.

### Pooled and individual evaluation

The method-selection Note keeps the condition visible and retrieves the canonical labels `一括評価` and `個別評価`. It also preserves the anti-double-counting workflow: individual-evaluation receivables are removed from the pooled population and the two estimates are combined.

The individual-evaluation formula uses minimal operands with relational modifiers visible:

`貸倒見積高＝（{{c1::債権残高}}－担保の{{c1::処分見込額}}－保証による{{c1::回収見込額}}）×{{c1::設定率}}`

### Nontrade receivables

The batch preserves that loans and other nontrade receivables can also require a bad-debt allowance. Because exam scope depends on the problem, the active retrieval rule is to use `問題文の指示` together with account balances rather than assuming only trade receivables are included.

### Liability-provision lifecycle

Repair, employee bonus, director bonus, retirement benefit, and product warranty Notes use the same accounting architecture without collapsing distinct account names:

- recognize the current-period cause with an account-level expense/provision entry;
- utilize the provision when the future payment occurs;
- where the source specifies it, charge any amount exceeding the provision balance to the payment-period expense.

This lifecycle integration reduces duplicate cards while preserving the distinct ALP propositions in active `Text`.

### Bonus calculation and provision/accrual distinction

Bonus-provision measurement is kept as an atomic formula:

`賞与引当金＝翌期支給の{{c1::賞与見積額}}×当期の{{c1::経過月数}}÷賞与計算期間の{{c1::月数}}`

The classification distinction is separately retrieved: estimated, not-yet-fixed future payments use `引当金`, while fixed amounts use `未払費用`.

### Manufactured-product warranty exception

For self-manufactured products, the condition remains visible and the account-name discriminators are retrieved as `製品保証費` and `製品保証引当金`, rather than the corresponding `商品` accounts.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/COM-09.tsv`.

## Deterministic validator

`scripts/validate_com09_production.py` checks:

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
COM-09 production validation: PASS
notes=22 cards=22 cloze_spans=55 included_alps=30 mapped=30 unmapped=0
multi_alp_notes=8 journal_entry_notes=9 formula_notes=4 canonical_exclusions=1
account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass formula_atomicity=pass visible_answer_leakage=0 deterministic_order=pass
```
