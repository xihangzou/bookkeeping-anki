#!/usr/bin/env python3
"""Validate COM-16 after cross-chapter deduplication against IND production Notes."""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "COM-16.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "COM-16.tsv"
FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-COM-16-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-COM-16-[0-9]{4}$")
ENTRY_ACCOUNT_RE = re.compile(r"（(?:借|貸)）\{\{c1::([^}]+)\}\}")
EXPECTED_IDS = [f"BK-COM-16-{n:04d}" for n in range(1, 24)]
EXPECTED_ACTIVE_SPANS = 61
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
FORBIDDEN_COMPACT = ("{{c1::（借）", "{{c1::（貸）", "{{c1::借方：", "{{c1::貸方：")
BROAD = {
    "仕訳を行う", "仕訳を行わない", "処理する", "計上する",
    "減少させる", "増加させる", "あり", "なし",
}
ARITH = ("＝", "+", "＋", "-", "－", "×", "÷", "／")

ACTIVE_ALP_MAP = {
    "BK-COM-16-0001": [
        "ALP-COM-16-0001", "ALP-COM-16-0002", "ALP-COM-16-0003", "ALP-COM-16-0004",
    ],
    "BK-COM-16-0004": ["ALP-COM-16-0005", "ALP-COM-16-0006", "ALP-COM-16-0007"],
    "BK-COM-16-0007": ["ALP-COM-16-0008", "ALP-COM-16-0009"],
    "BK-COM-16-0009": ["ALP-COM-16-0010", "ALP-COM-16-0011", "ALP-COM-16-0012"],
    "BK-COM-16-0012": ["ALP-COM-16-0013", "ALP-COM-16-0014", "ALP-COM-16-0015"],
    "BK-COM-16-0015": ["ALP-COM-16-0016", "ALP-COM-16-0017", "ALP-COM-16-0018"],
    "BK-COM-16-0018": ["ALP-COM-16-0019", "ALP-COM-16-0020"],
    "BK-COM-16-0020": ["ALP-COM-16-0021", "ALP-COM-16-0022"],
    "BK-COM-16-0022": ["ALP-COM-16-0023", "ALP-COM-16-0024"],
}

HISTORICAL_ALP_MAP = {
    "BK-COM-16-0002": ["ALP-COM-16-0002", "ALP-COM-16-0003"],
    "BK-COM-16-0003": ["ALP-COM-16-0004"],
    "BK-COM-16-0005": ["ALP-COM-16-0006"],
    "BK-COM-16-0006": ["ALP-COM-16-0007"],
    "BK-COM-16-0008": ["ALP-COM-16-0009"],
    "BK-COM-16-0010": ["ALP-COM-16-0011"],
    "BK-COM-16-0011": ["ALP-COM-16-0012"],
    "BK-COM-16-0013": ["ALP-COM-16-0014"],
    "BK-COM-16-0014": ["ALP-COM-16-0015"],
    "BK-COM-16-0016": ["ALP-COM-16-0017"],
    "BK-COM-16-0017": ["ALP-COM-16-0018"],
    "BK-COM-16-0019": ["ALP-COM-16-0020"],
    "BK-COM-16-0021": ["ALP-COM-16-0022"],
    "BK-COM-16-0023": ["ALP-COM-16-0024"],
}

DEPRECATED_TO = {
    "BK-COM-16-0002": "BK-COM-16-0001",
    "BK-COM-16-0003": "BK-COM-16-0001",
    "BK-COM-16-0005": "BK-COM-16-0004",
    "BK-COM-16-0006": "BK-COM-16-0004",
    "BK-COM-16-0008": "BK-COM-16-0007",
    "BK-COM-16-0010": "BK-COM-16-0009",
    "BK-COM-16-0011": "BK-COM-16-0009",
    "BK-COM-16-0013": "BK-COM-16-0012",
    "BK-COM-16-0014": "BK-COM-16-0012",
    "BK-COM-16-0016": "BK-COM-16-0015",
    "BK-COM-16-0017": "BK-COM-16-0015",
    "BK-COM-16-0019": "BK-COM-16-0018",
    "BK-COM-16-0021": "BK-COM-16-0020",
    "BK-COM-16-0023": "BK-COM-16-0022",
}

REQUIRED = {
    "BK-COM-16-0001": (
        "{{c1::製造業会計}}", "{{c1::1か月}}", "{{c1::製造原価}}",
        "{{c1::売上原価}}", "{{c1::原価差異}}", "{{c1::決算振替仕訳}}",
    ),
    "BK-COM-16-0004": (
        "直接材料費→（借）{{c1::仕掛品}}", "間接材料費→（借）{{c1::製造間接費}}",
        "材料帳簿棚卸高＝月初の{{c1::材料残高}}＋当月の{{c1::購入高}}－当月の{{c1::消費高}}",
        "（借）{{c1::製造間接費}}／（貸）{{c1::棚卸減耗損}}",
    ),
    "BK-COM-16-0007": (
        "当月賃金消費高＝当月の{{c1::賃金支払額}}＋当月末の{{c1::未払賃金}}－前月末の{{c1::未払賃金}}",
        "直接労務費は{{c1::仕掛品}}", "間接労務費は{{c1::製造間接費}}",
    ),
    "BK-COM-16-0009": (
        "退職給付費用＝{{c1::年間見積額}}÷12", "{{c1::製造部門}}対応分",
        "工場の水道光熱費などの間接経費は{{c1::製造間接費}}",
        "減価償却費は資産ごとの{{c1::月額}}", "{{c1::販売費及び一般管理費}}側",
    ),
    "BK-COM-16-0012": (
        "{{c1::予定配賦額}}を{{c1::仕掛品}}へ振り替え",
        "原価差異＝{{c1::予定配賦額}}－{{c1::実際発生額}}",
        "{{c1::不利差異}}", "{{c1::借方}}", "{{c1::有利差異}}", "{{c1::貸方}}",
    ),
    "BK-COM-16-0015": (
        "当月製造原価＝{{c1::直接材料費}}＋{{c1::直接労務費}}＋{{c1::製造間接費予定配賦額}}",
        "完成品原価＝月初の{{c1::仕掛品}}＋当月製造原価－月末の{{c1::仕掛品}}",
        "（借）{{c1::製品}}／（貸）{{c1::仕掛品}}",
    ),
    "BK-COM-16-0018": (
        "当月{{c1::売上原価}}＝月初の{{c1::製品}}＋{{c1::完成品原価}}－月末の{{c1::製品}}",
        "（借）{{c1::売上原価}}／（貸）{{c1::製品}}",
    ),
    "BK-COM-16-0020": (
        "不利差異は（借）{{c1::売上原価}}／（貸）{{c1::原価差異}}",
        "有利差異は（借）{{c1::原価差異}}／（貸）{{c1::売上原価}}",
        "{{c1::販売費及び一般管理費}}側",
    ),
    "BK-COM-16-0022": (
        "{{c1::材料}}・{{c1::仕掛品}}・{{c1::製品}}",
        "{{c1::棚卸資産}}", "{{c1::繰越利益剰余金}}",
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

    active_alp_to_notes: defaultdict[str, list[str]] = defaultdict(list)
    active_rendered = Counter()
    active_spans = 0
    ids: list[str] = []
    active_ids: list[str] = []
    deprecated_ids: list[str] = []

    for row in rows:
        nid = row["ID"]
        ids.append(nid)
        status = row["Status"]

        if not NOTE_RE.fullmatch(nid):
            errors.append(f"{nid}: invalid ID")
        if status not in {"approved", "deprecated"} or row["QA"] != "pass":
            errors.append(f"{nid}: lifecycle")
        if (row["SourceRepo"], row["SourceCommit"], row["SourcePath"]) != SOURCE:
            errors.append(f"{nid}: source")
        if row["Part"] != "commercial" or row["Chapter"] != "16 製造業会計":
            errors.append(f"{nid}: chapter")
        if row["Type"] not in ALLOWED_TYPES:
            errors.append(f"{nid}: type")
        if row["Difficulty"] not in {"1", "2", "3", "4", "5"}:
            errors.append(f"{nid}: difficulty")

        tags = sorted([
            "bookkeeping::commercial", "chapter::commercial::16",
            f"difficulty::{row['Difficulty']}", f"status::{status}",
            f"topic::{row['Topic'].strip().replace(' ', '_')}", f"type::{row['Type']}",
        ])
        if row["Tags"].split() != tags:
            errors.append(f"{nid}: tags")

        text = row["Text"]
        matches = CLOZE_RE.findall(text)
        if not matches or {int(i) for i, _ in matches} != {1}:
            errors.append(f"{nid}: c1-only")
        if any(x in text for x in FORBIDDEN_COMPACT):
            errors.append(f"{nid}: compact entry")
        if ("（借）" in text or "（貸）" in text) and not ENTRY_ACCOUNT_RE.search(text):
            errors.append(f"{nid}: journal syntax without account-level cloze")

        alps = row["ALP_IDs"].split()
        for alp in alps:
            if not ALP_RE.fullmatch(alp) or alp not in included_set:
                errors.append(f"{nid}: invalid ALP {alp}")

        if status == "approved":
            active_ids.append(nid)
            expected_alps = ACTIVE_ALP_MAP.get(nid)
            if expected_alps is None:
                errors.append(f"{nid}: unexpected approved Note")
            elif alps != expected_alps:
                errors.append(f"{nid}: active ALP map")

            active_spans += len(matches)
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

            for required in REQUIRED.get(nid, ()):
                if required not in text:
                    errors.append(f"{nid}: missing precision {required!r}")

            active_rendered[CLOZE_RE.sub("[…]", text)] += 1
            for alp in alps:
                if alp in included_set:
                    active_alp_to_notes[alp].append(nid)
            if alps and inv_by.get(alps[0]) and row["Section"] != inv_by[alps[0]]["source_section"]:
                errors.append(f"{nid}: primary section")

        else:
            deprecated_ids.append(nid)
            replacement = DEPRECATED_TO.get(nid)
            if replacement is None:
                errors.append(f"{nid}: unexpected deprecated Note")
            else:
                if f"統合先: {replacement}" not in row["Extra"]:
                    errors.append(f"{nid}: missing replacement mapping")
                replacement_alps = set(ACTIVE_ALP_MAP[replacement])
                if not set(alps).issubset(replacement_alps):
                    errors.append(f"{nid}: historical ALPs not covered by {replacement}")
            if alps != HISTORICAL_ALP_MAP.get(nid):
                errors.append(f"{nid}: historical ALP lineage changed")

    if ids != EXPECTED_IDS:
        errors.append("stable IDs/order")
    if set(active_ids) != set(ACTIVE_ALP_MAP):
        errors.append(f"active IDs={active_ids}")
    if set(deprecated_ids) != set(DEPRECATED_TO):
        errors.append(f"deprecated IDs={deprecated_ids}")
    if len(rows) != 23:
        errors.append(f"rows={len(rows)}")
    if len(active_ids) != 9:
        errors.append(f"active_notes={len(active_ids)}")
    if len(deprecated_ids) != 14:
        errors.append(f"deprecated_notes={len(deprecated_ids)}")
    if active_spans != EXPECTED_ACTIVE_SPANS:
        errors.append(f"active_spans={active_spans}")
    if len(included) != 24:
        errors.append(f"included={len(included)}")
    if len(excluded_rows) != 1 or excluded_rows[0].get("exclude_reason") != "DECORATIVE_EXAMPLE":
        errors.append("exclusions")

    for alp in included:
        if len(active_alp_to_notes[alp]) != 1:
            errors.append(f"{alp} active mapped {active_alp_to_notes[alp]}")

    if any(r.get("note_ids") not in ("", None) or r.get("qa_status") != "pending" for r in inventory):
        errors.append("inventory mutated")
    if any(count > 1 for count in active_rendered.values()):
        errors.append("duplicate active rendered text")

    if errors:
        print("COM-16 production validation: FAIL")
        for error in errors:
            print("-", error)
        return 1

    print("COM-16 production validation: PASS")
    print(
        f"rows={len(rows)} active_notes={len(active_ids)} deprecated_notes={len(deprecated_ids)} "
        f"active_cards={len(active_ids)} active_cloze_spans={active_spans}"
    )
    print(
        f"included_alps={len(included)} active_mapped={len(included)} active_unmapped=0 "
        f"historical_replacements={len(deprecated_ids)} canonical_exclusions={len(excluded_rows)}"
    )
    print(
        "cross_chapter_dedup=pass active_exact_once_alp_coverage=pass stable_id_lineage=pass "
        "account_level_journal_cloze=pass formula_atomicity=pass minimal_cloze_scope=pass "
        "visible_answer_leakage=0 deterministic_order=pass"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
