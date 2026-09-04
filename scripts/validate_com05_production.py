#!/usr/bin/env python3
"""Validate COM-05 production Notes under the current living recall rules."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "COM-05.tsv"
INVENTORY = ROOT / "inventory" / "topic_inventory" / "COM-05.tsv"

FIELDS = ["ID","Text","Extra","SourceRepo","SourceCommit","SourcePath","Part","Chapter","Section","Topic","Type","ALP_IDs","Difficulty","Tags","Status","QA"]
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE = re.compile(r"^BK-COM-05-[0-9]{4}$")
ALP_RE = re.compile(r"^ALP-COM-05-[0-9]{4}$")
EXPECTED_IDS = [f"BK-COM-05-{n:04d}" for n in range(1,39)]
EXPECTED_SPANS = 104
SOURCE = ("xihangzou/bookkeeping-integrated","569ed7b82e729334e1472286eaca7c4352e6fbdb","merged/textbook.md")
ALLOWED_TYPES = {"definition","classification","recognition","measurement","journal_entry","formula","procedure","comparison","exception","reasoning","ledger","financial_statement","cost_accounting"}
ENTRY_ACCOUNT_RE = re.compile(r"（(?:借|貸)）\{\{c1::([^}]+)\}\}")
FORBIDDEN_COMPACT = ("{{c1::（借）", "{{c1::（貸）", "{{c1::借方：", "{{c1::貸方：")
BROAD_ACTION_ANSWERS = {"仕訳を行う","仕訳を行わない","処理する","計上する","減少させる","増加させる"}

REQUIRED = {
    "BK-COM-05-0012": ("取得原価＝{{c1::購入代価}}＋{{c1::付随費用}}",),
    "BK-COM-05-0014": ("平均単価＝{{c1::取得原価合計}}÷{{c1::保有株式数合計}}",),
    "BK-COM-05-0015": ("売却原価＝{{c1::売却株式数}}×{{c1::平均単価}}", "売却損益＝{{c1::売却代金}}－上記原価"),
    "BK-COM-05-0016": ("公社債の売買価額＝{{c1::額面金額}}÷100×{{c1::100円当たりの売買単価}}",),
    "BK-COM-05-0019": ("クーポン利息＝{{c1::額面金額}}×{{c1::年利率}}×{{c1::対象月数}}÷12",),
    "BK-COM-05-0021": ("（貸）{{c1::有価証券利息}}", "{{c1::裸相場}}"),
    "BK-COM-05-0022": ("（借）{{c1::有価証券利息}}", "（貸）{{c1::有価証券利息}}"),
    "BK-COM-05-0024": (
        "売買目的有価証券＝{{c1::時価}}・差額は{{c1::当期損益}}",
        "満期保有目的の債券＝{{c1::取得原価}}または{{c1::償却原価}}",
        "子会社株式・関連会社株式＝{{c1::取得原価}}",
        "その他有価証券＝{{c1::時価}}・差額は{{c1::純資産}}",
    ),
    "BK-COM-05-0026": ("有価証券評価益＝{{c1::期末時価}}－{{c1::帳簿価額}}", "有価証券評価損＝{{c1::帳簿価額}}－{{c1::期末時価}}"),
    "BK-COM-05-0029": ("毎期償却額＝（{{c1::額面金額}}－{{c1::取得価額}}）÷{{c1::償還期間}}", "{{c1::月割}}"),
    "BK-COM-05-0030": ("（借）{{c1::満期保有目的の債券}}／（貸）{{c1::有価証券利息}}", "償却原価＝{{c1::決算整理前帳簿価額}}＋{{c1::当期償却額}}"),
    "BK-COM-05-0033": ("（借）{{c1::その他有価証券}}／（貸）{{c1::その他有価証券評価差額金}}", "（借）{{c1::その他有価証券評価差額金}}／（貸）{{c1::その他有価証券}}"),
    "BK-COM-05-0035": ("まず{{c1::償却原価法}}", "その後{{c1::償却原価}}と{{c1::期末時価}}"),
    "BK-COM-05-0036": ("{{c1::洗替方式}}", "{{c1::切放方式}}", "{{c1::取得原価}}", "{{c1::前期末時価}}"),
    "BK-COM-05-0038": ("{{c1::当期損益}}", "{{c1::取得原価}}", "{{c1::洗替方式}}"),
}

EXACT_TEXT = {
    "BK-COM-05-0024": "決算評価は、売買目的有価証券＝{{c1::時価}}・差額は{{c1::当期損益}}、満期保有目的の債券＝{{c1::取得原価}}または{{c1::償却原価}}、子会社株式・関連会社株式＝{{c1::取得原価}}、その他有価証券＝{{c1::時価}}・差額は{{c1::純資産}}とする。",
}

FORBIDDEN_COMPARISON_CELLS = (
    "{{c1::時価・差額は当期損益}}",
    "{{c1::取得原価または償却原価}}",
    "{{c1::時価・差額は純資産}}",
)


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
        if row["Part"] != "commercial" or row["Chapter"] != "05 有価証券":
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
            "chapter::commercial::05",
            f"difficulty::{row['Difficulty']}",
            "status::approved",
            f"topic::{row['Topic'].strip().replace(' ', '_')}",
            f"type::{row['Type']}",
        ])
        if row["Tags"].split() != expected_tags:
            errors.append(f"{nid}: required tags/order mismatch")

        text = row["Text"]
        if nid in EXACT_TEXT and text != EXACT_TEXT[nid]:
            errors.append(f"{nid}: active Text must match reviewed atomized comparison form")
        if nid == "BK-COM-05-0024" and any(old in text for old in FORBIDDEN_COMPARISON_CELLS):
            errors.append(f"{nid}: compound comparison cell retained inside one Cloze")

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
            if any(x in answer for x in ("（借）","（貸）","／","借方：","貸方：")):
                errors.append(f"{nid}: journal syntax inside Cloze {answer!r}")

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
    if len(rows) != 38:
        errors.append(f"expected 38 Notes, got {len(rows)}")
    if len(included) != 48:
        errors.append(f"expected 48 included ALPs, got {len(included)}")
    if len(excluded) != 2:
        errors.append(f"expected 2 decorative exclusions, got {len(excluded)}")
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
        print("COM-05 production validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    multi_alp = sum(1 for row in rows if len(row["ALP_IDs"].split()) > 1)
    journal = sum(1 for row in rows if row["Type"] == "journal_entry")
    formulas = sum(1 for row in rows if row["Type"] == "formula")

    print("COM-05 production validation: PASS")
    print("notes=38 cards=38 cloze_spans=104 included_alps=48 mapped=48 unmapped=0")
    print(f"multi_alp_notes={multi_alp} journal_entry_notes={journal} formula_notes={formulas} decorative_exclusions=2")
    print("account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass parallel_comparison_atomicity=pass visible_answer_leakage=0 deterministic_order=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
