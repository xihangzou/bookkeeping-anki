#!/usr/bin/env python3
"""Validate COM-07 production Notes under the current living recall rules."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "COM-07.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "COM-07.tsv"

FIELDS = ["ID","Text","Extra","SourceRepo","SourceCommit","SourcePath","Part","Chapter","Section","Topic","Type","ALP_IDs","Difficulty","Tags","Status","QA"]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-COM-07-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-COM-07-[0-9]{4}$")
EXPECTED_IDS = [f"BK-COM-07-{n:04d}" for n in range(1, 15)]
EXPECTED_SPANS = 27
SOURCE = ("xihangzou/bookkeeping-integrated","569ed7b82e729334e1472286eaca7c4352e6fbdb","merged/textbook.md")
ALLOWED_TYPES = {"definition","classification","recognition","measurement","journal_entry","formula","procedure","comparison","exception","reasoning","ledger","financial_statement","cost_accounting"}
ENTRY_ACCOUNT_RE = re.compile(r"（(?:借|貸)）\{\{c1::([^}]+)\}\}")
FORBIDDEN_COMPACT = ("{{c1::（借）", "{{c1::（貸）", "{{c1::借方：", "{{c1::貸方：")
BROAD_ACTION_ANSWERS = {"仕訳を行う","仕訳を行わない","処理する","計上する","減少させる","増加させる"}
ARITHMETIC_TOKENS = ("＝", "+", "＋", "-", "－", "×", "÷", "／")

EXPECTED_ALP_MAP = {
    "BK-COM-07-0001": ["ALP-COM-07-0001"],
    "BK-COM-07-0002": ["ALP-COM-07-0002"],
    "BK-COM-07-0003": ["ALP-COM-07-0003"],
    "BK-COM-07-0004": ["ALP-COM-07-0004"],
    "BK-COM-07-0005": ["ALP-COM-07-0005"],
    "BK-COM-07-0006": ["ALP-COM-07-0006", "ALP-COM-07-0010", "ALP-COM-07-0011"],
    "BK-COM-07-0007": ["ALP-COM-07-0007"],
    "BK-COM-07-0008": ["ALP-COM-07-0008"],
    "BK-COM-07-0009": ["ALP-COM-07-0009"],
    "BK-COM-07-0010": ["ALP-COM-07-0012", "ALP-COM-07-0013"],
    "BK-COM-07-0011": ["ALP-COM-07-0014", "ALP-COM-07-0015"],
    "BK-COM-07-0012": ["ALP-COM-07-0016"],
    "BK-COM-07-0013": ["ALP-COM-07-0017", "ALP-COM-07-0018"],
    "BK-COM-07-0014": ["ALP-COM-07-0019"],
}

REQUIRED = {
    "BK-COM-07-0001": ("{{c1::研究開発}}", "{{c1::研究開発費}}"),
    "BK-COM-07-0002": ("発生時に{{c1::研究開発費}}",),
    "BK-COM-07-0003": ("{{c1::無形固定資産}}",),
    "BK-COM-07-0004": ("{{c1::特許権}}", "{{c1::商標権}}", "{{c1::ソフトウェア}}", "{{c1::のれん}}"),
    "BK-COM-07-0005": ("{{c1::取得原価}}", "特許権等の対象資産"),
    "BK-COM-07-0006": ("残存価額{{c1::ゼロ}}", "{{c1::定額法}}", "{{c1::直接法}}", "{{c1::間接法}}"),
    "BK-COM-07-0007": ("{{c1::特許権償却}}", "減価償却費ではなく"),
    "BK-COM-07-0008": ("{{c1::月割}}",),
    "BK-COM-07-0009": ("年額償却費＝{{c1::取得原価}}÷{{c1::有効期間}}",),
    "BK-COM-07-0010": ("研究開発目的・自社利用目的・市場販売目的", "{{c1::研究開発費}}", "{{c1::範囲外}}"),
    "BK-COM-07-0011": ("{{c1::収益獲得}}", "{{c1::費用削減}}", "購入したものはこの条件を満たす"),
    "BK-COM-07-0012": ("（借）{{c1::ソフトウェア}}／（貸）現金等",),
    "BK-COM-07-0013": ("（借）{{c1::ソフトウェア仮勘定}}／（貸）現金等", "（借）{{c1::ソフトウェア}}／（貸）{{c1::ソフトウェア仮勘定}}・現金等"),
    "BK-COM-07-0014": ("（借）{{c1::ソフトウェア償却}}／（貸）{{c1::ソフトウェア}}", "残存価額ゼロ・定額法・直接法"),
}


def main() -> int:
    errors: list[str] = []

    with NOTES.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        header, rows = list(reader.fieldnames or []), list(reader)
    with INVENTORY.open(encoding="utf-8", newline="") as fh:
        inventory = list(csv.DictReader(fh, delimiter="\t"))

    if header != FIELDS:
        errors.append("header mismatch")

    included_rows = [r for r in inventory if r.get("status") == "INCLUDE"]
    included = [r["alp_id"] for r in included_rows]
    included_set = set(included)
    excluded = [r for r in inventory if r.get("status") == "EXCLUDE"]
    inventory_by_alp = {r["alp_id"]: r for r in included_rows}

    alp_to_notes: dict[str, list[str]] = defaultdict(list)
    ids: list[str] = []
    spans = 0
    rendered_texts: Counter[str] = Counter()
    primary_alp_numbers: list[int] = []

    for row in rows:
        nid = row["ID"]
        ids.append(nid)

        if not NOTE_RE.fullmatch(nid):
            errors.append(f"{nid}: invalid ID")
        if row["Status"] != "approved" or row["QA"] != "pass":
            errors.append(f"{nid}: lifecycle must be approved/pass")
        if (row["SourceRepo"], row["SourceCommit"], row["SourcePath"]) != SOURCE:
            errors.append(f"{nid}: source provenance mismatch")
        if row["Part"] != "commercial" or row["Chapter"] != "07 無形資産":
            errors.append(f"{nid}: part/chapter mismatch")
        if row["Type"] not in ALLOWED_TYPES:
            errors.append(f"{nid}: invalid type {row['Type']!r}")

        try:
            difficulty = int(row["Difficulty"])
        except ValueError:
            difficulty = 0
        if difficulty not in {1,2,3,4,5}:
            errors.append(f"{nid}: invalid difficulty")

        expected_tags = sorted([
            "bookkeeping::commercial",
            "chapter::commercial::07",
            f"difficulty::{row['Difficulty']}",
            "status::approved",
            f"topic::{row['Topic'].strip().replace(' ', '_')}",
            f"type::{row['Type']}",
        ])
        if row["Tags"].split() != expected_tags:
            errors.append(f"{nid}: required tags/order mismatch")

        text = row["Text"]
        matches = CLOZE_RE.findall(text)
        spans += len(matches)
        if not matches or {int(i) for i, _ in matches} != {1}:
            errors.append(f"{nid}: approved Notes must use c1 only")

        answers = [a.strip() for _, a in matches]
        visible = CLOZE_RE.sub("", text)
        for answer in answers:
            if len(answer) >= 2 and answer in visible:
                errors.append(f"{nid}: visible answer leakage {answer!r}")
            if answer in BROAD_ACTION_ANSWERS:
                errors.append(f"{nid}: broad/non-atomic Cloze answer {answer!r}")
            if any(x in answer for x in ("（借）","（貸）","借方：","貸方：")):
                errors.append(f"{nid}: journal syntax inside Cloze {answer!r}")
            if any(token in answer for token in ARITHMETIC_TOKENS):
                errors.append(f"{nid}: formula/operator structure hidden inside Cloze {answer!r}")

        for old in FORBIDDEN_COMPACT:
            if old in text:
                errors.append(f"{nid}: compact whole-entry Cloze retained {old!r}")

        for req in REQUIRED.get(nid, ()):
            if req not in text:
                errors.append(f"{nid}: missing required precision form {req!r}")

        if nid == "BK-COM-07-0013" and text.count("{{c1::ソフトウェア仮勘定}}") != 2:
            errors.append(f"{nid}: both in-progress and completion occurrences must be hidden")

        if row["Type"] == "journal_entry" and not ENTRY_ACCOUNT_RE.search(text):
            errors.append(f"{nid}: missing account-level journal Cloze")

        rendered = CLOZE_RE.sub("[…]", text)
        rendered_texts[rendered] += 1

        alps = row["ALP_IDs"].split()
        if alps != EXPECTED_ALP_MAP.get(nid):
            errors.append(f"{nid}: ALP mapping differs from deterministic design")
        if not alps:
            errors.append(f"{nid}: missing ALP mapping")
        else:
            primary_alp_numbers.append(int(alps[0].rsplit("-", 1)[1]))

        alp_nums = [int(a.rsplit("-", 1)[1]) for a in alps if ALP_RE.fullmatch(a)]
        if alp_nums != sorted(alp_nums):
            errors.append(f"{nid}: ALP IDs not in canonical order")

        for alp in alps:
            if not ALP_RE.fullmatch(alp) or alp not in included_set:
                errors.append(f"{nid}: invalid/nonincluded ALP {alp}")
                continue
            alp_to_notes[alp].append(nid)

        if alps:
            first = inventory_by_alp.get(alps[0])
            if first and row["Section"] != first["source_section"]:
                errors.append(f"{nid}: primary Section mismatch")

    if ids != EXPECTED_IDS:
        errors.append("stable Note IDs/order mismatch")
    if len(rows) != 14:
        errors.append(f"expected 14 Notes, got {len(rows)}")
    if len(included) != 19:
        errors.append(f"expected 19 included ALPs, got {len(included)}")
    if len(excluded) != 2:
        errors.append(f"expected 2 canonical exclusions, got {len(excluded)}")
    if sum(r.get("exclude_reason") == "DUPLICATE_EXACT" for r in excluded) != 1:
        errors.append("expected one DUPLICATE_EXACT exclusion")
    if sum(r.get("exclude_reason") == "DECORATIVE_EXAMPLE" for r in excluded) != 1:
        errors.append("expected one DECORATIVE_EXAMPLE exclusion")
    if spans != EXPECTED_SPANS:
        errors.append(f"expected {EXPECTED_SPANS} Cloze spans, got {spans}")
    if primary_alp_numbers != sorted(primary_alp_numbers):
        errors.append("Note order is not deterministic by primary ALP")

    bad_map = [alp for alp in included if len(alp_to_notes.get(alp, [])) != 1]
    if bad_map:
        errors.append(f"ALPs not mapped exactly once: {bad_map}")

    duplicate_rendered = [t for t, c in rendered_texts.items() if c > 1]
    if duplicate_rendered:
        errors.append(f"duplicate rendered Note text: {len(duplicate_rendered)}")

    for row in inventory:
        if row.get("note_ids") or row.get("qa_status") != "pending":
            errors.append("canonical ANKI-003 inventory must remain unmapped/pending")
            break

    if errors:
        print("COM-07 production validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    multi_alp = sum(1 for row in rows if len(row["ALP_IDs"].split()) > 1)
    journal = sum(1 for row in rows if row["Type"] == "journal_entry")
    formulas = sum(1 for row in rows if row["Type"] == "formula")

    print("COM-07 production validation: PASS")
    print("notes=14 cards=14 cloze_spans=27 included_alps=19 mapped=19 unmapped=0")
    print(f"multi_alp_notes={multi_alp} journal_entry_notes={journal} formula_notes={formulas} canonical_exclusions=2")
    print("account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass formula_atomicity=pass visible_answer_leakage=0 deterministic_order=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
