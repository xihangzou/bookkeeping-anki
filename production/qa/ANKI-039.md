# ANKI-039 — Journal-entry accounting QA

Result: **PASS**  
Issue: #40  
Normalized baseline: ANKI-038 / #39  
Final validation commit: `6e87a2e503eb192ba62ea1e140dd28642e9c9bee`  
GitHub Actions: `Validate production notes` run 363 — **success**

## Authoritative inputs

- normalized active production corpus after ANKI-038;
- pinned textbook baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`;
- canonical `inventory/topic_inventory/*.tsv` ALP inventory and source anchors;
- `GOVERNANCE.md`;
- `SPEC.md`;
- `rules/anki_card_rules.md`;
- `schema/note_schema.yaml`;
- chapter production validators plus `scripts/validate_corpus_production.py`.

Historical whole-entry Cloze exceptions are not current authority.

## Reproducible audit population

Run:

```bash
python scripts/validate_journal_production.py
```

The population is the union of every active approved Note that satisfies at least one of:

1. primary `Type == journal_entry`;
2. explicit debit/credit journal syntax in `Text`;
3. mapping from an included canonical ALP whose primary type is `journal_entry`.

This prevents a mistyped or integrated Note from escaping the audit merely because its Note-level primary type is not `journal_entry`.

Final population:

- audited Notes: **167**;
- primary `journal_entry` Notes: **136**;
- included canonical journal-entry ALPs: **167**;
- journal-entry ALPs represented in the audited population: **167 / 167**;
- Notes with explicit debit/credit syntax: **142**;
- explicit journal pairs structurally checked: **149**;
- visible simple-entry amount pairs mechanically balance-checked: **2**.

The validator prints the complete stable-ID population grouped by batch on every run.

## Accounting checks

The corpus-wide journal validator and the chapter validators jointly recheck:

- inclusion of every journal-entry ALP / Note dependency;
- debit/credit labels and account placement;
- account-level Cloze masking with visible debit/credit syntax;
- coherent same-index grouping within each journal pair, while allowing separate independent entries in one Note to use different indices;
- no debit/credit label or whole journal tuple hidden inside a Cloze;
- no amount bundled into an account-name Cloze;
- simple visible debit/credit amount equality where the syntax permits deterministic parsing;
- source repository / pinned commit / source-path traceability;
- active lifecycle and QA state;
- chapter-specific source-aligned accounting assertions, including recognition, adjustment/closing/transfer/correction treatment, compound-entry content, and amount semantics encoded by the batch validators;
- ALP mapping and stable-ID invariants;
- corpus-level orphan, duplicate-ID, and active-proposition normalization invariants.

All 31 chapter validators, governance validation, corpus normalization validation, and the journal validator passed together in Actions run 363.

## Defect log

Corpus defects are counted as distinct Note/category defect instances.

| Note | Category | Detected defect | Correction | Recheck |
|---|---|---|---|---|
| `BK-COM-01-0008` | journal Cloze structure | Two closing entries hid each entire debit/credit tuple inside one Cloze. | Kept debit/credit labels and separators visible; Clozed `仕入` / `繰越商品` at account level with coherent `c1` grouping. | PASS |
| `BK-COM-01-0009` | journal Cloze structure | Cost-of-sales-method sale and cost-transfer entries hid whole tuples and bundled amounts inside the Cloze. | Converted to visible debit/credit syntax with account-level `c1` targets; amounts remain visible. | PASS |
| `BK-COM-01-0009` | source / amount integrity | The production example used `100,000` / `60,000`, while the pinned textbook example is a credit sale of `20,000` with inventory cost `12,000`. | Re-anchored the example to `20,000` sales and `12,000` cost while preserving the same stable ID and ALP mapping. | PASS |

Defect count by category:

- journal Cloze-structure defects: **2**;
- source / amount-integrity defects: **1**;
- debit/credit-direction defects remaining after recheck: **0**;
- account-selection defects remaining after recheck: **0**;
- recognition-timing defects remaining after recheck: **0**;
- compound/special-entry defects remaining after recheck: **0**.

Total corpus defect instances detected: **3** across **2 Notes**.  
Corrected and rechecked Notes: **2**.  
Unresolved accounting defects: **0**.

## Audit-tool refinement

The first corpus-wide validator run correctly exposed the two COM-01 production defects, but an early implementation also produced three validator false positives:

- `BK-COM-13-0038`: `1/12` was initially mistaken for a debit/credit tuple separator;
- `BK-COM-15-0023` and `BK-COM-15-0024`: independent journal pairs using `c1` / `c2` / `c3` were initially treated as if the entire Note had to use one index.

The validator was corrected to recognize a whole-entry Cloze only when debit/credit labels occur inside the hidden span and to enforce same-index grouping **per coherent journal pair**. The affected production Notes were unchanged because their accounting/Cloze design already satisfied the current rules. The refined validator then passed the full corpus.

## Post-correction corpus invariants

`python scripts/validate_corpus_production.py` after the journal corrections reports:

- production rows: **811**;
- approved active Notes: **735**;
- deprecated lineage Notes: **76**;
- approved cards: **743**;
- approved Cloze spans: **2008**;
- included ALPs actively mapped: **965 / 965**;
- orphan ALPs: **0**;
- multiply mapped active ALPs: **0**;
- duplicate active Note IDs: **0**;
- exact duplicate active retrieval propositions: **0**.

The increase from the ANKI-038 historical snapshot of 2004 to 2008 active Cloze spans is solely the account-level decomposition of the two corrected COM-01 whole-entry Clozes; Note/card counts, stable IDs, and ALP mappings are unchanged.

## Completion evidence

- audited Note count: **167**;
- defect count by category: **2 journal-Cloze structure + 1 source/amount integrity**;
- corrected/rechecked Note count: **2**;
- unresolved accounting defect count: **0**;
- stable IDs / ALP mappings / source traceability: **preserved**;
- final result: **PASS**.

ANKI-039 is complete. ANKI-040 may continue formula/calculation QA; ANKI-041 must still wait for ANKI-040 before finalizing recall-quality QA.