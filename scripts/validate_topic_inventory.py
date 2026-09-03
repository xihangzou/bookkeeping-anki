#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "inventory" / "topic_inventory"
STRUCTURE_PATH = ROOT / "inventory" / "structure.md"

COLUMNS = [
    "alp_id",
    "source_part",
    "source_chapter",
    "source_section",
    "source_anchor",
    "summary",
    "type",
    "status",
    "include_reason",
    "exclude_reason",
    "note_ids",
    "qa_status",
]

ALLOWED_TYPES = {
    "definition",
    "classification",
    "recognition",
    "measurement",
    "journal_entry",
    "formula",
    "procedure",
    "comparison",
    "exception",
    "reasoning",
    "ledger",
    "financial_statement",
    "cost_accounting",
}

ALLOWED_EXCLUSION_REASONS = {
    "DUPLICATE_EXACT",
    "DUPLICATE_SEMANTIC",
    "PARAPHRASE_ONLY",
    "RHETORICAL_CONTEXT",
    "DECORATIVE_EXAMPLE",
    "DERIVABLE_TRIVIAL",
    "OUTSIDE_RECALL_GOAL",
}

EXPECTED_SHARDS = ["FND-00.tsv"] + [f"COM-{i:02d}.tsv" for i in range(1, 17)] + [
    f"IND-{i:02d}.tsv" for i in range(1, 15)
]

ID_RE = re.compile(r"^ALP-(FND-00|COM-\d{2}|IND-\d{2})-\d{4}$")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def count_structure_sections() -> tuple[int, int, int]:
    chapter_files = 0
    h2_sections = 0
    h3_sections = 0

    for line in STRUCTURE_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("#### `") and ".md`" in line:
            chapter_files += 1
        if not line.startswith("- H2 "):
            continue

        h2_sections += 1
        if "→ H3 " in line:
            h3_list = line.split("→ H3 ", 1)[1]
            h3_sections += sum(1 for item in h3_list.split(";") if item.strip())

    return chapter_files, h2_sections, h3_sections


def main() -> int:
    errors: list[str] = []
    ids: set[str] = set()
    included = 0
    excluded = 0
    by_type: Counter[str] = Counter()
    by_reason: Counter[str] = Counter()
    rows_total = 0

    if not DATA_DIR.exists():
        print(f"ERROR: missing data directory: {DATA_DIR}", file=sys.stderr)
        return 1
    if not STRUCTURE_PATH.exists():
        print(f"ERROR: missing frozen structure inventory: {STRUCTURE_PATH}", file=sys.stderr)
        return 1

    chapter_files, h2_sections, h3_sections = count_structure_sections()

    actual_shards = sorted(p.name for p in DATA_DIR.glob("*.tsv"))
    missing = sorted(set(EXPECTED_SHARDS) - set(actual_shards))
    unexpected = sorted(set(actual_shards) - set(EXPECTED_SHARDS))
    if missing:
        fail(errors, f"missing shards: {', '.join(missing)}")
    if unexpected:
        fail(errors, f"unexpected shards: {', '.join(unexpected)}")
    if chapter_files != len(EXPECTED_SHARDS):
        fail(errors, f"frozen structure chapter-file count {chapter_files} does not match expected shard count {len(EXPECTED_SHARDS)}")

    for shard_name in EXPECTED_SHARDS:
        path = DATA_DIR / shard_name
        if not path.exists():
            continue

        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, delimiter="\t")
            if reader.fieldnames != COLUMNS:
                fail(errors, f"{shard_name}: header mismatch: {reader.fieldnames}")
                continue

            shard_rows = 0
            for line_no, row in enumerate(reader, start=2):
                shard_rows += 1
                rows_total += 1
                loc = f"{shard_name}:{line_no}"
                status = row["status"].strip()

                for key in ("source_part", "source_chapter", "source_section", "source_anchor", "summary", "qa_status"):
                    if not row[key].strip():
                        fail(errors, f"{loc}: required field {key} is empty")

                if row["qa_status"].strip() != "pending":
                    fail(errors, f"{loc}: ANKI-003 qa_status must be pending")

                if row["note_ids"].strip():
                    fail(errors, f"{loc}: note_ids must remain empty at ANKI-003 stage")

                if status == "INCLUDE":
                    included += 1
                    alp_id = row["alp_id"].strip()
                    alp_type = row["type"].strip()
                    if not ID_RE.match(alp_id):
                        fail(errors, f"{loc}: invalid ALP ID {alp_id!r}")
                    elif alp_id in ids:
                        fail(errors, f"{loc}: duplicate ALP ID {alp_id}")
                    else:
                        ids.add(alp_id)
                    if alp_type not in ALLOWED_TYPES:
                        fail(errors, f"{loc}: invalid type {alp_type!r}")
                    else:
                        by_type[alp_type] += 1
                    if not row["include_reason"].strip():
                        fail(errors, f"{loc}: included row missing include_reason")
                    if row["exclude_reason"].strip():
                        fail(errors, f"{loc}: included row has exclude_reason")

                    expected_prefix = f"ALP-{shard_name[:-4]}-"
                    if alp_id and not alp_id.startswith(expected_prefix):
                        fail(errors, f"{loc}: ID {alp_id} does not match shard {shard_name}")

                elif status == "EXCLUDE":
                    excluded += 1
                    reason = row["exclude_reason"].strip()
                    if row["alp_id"].strip():
                        fail(errors, f"{loc}: excluded row must not have alp_id")
                    if row["type"].strip():
                        fail(errors, f"{loc}: excluded row must not have primary type")
                    if row["include_reason"].strip():
                        fail(errors, f"{loc}: excluded row must not have include_reason")
                    if reason not in ALLOWED_EXCLUSION_REASONS:
                        fail(errors, f"{loc}: invalid exclusion reason {reason!r}")
                    else:
                        by_reason[reason] += 1
                else:
                    fail(errors, f"{loc}: status must be INCLUDE or EXCLUDE, got {status!r}")

            if shard_rows == 0:
                fail(errors, f"{shard_name}: shard contains no candidate rows")

    print(f"source_chapter_files={chapter_files}")
    print(f"source_h2_sections={h2_sections}")
    print(f"source_h3_sections={h3_sections}")
    print(f"source_sections_reviewed={h2_sections + h3_sections}")
    print(f"shards_expected={len(EXPECTED_SHARDS)}")
    print(f"shards_present={len(set(actual_shards) & set(EXPECTED_SHARDS))}")
    print(f"candidate_rows={rows_total}")
    print(f"included_alps={included}")
    print(f"excluded_candidates={excluded}")
    print("included_by_type=" + ",".join(f"{k}:{v}" for k, v in sorted(by_type.items())))
    print("excluded_by_reason=" + ",".join(f"{k}:{v}" for k, v in sorted(by_reason.items())))

    if errors:
        print("VALIDATION: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
