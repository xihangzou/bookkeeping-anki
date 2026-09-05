# IND-14 Production QA

Issue: **ANKI-037 / #38**  
Chapter: **Industrial 14 — 本社工場会計**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/IND-14.tsv`

## Result

- production Notes: **11**
- generated cards: **11**
- Cloze spans: **27**
- included ALPs: **13**
- mapped included ALPs: **13**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **2**
- journal-entry primary Notes: **3**
- formula Notes: **0**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- parallel-term compound Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No IND-14 production Note IDs existed before ANKI-037. IDs are allocated deterministically in primary canonical ALP order as `BK-IND-14-0001`–`BK-IND-14-0011`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The canonical inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Two multi-ALP Notes compress facts that share one retrieval frame without losing distinct source meaning:

- `BK-IND-14-0005`: reciprocal `工場` / `本社` accounts plus their company-wide elimination (`0005`, `0006`)
- `BK-IND-14-0006`: one-side versus both-side transaction recording procedure (`0007`, `0008`)

The worked numerical example remains excluded as `DECORATIVE_EXAMPLE`; its accounting decisions are already represented by the active procedure and journal-entry Notes.

## Recall-design review

### Definition, ledgers, and account placement

`工場会計の独立` is retrieved from a visible description of separated books and factory-side manufacturing records. The ledger Note separately Clozes `工場元帳`, `本社元帳`, and its synonym `一般元帳` so parallel labels are atomic while remaining one coherent card.

Account-location recall tests the actual placement decision: manufacturing accounts such as materials, labor, expenses, manufacturing overhead, and work in process map to `工場`, while cash/deposit, receivable/payable, sales, and selling/administrative accounts map to `本社`.

The product-account exception tests `製品` as the account that may instead be established on the head-office side, avoiding a trivial binary Cloze of `本社` versus `工場`.

### Reciprocal accounts and financial-statement elimination

The reciprocal-account Note retrieves `工場` on the central-side books and `本社` on the manufacturing-site books, then retrieves their company-wide `相殺`. Visible prompts use `中央側` and `製造拠点側` so the target account names are not leaked by the question text.

The comparison Note connects this relation to `本支店会計` and its corresponding head-office/branch reciprocal accounts.

### One-side and both-side transaction procedure

A one-side transaction retrieves that normal recording is performed by `担当する側だけ`. A both-side transaction retrieves `会社全体` as the starting frame before the entry is divided between the two ledgers.

Factory-internal production activity uses a precise consequence Cloze: for material consumption, labor consumption, manufacturing-overhead allocation, and product completion, a head-office entry is `不要`. The visible frame uniquely identifies what is unnecessary and under which condition.

### Journal entries

All journal entries preserve debit/credit markers and separators and Cloze account names only.

- Material purchase and transfer: central side `(借) 工場 / (貸) 買掛金`; manufacturing-site side `(借) 材料 / (貸) 本社`.
- Head-office payment of factory costs: central side `(借) 工場 / (貸) 現金`; manufacturing-site side retrieves `賃金給料` and `製造間接費` as separate parallel Cloze spans, with `(貸) 本社`.
- Sale when the product account is maintained at the factory: product-cost transfer is central side `(借) 売上原価 / (貸) 工場`; manufacturing-site side `(借) 本社 / (貸) 製品`. Ordinary sales recognition remains visible as a separate standard entry rather than expanding this Note into a larger compound journal.

The prompts intentionally use `中央側` / `製造拠点側` and paraphrases such as `製造用物品` / `完成品` where needed to prevent visible leakage of target account names.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/IND-14.tsv`.

## Deterministic validator

`scripts/validate_ind14_production.py` checks:

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
- parallel-term Cloze atomicity
- account-level journal-entry masking / rejection of whole-entry Clozes
- arithmetic/operator non-hiding
- exact canonical exclusion family

Expected output:

```text
IND-14 production validation: PASS
notes=11 cards=11 cloze_spans=27 included_alps=13 mapped=13 unmapped=0
multi_alp_notes=2 journal_entry_notes=3 formula_notes=0 canonical_exclusions=1
account_level_journal_cloze=pass minimal_cloze_scope=pass parallel_term_atomicity=pass cost_accounting_treatment=pass visible_answer_leakage=0 deterministic_order=pass
```
