# Source Structure Inventory

Status: **ANKI-002 in progress**

Source baseline:

- repository: `xihangzou/bookkeeping-integrated`
- commit: `569ed7b82e729334e1472286eaca7c4352e6fbdb`
- merged source: `merged/textbook.md`

## Verified top-level structure

The pinned source has the following order:

1. Part 0 簿記の基礎
2. Part I 商業簿記
3. Part II 工業簿記

The source QA confirms:

- Commercial: chapter00 (序章 / Part 0 foundation) + chapter01–chapter16
- Industrial: chapter01–chapter14
- Numeric H1 chapters in merged textbook: 30
- Total chapter corpus files represented: 31

## Canonical source files

### Foundation / commercial base

- `commercial/chapter00.md`

### Commercial bookkeeping

- `commercial/chapter01.md`
- `commercial/chapter02.md`
- `commercial/chapter03.md`
- `commercial/chapter04.md`
- `commercial/chapter05.md`
- `commercial/chapter06.md`
- `commercial/chapter07.md`
- `commercial/chapter08.md`
- `commercial/chapter09.md`
- `commercial/chapter10.md`
- `commercial/chapter11.md`
- `commercial/chapter12.md`
- `commercial/chapter13.md`
- `commercial/chapter14.md`
- `commercial/chapter15.md`
- `commercial/chapter16.md`

### Industrial bookkeeping

- `industrial/chapter01.md`
- `industrial/chapter02.md`
- `industrial/chapter03.md`
- `industrial/chapter04.md`
- `industrial/chapter05.md`
- `industrial/chapter06.md`
- `industrial/chapter07.md`
- `industrial/chapter08.md`
- `industrial/chapter09.md`
- `industrial/chapter10.md`
- `industrial/chapter11.md`
- `industrial/chapter12.md`
- `industrial/chapter13.md`
- `industrial/chapter14.md`

## Verified boundary titles

- Commercial chapter01: `第1章 商品売買`
- Commercial chapter16: `第16章 製造業会計`
- Industrial chapter01: `第1章 工業簿記の基礎`
- Industrial chapter14: `第14章 本社工場会計`

Additional chapter titles and all H2/H3 heading paths will be populated by direct extraction from the pinned chapter corpus. This file is not complete until every heading path in all 31 chapter files is represented.

## ANKI-002 completion criteria

- [x] source commit pinned
- [x] Part order verified
- [x] 31 canonical chapter files enumerated
- [ ] every chapter title extracted
- [ ] every H2/H3 heading path extracted
- [ ] merged structure reconciled with chapter corpus
- [ ] structure inventory frozen for ANKI-003 decomposition
