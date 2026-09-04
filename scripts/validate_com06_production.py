#!/usr/bin/env python3
"""Validate COM-06 production Notes under the current living recall rules."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "COM-06.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "COM-06.tsv"

FIELDS = ["ID","Text","Extra","SourceRepo","SourceCommit","SourcePath","Part","Chapter","Section","Topic","Type","ALP_IDs","Difficulty","Tags","Status","QA"]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-COM-06-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-COM-06-[0-9]{4}$")
EXPECTED_IDS = [f"BK-COM-06-{n:04d}" for n in range(1, 41)]
EXPECTED_SPANS = 88
SOURCE = ("xihangzou/bookkeeping-integrated","569ed7b82e729334e1472286eaca7c4352e6fbdb","merged/textbook.md")
ALLOWED_TYPES = {"definition","classification","recognition","measurement","journal_entry","formula","procedure","comparison","exception","reasoning","ledger","financial_statement","cost_accounting"}
ENTRY_ACCOUNT_RE = re.compile(r"（(?:借|貸)）\{\{c1::([^}]+)\}\}")
FORBIDDEN_COMPACT = ("{{c1::（借）", "{{c1::（貸）", "{{c1::借方：", "{{c1::貸方：")
BROAD_ACTION_ANSWERS = {"仕訳を行う","仕訳を行わない","処理する","計上する","減少させる","増加させる"}
ARITHMETIC_TOKENS = ("＝", "+", "＋", "-", "－", "×", "÷", "／")

EXPECTED_ALP_MAP = {
    "BK-COM-06-0001": ["ALP-COM-06-0001"],
    "BK-COM-06-0002": ["ALP-COM-06-0002"],
    "BK-COM-06-0003": ["ALP-COM-06-0003"],
    "BK-COM-06-0004": ["ALP-COM-06-0004"],
    "BK-COM-06-0005": ["ALP-COM-06-0005"],
    "BK-COM-06-0006": ["ALP-COM-06-0006"],
    "BK-COM-06-0007": ["ALP-COM-06-0007"],
    "BK-COM-06-0008": ["ALP-COM-06-0008"],
    "BK-COM-06-0009": ["ALP-COM-06-0009"],
    "BK-COM-06-0010": ["ALP-COM-06-0010"],
    "BK-COM-06-0011": ["ALP-COM-06-0011"],
    "BK-COM-06-0012": ["ALP-COM-06-0012"],
    "BK-COM-06-0013": ["ALP-COM-06-0013"],
    "BK-COM-06-0014": ["ALP-COM-06-0014"],
    "BK-COM-06-0015": ["ALP-COM-06-0015"],
    "BK-COM-06-0016": ["ALP-COM-06-0016", "ALP-COM-06-0031"],
    "BK-COM-06-0017": ["ALP-COM-06-0017"],
    "BK-COM-06-0018": ["ALP-COM-06-0018"],
    "BK-COM-06-0019": ["ALP-COM-06-0019"],
    "BK-COM-06-0020": ["ALP-COM-06-0020"],
    "BK-COM-06-0021": ["ALP-COM-06-0021"],
    "BK-COM-06-0022": ["ALP-COM-06-0022"],
    "BK-COM-06-0023": ["ALP-COM-06-0023"],
    "BK-COM-06-0024": ["ALP-COM-06-0024"],
    "BK-COM-06-0025": ["ALP-COM-06-0025"],
    "BK-COM-06-0026": ["ALP-COM-06-0026"],
    "BK-COM-06-0027": ["ALP-COM-06-0027", "ALP-COM-06-0028"],
    "BK-COM-06-0028": ["ALP-COM-06-0029"],
    "BK-COM-06-0029": ["ALP-COM-06-0030"],
    "BK-COM-06-0030": ["ALP-COM-06-0032", "ALP-COM-06-0033"],
    "BK-COM-06-0031": ["ALP-COM-06-0034"],
    "BK-COM-06-0032": ["ALP-COM-06-0035"],
    "BK-COM-06-0033": ["ALP-COM-06-0036", "ALP-COM-06-0038"],
    "BK-COM-06-0034": ["ALP-COM-06-0037"],
    "BK-COM-06-0035": ["ALP-COM-06-0039"],
    "BK-COM-06-0036": ["ALP-COM-06-0040"],
    "BK-COM-06-0037": ["ALP-COM-06-0041"],
    "BK-COM-06-0038": ["ALP-COM-06-0042"],
    "BK-COM-06-0039": ["ALP-COM-06-0043"],
    "BK-COM-06-0040": ["ALP-COM-06-0044"],
}

REQUIRED = {
    "BK-COM-06-0001": ("取得原価＝{{c1::購入代価}}＋使用可能となるまでの{{c1::付随費用}}",),
    "BK-COM-06-0003": ("（借）{{c1::建設仮勘定}}／（貸）現金等",),
    "BK-COM-06-0004": ("（借）建物／（貸）{{c1::建設仮勘定}}",),
    "BK-COM-06-0006": ("割賦価格＝{{c1::現金正価}}＋{{c1::利息}}", "取得原価は{{c1::現金正価}}"),
    "BK-COM-06-0007": ("（貸）{{c1::未払金}}", "（借）{{c1::前払利息}}"),
    "BK-COM-06-0008": ("（借）{{c1::支払利息}}／（貸）{{c1::前払利息}}",),
    "BK-COM-06-0009": ("1回当たり支払利息＝{{c1::前払利息計上額}}÷{{c1::支払回数}}",),
    "BK-COM-06-0010": ("（借）{{c1::前払利息}}／（貸）{{c1::支払利息}}",),
    "BK-COM-06-0012": ("（貸）{{c1::国庫補助金受贈益}}",),
    "BK-COM-06-0013": ("（借）{{c1::固定資産圧縮損}}／（貸）対象固定資産",),
    "BK-COM-06-0016": ("固定資産売却損益＝{{c1::売却代金}}－{{c1::売却時帳簿価額}}", "帳簿価額＝{{c1::取得原価}}－{{c1::減価償却累計額}}"),
    "BK-COM-06-0021": ("（借）{{c1::貯蔵品}}", "固定資産除却損＝{{c1::帳簿価額}}－{{c1::処分可能価額}}"),
    "BK-COM-06-0022": ("固定資産廃棄損＝{{c1::廃棄時帳簿価額}}＋{{c1::廃棄費用}}",),
    "BK-COM-06-0023": ("（借）{{c1::火災損失}}",),
    "BK-COM-06-0024": ("（借）{{c1::未決算}}",),
    "BK-COM-06-0025": ("（借）{{c1::未収入金}}／（貸）{{c1::未決算}}", "{{c1::火災損失}}", "{{c1::保険差益}}"),
    "BK-COM-06-0026": ("（借）{{c1::火災損失}}／（貸）{{c1::仕入}}",),
    "BK-COM-06-0032": ("減価償却費＝（{{c1::取得原価}}－{{c1::残存価額}}）÷{{c1::耐用年数}}",),
    "BK-COM-06-0033": ("1年分の減価償却費×{{c1::使用月数}}÷12", "{{c1::月割}}", "{{c1::1日でも1か月}}"),
    "BK-COM-06-0034": ("減価償却費＝{{c1::期首帳簿価額}}×{{c1::償却率}}", "{{c1::取得原価}}－{{c1::期首減価償却累計額}}"),
    "BK-COM-06-0035": ("減価償却費＝（{{c1::取得原価}}－{{c1::残存価額}}）×{{c1::当期利用量}}÷{{c1::総利用可能量}}",),
    "BK-COM-06-0038": ("償却率＝（1÷{{c1::耐用年数}}）×200%",),
    "BK-COM-06-0039": ("{{c1::償却保証額}}", "{{c1::改定償却額}}"),
    "BK-COM-06-0040": ("償却保証額＝{{c1::取得原価}}×{{c1::保証率}}", "改定償却額＝{{c1::切替時の期首帳簿価額}}×{{c1::改定償却率}}"),
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
        if row["Part"] != "commercial" or row["Chapter"] != "06 有形固定資産":
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
            "chapter::commercial::06",
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
    if len(rows) != 40:
        errors.append(f"expected 40 Notes, got {len(rows)}")
    if len(included) != 44:
        errors.append(f"expected 44 included ALPs, got {len(included)}")
    if len(excluded) != 1:
        errors.append(f"expected 1 decorative exclusion, got {len(excluded)}")
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
        print("COM-06 production validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    multi_alp = sum(1 for row in rows if len(row["ALP_IDs"].split()) > 1)
    journal = sum(1 for row in rows if row["Type"] == "journal_entry")
    formulas = sum(1 for row in rows if row["Type"] == "formula")

    print("COM-06 production validation: PASS")
    print("notes=40 cards=40 cloze_spans=88 included_alps=44 mapped=44 unmapped=0")
    print(f"multi_alp_notes={multi_alp} journal_entry_notes={journal} formula_notes={formulas} decorative_exclusions=1")
    print("account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass formula_atomicity=pass visible_answer_leakage=0 deterministic_order=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
