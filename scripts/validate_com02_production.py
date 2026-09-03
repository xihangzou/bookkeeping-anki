#!/usr/bin/env python3
"""Validate COM-02 after ANKI-AUDIT-009 canonical-label audit."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "COM-02.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "COM-02.tsv"

FIELDS = ["ID","Text","Extra","SourceRepo","SourceCommit","SourcePath","Part","Chapter","Section","Topic","Type","ALP_IDs","Difficulty","Tags","Status","QA"]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-COM-02-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-COM-02-[0-9]{4}$")
EXPECTED_IDS = {f"BK-COM-02-{n:04d}" for n in range(1,18)}
EXPECTED_SPANS = 50
SOURCE = ("xihangzou/bookkeeping-integrated","569ed7b82e729334e1472286eaca7c4352e6fbdb","merged/textbook.md")
ALLOWED_REPEAT_ANSWERS = {
    "BK-COM-02-0009": {"仕入"},
    "BK-COM-02-0015": {"現金等","契約負債","仕掛品"},
    "BK-COM-02-0016": {"履行割合"},
}
JOURNAL_IDS = {"BK-COM-02-0002","BK-COM-02-0003","BK-COM-02-0004","BK-COM-02-0005","BK-COM-02-0009"}
ENTRY_ACCOUNT_RE = re.compile(r"（(?:借|貸)）\{\{c1::([^}]+)\}\}")
FORBIDDEN_BROAD = (
    "{{c1::（借）", "{{c1::借方：", "{{c1::果たした時点}}",
    "{{c1::売上を再計上しない}}", "{{c1::仕入を減額する}}",
)
FORBIDDEN_0006 = ("{{c1::出荷時}}", "{{c1::到着時}}", "{{c1::検収時}}")
REQUIRED = {
    "BK-COM-02-0001": ("{{c1::履行義務}}","{{c1::充足した時点}}"),
    "BK-COM-02-0002": ("（借）{{c1::売掛金}}／（貸）{{c1::売上}}",),
    "BK-COM-02-0003": ("（借）{{c1::前受金}}・{{c1::売掛金}}／（貸）{{c1::売上}}",),
    "BK-COM-02-0004": ("（借）{{c1::売上}}／（貸）{{c1::売掛金}}",),
    "BK-COM-02-0005": ("（借）{{c1::発送費}}／（貸）{{c1::現金}}",),
    "BK-COM-02-0006": ("出荷時なら{{c1::出荷基準}}","到着時なら{{c1::着荷基準}}","検収時なら{{c1::検収基準}}"),
    "BK-COM-02-0009": ("（借）{{c1::現金}}／（貸）{{c1::仕入}}","（借）{{c1::買掛金}}／（貸）{{c1::仕入}}"),
    "BK-COM-02-0012": ("{{c1::契約負債}}","{{c1::保証対価}}×{{c1::当期履行期間}}÷{{c1::総保証期間}}"),
    "BK-COM-02-0015": ("（借）{{c1::現金等}}／（貸）{{c1::契約負債}}","（借）{{c1::仕掛品}}／（貸）{{c1::現金等}}","（借）{{c1::契約負債}}／（貸）{{c1::役務収益}}","（借）{{c1::役務原価}}／（貸）{{c1::仕掛品}}"),
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
    alp_to_notes: dict[str, list[str]] = defaultdict(list)
    spans = 0
    ids: set[str] = set()

    for row in rows:
        nid = row["ID"]
        ids.add(nid)
        if not NOTE_RE.fullmatch(nid): errors.append(f"{nid}: invalid ID")
        if row["Status"] != "approved" or row["QA"] != "pass": errors.append(f"{nid}: lifecycle")
        if (row["SourceRepo"],row["SourceCommit"],row["SourcePath"]) != SOURCE: errors.append(f"{nid}: source provenance")
        text = row["Text"]
        matches = CLOZE_RE.findall(text)
        spans += len(matches)
        if {int(i) for i,_ in matches} != {1}: errors.append(f"{nid}: must use c1 only")
        answers = [a.strip() for _,a in matches]
        dup = {a for a,c in Counter(answers).items() if c > 1} - ALLOWED_REPEAT_ANSWERS.get(nid,set())
        if dup: errors.append(f"{nid}: unexpected repeated answers {sorted(dup)}")
        visible = CLOZE_RE.sub("", text)
        for a in answers:
            if len(a) >= 2 and a in visible: errors.append(f"{nid}: visible answer leakage {a!r}")
            if any(x in a for x in ("（借）","（貸）","／","借方：","貸方：")): errors.append(f"{nid}: journal syntax inside Cloze {a!r}")
        for old in FORBIDDEN_BROAD:
            if old in text: errors.append(f"{nid}: superseded broad/compact Cloze {old!r}")
        if nid == "BK-COM-02-0006":
            for old in FORBIDDEN_0006:
                if old in text: errors.append(f"{nid}: timing Cloze retained instead of canonical basis name {old!r}")
        for req in REQUIRED.get(nid,()):
            if req not in text: errors.append(f"{nid}: missing required precision form {req!r}")
        if nid in JOURNAL_IDS:
            if not ENTRY_ACCOUNT_RE.search(text): errors.append(f"{nid}: missing account-level journal Cloze")
        for alp in row["ALP_IDs"].split():
            if not ALP_RE.fullmatch(alp) or alp not in included_set: errors.append(f"{nid}: invalid ALP {alp}")
            alp_to_notes[alp].append(nid)

    if len(rows) != 17 or ids != EXPECTED_IDS: errors.append("stable Note set/count mismatch")
    if len(included) != 32: errors.append("included ALP count mismatch")
    if spans != EXPECTED_SPANS: errors.append(f"expected {EXPECTED_SPANS} Cloze spans, got {spans}")
    bad_map = [a for a in included if len(alp_to_notes.get(a,[])) != 1]
    if bad_map: errors.append(f"ALPs not mapped exactly once: {bad_map}")

    if errors:
        print("COM-02 ANKI-AUDIT-009 validation: FAIL", file=sys.stderr)
        for e in errors: print(f"- {e}", file=sys.stderr)
        return 1
    print("COM-02 ANKI-AUDIT-009 validation: PASS")
    print("notes=17 cards=17 cloze_spans=50 included_alps=32 unmapped=0")
    print("journal_account_level_cloze=pass canonical_label_priority=pass visible_answer_leakage=0")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
