# COM-02 Production QA

Task: ANKI-009 / Commercial chapter 02 `収益認識`

Governance: `GOVERNANCE.md`. COM-02 retains its explicitly audited chapter state from ANKI-009; current general rules are authoritative for new work, while this existing batch is migrated when a newer rule is explicitly applied to it.

Source baseline:
- repository: `xihangzou/bookkeeping-integrated`
- commit: `569ed7b82e729334e1472286eaca7c4352e6fbdb`
- canonical source path in Note rows: `merged/textbook.md`
- chapter source: `commercial/chapter02.md`
- canonical inventory: `inventory/topic_inventory/COM-02.tsv`

## Result

- approved production Notes: **17**
- generated Cloze cards: **17**
- canonical included COM-02 ALPs: **32**
- mapped included ALPs: **32**
- unmapped included ALPs: **0**
- ALPs mapped more than once: **0**
- approved multi-ALP Notes: **11**
- approved single-ALP Notes: **6**
- excluded decorative-example rows: **2**
- journal-entry Notes reviewed: **5**
- formula Notes reviewed: **3**
- approved Notes using more than one Cloze index: **0**
- exact duplicate Cloze answer spans within an approved Note: **0**
- exact rendered-text duplicates: **0**
- production lifecycle: all rows `Status=approved`, `QA=pass`

No COM-02 pilot IDs existed, so stable production IDs are allocated deterministically as `BK-COM-02-0001`–`BK-COM-02-0017` in primary canonical ALP order.

## Consolidation map

| Note | ALP mapping | Retrieval unit |
|---|---|---|
| `BK-COM-02-0001` | 0001, 0002 | 履行義務の意味と収益認識時点 |
| `BK-COM-02-0002` | 0003 | 掛売上の認識と後日回収 |
| `BK-COM-02-0003` | 0004, 0005 | 前受金から商品引渡時の売上認識 |
| `BK-COM-02-0004` | 0006 | 売上戻りの逆仕訳 |
| `BK-COM-02-0005` | 0007 | 当社負担の売上諸掛り |
| `BK-COM-02-0006` | 0008, 0009 | 出荷・着荷・検収の流れと認識基準 |
| `BK-COM-02-0007` | 0010, 0014 | 割戻しと変動対価の用語関係 |
| `BK-COM-02-0008` | 0011, 0012, 0013 | 返金負債と売上認識額 |
| `BK-COM-02-0009` | 0015, 0016 | 仕入割戻しの処理と仕入戻しとの対応 |
| `BK-COM-02-0010` | 0017, 0024 | 一時点・一定期間の収益認識と先受対価 |
| `BK-COM-02-0011` | 0018, 0019 | 無料保証と有償保証の会計上の区別 |
| `BK-COM-02-0012` | 0020, 0021, 0022 | 有償保証の契約負債と期間配分 |
| `BK-COM-02-0013` | 0023 | 商品販売と有償保証の複数履行義務 |
| `BK-COM-02-0014` | 0025 | サービス業の主要勘定科目 |
| `BK-COM-02-0015` | 0026, 0027, 0028, 0032 | サービス業の前受・繰延原価・履行時振替の一連処理 |
| `BK-COM-02-0016` | 0029, 0030 | 部分履行の収益・原価測定 |
| `BK-COM-02-0017` | 0031 | 仕掛品を経由しない例外 |

The non-contiguous multi-ALP mappings (`0010+0014`, `0017+0024`, `0026+0027+0028+0032`) are intentional. Each pair/group is one coherent accounting retrieval unit; `ALP_IDs` preserves exact source traceability while the first ALP supplies deterministic primary `Section` context.

## Cloze / recall QA

- Every approved Note generates one review card using only `c1`.
- Tightly coupled debit/credit pairs, recognition branches, formulas, and ordered service-accounting stages use same-index grouping to avoid sibling-answer leakage.
- Supporting definitions and examples remain visible or in `Extra` when they do not justify another review rotation.
- Cloze targets are canonical accounting terms, complete journal-entry patterns, recognition consequences, or short formulas rather than grammatical fragments.
- No exact Cloze answer span is repeated within the same approved Note.
- No duplicate rendered Note text exists within COM-02.

## Accounting QA

Reviewed against the pinned chapter source:

1. **Recognition timing** — revenue is recognized when the relevant performance obligation is satisfied; cash collection alone does not create a second sale.
2. **Prepayments** — consideration received before delivery/service remains a liability (`前受金` / `契約負債`) until performance.
3. **Returns and selling costs** — sales returns reverse the relevant sale; seller-borne shipping-type costs are separate expenses.
4. **Shipment bases** — shipment, arrival, and acceptance bases map to their corresponding recognition points.
5. **Rebates** — expected sales rebates reduce recognized revenue and create `返金負債`; purchase rebates reduce `仕入` when confirmed.
6. **Paid warranties** — paid warranty service is a separate performance obligation and is recognized over the service period; the allocation formula is preserved.
7. **Service businesses** — pre-revenue consideration, deferred service costs, completion entries, partial-completion revenue/cost allocation, and the direct-`役務原価` exception are internally consistent.

No local debit/credit, recognition-timing, formula, or amount-relationship blocker was found.

## Validation

`python scripts/validate_com02_production.py` checks:

- exact field order and stable COM-02 Note-ID set;
- pinned source fields and chapter metadata;
- canonical included ALP existence and canonical ALP order;
- exactly-once approved coverage for all 32 included ALPs;
- first-ALP `Section` consistency;
- required mechanically derived tags;
- `Status=approved` / `QA=pass` lifecycle;
- one generated card per approved Note under v1.2;
- duplicate Cloze-answer and exact rendered-text checks;
- deterministic chapter metrics.

The GitHub Actions production workflow runs this validator together with the existing FND-00 and COM-01 regression validators.
