# COM-02 Production QA

Status: **PASS target — ANKI-AUDIT-007 current living-rule migration**

Task lineage: ANKI-009 / #10 → ANKI-AUDIT-007 / #77

Governance: `GOVERNANCE.md`. This audit explicitly migrates COM-02 from its historical v1.2 authoring state to the latest merged living rules in `rules/cloze_rules.md`, `rules/coverage_rules.md`, and `rules/exam_yield_rules.md`.

Source baseline:
- repository: `xihangzou/bookkeeping-integrated`
- commit: `569ed7b82e729334e1472286eaca7c4352e6fbdb`
- canonical source path in Note rows: `merged/textbook.md`
- chapter source: `commercial/chapter02.md`
- canonical inventory: `inventory/topic_inventory/COM-02.tsv`

## Result

- approved production Notes: **17**
- generated Cloze cards: **17**
- active Cloze spans: **39** (historical COM-02 state: 32)
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
- exact visible-answer leakage for 2+ character answers: **0**
- exact rendered-text duplicates: **0**
- production lifecycle: all rows `Status=approved`, `QA=pass`

Stable IDs remain `BK-COM-02-0001`–`BK-COM-02-0017`; no COM-02 pilot IDs existed. No source provenance, ALP ID, or chapter-local Note ID was renumbered or reassigned.

## Why spans increased without adding cards

The current rules distinguish **review-card count** from **Cloze-span count**. COM-02 retains one `c1` card per Note, but broad answers were decomposed into short answer units on the same card.

Examples:

- recognition bases: one list-like answer became `{{c1::出荷時}}`, `{{c1::到着時}}`, `{{c1::検収時}}`;
- refund-liability measurement: `売上認識額＝{{c1::販売対価}}－{{c1::将来返金見積額}}`;
- paid-warranty allocation: `{{c1::保証対価}}×{{c1::当期履行期間}}÷{{c1::総保証期間}}`;
- partial service completion: formula terms are itemized and the structurally reused `{{c1::履行割合}}` is hidden in both formula positions.

Thus **32 → 39 spans** represents finer same-card recall, not seven extra review rotations.

## Consolidation map

| Note | ALP mapping | Retrieval unit |
|---|---|---|
| `BK-COM-02-0001` | 0001, 0002 | 履行義務の意味・充足・収益認識時点 |
| `BK-COM-02-0002` | 0003 | 掛売上の認識と後日回収 |
| `BK-COM-02-0003` | 0004, 0005 | 前受金と商品引渡時の売上認識 |
| `BK-COM-02-0004` | 0006 | 売上戻りの逆仕訳 |
| `BK-COM-02-0005` | 0007 | 当社負担の売上諸掛り |
| `BK-COM-02-0006` | 0008, 0009 | 出荷・着荷・検収と認識基準 |
| `BK-COM-02-0007` | 0010, 0014 | 割戻しと変動対価の用語 |
| `BK-COM-02-0008` | 0011, 0012, 0013 | 返金負債と売上認識額 |
| `BK-COM-02-0009` | 0015, 0016 | 仕入割戻しの処理と仕入戻しとの対応 |
| `BK-COM-02-0010` | 0017, 0024 | 一時点・一定期間の収益認識と先受対価 |
| `BK-COM-02-0011` | 0018, 0019 | 無料保証と有償保証の区別 |
| `BK-COM-02-0012` | 0020, 0021, 0022 | 有償保証の繰延べと期間配分 |
| `BK-COM-02-0013` | 0023 | 商品販売と有償保証の複数履行義務 |
| `BK-COM-02-0014` | 0025 | サービス業の主要勘定科目 |
| `BK-COM-02-0015` | 0026, 0027, 0028, 0032 | サービス業の基本仕訳フロー |
| `BK-COM-02-0016` | 0029, 0030 | 部分履行の収益・原価測定 |
| `BK-COM-02-0017` | 0031 | 仕掛品を経由しない例外 |

The non-contiguous mappings (`0010+0014`, `0017+0024`, `0026+0027+0028+0032`) remain intentional coherent integration units. Each mapped ALP's material proposition is now checked against active `Text`, not merely against the mapping field.

## Current-rule Cloze QA

- Every approved Note uses only `c1`, so every Note generates one review card.
- Normal answers are lexical accounting terms or short discriminators; broad explanatory/list/formula spans from the historical state were removed.
- Parallel answers use separate same-index spans rather than one joined answer span.
- Formula operators stay visible and operands are independently masked.
- Retrieval subjects remain visible after all `c1` spans are hidden.
- Exact visible-answer repetition for answers of two or more characters is zero.
- The only long/punctuated answer spans are deliberate compact journal-entry tuples on `0002`, `0004`, `0009`, and `0015`.
- `BK-COM-02-0016` deliberately repeats `履行割合` inside one coherent formula family; both occurrences are hidden on the same card.
- Definitions generally leave descriptive context visible and mask the technical term (`履行義務`, `割戻し`, `変動対価`).

## Material ALP-containment QA

All 32 included ALPs were re-read against the inventory summaries and pinned source. Material distinctions retained in active `Text` include:

1. **履行義務** — customer promise, satisfaction terminology, and recognition timing.
2. **掛売上** — delivery-time sale entry plus no second revenue recognition on collection.
3. **前受金** — liability before delivery, revenue recognition on delivery, and partial-prepayment settlement.
4. **返品 / 売上諸掛り** — reverse sale entry and seller-borne selling costs as separate expenses.
5. **認識基準** — shipment → arrival → acceptance flow, acceptance meaning, and all three recognition timings.
6. **売上割戻し** — rebate definition, variable consideration, refund liability, revenue-measurement formula, and purchase-rebate treatment.
7. **一定期間の履行** — partial-progress recognition and pre-revenue contract liability.
8. **有償保証** — free-versus-paid classification, separate performance obligation, pre-revenue deferral, period-allocation formula, and multiple-obligation treatment.
9. **サービス業** — `仕掛品` / `役務収益` / `役務原価`, prepayment, cost deferral, completion entries, partial-completion formulas, and direct-cost exception.

`Extra` contains examples and secondary explanation only; it is not the sole location of any mapped ALP's material proposition.

## Accounting QA

Reviewed against the pinned source:

- recognition timing is separated from cash settlement;
- prepayments remain liabilities until performance;
- sales returns reverse the relevant sale;
- seller-borne selling costs remain separate expenses;
- shipment / arrival / acceptance bases match the stated recognition points;
- expected sales rebates reduce revenue and create a refund liability;
- purchase rebates reduce `仕入` when confirmed;
- paid warranty service is recognized over the guarantee period;
- service-business prepayments, deferred costs, completion entries, partial-completion allocation, and the direct-`役務原価` exception are internally consistent.

No local debit/credit, recognition-timing, formula, or amount-relationship blocker remains.

## Deterministic validation

`python scripts/validate_com02_production.py` now checks:

- exact field order and stable Note-ID set;
- pinned source fields and chapter metadata;
- canonical included ALP existence, order, and exactly-once active coverage;
- first-ALP `Section` consistency;
- required tags and lifecycle;
- one-card (`c1`) shape for every approved Note;
- expected **39** Cloze spans;
- lexical/short answer shape outside reviewed compact-entry exceptions;
- formula itemization and approved repeated-term exception;
- exact visible-answer leakage for 2+ character answers;
- removal of superseded broad Cloze patterns;
- explicit material-content requirements for every stable Note;
- duplicate rendered-text checks and deterministic chapter metrics.

Expected output:

```text
COM-02 current-rule production validation: PASS
notes=17 included_alps=32 mapped=32 unmapped=0
generated_cards=17 cloze_spans=39 visible_answer_leakage=0 multi_alp_notes=11
lexical_atomicity=pass formula_itemization=pass compact_entry_exceptions=4 material_containment=pass
journal_entry_notes=5 formula_notes=3
```

The production workflow must also keep FND-00 and COM-01 regression validation green before merge.
