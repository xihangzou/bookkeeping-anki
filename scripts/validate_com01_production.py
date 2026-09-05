#!/usr/bin/env python3
"""Validate COM-01 under the current living Anki rules.

ANKI-039 retires the historical v1.8 whole-journal-entry Cloze exception.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "COM-01.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "COM-01.tsv"

FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]
SOURCE = (
    "xihangzou/bookkeeping-integrated",
    "569ed7b82e729334e1472286eaca7c4352e6fbdb",
    "merged/textbook.md",
)
NOTE_RE = re.compile(r"^BK-COM-01-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-COM-01-[0-9]{4}$")
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
ENTRY_ACCOUNT_RE = re.compile(r"(?:（借）|（貸）|借方：|貸方：)\s*\{\{c([1-9][0-9]*)::([^}]+)\}\}")
FORBIDDEN_COMPACT_RE = re.compile(r"\{\{c[1-9][0-9]*::(?:（借）|（貸）|借方：|貸方：)")
BROAD = {"仕訳を行う", "仕訳を行わない", "処理する", "計上する", "増加させる", "減少させる", "あり", "なし"}

EXPECTED_NOTES = 38
EXPECTED_INCLUDED_ALPS = 52
EXPECTED_CLOZE_SPANS = 103
EXPECTED_JOURNAL_NOTES = 8

REQUIRED_CURRENT_FORMS = {
    "BK-COM-01-0008": (
        "（借）{{c1::仕入}}／（貸）{{c1::繰越商品}}",
        "（借）{{c1::繰越商品}}／（貸）{{c1::仕入}}",
    ),
    "BK-COM-01-0009": (
        "掛けで20,000円販売し在庫原価12,000円",
        "（借）{{c1::売掛金}} 20,000円／（貸）{{c1::売上}} 20,000円",
        "（借）{{c1::売上原価}} 12,000円／（貸）{{c1::商品}} 12,000円",
    ),
    "BK-COM-01-0025": ("借方：{{c1::買掛金}}／貸方：{{c1::仕入}}",),
    "BK-COM-01-0042": ("借方：{{c1::棚卸減耗損}}／貸方：{{c1::繰越商品}}",),
    "BK-COM-01-0043": ("借方：{{c1::商品評価損}}／貸方：{{c1::繰越商品}}",),
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main() -> int:
    errors: list[str] = []
    rows = read_tsv(NOTES)
    inv = read_tsv(INVENTORY)

    if not rows or list(rows[0]) != FIELDS:
        errors.append("production header does not match canonical field order")
    if len(rows) != EXPECTED_NOTES:
        errors.append(f"expected {EXPECTED_NOTES} notes, found {len(rows)}")

    ids = [r["ID"] for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate stable Note IDs")

    included = {r["alp_id"] for r in inv if r["status"] == "INCLUDE"}
    if len(included) != EXPECTED_INCLUDED_ALPS:
        errors.append(f"expected {EXPECTED_INCLUDED_ALPS} INCLUDE ALPs, found {len(included)}")

    mapped: Counter[str] = Counter()
    spans = 0
    journal_count = 0

    for row in rows:
        nid = row["ID"]
        text = row["Text"]
        if not NOTE_RE.fullmatch(nid):
            errors.append(f"{nid}: invalid stable ID")
        if (row["SourceRepo"], row["SourceCommit"], row["SourcePath"]) != SOURCE:
            errors.append(f"{nid}: source traceability drift")
        if row["Part"] != "commercial" or row["Chapter"] != "01 商品売買":
            errors.append(f"{nid}: chapter metadata drift")
        if row["Status"] != "approved" or row["QA"] != "pass":
            errors.append(f"{nid}: active lifecycle/QA mismatch")
        if f"type::{row['Type']}" not in row["Tags"] or "status::approved" not in row["Tags"]:
            errors.append(f"{nid}: tag metadata drift")

        clozes = CLOZE_RE.findall(text)
        spans += len(clozes)
        if not clozes:
            errors.append(f"{nid}: no Cloze target")
        if {idx for idx, _ in clozes} != {"1"}:
            errors.append(f"{nid}: COM-01 should remain one coherent generated card")
        for _, answer in clozes:
            if answer in BROAD:
                errors.append(f"{nid}: broad/abstract Cloze answer {answer!r}")

        alps = row["ALP_IDs"].split()
        if not alps:
            errors.append(f"{nid}: missing ALP mapping")
        for alp in alps:
            if not ALP_RE.fullmatch(alp):
                errors.append(f"{nid}: invalid ALP ID {alp}")
            mapped[alp] += 1

        if row["Type"] == "journal_entry":
            journal_count += 1
            if FORBIDDEN_COMPACT_RE.search(text):
                errors.append(f"{nid}: whole-entry/direction label is inside Cloze")
            explicit = ENTRY_ACCOUNT_RE.findall(text)
            if any(ch.isdigit() for _, answer in explicit for ch in answer):
                errors.append(f"{nid}: amount is bundled inside an account-name Cloze")
            if explicit and len({idx for idx, _ in explicit}) != 1:
                errors.append(f"{nid}: coherent journal accounts must share one Cloze index")

        for required in REQUIRED_CURRENT_FORMS.get(nid, ()):
            if required not in text:
                errors.append(f"{nid}: missing current-rule/source-anchored form {required!r}")

    if spans != EXPECTED_CLOZE_SPANS:
        errors.append(f"expected {EXPECTED_CLOZE_SPANS} Cloze spans, found {spans}")
    if journal_count != EXPECTED_JOURNAL_NOTES:
        errors.append(f"expected {EXPECTED_JOURNAL_NOTES} journal-entry notes, found {journal_count}")

    if set(mapped) != included:
        errors.append(f"ALP coverage mismatch: missing={sorted(included-set(mapped))} extra={sorted(set(mapped)-included)}")
    multiply = sorted(alp for alp, count in mapped.items() if count != 1)
    if multiply:
        errors.append(f"active ALPs must map exactly once in COM-01: {multiply}")

    if errors:
        print("COM-01 production validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("COM-01 production validation: PASS")
    print(
        f"notes={len(rows)} cards={len(rows)} cloze_spans={spans} "
        f"included_alps={len(included)} mapped={len(mapped)} unmapped=0"
    )
    print(
        f"journal_entry_notes={journal_count} account_level_journal_cloze=pass "
        "source_traceability=pass alp_integrity=pass"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
