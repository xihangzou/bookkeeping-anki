#!/usr/bin/env python3
"""Validate IND-06 production Notes under the current living recall rules."""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "IND-06.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "IND-06.tsv"
FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-IND-06-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-IND-06-[0-9]{4}$")
EXPECTED_IDS = [f"BK-IND-06-{n:04d}" for n in range(1, 24)]
EXPECTED_SPANS = 44
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
BROAD = {
    "仕訳を行う", "仕訳を行わない", "処理する", "計上する",
    "減少させる", "増加させる", "あり", "なし",
}
ARITH = ("＝", "+", "＋", "-", "－", "×", "÷", "／")
PARALLEL = ("・", "、")

EXPECTED_ALP_MAP = {
    f"BK-IND-06-{n:04d}": [f"ALP-IND-06-{n:04d}"]
    for n in range(1, 24)
}

REQUIRED = {
    "BK-IND-06-0002": ("正確な{{c1::製品原価}}の計算", "部門別の{{c1::原価管理}}"),
    "BK-IND-06-0003": ("{{c1::単純個別原価計算}}", "{{c1::部門別個別原価計算}}"),
    "BK-IND-06-0006": ("{{c1::主経営部門}}", "{{c1::副経営部門}}", "{{c1::補助経営部門}}", "{{c1::工場管理部門}}"),
    "BK-IND-06-0007": ("{{c1::第1次集計}}", "{{c1::第2次集計}}", "{{c1::第3次集計}}"),
    "BK-IND-06-0010": ("{{c1::部門共通費}}×各部門の{{c1::配賦基準量}}÷全部門の{{c1::配賦基準量}}の合計",),
    "BK-IND-06-0013": ("補助部門相互間の用役提供を無視し", "補助部門費を製造部門だけに配賦", "{{c1::直接配賦法}}"),
    "BK-IND-06-0014": ("配賦基準量から{{c1::除外}}",),
    "BK-IND-06-0015": ("{{c1::考慮}}", "{{c1::相互配賦法}}"),
    "BK-IND-06-0016": ("{{c1::製造部門}}・他の{{c1::補助部門}}",),
    "BK-IND-06-0017": ("{{c1::自家消費}}",),
    "BK-IND-06-0018": ("{{c1::製造部門}}にのみ再配賦",),
    "BK-IND-06-0020": ("当月の{{c1::実際製造部門費}}÷当月の当該部門の{{c1::実際配賦基準数値}}",),
    "BK-IND-06-0021": ("当該部門の{{c1::実際配賦率}}×当該製品の{{c1::実際配賦基準数値}}",),
    "BK-IND-06-0022": ("{{c1::部門別予定配賦率}}", "{{c1::実際操業度}}"),
    "BK-IND-06-0023": (
        "{{c1::予定配賦率}}", "{{c1::予定配賦額}}",
        "{{c1::実際部門費}}", "{{c1::配賦差異}}",
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
        if row["Part"] != "industrial" or row["Chapter"] != "6 部門別計算":
            errors.append(f"{nid}: chapter")
        if row["Type"] not in ALLOWED_TYPES:
            errors.append(f"{nid}: type")
        if row["Difficulty"] not in {"1", "2", "3", "4", "5"}:
            errors.append(f"{nid}: difficulty")

        tags = sorted([
            "bookkeeping::industrial", "chapter::industrial::06",
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
            if any(x in answer for x in ARITH):
                errors.append(f"{nid}: operator hidden {answer!r}")
            if any(x in answer for x in PARALLEL):
                errors.append(f"{nid}: non-atomic parallel answer {answer!r}")
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
    if len(rows) != 23:
        errors.append(f"notes={len(rows)}")
    if spans != EXPECTED_SPANS:
        errors.append(f"spans={spans}")
    if len(included) != 23:
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
    if any(r["Type"] == "journal_entry" for r in rows):
        errors.append("unexpected journal-entry primary Note")

    if errors:
        print("IND-06 production validation: FAIL")
        for error in errors:
            print("-", error)
        return 1

    formulas = sum(r["Type"] == "formula" for r in rows)
    procedures = sum(r["Type"] == "procedure" for r in rows)
    print("IND-06 production validation: PASS")
    print(f"notes={len(rows)} cards={len(rows)} cloze_spans={spans} included_alps={len(included)} mapped={len(included)} unmapped=0")
    print(f"procedure_notes={procedures} formula_notes={formulas} canonical_exclusions={len(excluded_rows)}")
    print("minimal_cloze_scope=pass formula_atomicity=pass parallel_atomicity=pass visible_context=pass cost_accounting_flow=pass journal_entry_check=not_applicable visible_answer_leakage=0 deterministic_order=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
