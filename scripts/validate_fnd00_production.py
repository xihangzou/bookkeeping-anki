#!/usr/bin/env python3
"""Validate FND-00 after the v1.3 minimal/lexical-Cloze audit."""

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
RESERVED_PILOT_ONLY_ID = "BK-FND-00-0016"
EXPECTED_NOTE_IDS = {
    *(f"BK-FND-00-{n:04d}" for n in range(1, 16)),
    *(f"BK-FND-00-{n:04d}" for n in range(17, 93)),
}

EXPECTED_ACTIVE_IDS = {
    "BK-FND-00-0022",
    "BK-FND-00-0002",
    "BK-FND-00-0004",
    "BK-FND-00-0005",
    "BK-FND-00-0037",
    "BK-FND-00-0044",
    "BK-FND-00-0010",
    "BK-FND-00-0011",
    "BK-FND-00-0053",
    "BK-FND-00-0054",
    "BK-FND-00-0055",
    "BK-FND-00-0014",
    "BK-FND-00-0058",
    "BK-FND-00-0015",
    "BK-FND-00-0075",
    "BK-FND-00-0078",
    "BK-FND-00-0086",
    "BK-FND-00-0088",
}
EXPECTED_APPROVED_COUNT = 18
EXPECTED_DEPRECATED_COUNT = 73
EXPECTED_GENERATED_CARDS = 18
EXPECTED_CLOZE_SPANS = 36
EXPECTED_ACTIVE_ALPS = 36

ALLOWED_NONLEXICAL = {"ならない"}
BANNED_ANSWER_PUNCTUATION = set("。、，,；;／/→＋+・")


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
        if status == "approved":
            approved_count += 1
        else:
            deprecated_count += 1
        if row.get("QA") != "pass":
            fail(errors, f"{note_id}: audited production row must have QA=pass")

        text = row.get("Text", "")
        matches = CLOZE_RE.findall(text)
        if not matches:
            fail(errors, f"{note_id}: Text has no valid Cloze")

        if status == "approved":
            indices = {int(i) for i, _ in matches}
            # v1.3: one coherent active Note is one card. Parallel lexical
            # answers may use multiple distinct spans, but all share c1.
            if indices != {1}:
                fail(errors, f"{note_id}: approved v1.3 Note must use only c1, got {sorted(indices)}")
            generated_cards += 1
            cloze_spans += len(matches)

            answers = [a.strip() for _, a in matches]
            if any(not a for a in answers):
                fail(errors, f"{note_id}: empty Cloze answer")
            if len(answers) != len(set(answers)):
                fail(errors, f"{note_id}: duplicate exact Cloze answer inside Note")
            for answer in answers:
                if answer not in ALLOWED_NONLEXICAL and any(ch in answer for ch in BANNED_ANSWER_PUNCTUATION):
                    fail(errors, f"{note_id}: compound/list-like Cloze answer {answer!r}; split into same-index lexical spans")
                if len(answer) > 12 and answer not in ALLOWED_NONLEXICAL:
                    fail(errors, f"{note_id}: overly long Cloze answer {answer!r}")

            plain = CLOZE_RE.sub(lambda m: m.group(2), text).strip()
            approved_plain[plain] += 1

        raw_alps = row.get("ALP_IDs", "")
        alp_ids = raw_alps.split() if raw_alps else []
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
                fail(errors, f"{note_id}: Section mismatch")

        fixed = {
            "SourceRepo": SOURCE_REPO,
            "SourceCommit": SOURCE_COMMIT,
            "SourcePath": SOURCE_PATH,
            "Part": PART,
            "Chapter": CHAPTER,
        }
        for field, expected in fixed.items():
            if row.get(field) != expected:
                fail(errors, f"{note_id}: {field} mismatch")

        if row.get("Difficulty") not in {"1", "2", "3", "4", "5"}:
            fail(errors, f"{note_id}: invalid Difficulty")
        expected_tags = sorted({
            "bookkeeping::foundation",
            "chapter::foundation::00",
            f"difficulty::{row.get('Difficulty')}",
            f"status::{status}",
            f"topic::{normalized_topic(row.get('Topic', ''))}",
            f"type::{row.get('Type')}",
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
        fail(errors, f"expected {EXPECTED_CLOZE_SPANS} lexical Cloze spans, got {cloze_spans}")

    source_missing = [alp for alp in included_alps if not historical_alp_to_notes.get(alp)]
    if source_missing:
        fail(errors, f"included ALPs missing from production history: {source_missing}")

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
        print("FND-00 v1.3 production validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("FND-00 v1.3 production validation: PASS")
    print(
        f"rows=91 approved={approved_count} deprecated={deprecated_count} "
        f"source_reviewed_alps=91 active_recall_alps={len(active_alp_to_notes)}"
    )
    print(
        f"generated_cards={generated_cards} cloze_spans={cloze_spans} "
        f"same_index_parallelism=pass lexical_atomicity=pass "
        f"reserved_pilot_only_id={RESERVED_PILOT_ONLY_ID}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
