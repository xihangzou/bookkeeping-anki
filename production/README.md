# Production Notes

Canonical production Cloze-note batches live under `production/notes/` as UTF-8 TSV files following the v1.0 field order in `schema/note_schema.yaml`.

The source/schema/stable-ID baseline remains the frozen v1.0 contract. Active-deck selection is governed by the **v1.4 post-freeze exam-yield overlay** in `rules/exam_yield_rules.md`.

## Conventions

- one chapter/part batch per TSV file;
- rows are ordered by canonical ALP source order;
- exact source anchors are recovered through `ALP_IDs` and the canonical inventory;
- stable Note IDs are immutable; retired IDs remain in audit history and are never reassigned to unrelated content;
- chapter-local QA evidence is stored under `production/qa/`.

## Source coverage and active recall

v1.4 keeps separate metrics for:

- **source-reviewed coverage**: every included ALP has been reviewed and remains traceable in production history;
- **active direct-recall coverage**: ALPs represented on `Status=approved` Notes because spaced retrieval is useful.

A deprecated historical row can preserve source traceability without forcing a separate low-yield card. However, v1.4 intentionally uses a more permissive active-recall screen than v1.3: foundational terminology, workflow, ledger structure, period reading, and representative account-selection facts may remain active when they materially help problem solving or comprehension.

## Integration-first card control — v1.4

Reduce card count first by integrating facts that share one natural retrieval frame, then retire only genuinely low-value or redundant direct recall.

Examples:

- `仕訳 / 勘定 / 転記` on one recording-process card;
- main books plus `元丁 / 仕丁` on one posting-reference card;
- subsidiary-book types plus receivable/payable subledger organization on one card;
- three-voucher selection plus the voucher account-field rule on one card.

Integration must not erase the topic or create an overloaded mixed-purpose prompt.

## Cloze lexicality, context, and same-card grouping — v1.4

For facts that remain worth recalling:

- prefer one lexical accounting term / account name / distinguishing prefix per Cloze span;
- split compound answers into same-index spans rather than hiding a list as one span;
- parallel facts that form one coherent retrieval operation stay on the same card by reusing `c1`;
- use `c2+` only for a genuinely independent retrieval operation worth a separate review card;
- after the Cloze is hidden, the visible text must still identify the topic/retrieval frame;
- when direction itself is tested, use `{{c1::借}}方` / `{{c1::貸}}方`, including `{{c1::借}}方残高` / `{{c1::貸}}方残高`;
- track **generated-card count** separately from **Cloze-span count**.

For example, the three-voucher card must visibly say `3伝票制では` and use `{{c1::入金}}伝票`, `{{c1::出金}}伝票`, `{{c1::振替}}伝票` rather than hiding every occurrence of the word `伝票`.

## FND-00 audit result

FND-00 post-production audit stages:

- v1.1: 91 -> 57 approved Notes;
- v1.2: 110 -> 58 generated cards;
- v1.3: 18 approved Notes / 18 cards / 36 active ALPs;
- v1.4: **29 approved Notes / 29 cards / 70 lexical Cloze spans / 61 active ALPs**.

The 91 historical rows remain and all 91 included ALPs remain source-reviewed/traceable. Every approved FND-00 Note uses only `c1`; related lexical answers are represented by multiple `{{c1::...}}` spans on the same card.

## Existing commercial batches

- COM-01 currently reflects v1.2 generation: 38 approved Notes / 38 cards / 52 included ALPs active-mapped.
- COM-02 currently reflects v1.2 generation: 17 approved Notes / 17 cards / 32 included ALPs active-mapped.

v1.4 is the current target for future generation. Existing v1.2 commercial batches should be migrated only through explicit chapter audits so stable IDs and prior QA evidence remain auditable.

## Lifecycle

### `Status=approved`

Approved rows constitute the active study deck. They use `QA=pass` and `status::approved`.

### `Status=deprecated`

Deprecated rows are retained as production history. They:

- keep immutable Note IDs and source-traceable ALP mappings;
- use `QA=pass` after retirement is audited;
- use `status::deprecated`;
- are excluded from active export.

A deprecated stable Note can be reactivated through a reviewed audit when its original retrieval lineage is restored; its ID is never reassigned to unrelated material.

## Current batches

- `notes/FND-00.tsv` — Part 0 / bookkeeping foundations (ANKI-007; audits #56, #58, #62, #66)
- `notes/COM-01.tsv` — Commercial chapter 01 / 商品売買 (ANKI-008; v1.2 generation)
- `notes/COM-02.tsv` — Commercial chapter 02 / 収益認識 (ANKI-009; v1.2 generation)

Run `python scripts/validate_fnd00_production.py` to validate FND-00 historical source coverage, 29/62 lifecycle, 61 active-recall ALPs, **29 generated cards / 70 lexical spans**, same-index parallelism, visible-context cues, debit/credit first-character Clozes, and stable source/tag controls.

Run `python scripts/validate_com01_production.py` and `python scripts/validate_com02_production.py` for the existing v1.2 commercial batches.

Migration records:

- `scripts/migrate_fnd00_v1_2.py` — v1.2 rotation migration;
- `scripts/migrate_fnd00_v1_3.py` — v1.3 minimal/lexical migration;
- `scripts/migrate_fnd00_v1_4.py` — v1.4 balanced/context-preserving migration.