#!/usr/bin/env python3
"""Validate COM-03 production Notes under the current living recall rules."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "COM-03.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "COM-03.tsv"

FIELDS = ["ID","Text","Extra","SourceRepo","SourceCommit","SourcePath","Part","Chapter","Section","Topic","Type","ALP_IDs","Difficulty","Tags","Status","QA"]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-COM-03-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-COM-03-[0-9]{4}$")
EXPECTED_IDS = [f"BK-COM-03-{n:04d}" for n in range(1,26)]
EXPECTED_SPANS = 66
SOURCE = ("xihangzou/bookkeeping-integrated","569ed7b82e729334e1472286eaca7c4352e6fbdb","merged/textbook.md")
ALLOWED_TYPES = {"definition","classification","comparison","journal_entry","procedure","measurement"}
ALLOWED_REPEAT_ANSWERS = {
    "BK-COM-03-0001": {"通貨代用証券"},
    "BK-COM-03-0003": {"現金過不足","現金"},
    "BK-COM-03-0004": {"現金過不足"},
    "BK-COM-03-0005": {"現金"},
    "BK-COM-03-0009": {"当座預金"},
    "BK-COM-03-0013": {"当座預金","当座借越"},
    "BK-COM-03-0018": {"当座預金"},
    "BK-COM-03-0024": {"小口現金","当座預金"},
}
JOURNAL_IDS = {
    "BK-COM-03-0003","BK-COM-03-0004","BK-COM-03-0005","BK-COM-03-0007",
    "BK-COM-03-0013","BK-COM-03-0018","BK-COM-03-0024",
}
ENTRY_ACCOUNT_RE = re.compile(r"（(?:借|貸)）\{\{c1::([^}]+)\}\}")
FORBIDDEN_COMPACT = ("{{c1::（借）", "{{c1::（貸）", "{{c1::借方：", "{{c1::貸方：")
BROAD_ACTION_ANSWERS = {
    "仕訳を行う",
    "仕訳を行わない",
    "日々の少額支払い",
    "支払内容の報告",
    "費用仕訳",
    "同額補給",
}
REQUIRED = {
    "BK-COM-03-0001": ("{{c1::通貨代用証券}}","{{c1::郵便切手}}"),
    "BK-COM-03-0003": ("（借）{{c1::現金過不足}}／（貸）{{c1::現金}}","（借）{{c1::現金}}／（貸）{{c1::現金過不足}}"),
    "BK-COM-03-0004": ("（借）{{c1::雑損}}／（貸）{{c1::現金過不足}}","（借）{{c1::現金過不足}}／（貸）{{c1::雑益}}"),
    "BK-COM-03-0005": ("{{c1::現金過不足}}を用いず","（借）{{c1::雑損}}／（貸）{{c1::現金}}","（借）{{c1::現金}}／（貸）{{c1::雑益}}"),
    "BK-COM-03-0006": ("現金実査額＝{{c1::通貨}}＋{{c1::通貨代用証券}}",),
    "BK-COM-03-0007": ("（借）{{c1::貯蔵品}}／（貸）{{c1::通信費}}",),
    "BK-COM-03-0009": ("{{c1::現金}}","{{c1::当座預金}}"),
    "BK-COM-03-0013": ("（借）{{c1::当座預金}}／（貸）{{c1::当座借越}}","（借）{{c1::当座借越}}／（貸）{{c1::当座預金}}"),
    "BK-COM-03-0014": ("{{c1::銀行勘定調整表}}",),
    "BK-COM-03-0015": ("{{c1::当社}}側","{{c1::銀行}}側","{{c1::同額}}"),
    "BK-COM-03-0016": ("{{c1::未渡小切手}}","{{c1::未取付小切手}}","{{c1::未取立小切手}}"),
    "BK-COM-03-0017": ("{{c1::当社}}側の修正項目",),
    "BK-COM-03-0018": ("（借）{{c1::当座預金}}／（貸）{{c1::買掛金}}","（借）{{c1::当座預金}}／（貸）{{c1::未払金}}"),
    "BK-COM-03-0019": ("{{c1::加算}}","{{c1::減算}}"),
    "BK-COM-03-0020": ("{{c1::未渡小切手}}","{{c1::未取付小切手}}"),
    "BK-COM-03-0022": ("{{c1::定額資金前渡制度}}",),
    "BK-COM-03-0023": ("支払内容の{{c1::報告}}","同額の{{c1::補給}}"),
    "BK-COM-03-0024": ("（借）{{c1::小口現金}}／（貸）{{c1::当座預金}}",),
    "BK-COM-03-0025": ("補給額＝{{c1::報告済支払合計額}}",),
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

    included = [r["alp_id"] for r in inventory if r.get("status") == "INCLUDE"]
    included_set = set(included)
    excluded = [r for r in inventory if r.get("status") == "EXCLUDE"]
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
        if row["Part"] != "commercial" or row["Chapter"] != "03 現金預金":
            errors.append(f"{nid}: part/chapter mismatch")
        if row["Type"] not in ALLOWED_TYPES:
            errors.append(f"{nid}: invalid type {row['Type']!r}")
        try:
            difficulty = int(row["Difficulty"])
        except ValueError:
            difficulty = 0
        if difficulty not in {1,2,3}:
            errors.append(f"{nid}: invalid difficulty")
        for token in (
            "bookkeeping::commercial", "chapter::commercial::03",
            f"difficulty::{row['Difficulty']}", "status::approved",
            f"topic::{row['Topic']}", f"type::{row['Type']}",
        ):
            if token not in row["Tags"]:
                errors.append(f"{nid}: missing tag {token!r}")

        text = row["Text"]
        matches = CLOZE_RE.findall(text)
        spans += len(matches)
        if not matches or {int(i) for i,_ in matches} != {1}:
            errors.append(f"{nid}: approved Notes must use c1 only")
        answers = [a.strip() for _,a in matches]
        duplicate_answers = {a for a,c in Counter(answers).items() if c > 1}
        unexpected = duplicate_answers - ALLOWED_REPEAT_ANSWERS.get(nid,set())
        if unexpected:
            errors.append(f"{nid}: unexpected repeated answers {sorted(unexpected)}")
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
        if nid in JOURNAL_IDS and not ENTRY_ACCOUNT_RE.search(text):
            errors.append(f"{nid}: missing account-level journal Cloze")

        rendered = CLOZE_RE.sub("[…]", text)
        rendered_texts[rendered] += 1
        alps = row["ALP_IDs"].split()
        if not alps:
            errors.append(f"{nid}: missing ALP mapping")
        else:
            primary_alp_numbers.append(int(alps[0].rsplit("-",1)[1]))
        for alp in alps:
            if not ALP_RE.fullmatch(alp) or alp not in included_set:
                errors.append(f"{nid}: invalid/nonincluded ALP {alp}")
            alp_to_notes[alp].append(nid)

    if ids != EXPECTED_IDS:
        errors.append("stable Note IDs/order mismatch")
    if len(rows) != 25:
        errors.append(f"expected 25 Notes, got {len(rows)}")
    if len(included) != 38:
        errors.append(f"expected 38 included ALPs, got {len(included)}")
    if len(excluded) != 2:
        errors.append(f"expected 2 decorative exclusions, got {len(excluded)}")
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

    if errors:
        print("COM-03 production validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    multi_alp = sum(1 for row in rows if len(row["ALP_IDs"].split()) > 1)
    journal = sum(1 for row in rows if row["Type"] == "journal_entry")
    measurement = sum(1 for row in rows if row["Type"] == "measurement")
    print("COM-03 production validation: PASS")
    print("notes=25 cards=25 cloze_spans=66 included_alps=38 mapped=38 unmapped=0")
    print(f"multi_alp_notes={multi_alp} journal_entry_notes={journal} measurement_notes={measurement} decorative_exclusions=2")
    print("account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass visible_answer_leakage=0 deterministic_order=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
