# COM-01 Production QA

Status: **PASS — chapter-local deterministic validation completed for ANKI-008**

## Contract

- frozen v1.0 source/schema/stable-ID baseline: `FREEZE.md`, `rules/cloze_rules.md`, `rules/coverage_rules.md`, `schema/note_schema.yaml`
- v1.2 post-freeze exam-yield / rotation-efficiency overlay: `rules/exam_yield_rules.md`
- canonical ALP shard: `inventory/topic_inventory/COM-01.tsv`
- source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`, Commercial chapter 01

## Coverage and lifecycle

| Metric | Result |
|---|---:|
| Canonical included ALPs | 52 |
| Approved production Notes | 38 |
| Generated Cloze cards | 38 |
| Included ALPs mapped | 52 |
| Unmapped included ALPs | 0 |
| ALPs mapped more than once | 0 |
| Approved multi-ALP Notes | 14 |
| Promoted pilot Note IDs | 18 |
| Reserved pilot-only duplicate-application IDs | 5 |
| Deprecated production rows | 0 |
| Excluded decorative-example rows | 3 |

Every included COM-01 ALP maps exactly once to an approved production Note. Multi-ALP consolidation is used only where source propositions form one coherent retrieval unit or would otherwise create a semantic duplicate.

The following pilot-only synthetic application IDs remain reserved and are not reused: `BK-COM-01-0006`, `BK-COM-01-0013`, `BK-COM-01-0015`, `BK-COM-01-0020`, `BK-COM-01-0023`.

## v1.2 Cloze / rotation checks

- every approved Note generates exactly one Anki card (`c1` only);
- generated cards = approved Notes = **38**;
- exact duplicate Cloze answer spans within an approved Note = **0**;
- exact rendered-text duplicates across approved Notes = **0**;
- supporting context remains visible when an additional Cloze rotation would be low-yield;
- same-index grouping is used for coupled journal entries, formulas, comparisons, and sequences;
- all rows use `Status=approved`, `QA=pass`, and mechanically matching tags.

## Stable IDs and source traceability

- 18 reviewed pilot IDs are promoted without renumbering;
- 20 new production IDs are allocated deterministically as `BK-COM-01-0024`–`BK-COM-01-0043`;
- the 5 reserved pilot-only IDs remain absent;
- every `ALP_IDs` list resolves to canonical `INCLUDE` rows and is source-ordered;
- `Section` matches the primary/first ALP source section;
- pinned source repository, commit, path, part, and chapter fields validate for every row.

## Accounting checks

Journal-entry Notes reviewed: **8**.

Reviewed patterns include:

- 三分法の仕入・売上、前払金充当、仕入返品;
- 三分法の期首・期末商品振替;
- 売上原価対立法の仕入・売上原価振替;
- 棚卸減耗損および商品評価損の計上.

No local account-selection, debit/credit-direction, recognition-timing, or compound-entry blocker remains.

Formula Notes reviewed: **10**.

Reviewed relationships include:

- 純仕入高および仕入金額;
- 移動平均・総平均;
- 月末数量・月末棚卸高;
- 売上原価・売上総利益;
- 期末帳簿棚卸高;
- 棚卸減耗数量・棚卸減耗損;
- 商品評価損.

No local formula-structure or arithmetic blocker remains.

## Duplicate / ambiguity checks

The batch was reviewed against the v1.0 generated-card duplicate rules and the v1.2 active-deck overlay. Direct formula restatements, decorative numeric examples, and low-yield sibling rotations were not added merely to increase Note count. The retained numeric pure-purchase application `BK-COM-01-0004` preserves the reviewed pilot distinction from the Foundation pure-formula retrieval unit.

## Deterministic validation

Run:

```text
python scripts/validate_com01_production.py
```

Expected output:

```text
COM-01 v1.2 production validation: PASS
notes=38 included_alps=52 mapped=52 unmapped=0
generated_cards=38 multi_card_approved_notes=0 multi_alp_notes=14
promoted_pilot_ids=18 reserved_pilot_only_ids=5
journal_entry_notes=8 formula_notes=10
```
