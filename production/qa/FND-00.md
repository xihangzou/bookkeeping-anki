# FND-00 Production QA

Issue: ANKI-007 / #8

Contract: frozen v1.0 (`FREEZE.md`, `rules/cloze_rules.md`, `rules/coverage_rules.md`, `schema/note_schema.yaml`).

## Batch summary

- production path: `production/notes/FND-00.tsv`
- production Notes: **91**
- canonical included FND-00 ALPs: **91**
- mapped included ALPs: **91**
- unmapped included ALPs: **0**
- mapped excluded decorative examples: **0**
- production lifecycle: every row `Status=approved`, `QA=pass`
- source baseline: `xihangzou/bookkeeping-integrated@569ed7b82e729334e1472286eaca7c4352e6fbdb`, `merged/textbook.md`

Rows are serialized in canonical ALP source order. Stable Note IDs are not reordered to match the rows.

## Pilot Note promotion

Sixteen FND pilot Note IDs were promoted into the production batch while preserving their stable IDs and canonical ALP mappings:

`BK-FND-00-0001`–`0015` except no gap within that range, plus `BK-FND-00-0017`, corresponding to ALPs 0003, 0012, 0017, 0022, 0024, 0026, 0027, 0029, 0035, 0038, 0040, 0041, 0052, 0053, 0058, and 0072.

`BK-FND-00-0016` is intentionally **not** production-approved. It is the pilot-only synthetic numeric application of ALP-FND-00-0058. The ID remains reserved and is not reused. New production IDs therefore begin at `BK-FND-00-0018` and continue deterministically through `BK-FND-00-0092` for previously unmapped ALPs.

The ALP-FND-00-0058 production wording is tightened to the algebraic relation `誤仕訳＋訂正仕訳＝正しい仕訳` so it remains distinct from the procedural ALP-FND-00-0057 Note.

## Mechanical validation

`python scripts/validate_fnd00_production.py` checks:

- exact frozen v1.0 TSV header and fixed source fields;
- Note-ID and ALP-ID syntax;
- stable pilot-ID promotion and reservation of `BK-FND-00-0016`;
- deterministic new-ID allocation from `0018` onward;
- exactly one canonical included ALP per ANKI-007 production row;
- 91/91 included-ALP coverage and zero excluded mappings;
- valid Cloze syntax on every Note;
- mechanically derived required tags, uniqueness, and lexical ordering;
- `Status=approved` / `QA=pass` on every production row;
- no production use of the pilot-only lifecycle marker;
- no exact rendered-text duplicate.

Expected validator result:

```text
FND-00 production validation: PASS
notes=91 included_alps=91 mapped=91 unmapped=0
promoted_pilot_ids=16 reserved_pilot_only_id=BK-FND-00-0016
journal_entry_notes=10 formula_notes=3
```

## Local Cloze / ambiguity QA

Every Note was reviewed against the frozen v1.0 retrieval rules with the following checks:

- the visible context identifies the accounting proposition being tested;
- each Cloze has a unique or materially unique semantic answer class;
- journal-entry sides are grouped when splitting would leak the coupled answer;
- amounts copied directly from a transaction are not separately Clozed;
- sequence Notes use multiple groups only where the missing stage still requires substantive recall;
- parallel relations are grouped or reframed when a visible sibling would disclose the answer;
- no placeholder such as `本来の勘定科目` is used as an underdetermined target.

The known pilot warning families remain handled under the frozen v1.0 rules: low-retrieval-value stakeholder matching, positional sequence cues, and large coupled answers are retained only where coverage or accounting coherence gives them retrieval value.

## Local duplicate review

No exact rendered-text duplicates remain. High-similarity pairs were manually checked and retained because they test different retrieval operations or contexts:

- ALP 0019 vs 0022: B/S three-element **定位置** vs all-five-element **増加側** classification;
- ALP 0024 vs 0039: one-entry debit/credit equality vs aggregate trial-balance equality after posting;
- ALP 0053 vs 0055: temporary **payment/asset** process vs temporary **receipt/liability** process;
- ALP 0054 vs 0056: 仮払金 asset classification vs 仮受金 liability classification;
- ALP 0057 vs 0058: correction **procedure** vs correction **algebraic relation**;
- ALP 0041 vs 0052: simple cash salary payment vs compound gross-pay/withholding entry.

These are intentional contrasts rather than semantic duplicates.

## Accounting and formula QA

Journal-entry Notes reviewed: **10**. Formula Notes reviewed: **3**.

Checks performed locally:

- debit/credit direction is consistent with the five-element rules;
- salary expense is recorded gross when employee deductions are withheld;
- employee income-tax and social-insurance deductions are liabilities, not company expenses;
- employer social-insurance burden is `法定福利費`;
- settlement of `所得税預り金` reduces the liability on the debit side;
- `仮払金` is an asset and is removed on the credit side when settled;
- `仮受金` is a liability and is removed on the debit side when settled;
- correction-entry relation is internally consistent;
- `当期純利益＝収益－費用` is correct for the stated profit case;
- `純売上高＝総売上高－売上戻り高` and `純仕入高＝総仕入高－仕入戻し高` are internally consistent.

Result: **PASS — no local accounting, formula, ambiguity, or source-traceability blocker identified.**

## Downstream status

This QA is chapter-local production approval for ANKI-007. Corpus-wide normalization, journal-entry QA, formula QA, recall QA, final coverage audit, and Anki export remain the later ANKI-038–043 gates.
