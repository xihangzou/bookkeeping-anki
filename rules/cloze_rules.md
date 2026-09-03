# Cloze Rules

Status: **v0.9 — representative pilot後に一度だけv1.0へ改訂可**

## 1. Objective

Cloze は文章の穴埋めではなく、会計知識を正確に想起するための retrieval prompt として設計する。

最優先順位は次の通り。

1. 何を思い出すべきか明確
2. 正答が一意または実質一意
3. 会計上重要な情報を想起させる
4. 不要な暗記負荷を増やさない
5. 後続の2級・CPA学習でも崩れない理解を作る

本ルールは `SPEC.md`、`rules/coverage_rules.md`、`schema/note_schema.yaml`、`pilot/PLAN.md` と整合して運用する。矛盾を発見した場合はローカル判断で補完せず、明示的に解消する。

## 2. Atomicity

原則として `1 Note = 1 coherent recall unit`。

- 1つの定義
- 1つの認識ルール
- 1つの仕訳パターン
- 1つの計算関係
- 1つの比較軸
- 1つの手続ブロック

複数論点を1 Noteに混ぜない。ただし、分離すると関係性自体が失われる場合は同一Noteに置く。

## 3. Cloze count

原則は **1〜3 cloze groups / Note**。

4個以上を許容する主なケース：

- 一連の手続順序
- 財務諸表の構造
- 同一ルール内の不可分な複数要素
- 比較表の1行をまとめて覚える場合

カード数を増やすためだけに `c1`, `c2`, `c3` を分けない。

## 4. Anki Cloze semantics and numbering

Ankiでは、異なるCloze番号は原則として異なるカードを生成する。同じ番号を複数箇所に使うと、その箇所は同じカード上で同時に隠れる。

### Same number

同時に一塊として再生できるべき情報は同じ番号にする。

例：

```text
資産は通常 {{c1::借方}} 側に位置し、増加は {{c1::借方}} に記入する。
```

### Different numbers

独立して問う価値がある情報は別番号にする。

```text
売掛金は {{c1::資産}} であり、通常は {{c2::借方}} 残高を持つ。
```

ただし、別番号にすると他のClozeの正答が表示される。したがって、**各 `cN` が実際にカード化された状態を想定し、残りの表示情報が答えを実質的に漏らしていないか確認する**。

## 5. Context sufficiency

禁止：

```text
{{c1::買掛金}}
```

許容：

```text
商品を掛けで仕入れたとき、代金の支払義務は {{c1::買掛金}} として処理する。
```

穴を表示した状態でも、何を答えるカードか判断できなければならない。

## 6. Do not over-delete

原則として文全体・仕訳全体・公式全体を1つの巨大Clozeにしない。

悪い例：

```text
商品100円を掛けで仕入れた。
{{c1::借方 仕入100 / 貸方 買掛金100}}
```

ただし、複数要素が1つの不可分なretrieval targetである場合は、必要な要素を同じCloze番号で隠すことがある。重要なのは「隠す範囲を大きくすること」ではなく、「何を一体として再生すべきか」を先に決めることである。

## 7. Journal-entry rules

仕訳ALPでは、作成前にretrieval targetを次のいずれかとして明確化する。

1. 仕訳全体の組合せ
2. 独立して想起する価値がある一方の勘定科目
3. 金額・計算要素
4. 借貸方向そのもの

### Whole coupled entry

借方・貸方の組合せ全体を再生することが目標なら、片側だけ表示されて他方の答えを漏らす構造を避ける。

標準例：

```text
商品100円を掛けで仕入れた。
借方：{{c1::仕入}} 100
貸方：{{c1::買掛金}} 100
```

これにより、同一カード上で両方の勘定科目を同時に再生する。

### Independent side recall

一方の勘定科目だけを独立して問うこと自体にretrieval価値がある場合は別番号を使ってよい。

```text
商品100円を掛けで仕入れた。
借方：{{c1::仕入}} 100
貸方：{{c2::買掛金}} 100
```

ただしこの場合、`c1`カードでは貸方、`c2`カードでは借方が見える。その表示が正答をほぼ決定してしまう場合は採用しない。

### Amounts

金額が問題文からそのまま転記するだけなら、原則Clozeにしない。

金額Clozeを使うのは次の場合。

- 計算が必要
- 配賦が必要
- 差額計算が必要
- 税・利息・減価償却等の測定ルールが含まれる
- 金額関係そのものが論点

### Debit / credit labels

「借方」「貸方」自体を隠すのは、借貸方向が学習目標であるカードに限る。通常の仕訳カードではラベルを表示して勘定科目の想起に集中させる。

### Reasoning

重要な仕訳には、必要に応じて `Extra` に次を示す。

- 各勘定の5要素分類
- 増減
- 借貸決定理由
- 認識タイミング

## 8. Definition cards

定義語または定義の中核を隠す。

```text
{{c1::試算表}}とは、総勘定元帳の各勘定の金額を集計した一覧表である。
```

定義文を丸ごと隠さない。

## 9. Classification cards

複数属性を関係づけて覚える。

```text
仮払金は原則 {{c1::資産}}、仮受金は原則 {{c2::負債}} として扱う。
```

単純な「勘定科目→5要素」を大量に重複生成しない。同じ分類が仕訳・説明カードで十分に想起される場合はcoverage上の重複を確認する。

## 10. Recognition / timing cards

「いつ計上するか」は独立した重要論点として扱う。

```text
掛け仕入では、仕入は代金支払時ではなく {{c1::商品を受け取った時点}} で計上する。
```

支払・入金と収益費用認識を混同しやすい論点は優先的にカード化する。

## 11. Measurement cards

`measurement` は、金額・評価額・配賦額などの決定ルールそのものを想起対象にする。

```text
期末商品の取得原価が120、正味売却価額が100の場合、評価額は {{c1::100}} となる。
```

単なる数値代入ではなく、どの測定ルールを使うか、どの金額を採用するか、どの差額を認識するかにretrieval価値がある場合に作成する。

公式を使うだけの問題は `formula`、認識時点が主題なら `recognition`、仕訳再生が主題なら `journal_entry` をprimary typeとする。

## 12. Formula cards

公式全体を一度に隠すより、意味構造を残す。

標準例：

```text
売上原価 = {{c1::期首商品棚卸高}} + {{c2::当期商品仕入高}} - {{c3::期末商品棚卸高}}
```

ただし公式を一体として再生することが重要な場合は、同一Cloze groupにまとめてもよい。

数値例は公式適用に追加の判断がある場合のみ別Note化する。

## 13. Procedure cards

順序自体が論点の場合は系列として出す。

```text
簿記の基本的な一巡：
取引 → {{c1::仕訳}} → {{c2::勘定への転記}} → {{c3::試算表}} → {{c4::決算手続き}} → {{c5::財務諸表}}
```

単なる箇条書き一覧は、順序が試験・理解上重要でなければ無理に順序カードにしない。

## 14. Comparison cards

比較対象と比較軸を明示する。

```text
三分法では商品仕入時に {{c1::仕入}} を用いるのに対し、売上原価対立法では {{c2::商品}} を用いる。
```

「AとBの違いは？」のような自由回答型をClozeへ無理に変換しない。比較軸ごとに必要十分な文へ分解する。

## 15. Exception / condition cards

条件を必ず見える側に残し、結論をClozeにする。

```text
正味売却価額が取得原価を下回る場合、商品は原則 {{c1::正味売却価額}} で評価する。
```

条件まで隠して、何の例外を答えるのか不明にしてはいけない。

## 16. Reasoning cards

丸暗記では後続論点が崩れる場合、因果関係をCloze化する。

```text
買掛金支払時に仕入を再計上しないのは、仕入が {{c1::商品受取時にすでに計上されている}} ためである。
```

すべての説明文をreasoning cardにする必要はない。

## 17. Ledger cards

`ledger` は、仕訳後の転記、勘定記入、残高判定、帳簿上の機械的処理などを扱う。

例：

```text
仕訳を勘定へ転記するとき、各勘定には取引日・{{c1::相手科目}}・金額を記入する。
```

```text
借方合計が貸方合計を上回る勘定は {{c1::借方残高}} となる。
```

仕訳そのものを再生する場合は `journal_entry`、帳簿上の転記・集計・残高処理が主題なら `ledger` とする。

## 18. Financial-statement cards

`financial_statement` は、財務諸表上の表示位置、構造、項目間関係、報告目的を扱う。

例：

```text
貸借対照表では、資産は {{c1::借方側}}、負債・純資産は {{c2::貸方側}} に表示する。
```

構造全体の相互関係を一体として覚える必要がある場合は同じ番号にまとめる。独立して問う場合は別番号にしてよいが、各カードで他方の表示が答えを漏らさないか確認する。

## 19. Cost-accounting cards

`cost_accounting` は、工業簿記に固有の原価の集計・配賦・振替・原価流れ・部門/製品間関係を扱う。

単一の数式だけが主題なら `formula`、単一の配賦額決定が主題なら `measurement`、仕訳再生が主題なら `journal_entry` を優先する。`cost_accounting` は、原価計算固有の流れや関係性がprimary retrieval targetである場合に使用する。

例：

```text
製造原価の流れでは、材料・労務費・経費を集計した後、仕掛品を経て {{c1::製品}} へ振り替える。
```

工業簿記の複雑な原価流れを1 Noteに過剰集約せず、判断単位ごとに分解する。

## 20. Tables

表をそのまま大量Cloze化しない。

- 1行 = 1意味単位を基本
- 比較軸を明示
- 行間の関係が重要なら統合Note
- 列見出しを残して答えの種類を明確化

## 21. Numerical examples

数値だけ変えた同型例は原則1つに統合する。

複数例を残す条件：

- 条件分岐が異なる
- 複合仕訳になる
- 端数・配賦・差額など新しい判断が加わる
- 誤りやすい境界条件を示す

## 22. Extra field

`Extra` は以下に使用できる。

- なぜそうなるか
- 計算過程
- 仕訳分解
- common error
- textbook内の関連節
- CPA学習への短いbridge

禁止：Cloze側で問うべき答えをExtraだけに置くこと。

## 23. Duplicate control

意味的に同じRecall Unitを、語順や数値だけ変えて複数Noteにしない。

重複候補は次の順で処理する。

1. 完全重複 → 1 Noteへ統合
2. 同じ事実・異なる文脈 → retrieval価値を比較
3. 異なる判断を要求 → 別Noteとして保持

## 24. Ambiguity and rendered-card leakage test

Note作成時に次を確認する。

- 正答候補が複数ないか
- textbook用語とカード用語が一致しているか
- 文脈なしに穴の種類が推測不能ではないか
- 同義語を不当に誤答扱いしないか
- 単位・期間・主体が明確か

さらに、異なるCloze番号を含むNoteでは、**生成される各 `cN` カードを個別に確認する**。

各カードについて：

- 他のClozeの表示答えが対象Clozeを実質的に漏らしていないか
- 文法・語尾・レイアウトだけで答えが推測できないか
- 片側が見えることで仕訳・比較・構造の答えが一意に決まってしまわないか
- 隠した範囲が大きすぎず、かつ断片的すぎないか

answer leakageがある場合は、同一番号への統合、文面再設計、Note分割、または不要カードの削除で解消する。

## 25. Canonical ALP-type mapping check

`schema/note_schema.yaml` のprimary typeは以下の13種類であり、すべて本ルールでauthoring可能でなければならない。

- `definition` → §8
- `classification` → §9
- `recognition` → §10
- `measurement` → §11
- `journal_entry` → §7
- `formula` → §12
- `procedure` → §13
- `comparison` → §14
- `exception` → §15
- `reasoning` → §16
- `ledger` → §17
- `financial_statement` → §18
- `cost_accounting` → §19

secondary characteristicsはTagsに置き、ad-hoc primary typeを追加しない。

## 26. Pilot validation checklist

v1.0確定前に、`SPEC.md` と `pilot/PLAN.md` に従う **30〜50 representative Notes** のpilotで検証する。

pilotはPart 0だけに限定せず、**Part 0 + early commercial bookkeeping** の代表サンプルを含む。

最低限確認するrecall types：

- definition
- classification
- recognition
- measurement / numerical application
- simple journal entry
- compound journal entry
- formula
- procedure/order
- comparison
- exception/condition
- reasoning
- ledger
- financial_statement
- cost_accounting はPart II本番前にルール適用可能性を確認し、pilot時点で教材範囲外なら型マッピングのレビューで代替する

pilotでは `pilot/PLAN.md` のstress casesとreview dimensionsを使用し、実際のAnki renderingを確認する。

pilotで発見したルール問題は **`pilot/review.md`** に記録し、v1.0への改訂理由を残す。

v1.0へ進む条件：

- pilot上の会計誤りが0
- ambiguous promptが0
- rendered-card answer leakageが0
- recurring failure patternが明文化済み
- `rules/cloze_rules.md` をv1.0へ一度だけ改訂
- v1.0をfreeze

ANKI-007の完了だけでは、上記のPart 0 + early-commercial representative pilot要件を満たした証拠がない限り、pilot gate PASSとはみなさない。
