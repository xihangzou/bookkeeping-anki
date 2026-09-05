#!/usr/bin/env python3
"""Validate COM-15 production Notes under the current living recall rules."""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "COM-15.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "COM-15.tsv"
FIELDS = ["ID","Text","Extra","SourceRepo","SourceCommit","SourcePath","Part","Chapter","Section","Topic","Type","ALP_IDs","Difficulty","Tags","Status","QA"]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-COM-15-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-COM-15-[0-9]{4}$")
ENTRY_ACCOUNT_RE = re.compile(r"（(?:借|貸)）\{\{c[1-9][0-9]*::([^}]+)\}\}")
EXPECTED_IDS = [f"BK-COM-15-{n:04d}" for n in range(1,45)]
EXPECTED_SPANS = 110
EXPECTED_CARDS = 50
SOURCE = ("xihangzou/bookkeeping-integrated","569ed7b82e729334e1472286eaca7c4352e6fbdb","merged/textbook.md")
ALLOWED_TYPES = {"definition","classification","recognition","measurement","journal_entry","formula","procedure","comparison","exception","reasoning","ledger","financial_statement","cost_accounting"}
BROAD = {"仕訳を行う","仕訳を行わない","処理する","計上する","減少させる","増加させる","あり","なし"}
ARITH = ("＝","+","＋","-","－","×","÷","／")
PARALLEL = ("・","、")
FORBIDDEN_COMPACT = ("{{c1::（借）","{{c1::（貸）","{{c2::（借）","{{c2::（貸）","{{c3::（借）","{{c3::（貸）")

EXPECTED_ALP_MAP = {}
alp = 1
for note in range(1,45):
    if note == 3:
        vals = [3,4]
        alp = 5
    elif note == 40:
        vals = [41,42]
        alp = 43
    else:
        vals = [alp]
        alp += 1
    EXPECTED_ALP_MAP[f"BK-COM-15-{note:04d}"] = [f"ALP-COM-15-{v:04d}" for v in vals]

EXPECTED_GROUPS = {
    **{f"BK-COM-15-{n:04d}": {1} for n in range(1,45)},
    "BK-COM-15-0023": {1,2,3},
    "BK-COM-15-0024": {1,2,3},
    "BK-COM-15-0044": {1,2,3},
}

REQUIRED = {
    "BK-COM-15-0003": ("{{c1::単純合算}}","{{c1::連結修正仕訳}}","{{c1::連結精算表}}"),
    "BK-COM-15-0005": ("{{c1::親会社株主に帰属する当期純利益}}＝当期純利益－{{c1::非支配株主に帰属する当期純利益}}",),
    "BK-COM-15-0007": ("（借）{{c1::資本金}}・{{c1::資本剰余金}}・{{c1::利益剰余金}}／（貸）{{c1::子会社株式}}",),
    "BK-COM-15-0008": ("完全所有ののれん＝{{c1::子会社株式取得原価}}－支配獲得時の{{c1::子会社資本合計}}",),
    "BK-COM-15-0011": ("（借）{{c1::のれん償却}}／（貸）{{c1::のれん}}",),
    "BK-COM-15-0013": ("（借）{{c1::受取配当金}}／（貸）{{c1::利益剰余金}}",),
    "BK-COM-15-0015": ("非支配株主持分＝{{c1::子会社資本合計}}×{{c1::非支配株主持分比率}}",),
    "BK-COM-15-0016": ("部分所有ののれん＝{{c1::子会社株式取得原価}}－{{c1::子会社資本合計}}×{{c1::親会社持分比率}}",),
    "BK-COM-15-0019": ("（借）{{c1::非支配株主に帰属する当期純利益}}／（貸）{{c1::非支配株主持分}}",),
    "BK-COM-15-0020": ("（借）{{c1::受取配当金}}","（借）{{c1::非支配株主持分}}","（貸）{{c1::利益剰余金}}"),
    "BK-COM-15-0021": ("（借）{{c1::利益剰余金}}／（貸）{{c1::非支配株主持分}}",),
    "BK-COM-15-0023": ("（借）{{c1::売上高}}／（貸）{{c1::売上原価}}","（借）{{c2::買掛金}}／（貸）{{c2::売掛金}}","（借）{{c3::支払手形}}／（貸）{{c3::受取手形}}"),
    "BK-COM-15-0024": ("（借）{{c1::借入金}}／（貸）{{c1::貸付金}}","（借）{{c2::受取利息}}／（貸）{{c2::支払利息}}","（借）{{c3::未払費用}}／（貸）{{c3::未収収益}}"),
    "BK-COM-15-0028": ("（借）{{c1::売上原価}}／（貸）{{c1::商品}}",),
    "BK-COM-15-0029": ("未実現利益＝{{c1::内部在庫額}}×{{c1::利益率}}",),
    "BK-COM-15-0030": ("未実現利益＝{{c1::内部在庫額}}÷（1＋{{c1::利益加算率}}）×{{c1::利益加算率}}",),
    "BK-COM-15-0031": ("（借）{{c1::利益剰余金}}／（貸）{{c1::売上原価}}",),
    "BK-COM-15-0032": ("（借）{{c1::土地売却益}}／（貸）{{c1::土地}}",),
    "BK-COM-15-0034": ("（借）{{c1::利益剰余金}}／（貸）{{c1::土地}}",),
    "BK-COM-15-0035": ("（借）{{c1::貸倒引当金}}／（貸）{{c1::貸倒引当金繰入}}",),
    "BK-COM-15-0038": ("（借）{{c1::非支配株主持分}}／（貸）{{c1::非支配株主に帰属する当期純利益}}",),
    "BK-COM-15-0039": ("子会社利益を減らす","子会社利益を増やす"),
    "BK-COM-15-0040": ("（借）{{c1::支払手形}}／（貸）{{c1::借入金}}","（借）{{c1::支払手形}}／（貸）{{c1::受取手形}}"),
    "BK-COM-15-0044": ("資本金・{{c1::当期首残高}}","利益剰余金・{{c2::剰余金の配当}}","非支配株主持分・{{c3::当期変動額}}"),
}

def rendered_for_group(text: str, target: int) -> str:
    return CLOZE_RE.sub(lambda m: "" if int(m.group(1)) == target else m.group(2), text)

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

    inc = [r for r in inv if r.get("status") == "INCLUDE"]
    exc = [r for r in inv if r.get("status") == "EXCLUDE"]
    included = [r["alp_id"] for r in inc]
    included_set = set(included)
    inv_by = {r["alp_id"]: r for r in inc}
    alp_to_notes = defaultdict(list)
    rendered = Counter()
    ids = []
    spans = 0
    cards = 0

    for row in rows:
        nid = row["ID"]
        ids.append(nid)
        if not NOTE_RE.fullmatch(nid):
            errors.append(f"{nid}: invalid ID")
        if row["Status"] != "approved" or row["QA"] != "pass":
            errors.append(f"{nid}: lifecycle")
        if (row["SourceRepo"], row["SourceCommit"], row["SourcePath"]) != SOURCE:
            errors.append(f"{nid}: source")
        if row["Part"] != "commercial" or row["Chapter"] != "15 連結会計":
            errors.append(f"{nid}: chapter")
        if row["Type"] not in ALLOWED_TYPES:
            errors.append(f"{nid}: type")
        if row["Difficulty"] not in {"1","2","3","4","5"}:
            errors.append(f"{nid}: difficulty")

        tags = sorted([
            "bookkeeping::commercial",
            "chapter::commercial::15",
            f"difficulty::{row['Difficulty']}",
            "status::approved",
            f"topic::{row['Topic'].strip().replace(' ','_')}",
            f"type::{row['Type']}",
        ])
        if row["Tags"].split() != tags:
            errors.append(f"{nid}: tags")

        text = row["Text"]
        ms = CLOZE_RE.findall(text)
        spans += len(ms)
        groups = {int(i) for i,_ in ms}
        cards += len(groups)
        if not ms or groups != EXPECTED_GROUPS.get(nid):
            errors.append(f"{nid}: cloze groups {groups}")
        if any(x in text for x in FORBIDDEN_COMPACT):
            errors.append(f"{nid}: compact journal Cloze")
        if ("（借）" in text or "（貸）" in text) and not ENTRY_ACCOUNT_RE.search(text):
            errors.append(f"{nid}: journal syntax without account-level Cloze")

        for group in groups:
            visible = rendered_for_group(text, group)
            answers = [a.strip() for i,a in ms if int(i) == group]
            for answer in answers:
                if len(answer) >= 2 and answer in visible:
                    errors.append(f"{nid} c{group}: visible leakage {answer!r}")
                if answer in BROAD:
                    errors.append(f"{nid} c{group}: broad answer {answer!r}")
                if any(x in answer for x in ARITH):
                    errors.append(f"{nid} c{group}: operator hidden {answer!r}")
                if any(x in answer for x in PARALLEL):
                    errors.append(f"{nid} c{group}: non-atomic parallel answer {answer!r}")

        for req in REQUIRED.get(nid, ()):
            if req not in text:
                errors.append(f"{nid}: missing precision {req!r}")

        rendered[CLOZE_RE.sub("[…]", text)] += 1
        alps = row["ALP_IDs"].split()
        if alps != EXPECTED_ALP_MAP.get(nid):
            errors.append(f"{nid}: ALP map {alps}")
        for alp_id in alps:
            if not ALP_RE.fullmatch(alp_id) or alp_id not in included_set:
                errors.append(f"{nid}: invalid ALP {alp_id}")
            else:
                alp_to_notes[alp_id].append(nid)
        if alps and inv_by.get(alps[0]) and row["Section"] != inv_by[alps[0]]["source_section"]:
            errors.append(f"{nid}: section")

    if ids != EXPECTED_IDS:
        errors.append("stable IDs/order")
    if len(rows) != 44:
        errors.append(f"notes={len(rows)}")
    if spans != EXPECTED_SPANS:
        errors.append(f"spans={spans}")
    if cards != EXPECTED_CARDS:
        errors.append(f"cards={cards}")
    if len(included) != 46:
        errors.append(f"included={len(included)}")
    if len(exc) != 1 or exc[0].get("exclude_reason") != "DECORATIVE_EXAMPLE":
        errors.append("exclusions")
    for alp_id in included:
        if len(alp_to_notes[alp_id]) != 1:
            errors.append(f"{alp_id} mapped {alp_to_notes[alp_id]}")
    if any(r.get("note_ids") not in ("", None) or r.get("qa_status") != "pending" for r in inv):
        errors.append("inventory mutated")
    if any(v > 1 for v in rendered.values()):
        errors.append("duplicate rendered text")

    if errors:
        print("COM-15 production validation: FAIL")
        for error in errors:
            print("-", error)
        return 1

    multi = sum(len(v) > 1 for v in EXPECTED_ALP_MAP.values())
    types = Counter(r["Type"] for r in rows)
    print("COM-15 production validation: PASS")
    print(f"notes={len(rows)} cards={cards} cloze_spans={spans} included_alps={len(included)} mapped={len(included)} unmapped=0")
    print(f"multi_alp_notes={multi} journal_entry_notes={types['journal_entry']} formula_notes={types['formula']} financial_statement_notes={types['financial_statement']} canonical_exclusions={len(exc)}")
    print("account_level_journal_cloze=pass formula_atomicity=pass parallel_overload_split=pass minimal_cloze_scope=pass visible_answer_leakage=0 deterministic_order=pass")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
