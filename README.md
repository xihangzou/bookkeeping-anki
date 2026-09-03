# bookkeeping-anki

`xihangzou/bookkeeping-integrated/merged/textbook.md` を唯一の教材ソースとして、簿記2級・3級の全内容を必要十分に想起できる Anki Cloze デッキを構築するリポジトリ。

最終目標は CPA 学習へ進むための簿記基礎を100%定着させること。ここでいう「簿記初級」は日商簿記2級・3級の統合範囲、すなわち `textbook.md` 全内容を指す。

## Source of truth

- Repository: `xihangzou/bookkeeping-integrated`
- File: `merged/textbook.md`
- Baseline commit: `569ed7b82e729334e1472286eaca7c4352e6fbdb`
- Structure: Part 0 簿記の基礎 / Part I 商業簿記 / Part II 工業簿記

カードは必ずソース位置へ追跡可能にし、ソースにない論点を勝手に追加しない。CPAへの橋渡し情報は `Extra` に補助情報として置けるが、coverage 判定には含めない。

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
4. 1つの小さな想起単位へ変換する。
5. Anki Cloze Note を生成する。
6. coverage / 会計処理 / Cloze品質を別々にQAする。

カード数は先に決めない。必要十分な coverage の結果として決まる。

## Repository layout

```text
bookkeeping-anki/
├── README.md
├── SPEC.md
├── TASKS.md
├── rules/
│   ├── cloze_rules.md
│   └── coverage_rules.md
├── schema/
│   └── note_schema.yaml
├── inventory/
├── cards/
├── pilot/
├── qa/
└── export/
```

## Workflow

`Specification -> Structure inventory -> Topic inventory -> Pilot -> Rules v1.0 -> Full generation -> Cross-chapter normalization -> QA -> Export`

Cloze規則は最初に v0.9 として固定し、pilot 後に一度だけ v1.0 へ改訂する。全量生成開始後は原則として仕様変更しない。
