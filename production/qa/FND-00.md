# FND-00 Production QA

Issues: ANKI-007 / #8; post-production audit ANKI-AUDIT-001 / #56

Contracts:
- frozen v1.0 source/schema/Cloze baseline (`FREEZE.md`, `rules/cloze_rules.md`, `rules/coverage_rules.md`, `schema/note_schema.yaml`)
- v1.1 post-freeze active-deck overlay (`rules/exam_yield_rules.md`)

## Audit objective

ANKI-007 established complete Part 0 source coverage, but the first 91-Note production pass still contained several Notes that were technically correct yet inefficient for exam preparation:

- low-retrieval-value introductory terminology;
- repeated general rules represented as separate cards;
- direct label association that did not test an accounting decision;
- oversized memorization lists for expense accounts / ledger fields;
- fragmented definitions that were better tested as one recognition or comparison unit;
- one transaction-duality wording that could mislead learners when they later encounter compound entries.

ANKI-AUDIT-001 therefore optimizes the **active approved deck** while preserving the complete canonical ALP inventory and all stable Note-ID history.

## Before / after

| Metric | ANKI-007 | v1.1 audit |
|---|---:|---:|
| historical production rows | 91 | 91 |
| active `approved` Notes | 91 | **57** |
| `deprecated` audit rows | 0 | **34** |
| canonical included FND-00 ALPs | 91 | **91** |
| ALPs mapped to an approved Note | 91 | **91** |
| active unmapped ALPs | 0 | **0** |
| approved multi-ALP Notes | 0 | **25** |
| stable IDs reused / renumbered | 0 | **0** |

The approved Note count is an audit outcome, not a quota.

## Active-deck targeting decision

Direct Cloze recall is prioritized when it materially supports:

- account selection / classification;
- debit-credit direction;
- recognition timing;
- journal-entry construction and settlement;
- formula/calculation use;
- testable ledger / voucher mechanics;
- discrimination between similar treatments;
- exam-document interpretation;
- terminology and notation needed to parse normal bookkeeping questions;
- durable causal accounting structure useful for later 2級 / CPA study.

Source propositions with lower independent exam yield remain traceable, but are placed in the visible context or `ALP_IDs` of a coherent higher-yield approved Note rather than generating a separate active card.

## Deprecated Notes and replacements

The following 34 stable IDs are retained as `Status=deprecated`, `QA=pass`. Their IDs remain permanently reserved.

| Deprecated Note | Active replacement |
|---|---|
| `BK-FND-00-0001` | `BK-FND-00-0019` |
| `BK-FND-00-0006`, `BK-FND-00-0007` | `BK-FND-00-0037` |
| `BK-FND-00-0020`, `BK-FND-00-0021` | `BK-FND-00-0018` |
| `BK-FND-00-0023` | `BK-FND-00-0003` |
| `BK-FND-00-0031` | `BK-FND-00-0002` |
| `BK-FND-00-0033`, `BK-FND-00-0034`, `BK-FND-00-0035` | `BK-FND-00-0004` |
| `BK-FND-00-0036` | `BK-FND-00-0005` |
| `BK-FND-00-0038` | `BK-FND-00-0025` |
| `BK-FND-00-0040` | `BK-FND-00-0039` |
| `BK-FND-00-0041` | `BK-FND-00-0026` |
| `BK-FND-00-0042` | `BK-FND-00-0043` |
| `BK-FND-00-0045`, `BK-FND-00-0046` | `BK-FND-00-0044` |
| `BK-FND-00-0052` | `BK-FND-00-0053` |
| `BK-FND-00-0056` | `BK-FND-00-0055` |
| `BK-FND-00-0057` | `BK-FND-00-0014` |
| `BK-FND-00-0059` | `BK-FND-00-0058` |
| `BK-FND-00-0060`, `BK-FND-00-0061` | `BK-FND-00-0015` |
| `BK-FND-00-0063`, `BK-FND-00-0065` | `BK-FND-00-0062` |
| `BK-FND-00-0066` | `BK-FND-00-0064` |
| `BK-FND-00-0067` | `BK-FND-00-0068` |
| `BK-FND-00-0076` | `BK-FND-00-0074` |
| `BK-FND-00-0077` | `BK-FND-00-0078` |
| `BK-FND-00-0081`, `BK-FND-00-0082`, `BK-FND-00-0083` | `BK-FND-00-0084` |
| `BK-FND-00-0085` | `BK-FND-00-0086` |
| `BK-FND-00-0087` | `BK-FND-00-0088` |

## Material quality corrections

### 1. Transaction duality accuracy

Old `BK-FND-00-0036` stated that one transaction changes multiple accounts by the same amount. That wording is potentially misleading for compound entries, where individual account amounts can differ.

The active `BK-FND-00-0005` now teaches the durable rule:

- one transaction is recorded on both debit and credit sides; and
- **total debits equal total credits**.

ALP-FND-00-0023 and ALP-FND-00-0024 are both mapped to that approved Note.

### 2. Expense-account memorization

Old `BK-FND-00-0047` required direct recall of a long list of expense-account names.

The revised card tests **account selection from transaction content** with representative cases (travel fare, communications, advertising); the remaining textbook examples stay visible in `Extra`. This tests the accounting operation that exam questions actually require instead of list recitation.

### 3. Debit-credit fragmentation

Separate Notes for:

- asset/liability/equity normal position;
- debit=left / credit=right;
- increase on normal side / decrease on opposite side;
- all-five-element increase direction

were consolidated into `BK-FND-00-0004`. The active card now asks one complete five-element debit-credit rule rather than four overlapping fragments.

### 4. Transaction recognition

Definition + fire/theft positive case + contract-only negative case were consolidated into `BK-FND-00-0037`. The card now tests the actual recognition criterion: whether the five elements change.

### 5. Trial-balance controls

Trial-balance definition, purpose, and aggregate debit-credit equality were consolidated into `BK-FND-00-0044`. The important limitation (balanced totals do not detect every error) remains a separate exception Note `BK-FND-00-0011`.

### 6. Payroll and temporary accounts

- withholding mechanism was merged into the gross-pay / income-tax liability Note;
- employee vs employer social-insurance treatment is now one comparison-like journal-entry Note;
- 仮払金 classification is embedded in its settlement procedure;
- 仮受金 classification is embedded in its settlement procedure;
- correction procedure, formula, and warning are one coherent correction-entry rule.

### 7. Bookkeeping forms and vouchers

Long form-field and label lists were reduced or consolidated:

- journal/general-ledger definitions are one time-order vs account-order Note;
- `元丁` vs `仕丁` is directly tested instead of memorizing every form column;
- subsidiary-book definition is merged into the subsidiary-journal vs subsidiary-ledger distinction;
- hand-note fields emphasize maturity / payment location / disposition rather than every column;
- individual/aggregate posting, aggregation tables, processing order, and subsidiary-ledger exception are one workflow Note;
- document definition is merged into document discrimination; document limitations are merged into document-to-entry reasoning.

## v1.1 mechanical validation

GitHub Actions `Validate production notes` executed `python scripts/validate_fnd00_production.py` successfully on PR #57.

Validator result:

```text
FND-00 v1.1 production validation: PASS
rows=91 approved=57 deprecated=34 included_alps=91 approved_mapped=91 unmapped=0
approved_multi_alp_notes=25 reserved_pilot_only_id=BK-FND-00-0016
approved_journal_entry_notes=8 approved_formula_notes=3
```

The validator enforces:

- the original **91-row stable Note-ID history** remains present;
- `BK-FND-00-0016` remains reserved and unused;
- exactly **57 approved / 34 deprecated** rows;
- deprecated IDs equal the reviewed retirement set;
- approved Notes may map multiple ALPs in canonical source order;
- every one of the **91 included ALPs maps to exactly one approved Note**;
- deprecated mappings do not count as active coverage;
- primary `Section` matches the first mapped ALP;
- source fields remain pinned;
- tags follow the row's approved/deprecated lifecycle;
- every row has valid Cloze syntax and `QA=pass`;
- approved Notes contain no exact rendered-text duplicates.

## Downstream effect

FND-00 now distinguishes **canonical source coverage** from **active study-card count**. Downstream export must include `Status=approved` rows only. The same exam-yield audit rule should be applied during ANKI-008 onward generation rather than waiting for a later cleanup pass.
