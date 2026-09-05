#!/usr/bin/env python3
"""Validate IND-04 production Notes under the current living recall rules."""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "IND-04.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "IND-04.tsv"
FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-IND-04-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-IND-04-[0-9]{4}$")
EXPECTED_IDS = [f"BK-IND-04-{n:04d}" for n in range(1, 18)]
EXPECTED_CARDS = 19
EXPECTED_SPANS = 47
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
    "振り替える", "増加させる", "減少させる", "あり", "なし",
}
ARITH = ("＝", "+", "＋", "-", "－", "×", "÷", "／")
FORBIDDEN_COMPACT = (
    "{{c1::（借）", "{{c1::（貸）", "{{c1::借方：", "{{c1::貸方：",
)
EXPECTED_ALP_MAP = {
    f"BK-IND-04-{n:04d}": [f"ALP-IND-04-{n:04d}"] for n in range(1, 18)
}
EXPECTED_INDICES = {
    **{f"BK-IND-04-{n:04d}": {1} for n in range(1, 18)},
    "BK-IND-04-0003": {1, 2, 3},
}
REQUIRED = {
    "BK-IND-04-0001": ("{{c1::経費}}",),
    "BK-IND-04-0002": ("{{c1::直接経費}}", "{{c1::間接経費}}"),
    "BK-IND-04-0003": (
        "加工委託の対価＝{{c1::外注加工賃}}",
        "特許使用の対価＝{{c1::特許権使用料}}",
        "工場従業員の移動費＝{{c2::旅費交通費}}",
        "工場設備の期間費用＝{{c2::減価償却費}}",
        "工場の水道・電気等＝{{c3::水道光熱費}}",
        "工場建物の家賃＝{{c3::賃借料}}",
        "材料の帳簿在高と実際在高の差＝{{c3::棚卸減耗費}}",
    ),
    "BK-IND-04-0004": ("{{c1::外注加工賃}}", "{{c1::特許権使用料}}", "直接経費となる"),
    "BK-IND-04-0005": ("（借）{{c1::仕掛品}}", "（借）{{c1::製造間接費}}", "貸方は経費勘定"),
    "BK-IND-04-0006": ("{{c1::支払経費}}", "{{c1::月割経費}}", "{{c1::測定経費}}", "{{c1::発生経費}}"),
    "BK-IND-04-0007": ("{{c1::当月支払額}}－{{c1::前月未払額}}＋{{c1::当月未払額}}",),
    "BK-IND-04-0008": ("{{c1::当月支払額}}＋{{c1::前月前払額}}－{{c1::当月前払額}}",),
    "BK-IND-04-0009": (
        "月初に（借）{{c1::未払経費}}／（貸）経費",
        "月末に（借）経費／（貸）{{c1::未払経費}}",
        "月初に（借）経費／（貸）{{c1::前払経費}}",
        "月末に（借）{{c1::前払経費}}／（貸）経費",
    ),
    "BK-IND-04-0010": ("{{c1::月割経費}}", "年額÷{{c1::12か月}}"),
    "BK-IND-04-0011": ("{{c1::測定経費}}", "{{c1::基本料金}}＋{{c1::当月測定量に基づく金額}}"),
    "BK-IND-04-0012": ("{{c1::発生経費}}", "{{c1::当月発生額}}"),
    "BK-IND-04-0013": (
        "経費に関する{{c1::諸勘定}}を設ける",
        "{{c1::経費勘定}}を設ける",
        "経費に関する勘定を{{c1::設けない}}",
    ),
    "BK-IND-04-0014": ("{{c1::各経費勘定}}", "{{c1::仕掛品}}", "{{c1::製造間接費}}"),
    "BK-IND-04-0015": ("{{c1::経費勘定}}", "{{c1::仕掛品}}", "{{c1::製造間接費}}"),
    "BK-IND-04-0016": ("（借）{{c1::仕掛品}}", "（借）{{c1::製造間接費}}", "直接計上する"),
    "BK-IND-04-0017": ("原価は{{c1::同額}}になる",),
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
    cards = 0
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
        if row["Part"] != "industrial" or row["Chapter"] != "4 経費":
            errors.append(f"{nid}: chapter")
        if row["Type"] not in ALLOWED_TYPES:
            errors.append(f"{nid}: type")
        if row["Difficulty"] not in {"1", "2", "3", "4", "5"}:
            errors.append(f"{nid}: difficulty")

        tags = sorted([
            "bookkeeping::industrial", "chapter::industrial::04",
            f"difficulty::{row['Difficulty']}", "status::approved",
            f"topic::{row['Topic'].strip().replace(' ', '_')}", f"type::{row['Type']}",
        ])
        if row["Tags"].split() != tags:
            errors.append(f"{nid}: tags")

        text = row["Text"]
        matches = CLOZE_RE.findall(text)
        spans += len(matches)
        indices = {int(i) for i, _ in matches}
        cards += len(indices)
        if not matches or indices != EXPECTED_INDICES.get(nid, {1}):
            errors.append(f"{nid}: cloze indices {sorted(indices)}")
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
            if "・" in answer:
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
    if len(rows) != 17:
        errors.append(f"notes={len(rows)}")
    if cards != EXPECTED_CARDS:
        errors.append(f"cards={cards}")
    if spans != EXPECTED_SPANS:
        errors.append(f"spans={spans}")
    if len(included) != 17:
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
        print("IND-04 production validation: FAIL")
        for error in errors:
            print("-", error)
        return 1

    journals = sum(r["Type"] == "journal_entry" for r in rows)
    formulas = sum(r["Type"] == "formula" for r in rows)
    print("IND-04 production validation: PASS")
    print(f"notes={len(rows)} cards={cards} cloze_spans={spans} included_alps={len(included)} mapped={len(included)} unmapped=0")
    print(f"multi_alp_notes=0 journal_entry_notes={journals} formula_notes={formulas} canonical_exclusions={len(excluded_rows)}")
    print("account_level_journal_cloze=pass minimal_cloze_scope=pass formula_atomicity=pass cost_accounting_treatment=pass visible_answer_leakage=0 deterministic_order=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
