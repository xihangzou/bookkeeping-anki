# COM-14 Production QA

Issue: **ANKI-021 / #22**  
Chapter: **Commercial 14 — 本支店会計**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/COM-14.tsv`

## Result

- production Notes: **19**
- generated cards: **19**
- Cloze spans: **52**
- included ALPs: **23**
- mapped included ALPs: **23**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **4**
- journal-entry primary Notes: **7**
- formula Notes: **0**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No COM-14 production Note IDs existed on `main` before ANKI-021. IDs are allocated deterministically in primary canonical ALP order as `BK-COM-14-0001`–`BK-COM-14-0019`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The ANKI-003 inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Four multi-ALP Notes are used where one retrieval frame materially represents related source propositions without duplicating review:

- `BK-COM-14-0003`: reciprocal account selection and the nature of the reciprocal accounts (`0003`, `0004`)
- `BK-COM-14-0012`: consolidation sequence and the rule that combination/elimination are performed outside the individual ledgers (`0013`, `0015`)
- `BK-COM-14-0014`: the two interbranch-accounting methods and the headquarters-entry distinction (`0016`, `0019`)
- `BK-COM-14-0017`: local profit closing and subsequent aggregation into combined income (`0020`, `0021`)

The depreciation/consolidation numerical worked example remains excluded as `DECORATIVE_EXAMPLE` because it adds no retrieval operation beyond the active consolidation sequence and reciprocal-account elimination rules.

## Recall-design review

### Reciprocal accounts and prompt sufficiency

The batch retrieves `支店`, `本店`, and `照合勘定` while keeping the accounting role visible. Where `支店` or `本店` itself is the answer, prompts use role language such as `本部`, `営業拠点`, `現地拠点`, or `回収拠点` so the target answer does not appear elsewhere on the generated card.

The reciprocal-balance rule separately retrieves `同額` and `反対`. The reverse-direction Note hides all four debit/credit occurrences with the same `c1`, preventing the normal position from leaking the exceptional position or vice versa.

### Journal entries

All displayed journal entries retain debit/credit labels and separators and Cloze account names individually with the same `c1` for the coherent entry. No whole-entry Cloze is used.

Accounting review confirms the source patterns:

- collection of headquarters receivable by the local branch: headquarters `(借)支店/(貸)売掛金`; local branch `(借)現金/(貸)本店`
- payment of headquarters payable by the local branch: headquarters `(借)買掛金/(貸)支店`; local branch `(借)本店/(貸)現金`
- headquarters payment of a branch expense: headquarters `(借)支店/(貸)現金`; local branch `(借)営業費/(貸)本店`
- headquarters shipment of merchandise to a branch: headquarters `(借)支店/(貸)仕入`; local branch `(借)仕入/(貸)本店`
- consolidation elimination of normal reciprocal balances: `(借)本店/(貸)支店`
- transfer of branch profit to combined income: headquarters `(借)支店/(貸)総合損益`; local branch `(借)損益/(貸)本店`
- final transfer of combined income: `(借)総合損益/(貸)繰越利益剰余金`

Amounts from source examples are not Clozed because the active targets are account selection and bookkeeping mechanics rather than arbitrary numeric substitution.

### Consolidated financial statements

The canonical label `合併財務諸表` is retrieved from its defining relationship. A separate procedure Note retrieves the consolidation operations `合算` and `相殺消去`, while keeping the first-stage adjusted trial balances visible; `会計帳簿の枠外` is also retrieved as the stage-location rule. This makes the later consolidation procedure materially distinct from the earlier Note that tests each location's independent closing work.

### Interbranch methods

The comparison Note retrieves the canonical method labels from their distinguishing headquarters-participation rule: direct local recording with no headquarters entry versus treatment as a headquarters-routed transaction with a headquarters transfer entry.

Separate application Notes then retrieve the operational accounts. Under `支店分散計算制度`, each branch uses the `相手支店` account and headquarters recording is `不要`. Under the centralized method, the transaction is treated as `本店経由`; headquarters uses `各支店` accounts and each branch uses the `本店` account. These are different retrieval operations rather than reworded duplicates.

### Closing process

The closing sequence retrieves the local `損益` account and headquarters `総合損益` account in one coherent frame. The branch-profit transfer and final retained-earnings transfer remain separate account-level journal Notes because each requires an independent entry that must be executable from memory.

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/COM-14.tsv`.

## Deterministic validator

`scripts/validate_com14_production.py` checks:

- exact field order and deterministic stable IDs
- pinned source provenance
- Part/Chapter/primary Section consistency
- required deterministic tags and lifecycle
- `c1`-only generation and exact card/span counts
- exact deterministic Note-to-ALP mapping and exact-once INCLUDE-ALP coverage
- canonical inventory immutability
- local duplicate rendered text
- visible-answer leakage
- broad/non-atomic Cloze answers
- account-level journal-entry masking whenever debit/credit syntax appears
- required reciprocal-account, consolidation, interbranch-method, and closing precision forms
- exact canonical exclusion family

Expected output:

```text
COM-14 production validation: PASS
notes=19 cards=19 cloze_spans=52 included_alps=23 mapped=23 unmapped=0
multi_alp_notes=4 journal_entry_notes=7 formula_notes=0 canonical_exclusions=1
account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass procedure_precision=pass visible_answer_leakage=0 deterministic_order=pass
```
