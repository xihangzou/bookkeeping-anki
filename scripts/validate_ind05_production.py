#!/usr/bin/env python3
"""Validate IND-05 production Notes under the current living recall rules."""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "IND-05.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "IND-05.tsv"
FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-IND-05-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-IND-05-[0-9]{4}$")
EXPECTED_IDS = [f"BK-IND-05-{n:04d}" for n in range(1, 27)]
EXPECTED_SPANS = 61
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
    "減少させる", "増加させる", "あり", "なし",
}
ARITH = ("＝", "+", "＋", "-", "－", "×", "÷", "／")

EXPECTED_ALP_MAP = {
    "BK-IND-05-0001": ["ALP-IND-05-0001"],
    "BK-IND-05-0002": ["ALP-IND-05-0002"],
    "BK-IND-05-0003": ["ALP-IND-05-0003"],
    "BK-IND-05-0004": ["ALP-IND-05-0004"],
    "BK-IND-05-0005": ["ALP-IND-05-0005"],
    "BK-IND-05-0006": ["ALP-IND-05-0006", "ALP-IND-05-0007"],
    "BK-IND-05-0007": ["ALP-IND-05-0008"],
    "BK-IND-05-0008": ["ALP-IND-05-0009"],
    "BK-IND-05-0009": ["ALP-IND-05-0010"],
    "BK-IND-05-0010": ["ALP-IND-05-0011"],
    "BK-IND-05-0011": ["ALP-IND-05-0012"],
    "BK-IND-05-0012": ["ALP-IND-05-0013"],
    "BK-IND-05-0013": ["ALP-IND-05-0014"],
    "BK-IND-05-0014": ["ALP-IND-05-0015"],
    "BK-IND-05-0015": ["ALP-IND-05-0016"],
    "BK-IND-05-0016": ["ALP-IND-05-0017"],
    "BK-IND-05-0017": ["ALP-IND-05-0018"],
    "BK-IND-05-0018": ["ALP-IND-05-0019"],
    "BK-IND-05-0019": ["ALP-IND-05-0020"],
    "BK-IND-05-0020": ["ALP-IND-05-0021"],
    "BK-IND-05-0021": ["ALP-IND-05-0022"],
    "BK-IND-05-0022": ["ALP-IND-05-0023"],
    "BK-IND-05-0023": ["ALP-IND-05-0024"],
    "BK-IND-05-0024": ["ALP-IND-05-0025"],
    "BK-IND-05-0025": ["ALP-IND-05-0026"],
    "BK-IND-05-0026": ["ALP-IND-05-0027"],
}

REQUIRED = {
    "BK-IND-05-0001": ("{{c1::配賦基準}}",),
    "BK-IND-05-0002": ("（借）{{c1::製造間接費}}／（貸）材料・賃金・経費", "（借）{{c1::仕掛品}}／（貸）{{c1::製造間接費}}"),
    "BK-IND-05-0003": ("{{c1::直接材料費}}", "{{c1::直接労務費}}", "{{c1::直接作業時間}}", "{{c1::機械稼働時間}}", "{{c1::生産量}}"),
    "BK-IND-05-0004": ("製造間接費{{c1::実際発生額}}÷当月の実際{{c1::配賦基準数値総額}}",),
    "BK-IND-05-0005": ("{{c1::実際配賦率}}×各製品の{{c1::実際配賦基準数値}}",),
    "BK-IND-05-0006": ("{{c1::予定配賦}}", "実際発生額の集計前", "製品原価の変動を抑えられる"),
    "BK-IND-05-0007": ("原則として{{c1::予定配賦}}",),
    "BK-IND-05-0008": ("{{c1::基準操業度}}",),
    "BK-IND-05-0009": ("{{c1::製造間接費予定額}}÷年間の{{c1::基準操業度}}",),
    "BK-IND-05-0010": ("{{c1::予定配賦率}}×{{c1::実際操業度}}",),
    "BK-IND-05-0011": ("（借）{{c1::仕掛品}}／（貸）{{c1::製造間接費}}",),
    "BK-IND-05-0012": ("{{c1::予定配賦額}}－{{c1::実際発生額}}",),
    "BK-IND-05-0013": ("{{c1::不利差異}}", "{{c1::借方差異}}", "{{c1::有利差異}}", "{{c1::貸方差異}}"),
    "BK-IND-05-0014": ("（借）{{c1::製造間接費配賦差異}}／（貸）{{c1::製造間接費}}", "（借）{{c1::製造間接費}}／（貸）{{c1::製造間接費配賦差異}}"),
    "BK-IND-05-0015": ("{{c1::加算}}", "{{c1::減算}}", "（借）{{c1::売上原価}}／（貸）{{c1::製造間接費配賦差異}}", "（借）{{c1::製造間接費配賦差異}}／（貸）{{c1::売上原価}}"),
    "BK-IND-05-0016": ("{{c1::原価管理}}",),
    "BK-IND-05-0017": ("{{c1::予算許容額}}",),
    "BK-IND-05-0018": ("{{c1::予算許容額}}－{{c1::実際発生額}}",),
    "BK-IND-05-0019": ("{{c1::予定配賦額}}－{{c1::予算許容額}}",),
    "BK-IND-05-0020": ("{{c1::予算差異}}＋{{c1::操業度差異}}",),
    "BK-IND-05-0021": ("{{c1::変動費率}}×{{c1::実際操業度}}＋{{c1::固定費予算}}",),
    "BK-IND-05-0022": ("{{c1::固定費予算}}÷{{c1::基準操業度}}",),
    "BK-IND-05-0023": ("（{{c1::実際操業度}}－{{c1::基準操業度}}）×{{c1::固定費率}}",),
    "BK-IND-05-0024": ("{{c1::変動費率}}＋{{c1::固定費率}}",),
    "BK-IND-05-0025": ("{{c1::固定予算}}", "予算許容額を変化させない"),
    "BK-IND-05-0026": ("{{c1::予定配賦率}}", "{{c1::操業度差異}}"),
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
        if row["Part"] != "industrial" or row["Chapter"] != "5 製造間接費":
            errors.append(f"{nid}: chapter")
        if row["Type"] not in ALLOWED_TYPES:
            errors.append(f"{nid}: type")
        if row["Difficulty"] not in {"1", "2", "3", "4", "5"}:
            errors.append(f"{nid}: difficulty")

        tags = sorted([
            "bookkeeping::industrial", "chapter::industrial::05",
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
            if "・" in answer or "／" in answer:
                errors.append(f"{nid}: non-atomic parallel answer {answer!r}")
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
    if len(rows) != 26:
        errors.append(f"notes={len(rows)}")
    if spans != EXPECTED_SPANS:
        errors.append(f"spans={spans}")
    if len(included) != 27:
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
        print("IND-05 production validation: FAIL")
        for error in errors:
            print("-", error)
        return 1

    multi = sum(len(v) > 1 for v in EXPECTED_ALP_MAP.values())
    journals = sum(r["Type"] == "journal_entry" for r in rows)
    formulas = sum(r["Type"] == "formula" for r in rows)
    print("IND-05 production validation: PASS")
    print(f"notes={len(rows)} cards={len(rows)} cloze_spans={spans} included_alps={len(included)} mapped={len(included)} unmapped=0")
    print(f"multi_alp_notes={multi} journal_entry_notes={journals} formula_notes={formulas} canonical_exclusions={len(excluded_rows)}")
    print("account_level_journal_cloze=pass minimal_cloze_scope=pass parallel_atomicity=pass formula_atomicity=pass cost_accounting_treatment=pass visible_answer_leakage=0 deterministic_order=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())