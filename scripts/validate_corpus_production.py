#!/usr/bin/env python3
"""Corpus-wide normalization validation for ANKI-038.

Checks the canonical production corpus across foundation, commercial, and
industrial batches without mutating stable IDs or the canonical ALP inventory.
The validator is intentionally deterministic and reports cross-batch semantic
similarity candidates for human review while treating exact duplicate retrieval
propositions and mapping/orphan defects as blockers.
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

NOTE_FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]
CLOZE_RE = re.compile(r"\{\{c(\d+)::(.*?)(?:::[^{}]*?)?\}\}")
SPACE_RE = re.compile(r"\s+")
PUNCT_RE = re.compile(r"[\s\u3000、。，．・：:；;（）()［］\[\]「」『』【】/／→←=＝+＋\-－×÷・]|")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)
        if path.parent == NOTES_DIR and reader.fieldnames != NOTE_FIELDS:
            raise AssertionError(f"unexpected note schema fields in {path}: {reader.fieldnames}")
        return rows


def visible_plain(text: str) -> str:
    # Reconstruct the proposition with answers visible and Cloze syntax removed.
    text = CLOZE_RE.sub(lambda m: m.group(2), text)
    return SPACE_RE.sub(" ", text).strip()


def compact_semantic(text: str) -> str:
    text = visible_plain(text)
    # Keep Japanese/Latin/accounting symbols content while removing layout noise.
    return re.sub(r"[^0-9A-Za-z一-龯ぁ-んァ-ヶ々〆ヶ]", "", text).lower()


def bigrams(text: str) -> set[str]:
    if len(text) < 2:
        return {text} if text else set()
    return {text[i : i + 2] for i in range(len(text) - 1)}


def similarity(a: str, b: str) -> float:
    aa, bb = bigrams(a), bigrams(b)
    if not aa or not bb:
        return 0.0
    return len(aa & bb) / len(aa | bb)


def batch_of(note_id: str) -> str:
    m = re.match(r"BK-(FND|COM|IND)-(\d{2})-", note_id)
    if not m:
        return "UNKNOWN"
    return f"{m.group(1)}-{m.group(2)}"


def main() -> int:
    note_paths = sorted(NOTES_DIR.glob("*.tsv"))
    inventory_paths = sorted(INVENTORY_DIR.glob("*.tsv"))
    if len(note_paths) != 31:
        raise AssertionError(f"expected 31 production batches, found {len(note_paths)}")
    if len(inventory_paths) != 31:
        raise AssertionError(f"expected 31 inventory shards, found {len(inventory_paths)}")

    all_notes: list[dict[str, str]] = []
    for path in note_paths:
        rows = read_tsv(path)
        for row in rows:
            row["_file"] = path.name
        all_notes.extend(rows)

    included_alps: dict[str, dict[str, str]] = {}
    excluded_candidates = 0
    for path in inventory_paths:
        for row in read_tsv(path):
            if row["status"] == "INCLUDE":
                alp = row["alp_id"]
                if alp in included_alps:
                    raise AssertionError(f"duplicate canonical ALP ID: {alp}")
                included_alps[alp] = row
            elif row["status"] == "EXCLUDE":
                excluded_candidates += 1
            else:
                raise AssertionError(f"invalid inventory status in {path}: {row['status']}")

    errors: list[str] = []
    ids = [r["ID"] for r in all_notes]
    duplicate_ids = sorted(k for k, v in Counter(ids).items() if v > 1)
    if duplicate_ids:
        errors.append(f"duplicate stable Note IDs: {duplicate_ids}")

    approved = [r for r in all_notes if r["Status"] == "approved"]
    deprecated = [r for r in all_notes if r["Status"] == "deprecated"]
    other_status = [r for r in all_notes if r["Status"] not in {"approved", "deprecated"}]
    if other_status:
        errors.append(
            "non-final production lifecycle rows: "
            + ", ".join(f"{r['ID']}={r['Status']}" for r in other_status[:20])
        )

    bad_qa = [r["ID"] for r in all_notes if r["QA"] != "pass"]
    if bad_qa:
        errors.append(f"production rows without QA=pass: {bad_qa[:20]}")

    active_map: dict[str, list[str]] = defaultdict(list)
    orphan_note_refs: list[tuple[str, str]] = []
    empty_active_mappings: list[str] = []
    for row in approved:
        alps = row["ALP_IDs"].split()
        if not alps:
            empty_active_mappings.append(row["ID"])
        for alp in alps:
            if alp not in included_alps:
                orphan_note_refs.append((row["ID"], alp))
            active_map[alp].append(row["ID"])

    if empty_active_mappings:
        errors.append(f"approved Notes without ALP mapping: {empty_active_mappings}")
    if orphan_note_refs:
        errors.append(f"approved Notes referencing non-INCLUDE ALPs: {orphan_note_refs[:20]}")

    orphan_alps = sorted(alp for alp in included_alps if not active_map.get(alp))
    multiply_mapped = sorted((alp, active_map[alp]) for alp in included_alps if len(active_map.get(alp, [])) > 1)
    if orphan_alps:
        errors.append(f"orphan included ALPs: {orphan_alps[:50]}")
    if multiply_mapped:
        errors.append(f"multiply mapped active ALPs require explicit normalization: {multiply_mapped[:30]}")

    # Exact duplicate proposition check across active retrieval units. Using plain
    # visible proposition catches duplicates even if Cloze numbering/boundaries differ.
    by_plain: dict[str, list[str]] = defaultdict(list)
    for row in approved:
        by_plain[visible_plain(row["Text"])].append(row["ID"])
    exact_duplicate_groups = [ids for ids in by_plain.values() if len(ids) > 1]
    if exact_duplicate_groups:
        errors.append(f"exact duplicate active retrieval propositions: {exact_duplicate_groups[:30]}")

    generated_cards = 0
    cloze_spans = 0
    malformed_cloze: list[str] = []
    for row in approved:
        groups = set(CLOZE_RE.findall(row["Text"]))
        # findall returns tuples; first item is cN index.
        indices = {g[0] for g in groups}
        spans = list(CLOZE_RE.finditer(row["Text"]))
        if not indices or not spans:
            malformed_cloze.append(row["ID"])
        generated_cards += len(indices)
        cloze_spans += len(spans)
    if malformed_cloze:
        errors.append(f"approved Notes without valid Cloze spans: {malformed_cloze}")

    # Human-review candidate set: cross-batch active pairs with substantial textual
    # similarity. Informational only; ANKI-038 report records merge/retain decisions.
    semantic_rows = []
    compact_cache = {r["ID"]: compact_semantic(r["Text"]) for r in approved}
    for i, left in enumerate(approved):
        a = compact_cache[left["ID"]]
        if len(a) < 18:
            continue
        for right in approved[i + 1 :]:
            if batch_of(left["ID"]) == batch_of(right["ID"]):
                continue
            b = compact_cache[right["ID"]]
            if len(b) < 18:
                continue
            # Cheap length filter before bigram Jaccard.
            ratio = min(len(a), len(b)) / max(len(a), len(b))
            if ratio < 0.55:
                continue
            score = similarity(a, b)
            if score >= 0.50:
                semantic_rows.append((score, left["ID"], right["ID"], left["Topic"], right["Topic"]))
    semantic_rows.sort(reverse=True)

    deprecated_lineage_hints = sum(
        1
        for r in deprecated
        if re.search(r"統合|移行|退役|deprecated|ALPは|source traceability|履歴|replacement", r["Extra"], re.I)
    )

    print("ANKI-038 corpus normalization validation")
    print(f"batches={len(note_paths)} production_rows={len(all_notes)} approved_notes={len(approved)} deprecated_notes={len(deprecated)}")
    print(f"approved_cards={generated_cards} approved_cloze_spans={cloze_spans}")
    print(f"included_alps={len(included_alps)} excluded_candidates={excluded_candidates} active_mapped_alps={len(active_map)}")
    print(f"orphan_alps={len(orphan_alps)} orphan_note_refs={len(orphan_note_refs)} multiply_mapped_alps={len(multiply_mapped)}")
    print(f"duplicate_note_ids={len(duplicate_ids)} exact_duplicate_active_propositions={len(exact_duplicate_groups)}")
    print(f"deprecated_lineage_hints={deprecated_lineage_hints}/{len(deprecated)}")
    print(f"semantic_similarity_candidates_ge_0.50={len(semantic_rows)}")
    for score, left, right, ltopic, rtopic in semantic_rows[:50]:
        print(f"SEMANTIC_CANDIDATE {score:.3f} {left} [{ltopic}] <> {right} [{rtopic}]")

    if errors:
        print("ANKI-038 corpus normalization validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("ANKI-038 corpus normalization validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
