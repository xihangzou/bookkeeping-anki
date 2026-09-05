#!/usr/bin/env python3
"""Validate IND-09 production Notes under the current living recall rules."""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "IND-09.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "IND-09.tsv"
FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-IND-09-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-IND-09-[0-9]{4}$")
EXPECTED_IDS = [f"BK-IND-09-{n:04d}" for n in range(1, 15)]
EXPECTED_SPANS = 27
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

EXPECTED_ALP_MAP = {
    "BK-IND-09-0001": ["ALP-IND-09-0001"],
    "BK-IND-09-0002": ["ALP-IND-09-0002", "ALP-IND-09-0003"],
    "BK-IND-09-0003": ["ALP-IND-09-0004", "ALP-IND-09-0005"],
    "BK-IND-09-0004": ["ALP-IND-09-0006"],
    "BK-IND-09-0005": ["ALP-IND-09-0007"],
    "BK-IND-09-0006": ["ALP-IND-09-0008", "ALP-IND-09-0009", "ALP-IND-09-0010"],
    "BK-IND-09-0007": ["ALP-IND-09-0011"],
    "BK-IND-09-0008": ["ALP-IND-09-0012", "ALP-IND-09-0019"],
    "BK-IND-09-0009": ["ALP-IND-09-0013"],
    "BK-IND-09-0010": ["ALP-IND-09-0014"],
    "BK-IND-09-0011": ["ALP-IND-09-0015"],
    "BK-IND-09-0012": ["ALP-IND-09-0016"],
    "BK-IND-09-0013": ["ALP-IND-09-0017"],
    "BK-IND-09-0014": ["ALP-IND-09-0018"],
}

REQUIRED = {
    "BK-IND-09-0001": ("{{c1::工程別総合原価計算}}", "工程ごとに仕掛品勘定"),
    "BK-IND-09-0002": ("{{c1::累加法}}", "{{c1::前工程費}}"),
    "BK-IND-09-0003": ("第一工程完了品原価を{{c1::前工程費}}", "第二工程では{{c1::加工費}}", "{{c1::実在量}}"),
    "BK-IND-09-0004": ("{{c1::先入先出法}}・{{c1::平均法}}",),
    "BK-IND-09-0005": ("{{c1::組別総合原価計算}}",),
    "BK-IND-09-0006": ("{{c1::組直接費}}", "{{c1::組間接費}}", "{{c1::当月投入原価}}"),
    "BK-IND-09-0007": ("{{c1::組直接費}}", "{{c1::組間接費}}", "区分は一律ではない"),
    "BK-IND-09-0008": ("{{c1::借方}}", "{{c1::貸方}}"),
    "BK-IND-09-0009": ("{{c1::等級別総合原価計算}}",),
    "BK-IND-09-0010": ("{{c1::等価係数}}",),
    "BK-IND-09-0011": ("{{c1::生産量}}×{{c1::等価係数}}",),
    "BK-IND-09-0012": ("{{c1::完成品総合原価}}×", "{{c1::積数}}÷{{c1::積数合計}}"),
    "BK-IND-09-0013": ("{{c1::完成品原価}}÷", "{{c1::生産量}}"),
    "BK-IND-09-0014": ("{{c1::積数}}", "その比で"),
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
        if row["Part"] != "industrial" or row["Chapter"] != "9 その他の総合原価計算":
            errors.append(f"{nid}: chapter")
        if row["Type"] not in ALLOWED_TYPES:
            errors.append(f"{nid}: type")
        if row["Difficulty"] not in {"1", "2", "3", "4", "5"}:
            errors.append(f"{nid}: difficulty")

        tags = sorted([
            "bookkeeping::industrial", "chapter::industrial::09",
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
    if len(rows) != 14:
        errors.append(f"notes={len(rows)}")
    if spans != EXPECTED_SPANS:
        errors.append(f"spans={spans}")
    if len(included) != 19:
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

    if errors:
        print("IND-09 production validation: FAIL")
        for error in errors:
            print("-", error)
        return 1

    multi = sum(len(v) > 1 for v in EXPECTED_ALP_MAP.values())
    journals = sum(r["Type"] == "journal_entry" for r in rows)
    formulas = sum(r["Type"] == "formula" for r in rows)
    print("IND-09 production validation: PASS")
    print(f"notes={len(rows)} cards={len(rows)} cloze_spans={spans} included_alps={len(included)} mapped={len(included)} unmapped=0")
    print(f"multi_alp_notes={multi} journal_entry_notes={journals} formula_notes={formulas} canonical_exclusions={len(excluded_rows)}")
    print("minimal_cloze_scope=pass formula_atomicity=pass cost_accounting_flow=pass visible_answer_leakage=0 deterministic_order=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
