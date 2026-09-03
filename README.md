# bookkeeping-anki

`xihangzou/bookkeeping-integrated/merged/textbook.md` を教材ソースとして、簿記2級・3級の全内容を必要十分に想起できる Anki Cloze デッキを構築するリポジトリ。

最終目標は CPA 学習へ進むための簿記基礎を100%定着させること。ここでいう「簿記初級」は日商簿記2級・3級の統合範囲、すなわち `textbook.md` 全内容を指す。

## Source of truth

- Repository: `xihangzou/bookkeeping-integrated`
- File: `merged/textbook.md`
- Current production source baseline: `569ed7b82e729334e1472286eaca7c4352e6fbdb`
- Structure: Part 0 簿記の基礎 / Part I 商業簿記 / Part II 工業簿記

カードは必ずソース位置へ追跡可能にし、ソースにない論点を勝手に追加しない。CPAへの橋渡し情報は `Extra` に補助情報として置けるが、coverage 判定には含めない。

## Governance

このリポジトリは **living specification** 方式で運用する。

- 最新merge済みの `SPEC.md`、`rules/*.md`、`schema/note_schema.yaml`、関連QA/validator が現行基準。
- pilotやproduction auditで改善点が見つかれば、ルール・仕様・schema・QA基準を継続的に更新する。
- v1.0は初期production baselineの履歴であり、恒久的な固定仕様ではない。
- 過去版の再現性はGit履歴、issue/PR、migration、QA記録で確保する。
- stable Note IDの不変性、ID非再利用、source traceability、既存batchのpinned source commitなどのlineage要件は維持する。

詳細は `GOVERNANCE.md`。`FREEZE.md` はv1.0 pilot gateの歴史記録として保持する。

## Goal

100点満点理解とは、`textbook.md` に含まれる全論点について、試験・理解上必要な次の情報を取りこぼさず想起できる状態をいう。

- 定義
- 分類
- 認識条件・タイミング
- 測定・計算方法
- 仕訳
- 手続・順序
- 比較
- 例外・条件分岐
- 理解に不可欠な理由・因果関係

全文を文章単位で暗記することは目的ではない。重複説明・単なる言い換え・学習価値のない数値は統合または除外する。

## Design principle

1. `textbook.md` を見出し単位で構造化する。
2. 各節を Atomic Learning Point に分解する。
3. 必要十分性を判定する。
4. coherent recall unitへ統合する。
5. Anki Cloze Note を生成する。
6. coverage / 会計処理 / Cloze品質を別々にQAする。
7. audit結果を現行ルールへ反映し、必要なbatchを明示的にmigrationする。

カード数は先に決めない。必要十分な coverage と回転効率の結果として決まる。

## Repository layout

```text
bookkeeping-anki/
├── README.md
├── GOVERNANCE.md
├── SPEC.md
├── FREEZE.md
├── TASKS.md
├── rules/
│   ├── cloze_rules.md
│   ├── coverage_rules.md
│   └── exam_yield_rules.md
├── schema/
│   └── note_schema.yaml
├── inventory/
├── pilot/
├── production/
├── qa/
└── export/
```

## Workflow

`Specification -> Structure inventory -> Topic inventory -> Pilot -> Initial production baseline -> Full generation -> Iterative audits / rule updates -> Cross-chapter normalization -> QA -> Export`

ルールはpilot後に一度だけ固定するのではなく、実データの監査結果に応じて更新する。変更は必ず明示的に文書・validator・migrationへ反映し、既存production batchへの適用範囲を記録する。
