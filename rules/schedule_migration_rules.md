# Schedule migration rules: old 日商簿記 -> Bookkeeping Master

## Purpose

These rules govern one-way migration of review history and scheduling state from an older Anki deck into the canonical `Bookkeeping Master` export. New repository content remains authoritative; migration may modify scheduling metadata only and must never overwrite canonical note text, fields, templates, styling, tags, media, or stable Note IDs.

## 1. Matching authority

1. Content equivalence is decided before review data is considered. Review maturity, interval length, repetitions, or FSRS state can never make a semantic match valid.
2. Strong matching uses normalized cloze targets, Japanese character-context similarity, recoverable Part/Chapter structure, and ambiguity margins.
3. A grouped new card may inherit progress only when all of its tested cloze targets are covered by the selected old constituent cards.
4. Every tested target on a selected old card must map back to a tested target on the new card. Old cards that only share an answer token but ask a different accounting question are rejected.
5. Fuzzy composition is restricted to multi-target cards with full target coverage and adequate prompt/context evidence. Single-token weak fuzzy matches remain New.
6. Explicit semantic contradictions are rejected, including procedural-stage conflicts such as `第1次` versus `第2次`.
7. Prefix/suffix lookalikes that change accounting meaning, such as `X` versus `X法`, `X費`, `X益`, or `X損`, are not equivalent merely because their strings are similar.
8. Ambiguous, partial, expanded, or newly tested content remains genuinely New. No review history is fabricated to improve coverage.
9. One old card may contribute to at most one migrated new card.

## 2. Multi-card review-history integration

When one new card is matched to multiple old cards, their raw revlogs must not simply be concatenated. A virtual composite history is generated instead.

- Composite review rounds = the minimum number of review events among all required old constituents.
- When source histories have unequal lengths, events are aligned by progress quantile so both early and recent evidence are represented.
- Synthetic review timestamp = the latest timestamp among the aligned source events for that round.
- Synthetic rating/ease = the worst rating among the aligned source events.
- Synthetic resulting interval = the shortest resulting interval among the aligned source events.
- Synthetic factor = the lowest positive factor among the aligned source events.
- Synthetic review time = the sum of source review times for that aligned round.
- `lastIvl` is rebuilt from the preceding synthetic round so the generated history is internally sequential.
- The generated revlog must have unique, strictly increasing IDs for the new card.

For a one-old-card to one-new-card match, preserve the genuine old card history rather than synthesizing it.

## 3. Current schedule integration

A multi-card composite uses a conservative bottleneck model because the new card requires all of its tested content to be recalled.

- Due = earliest source due date.
- Interval = shortest source interval.
- Ease factor = lowest positive source factor.
- FSRS stability = lowest source stability.
- FSRS difficulty = highest source difficulty.
- Repetitions = number of complete synthetic composite rounds.
- Lapses = highest source lapse count.
- Flags = bitwise union of source flags.
- Only mature review-state source cards (`type=2`, `queue=2`) with actual review history may contribute to a migrated mature card.

This prevents several mature constituent cards from making a newly combined card appear more mature than its weakest required component.

## 4. Validation requirements

Every migration output must pass all of the following before use:

1. SQLite `PRAGMA integrity_check = ok`.
2. No orphan `revlog.cid` references.
3. No duplicate revlog IDs.
4. Generated composite histories are chronological and their `lastIvl` chain is internally consistent.
5. Canonical note-content hash is unchanged before versus after schedule migration.
6. Canonical card/note counts are unchanged.
7. Unmatched cards remain New.
8. Original source APKG files are not modified.
9. A per-new-card migration report and per-old-card matching audit are retained with the migrated APKG.
