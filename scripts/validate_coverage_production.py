#!/usr/bin/env python3
"""Final source -> candidate -> ALP -> approved Note coverage gate for ANKI-042."""

from __future__ import annotations

import csv
import hashlib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "inventory" / "structure.md"
INVENTORY_DIR = ROOT / "inventory" / "topic_inventory"
NOTES_DIR = ROOT / "production" / "notes"
RULES = ROOT / "rules" / "anki_card_rules.md"
SCHEMA = ROOT / "schema" / "note_schema.yaml"

SOURCE_REPO = "xihangzou/bookkeeping-integrated"
SOURCE_COMMIT = "569ed7b82e729334e1472286eaca7c4352e6fbdb"
SOURCE_PATH = "merged/textbook.md"

EXPECTED_SHARDS = ["FND-00.tsv"] + [f"COM-{i:02d}.tsv" for i in range(1, 17)] + [
    f"IND-{i:02d}.tsv" for i in range(1, 15)
]
EXPECTED_CHAPTER_FILES = 31
EXPECTED_H2 = 110
EXPECTED_H3 = 387
EXPECTED_SECTIONS = 497
EXPECTED_CANDIDATES = 1004
EXPECTED_INCLUDED = 965
EXPECTED_EXCLUDED = 39
EXPECTED_EXCLUSION_REASONS = Counter({"DECORATIVE_EXAMPLE": 38, "DUPLICATE_EXACT": 1})
EXPECTED_PRODUCTION_ROWS = 811
EXPECTED_APPROVED = 735
EXPECTED_DEPRECATED = 76
EXPECTED_CARDS = 748
EXPECTED_CLOZE_SPANS = 2008

INVENTORY_FIELDS = [
    "alp_id", "source_part", "source_chapter", "source_section", "source_anchor",
    "summary", "type", "status", "include_reason", "exclude_reason", "note_ids", "qa_status",
]
NOTE_FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]
ALLOWED_EXCLUSION_REASONS = {
    "DUPLICATE_EXACT", "DUPLICATE_SEMANTIC", "PARAPHRASE_ONLY",
    "RHETORICAL_CONTEXT", "DECORATIVE_EXAMPLE", "DERIVABLE_TRIVIAL",
    "OUTSIDE_RECALL_GOAL",
}
ALP_RE = re.compile(r"^ALP-(FND-00|COM-\d{2}|IND-\d{2})-\d{4}$")
NOTE_RE = re.compile(r"^BK-(FND-00|COM-\d{2}|IND-\d{2})-\d{4}$")
CLOZE_RE = re.compile(r"\{\{c(\d+)::(.*?)(?:::[^{}]*?)?\}\}")
SPACE_RE = re.compile(r"\s+")


def read_tsv(path: Path, expected_fields: list[str]) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if reader.fieldnames != expected_fields:
            raise AssertionError(f"unexpected TSV header in {path}: {reader.fieldnames}")
        return list(reader)


def structure_counts() -> tuple[int, int, int, set[str]]:
    chapter_files = 0
    h2 = 0
    h3 = 0
    paths: set[str] = set()
    for line in STRUCTURE.read_text(encoding="utf-8").splitlines():
        if line.startswith("#### `") and ".md`" in line:
            chapter_files += 1
            paths.add(line.split("`", 2)[1])
        if line.startswith("- H2 "):
            h2 += 1
            if "→ H3 " in line:
                h3_list = line.split("→ H3 ", 1)[1]
                h3 += sum(1 for item in h3_list.split(";") if item.strip())
    return chapter_files, h2, h3, paths


def visible_plain(text: str) -> str:
    return SPACE_RE.sub(" ", CLOZE_RE.sub(lambda m: m.group(2), text)).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []

    for path in (STRUCTURE, INVENTORY_DIR, NOTES_DIR, RULES, SCHEMA):
        if not path.exists():
            fail(errors, f"missing authoritative input: {path.relative_to(ROOT)}")
    if errors:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    chapter_files, h2, h3, structure_paths = structure_counts()
    if (chapter_files, h2, h3, h2 + h3) != (
        EXPECTED_CHAPTER_FILES, EXPECTED_H2, EXPECTED_H3, EXPECTED_SECTIONS
    ):
        fail(errors, f"source structure count drift: chapters={chapter_files} h2={h2} h3={h3} sections={h2+h3}")

    actual_inventory = sorted(p.name for p in INVENTORY_DIR.glob("*.tsv"))
    actual_notes = sorted(p.name for p in NOTES_DIR.glob("*.tsv"))
    if actual_inventory != sorted(EXPECTED_SHARDS):
        fail(errors, "canonical inventory shard set differs from expected 31-batch corpus")
    if actual_notes != sorted(EXPECTED_SHARDS):
        fail(errors, "production Note shard set differs from expected 31-batch corpus")

    included: dict[str, dict[str, str]] = {}
    excluded: list[dict[str, str]] = []
    candidate_rows = 0
    exclusion_reasons: Counter[str] = Counter()
    candidate_chapters: set[str] = set()
    candidate_sections: set[tuple[str, str]] = set()
    unexplained_exclusions: list[str] = []

    for shard_name in EXPECTED_SHARDS:
        path = INVENTORY_DIR / shard_name
        rows = read_tsv(path, INVENTORY_FIELDS)
        if not rows:
            fail(errors, f"{shard_name}: empty candidate inventory shard")
            continue
        for line_no, row in enumerate(rows, start=2):
            candidate_rows += 1
            loc = f"{shard_name}:{line_no}"
            anchor = row["source_anchor"].strip()
            section = row["source_section"].strip()
            anchor_path = anchor.split("::", 1)[0] if "::" in anchor else ""
            if not anchor or not section or not row["summary"].strip():
                fail(errors, f"{loc}: missing source anchor/section/summary")
            if anchor_path not in structure_paths:
                fail(errors, f"{loc}: source anchor chapter not present in pinned structure: {anchor!r}")
            candidate_chapters.add(anchor_path)
            candidate_sections.add((anchor, section))

            status = row["status"].strip()
            if status == "INCLUDE":
                alp = row["alp_id"].strip()
                if not ALP_RE.fullmatch(alp):
                    fail(errors, f"{loc}: invalid included ALP ID {alp!r}")
                if alp in included:
                    fail(errors, f"{loc}: duplicate included ALP ID {alp}")
                included[alp] = row
                if not row["include_reason"].strip() or row["exclude_reason"].strip():
                    fail(errors, f"{loc}: INCLUDE decision lacks canonical include-only rationale")
            elif status == "EXCLUDE":
                excluded.append(row)
                reason = row["exclude_reason"].strip()
                if not reason:
                    unexplained_exclusions.append(loc)
                elif reason not in ALLOWED_EXCLUSION_REASONS:
                    fail(errors, f"{loc}: exclusion reason is not allowed by consolidated rules: {reason}")
                else:
                    exclusion_reasons[reason] += 1
                if row["alp_id"].strip() or row["include_reason"].strip():
                    fail(errors, f"{loc}: EXCLUDE decision must not carry ALP/include_reason")
            else:
                fail(errors, f"{loc}: candidate lacks INCLUDE/EXCLUDE decision")

    if candidate_rows != EXPECTED_CANDIDATES:
        fail(errors, f"candidate proposition count drift: {candidate_rows} != {EXPECTED_CANDIDATES}")
    if len(included) != EXPECTED_INCLUDED:
        fail(errors, f"included ALP count drift: {len(included)} != {EXPECTED_INCLUDED}")
    if len(excluded) != EXPECTED_EXCLUDED:
        fail(errors, f"excluded candidate count drift: {len(excluded)} != {EXPECTED_EXCLUDED}")
    if exclusion_reasons != EXPECTED_EXCLUSION_REASONS:
        fail(errors, f"canonical exclusion distribution drift: {dict(exclusion_reasons)}")
    if unexplained_exclusions:
        fail(errors, f"unexplained exclusions: {unexplained_exclusions[:20]}")
    if candidate_chapters != structure_paths:
        missing = sorted(structure_paths - candidate_chapters)
        extra = sorted(candidate_chapters - structure_paths)
        fail(errors, f"source chapter representation mismatch: missing={missing} extra={extra}")
    if len(candidate_sections) != EXPECTED_SECTIONS:
        fail(errors, f"canonical source-section representation drift: {len(candidate_sections)} != {EXPECTED_SECTIONS}")

    rules_text = RULES.read_text(encoding="utf-8")
    for reason in exclusion_reasons:
        if f"`{reason}`" not in rules_text:
            fail(errors, f"used exclusion reason is absent from consolidated rules: {reason}")

    all_notes: list[dict[str, str]] = []
    for shard_name in EXPECTED_SHARDS:
        rows = read_tsv(NOTES_DIR / shard_name, NOTE_FIELDS)
        for row in rows:
            row["_shard"] = shard_name
        all_notes.extend(rows)

    note_ids = [row["ID"] for row in all_notes]
    duplicates = sorted(k for k, v in Counter(note_ids).items() if v > 1)
    if duplicates:
        fail(errors, f"duplicate stable Note IDs: {duplicates[:20]}")
    invalid_ids = [nid for nid in note_ids if not NOTE_RE.fullmatch(nid)]
    if invalid_ids:
        fail(errors, f"invalid stable Note IDs: {invalid_ids[:20]}")

    approved = [row for row in all_notes if row["Status"] == "approved"]
    deprecated = [row for row in all_notes if row["Status"] == "deprecated"]
    other = [row for row in all_notes if row["Status"] not in {"approved", "deprecated"}]
    if len(all_notes) != EXPECTED_PRODUCTION_ROWS:
        fail(errors, f"production row count drift: {len(all_notes)} != {EXPECTED_PRODUCTION_ROWS}")
    if len(approved) != EXPECTED_APPROVED:
        fail(errors, f"approved Note count drift: {len(approved)} != {EXPECTED_APPROVED}")
    if len(deprecated) != EXPECTED_DEPRECATED:
        fail(errors, f"deprecated lineage Note count drift: {len(deprecated)} != {EXPECTED_DEPRECATED}")
    if other:
        fail(errors, f"non-final production lifecycle statuses: {[r['ID'] for r in other[:20]]}")

    provenance_defects = [
        row["ID"] for row in all_notes
        if row["SourceRepo"] != SOURCE_REPO
        or row["SourceCommit"] != SOURCE_COMMIT
        or row["SourcePath"] != SOURCE_PATH
    ]
    if provenance_defects:
        fail(errors, f"source provenance drift: {provenance_defects[:20]}")
    bad_qa = [row["ID"] for row in all_notes if row["QA"] != "pass"]
    if bad_qa:
        fail(errors, f"production rows without QA=pass: {bad_qa[:20]}")

    active_map: dict[str, list[str]] = defaultdict(list)
    orphan_note_refs: list[tuple[str, str]] = []
    orphan_notes: list[str] = []
    for row in approved:
        alps = row["ALP_IDs"].split()
        if not alps:
            orphan_notes.append(row["ID"])
            continue
        valid = 0
        for alp in alps:
            if alp not in included:
                orphan_note_refs.append((row["ID"], alp))
            else:
                valid += 1
                active_map[alp].append(row["ID"])
        if valid == 0:
            orphan_notes.append(row["ID"])

    orphan_alps = sorted(alp for alp in included if not active_map.get(alp))
    multiply_mapped = sorted((alp, ids) for alp, ids in active_map.items() if len(ids) != 1)
    if orphan_note_refs:
        fail(errors, f"approved Notes reference non-INCLUDE ALPs: {orphan_note_refs[:20]}")
    if orphan_notes:
        fail(errors, f"orphan approved Notes: {orphan_notes[:20]}")
    if orphan_alps:
        fail(errors, f"orphan included ALPs: {orphan_alps[:20]}")
    if multiply_mapped:
        fail(errors, f"included ALPs not normalized to exactly one active Note: {multiply_mapped[:20]}")

    by_plain: dict[str, list[str]] = defaultdict(list)
    cards = 0
    cloze_spans = 0
    for row in approved:
        by_plain[visible_plain(row["Text"])].append(row["ID"])
        spans = list(CLOZE_RE.finditer(row["Text"]))
        indices = {m.group(1) for m in spans}
        if not spans or not indices:
            fail(errors, f"approved Note has no valid Cloze retrieval unit: {row['ID']}")
        cards += len(indices)
        cloze_spans += len(spans)
    exact_duplicates = [ids for ids in by_plain.values() if len(ids) > 1]
    if exact_duplicates:
        fail(errors, f"exact duplicate active retrieval propositions: {exact_duplicates[:20]}")
    if cards != EXPECTED_CARDS:
        fail(errors, f"active card count drift: {cards} != {EXPECTED_CARDS}")
    if cloze_spans != EXPECTED_CLOZE_SPANS:
        fail(errors, f"active Cloze span count drift: {cloze_spans} != {EXPECTED_CLOZE_SPANS}")

    decision_coverage = 100.0 * (len(included) + len(excluded)) / candidate_rows if candidate_rows else 0.0
    semantic_coverage = 100.0 * (len(included) - len(orphan_alps)) / len(included) if included else 0.0
    active_mapped_alps = sum(1 for alp in included if active_map.get(alp))

    print("ANKI-042 final semantic coverage validation")
    print(f"source_repo={SOURCE_REPO}")
    print(f"source_commit={SOURCE_COMMIT}")
    print(f"source_path={SOURCE_PATH}")
    print(f"source_chapter_files={chapter_files}")
    print(f"source_h2_sections={h2}")
    print(f"source_h3_sections={h3}")
    print(f"source_sections_reviewed={h2+h3}")
    print(f"represented_source_sections={len(candidate_sections)}")
    print(f"candidate_propositions={candidate_rows}")
    print(f"included_alps={len(included)}")
    print(f"excluded_candidates={len(excluded)}")
    print("excluded_by_reason=" + ",".join(f"{k}:{v}" for k, v in sorted(exclusion_reasons.items())))
    print(f"production_rows={len(all_notes)}")
    print(f"approved_notes={len(approved)}")
    print(f"deprecated_notes={len(deprecated)}")
    print(f"approved_cards={cards}")
    print(f"approved_cloze_spans={cloze_spans}")
    print(f"mapped_included_alps={active_mapped_alps}")
    print(f"unmapped_included_alps={len(orphan_alps)}")
    print(f"orphan_notes={len(orphan_notes)}")
    print(f"unexplained_exclusions={len(unexplained_exclusions)}")
    print(f"exact_duplicate_active_propositions={len(exact_duplicates)}")
    print(f"decision_coverage_pct={decision_coverage:.2f}")
    print(f"semantic_coverage_pct={semantic_coverage:.2f}")
    print(f"rules_sha256={sha256(RULES)}")
    print(f"schema_sha256={sha256(SCHEMA)}")

    if errors:
        print("ANKI-042 final semantic coverage validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("ANKI-042 final semantic coverage validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
