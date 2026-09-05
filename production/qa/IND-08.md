# IND-08 Production QA

Issue: **ANKI-031 / #32**  
Chapter: **Industrial 08 — 総合原価計算**  
Rules: current living `SPEC.md` and sole authoritative `rules/anki_card_rules.md`  
Source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`  
Canonical shard: `inventory/topic_inventory/IND-08.tsv`

## Result

- production Notes: **27**
- generated cards: **27**
- Cloze spans: **72**
- included ALPs: **33**
- mapped included ALPs: **33**
- unmapped included ALPs: **0**
- multiply mapped included ALPs: **0**
- coherent multi-ALP Notes: **5**
- formula Notes: **5**
- procedure Notes: **7**
- measurement Notes: **5**
- canonical exclusions: **1** (`DECORATIVE_EXAMPLE` 1)
- visible-answer leakage for 2+ character answers: **0**
- broad/non-atomic targeted action Clozes: **0**
- parallel terms joined by `・` inside one Cloze: **0**
- every approved Note uses only `c1`
- lifecycle: all rows `Status=approved`, `QA=pass`

## Stable IDs

No IND-08 production Note IDs existed before ANKI-031. IDs are allocated deterministically in primary canonical ALP order as `BK-IND-08-0001`–`BK-IND-08-0027`.

## Coverage architecture

Every canonical INCLUDE ALP is mapped exactly once through `ALP_IDs`. The canonical inventory remains immutable: `note_ids` stays empty and `qa_status` stays `pending`.

Coherent multi-ALP Notes are used only where the propositions share one retrieval frame:

- `BK-IND-08-0006`: 加工進捗度と加工換算量 (`0006`, `0007`)
- `BK-IND-08-0013`: 先入先出法の材料費・加工費配分 (`0014`, `0015`)
- `BK-IND-08-0015`: 平均法の材料費・加工費配分 (`0017`, `0018`)
- `BK-IND-08-0017`: 正常減損と仕損の相違 (`0020`, `0021`)
- `BK-IND-08-0027`: 追加材料の終点・途中点・平均投入 (`0031`–`0033`)

例題8-1〜8-6は、先入先出法・平均法・仕損・追加材料の規則を数値置換した具体例であり、新しい判断分岐を追加しないため canonical `DECORATIVE_EXAMPLE` のまま除外する。

## Recall-design review

### 総合原価計算と月末仕掛品

総合原価計算・継続製造指図書・個別原価計算との集計単位の差を、名称だけでなく適用形態と配分対象が見える文脈で取得する。

加工費は `直接労務費`・`直接経費`・`製造間接費`を別々の短い Cloze span とし、並列項目を一括で隠さない。始点投入材料は実在量、加工費は加工換算量という配分基準を独立した measurement Note で保持する。

### Formula atomicity

演算子は常に可視とし、式のオペランドだけを個別に Cloze 化する。

- `加工換算量＝実在量×加工進捗度`
- `月末仕掛品材料費＝対象材料費×月末仕掛品数量÷対象投入数量`
- `月末仕掛品加工費＝対象加工費×月末仕掛品加工換算量÷対象加工換算量合計`
- `完成品原価＝月初仕掛品原価＋当月製造費用－月末仕掛品原価`
- `正常仕損費＝仕損品原価－仕損品評価額`

### 先入先出法と平均法

先入先出法は月初仕掛品を先に完成させる前提と、当月投入数量・前月加工済み部分を除く加工換算量基準を同じ方法文脈で保持する。平均法は月初原価と当月原価を合算し、材料数量と加工換算量のそれぞれの分母を明示する。

### 仕損・減損

正常仕損と正常減損は、実体の残存・消失と評価額の有無を同じ比較フレームで取得する。

仕損費の負担先は条件を可視に保ち、月末仕掛の進捗度が仕損発生点未満なら `完成品のみ`、発生点以上なら `完成品` と `月末仕掛品` の両者とする。

度外視法の分母処理は、完成品のみ負担では仕損数量・仕損加工換算量を **含める**、両者負担では **除外する** と明示して逆転ミスを防ぐ。

仕損品評価額がある場合は `貯蔵品` として資産計上し、完成品のみ負担では完成品原価から控除、両者負担では対象製造費用から先に控除してから仕損を度外視する。

### 追加材料

追加材料は投入点と加工進捗度の関係を判断軸にし、終点投入・途中点投入・平均投入を一つの比較可能な retrieval frame に統合する。

- 終点投入: 完成品のみ
- 途中点投入: 投入点を通過した加工品だけ
- 平均投入: 加工換算量で按分

## Journal-entry and cost-accounting QA

IND-08 canonical shardには standalone `journal_entry` ALP はないため、不要な仕訳 Note は追加していない。validator は将来借貸表記が追加された場合でも account-level masking を要求し、compact whole-entry Cloze を拒否する。

原価計算固有の配分ロジックは、より正確な `formula` / `measurement` / `procedure` 型で表現し、仕損の分母処理、FIFO・平均法、追加材料の投入点判定を章固有 precision checks で固定する。

## Source traceability

Each row pins:

- `SourceRepo=xihangzou/bookkeeping-integrated`
- `SourceCommit=569ed7b82e729334e1472286eaca7c4352e6fbdb`
- `SourcePath=merged/textbook.md`

Exact chapter anchors remain recoverable through each mapped canonical ALP in `inventory/topic_inventory/IND-08.tsv`.

## Deterministic validator

`scripts/validate_ind08_production.py` checks:

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
- parallel `・`-joined terms are split into separate Cloze spans
- account-level journal-entry masking if debit/credit syntax appears
- formula/operator atomicity
- FIFO/average process-costing precision
- spoilage burden and scrap-value precision
- added-material endpoint/midpoint/uniform precision
- exact canonical exclusion family

Expected output:

```text
IND-08 production validation: PASS
notes=27 cards=27 cloze_spans=72 included_alps=33 mapped=33 unmapped=0
multi_alp_notes=5 formula_notes=5 procedure_notes=7 measurement_notes=5 canonical_exclusions=1
process_costing=pass spoilage_logic=pass added_materials=pass formula_atomicity=pass account_level_masking=pass minimal_cloze_scope=pass visible_answer_leakage=0 deterministic_order=pass
```

## Initial implementation commits

- `f1a3b3f631fb2afa7527c9f3c3a355302c0d3ee1` — add `production/notes/IND-08.tsv`
- `bc79c0ec937a1a4cb93a34a99545d39eed978675` — add `scripts/validate_ind08_production.py`
