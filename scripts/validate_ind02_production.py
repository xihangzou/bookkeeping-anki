#!/usr/bin/env python3
"""Validate IND-02 production Notes under the current living recall rules."""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "IND-02.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "IND-02.tsv"
FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-IND-02-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-IND-02-[0-9]{4}$")
EXPECTED_IDS = [f"BK-IND-02-{n:04d}" for n in range(1, 25)]
EXPECTED_SPANS = 48
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
    "BK-IND-02-0001": ["ALP-IND-02-0001"],
    "BK-IND-02-0002": ["ALP-IND-02-0002"],
    "BK-IND-02-0003": ["ALP-IND-02-0003", "ALP-IND-02-0017"],
    "BK-IND-02-0004": ["ALP-IND-02-0004"],
    "BK-IND-02-0005": ["ALP-IND-02-0005", "ALP-IND-02-0006"],
    "BK-IND-02-0006": ["ALP-IND-02-0007"],
    "BK-IND-02-0007": ["ALP-IND-02-0008"],
    "BK-IND-02-0008": ["ALP-IND-02-0009"],
    "BK-IND-02-0009": ["ALP-IND-02-0010"],
    "BK-IND-02-0010": ["ALP-IND-02-0011", "ALP-IND-02-0012"],
    "BK-IND-02-0011": ["ALP-IND-02-0013"],
    "BK-IND-02-0012": ["ALP-IND-02-0014"],
    "BK-IND-02-0013": ["ALP-IND-02-0015"],
    "BK-IND-02-0014": ["ALP-IND-02-0016"],
    "BK-IND-02-0015": ["ALP-IND-02-0018"],
    "BK-IND-02-0016": ["ALP-IND-02-0019"],
    "BK-IND-02-0017": ["ALP-IND-02-0020"],
    "BK-IND-02-0018": ["ALP-IND-02-0021", "ALP-IND-02-0022"],
    "BK-IND-02-0019": ["ALP-IND-02-0023", "ALP-IND-02-0024"],
    "BK-IND-02-0020": ["ALP-IND-02-0025"],
    "BK-IND-02-0021": ["ALP-IND-02-0026"],
    "BK-IND-02-0022": ["ALP-IND-02-0027"],
    "BK-IND-02-0023": ["ALP-IND-02-0028"],
    "BK-IND-02-0024": ["ALP-IND-02-0029"],
}

REQUIRED = {
    "BK-IND-02-0001": ("{{c1::材料}}", "{{c1::資産}}", "{{c1::材料費}}"),
    "BK-IND-02-0002": ("{{c1::月初材料}}＋{{c1::当月購入}}＝{{c1::当月消費}}＋{{c1::月末材料}}",),
    "BK-IND-02-0003": ("（借）{{c1::仕掛品}}", "（借）{{c1::製造間接費}}", "材料勘定の貸方"),
    "BK-IND-02-0004": ("{{c1::直接材料費}}", "{{c1::間接材料費}}"),
    "BK-IND-02-0005": ("{{c1::主要材料費}}", "{{c1::買入部品費}}"),
    "BK-IND-02-0006": ("{{c1::補助材料費・工場消耗品費・消耗工具器具備品費}}",),
    "BK-IND-02-0007": ("{{c1::購入代価}}＋{{c1::材料副費}}",),
    "BK-IND-02-0008": ("（貸）{{c1::買掛金}}", "（貸）{{c1::現金}}"),
    "BK-IND-02-0009": ("（借）{{c1::買掛金}}／（貸）材料",),
    "BK-IND-02-0010": ("{{c1::外部材料副費（材料引取費用）}}", "{{c1::内部材料副費（材料取扱費用）}}", "外部材料副費は購入原価に必ず含める"),
    "BK-IND-02-0011": ("{{c1::含めない}}", "{{c1::一部を含める}}", "{{c1::全部を含める}}"),
    "BK-IND-02-0012": ("購入代価等×{{c1::予定配賦率}}",),
    "BK-IND-02-0013": ("{{c1::材料副費配賦差異}}",),
    "BK-IND-02-0014": ("{{c1::材料消費単価}}×{{c1::材料消費数量}}",),
    "BK-IND-02-0015": ("{{c1::材料元帳}}",),
    "BK-IND-02-0016": ("{{c1::継続記録法}}",),
    "BK-IND-02-0017": ("{{c1::月初在庫数量}}＋{{c1::当月購入数量}}－{{c1::月末実地棚卸数量}}",),
    "BK-IND-02-0018": ("{{c1::継続記録法}}", "{{c1::棚卸計算法}}", "{{c1::実地棚卸}}"),
    "BK-IND-02-0019": ("{{c1::製造間接費}}", "{{c1::営業外費用}}", "{{c1::特別損失}}"),
    "BK-IND-02-0020": ("{{c1::先入先出法}}",),
    "BK-IND-02-0021": ("{{c1::合計原価}}", "{{c1::合計数量}}"),
    "BK-IND-02-0022": ("{{c1::予定消費単価（予定消費価格）}}",),
    "BK-IND-02-0023": ("{{c1::実際消費数量}}×{{c1::予定消費単価}}",),
    "BK-IND-02-0024": ("{{c1::予定消費額}}－{{c1::実際消費額}}", "{{c1::売上原価}}"),
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
        if row["Part"] != "industrial" or row["Chapter"] != "2 材料費":
            errors.append(f"{nid}: chapter")
        if row["Type"] not in ALLOWED_TYPES:
            errors.append(f"{nid}: type")
        if row["Difficulty"] not in {"1", "2", "3", "4", "5"}:
            errors.append(f"{nid}: difficulty")

        tags = sorted([
            "bookkeeping::industrial", "chapter::industrial::02",
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
    if len(rows) != 24:
        errors.append(f"notes={len(rows)}")
    if spans != EXPECTED_SPANS:
        errors.append(f"spans={spans}")
    if len(included) != 29:
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
        print("IND-02 production validation: FAIL")
        for error in errors:
            print("-", error)
        return 1

    multi = sum(len(v) > 1 for v in EXPECTED_ALP_MAP.values())
    journals = sum(r["Type"] == "journal_entry" for r in rows)
    formulas = sum(r["Type"] == "formula" for r in rows)
    print("IND-02 production validation: PASS")
    print(f"notes={len(rows)} cards={len(rows)} cloze_spans={spans} included_alps={len(included)} mapped={len(included)} unmapped=0")
    print(f"multi_alp_notes={multi} journal_entry_notes={journals} formula_notes={formulas} canonical_exclusions={len(excluded_rows)}")
    print("account_level_journal_cloze=pass minimal_cloze_scope=pass formula_atomicity=pass cost_accounting_treatment=pass visible_answer_leakage=0 deterministic_order=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())