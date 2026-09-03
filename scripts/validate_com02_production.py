#!/usr/bin/env python3
"""Validate COM-02 after ANKI-AUDIT-007 current-rule migration."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "COM-02.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "COM-02.tsv"

FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]

SOURCE_REPO = "xihangzou/bookkeeping-integrated"
SOURCE_COMMIT = "569ed7b82e729334e1472286eaca7c4352e6fbdb"
SOURCE_PATH = "merged/textbook.md"
PART = "commercial"
CHAPTER = "02 収益認識"
NOTE_RE = re.compile(r"^BK-COM-02-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-COM-02-[0-9]{4}$")
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")

ALLOWED_TYPES = {
    "definition", "classification", "recognition", "measurement",
    "journal_entry", "formula", "procedure", "comparison", "exception",
    "reasoning", "ledger", "financial_statement", "cost_accounting",
}

EXPECTED_NOTE_IDS = {f"BK-COM-02-{n:04d}" for n in range(1, 18)}
EXPECTED_NOTE_COUNT = 17
EXPECTED_INCLUDED_ALP_COUNT = 32
EXPECTED_GENERATED_CARD_COUNT = 17
EXPECTED_MULTI_ALP_NOTE_COUNT = 11
EXPECTED_CLOZE_SPANS = 39

COMPACT_JOURNAL_ENTRY_IDS = {
    "BK-COM-02-0002",
    "BK-COM-02-0004",
    "BK-COM-02-0009",
    "BK-COM-02-0015",
}

ALLOWED_REPEAT_ANSWERS = {
    "BK-COM-02-0016": {"履行割合"},
}

MAX_NORMAL_ANSWER_CHARS = 12
BANNED_ANSWER_PUNCTUATION = set("。、，；;／/→＋+・－−-=＝（）()×÷")

CONTENT_REQUIREMENTS = {
    "BK-COM-02-0001": (
        "{{c1::履行義務}}", "「充足」", "{{c1::果たした時点}}",
    ),
    "BK-COM-02-0002": (
        "商品引渡時", "{{c1::（借）売掛金／（貸）売上}}",
        "代金回収", "収益は再計上しない",
    ),
    "BK-COM-02-0003": (
        "収益をまだ認識せず", "負債の{{c1::前受金}}",
        "貸方に{{c1::売上}}", "残額は現金または売掛金",
    ),
    "BK-COM-02-0004": (
        "販売時の逆仕訳", "{{c1::（借）売上／（貸）売掛金}}",
    ),
    "BK-COM-02-0005": (
        "当社負担の売上諸掛り", "運送料・保険料・梱包代",
        "{{c1::発送費}}", "費用勘定",
    ),
    "BK-COM-02-0006": (
        "出荷→着荷→検収", "{{c1::出荷時}}",
        "{{c1::到着時}}", "{{c1::検収時}}",
        "顧客が到着商品を注文どおりか確認",
    ),
    "BK-COM-02-0007": (
        "{{c1::割戻し}}", "{{c1::変動対価}}",
    ),
    "BK-COM-02-0008": (
        "収益から控除", "負債の{{c1::返金負債}}",
        "売上認識額＝{{c1::販売対価}}－{{c1::将来返金見積額}}",
    ),
    "BK-COM-02-0009": (
        "購入時は対価全額を仕入計上", "割戻し確定時に仕入を減額",
        "{{c1::（借）現金／（貸）仕入}}",
        "{{c1::（借）買掛金／（貸）仕入}}", "仕入戻しと同じ仕訳形",
    ),
    "BK-COM-02-0010": (
        "一時点で充足", "一定期間にわたり充足",
        "{{c1::履行済み部分}}", "{{c1::契約負債}}",
    ),
    "BK-COM-02-0011": (
        "無料保証", "{{c1::商品保証引当金}}",
        "有償保証", "独立した{{c1::履行義務}}",
    ),
    "BK-COM-02-0012": (
        "契約負債（前受金でも可）", "当期保証収益＝",
        "{{c1::保証対価}}×{{c1::当期履行期間}}÷{{c1::総保証期間}}",
        "負債から売上へ振り替える",
    ),
    "BK-COM-02-0013": (
        "履行義務ごとに区分", "{{c1::販売時}}",
        "{{c1::保証期間}}", "契約負債として繰り延べる",
    ),
    "BK-COM-02-0014": (
        "資産の{{c1::仕掛品}}", "収益の{{c1::役務収益}}",
        "費用の{{c1::役務原価}}",
    ),
    "BK-COM-02-0015": (
        "{{c1::（借）現金等／（貸）契約負債}}",
        "{{c1::（借）仕掛品／（貸）現金等}}",
        "{{c1::（借）契約負債／（貸）役務収益}}",
        "{{c1::（借）役務原価／（貸）仕掛品}}",
    ),
    "BK-COM-02-0016": (
        "サービスが一部完了", "進捗に応じて収益と原価を認識",
        "部分履行収益＝{{c1::契約対価}}×{{c1::履行割合}}",
        "対応原価＝{{c1::繰延費用}}×{{c1::履行割合}}",
    ),
    "BK-COM-02-0017": (
        "発生時点にほとんど差がない", "{{c1::仕掛品}}に繰り延べず",
        "直接{{c1::役務原価}}",
    ),
}

FORBIDDEN_TEXT = {
    "BK-COM-02-0001": ("{{c1::顧客との約束}}", "{{c1::充足した時点}}"),
    "BK-COM-02-0002": ("{{c1::借方：売掛金／貸方：売上}}", "{{c1::売上を再計上しない}}"),
    "BK-COM-02-0003": ("{{c1::前受金（負債）}}",),
    "BK-COM-02-0005": ("{{c1::「発送費」など支払内容が分かる費用勘定}}",),
    "BK-COM-02-0006": ("{{c1::出荷基準＝出荷時、着荷基準＝到着時、検収基準＝検収時}}",),
    "BK-COM-02-0007": ("{{c1::割戻し（リベート）}}",),
    "BK-COM-02-0008": ("{{c1::販売対価－将来返金見積額}}",),
    "BK-COM-02-0009": ("{{c1::仕入を減額する}}", "{{c1::仕入戻しと同様}}"),
    "BK-COM-02-0010": ("{{c1::履行済み部分に応じて収益を認識する}}",),
    "BK-COM-02-0011": ("{{c1::独立した履行義務}}",),
    "BK-COM-02-0012": (
        "{{c1::契約負債（または前受金）}}",
        "{{c1::保証対価×当期履行期間÷総保証期間}}",
    ),
    "BK-COM-02-0013": (
        "{{c1::販売時に売上認識}}",
        "{{c1::契約負債として繰り延べ、保証期間にわたり収益認識}}",
    ),
    "BK-COM-02-0015": ("{{c1::契約負債→役務収益、仕掛品→役務原価へ振り替える}}",),
    "BK-COM-02-0016": (
        "{{c1::契約対価×履行割合}}",
        "{{c1::繰延費用（仕掛品）×履行割合}}",
    ),
    "BK-COM-02-0017": ("{{c1::仕掛品を経由せず直接役務原価を計上できる}}",),
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def normalized_topic(topic: str) -> str:
    return "_".join(topic.strip().split())


def main() -> int:
    errors: list[str] = []

    note_header, notes = load_tsv(NOTES)
    if note_header != FIELDS:
        fail(errors, f"header mismatch: {note_header!r}")

    _, inventory = load_tsv(INVENTORY)
    included = [r for r in inventory if r.get("status") == "INCLUDE"]
    excluded = [r for r in inventory if r.get("status") == "EXCLUDE"]
    included_alps = [r["alp_id"] for r in included]
    included_set = set(included_alps)
    inventory_by_alp = {r["alp_id"]: r for r in included}

    if len(included_alps) != EXPECTED_INCLUDED_ALP_COUNT:
        fail(
            errors,
            f"expected {EXPECTED_INCLUDED_ALP_COUNT} included COM-02 ALPs, "
            f"got {len(included_alps)}",
        )

    seen_ids: set[str] = set()
    alp_to_notes: dict[str, list[str]] = defaultdict(list)
    plain_text_counter: Counter[str] = Counter()
    generated_card_count = 0
    cloze_span_count = 0
    visible_answer_leakage_count = 0
    first_alp_sequences: list[int] = []
    multi_alp_note_count = 0

    for row_no, row in enumerate(notes, start=2):
        note_id = row.get("ID", "")
        if not NOTE_RE.fullmatch(note_id):
            fail(errors, f"row {row_no}: invalid Note ID {note_id!r}")
        if note_id in seen_ids:
            fail(errors, f"row {row_no}: duplicate Note ID {note_id}")
        seen_ids.add(note_id)

        if row.get("Status") != "approved":
            fail(errors, f"{note_id}: production row must have Status=approved")
        if row.get("QA") != "pass":
            fail(errors, f"{note_id}: production row must have QA=pass")

        text = row.get("Text", "")
        matches = CLOZE_RE.findall(text)
        if not matches:
            fail(errors, f"{note_id}: Text has no valid Cloze")
        indices = {int(index) for index, _ in matches}
        if indices != {1}:
            fail(
                errors,
                f"{note_id}: current COM-02 requires one generated card; "
                f"found Cloze indices {sorted(indices)}",
            )
        generated_card_count += len(indices)
        cloze_span_count += len(matches)

        answers = [answer.strip() for _, answer in matches]
        if any(not answer for answer in answers):
            fail(errors, f"{note_id}: empty/whitespace Cloze answer")

        duplicates = {
            answer for answer, count in Counter(answers).items() if count > 1
        }
        allowed_duplicates = ALLOWED_REPEAT_ANSWERS.get(note_id, set())
        unexpected_duplicates = sorted(duplicates - allowed_duplicates)
        if unexpected_duplicates:
            fail(
                errors,
                f"{note_id}: duplicate exact Cloze answer span(s): "
                f"{unexpected_duplicates}",
            )

        visible_text = CLOZE_RE.sub("", text)
        for answer in answers:
            if len(answer) >= 2 and answer in visible_text:
                visible_answer_leakage_count += 1
                fail(
                    errors,
                    f"{note_id}: visible answer leakage for Cloze answer "
                    f"{answer!r}",
                )

            if note_id in COMPACT_JOURNAL_ENTRY_IDS:
                if "（借）" not in answer or "／（貸）" not in answer:
                    fail(
                        errors,
                        f"{note_id}: compact-entry exception contains a "
                        f"non-entry answer {answer!r}",
                    )
            else:
                if len(answer) > MAX_NORMAL_ANSWER_CHARS:
                    fail(
                        errors,
                        f"{note_id}: non-entry Cloze answer too long "
                        f"({len(answer)} chars): {answer!r}",
                    )
                bad = sorted(set(answer) & BANNED_ANSWER_PUNCTUATION)
                if bad:
                    fail(
                        errors,
                        f"{note_id}: non-entry Cloze answer contains "
                        f"compound punctuation/operators {bad}: {answer!r}",
                    )

        for required in CONTENT_REQUIREMENTS.get(note_id, ()):
            if required not in text:
                fail(
                    errors,
                    f"{note_id}: missing required current-rule content "
                    f"{required!r}",
                )
        for forbidden in FORBIDDEN_TEXT.get(note_id, ()):
            if forbidden in text:
                fail(
                    errors,
                    f"{note_id}: retained superseded broad Cloze "
                    f"{forbidden!r}",
                )

        plain = CLOZE_RE.sub(lambda m: m.group(2), text).strip()
        plain_text_counter[plain] += 1

        raw_alp_ids = row.get("ALP_IDs", "")
        alp_ids = raw_alp_ids.split(" ") if raw_alp_ids else []
        if not alp_ids or any(not alp for alp in alp_ids):
            fail(errors, f"{note_id}: ALP_IDs must contain at least one ID")
        if len(alp_ids) != len(set(alp_ids)):
            fail(errors, f"{note_id}: duplicate ALP IDs in mapping")
        if len(alp_ids) > 1:
            multi_alp_note_count += 1

        sequences: list[int] = []
        for alp_id in alp_ids:
            if not ALP_RE.fullmatch(alp_id):
                fail(errors, f"{note_id}: invalid ALP ID {alp_id!r}")
                continue
            if alp_id not in included_set:
                fail(errors, f"{note_id}: ALP is not canonical INCLUDE: {alp_id}")
                continue
            sequences.append(int(alp_id.rsplit("-", 1)[1]))
            alp_to_notes[alp_id].append(note_id)

        if sequences != sorted(sequences):
            fail(errors, f"{note_id}: ALP_IDs not in canonical source order")
        if sequences:
            first_alp_sequences.append(sequences[0])

        if alp_ids and alp_ids[0] in inventory_by_alp:
            expected_section = inventory_by_alp[alp_ids[0]].get(
                "source_section", ""
            )
            if row.get("Section") != expected_section:
                fail(
                    errors,
                    f"{note_id}: Section={row.get('Section')!r}, "
                    f"expected first-ALP section {expected_section!r}",
                )

        fixed = {
            "SourceRepo": SOURCE_REPO,
            "SourceCommit": SOURCE_COMMIT,
            "SourcePath": SOURCE_PATH,
            "Part": PART,
            "Chapter": CHAPTER,
        }
        for field, expected in fixed.items():
            if row.get(field) != expected:
                fail(
                    errors,
                    f"{note_id}: {field}={row.get(field)!r}, expected "
                    f"{expected!r}",
                )

        if row.get("Difficulty") not in {"1", "2", "3", "4", "5"}:
            fail(errors, f"{note_id}: invalid Difficulty {row.get('Difficulty')!r}")
        if not row.get("Topic") or "::" in row.get("Topic", ""):
            fail(errors, f"{note_id}: invalid Topic")
        if row.get("Type") not in ALLOWED_TYPES:
            fail(errors, f"{note_id}: invalid Type {row.get('Type')!r}")

        expected_tags = sorted({
            "bookkeeping::commercial",
            "chapter::commercial::02",
            f"difficulty::{row.get('Difficulty')}",
            "status::approved",
            f"topic::{normalized_topic(row.get('Topic', ''))}",
            f"type::{row.get('Type')}",
        })
        actual_tags = row.get("Tags", "").split()
        if actual_tags != expected_tags:
            fail(
                errors,
                f"{note_id}: tag mismatch; got {actual_tags}, "
                f"expected {expected_tags}",
            )

    if len(notes) != EXPECTED_NOTE_COUNT:
        fail(errors, f"expected {EXPECTED_NOTE_COUNT} Notes, got {len(notes)}")
    if seen_ids != EXPECTED_NOTE_IDS:
        missing_ids = sorted(EXPECTED_NOTE_IDS - seen_ids)
        unexpected_ids = sorted(seen_ids - EXPECTED_NOTE_IDS)
        fail(
            errors,
            f"stable Note-ID set mismatch; missing={missing_ids}, "
            f"unexpected={unexpected_ids}",
        )
    if first_alp_sequences != sorted(first_alp_sequences):
        fail(errors, "production rows are not ordered by primary canonical ALP")
    if generated_card_count != EXPECTED_GENERATED_CARD_COUNT:
        fail(
            errors,
            f"expected {EXPECTED_GENERATED_CARD_COUNT} generated cards, "
            f"got {generated_card_count}",
        )
    if cloze_span_count != EXPECTED_CLOZE_SPANS:
        fail(
            errors,
            f"expected {EXPECTED_CLOZE_SPANS} Cloze spans, "
            f"got {cloze_span_count}",
        )
    if multi_alp_note_count != EXPECTED_MULTI_ALP_NOTE_COUNT:
        fail(
            errors,
            f"expected {EXPECTED_MULTI_ALP_NOTE_COUNT} multi-ALP Notes, "
            f"got {multi_alp_note_count}",
        )

    missing = [alp for alp in included_alps if not alp_to_notes.get(alp)]
    multiply_mapped = [
        alp for alp in included_alps if len(alp_to_notes.get(alp, [])) != 1
    ]
    if missing:
        fail(errors, f"unmapped included ALPs: {missing}")
    if multiply_mapped:
        fail(errors, f"ALPs not mapped exactly once: {multiply_mapped}")

    rendered_duplicates = [
        text for text, count in plain_text_counter.items() if count > 1
    ]
    if rendered_duplicates:
        fail(
            errors,
            f"exact rendered-text duplicates among approved Notes: "
            f"{rendered_duplicates}",
        )

    if any(r.get("alp_id") for r in excluded):
        fail(errors, "excluded COM-02 rows unexpectedly carry canonical ALP IDs")

    if errors:
        print("COM-02 current-rule production validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    journal_count = sum(1 for r in notes if r.get("Type") == "journal_entry")
    formula_count = sum(1 for r in notes if r.get("Type") == "formula")

    print("COM-02 current-rule production validation: PASS")
    print(
        f"notes={len(notes)} included_alps={len(included_alps)} "
        f"mapped={len(alp_to_notes)} unmapped=0"
    )
    print(
        f"generated_cards={generated_card_count} cloze_spans={cloze_span_count} "
        f"visible_answer_leakage={visible_answer_leakage_count} "
        f"multi_alp_notes={multi_alp_note_count}"
    )
    print(
        "lexical_atomicity=pass formula_itemization=pass "
        "compact_entry_exceptions=4 material_containment=pass"
    )
    print(
        f"journal_entry_notes={journal_count} formula_notes={formula_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
