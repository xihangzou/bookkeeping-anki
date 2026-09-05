# COM-16 Production QA

Issue: **ANKI-023 / #24**  
Chapter: **Commercial 16 — 製造業会計**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/COM-16.tsv`

## Result after cross-chapter deduplication

COM-16 originally contained 23 approved one-topic Notes. A targeted retrieval-unit audit found substantial semantic overlap with the already-produced industrial-bookkeeping chapters, especially `IND-02`, `IND-03`, `IND-04`, `IND-05`, `IND-07`, and `IND-10`.

The correction keeps COM-16 active only where the retrieval operation is the **integrated monthly manufacturing-accounting / commercial-closing flow** rather than the same isolated industrial-bookkeeping rule.

- production rows: **23**
- active approved Notes/cards: **9**
- deprecated historical Notes: **14**
- active Cloze spans: **61**
- included COM-16 ALPs: **24**
- active mapped included ALPs: **24**
- active unmapped ALPs: **0**
- active multiply mapped ALPs: **0**
- deprecated Notes with explicit replacement mapping: **14 / 14**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- stable Note IDs preserved: **23 / 23**
- visible-answer leakage in active cards: **0**
- active cards use only `c1`

## Normalization design

The inventory remains immutable. No ALP is deleted or renumbered. Instead:

1. the 24 included COM-16 ALPs are remapped exactly once across nine approved integrated Notes;
2. superseded one-topic Notes are retained as `Status=deprecated` so their stable IDs and historical ALP lineage remain auditable;
3. every deprecated row records `統合先: BK-COM-16-....` in `Extra`;
4. deprecated rows are excluded from active export under the existing production lifecycle contract.

### Active mapping

| Active Note | COM-16 ALPs | Retrieval frame | Main overlap removed |
|---|---|---|---|
| `BK-COM-16-0001` | `0001–0004` | 製造業会計→月次決算→P/L・B/S、月次締切境界 | IND-01 / IND-10 |
| `BK-COM-16-0004` | `0005–0007` | 材料消費・帳簿残高・正常減耗の月次材料フロー | IND-02 |
| `BK-COM-16-0007` | `0008–0009` | 賃金消費額測定→直接/間接労務費振替 | IND-03 |
| `BK-COM-16-0009` | `0010–0012` | 退職給付・間接経費・減価償却の月次機能別配分 | IND-03 / IND-04 |
| `BK-COM-16-0012` | `0013–0015` | 予定配賦→原価差異→有利/不利方向 | IND-05 |
| `BK-COM-16-0015` | `0016–0018` | 当月製造原価→完成品原価→仕掛品から製品 | IND-07 / IND-10 |
| `BK-COM-16-0018` | `0019–0020` | 月次売上原価→製品から売上原価 | IND-07 / IND-10 |
| `BK-COM-16-0020` | `0021–0022` | 原価差異の売上原価賦課→製造業P/L | IND-05 / IND-10 |
| `BK-COM-16-0022` | `0023–0024` | 製造業B/S棚卸資産→利益剰余金・貸借連携 | IND-10 / COM-13 |

## Why these nine Notes remain active

The industrial chapters teach the component rules as independent retrieval units: material accounting, labor accounting, expenses, overhead allocation, individual cost flow, and industrial financial statements. Repeating those same propositions as separate COM-16 cards would violate retrieval-unit-level duplicate control.

COM-16 has a distinct role: it connects those component rules into a **single monthly manufacturing closing problem in the commercial-bookkeeping sequence**. The retained Notes therefore test larger but coherent transitions such as material/labor inputs → manufacturing overhead → work in process → finished goods → cost of goods sold → variance-adjusted P/L/B/S.

This changes the retrieval operation from “recall one industrial rule” to “reconstruct the relevant part of the monthly commercial-closing flow.” The overlap is therefore retained only in integrated form, not as duplicate one-proposition cards.

## Deprecated lineage

The following historical Notes remain in the TSV but are excluded from active export:

- `BK-COM-16-0002`, `0003` → `BK-COM-16-0001`
- `BK-COM-16-0005`, `0006` → `BK-COM-16-0004`
- `BK-COM-16-0008` → `BK-COM-16-0007`
- `BK-COM-16-0010`, `0011` → `BK-COM-16-0009`
- `BK-COM-16-0013`, `0014` → `BK-COM-16-0012`
- `BK-COM-16-0016`, `0017` → `BK-COM-16-0015`
- `BK-COM-16-0019` → `BK-COM-16-0018`
- `BK-COM-16-0021` → `BK-COM-16-0020`
- `BK-COM-16-0023` → `BK-COM-16-0022`

Their original Text, source provenance, and original ALP mappings are retained for audit history. Stable IDs are not reused.

## Recall / accounting QA

The nine active Notes retain current-rule mechanics:

- journal syntax `(借)/(貸)` remains visible and account names are Clozed at account level;
- formula operators remain visible;
- same-answer repeated operands/accounts use the same `c1` so no sibling answer leaks;
- monthly/timing qualifiers stay visible where they identify the calculation role;
- the material proposition of every mapped ALP remains in active `Text` rather than only in `Extra`;
- no active rendered Note duplicates another COM-16 Note;
- one-topic repetitions that already exist in IND are no longer active COM-16 cards.

## Deterministic validator

`scripts/validate_com16_production.py` now validates both the active normalized deck and the historical lineage. It checks:

- all 23 stable IDs remain present and ordered;
- exactly 9 rows are `approved` and 14 are `deprecated`;
- every deprecated Note has a deterministic replacement mapping;
- historical ALP mappings of deprecated IDs are unchanged;
- all 24 included COM-16 ALPs map exactly once to approved active Text;
- active source/section/tag/lifecycle fields follow the schema;
- active Cloze leakage, broad-answer, formula-operator, and journal-account masking rules pass;
- canonical inventory remains unchanged;
- the one existing `DECORATIVE_EXAMPLE` exclusion remains unchanged.

Expected output:

```text
COM-16 production validation: PASS
rows=23 active_notes=9 deprecated_notes=14 active_cards=9 active_cloze_spans=61
included_alps=24 active_mapped=24 active_unmapped=0 historical_replacements=14 canonical_exclusions=1
cross_chapter_dedup=pass active_exact_once_alp_coverage=pass stable_id_lineage=pass account_level_journal_cloze=pass formula_atomicity=pass minimal_cloze_scope=pass visible_answer_leakage=0 deterministic_order=pass
```
