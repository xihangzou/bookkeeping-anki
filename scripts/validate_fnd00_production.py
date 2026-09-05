#!/usr/bin/env python3
"""Validate FND-00 after the v1.6 completeness / itemized-formula audit."""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "FND-00.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "FND-00.tsv"
FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]
SOURCE_REPO = "xihangzou/bookkeeping-integrated"
SOURCE_COMMIT = "569ed7b82e729334e1472286eaca7c4352e6fbdb"
SOURCE_PATH = "merged/textbook.md"
PART = "foundation"
CHAPTER = "00 序章 簿記の基本"
NOTE_RE = re.compile(r"^BK-FND-00-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-FND-00-[0-9]{4}$")
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NUMERIC_ANSWER_RE = re.compile(r"^[0-9,]+円?$")
RESERVED_PILOT_ONLY_ID = "BK-FND-00-0016"
EXPECTED_NOTE_IDS = {
    *(f"BK-FND-00-{n:04d}" for n in range(1, 16)),
    *(f"BK-FND-00-{n:04d}" for n in range(17, 93)),
}
EXPECTED_ACTIVE_IDS = {
    "BK-FND-00-0018", "BK-FND-00-0022", "BK-FND-00-0003", "BK-FND-00-0024",
    "BK-FND-00-0025", "BK-FND-00-0026", "BK-FND-00-0027", "BK-FND-00-0002",
    "BK-FND-00-0004", "BK-FND-00-0005", "BK-FND-00-0037", "BK-FND-00-0009",
    "BK-FND-00-0044", "BK-FND-00-0010", "BK-FND-00-0011", "BK-FND-00-0012",
    "BK-FND-00-0047", "BK-FND-00-0048", "BK-FND-00-0053", "BK-FND-00-0054",
    "BK-FND-00-0055", "BK-FND-00-0014", "BK-FND-00-0058", "BK-FND-00-0015",
    "BK-FND-00-0062", "BK-FND-00-0068", "BK-FND-00-0075", "BK-FND-00-0078",
    "BK-FND-00-0084", "BK-FND-00-0086", "BK-FND-00-0088", "BK-FND-00-0091",
}
EXPECTED_APPROVED_COUNT = 32
EXPECTED_DEPRECATED_COUNT = 59
EXPECTED_GENERATED_CARDS = 37
EXPECTED_CLOZE_SPANS = 150
EXPECTED_ACTIVE_ALPS = 91
EXPECTED_ACTIVE_INDICES = {
    "BK-FND-00-0047": {1, 2},
    "BK-FND-00-0068": {1, 2, 3},
    "BK-FND-00-0091": {1, 2, 3},
}
ALLOWED_NONLEXICAL = {"ならない", "に終わる", "から始まる"}
BANNED_ANSWER_PUNCTUATION = set("。、，；;／/→＋+・－−-=＝")
CONTENT_REQUIREMENTS = {
    "BK-FND-00-0002": ("当期純利益＝{{c1::収益}}－{{c1::費用}}",),
    "BK-FND-00-0047": (
        "{{c1::給料}}", "{{c1::水道光熱費}}", "{{c1::旅費交通費}}",
        "{{c1::広告宣伝費}}", "{{c1::消耗品費}}", "{{c2::通信費}}",
        "{{c2::保険料}}", "{{c2::保管費}}", "{{c2::諸会費}}", "{{c2::雑費}}",
    ),
    "BK-FND-00-0062": ("{{c1::標準式}}", "{{c1::残高式}}", "日付・摘要・{{c1::仕丁}}・借方金額・貸方金額"),
    "BK-FND-00-0075": (
        "純売上高＝{{c1::総売上高}}－{{c1::売上戻り高}}",
        "純仕入高＝{{c1::総仕入高}}－{{c1::仕入戻り高}}",
    ),
    "BK-FND-00-0084": ("各伝票から{{c1::個別転記}}する",),
}

VISIBLE_CONTEXT_CUES = {
    "BK-FND-00-0018": "会社の取引を記録する媒体",
    "BK-FND-00-0003": "資金調達・運用",
    "BK-FND-00-0024": "商品売買の基本用語",
    "BK-FND-00-0025": "簿記の記録過程",
    "BK-FND-00-0026": "勘定残高",
    "BK-FND-00-0027": "会計期間の表記",
    "BK-FND-00-0002": "簿記の5要素",
    "BK-FND-00-0004": "5要素の増加の定位置",
    "BK-FND-00-0037": "簿記上の記録対象の判定",
    "BK-FND-00-0009": "会社活動を一定期間に区切る単位",
    "BK-FND-00-0044": "総勘定元帳",
    "BK-FND-00-0010": "試算表の種類",
    "BK-FND-00-0012": "基本的な費用仕訳",
    "BK-FND-00-0047": "費用科目の選択",
    "BK-FND-00-0048": "立替金・預り金",
    "BK-FND-00-0053": "給与の源泉徴収",
    "BK-FND-00-0055": "社会保険料の給与処理",
    "BK-FND-00-0015": "訂正仕訳",
    "BK-FND-00-0062": "主要簿",
    "BK-FND-00-0068": "補助簿",
    "BK-FND-00-0075": "売上帳・仕入帳",
    "BK-FND-00-0078": "3伝票制",
    "BK-FND-00-0084": "伝票からの転記",
    "BK-FND-00-0086": "証ひょうの種類",
    "BK-FND-00-0088": "証ひょうから仕訳を判断",
    "BK-FND-00-0091": "簿記の略語・記号",
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
    header, notes = load_tsv(NOTES)
    if header != FIELDS:
        fail(errors, f"header mismatch: {header!r}")
    _, inventory = load_tsv(INVENTORY)
    included = [r for r in inventory if r.get("status") == "INCLUDE"]
    excluded = [r for r in inventory if r.get("status") == "EXCLUDE"]
    included_alps = [r["alp_id"] for r in included]
    included_set = set(included_alps)
    inventory_by_alp = {r["alp_id"]: r for r in included}
    if len(included_alps) != 91:
        fail(errors, f"expected 91 included FND-00 ALPs, got {len(included_alps)}")

    seen_ids: set[str] = set()
    historical_alp_to_notes: dict[str, list[str]] = defaultdict(list)
    active_alp_to_notes: dict[str, list[str]] = defaultdict(list)
    approved_plain = Counter()
    approved_count = deprecated_count = generated_cards = cloze_spans = 0
    visible_answer_leaks = 0

    for row_no, row in enumerate(notes, start=2):
        note_id = row.get("ID", "")
        if not NOTE_RE.fullmatch(note_id):
            fail(errors, f"row {row_no}: invalid Note ID {note_id!r}")
        if note_id in seen_ids:
            fail(errors, f"row {row_no}: duplicate Note ID {note_id}")
        seen_ids.add(note_id)
        if note_id == RESERVED_PILOT_ONLY_ID:
            fail(errors, f"row {row_no}: reserved pilot-only ID reused")

        status = row.get("Status", "")
        expected_status = "approved" if note_id in EXPECTED_ACTIVE_IDS else "deprecated"
        if status != expected_status:
            fail(errors, f"{note_id}: status={status!r}, expected {expected_status!r}")
        approved_count += status == "approved"
        deprecated_count += status == "deprecated"
        if row.get("QA") != "pass":
            fail(errors, f"{note_id}: audited production row must have QA=pass")

        text = row.get("Text", "")
        matches = CLOZE_RE.findall(text)
        if not matches:
            fail(errors, f"{note_id}: Text has no valid Cloze")

        if status == "approved":
            indices = {int(i) for i, _ in matches}
            expected_indices = EXPECTED_ACTIVE_INDICES.get(note_id, {1})
            if indices != expected_indices:
                fail(errors, f"{note_id}: Cloze indices={sorted(indices)}, expected {sorted(expected_indices)}")
            generated_cards += len(indices)
            cloze_spans += len(matches)
            answers = [a.strip() for _, a in matches]
            if any(not a for a in answers):
                fail(errors, f"{note_id}: empty Cloze answer")
            if len(answers) != len(set(answers)):
                fail(errors, f"{note_id}: duplicate exact Cloze answer inside Note")
            for answer in answers:
                if answer not in ALLOWED_NONLEXICAL and not NUMERIC_ANSWER_RE.fullmatch(answer):
                    if any(ch in answer for ch in BANNED_ANSWER_PUNCTUATION):
                        fail(errors, f"{note_id}: compound/list-like Cloze answer {answer!r}; split into same-index spans")
                if len(answer) > 14 and answer not in ALLOWED_NONLEXICAL:
                    fail(errors, f"{note_id}: overly long Cloze answer {answer!r}")
                if answer in {"借方", "貸方"}:
                    fail(errors, f"{note_id}: debit/credit side must Cloze first character only")

            hidden = CLOZE_RE.sub("___", text)
            required_cue = VISIBLE_CONTEXT_CUES.get(note_id)
            if required_cue and required_cue not in hidden:
                fail(errors, f"{note_id}: visible context cue {required_cue!r} disappears after masking")

            # A Cloze answer must not be given away elsewhere on the same card.
            # One-character discriminators such as 借/貸 are intentionally exempt.
            # This chapter validator masks every index at once; the corpus-wide
            # recall validator separately renders each generated sibling card.
            for answer in answers:
                if len(answer) >= 2 and answer in hidden:
                    visible_answer_leaks += 1
                    fail(errors, f"{note_id}: Cloze answer {answer!r} remains visible elsewhere on the card")

            if "借" in answers and not re.search(r"\{\{c[1-9][0-9]*::借\}\}方", text):
                fail(errors, f"{note_id}: 借 direction must use first-character Cloze shape")
            if "貸" in answers and not re.search(r"\{\{c[1-9][0-9]*::貸\}\}方", text):
                fail(errors, f"{note_id}: 貸 direction must use first-character Cloze shape")

            for required in CONTENT_REQUIREMENTS.get(note_id, ()):
                if required not in text:
                    fail(errors, f"{note_id}: required v1.6 content missing: {required!r}")

            if note_id == "BK-FND-00-0018" and text.startswith("簿記の基本では、"):
                fail(errors, "BK-FND-00-0018: answer-leaking prefix must be removed")
            if note_id == "BK-FND-00-0027":
                if "{{c1::に終わる}}" not in text or "{{c1::から始まる}}" not in text:
                    fail(errors, "BK-FND-00-0027: required particle-inclusive Clozes missing")

            plain = CLOZE_RE.sub(lambda m: m.group(2), text).strip()
            approved_plain[plain] += 1

        alp_ids = row.get("ALP_IDs", "").split()
        if not alp_ids:
            fail(errors, f"{note_id}: ALP_IDs must be nonempty")
        if len(alp_ids) != len(set(alp_ids)):
            fail(errors, f"{note_id}: duplicate ALP IDs")
        sequences: list[int] = []
        for alp in alp_ids:
            if not ALP_RE.fullmatch(alp):
                fail(errors, f"{note_id}: invalid ALP ID {alp!r}")
                continue
            if alp not in included_set:
                fail(errors, f"{note_id}: ALP not canonical INCLUDE: {alp}")
                continue
            historical_alp_to_notes[alp].append(note_id)
            if status == "approved":
                active_alp_to_notes[alp].append(note_id)
            sequences.append(int(alp.rsplit("-", 1)[1]))
        if sequences != sorted(sequences):
            fail(errors, f"{note_id}: ALP_IDs not in source order")
        if alp_ids and alp_ids[0] in inventory_by_alp:
            expected_section = inventory_by_alp[alp_ids[0]].get("source_section", "")
            if row.get("Section") != expected_section:
                fail(errors, f"{note_id}: Section mismatch: {row.get('Section')!r} != {expected_section!r}")

        fixed = {
            "SourceRepo": SOURCE_REPO, "SourceCommit": SOURCE_COMMIT,
            "SourcePath": SOURCE_PATH, "Part": PART, "Chapter": CHAPTER,
        }
        for field, expected in fixed.items():
            if row.get(field) != expected:
                fail(errors, f"{note_id}: {field} mismatch")
        if row.get("Difficulty") not in {"1", "2", "3", "4", "5"}:
            fail(errors, f"{note_id}: invalid Difficulty")
        expected_tags = sorted({
            "bookkeeping::foundation", "chapter::foundation::00",
            f"difficulty::{row.get('Difficulty')}", f"status::{status}",
            f"topic::{normalized_topic(row.get('Topic', ''))}", f"type::{row.get('Type')}",
        })
        if row.get("Tags", "").split() != expected_tags:
            fail(errors, f"{note_id}: tag mismatch")

    if len(notes) != 91:
        fail(errors, f"expected 91 historical rows, got {len(notes)}")
    if seen_ids != EXPECTED_NOTE_IDS:
        fail(errors, "stable Note-ID set mismatch")
    if approved_count != EXPECTED_APPROVED_COUNT:
        fail(errors, f"expected {EXPECTED_APPROVED_COUNT} approved, got {approved_count}")
    if deprecated_count != EXPECTED_DEPRECATED_COUNT:
        fail(errors, f"expected {EXPECTED_DEPRECATED_COUNT} deprecated, got {deprecated_count}")
    if generated_cards != EXPECTED_GENERATED_CARDS:
        fail(errors, f"expected {EXPECTED_GENERATED_CARDS} cards, got {generated_cards}")
    if cloze_spans != EXPECTED_CLOZE_SPANS:
        fail(errors, f"expected {EXPECTED_CLOZE_SPANS} Cloze spans, got {cloze_spans}")

    source_missing = [alp for alp in included_alps if not historical_alp_to_notes.get(alp)]
    if source_missing:
        fail(errors, f"included ALPs missing from production history: {source_missing}")
    active_missing = [alp for alp in included_alps if not active_alp_to_notes.get(alp)]
    if active_missing:
        fail(errors, f"included ALPs missing from active deck: {active_missing}")
    active_multiply = [alp for alp, ids in active_alp_to_notes.items() if len(ids) > 1]
    if active_multiply:
        fail(errors, f"ALPs mapped to multiple active Notes: {active_multiply}")
    if len(active_alp_to_notes) != EXPECTED_ACTIVE_ALPS:
        fail(errors, f"expected {EXPECTED_ACTIVE_ALPS} direct-recall ALPs, got {len(active_alp_to_notes)}")

    rendered_duplicates = [t for t, count in approved_plain.items() if count > 1]
    if rendered_duplicates:
        fail(errors, f"rendered-text duplicates among approved Notes: {rendered_duplicates}")
    if any(r.get("alp_id") for r in excluded):
        fail(errors, "excluded FND-00 rows unexpectedly carry ALP IDs")

    if errors:
        print("FND-00 v1.6 production validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("FND-00 v1.6 production validation: PASS")
    print(
        f"rows=91 approved={approved_count} deprecated={deprecated_count} "
        f"source_reviewed_alps=91 active_recall_alps={len(active_alp_to_notes)}"
    )
    print(
        f"generated_cards={generated_cards} cloze_spans={cloze_spans} "
        f"index_grouping=pass lexical_atomicity=pass visible_context=pass "
        f"visible_answer_leakage={visible_answer_leaks} debit_credit_first_character=pass "
        f"reserved_pilot_only_id={RESERVED_PILOT_ONLY_ID}"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
