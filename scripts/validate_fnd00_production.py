#!/usr/bin/env python3
"""Validate the ANKI-007 FND-00 production batch under the frozen v1.0 contract."""

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

# Stable pilot IDs promoted into production. BK-FND-00-0016 remains reserved as
# pilot-only numeric-application evidence and must not be reused.
PROMOTED_PILOT_IDS = {
    "ALP-FND-00-0003": "BK-FND-00-0001",
    "ALP-FND-00-0012": "BK-FND-00-0002",
    "ALP-FND-00-0017": "BK-FND-00-0003",
    "ALP-FND-00-0022": "BK-FND-00-0004",
    "ALP-FND-00-0024": "BK-FND-00-0005",
    "ALP-FND-00-0026": "BK-FND-00-0006",
    "ALP-FND-00-0027": "BK-FND-00-0007",
    "ALP-FND-00-0029": "BK-FND-00-0008",
    "ALP-FND-00-0035": "BK-FND-00-0009",
    "ALP-FND-00-0038": "BK-FND-00-0010",
    "ALP-FND-00-0040": "BK-FND-00-0011",
    "ALP-FND-00-0041": "BK-FND-00-0012",
    "ALP-FND-00-0052": "BK-FND-00-0013",
    "ALP-FND-00-0053": "BK-FND-00-0014",
    "ALP-FND-00-0058": "BK-FND-00-0015",
    "ALP-FND-00-0072": "BK-FND-00-0017",
}
RESERVED_PILOT_ONLY_ID = "BK-FND-00-0016"


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def normalized_topic(topic: str) -> str:
    return "_".join(topic.strip().split())


def expected_id_map(included_alps: list[str]) -> dict[str, str]:
    mapping = dict(PROMOTED_PILOT_IDS)
    next_sequence = 18
    for alp_id in included_alps:
        if alp_id in mapping:
            continue
        mapping[alp_id] = f"BK-FND-00-{next_sequence:04d}"
        next_sequence += 1
    return mapping


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
    excluded_anchors = {r.get("source_anchor", "") for r in excluded}

    if len(included_alps) != 91:
        fail(errors, f"expected 91 included FND-00 ALPs, got {len(included_alps)}")

    expected_ids = expected_id_map(included_alps)
    seen_ids: set[str] = set()
    alp_to_notes: dict[str, list[str]] = defaultdict(list)
    plain_text_counter: Counter[str] = Counter()

    for row_no, row in enumerate(notes, start=2):
        note_id = row.get("ID", "")
        if not NOTE_RE.fullmatch(note_id):
            fail(errors, f"row {row_no}: invalid Note ID {note_id!r}")
        if note_id in seen_ids:
            fail(errors, f"row {row_no}: duplicate Note ID {note_id}")
        seen_ids.add(note_id)
        if note_id == RESERVED_PILOT_ONLY_ID:
            fail(errors, f"row {row_no}: reserved pilot-only ID reused")

        text = row.get("Text", "")
        matches = CLOZE_RE.findall(text)
        if not matches:
            fail(errors, f"{note_id}: Text has no valid Cloze")
        plain = CLOZE_RE.sub(lambda m: m.group(2), text).strip()
        plain_text_counter[plain] += 1

        alp_ids = row.get("ALP_IDs", "").split(" ") if row.get("ALP_IDs") else []
        if len(alp_ids) != 1:
            fail(errors, f"{note_id}: ANKI-007 batch expects exactly one canonical ALP mapping")
        for alp_id in alp_ids:
            if not ALP_RE.fullmatch(alp_id):
                fail(errors, f"{note_id}: invalid ALP ID {alp_id!r}")
                continue
            if alp_id not in included_set:
                fail(errors, f"{note_id}: ALP is not canonical INCLUDE: {alp_id}")
            alp_to_notes[alp_id].append(note_id)
            if expected_ids.get(alp_id) != note_id:
                fail(errors, f"{note_id}: deterministic stable-ID mismatch for {alp_id}; expected {expected_ids.get(alp_id)}")

        fixed = {
            "SourceRepo": SOURCE_REPO,
            "SourceCommit": SOURCE_COMMIT,
            "SourcePath": SOURCE_PATH,
            "Part": PART,
            "Chapter": CHAPTER,
            "Status": "approved",
            "QA": "pass",
        }
        for field, expected in fixed.items():
            if row.get(field) != expected:
                fail(errors, f"{note_id}: {field}={row.get(field)!r}, expected {expected!r}")

        if row.get("Difficulty") not in {"1", "2", "3", "4", "5"}:
            fail(errors, f"{note_id}: invalid Difficulty {row.get('Difficulty')!r}")
        if not row.get("Topic") or "::" in row.get("Topic", ""):
            fail(errors, f"{note_id}: invalid Topic")

        expected_tags = sorted({
            "bookkeeping::foundation",
            "chapter::foundation::00",
            f"difficulty::{row.get('Difficulty')}",
            "status::approved",
            f"topic::{normalized_topic(row.get('Topic', ''))}",
            f"type::{row.get('Type')}",
        })
        actual_tags = row.get("Tags", "").split()
        if actual_tags != expected_tags:
            fail(errors, f"{note_id}: tag mismatch; got {actual_tags}, expected {expected_tags}")
        if "pilot" in row.get("Status", "") or any("status::pilot" == t for t in actual_tags):
            fail(errors, f"{note_id}: pilot-only lifecycle marker remains")

    if len(notes) != 91:
        fail(errors, f"expected 91 production Notes, got {len(notes)}")

    missing = [alp for alp in included_alps if not alp_to_notes.get(alp)]
    multiply_mapped = [alp for alp in included_alps if len(alp_to_notes.get(alp, [])) != 1]
    if missing:
        fail(errors, f"unmapped included ALPs: {missing}")
    if multiply_mapped:
        fail(errors, f"ALPs not mapped exactly once in ANKI-007 batch: {multiply_mapped}")

    duplicates = [text for text, count in plain_text_counter.items() if count > 1]
    if duplicates:
        fail(errors, f"exact rendered-text duplicates: {duplicates}")

    # Excluded decorative examples have no ALP IDs, so they cannot be mapped by
    # ALP_IDs. Retain a sanity assertion that the inventory still contains them
    # only as EXCLUDE records rather than accidentally assigned canonical IDs.
    if any(r.get("alp_id") for r in excluded):
        fail(errors, "excluded FND-00 rows unexpectedly carry canonical ALP IDs")
    if not excluded_anchors:
        fail(errors, "expected explicit excluded decorative-example anchors")

    if errors:
        print("FND-00 production validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    journal_count = sum(1 for r in notes if r.get("Type") == "journal_entry")
    formula_count = sum(1 for r in notes if r.get("Type") == "formula")
    print("FND-00 production validation: PASS")
    print(f"notes={len(notes)} included_alps={len(included_alps)} mapped={len(alp_to_notes)} unmapped=0")
    print(f"promoted_pilot_ids={len(PROMOTED_PILOT_IDS)} reserved_pilot_only_id={RESERVED_PILOT_ONLY_ID}")
    print(f"journal_entry_notes={journal_count} formula_notes={formula_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
