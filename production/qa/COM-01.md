# COM-01 Production QA

Status: **PASS — v1.6 recall-design / formula-itemization audit completed**

## Contract

- frozen v1.0 source/schema/stable-ID baseline: `FREEZE.md`, `rules/cloze_rules.md`, `rules/coverage_rules.md`, `schema/note_schema.yaml`
- current v1.6 post-freeze active-deck / recall-design overlay: `rules/exam_yield_rules.md`
- canonical ALP shard: `inventory/topic_inventory/COM-01.tsv`
- source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`, Commercial chapter 01

## Coverage and lifecycle

| Metric | Result |
|---|---:|
| Canonical included ALPs | 52 |
| Approved production Notes | 38 |
| Generated Cloze cards | 38 |
| Active Cloze spans | 92 |
| Included ALPs mapped | 52 |
| Unmapped included ALPs | 0 |
| ALPs mapped more than once | 0 |
| Approved multi-ALP Notes | 14 |
| Promoted pilot Note IDs | 18 |
| Reserved pilot-only duplicate-application IDs | 5 |
| Deprecated production rows | 0 |
| Excluded decorative-example rows | 3 |
| Exact visible-answer leakage (2+ chars) | 0 |

Every included COM-01 ALP remains mapped exactly once to an approved production Note. The v1.6 audit changes recall design inside existing Notes rather than increasing card count or retiring source content.

The following pilot-only synthetic application IDs remain reserved and are not reused: `BK-COM-01-0006`, `BK-COM-01-0013`, `BK-COM-01-0015`, `BK-COM-01-0020`, `BK-COM-01-0023`.

## v1.6 recall-design changes

- all approved Notes still use only `c1`, so **38 Notes = 38 generated cards**;
- parallel answers are separate same-index spans rather than list-like compound answers;
- arithmetic and accounting formulas keep operators visible and Cloze individual terms;
- long sequence/procedure Clozes are split into shorter same-card units;
- debit/credit direction retrieval uses `{{c1::借}}方` / `{{c1::貸}}方` where the side itself is tested;
- 2+ character Cloze answers do not appear verbatim in the visible portion of the same generated card;
- visible cues remain after masking so each card retains a recognizable retrieval frame;
- integrated Notes retain source propositions needed to recover all mapped ALPs.

Representative migrations:

- `BK-COM-01-0004`: numeric pilot application -> source-faithful `純仕入高＝{{c1::総仕入高}}－{{c1::仕入戻し高}}`;
- `BK-COM-01-0005`: acquisition-cost terms itemized while keeping transport / insurance / packing content;
- `BK-COM-01-0007`, `0031`: method families split into separate same-`c1` lexical spans;
- `BK-COM-01-0012`, `0014`, `0034`, `0035`, `0039`, `0019`, `0021`, `0022`: formulas itemized term by term;
- `BK-COM-01-0017`: closing sequence split into three ordered same-card spans;
- journal-entry Notes use account-level or direction-level spans instead of hiding an entire entry;
- `BK-COM-01-0041`: financial-statement mapping redesigned to avoid substring answer leakage.

## Source-content preservation

The audit explicitly checks mapped multi-ALP Notes for material source details, including:

- 三分法 account classification and closing mechanics;
- 分記法 account classification and profit relationship;
- 売上原価対立法 account family and inventory-asset recognition;
- 商品有高帳 as a subsidiary ledger and original-cost recording;
- cost-flow premise plus FIFO / moving-average / total-average families;
- FIFO old/new cost-layer mechanics;
- acquisition-cost ancillary charges (`運送料`, `保険料`, `梱包代`);
- inventory shrinkage, lower-of-cost valuation, and statement-display relationships.

## Stable IDs and source traceability

- all 38 production Note IDs are unchanged;
- 18 reviewed pilot IDs remain promoted without renumbering;
- 20 production IDs remain `BK-COM-01-0024`–`BK-COM-01-0043`;
- the 5 reserved pilot-only IDs remain absent;
- every `ALP_IDs` list resolves to canonical `INCLUDE` rows and remains source-ordered;
- `Section` still matches the primary/first ALP source section;
- pinned source repository, commit, path, part, and chapter fields remain unchanged.

## Accounting checks

Journal-entry Notes reviewed: **8**.

Reviewed patterns include:

- 三分法の仕入・売上、前払金充当、仕入返品;
- 三分法の期首・期末商品振替;
- 売上原価対立法の仕入・売上原価振替;
- 棚卸減耗損および商品評価損の計上.

Formula Notes reviewed: **10**.

Reviewed relationships include:

- 純仕入高および仕入金額;
- 移動平均・総平均;
- 月末数量・月末棚卸高;
- 売上原価・売上総利益;
- 期末帳簿棚卸高;
- 棚卸減耗数量・棚卸減耗損;
- 商品評価損・評価後期末在庫額.

No local account-selection, debit/credit-direction, recognition-timing, formula-structure, or source-content blocker remains.

## Deterministic validation

Run:

```text
python scripts/validate_com01_production.py
```

Expected output:

```text
COM-01 v1.6 production validation: PASS
notes=38 included_alps=52 mapped=52 unmapped=0
generated_cards=38 cloze_spans=92 visible_answer_leakage=0 multi_alp_notes=14
promoted_pilot_ids=18 reserved_pilot_only_ids=5
journal_entry_notes=8 formula_notes=10
```
