#!/usr/bin/env python3
"""Corpus-wide journal-entry QA for ANKI-039.

The audited population is reconstructed from the normalized active corpus as:
1) every approved Note whose primary Type is ``journal_entry``;
2) every approved Note containing explicit debit/credit journal syntax; and
3) every approved Note mapped from an INCLUDE ALP whose canonical type is
   ``journal_entry``.

This makes population selection reproducible and prevents a mistyped Note from
silently escaping the accounting audit.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "production" / "notes"
INVENTORY_DIR = ROOT / "inventory" / "topic_inventory"
SCRIPTS_DIR = ROOT / "scripts"

SOURCE = (
    "xihangzou/bookkeeping-integrated",
    "569ed7b82e729334e1472286eaca7c4352e6fbdb",
    "merged/textbook.md",
)
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
EXPLICIT_JOURNAL_RE = re.compile(r"(?:（借）|（貸）|借方：|貸方：)")
ACCOUNT_AFTER_LABEL_RE = re.compile(
    r"(?:（借）|（貸）|借方：|貸方：)\s*\{\{c([1-9][0-9]*)::([^}]+)\}\}"
)
COMPACT_LABEL_RE = re.compile(
    r"\{\{c[1-9][0-9]*::(?:（借）|（貸）|借方：|貸方：)"
)
COMPACT_TUPLE_RE = re.compile(r"\{\{c[1-9][0-9]*::[^}]*[／/][^}]*\}\}")
PAIR_WITH_AMOUNTS_RE = re.compile(
    r"(?:（借）|借方：)\s*\{\{c[1-9][0-9]*::[^}]+\}\}\s*"
    r"([0-9][0-9,]*円)?\s*[／/]\s*"
    r"(?:（貸）|貸方：)\s*\{\{c[1-9][0-9]*::[^}]+\}\}\s*"
    r"([0-9][0-9,]*円)?"
)
BROAD_ANSWERS = {
    "仕訳を行う", "仕訳を行わない", "処理する", "計上する",
    "増加させる", "減少させる", "あり", "なし",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def amount_value(value: str) -> int:
    return int(value.removesuffix("円").replace(",", ""))


def main() -> int:
    errors: list[str] = []
    all_active: dict[str, dict[str, str]] = {}
    note_batch: dict[str, str] = {}
    alp_to_notes: defaultdict[str, list[str]] = defaultdict(list)

    for path in sorted(NOTES_DIR.glob("*.tsv")):
        batch = path.stem
        for row in read_tsv(path):
            if row.get("Status") != "approved":
                continue
            nid = row["ID"]
            if nid in all_active:
                errors.append(f"duplicate active Note ID: {nid}")
                continue
            all_active[nid] = row
            note_batch[nid] = batch
            for alp in row.get("ALP_IDs", "").split():
                alp_to_notes[alp].append(nid)

    journal_alps: set[str] = set()
    for path in sorted(INVENTORY_DIR.glob("*.tsv")):
        for row in read_tsv(path):
            if row.get("status") == "INCLUDE" and row.get("type") == "journal_entry":
                journal_alps.add(row["alp_id"])

    population: set[str] = set()
    for nid, row in all_active.items():
        if row.get("Type") == "journal_entry" or EXPLICIT_JOURNAL_RE.search(row.get("Text", "")):
            population.add(nid)
    for alp in journal_alps:
        mapped = alp_to_notes.get(alp, [])
        if not mapped:
            errors.append(f"journal-entry ALP is not actively mapped: {alp}")
        population.update(mapped)

    by_batch: Counter[str] = Counter(note_batch[nid] for nid in population)
    amount_pairs_checked = 0
    explicit_notes = 0
    primary_journal_notes = 0
    mapped_journal_alps = set()

    for nid in sorted(population):
        row = all_active[nid]
        text = row.get("Text", "")
        batch = note_batch[nid]

        if (row.get("SourceRepo"), row.get("SourceCommit"), row.get("SourcePath")) != SOURCE:
            errors.append(f"{nid}: source traceability drift")
        if row.get("QA") != "pass":
            errors.append(f"{nid}: QA must be pass")
        if not CLOZE_RE.search(text):
            errors.append(f"{nid}: audited Note has no Cloze target")

        if row.get("Type") == "journal_entry":
            primary_journal_notes += 1
        mapped_journal_alps.update(set(row.get("ALP_IDs", "").split()) & journal_alps)

        if COMPACT_LABEL_RE.search(text):
            errors.append(f"{nid}: debit/credit label is hidden inside a Cloze")
        if COMPACT_TUPLE_RE.search(text):
            errors.append(f"{nid}: whole debit/credit tuple is hidden inside one Cloze")

        for _, answer in CLOZE_RE.findall(text):
            if answer in BROAD_ANSWERS:
                errors.append(f"{nid}: broad/abstract journal Cloze answer {answer!r}")

        explicit = ACCOUNT_AFTER_LABEL_RE.findall(text)
        if EXPLICIT_JOURNAL_RE.search(text):
            explicit_notes += 1
            if not explicit:
                errors.append(f"{nid}: explicit journal syntax lacks account-level Cloze")
        if explicit:
            indices = {idx for idx, _ in explicit}
            if len(indices) != 1:
                errors.append(f"{nid}: journal account targets do not use coherent same-index grouping")
            for _, answer in explicit:
                if any(ch.isdigit() for ch in answer) or "円" in answer:
                    errors.append(f"{nid}: account Cloze improperly bundles a visible amount: {answer!r}")
                if any(token in answer for token in ("（借）", "（貸）", "借方：", "貸方：", "／", "/")):
                    errors.append(f"{nid}: account Cloze is broader than one account: {answer!r}")

        for debit_amount, credit_amount in PAIR_WITH_AMOUNTS_RE.findall(text):
            if debit_amount and credit_amount:
                amount_pairs_checked += 1
                if amount_value(debit_amount) != amount_value(credit_amount):
                    errors.append(
                        f"{nid}: visible simple-entry amounts do not balance: "
                        f"debit={debit_amount} credit={credit_amount}"
                    )

        validator = SCRIPTS_DIR / f"validate_{batch.lower().replace('-', '')}_production.py"
        if not validator.exists():
            errors.append(f"{nid}: missing chapter production validator for {batch}")

    missing_journal_alps = sorted(journal_alps - mapped_journal_alps)
    if missing_journal_alps:
        errors.append(f"journal ALPs missing from audited population: {missing_journal_alps}")

    print("ANKI-039 journal population")
    for batch in sorted(by_batch):
        ids = sorted(nid for nid in population if note_batch[nid] == batch)
        print(f"{batch}: {len(ids)} :: {' '.join(ids)}")
    print(
        f"audited_notes={len(population)} primary_journal_notes={primary_journal_notes} "
        f"journal_alps={len(journal_alps)} mapped_journal_alps={len(mapped_journal_alps)} "
        f"explicit_journal_notes={explicit_notes} amount_pairs_checked={amount_pairs_checked}"
    )

    if errors:
        print(f"defects={len(errors)} unresolved={len(errors)}", file=sys.stderr)
        print("ANKI-039 journal-entry validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("defects=0 unresolved=0")
    print("ANKI-039 journal-entry validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
