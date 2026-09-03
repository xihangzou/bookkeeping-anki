#!/usr/bin/env python3
"""Validate the FND-00 production batch after the v1.1 exam-yield audit."""

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

# ANKI-AUDIT-001 keeps all assigned production IDs as audit history. The
# pilot-only synthetic application ID remains reserved and absent.
RESERVED_PILOT_ONLY_ID = "BK-FND-00-0016"
EXPECTED_NOTE_IDS = {
    *(f"BK-FND-00-{n:04d}" for n in range(1, 16)),
    *(f"BK-FND-00-{n:04d}" for n in range(17, 93)),
}

DEPRECATED_IDS = {
    "BK-FND-00-0001", "BK-FND-00-0006", "BK-FND-00-0007",
    "BK-FND-00-0020", "BK-FND-00-0021", "BK-FND-00-0023",
    "BK-FND-00-0031", "BK-FND-00-0033", "BK-FND-00-0034",
    "BK-FND-00-0035", "BK-FND-00-0036", "BK-FND-00-0038",
    "BK-FND-00-0040", "BK-FND-00-0041", "BK-FND-00-0042",
    "BK-FND-00-0045", "BK-FND-00-0046", "BK-FND-00-0052",
    "BK-FND-00-0056", "BK-FND-00-0057", "BK-FND-00-0059",
    "BK-FND-00-0060", "BK-FND-00-0061", "BK-FND-00-0063",
    "BK-FND-00-0065", "BK-FND-00-0066", "BK-FND-00-0067",
    "BK-FND-00-0076", "BK-FND-00-0077", "BK-FND-00-0081",
    "BK-FND-00-0082", "BK-FND-00-0083", "BK-FND-00-0085",
    "BK-FND-00-0087",
}
EXPECTED_APPROVED_COUNT = 57
EXPECTED_DEPRECATED_COUNT = 34


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

    if len(included_alps) != 91:
        fail(errors, f"expected 91 included FND-00 ALPs, got {len(included_alps)}")

    seen_ids: set[str] = set()
    approved_alp_to_notes: dict[str, list[str]] = defaultdict(list)
    approved_plain_text_counter: Counter[str] = Counter()
    approved_count = 0
    deprecated_count = 0

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
        if status not in {"approved", "deprecated"}:
            fail(errors, f"{note_id}: production audit allows only approved/deprecated, got {status!r}")
        if status == "approved":
            approved_count += 1
            if note_id in DEPRECATED_IDS:
                fail(errors, f"{note_id}: expected deprecated but is approved")
        else:
            deprecated_count += 1
            if note_id not in DEPRECATED_IDS:
                fail(errors, f"{note_id}: unexpected deprecated Note")

        if row.get("QA") != "pass":
            fail(errors, f"{note_id}: audited production row must have QA=pass")

        text = row.get("Text", "")
        matches = CLOZE_RE.findall(text)
        if not matches:
            fail(errors, f"{note_id}: Text has no valid Cloze")
        plain = CLOZE_RE.sub(lambda m: m.group(2), text).strip()
        if status == "approved":
            approved_plain_text_counter[plain] += 1

        raw_alp_ids = row.get("ALP_IDs", "")
        alp_ids = raw_alp_ids.split(" ") if raw_alp_ids else []
        if not alp_ids or any(not alp for alp in alp_ids):
            fail(errors, f"{note_id}: ALP_IDs must contain at least one ID")
        if len(alp_ids) != len(set(alp_ids)):
            fail(errors, f"{note_id}: duplicate ALP IDs in mapping")

        sequences: list[int] = []
        for alp_id in alp_ids:
            if not ALP_RE.fullmatch(alp_id):
                fail(errors, f"{note_id}: invalid ALP ID {alp_id!r}")
                continue
            if alp_id not in included_set:
                fail(errors, f"{note_id}: ALP is not canonical INCLUDE: {alp_id}")
                continue
            sequences.append(int(alp_id.rsplit("-", 1)[1]))
            if status == "approved":
                approved_alp_to_notes[alp_id].append(note_id)

        if sequences != sorted(sequences):
            fail(errors, f"{note_id}: ALP_IDs not in canonical source order")

        if alp_ids and alp_ids[0] in inventory_by_alp:
            expected_section = inventory_by_alp[alp_ids[0]].get("source_section", "")
            if row.get("Section") != expected_section:
                fail(errors, f"{note_id}: Section={row.get('Section')!r}, expected first-ALP section {expected_section!r}")

        fixed = {
            "SourceRepo": SOURCE_REPO,
            "SourceCommit": SOURCE_COMMIT,
            "SourcePath": SOURCE_PATH,
            "Part": PART,
            "Chapter": CHAPTER,
        }
        for field, expected in fixed.items():
            if row.get(field) != expected:
                fail(errors, f"{note_id}: {field}={row.get(field)!r}, expected {expected!r}")

        if row.get("Difficulty") not in {"1", "2", "3", "4", "5"}:
            fail(errors, f"{note_id}: invalid Difficulty {row.get('Difficulty')!r}")
        if not row.get("Topic") or "::" in row.get("Topic", ""):
            fail(errors, f"{note_id}: invalid Topic")
        if not row.get("Type"):
            fail(errors, f"{note_id}: Type must be nonempty")

        expected_tags = sorted({
            "bookkeeping::foundation",
            "chapter::foundation::00",
            f"difficulty::{row.get('Difficulty')}",
            f"status::{status}",
            f"topic::{normalized_topic(row.get('Topic', ''))}",
            f"type::{row.get('Type')}",
        })
        actual_tags = row.get("Tags", "").split()
        if actual_tags != expected_tags:
            fail(errors, f"{note_id}: tag mismatch; got {actual_tags}, expected {expected_tags}")

    if len(notes) != 91:
        fail(errors, f"expected 91 historical production rows, got {len(notes)}")
    if seen_ids != EXPECTED_NOTE_IDS:
        missing_ids = sorted(EXPECTED_NOTE_IDS - seen_ids)
        unexpected_ids = sorted(seen_ids - EXPECTED_NOTE_IDS)
        fail(errors, f"stable Note-ID set mismatch; missing={missing_ids}, unexpected={unexpected_ids}")
    if approved_count != EXPECTED_APPROVED_COUNT:
        fail(errors, f"expected {EXPECTED_APPROVED_COUNT} approved Notes, got {approved_count}")
    if deprecated_count != EXPECTED_DEPRECATED_COUNT:
        fail(errors, f"expected {EXPECTED_DEPRECATED_COUNT} deprecated Notes, got {deprecated_count}")

    missing = [alp for alp in included_alps if not approved_alp_to_notes.get(alp)]
    multiply_mapped = [alp for alp in included_alps if len(approved_alp_to_notes.get(alp, [])) != 1]
    if missing:
        fail(errors, f"unmapped included ALPs in active approved deck: {missing}")
    if multiply_mapped:
        fail(errors, f"ALPs not mapped exactly once to approved Notes: {multiply_mapped}")

    duplicates = [text for text, count in approved_plain_text_counter.items() if count > 1]
    if duplicates:
        fail(errors, f"exact rendered-text duplicates among approved Notes: {duplicates}")

    if any(r.get("alp_id") for r in excluded):
        fail(errors, "excluded FND-00 rows unexpectedly carry canonical ALP IDs")

    if errors:
        print("FND-00 v1.1 production validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    approved_rows = [r for r in notes if r.get("Status") == "approved"]
    journal_count = sum(1 for r in approved_rows if r.get("Type") == "journal_entry")
    formula_count = sum(1 for r in approved_rows if r.get("Type") == "formula")
    multi_alp_count = sum(1 for r in approved_rows if len(r.get("ALP_IDs", "").split()) > 1)

    print("FND-00 v1.1 production validation: PASS")
    print(
        f"rows={len(notes)} approved={approved_count} deprecated={deprecated_count} "
        f"included_alps={len(included_alps)} approved_mapped={len(approved_alp_to_notes)} unmapped=0"
    )
    print(f"approved_multi_alp_notes={multi_alp_count} reserved_pilot_only_id={RESERVED_PILOT_ONLY_ID}")
    print(f"approved_journal_entry_notes={journal_count} approved_formula_notes={formula_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
