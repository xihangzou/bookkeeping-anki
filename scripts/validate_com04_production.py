#!/usr/bin/env python3
"""Validate COM-04 production Notes under the current living recall rules."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "COM-04.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "COM-04.tsv"

FIELDS = ["ID","Text","Extra","SourceRepo","SourceCommit","SourcePath","Part","Chapter","Section","Topic","Type","ALP_IDs","Difficulty","Tags","Status","QA"]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-COM-04-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-COM-04-[0-9]{4}$")
EXPECTED_IDS = [f"BK-COM-04-{n:04d}" for n in range(1,30)]
EXPECTED_SPANS = 94
SOURCE = ("xihangzou/bookkeeping-integrated","569ed7b82e729334e1472286eaca7c4352e6fbdb","merged/textbook.md")
ALLOWED_TYPES = {"definition","classification","comparison","journal_entry","formula","measurement","procedure","exception"}
ENTRY_ACCOUNT_RE = re.compile(r"（(?:借|貸)）\{\{c1::([^}]+)\}\}")
FORBIDDEN_COMPACT = ("{{c1::（借）", "{{c1::（貸）", "{{c1::借方：", "{{c1::貸方：")
BROAD_ACTION_ANSWERS = {"仕訳を行う","仕訳を行わない","処理する","計上する","減少させる","増加させる"}
REQUIRED = {
    "BK-COM-04-0002": ("（借）{{c1::立替金}}／（貸）{{c1::現金}}","{{c1::相殺}}"),
    "BK-COM-04-0003": ("（借）{{c1::受取商品券}}／（貸）{{c1::売上}}","（借）{{c1::現金}}／（貸）{{c1::受取商品券}}"),
    "BK-COM-04-0007": ("利息＝{{c1::元金}}×{{c1::年利率}}","{{c1::月数}}/12","{{c1::日数}}/365"),
    "BK-COM-04-0012": ("（借）{{c1::仕入}}／（貸）{{c1::支払手形}}","（借）{{c1::受取手形}}／（貸）{{c1::売上}}"),
    "BK-COM-04-0013": ("（借）{{c1::当座預金}}／（貸）{{c1::受取手形}}","（借）{{c1::支払手形}}／（貸）{{c1::当座預金}}"),
    "BK-COM-04-0014": ("（借）{{c1::受取手形}}／（貸）{{c1::売掛金}}","（借）{{c1::買掛金}}／（貸）{{c1::支払手形}}"),
    "BK-COM-04-0016": ("（借）{{c1::支払手形}}",),
    "BK-COM-04-0017": ("{{c1::手形の割引}}","{{c1::手形売却損}}"),
    "BK-COM-04-0018": ("割引料＝{{c1::手形金額}}×{{c1::割引率}}×{{c1::割引日数}}÷365",),
    "BK-COM-04-0020": ("{{c1::譲渡記録}}","{{c1::分割}}","{{c1::電子記録債権売却損}}"),
    "BK-COM-04-0022": ("（借）{{c1::不渡手形}}／（貸）{{c1::受取手形}}",),
    "BK-COM-04-0024": ("（借）{{c1::不渡手形}}／（貸）{{c1::当座預金}}",),
    "BK-COM-04-0026": ("{{c1::支払利息}}","{{c1::受取利息}}"),
    "BK-COM-04-0027": ("{{c1::営業外受取手形}}","{{c1::営業外支払手形}}"),
    "BK-COM-04-0028": ("{{c1::債務の保証}}","{{c1::偶発債務}}","（借）{{c1::保証債務見返}}／（貸）{{c1::保証債務}}"),
    "BK-COM-04-0029": ("（借）{{c1::保証債務}}／（貸）{{c1::保証債務見返}}","{{c1::未収入金}}","{{c1::立替金}}","{{c1::貸付金}}"),
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
        if (row["SourceRepo"],row["SourceCommit"],row["SourcePath"]) != SOURCE:
            errors.append(f"{nid}: source provenance mismatch")
        if row["Part"] != "commercial" or row["Chapter"] != "04 債権債務":
            errors.append(f"{nid}: part/chapter mismatch")
        if row["Type"] not in ALLOWED_TYPES:
            errors.append(f"{nid}: invalid type {row['Type']!r}")
        try:
            difficulty = int(row["Difficulty"])
        except ValueError:
            difficulty = 0
        if difficulty not in {1,2,3}:
            errors.append(f"{nid}: invalid difficulty")
        expected_tags = sorted([
            "bookkeeping::commercial", "chapter::commercial::04",
            f"difficulty::{row['Difficulty']}", "status::approved",
            f"topic::{row['Topic'].strip().replace(' ', '_')}", f"type::{row['Type']}",
        ])
        if row["Tags"].split() != expected_tags:
            errors.append(f"{nid}: required tags/order mismatch")

        text = row["Text"]
        matches = CLOZE_RE.findall(text)
        spans += len(matches)
        if not matches or {int(i) for i,_ in matches} != {1}:
            errors.append(f"{nid}: approved Notes must use c1 only")
        answers = [a.strip() for _,a in matches]
        visible = CLOZE_RE.sub("", text)
        for answer in answers:
            if len(answer) >= 2 and answer in visible:
                errors.append(f"{nid}: visible answer leakage {answer!r}")
            if answer in BROAD_ACTION_ANSWERS:
                errors.append(f"{nid}: broad/non-atomic Cloze answer {answer!r}")
            if any(x in answer for x in ("（借）","（貸）","／","借方：","貸方：")):
                errors.append(f"{nid}: journal syntax inside Cloze {answer!r}")
        for old in FORBIDDEN_COMPACT:
            if old in text:
                errors.append(f"{nid}: compact whole-entry Cloze retained {old!r}")
        for req in REQUIRED.get(nid,()):
            if req not in text:
                errors.append(f"{nid}: missing required precision form {req!r}")
        if row["Type"] == "journal_entry" and not ENTRY_ACCOUNT_RE.search(text):
            errors.append(f"{nid}: missing account-level journal Cloze")

        rendered = CLOZE_RE.sub("[…]", text)
        rendered_texts[rendered] += 1
        alps = row["ALP_IDs"].split()
        if not alps:
            errors.append(f"{nid}: missing ALP mapping")
        else:
            primary_alp_numbers.append(int(alps[0].rsplit("-",1)[1]))
        alp_nums = [int(a.rsplit("-",1)[1]) for a in alps if ALP_RE.fullmatch(a)]
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
    if len(rows) != 29:
        errors.append(f"expected 29 Notes, got {len(rows)}")
    if len(included) != 41:
        errors.append(f"expected 41 included ALPs, got {len(included)}")
    if len(excluded) != 1:
        errors.append(f"expected 1 decorative exclusion, got {len(excluded)}")
    if spans != EXPECTED_SPANS:
        errors.append(f"expected {EXPECTED_SPANS} Cloze spans, got {spans}")
    if primary_alp_numbers != sorted(primary_alp_numbers):
        errors.append("Note order is not deterministic by primary ALP")
    bad_map = [alp for alp in included if len(alp_to_notes.get(alp,[])) != 1]
    if bad_map:
        errors.append(f"ALPs not mapped exactly once: {bad_map}")
    duplicate_rendered = [t for t,c in rendered_texts.items() if c > 1]
    if duplicate_rendered:
        errors.append(f"duplicate rendered Note text: {len(duplicate_rendered)}")
    for row in inventory:
        if row.get("note_ids") or row.get("qa_status") != "pending":
            errors.append("canonical ANKI-003 inventory must remain unmapped/pending")
            break

    if errors:
        print("COM-04 production validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    multi_alp = sum(1 for row in rows if len(row["ALP_IDs"].split()) > 1)
    journal = sum(1 for row in rows if row["Type"] == "journal_entry")
    formulas = sum(1 for row in rows if row["Type"] == "formula")
    print("COM-04 production validation: PASS")
    print("notes=29 cards=29 cloze_spans=94 included_alps=41 mapped=41 unmapped=0")
    print(f"multi_alp_notes={multi_alp} journal_entry_notes={journal} formula_notes={formulas} decorative_exclusions=1")
    print("account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass visible_answer_leakage=0 deterministic_order=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
