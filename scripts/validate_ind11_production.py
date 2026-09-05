#!/usr/bin/env python3
"""Validate IND-11 production Notes under the current living recall rules."""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "IND-11.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "IND-11.tsv"
FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-IND-11-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-IND-11-[0-9]{4}$")
DEPRECATED_IDS = {"BK-IND-11-0021"}
EXPECTED_IDS = [f"BK-IND-11-{n:04d}" for n in range(1, 30)]
EXPECTED_SPANS = 77
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
PARALLEL_SEP = ("・", "、")

EXPECTED_ALP_MAP = {
    "BK-IND-11-0001": ["ALP-IND-11-0001"],
    "BK-IND-11-0002": ["ALP-IND-11-0002"],
    "BK-IND-11-0003": ["ALP-IND-11-0003"],
    "BK-IND-11-0004": ["ALP-IND-11-0004"],
    "BK-IND-11-0005": ["ALP-IND-11-0005"],
    "BK-IND-11-0006": ["ALP-IND-11-0006"],
    "BK-IND-11-0007": ["ALP-IND-11-0007"],
    "BK-IND-11-0008": ["ALP-IND-11-0008"],
    "BK-IND-11-0009": ["ALP-IND-11-0009"],
    "BK-IND-11-0010": ["ALP-IND-11-0010"],
    "BK-IND-11-0011": ["ALP-IND-11-0011"],
    "BK-IND-11-0012": ["ALP-IND-11-0012"],
    "BK-IND-11-0013": ["ALP-IND-11-0013"],
    "BK-IND-11-0014": ["ALP-IND-11-0014"],
    "BK-IND-11-0015": ["ALP-IND-11-0015"],
    "BK-IND-11-0016": ["ALP-IND-11-0016"],
    "BK-IND-11-0017": ["ALP-IND-11-0017"],
    "BK-IND-11-0018": ["ALP-IND-11-0018"],
    "BK-IND-11-0019": ["ALP-IND-11-0019"],
    "BK-IND-11-0020": ["ALP-IND-11-0020"],
    "BK-IND-11-0021": ["ALP-IND-11-0021"],
    "BK-IND-11-0022": ["ALP-IND-11-0022"],
    "BK-IND-11-0023": ["ALP-IND-11-0023"],
    "BK-IND-11-0024": ["ALP-IND-11-0024"],
    "BK-IND-11-0025": ["ALP-IND-11-0025"],
    "BK-IND-11-0026": ["ALP-IND-11-0026"],
    "BK-IND-11-0027": ["ALP-IND-11-0027"],
    "BK-IND-11-0028": ["ALP-IND-11-0028"],
    "BK-IND-11-0029": ["ALP-IND-11-0029", "ALP-IND-11-0030", "ALP-IND-11-0031"],
}

REQUIRED = {
    "BK-IND-11-0001": ("{{c1::実際原価}}", "{{c1::原価管理}}"),
    "BK-IND-11-0002": ("{{c1::実際消費量}}", "{{c1::標準消費量}}", "{{c1::標準直接作業時間}}"),
    "BK-IND-11-0003": ("{{c1::標準原価差異}}", "{{c1::差異処理}}"),
    "BK-IND-11-0004": ("{{c1::原価標準}}", "{{c1::標準原価}}"),
    "BK-IND-11-0005": ("標準原価＝{{c1::原価標準}}×{{c1::実際生産量}}",),
    "BK-IND-11-0006": ("標準直接材料費＝{{c1::標準価格}}×{{c1::標準消費数量}}",),
    "BK-IND-11-0007": ("標準直接労務費＝{{c1::標準賃率}}×{{c1::標準直接作業時間}}",),
    "BK-IND-11-0008": ("標準製造間接費＝{{c1::標準配賦率}}×{{c1::標準操業度}}",),
    "BK-IND-11-0009": ("{{c1::客観的}}", "{{c1::達成可能}}"),
    "BK-IND-11-0010": ("製品1個あたりの{{c1::原価標準}}×{{c1::当月完成品数量}}",),
    "BK-IND-11-0011": ("仕掛品の{{c1::実在量}}", "{{c1::加工換算量}}"),
    "BK-IND-11-0012": ("{{c1::加工換算量}}",),
    "BK-IND-11-0013": ("{{c1::価格差異}}", "{{c1::数量差異}}", "{{c1::賃率差異}}", "{{c1::作業時間差異}}", "{{c1::予算差異}}", "{{c1::操業度差異}}", "{{c1::能率差異}}"),
    "BK-IND-11-0014": ("{{c1::標準直接材料費}}－{{c1::実際直接材料費}}",),
    "BK-IND-11-0015": ("（{{c1::標準価格}}－{{c1::実際価格}}）×{{c1::実際消費量}}",),
    "BK-IND-11-0016": ("（{{c1::標準消費量}}－{{c1::実際消費量}}）×{{c1::標準価格}}",),
    "BK-IND-11-0017": ("{{c1::標準直接労務費}}－{{c1::実際直接労務費}}",),
    "BK-IND-11-0018": ("（{{c1::標準賃率}}－{{c1::実際賃率}}）×{{c1::実際直接作業時間}}",),
    "BK-IND-11-0019": ("（{{c1::標準直接作業時間}}－{{c1::実際直接作業時間}}）×{{c1::標準賃率}}",),
    "BK-IND-11-0020": ("{{c1::予算許容額}}－{{c1::実際発生額}}",),
    "BK-IND-11-0021": ("（{{c1::実際操業度}}－{{c1::基準操業度}}）×{{c1::固定費率}}",),
    "BK-IND-11-0022": ("（{{c1::標準操業度}}－{{c1::実際操業度}}）×{{c1::標準配賦率}}",),
    "BK-IND-11-0023": ("（{{c1::標準操業度}}－{{c1::実際操業度}}）×{{c1::変動費率}}",),
    "BK-IND-11-0024": ("（{{c1::標準操業度}}－{{c1::実際操業度}}）×{{c1::固定費率}}",),
    "BK-IND-11-0025": ("予算許容額＝{{c1::標準配賦率}}×{{c1::基準操業度}}", "操業度差異＝（{{c1::実際操業度}}－{{c1::基準操業度}}）×{{c1::標準配賦率}}"),
    "BK-IND-11-0026": ("{{c1::4分法}}",),
    "BK-IND-11-0027": ("{{c1::標準配賦率}}", "{{c1::操業度差異}}"),
    "BK-IND-11-0028": ("{{c1::売上原価}}", "{{c1::加算}}", "{{c1::減算}}"),
    "BK-IND-11-0029": ("{{c1::標準原価}}", "{{c1::各原価要素勘定}}", "{{c1::実際原価}}", "{{c1::仕掛品勘定}}"),
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
        expected_status = "deprecated" if nid in DEPRECATED_IDS else "approved"
        if row["Status"] != expected_status or row["QA"] != "pass":
            errors.append(f"{nid}: lifecycle")
        if nid in DEPRECATED_IDS and "統合先: BK-IND-05-0023" not in row["Extra"]:
            errors.append(f"{nid}: missing replacement lineage")
        if (row["SourceRepo"], row["SourceCommit"], row["SourcePath"]) != SOURCE:
            errors.append(f"{nid}: source")
        if row["Part"] != "industrial" or row["Chapter"] != "11 標準原価計算":
            errors.append(f"{nid}: chapter")
        if row["Type"] not in ALLOWED_TYPES:
            errors.append(f"{nid}: type")
        if row["Difficulty"] not in {"1", "2", "3", "4", "5"}:
            errors.append(f"{nid}: difficulty")

        tags = sorted([
            "bookkeeping::industrial", "chapter::industrial::11",
            f"difficulty::{row['Difficulty']}", f"status::{expected_status}",
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
            if any(x in answer for x in PARALLEL_SEP):
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
    if len(rows) != 29:
        errors.append(f"notes={len(rows)}")
    if spans != EXPECTED_SPANS:
        errors.append(f"spans={spans}")
    if len(included) != 31:
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
        print("IND-11 production validation: FAIL")
        for error in errors:
            print("-", error)
        return 1

    active = [r for r in rows if r["Status"] == "approved"]
    active_spans = sum(len(CLOZE_RE.findall(r["Text"])) for r in active)
    multi = sum(len(v) > 1 for v in EXPECTED_ALP_MAP.values())
    journals = sum(r["Type"] == "journal_entry" for r in active)
    formulas = sum(r["Type"] == "formula" for r in active)
    print("IND-11 production validation: PASS")
    print(f"rows={len(rows)} active_notes={len(active)} deprecated_notes={len(rows)-len(active)} active_cards={len(active)} active_cloze_spans={active_spans} included_alps={len(included)}")
    print(f"multi_alp_notes={multi} journal_entry_notes={journals} formula_notes={formulas} canonical_exclusions={len(excluded_rows)}")
    print("minimal_cloze_scope=pass parallel_term_atomicity=pass formula_atomicity=pass cost_accounting_treatment=pass visible_answer_leakage=0 deterministic_order=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())