# Recall Precision Rules

Status: **Current authoritative specialization**
Issue: **ANKI-AUDIT-008 / #79; ANKI-AUDIT-009 / #81; ANKI-AUDIT-010 / #84; ANKI-AUDIT-011 / #87**
Governance: `GOVERNANCE.md`

This file specializes `rules/cloze_rules.md` and `rules/exam_yield_rules.md` for answer precision. Where an older generic rule allows a broader form, this more specific reviewed rule takes precedence for new work and explicitly migrated batches.

## 1. Journal entries: Cloze account names, not the tuple

For ordinary journal-entry recall, keep debit/credit labels, separators, and amounts visible. Cloze each account name separately using the same index when the entry is one coherent retrieval unit.

Preferred:

`（借）{{c1::売掛金}}／（貸）{{c1::売上}}`

`（借）{{c1::買掛金}}／（貸）{{c1::仕入}}`

Avoid:

`{{c1::（借）売掛金／（貸）売上}}`

`{{c1::借方：売掛金／貸方：売上}}`

The old compact-whole-entry exception is retired for newly authored or explicitly re-audited production Notes. If the same account occurs twice in one integrated procedure, hide every occurrence with the same `c1` so the visible card does not leak the answer.

Amounts copied directly from the prompt remain visible. Cloze an amount only when calculation or measurement is itself the target.

## 2. Canonical answer precision

Prefer the smallest accounting answer that captures the material proposition:

- account name;
- technical term;
- recognition point;
- method/document name;
- formula operand;
- short discriminator.

Avoid approximate prose such as `果たした時点`, `売上を再計上しない`, `仕入を減額する`, or a whole explanatory clause when a canonical accounting term or exact timing discriminator can be recalled instead.

For recognition rules, keep the accounting subject visible and Cloze the timing concept when the **timing itself** is the learning target. Example:

`本業収益は、その約束を{{c1::充足した時点}}に認識する。`

### Canonical-label priority

When a visible fact, description, example, timing point, or treatment maps one-to-one to a named accounting concept, **prefer the canonical accounting label as the Cloze answer** when identifying that label is the useful retrieval operation.

Preferred:

`売上を認識する時点が出荷時なら{{c1::出荷基準}}、到着時なら{{c1::着荷基準}}、検収時なら{{c1::検収基準}}という。`

Avoid when the real target is method/basis identification:

`出荷基準では{{c1::出荷時}}、着荷基準では{{c1::到着時}}、検収基準では{{c1::検収時}}に認識する。`

Apply the same principle to method names, document names, classifications, account names, and other conventional labels. Do not mechanically reverse every definition: if the timing, calculation result, or treatment itself has the higher independent exam value, keep that as the target instead.

## 3. Minimal Cloze scope and lexical atomicity

A Cloze answer must be the **smallest uniquely recoverable unit** supported by the visible context. Do not hide a whole phrase merely because the phrase is technically correct.

When a compound label is already identified by visible context, Cloze only the discriminating token.

Preferred:

`不一致原因が{{c1::当社}}側にある場合は帳簿を修正して仕訳を行う。`

`時間差だけの場合は{{c1::銀行}}側を修正して仕訳しない。`

`保有手形を支払等のため譲渡することを手形の{{c1::裏書}}という。`

Avoid:

`不一致原因が{{c1::当社側の修正項目}}である。`

`保有手形を支払等のため譲渡することを{{c1::手形の裏書}}という。`

For compound technical labels, keep a fixed head, classifier, or relational frame visible when it is already supplied by the sentence and the remaining lexical token is uniquely recoverable. The fact that the full expression is a canonical term does not by itself justify hiding redundant visible context. Examples include patterns such as `手形の{{c1::裏書}}` rather than hiding `手形の裏書` as one span. If removing the fixed part would make the answer ambiguous, keep the smallest larger unit needed for unique recovery.

Broad action phrases are normally poor recall targets because several paraphrases can be equally correct. Keep the resulting treatment visible and Cloze the cause, classification, account, direction, or other discriminator that determines it.

Avoid as standalone answers unless the exact wording itself is a canonical term:

- `{{c1::仕訳を行う}}`
- `{{c1::仕訳を行わない}}`
- `{{c1::処理する}}`
- a full explanatory action clause

If an operation itself has independent exam value, prefer a short exact operator or direction such as `{{c1::加算}}`, `{{c1::減算}}`, `{{c1::借方}}`, or `{{c1::貸方}}` while keeping its object visible.

### Procedures and ordered sequences

Do not Cloze an entire multi-step phrase or several long arrow-separated steps. Keep the procedure frame and most step descriptions visible. Hide only one or a few short sequence-critical labels or discriminators.

Preferred:

`前渡→日々の少額支払い→支払内容の{{c1::報告}}→費用仕訳→支払額と同額の{{c1::補給}}`

Avoid:

`前渡→{{c1::日々の少額支払い}}→{{c1::支払内容の報告}}→{{c1::費用仕訳}}→{{c1::同額補給}}`

If several steps each require independent active recall, split them into separate Notes or test the accounting mechanics directly rather than hiding the whole process vocabulary on one card.

## 4. Essential-recall test

A Note should earn active review time by testing at least one of the following:

- account selection or journal mechanics;
- recognition timing;
- classification that changes accounting treatment;
- formula/measurement relationship;
- method or document discrimination needed to solve questions;
- a material exception that changes the entry or measurement.

Do not create a Cloze merely because a sentence contains terminology. Example-only details, explanatory paraphrases, and obvious consequences should normally remain visible or move to `Extra` unless direct recall has independent exam value.

When one sentence already supplies enough context to retrieve the target, remove trailing examples, enumerations, or explanatory sentences from active `Text` if they do not change the retrieval operation. Preserve useful examples in `Extra`. Active Text should remain sufficient to represent the included ALP materially, but should not carry duplicated teaching prose that is already tested elsewhere.

An included ALP still must remain materially represented in active `Text`; this rule changes what is hidden, not whether source content is silently dropped.

## 5. Reference style

Use FND-00 and COM-01 as the default style reference for short, visible-context, same-card lexical answers. ANKI-AUDIT-008 specifically supersedes legacy compact-entry examples that remain in older chapter history. ANKI-AUDIT-009 adds canonical-label priority when a description-to-label mapping is the intended retrieval task. ANKI-AUDIT-010 adds the minimal-scope rule requiring newly authored and re-audited cards to avoid broad verb phrases and overlong procedure Clozes. ANKI-AUDIT-011 further requires redundant fixed parts of compound labels to stay visible when the remaining token is uniquely recoverable, and moves nonessential explanatory tails out of active Text when the recall target is already fully determined.

Existing chapters are migrated deliberately under `GOVERNANCE.md`; historical audit states remain reproducible through Git history.
