#!/usr/bin/env python3
"""Deterministically verify ANKI-PILOT-003 card-level validation coverage."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "pilot" / "notes.tsv"
VALIDATION = ROOT / "pilot" / "card_validation.tsv"
CLOZE_RE = re.compile(r"\{\{c(\d+)::(.*?)\}\}")
CHECK_KEYS = ("acct", "amb", "ctx", "atom", "ans", "num", "dup", "src", "repeat", "leak")
CHECK_VALUES = {"P", "W", "F"}


def load_notes() -> dict[str, dict[int, list[str]]]:
    result: dict[str, dict[int, list[str]]] = {}
    with NOTES.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            groups: dict[int, list[str]] = defaultdict(list)
            for number, answer in CLOZE_RE.findall(row["Text"]):
                groups[int(number)].append(answer)
            if not groups:
                raise AssertionError(f"{row['ID']}: no Cloze groups")
            result[row["ID"]] = dict(sorted(groups.items()))
    return result


def expected_rows(notes: dict[str, dict[int, list[str]]]):
    expected = {}
    for note_id, groups in notes.items():
        for number, answers in groups.items():
            visible = []
            for other_number, other_answers in groups.items():
                if other_number == number:
                    continue
                visible.extend(f"c{other_number}:{answer}" for answer in other_answers)
            expected[(note_id, f"c{number}")] = {
                "targets": " | ".join(answers),
                "visible_other_answers": " | ".join(visible) if visible else "-",
            }
    return expected


def parse_checks(raw: str) -> dict[str, str]:
    parsed = {}
    for item in raw.split(";"):
        key, value = item.split("=", 1)
        parsed[key] = value
    if tuple(parsed) != CHECK_KEYS:
        raise AssertionError(f"invalid check key/order: {raw}")
    if any(value not in CHECK_VALUES for value in parsed.values()):
        raise AssertionError(f"invalid check value: {raw}")
    return parsed


def main() -> None:
    notes = load_notes()
    expected = expected_rows(notes)
    seen = {}
    severity = Counter()

    with VALIDATION.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            key = (row["note_id"], row["cloze"])
            if key in seen:
                raise AssertionError(f"duplicate validation row: {key}")
            if key not in expected:
                raise AssertionError(f"unexpected validation row: {key}")
            if row["targets"] != expected[key]["targets"]:
                raise AssertionError(f"target mismatch for {key}")
            if row["visible_other_answers"] != expected[key]["visible_other_answers"]:
                raise AssertionError(f"visible-answer mismatch for {key}")

            checks = parse_checks(row["checks"])
            defects = row["defect_codes"]
            row_severity = row["severity"]
            if defects == "NONE":
                if row_severity != "none":
                    raise AssertionError(f"NONE defect with non-none severity for {key}")
                if any(value != "P" for value in checks.values()):
                    raise AssertionError(f"non-pass check without defect code for {key}")
            elif row_severity == "none":
                raise AssertionError(f"defect without severity for {key}")

            severity[row_severity] += 1
            seen[key] = row

    missing = sorted(set(expected) - set(seen))
    if missing:
        raise AssertionError(f"missing validation rows: {missing}")

    print(f"PASS: {len(notes)} notes / {len(expected)} rendered Cloze cards validated")
    print("severity:", ", ".join(f"{name}={count}" for name, count in sorted(severity.items())))


if __name__ == "__main__":
    main()
