#!/usr/bin/env python3
"""Validate COM-01 after the v1.6 recall-design / formula-itemization audit."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "COM-01.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "COM-01.tsv"

FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]

SOURCE_REPO = "xihangzou/bookkeeping-integrated"
SOURCE_COMMIT = "569ed7b82e729334e1472286eaca7c4352e6fbdb"
SOURCE_PATH = "merged/textbook.md"
PART = "commercial"
CHAPTER = "01 商品売買"
NOTE_RE = re.compile(r"^BK-COM-01-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-COM-01-[0-9]{4}$")
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NUMERIC_ANSWER_RE = re.compile(r"^[0-9,]+円?$")
BANNED_ANSWER_PUNCTUATION = set("。、，；;／/→＋+・－−-=＝")

ALLOWED_TYPES = {
    "definition", "classification", "recognition", "measurement",
    "journal_entry", "formula", "procedure", "comparison", "exception",
    "reasoning", "ledger", "financial_statement", "cost_accounting",
}

RESERVED_PILOT_ONLY_IDS = {
    "BK-COM-01-0006",
    "BK-COM-01-0013",
    "BK-COM-01-0015",
    "BK-COM-01-0020",
    "BK-COM-01-0023",
}
PROMOTED_PILOT_IDS = {
    "BK-COM-01-0001", "BK-COM-01-0002", "BK-COM-01-0003",
    "BK-COM-01-0004", "BK-COM-01-0005", "BK-COM-01-0007",
    "BK-COM-01-0008", "BK-COM-01-0009", "BK-COM-01-0010",
    "BK-COM-01-0011", "BK-COM-01-0012", "BK-COM-01-0014",
    "BK-COM-01-0016", "BK-COM-01-0017", "BK-COM-01-0018",
    "BK-COM-01-0019", "BK-COM-01-0021", "BK-COM-01-0022",
}
EXPECTED_NOTE_IDS = {
    *PROMOTED_PILOT_IDS,
    *(f"BK-COM-01-{n:04d}" for n in range(24, 44)),
}
EXPECTED_NOTE_COUNT = 38
EXPECTED_INCLUDED_ALP_COUNT = 52
EXPECTED_GENERATED_CARD_COUNT = 38
EXPECTED_MULTI_ALP_NOTE_COUNT = 14
EXPECTED_CLOZE_SPANS = 92

CONTENT_REQUIREMENTS = {
    "BK-COM-01-0024": (
        "{{c1::仕入}}", "{{c1::費用}}", "{{c1::売上}}", "{{c1::収益}}",
    ),
    "BK-COM-01-0004": (
        "純仕入高＝{{c1::総仕入高}}－{{c1::仕入戻し高}}",
    ),
    "BK-COM-01-0005": (
        "運送料・保険料・梱包代",
        "仕入金額＝{{c1::購入代価}}＋{{c1::当社負担の仕入諸掛り}}",
    ),
    "BK-COM-01-0007": (
        "{{c1::三分法}}", "{{c1::分記法}}", "{{c1::売上原価対立法}}",
    ),
    "BK-COM-01-0008": (
        "{{c1::借}}方：仕入", "{{c1::貸}}方：仕入",
    ),
    "BK-COM-01-0027": (
        "{{c1::商品}}（資産）", "{{c1::商品売買益}}（収益）",
        "利益額＝{{c1::販売価格}}－{{c1::商品原価}}",
    ),
    "BK-COM-01-0028": (
        "{{c1::商品}}", "{{c1::売上原価}}", "{{c1::売上}}",
        "在庫資産を増加",
    ),
    "BK-COM-01-0009": (
        "{{c1::売掛金}}", "{{c1::売上}}", "{{c1::売上原価}}", "{{c1::商品}}",
    ),
    "BK-COM-01-0010": (
        "{{c1::決算時}}", "{{c1::売上の都度}}", "{{c1::売上時}}",
    ),
    "BK-COM-01-0030": (
        "{{c1::補助簿}}", "{{c1::原価}}",
    ),
    "BK-COM-01-0031": (
        "{{c1::仮定計算}}", "{{c1::先入先出法}}",
        "{{c1::移動平均法}}", "{{c1::総平均法}}",
    ),
    "BK-COM-01-0011": (
        "{{c1::先に仕入れた商品}}", "{{c1::古い原価層}}", "{{c1::新しい原価層}}",
    ),
    "BK-COM-01-0012": (
        "平均単価＝{{c1::在庫金額}}÷{{c1::在庫数量}}",
    ),
    "BK-COM-01-0032": (
        "{{c1::払出額}}・{{c1::残高額}}",
    ),
    "BK-COM-01-0014": (
        "総平均単価＝（{{c1::期首商品金額}}＋{{c1::期中仕入金額}}）"
        "÷（{{c1::期首商品数量}}＋{{c1::期中仕入数量}}）",
    ),
    "BK-COM-01-0034": (
        "月末数量＝{{c1::期首数量}}＋{{c1::仕入数量}}－{{c1::販売数量}}",
        "月末商品棚卸高＝月末数量×{{c1::払出単価}}",
    ),
    "BK-COM-01-0035": (
        "売上原価＝{{c1::期首商品}}＋{{c1::当期仕入}}－{{c1::期末商品}}",
        "売上総利益＝{{c1::売上高}}－売上原価",
    ),
    "BK-COM-01-0039": (
        "期末帳簿棚卸高＝{{c1::取得単価}}×{{c1::帳簿棚卸数量}}",
    ),
    "BK-COM-01-0017": (
        "{{c1::売上原価の算定}}→{{c1::棚卸減耗損の計上}}→{{c1::商品評価損の計上}}",
    ),
    "BK-COM-01-0041": (
        "{{c1::繰越商品}}→商品", "売上→{{c1::売上高}}", "仕入→{{c1::売上原価}}",
    ),
    "BK-COM-01-0019": (
        "棚卸減耗数量＝{{c1::帳簿棚卸数量}}－{{c1::実地棚卸数量}}",
        "棚卸減耗損＝{{c1::取得単価}}×棚卸減耗数量",
    ),
    "BK-COM-01-0021": (
        "原則取得原価", "評価後期末在庫額＝{{c1::正味売却価額}}×{{c1::実地棚卸数量}}",
    ),
    "BK-COM-01-0022": (
        "商品評価損＝（{{c1::取得単価}}－{{c1::正味売却価額}}）×{{c1::実地棚卸数量}}",
    ),
}

VISIBLE_CONTEXT_CUES = {
    "BK-COM-01-0004": "純仕入高＝",
    "BK-COM-01-0005": "仕入金額＝",
    "BK-COM-01-0007": "商品売買の代表的な記帳方法",
    "BK-COM-01-0008": "三分法の売上原価算定",
    "BK-COM-01-0027": "分記法",
    "BK-COM-01-0028": "3勘定方式",
    "BK-COM-01-0009": "100,000円販売",
    "BK-COM-01-0031": "払出単価",
    "BK-COM-01-0012": "移動平均法",
    "BK-COM-01-0014": "総平均単価＝",
    "BK-COM-01-0034": "月末数量＝",
    "BK-COM-01-0035": "売上原価＝",
    "BK-COM-01-0039": "期末帳簿棚卸高＝",
    "BK-COM-01-0019": "棚卸減耗数量＝",
    "BK-COM-01-0021": "評価後期末在庫額＝",
    "BK-COM-01-0022": "商品評価損＝",
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
            f"expected {EXPECTED_INCLUDED_ALP_COUNT} included COM-01 ALPs, "
            f"got {len(included_alps)}",
        )

    seen_ids: set[str] = set()
    alp_to_notes: dict[str, list[str]] = defaultdict(list)
    plain_text_counter: Counter[str] = Counter()
    generated_card_count = 0
    cloze_span_count = 0
    visible_answer_leakage = 0
    first_alp_sequences: list[int] = []
    multi_alp_note_count = 0

    for row_no, row in enumerate(notes, start=2):
        note_id = row.get("ID", "")
        if not NOTE_RE.fullmatch(note_id):
            fail(errors, f"row {row_no}: invalid Note ID {note_id!r}")
        if note_id in seen_ids:
            fail(errors, f"row {row_no}: duplicate Note ID {note_id}")
        seen_ids.add(note_id)
        if note_id in RESERVED_PILOT_ONLY_IDS:
            fail(errors, f"row {row_no}: reserved pilot-only ID reused: {note_id}")

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
                f"{note_id}: v1.6 COM-01 approved Note must use only c1; "
                f"found Cloze indices {sorted(indices)}",
            )
        generated_card_count += len(indices)
        cloze_span_count += len(matches)

        answers = [answer.strip() for _, answer in matches]
        if any(not answer for answer in answers):
            fail(errors, f"{note_id}: empty/whitespace Cloze answer")
        duplicate_answers = [
            answer for answer, count in Counter(answers).items() if count > 1
        ]
        if duplicate_answers:
            fail(
                errors,
                f"{note_id}: duplicate exact Cloze answer span(s): {duplicate_answers}",
            )

        hidden = CLOZE_RE.sub("___", text)
        for answer in answers:
            if not NUMERIC_ANSWER_RE.fullmatch(answer):
                if any(ch in answer for ch in BANNED_ANSWER_PUNCTUATION):
                    fail(
                        errors,
                        f"{note_id}: compound/list/formula-like Cloze answer {answer!r}; "
                        "split into same-index lexical spans",
                    )
            if len(answer) > 14:
                fail(errors, f"{note_id}: overly long Cloze answer {answer!r}")
            if answer in {"借方", "貸方"}:
                fail(
                    errors,
                    f"{note_id}: debit/credit side must Cloze first character only",
                )
            if len(answer) >= 2 and answer in hidden:
                visible_answer_leakage += 1
                fail(
                    errors,
                    f"{note_id}: Cloze answer {answer!r} remains visible elsewhere "
                    "on the same generated card",
                )

        if "借" in answers and "{{c1::借}}方" not in text:
            fail(errors, f"{note_id}: 借 direction must use {{c1::借}}方 shape")
        if "貸" in answers and "{{c1::貸}}方" not in text:
            fail(errors, f"{note_id}: 貸 direction must use {{c1::貸}}方 shape")

        required_cue = VISIBLE_CONTEXT_CUES.get(note_id)
        if required_cue and required_cue not in hidden:
            fail(
                errors,
                f"{note_id}: visible context cue {required_cue!r} disappears after masking",
            )

        for required in CONTENT_REQUIREMENTS.get(note_id, ()):
            if required not in text:
                fail(errors, f"{note_id}: required v1.6 content missing: {required!r}")

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
            expected_section = inventory_by_alp[alp_ids[0]].get("source_section", "")
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
                    f"{note_id}: {field}={row.get(field)!r}, expected {expected!r}",
                )

        if row.get("Difficulty") not in {"1", "2", "3", "4", "5"}:
            fail(errors, f"{note_id}: invalid Difficulty {row.get('Difficulty')!r}")
        if not row.get("Topic") or "::" in row.get("Topic", ""):
            fail(errors, f"{note_id}: invalid Topic")
        if row.get("Type") not in ALLOWED_TYPES:
            fail(errors, f"{note_id}: invalid Type {row.get('Type')!r}")

        expected_tags = sorted({
            "bookkeeping::commercial",
            "chapter::commercial::01",
            f"difficulty::{row.get('Difficulty')}",
            "status::approved",
            f"topic::{normalized_topic(row.get('Topic', ''))}",
            f"type::{row.get('Type')}",
        })
        actual_tags = row.get("Tags", "").split()
        if actual_tags != expected_tags:
            fail(
                errors,
                f"{note_id}: tag mismatch; got {actual_tags}, expected {expected_tags}",
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
            f"expected {EXPECTED_CLOZE_SPANS} v1.6 Cloze spans, got {cloze_span_count}",
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
            f"exact rendered-text duplicates among approved Notes: {rendered_duplicates}",
        )

    if any(r.get("alp_id") for r in excluded):
        fail(errors, "excluded COM-01 rows unexpectedly carry canonical ALP IDs")

    if errors:
        print("COM-01 v1.6 production validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    journal_count = sum(1 for r in notes if r.get("Type") == "journal_entry")
    formula_count = sum(1 for r in notes if r.get("Type") == "formula")

    print("COM-01 v1.6 production validation: PASS")
    print(
        f"notes={len(notes)} included_alps={len(included_alps)} "
        f"mapped={len(alp_to_notes)} unmapped=0"
    )
    print(
        f"generated_cards={generated_card_count} cloze_spans={cloze_span_count} "
        f"visible_answer_leakage={visible_answer_leakage} "
        f"multi_alp_notes={multi_alp_note_count}"
    )
    print(
        f"promoted_pilot_ids={len(PROMOTED_PILOT_IDS)} "
        f"reserved_pilot_only_ids={len(RESERVED_PILOT_ONLY_IDS)}"
    )
    print(
        f"journal_entry_notes={journal_count} formula_notes={formula_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
