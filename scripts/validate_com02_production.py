#!/usr/bin/env python3
"""Validate the COM-02 production batch under frozen v1.0 + v1.2 overlay."""

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
                f"{note_id}: v1.2 COM-02 requires one generated card; "
                f"found Cloze indices {sorted(indices)}",
            )
        generated_card_count += len(indices)

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
        fail(errors, "excluded COM-02 rows unexpectedly carry canonical ALP IDs")

    if errors:
        print("COM-02 v1.2 production validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    journal_count = sum(1 for r in notes if r.get("Type") == "journal_entry")
    formula_count = sum(1 for r in notes if r.get("Type") == "formula")

    print("COM-02 v1.2 production validation: PASS")
    print(
        f"notes={len(notes)} included_alps={len(included_alps)} "
        f"mapped={len(alp_to_notes)} unmapped=0"
    )
    print(
        f"generated_cards={generated_card_count} multi_card_approved_notes=0 "
        f"multi_alp_notes={multi_alp_note_count}"
    )
    print(f"journal_entry_notes={journal_count} formula_notes={formula_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
