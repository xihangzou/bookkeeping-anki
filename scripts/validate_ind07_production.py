#!/usr/bin/env python3
"""Validate IND-07 production Notes under the current living recall rules."""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "IND-07.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "IND-07.tsv"
FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-IND-07-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-IND-07-[0-9]{4}$")
EXPECTED_IDS = [f"BK-IND-07-{n:04d}" for n in range(1, 16)]
EXPECTED_SPANS = 30
SOURCE = (
    "xihangzou/bookkeeping-integrated",
    "569ed7b82e729334e1472286eaca7c4352e6fbdb",
    "merged/textbook.md",
)
ALLOWED_TYPES = {
    "definition", "classification", "recognition", "measurement",
    "journal_entry", "formula", "procedure", "comparison", "exception",
    "reasoning", "ledger", "financial_statement", "cost_accounting",
}
FORBIDDEN_COMPACT = (
    "{{c1::（借）", "{{c1::（貸）", "{{c1::借方：", "{{c1::貸方：",
)
BROAD = {
    "仕訳を行う", "仕訳を行わない", "処理する", "計上する",
    "振り替える", "繰り越す", "賦課する", "配賦する", "あり", "なし",
}
ARITH = ("＝", "+", "＋", "-", "－", "×", "÷", "／")

EXPECTED_ALP_MAP = {
    "BK-IND-07-0001": ["ALP-IND-07-0001"],
    "BK-IND-07-0002": ["ALP-IND-07-0002"],
    "BK-IND-07-0003": ["ALP-IND-07-0003"],
    "BK-IND-07-0004": ["ALP-IND-07-0004", "ALP-IND-07-0005"],
    "BK-IND-07-0005": ["ALP-IND-07-0006"],
    "BK-IND-07-0006": ["ALP-IND-07-0007", "ALP-IND-07-0008"],
    "BK-IND-07-0007": ["ALP-IND-07-0009"],
    "BK-IND-07-0008": ["ALP-IND-07-0010"],
    "BK-IND-07-0009": ["ALP-IND-07-0011"],
    "BK-IND-07-0010": ["ALP-IND-07-0012"],
    "BK-IND-07-0011": ["ALP-IND-07-0013"],
    "BK-IND-07-0012": ["ALP-IND-07-0014"],
    "BK-IND-07-0013": ["ALP-IND-07-0015"],
    "BK-IND-07-0014": ["ALP-IND-07-0016", "ALP-IND-07-0018"],
    "BK-IND-07-0015": ["ALP-IND-07-0017"],
}

REQUIRED = {
    "BK-IND-07-0001": ("{{c1::個別原価計算}}",),
    "BK-IND-07-0002": ("{{c1::特定製造指図書}}",),
    "BK-IND-07-0003": ("{{c1::単純個別原価計算}}", "{{c1::部門別個別原価計算}}"),
    "BK-IND-07-0004": ("{{c1::原価計算票}}", "{{c1::原価元帳}}"),
    "BK-IND-07-0005": ("{{c1::原価計算表（総括表）}}",),
    "BK-IND-07-0006": ("{{c1::賦課（直課）}}", "{{c1::配賦計算}}"),
    "BK-IND-07-0007": ("{{c1::賦課}}", "{{c1::単一配賦率}}"),
    "BK-IND-07-0008": ("（借）{{c1::製品}}／（貸）{{c1::仕掛品}}", "{{c1::仕掛品}}として繰り越す"),
    "BK-IND-07-0009": ("（借）{{c1::売上原価}}／（貸）{{c1::製品}}", "{{c1::製品}}として繰り越す"),
    "BK-IND-07-0010": ("{{c1::配賦率}}", "{{c1::配賦基準}}"),
    "BK-IND-07-0011": ("{{c1::仕損}}", "{{c1::仕損品}}", "{{c1::仕損費}}"),
    "BK-IND-07-0012": ("{{c1::補修指図書}}",),
    "BK-IND-07-0013": ("当初の{{c1::製造指図書}}",),
    "BK-IND-07-0014": ("{{c1::直接経費処理}}", "日商簿記2級"),
    "BK-IND-07-0015": (
        "（借）{{c1::仕損費}}／（貸）{{c1::仕掛品}}",
        "（借）{{c1::仕掛品}}／（貸）{{c1::仕損費}}",
    ),
}


def main() -> int:
    errors: list[str] = []
    with NOTES.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        header = list(reader.fieldnames or [])
        rows = list(reader)
    with INVENTORY.open(encoding="utf-8", newline="") as f:
        inventory = list(csv.DictReader(f, delimiter="\t"))

    if header != FIELDS:
        errors.append("header mismatch")

    included_rows = [r for r in inventory if r.get("status") == "INCLUDE"]
    excluded_rows = [r for r in inventory if r.get("status") == "EXCLUDE"]
    included = [r["alp_id"] for r in included_rows]
    included_set = set(included)
    inv_by = {r["alp_id"]: r for r in included_rows}
    alp_to_notes: defaultdict[str, list[str]] = defaultdict(list)
    rendered = Counter()
    spans = 0
    ids: list[str] = []

    for row in rows:
        nid = row["ID"]
        ids.append(nid)
        if not NOTE_RE.fullmatch(nid):
            errors.append(f"{nid}: invalid ID")
        if row["Status"] != "approved" or row["QA"] != "pass":
            errors.append(f"{nid}: lifecycle")
        if (row["SourceRepo"], row["SourceCommit"], row["SourcePath"]) != SOURCE:
            errors.append(f"{nid}: source")
        if row["Part"] != "industrial" or row["Chapter"] != "7 個別原価計算":
            errors.append(f"{nid}: chapter")
        if row["Type"] not in ALLOWED_TYPES:
            errors.append(f"{nid}: type")
        if row["Difficulty"] not in {"1", "2", "3", "4", "5"}:
            errors.append(f"{nid}: difficulty")

        tags = sorted([
            "bookkeeping::industrial", "chapter::industrial::07",
            f"difficulty::{row['Difficulty']}", "status::approved",
            f"topic::{row['Topic'].strip().replace(' ', '_')}", f"type::{row['Type']}",
        ])
        if row["Tags"].split() != tags:
            errors.append(f"{nid}: tags")

        text = row["Text"]
        matches = CLOZE_RE.findall(text)
        spans += len(matches)
        if not matches or {int(i) for i, _ in matches} != {1}:
            errors.append(f"{nid}: c1-only")
        visible = CLOZE_RE.sub("", text)
        for _, answer in matches:
            answer = answer.strip()
            if len(answer) >= 2 and answer in visible:
                errors.append(f"{nid}: visible leakage {answer!r}")
            if answer in BROAD:
                errors.append(f"{nid}: broad answer {answer!r}")
            if any(x in answer for x in ("（借）", "（貸）", "借方：", "貸方：")):
                errors.append(f"{nid}: journal syntax hidden")
            if any(x in answer for x in ARITH):
                errors.append(f"{nid}: operator hidden {answer!r}")
        if any(x in text for x in FORBIDDEN_COMPACT):
            errors.append(f"{nid}: compact journal entry")
        for required in REQUIRED.get(nid, ()):
            if required not in text:
                errors.append(f"{nid}: missing precision {required!r}")
        rendered[CLOZE_RE.sub("[…]", text)] += 1

        alps = row["ALP_IDs"].split()
        if alps != EXPECTED_ALP_MAP.get(nid):
            errors.append(f"{nid}: ALP map")
        for alp in alps:
            if not ALP_RE.fullmatch(alp) or alp not in included_set:
                errors.append(f"{nid}: invalid ALP {alp}")
            else:
                alp_to_notes[alp].append(nid)
        if alps and inv_by.get(alps[0]) and row["Section"] != inv_by[alps[0]]["source_section"]:
            errors.append(f"{nid}: section")

    if ids != EXPECTED_IDS:
        errors.append("stable IDs/order")
    if len(rows) != 15:
        errors.append(f"notes={len(rows)}")
    if spans != EXPECTED_SPANS:
        errors.append(f"spans={spans}")
    if len(included) != 18:
        errors.append(f"included={len(included)}")
    if len(excluded_rows) != 1 or excluded_rows[0].get("exclude_reason") != "DECORATIVE_EXAMPLE":
        errors.append("exclusions")
    for alp in included:
        if len(alp_to_notes[alp]) != 1:
            errors.append(f"{alp} mapped {alp_to_notes[alp]}")
    if any(r.get("note_ids") not in ("", None) or r.get("qa_status") != "pending" for r in inventory):
        errors.append("inventory mutated")
    if any(count > 1 for count in rendered.values()):
        errors.append("duplicate rendered text")

    # Chapter-specific accounting mechanics.
    by_id = {r["ID"]: r for r in rows}
    if by_id.get("BK-IND-07-0008", {}).get("Type") != "journal_entry":
        errors.append("completion flow journal type")
    if by_id.get("BK-IND-07-0009", {}).get("Type") != "journal_entry":
        errors.append("sale flow journal type")
    if by_id.get("BK-IND-07-0015", {}).get("Type") != "journal_entry":
        errors.append("spoilage flow journal type")
    if "直接経費処理" not in by_id.get("BK-IND-07-0014", {}).get("Text", ""):
        errors.append("spoilage direct-expense scope")
    if any(r["Type"] == "formula" for r in rows):
        errors.append("unexpected formula note")

    if errors:
        print("IND-07 production validation: FAIL")
        for error in errors:
            print("-", error)
        return 1

    multi = sum(len(v) > 1 for v in EXPECTED_ALP_MAP.values())
    journals = sum(r["Type"] == "journal_entry" for r in rows)
    formulas = sum(r["Type"] == "formula" for r in rows)
    print("IND-07 production validation: PASS")
    print(f"notes={len(rows)} cards={len(rows)} cloze_spans={spans} included_alps={len(included)} mapped={len(included)} unmapped=0")
    print(f"multi_alp_notes={multi} journal_entry_notes={journals} formula_notes={formulas} canonical_exclusions={len(excluded_rows)}")
    print("account_level_journal_cloze=pass minimal_cloze_scope=pass formula_atomicity=not_applicable cost_accounting_treatment=pass visible_answer_leakage=0 deterministic_order=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
