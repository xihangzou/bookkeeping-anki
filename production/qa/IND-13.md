# IND-13 Production QA

Issue: **ANKI-036 / #37**  
Chapter: **Industrial 13 — CVP分析**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/IND-13.tsv`

## Result

- production Notes: **15**
- generated cards: **15**
- Cloze spans: **55**
- included ALPs: **24**
- mapped included ALPs: **24**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **8**
- formula primary Notes: **11**
- definition primary Notes: **4**
- journal-entry primary Notes: **0**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- non-atomic parallel-term Clozes: **0**
- hidden arithmetic operators: **0**
- duplicate rendered Note prompts: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs and inventory lineage

No IND-13 production Note IDs existed on `main` before ANKI-036. IDs are allocated deterministically by the first mapped ALP in canonical source order as `BK-IND-13-0001`–`BK-IND-13-0015`.

The canonical ANKI-003 inventory is not mutated: `note_ids` remains empty and `qa_status` remains `pending`. Production coverage is recorded through Note `ALP_IDs` and this QA artifact.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once. Eight integrated Notes combine ALPs only where one retrieval frame covers a tightly coupled relationship:

- `BK-IND-13-0001`: CVP definition and cost-behavior premise (`0001`, `0002`)
- `BK-IND-13-0003`: contribution-margin ratio, variable-cost ratio, and 100% identity (`0004`–`0006`)
- `BK-IND-13-0005`: break-even sales and volume formulas (`0008`, `0009`)
- `BK-IND-13-0006`: target-profit sales and volume formulas (`0010`, `0011`)
- `BK-IND-13-0010`: safety-margin rate formula and interpretation (`0015`, `0016`)
- `BK-IND-13-0011`: operating-leverage formula and interpretation (`0017`, `0018`)
- `BK-IND-13-0012`: cost separation and account-analysis method (`0019`, `0020`)
- `BK-IND-13-0013`: high-low method and normal-operating-range exception (`0021`, `0024`)

The numerical examples in examples 13-1–13-3 remain excluded as `DECORATIVE_EXAMPLE`; they add number substitution rather than a new retrieval operation.

## Recall-design review

### CVP and contribution relationships

The active prompts preserve the named accounting subject while testing the canonical method label, cost-behavior categories, and quantitative relationships. Closely coupled identities are grouped into one `c1` card to prevent sibling formulas from revealing target operands.

### Break-even and target-profit formulas

Sales-based and volume-based forms are paired only where their shared numerator and different denominator encode one coherent comparison. Arithmetic operators remain visible and each hidden formula term is an atomic operand or result label.

### Safety margin and operating leverage

The formulas and their economic interpretations are integrated only when the interpretation directly explains how to read the computed indicator. Repeated target terms use the same Cloze index so visible text does not leak the answer.

### High-low method

The method Note keeps the normal-operating-range condition explicit and tests the high and low operating points as separate Cloze spans. The variable-rate and fixed-cost formulas are separate Notes because each requires a distinct calculation relationship.

## Accounting / calculation QA

Manual review against the pinned chapter and canonical ALPs confirms:

- contribution margin = sales − variable costs = fixed costs + operating profit
- contribution-margin ratio + variable-cost ratio = 100%
- break-even sales = fixed costs ÷ contribution-margin ratio
- break-even volume = fixed costs ÷ unit contribution margin
- target-profit sales/volume add target operating profit to fixed costs
- target operating-margin sales = fixed costs ÷ (contribution-margin ratio − target operating-margin ratio)
- break-even ratio, margin-of-safety amount/rate identities are preserved
- operating leverage = contribution margin ÷ operating profit, with the fixed-cost sensitivity interpretation preserved
- high-low variable rate and fixed-cost formulas use only normal-operating-range high/low points

No journal entries occur in the chapter, so account-level journal masking is not applicable.

## Deterministic validator

`scripts/validate_ind13_production.py` checks:

- exact field order and deterministic stable IDs
- pinned source provenance
- Part/Chapter/primary Section consistency
- required deterministic tags and lifecycle
- exact-once INCLUDE ALP coverage and exact expected mappings
- canonical inventory immutability
- `c1`-only deterministic card generation
- expected Note/card/Cloze-span counts
- minimal Cloze scope, visible-answer leakage, and hidden-operator checks
- atomic parallel-term Cloze spans
- required formula/definition precision anchors
- duplicate rendered prompts
- canonical exclusion count/reason

Expected validator output:

```text
IND-13 production validation: PASS
notes=15 cards=15 cloze_spans=55 included_alps=24 mapped=24 unmapped=0
multi_alp_notes=8 formula_notes=11 definition_notes=4 canonical_exclusions=1
atomic_formula_operands=pass parallel_term_atomicity=pass minimal_cloze_scope=pass visible_answer_leakage=0 duplicate_rendered_text=0 deterministic_order=pass
```
