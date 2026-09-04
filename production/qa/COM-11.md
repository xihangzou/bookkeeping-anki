# COM-11 Production QA

Issue: **ANKI-018 / #19**  
Chapter: **Commercial 11 — 外貨建取引**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/COM-11.tsv`

## Result

- production Notes: **17**
- generated cards: **17**
- Cloze spans: **41**
- included ALPs: **21**
- mapped included ALPs: **21**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **4**
- journal-entry primary Notes: **3**
- formula Notes: **2**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No COM-11 production Note IDs existed before ANKI-018. IDs are allocated deterministically in primary canonical ALP order as `BK-COM-11-0001`–`BK-COM-11-0017`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The ANKI-003 inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Coherent multi-ALP Notes are used only where one retrieval frame naturally represents the related rules without duplicating review:

- `BK-COM-11-0008`: payable and receivable settlement-direction rules (`0008`, `0009`)
- `BK-COM-11-0009`: year-end CR remeasurement and its exchange-difference treatment (`0010`, `0011`)
- `BK-COM-11-0012`: foreign-exchange forward definition and FR terminology (`0014`, `0015`)
- `BK-COM-11-0013`: allocation method and the independent-method scope boundary (`0016`, `0017`)

The worked numerical examples remain excluded as `DECORATIVE_EXAMPLE` because they add no retrieval operation beyond the active conversion, settlement, remeasurement, and forward-contract rules.

## Recall-design review

### Minimal lexical scope and visible context

The batch follows the consolidated current rules:

- canonical labels such as `外貨建取引`, `換算`, `為替予約`, `先物為替相場（FR）`, and `振当処理` are retrieved directly;
- rate Clozes target the shortest semantically discriminating unit: a bare `HR`/`FR` is used only when the visible prompt already fixes its accounting role; when the timing itself is the learning target, the timing modifier is included in the answer;
- abstract binary Clozes such as `あり` / `なし` are avoided when a specific rate, account, or accounting treatment can be retrieved instead;
- broad answers such as `仕訳を行う`, `仕訳を行わない`, and `処理する` are not used;
- arithmetic operators remain visible and formula Clozes target atomic operands/rates;
- debit/credit syntax stays visible where journal entries are shown, with account names Clozed individually;
- repeated same-answer spans use the same `c1` so visible siblings cannot leak the answer.

### Initial recognition and advances

The opening Notes distinguish HR and CR, preserve the core conversion formula, and test the initial-recognition rule that ordinary foreign-currency merchandise transactions use transaction-date HR.

Advance-payment treatment keeps the account role and rate timing distinct: the payer records `前払金`, the recipient records `前受金`, and the advance portion continues to use the advance-date HR when the goods are later delivered. The partial-advance formula Note retrieves the timing-specific rate operands `手付金授受時HR` and `商品受渡時HR`, rather than two context-light `HR` answers.

### Settlement and year-end remeasurement

Settlement differences are retrieved as `為替差損益`. The payable/receivable direction Note keeps the economic subject visible while hiding all four gain/loss outcomes together to avoid sibling leakage.

At year-end, remaining foreign currency and foreign-currency monetary receivables/payables are remeasured at CR, with the difference from the pre-adjustment book amount recognized as exchange gain/loss. A separate direction matrix retrieves the asset/liability increase/decrease logic, and the balance-sheet Note retrieves the final `CR換算額`.

### Foreign-exchange forwards

The forward section retrieves `為替予約`, `先物為替相場（FR）`, and `振当処理` as canonical labels. The scope boundary that `独立処理` is outside Level 2 is retained in active text rather than relegated to `Extra`.

For a forward arranged before transaction recognition, the Note uses account-level journal Clozes for purchase and sale entries, applies FR from initial recognition, and retrieves that exchange gain/loss does not arise. For a forward arranged after transaction recognition, the Note distinguishes initial HR recognition from later FR remeasurement and exchange-difference recognition.

The year-end exception avoids a broad action Cloze: because the settlement amount is already fixed at FR, CR remeasurement and the related adjusting entry are both retrieved with the short discriminator `不要`.

The final comparison Note no longer uses the abstract Clozes `あり` / `なし`. It actively contrasts the transaction-date and reservation-date rate choices (`FR` vs `HR`→`FR`), while the already-covered exchange-difference consequence remains visible. This avoids both duplicated recall and visible-answer leakage.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/COM-11.tsv`.

## Deterministic validator

`scripts/validate_com11_production.py` checks:

- exact field order and deterministic stable IDs
- pinned source provenance
- Part/Chapter/primary Section consistency
- required deterministic tags and lifecycle
- `c1`-only generation
- exact deterministic Note-to-ALP mapping and exact-once INCLUDE-ALP coverage
- canonical inventory immutability
- local duplicate rendered text
- visible-answer leakage
- broad/non-atomic Cloze answers, including abstract `あり` / `なし`
- account-level journal-entry masking whenever debit/credit syntax appears
- formula/operator atomicity and required precision forms
- exact canonical exclusion family

Expected output:

```text
COM-11 production validation: PASS
notes=17 cards=17 cloze_spans=41 included_alps=21 mapped=21 unmapped=0
multi_alp_notes=4 journal_entry_notes=3 formula_notes=2 canonical_exclusions=1
account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass formula_atomicity=pass visible_answer_leakage=0 deterministic_order=pass
```