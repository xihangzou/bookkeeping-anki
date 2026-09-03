# Cloze Rules

Status: **Current authoritative Cloze rules — living specification**
Governance: `GOVERNANCE.md`

## 1. Objective

Cloze は文章の穴埋めではなく、会計知識を正確に想起するための retrieval prompt として設計する。

最優先順位は次の通り。

1. 何を思い出すべきか明確
2. 正答が一意または実質一意
3. 会計上重要な情報を想起させる
4. 不要な暗記負荷を増やさない
5. 後続の2級・CPA学習でも崩れない理解を作る
6. 反復後も意味のある retrieval を要求する

本ルールは `SPEC.md`、`rules/coverage_rules.md`、`schema/note_schema.yaml`、`pilot/PLAN.md` と整合して運用する。矛盾を発見した場合はローカル判断で補完せず、明示的に解消する。

v1.0 は `pilot/review.md` に記録された ANKI-PILOT-003/004 の実測結果を根拠として成立した初期production baselineである。現在はliving specificationとして、pilot・production audit・後続chapterの実測結果に基づき本ルール自体を明示的に更新する。schema/tag/source/TSVのlineage要件は、変更不要だったというv1.0時点の判断を履歴として保持しつつ、将来のreviewed changeを妨げない。

## 2. Atomicity

原則として `1 Note = 1 coherent recall unit`。

- 1つの定義
- 1つの認識ルール
- 1つの仕訳パターン
- 1つの計算関係
- 1つの比較軸
- 1つの手続ブロック

複数論点を1 Noteに混ぜない。ただし、分離すると関係性自体が失われる場合は同一Noteに置く。

### Multi-ALP Notes

1 Note に複数 ALP を map してよいのは、複数 ALP が同一の coherent recall unit を構成するときだけである。

- 各 ALP は個別に canonical inventory へ解決できなければならない。
- ALP をまとめる理由は「同じ文章に置きやすい」ではなく「一体として想起する必要がある」でなければならない。
- 1つの generated card が複数の独立判断を同時に要求するなら Note を分割する。
- 分割すると sibling answer が漏れる、または会計上不可分な関係が失われる場合は same-index grouping を優先する。

schema の `ALP_IDs`、primary source context、canonical source order は変更しない。

## 3. Cloze count

原則は **1〜3 cloze groups / Note**。

4個以上を許容する主なケース：

- 一連の手続順序
- 財務諸表の構造
- 同一ルール内の不可分な複数要素
- 比較表の1行をまとめて覚える場合

カード数を増やすためだけに `c1`, `c2`, `c3` を分けない。

cloze group 数ではなく、generated card ごとの retrieval unit を評価する。1 Note に複数 group があっても、各 card が独立して有用でなければ group を統合または Note を再設計する。

## 4. Anki Cloze semantics and numbering

Ankiでは、異なるCloze番号は原則として異なるカードを生成する。同じ番号を複数箇所に使うと、その箇所は同じカード上で同時に隠れる。

### Same number

同時に一塊として再生できるべき情報は同じ番号にする。

```text
資産は通常 {{c1::借方}} 側に位置し、増加は {{c1::借方}} に記入する。
```

same-index masking を優先する条件：

- 片方を表示するともう片方の答えが実質的に決まる
- paired relation の独立 recall に追加価値がほぼない
- journal entry の debit/credit sides が1つの不可分な entry unit である
- comparison の複数 branch が同じ answer を共有し、別 card 化すると sibling leakage が生じる
- parallel formula の一方を表示すると、もう一方の operands / operation がほぼ露出する

### Different numbers

独立して問う価値がある情報は別番号にする。

```text
売掛金は {{c1::資産}} であり、通常は {{c2::借方}} 残高を持つ。
```

別番号を採用するには、各 `cN` の rendered state で次を満たす必要がある。

1. visible sibling answer を見ても target の recall が非自明である。
2. hidden member 自体に独立した retrieval value がある。
3. grammar、position、parallel structure だけでは答えが決まらない。
4. 同じ proposition を別 context の card がすでに実質同一に問うていない。

単に「別々に覚えられる」だけでは different-index の根拠にならない。

## 5. Context sufficiency and unique answer class

禁止：

```text
{{c1::買掛金}}
```

許容：

```text
商品を掛けで仕入れたとき、代金の支払義務は {{c1::買掛金}} として処理する。
```

穴を表示した状態でも、何を答えるカードか判断できなければならない。

さらに、Cloze は **unique semantic answer class** を持たなければならない。

禁止例：

```text
内容確定後は {{c1::本来の勘定科目}} に振り替える。
```

具体的な transaction facts がないため、複数の勘定科目・表現が正答になり得る。

placeholder 表現（例：`適切な勘定科目`、`本来の科目`、`正しい処理`）を target にしてよいのは、visible context が semantic answer を一意に決定するときだけである。

## 6. Do not over-delete

原則として文全体・仕訳全体・公式全体を1つの巨大Clozeにしない。

悪い例：

```text
商品100円を掛けで仕入れた。
{{c1::借方 仕入100 / 貸方 買掛金100}}
```

ただし、複数要素が1つの不可分なretrieval targetである場合は、必要な要素を同じCloze番号で隠すことがある。重要なのは「隠す範囲を大きくすること」ではなく、「何を一体として再生すべきか」を先に決めることである。

大きな same-index answer は自動的に不適切ではない。分割による leakage と、統合による recall load を比較し、より有効な方を採用する。

## 7. Journal-entry rules

仕訳ALPでは、作成前にretrieval targetを次のいずれかとして明確化する。

1. 仕訳全体の組合せ
2. 独立して想起する価値がある一方の勘定科目
3. 金額・計算要素
4. 借貸方向そのもの

### Whole coupled entry

借方・貸方の組合せ全体を再生することが目標なら、片側だけ表示されて他方の答えを漏らす構造を避ける。

```text
商品100円を掛けで仕入れた。
借方：{{c1::仕入}} 100
貸方：{{c1::買掛金}} 100
```

multi-field same-index answer は、複数 field が1つの inseparable entry / paired-entry unit を構成する場合に許容する。

### Coupled answer size

answer に **4つ以上の account positions** が含まれる場合は、次を必ず確認する。

- 1つの compound entry として一体再生することが学習目標か
- 安全に分割しても counterpart leakage が起きないか
- 分割すると別の誤った accounting pattern を学習させないか

安全に分割できるなら分割する。分割が leakage または会計上の関係破壊を生む場合は same-index grouping を維持してよい。必要に応じて `Extra` に entry decomposition / reasoning を示す。

### Independent side recall

一方の勘定科目だけを独立して問うこと自体にretrieval価値がある場合は別番号を使ってよい。

```text
商品100円を掛けで仕入れた。
借方：{{c1::仕入}} 100
貸方：{{c2::買掛金}} 100
```

ただし `c1` card では貸方、`c2` card では借方が見える。その表示が正答をほぼ決定してしまう場合は採用しない。

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

## 12. Formula and calculation cards

公式全体を一度に隠すより、意味構造を残す。

```text
売上原価 = {{c1::期首商品棚卸高}} + {{c2::当期商品仕入高}} - {{c3::期末商品棚卸高}}
```

ただし公式を一体として再生することが重要な場合は、同一Cloze groupにまとめてもよい。

### Parallel formulas

parallel formula を different-index で同一 Note に置く場合、visible sibling formula が hidden formula の operands / operation を実質的に開示しないことを確認する。

開示する場合は次のいずれかを行う。

- same-index でまとめる
- discriminating context を追加する
- Note を分割する
- 片方の retrieval unit が重複なら削除する

### Formula recall vs application

同一公式を別 context で再度 Cloze 化するだけでは追加 coverage とみなさない。2枚目を残すなら、少なくとも次のいずれかが必要である。

- numeric application
- condition selection
- exception
- multi-step calculation
- materially different decision

数値例は、公式適用に追加の判断がある場合のみ別Note化する。単純代入でも cross-context semantic duplicate を解消する目的で application recall に変換する場合は、式そのものではなく計算結果または判断を target にする。

## 13. Procedure cards

順序自体が論点の場合は系列として出す。

```text
簿記の基本的な一巡：
取引 → {{c1::仕訳}} → {{c2::勘定への転記}} → {{c3::試算表}} → {{c4::決算手続き}} → {{c5::財務諸表}}
```

単なる箇条書き一覧は、順序が試験・理解上重要でなければ無理に順序カードにしない。

### Positional sequence cueing

visible neighboring stages が missing stage の「位置」を示すこと自体は直ちに leakage ではない。各 card で exact stage wording / function の substantive recall がまだ必要なら different-index を許容する。

一方、neighbors を見るだけで答えがほぼ決まる場合は次を検討する。

- whole-sequence recall
- same-index grouping
- discriminating prompt
- sequence を意味単位に分割

## 14. Comparison cards

比較対象と **1つの named comparison axis** を明示する。

```text
三分法では商品仕入時に {{c1::仕入}} を用いるのに対し、売上原価対立法では {{c2::商品}} を用いる。
```

すべての branch は同じ answer category を返さなければならない。たとえば timing の比較なら全 branch が timing を答え、account/object と混在させない。

複数 branch が同じ answer を持ち、別番号にすると sibling answer が露出する場合は、その共有 proposition を同じ Cloze group で mask する。

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

```text
仕訳を勘定へ転記するとき、各勘定には取引日・{{c1::相手科目}}・金額を記入する。
```

```text
借方合計が貸方合計を上回る勘定は {{c1::借方残高}} となる。
```

仕訳そのものを再生する場合は `journal_entry`、帳簿上の転記・集計・残高処理が主題なら `ledger` とする。

## 18. Financial-statement cards

`financial_statement` は、財務諸表上の表示位置、構造、項目間関係、報告目的を扱う。

```text
貸借対照表では、資産は {{c1::借方側}}、負債・純資産は {{c2::貸方側}} に表示する。
```

構造全体の相互関係を一体として覚える必要がある場合は同じ番号にまとめる。独立して問う場合は別番号にしてよいが、各カードで他方の表示が答えを漏らさないか確認する。

## 19. Cost-accounting cards

`cost_accounting` は、工業簿記に固有の原価の集計・配賦・振替・原価流れ・部門/製品間関係を扱う。

単一の数式だけが主題なら `formula`、単一の配賦額決定が主題なら `measurement`、仕訳再生が主題なら `journal_entry` を優先する。`cost_accounting` は、原価計算固有の流れや関係性がprimary retrieval targetである場合に使用する。

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

表由来の card は、label や row heading が target を自動的に連想させ、反復後に retrieval がほぼ不要にならないか確認する。

## 21. Numerical examples

数値だけ変えた同型例は原則1つに統合する。

複数例を残す条件：

- 条件分岐が異なる
- 複合仕訳になる
- 端数・配賦・差額など新しい判断が加わる
- 誤りやすい境界条件を示す
- formula recall と distinct application recall を明確に分ける

## 22. Extra field and answer equivalence

`Extra` は以下に使用できる。

- なぜそうなるか
- 計算過程
- 仕訳分解
- common error
- textbook内の関連節
- CPA学習への短いbridge
- useful な acceptable answer variants

禁止：Cloze側で問うべき答えをExtraだけに置くこと。

### Semantic answer acceptance

canonical Cloze text は intended meaning を示すが、原則として唯一の literal string を強制しない。

- `販売目的` と `販売する目的` のように会計上同義なら semantic equivalent として扱う。
- 長い canonical phrase の modifier が tested distinction でないなら、短い accounting-equivalent answer を誤答扱いしない。
- exact terminology 自体が学習目標なら、そのことが prompt から明確でなければならない。

## 23. Duplicate control at retrieval-unit level

意味的に同じ Recall Unit を、語順や数値だけ変えて複数Noteにしない。

重複判定は **Note 単位ではなく generated-card / retrieval-unit 単位** で行う。1 Note の一部だけが別 Note の card と重複する `NOTE_PARTIAL_DUPLICATE` も検出対象である。

重複候補は次の順で処理する。

1. 完全重複 → 1 retrieval unitへ統合
2. 同じ事実・異なる文脈 → second card が新しい retrieval operation を追加するか確認
3. condition / application / exception / decision が materially different → 別 card として保持
4. 文脈だけ異なり答える proposition が同じ → merge/remove、または distinct application へ再設計

ALP coverage を維持するために重複 card を残す必要はない。複数 ALP は1つの coherent Note / retrieval unit に map できる。

## 24. Ambiguity, leakage, and retrieval-value test

Note作成時に次を確認する。

- 正答候補が複数ないか
- semantic answer class が一意か
- textbook用語とカード用語が一致しているか
- 文脈なしに穴の種類が推測不能ではないか
- 同義語を不当に誤答扱いしないか
- 単位・期間・主体が明確か

異なるCloze番号を含むNoteでは、**生成される各 `cN` カードを個別に確認する**。

各カードについて：

- 他のClozeの表示答えが対象Clozeを実質的に漏らしていないか
- 文法・語尾・レイアウトだけで答えが推測できないか
- 片側が見えることで仕訳・比較・構造の答えが一意に決まってしまわないか
- 隠した範囲が大きすぎず、かつ断片的すぎないか
- visible cue が反復後に target recall をほぼ自動化していないか
- cross-Note / sibling-card semantic duplicate がないか

### Retrieval value

正確で coverage-relevant でも、visible cue から answer association が機械的に出るだけの card は増やさない。

低 retrieval value の card を残すのは、explicit coverage 上その proposition 自体を独立して想起する必要がある場合に限る。可能なら、単純 label association よりも condition、contrast、decision、reasoning を問う形へ再設計する。

answer leakage がある場合は、同一番号への統合、文面再設計、Note分割、または不要 card の削除で解消する。

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

## 26. Historical v1.0 pilot validation gate

representative pilot は Part 0 + early commercial bookkeeping の **40 Notes** を使用し、ANKI-PILOT-003/004 で generated Cloze cards を rendering 単位で検証した。

pilot evidence は `pilot/card_validation.tsv`、`pilot/VALIDATION.md`、`pilot/review.md` に保持する。

v1.0 へ進む条件：

- pilot上の会計誤りが0
- ambiguous prompt の unresolved blocking finding が0
- rendered-card direct answer leakage の unresolved blocking finding が0
- recurring failure pattern が明文化済み
- semantic duplicate が解消または明示的に distinct retrieval operation へ変換済み
- canonical ALP IDs / source mappings が不変

ANKI-PILOT-004 後の corrected pilot は **40 Notes / 62 generated cards、0 major、0 blocking** であり、この v1.0 の根拠となる。

Pilot corpus は historical baseline evidence として `Status=pilot` / `QA=pending` のまま保持してよい。production へ再利用する場合は、再利用時点のcurrent authoritative rulesとstable ID/source-mapping要件を満たしたものだけを昇格させる。

## 27. ANKI-PILOT-005 decision matrix

| Pilot finding family | v1.0 treatment |
|---|---|
| `POSITIONAL_SEQUENCE_CUE` | §13: neighbors が位置だけを示す場合と答えを実質開示する場合を区別し、後者は grouping / redesign |
| `PARALLEL_RELATION_CUE` | §4: paired members が mutually revealing なら same-index を優先 |
| `PARALLEL_FORMULA_CUE` | §12: sibling formula が hidden operation を開示する場合は grouping / context / split |
| `LARGE_COUPLED_ANSWER` | §7: 4+ account positions は分割可能性を必須確認、不可分なら same-index を許容 |
| `SYNONYM_VARIANT` / `ANSWER_OVERSPECIFIED` | §22: canonical answer は原則 semantic target、literal-only grading は exact terminology が target のときのみ |
| `SEMANTIC_DUPLICATE` / `NOTE_PARTIAL_DUPLICATE` | §23: generated-card / retrieval-unit level で deduplicate |
| `COMPARISON_AXIS_MISMATCH` | §14: 全 branch を1 named axis / answer category に統一 |
| `ANSWER_FORM_AMBIGUITY` | §5: unique semantic answer class を必須化 |
| `LOW_RETRIEVAL_VALUE` | §24: repeated review 後も meaningful retrieval を要求する utility check |

### Explicit no-change decisions

pilot evidence から次の contract 変更は要求されなかった。

- `schema/note_schema.yaml` field set / allowed values
- tag namespaces / `Status` / `QA` fields
- deterministic TSV serialization
- pinned source fields / canonical ALP source traceability

ANKI-PILOT-006 ではこれらの semantics を変更せず、schema version/lifecycle metadata を当時のv1.0 production baselineとして記録した。この判断はhistorical evidenceであり、後続のreviewed schema/rule変更を禁止しない。

## 28. Historical ANKI-PILOT-006 baseline decision

The final pilot gate passed and established **v1.0** as the initial chapter-wide production baseline. Under current governance this is a historical milestone, not a permanent semantic freeze.

Freeze evidence:

- corrected pilot: **40 Notes / 62 generated cards**;
- accounting failures: **0**;
- source-traceability failures: **0**;
- major findings: **0**;
- blocking findings: **0**;
- recurring/minor finding families have explicit rule treatment or documented no-change decisions;
- canonical ALP IDs and source mappings remain unchanged;
- `rules/coverage_rules.md`, `schema/note_schema.yaml`, and `SPEC.md` were aligned at the historical v1.0 production gate.

ANKI-007 onward was authorized by that historical gate. Current and future generation must use the latest merged authoritative rules. Semantic changes must still be explicit, reviewed, validated, and migrated where necessary, but no permanent v1.0 freeze or special later reviewed exception mechanism applies.
