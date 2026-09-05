#!/usr/bin/env python3
"""Validate IND-08 production Notes under the current living recall rules."""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "IND-08.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "IND-08.tsv"

FIELDS = ["ID","Text","Extra","SourceRepo","SourceCommit","SourcePath","Part","Chapter","Section","Topic","Type","ALP_IDs","Difficulty","Tags","Status","QA"]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-IND-08-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-IND-08-[0-9]{4}$")
EXPECTED_IDS = [f"BK-IND-08-{n:04d}" for n in range(1, 28)]
EXPECTED_SPANS = 72
SOURCE = ("xihangzou/bookkeeping-integrated", "569ed7b82e729334e1472286eaca7c4352e6fbdb", "merged/textbook.md")
ALLOWED_TYPES = {"definition","classification","recognition","measurement","journal_entry","formula","procedure","comparison","exception","reasoning","ledger","financial_statement","cost_accounting"}
ENTRY_ACCOUNT_RE = re.compile(r"（(?:借|貸)）\{\{c1::([^}]+)\}\}")
FORBIDDEN_COMPACT = ("{{c1::（借）", "{{c1::（貸）", "{{c1::借方：", "{{c1::貸方：")
BROAD = {"仕訳を行う","仕訳を行わない","処理する","計上する","減少させる","増加させる","あり","なし"}
ARITH = ("＝","+","＋","-","－","×","÷","／")

EXPECTED_ALP_MAP = {
    "BK-IND-08-0001":["ALP-IND-08-0001"],
    "BK-IND-08-0002":["ALP-IND-08-0002"],
    "BK-IND-08-0003":["ALP-IND-08-0003"],
    "BK-IND-08-0004":["ALP-IND-08-0004"],
    "BK-IND-08-0005":["ALP-IND-08-0005"],
    "BK-IND-08-0006":["ALP-IND-08-0006","ALP-IND-08-0007"],
    "BK-IND-08-0007":["ALP-IND-08-0008"],
    "BK-IND-08-0008":["ALP-IND-08-0009"],
    "BK-IND-08-0009":["ALP-IND-08-0010"],
    "BK-IND-08-0010":["ALP-IND-08-0011"],
    "BK-IND-08-0011":["ALP-IND-08-0012"],
    "BK-IND-08-0012":["ALP-IND-08-0013"],
    "BK-IND-08-0013":["ALP-IND-08-0014","ALP-IND-08-0015"],
    "BK-IND-08-0014":["ALP-IND-08-0016"],
    "BK-IND-08-0015":["ALP-IND-08-0017","ALP-IND-08-0018"],
    "BK-IND-08-0016":["ALP-IND-08-0019"],
    "BK-IND-08-0017":["ALP-IND-08-0020","ALP-IND-08-0021"],
    "BK-IND-08-0018":["ALP-IND-08-0022"],
    "BK-IND-08-0019":["ALP-IND-08-0023"],
    "BK-IND-08-0020":["ALP-IND-08-0024"],
    "BK-IND-08-0021":["ALP-IND-08-0025"],
    "BK-IND-08-0022":["ALP-IND-08-0026"],
    "BK-IND-08-0023":["ALP-IND-08-0027"],
    "BK-IND-08-0024":["ALP-IND-08-0028"],
    "BK-IND-08-0025":["ALP-IND-08-0029"],
    "BK-IND-08-0026":["ALP-IND-08-0030"],
    "BK-IND-08-0027":["ALP-IND-08-0031","ALP-IND-08-0032","ALP-IND-08-0033"],
}

REQUIRED = {
    "BK-IND-08-0001": ("{{c1::総合原価計算}}",),
    "BK-IND-08-0002": ("{{c1::継続製造指図書}}", "{{c1::月末}}"),
    "BK-IND-08-0003": ("{{c1::特定製造指図書別}}", "{{c1::期間単位}}", "{{c1::完成品}}", "{{c1::月末仕掛品}}"),
    "BK-IND-08-0006": ("{{c1::加工換算量}}＝{{c1::実在量}}×{{c1::加工進捗度}}",),
    "BK-IND-08-0008": ("直接材料費は{{c1::実在量}}", "加工費は{{c1::加工換算量}}"),
    "BK-IND-08-0009": ("月末仕掛品材料費＝{{c1::対象材料費}}×{{c1::月末仕掛品数量}}÷{{c1::対象投入数量}}",),
    "BK-IND-08-0010": ("月末仕掛品加工費＝{{c1::対象加工費}}×{{c1::月末仕掛品加工換算量}}÷{{c1::対象加工換算量合計}}",),
    "BK-IND-08-0011": ("完成品原価＝{{c1::月初仕掛品原価}}＋{{c1::当月製造費用}}－{{c1::月末仕掛品原価}}",),
    "BK-IND-08-0013": ("{{c1::当月投入数量}}", "{{c1::前月加工済み部分}}"),
    "BK-IND-08-0015": ("{{c1::月初材料費}}＋{{c1::当月材料費}}", "{{c1::月初加工費}}＋{{c1::当月加工費}}", "{{c1::加工換算量合計}}"),
    "BK-IND-08-0016": ("{{c1::正常仕損}}", "{{c1::仕損品原価}}－{{c1::仕損品評価額}}"),
    "BK-IND-08-0017": ("{{c1::正常減損}}", "{{c1::消失}}", "{{c1::残る}}", "{{c1::仕損品評価額}}"),
    "BK-IND-08-0018": ("{{c1::度外視法}}",),
    "BK-IND-08-0019": ("進捗度＜仕損発生点なら{{c1::完成品のみ}}", "進捗度≧仕損発生点なら{{c1::完成品}}と{{c1::月末仕掛品}}"),
    "BK-IND-08-0020": ("{{c1::当月投入分}}",),
    "BK-IND-08-0021": ("分母に{{c1::仕損数量}}と{{c1::仕損加工換算量}}を含める",),
    "BK-IND-08-0022": ("分母から{{c1::仕損数量}}と{{c1::仕損加工換算量}}を除外する",),
    "BK-IND-08-0023": ("{{c1::仕損品評価額}}は{{c1::貯蔵品}}として資産計上",),
    "BK-IND-08-0024": ("仕損品評価額は{{c1::完成品原価}}から控除",),
    "BK-IND-08-0025": ("評価額を{{c1::対象製造費用}}から先に控除", "{{c1::仕損数量}}と{{c1::仕損加工換算量}}を按分分母から除外"),
    "BK-IND-08-0026": ("{{c1::追加材料}}", "{{c1::投入点}}", "{{c1::加工進捗度}}"),
    "BK-IND-08-0027": ("終点投入なら{{c1::完成品のみ}}", "{{c1::投入点を通過した加工品}}", "平均投入なら{{c1::加工換算量}}"),
}

def main() -> int:
    errors = []
    with NOTES.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        header = list(reader.fieldnames or [])
        rows = list(reader)
    with INVENTORY.open(encoding="utf-8", newline="") as f:
        inv = list(csv.DictReader(f, delimiter="\t"))

    if header != FIELDS:
        errors.append("header mismatch")

    included_rows = [r for r in inv if r.get("status") == "INCLUDE"]
    excluded_rows = [r for r in inv if r.get("status") == "EXCLUDE"]
    included = [r["alp_id"] for r in included_rows]
    included_set = set(included)
    inv_by = {r["alp_id"]: r for r in included_rows}

    alp_to_notes = defaultdict(list)
    rendered = Counter()
    spans = 0
    ids = []

    for row in rows:
        nid = row["ID"]
        ids.append(nid)
        if not NOTE_RE.fullmatch(nid):
            errors.append(f"{nid}: invalid ID")
        if row["Status"] != "approved" or row["QA"] != "pass":
            errors.append(f"{nid}: lifecycle")
        if (row["SourceRepo"], row["SourceCommit"], row["SourcePath"]) != SOURCE:
            errors.append(f"{nid}: source")
        if row["Part"] != "industrial" or row["Chapter"] != "8 総合原価計算":
            errors.append(f"{nid}: chapter")
        if row["Type"] not in ALLOWED_TYPES:
            errors.append(f"{nid}: type")
        if row["Difficulty"] not in {"1","2","3","4","5"}:
            errors.append(f"{nid}: difficulty")

        expected_tags = sorted([
            "bookkeeping::industrial",
            "chapter::industrial::08",
            f"difficulty::{row['Difficulty']}",
            "status::approved",
            f"topic::{row['Topic'].strip().replace(' ', '_')}",
            f"type::{row['Type']}",
        ])
        if row["Tags"].split() != expected_tags:
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
            if "・" in answer:
                errors.append(f"{nid}: parallel phrase should use separate clozes {answer!r}")
            if any(x in answer for x in ("（借）","（貸）","借方：","貸方：")):
                errors.append(f"{nid}: journal syntax hidden")
            if any(x in answer for x in ARITH):
                errors.append(f"{nid}: operator hidden {answer!r}")

        if any(x in text for x in FORBIDDEN_COMPACT):
            errors.append(f"{nid}: compact entry")
        if ("（借）" in text or "（貸）" in text) and not ENTRY_ACCOUNT_RE.search(text):
            errors.append(f"{nid}: journal syntax without account-level cloze")

        for req in REQUIRED.get(nid, ()):
            if req not in text:
                errors.append(f"{nid}: missing precision {req!r}")

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
    if len(rows) != 27:
        errors.append(f"notes={len(rows)}")
    if spans != EXPECTED_SPANS:
        errors.append(f"spans={spans}")
    if len(included) != 33:
        errors.append(f"included={len(included)}")
    if len(excluded_rows) != 1 or excluded_rows[0].get("exclude_reason") != "DECORATIVE_EXAMPLE":
        errors.append("exclusions")

    for alp in included:
        if len(alp_to_notes[alp]) != 1:
            errors.append(f"{alp} mapped {alp_to_notes[alp]}")

    if any(r.get("note_ids") not in ("", None) or r.get("qa_status") != "pending" for r in inv):
        errors.append("inventory mutated")
    if any(v > 1 for v in rendered.values()):
        errors.append("duplicate rendered text")

    if errors:
        print("IND-08 production validation: FAIL")
        for error in errors:
            print("-", error)
        return 1

    multi = sum(len(v) > 1 for v in EXPECTED_ALP_MAP.values())
    formulas = sum(r["Type"] == "formula" for r in rows)
    procedures = sum(r["Type"] == "procedure" for r in rows)
    measurements = sum(r["Type"] == "measurement" for r in rows)
    print("IND-08 production validation: PASS")
    print(f"notes={len(rows)} cards={len(rows)} cloze_spans={spans} included_alps={len(included)} mapped={len(included)} unmapped=0")
    print(f"multi_alp_notes={multi} formula_notes={formulas} procedure_notes={procedures} measurement_notes={measurements} canonical_exclusions={len(excluded_rows)}")
    print("process_costing=pass spoilage_logic=pass added_materials=pass formula_atomicity=pass account_level_masking=pass minimal_cloze_scope=pass visible_answer_leakage=0 deterministic_order=pass")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
