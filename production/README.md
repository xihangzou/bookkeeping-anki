# Production Notes

Canonical production Cloze-note batches live under `production/notes/` as UTF-8 TSV files following the current schema in `schema/note_schema.yaml`.

Repository-wide governance is defined in `GOVERNANCE.md`. The sole current Markdown authority for card design, coverage, active-deck integration, duplicate control, recall precision, formulas, and journal-entry masking is:

- `rules/anki_card_rules.md`

The former standalone rule paths are compatibility/history pointers only.

## Conventions

- one chapter/part batch per TSV file;
- stable Note IDs are immutable; deprecated IDs are never reassigned to unrelated content;
- source anchors are recovered through canonical `ALP_IDs`;
- existing batches retain pinned source provenance until an explicit source-baseline migration;
- chapter QA lives under `production/qa/`;
- active card count is the number of distinct Cloze indices, while Cloze-span count tracks masked answer units.

## Living-rule application

`rules/anki_card_rules.md` is authoritative for new generation. Existing batches retain explicit audited states and are migrated deliberately when a newer rule is applied to them.

Rule changes should:

1. be written into `rules/anki_card_rules.md` rather than a new overlay file;
2. update validators when mechanically enforceable;
3. migrate affected chapter batches explicitly rather than silently rewriting history;
4. preserve historical audit metrics and stable-ID/source lineage.

`FREEZE.md` is the historical v1.0 pilot-baseline record only.

## Integration-first, content-preserving design

Card-count control comes primarily from coherent integration:

1. preserve useful examinable ALPs and their material source propositions;
2. combine facts belonging to one retrieval frame;
3. use separate short `{{c1::...}}` spans for parallel answers on the same card;
4. add another Note only when integration would become incoherent or overloaded.

An ALP mapping alone is not enough: the material proposition must be recoverable from active Note `Text`; `Extra` is supporting context rather than a substitute for source containment.

## Current recall rules: production summary

The authoritative details are in `rules/anki_card_rules.md`. In particular:

- Cloze answers use the smallest uniquely recoverable accounting unit;
- retrieval subjects and method/context frames remain visible;
- canonical accounting labels are preferred when label identification is the useful operation;
- broad action answers such as `仕訳を行う` / `仕訳を行わない` / `処理する` are normally forbidden;
- compound terms keep redundant fixed heads visible when the remaining discriminator is unique;
- formula operators remain visible and operands are separately Clozed;
- timing/relational modifiers stay outside formula-operand Clozes when they already identify the operand role;
- procedure frames remain visible and only short sequence-critical labels are hidden;
- compound comparison cells are decomposed into separate semantic spans;
- ordinary new/re-audited journal entries keep debit/credit syntax visible and Cloze account names separately with the same `c1` when one coherent entry is being recalled;
- the historical compact whole-entry Cloze exception is retired for new/re-audited production;
- visible-answer leakage and ambiguity are checked at generated-card level;
- duplicates are controlled at retrieval-unit level, not merely Note level;
- every mapped included ALP must remain materially represented in active `Text`.

FND-00 and COM-01 remain general style references for context-rich, same-card, short-answer Notes. Later chapter audits contributed rules now integrated into the single authoritative rule document rather than forming separate rule authorities.

## Historical audit lineage

FND-00 audit progression remains historical evidence:

- v1.1: 91 -> 57 approved Notes;
- v1.2: 110 -> 58 generated cards;
- v1.3: 18 cards / 36 active ALPs;
- v1.4: 29 cards / 61 active ALPs;
- v1.5: 32 cards / 120 Cloze spans / 91 active ALPs;
- v1.6: 32 approved Notes / 32 cards / 150 Cloze spans / 91 active ALPs.

COM-01 through later commercial batches retain their chapter-local QA and issue/PR histories under `production/qa/` and Git history. ANKI-AUDIT-008 through ANKI-AUDIT-013 supplied precision refinements now incorporated directly into `rules/anki_card_rules.md`.

## Lifecycle

`Status=approved` rows constitute the active deck. `Status=deprecated` rows preserve immutable historical lineage and source traceability but are excluded from active export.

## ANKI-038 normalized corpus

Cross-chapter semantic normalization is recorded in `production/qa/ANKI-038.md`. The normalized corpus has 811 production rows, 735 approved active Notes, 76 deprecated lineage Notes, 743 generated active cards, 2,004 active Cloze spans, and 965 / 965 included ALPs actively mapped with zero orphan ALPs and zero exact duplicate active retrieval propositions.

Corpus-level invariants are enforced by `scripts/validate_corpus_production.py`. Exact duplicates are blockers; semantic similarity candidates are reviewed under the retrieval-unit duplicate rule and either merged or documented as materially distinct retrieval contexts.

The ANKI-038 full-validator gate passes across governance, all 31 production batches, and the corpus-level normalization validator.

## Validation

Production validators live under `scripts/validate_*_production.py` and are wired into `.github/workflows/validate-production.yml`. The consolidated workflow includes every production batch validator plus the corpus-level normalization validator.

All new generation and later QA corrections should validate against the current schema, `GOVERNANCE.md`, and `rules/anki_card_rules.md` semantics before merge.