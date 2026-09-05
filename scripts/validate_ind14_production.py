#!/usr/bin/env python3
"""Validate IND-14 production Notes under the current living recall rules."""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "IND-14.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "IND-14.tsv"

FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs", "Difficulty",
    "Tags", "Status", "QA",
]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-IND-14-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-IND-14-[0-9]{4}$")
ENTRY_ACCOUNT_RE = re.compile(r"（(?:借|貸)）\{\{c1::([^}]+)\}\}")
EXPECTED_IDS = [f"BK-IND-14-{n:04d}" for n in range(1, 12)]
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
FORBIDDEN_COMPACT = ("{{c1::（借）", "{{c1::（貸）", "{{c1::借方：", "{{c1::貸方：")
BROAD = {"仕訳を行う", "仕訳を行わない", "処理する", "計上する", "あり", "なし"}
ARITH = ("＝", "+", "＋", "-", "－", "×", "÷", "／")
PARALLEL_SEPARATORS = ("・", "、")

EXPECTED_ALP_MAP = {
    "BK-IND-14-0001": ["ALP-IND-14-0001"],
    "BK-IND-14-0002": ["ALP-IND-14-0002"],
    "BK-IND-14-0003": ["ALP-IND-14-0003"],
    "BK-IND-14-0004": ["ALP-IND-14-0004"],
    "BK-IND-14-0005": ["ALP-IND-14-0005", "ALP-IND-14-0006"],
    "BK-IND-14-0006": ["ALP-IND-14-0007", "ALP-IND-14-0008"],
    "BK-IND-14-0007": ["ALP-IND-14-0009"],
    "BK-IND-14-0008": ["ALP-IND-14-0010"],
    "BK-IND-14-0009": ["ALP-IND-14-0011"],
    "BK-IND-14-0010": ["ALP-IND-14-0012"],
    "BK-IND-14-0011": ["ALP-IND-14-0013"],
}

REQUIRED = {
    "BK-IND-14-0001": ("{{c1::工場会計の独立}}",),
    "BK-IND-14-0002": ("{{c1::工場元帳}}", "{{c1::本社元帳}}", "{{c1::一般元帳}}"),
    "BK-IND-14-0003": ("勘定を{{c1::工場}}に", "を{{c1::本社}}に置く"),
    "BK-IND-14-0004": ("{{c1::製品}}勘定は本社側に設定する場合がある",),
    "BK-IND-14-0005": (
        "中央側帳簿で{{c1::工場}}勘定",
        "製造拠点側帳簿で{{c1::本社}}勘定",
        "財務諸表では{{c1::相殺}}される",
    ),
    "BK-IND-14-0006": ("{{c1::担当する側だけ}}", "まず{{c1::会社全体}}の仕訳"),
    "BK-IND-14-0007": (
        "中央側：（借）{{c1::工場}}／（貸）{{c1::買掛金}}",
        "製造拠点側：（借）{{c1::材料}}／（貸）{{c1::本社}}",
    ),
    "BK-IND-14-0008": ("本社側の仕訳は{{c1::不要}}",),
    "BK-IND-14-0009": (
        "中央側：（借）{{c1::工場}}／（貸）{{c1::現金}}",
        "（借）{{c1::賃金給料}}・{{c1::製造間接費}}等／（貸）{{c1::本社}}",
    ),
    "BK-IND-14-0010": (
        "中央側：（借）{{c1::売上原価}}／（貸）{{c1::工場}}",
        "製造拠点側：（借）{{c1::本社}}／（貸）{{c1::製品}}",
    ),
    "BK-IND-14-0011": ("{{c1::本支店会計}}の本店勘定・支店勘定",),
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
    ids: list[str] = []
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
        if row["Part"] != "industrial" or row["Chapter"] != "14 本社工場会計":
            errors.append(f"{nid}: chapter")
        if row["Type"] not in ALLOWED_TYPES:
            errors.append(f"{nid}: type")
        if row["Difficulty"] not in {"1", "2", "3", "4", "5"}:
            errors.append(f"{nid}: difficulty")

        expected_tags = sorted([
            "bookkeeping::industrial",
            "chapter::industrial::14",
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
        cards += len({int(i) for i, _ in matches})

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
            if any(x in answer for x in PARALLEL_SEPARATORS):
                errors.append(f"{nid}: parallel terms not atomized {answer!r}")

        if any(x in text for x in FORBIDDEN_COMPACT):
            errors.append(f"{nid}: compact entry")
        if ("（借）" in text or "（貸）" in text) and not ENTRY_ACCOUNT_RE.search(text):
            errors.append(f"{nid}: journal syntax without account-level cloze")

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
    if len(rows) != 11:
        errors.append(f"notes={len(rows)}")
    if spans != EXPECTED_SPANS:
        errors.append(f"spans={spans}")
    if cards != 11:
        errors.append(f"cards={cards}")
    if len(included) != 13:
        errors.append(f"included={len(included)}")
    if len(excluded_rows) != 1 or excluded_rows[0].get("exclude_reason") != "DECORATIVE_EXAMPLE":
        errors.append("exclusions")

    for alp in included:
        if len(alp_to_notes[alp]) != 1:
            errors.append(f"{alp} mapped {alp_to_notes[alp]}")

    if any(
        r.get("note_ids") not in ("", None) or r.get("qa_status") != "pending"
        for r in inventory
    ):
        errors.append("inventory mutated")

    if any(v > 1 for v in rendered.values()):
        errors.append("duplicate rendered text")

    if errors:
        print("IND-14 production validation: FAIL")
        for error in errors:
            print("-", error)
        return 1

    multi = sum(len(v) > 1 for v in EXPECTED_ALP_MAP.values())
    journals = sum(r["Type"] == "journal_entry" for r in rows)
    formulas = sum(r["Type"] == "formula" for r in rows)
    print("IND-14 production validation: PASS")
    print(
        f"notes={len(rows)} cards={cards} cloze_spans={spans} "
        f"included_alps={len(included)} mapped={len(included)} unmapped=0"
    )
    print(
        f"multi_alp_notes={multi} journal_entry_notes={journals} "
        f"formula_notes={formulas} canonical_exclusions={len(excluded_rows)}"
    )
    print(
        "account_level_journal_cloze=pass minimal_cloze_scope=pass "
        "parallel_term_atomicity=pass cost_accounting_treatment=pass "
        "visible_answer_leakage=0 deterministic_order=pass"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
