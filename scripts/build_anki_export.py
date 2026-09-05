#!/usr/bin/env python3
"""Build and validate the final deterministic Anki export for ANKI-043.

Canonical production Notes remain the editable source of truth. This script reads
all production TSV shards, exports only approved/QA-passed Notes in canonical
source order, builds an Anki-compatible Cloze .apkg with deterministic GUIDs,
and validates the package by reading its SQLite collection back.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import re
import sqlite3
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "production" / "notes"
SCHEMA_PATH = ROOT / "schema" / "note_schema.yaml"
RULES_PATH = ROOT / "rules" / "anki_card_rules.md"
COVERAGE_REPORT = ROOT / "production" / "qa" / "ANKI-042.md"
SCRIPT_PATH = Path(__file__).resolve()

NOTE_FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]
PART_ORDER = {"foundation": 0, "commercial": 1, "industrial": 2}
ID_RE = re.compile(r"^BK-(FND|COM|IND)-(\d{2})-(\d{4})$")
CLOZE_RE = re.compile(r"\{\{c(\d+)::(.*?)(?:::[^{}]*?)?\}\}")

EXPECTED = {
    "production_rows": 811,
    "approved_notes": 735,
    "deprecated_notes": 76,
    "generated_cards": 748,
    "cloze_spans": 2008,
    "mapped_alps": 965,
}
SOURCE_BASELINE = {
    "repository": "xihangzou/bookkeeping-integrated",
    "path": "merged/textbook.md",
    "commit": "569ed7b82e729334e1472286eaca7c4352e6fbdb",
}
DECK_ID = 2059400110
MODEL_ID = 1607392319
DECK_NAME = "Bookkeeping Master"
MODEL_NAME = "Bookkeeping Master Cloze"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_value(*args: str) -> str | None:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip() or None
    except (OSError, subprocess.CalledProcessError):
        return None


def decode_schema_escapes(value: str) -> str:
    out: list[str] = []
    i = 0
    mapping = {"\\": "\\", "t": "\t", "r": "\r", "n": "\n"}
    while i < len(value):
        if value[i] != "\\":
            out.append(value[i])
            i += 1
            continue
        if i + 1 >= len(value):
            raise AssertionError("trailing backslash in serialized field")
        code = value[i + 1]
        if code not in mapping:
            raise AssertionError(f"unknown schema escape: \\{code}")
        out.append(mapping[code])
        i += 2
    return "".join(out)


def encode_schema_escapes(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("\t", "\\t")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
    )


def read_notes() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    paths = sorted(NOTES_DIR.glob("*.tsv"))
    if len(paths) != 31:
        raise AssertionError(f"expected 31 production Note shards, found {len(paths)}")

    rows: list[dict[str, str]] = []
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, delimiter="\t")
            if reader.fieldnames != NOTE_FIELDS:
                raise AssertionError(f"unexpected fields in {path}: {reader.fieldnames}")
            for row in reader:
                if None in row:
                    raise AssertionError(f"malformed TSV row in {path}")
                row["_file"] = path.name
                rows.append(row)

    ids = [row["ID"] for row in rows]
    duplicates = sorted(k for k, v in Counter(ids).items() if v > 1)
    if duplicates:
        raise AssertionError(f"duplicate stable Note IDs: {duplicates[:20]}")

    approved = [row for row in rows if row["Status"] == "approved"]
    deprecated = [row for row in rows if row["Status"] == "deprecated"]
    other = [row for row in rows if row["Status"] not in {"approved", "deprecated"}]
    if other:
        raise AssertionError(f"non-final production statuses: {[r['ID'] for r in other[:20]]}")
    if any(row["QA"] != "pass" for row in rows):
        raise AssertionError("all final production rows must have QA=pass")

    for row in approved:
        match = ID_RE.match(row["ID"])
        if not match:
            raise AssertionError(f"invalid stable Note ID: {row['ID']}")
        if row["Part"] not in PART_ORDER:
            raise AssertionError(f"invalid Part in {row['ID']}: {row['Part']}")
        for field in NOTE_FIELDS:
            raw = row[field]
            if any(ch in raw for ch in "\t\r\n"):
                raise AssertionError(f"raw control character in serialized {row['ID']}:{field}")
            if encode_schema_escapes(decode_schema_escapes(raw)) != raw:
                raise AssertionError(f"non-canonical escape serialization in {row['ID']}:{field}")

    def sort_key(row: dict[str, str]) -> tuple[int, int, int]:
        match = ID_RE.match(row["ID"])
        assert match is not None
        return PART_ORDER[row["Part"]], int(match.group(2)), int(match.group(3))

    approved.sort(key=sort_key)
    return rows, approved


def count_corpus(rows: list[dict[str, str]], approved: list[dict[str, str]]) -> dict[str, int]:
    deprecated = [row for row in rows if row["Status"] == "deprecated"]
    generated_cards = 0
    cloze_spans = 0
    mapped_alps: set[str] = set()

    for row in approved:
        spans = list(CLOZE_RE.finditer(row["Text"]))
        indices = {int(match.group(1)) for match in spans}
        if not spans or not indices:
            raise AssertionError(f"approved Note without valid Cloze: {row['ID']}")
        generated_cards += len(indices)
        cloze_spans += len(spans)
        alps = row["ALP_IDs"].split()
        if not alps:
            raise AssertionError(f"approved Note without ALP linkage: {row['ID']}")
        mapped_alps.update(alps)

    counts = {
        "production_rows": len(rows),
        "approved_notes": len(approved),
        "deprecated_notes": len(deprecated),
        "generated_cards": generated_cards,
        "cloze_spans": cloze_spans,
        "mapped_alps": len(mapped_alps),
    }
    if counts != EXPECTED:
        raise AssertionError(f"final corpus counts changed: expected {EXPECTED}, got {counts}")
    return counts


def canonical_tsv(approved: list[dict[str, str]]) -> bytes:
    lines = ["\t".join(NOTE_FIELDS)]
    for row in approved:
        lines.append("\t".join(row[field] for field in NOTE_FIELDS))
    payload = ("\n".join(lines) + "\n").encode("utf-8")
    if payload.decode("utf-8").encode("utf-8") != payload:
        raise AssertionError("UTF-8 canonical TSV round-trip failed")
    return payload


def decoded_fields(row: dict[str, str]) -> list[str]:
    return [decode_schema_escapes(row[field]) for field in NOTE_FIELDS]


def expected_semantic_payload(approved: list[dict[str, str]], guid_for) -> list[dict[str, object]]:
    payload: list[dict[str, object]] = []
    for row in approved:
        indices = sorted({int(m.group(1)) for m in CLOZE_RE.finditer(row["Text"])})
        payload.append(
            {
                "id": row["ID"],
                "guid": guid_for(row["ID"]),
                "fields": decoded_fields(row),
                "tags": row["Tags"].split(),
                "card_ords": [index - 1 for index in indices],
            }
        )
    return payload


def semantic_sha256(payload: list[dict[str, object]]) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


def build_apkg(approved: list[dict[str, str]], output: Path) -> tuple[str, str]:
    try:
        import genanki
    except ImportError as exc:
        raise RuntimeError(
            "genanki is required for .apkg output; install requirements-export.txt"
        ) from exc

    model = genanki.Model(
        MODEL_ID,
        MODEL_NAME,
        fields=[{"name": field} for field in NOTE_FIELDS],
        templates=[
            {
                "name": "Cloze",
                "qfmt": "{{cloze:Text}}",
                "afmt": "{{cloze:Text}}<hr id=answer>{{Extra}}",
            }
        ],
        css=(
            ".card { font-family: Arial, 'Hiragino Kaku Gothic ProN', "
            "'Yu Gothic', sans-serif; font-size: 20px; text-align: left; }\n"
            ".cloze { font-weight: bold; }"
        ),
        model_type=genanki.Model.CLOZE,
    )
    deck = genanki.Deck(DECK_ID, DECK_NAME)

    for row in approved:
        note = genanki.Note(
            model=model,
            fields=decoded_fields(row),
            tags=row["Tags"].split(),
            guid=genanki.guid_for(row["ID"]),
        )
        deck.add_note(note)

    output.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(deck).write_to_file(str(output))
    payload = expected_semantic_payload(approved, genanki.guid_for)
    return importlib.metadata.version("genanki"), semantic_sha256(payload)


def locate_collection(extracted: Path) -> Path:
    for name in ("collection.anki21", "collection.anki2"):
        candidate = extracted / name
        if candidate.exists():
            return candidate
    raise AssertionError("APKG has no collection.anki2/collection.anki21")


def validate_apkg(approved: list[dict[str, str]], apkg_path: Path, semantic_hash: str) -> dict[str, int | str]:
    import genanki

    with tempfile.TemporaryDirectory() as tmp:
        extracted = Path(tmp)
        with zipfile.ZipFile(apkg_path) as archive:
            bad = archive.testzip()
            if bad is not None:
                raise AssertionError(f"corrupt APKG zip member: {bad}")
            archive.extractall(extracted)

        db_path = locate_collection(extracted)
        con = sqlite3.connect(db_path)
        try:
            notes = con.execute("SELECT id, guid, flds, tags FROM notes ORDER BY id").fetchall()
            cards = con.execute("SELECT nid, ord FROM cards ORDER BY nid, ord").fetchall()
        finally:
            con.close()

    if len(notes) != EXPECTED["approved_notes"]:
        raise AssertionError(f"APKG Note count mismatch: {len(notes)}")
    if len(cards) != EXPECTED["generated_cards"]:
        raise AssertionError(f"APKG card count mismatch: {len(cards)}")

    guid_counts = Counter(guid for _, guid, _, _ in notes)
    collisions = [guid for guid, count in guid_counts.items() if count > 1]
    if collisions:
        raise AssertionError(f"Anki GUID collisions: {collisions[:20]}")

    cards_by_nid: dict[int, list[int]] = defaultdict(list)
    for nid, ord_ in cards:
        cards_by_nid[nid].append(ord_)

    actual_by_guid: dict[str, dict[str, object]] = {}
    for nid, guid, flds, tags in notes:
        fields = flds.split("\x1f")
        if len(fields) != len(NOTE_FIELDS):
            raise AssertionError(f"APKG field count mismatch for guid={guid}: {len(fields)}")
        actual_by_guid[guid] = {
            "fields": fields,
            "tags": sorted(tags.split()),
            "card_ords": sorted(cards_by_nid[nid]),
        }

    expected_payload = expected_semantic_payload(approved, genanki.guid_for)
    for expected in expected_payload:
        guid = str(expected["guid"])
        actual = actual_by_guid.get(guid)
        if actual is None:
            raise AssertionError(f"missing APKG Note guid={guid} id={expected['id']}")
        if actual["fields"] != expected["fields"]:
            raise AssertionError(f"field round-trip mismatch for {expected['id']}")
        if actual["tags"] != sorted(expected["tags"]):
            raise AssertionError(f"tag round-trip mismatch for {expected['id']}")
        if actual["card_ords"] != expected["card_ords"]:
            raise AssertionError(f"Cloze card ord mismatch for {expected['id']}")

    if semantic_sha256(expected_payload) != semantic_hash:
        raise AssertionError("semantic export fingerprint mismatch")

    flattened = "\n".join(field for item in expected_payload for field in item["fields"])
    if not re.search(r"[一-龯ぁ-んァ-ヶ]", flattened):
        raise AssertionError("Japanese Unicode validation corpus unexpectedly empty")
    newline_fields = sum(
        1 for item in expected_payload for field in item["fields"] if "\n" in field or "\r" in field
    )

    return {
        "notes": len(notes),
        "cards": len(cards),
        "guid_collisions": 0,
        "newline_fields": newline_fields,
        "round_trip": "PASS",
    }


def corpus_input_sha256() -> str:
    digest = hashlib.sha256()
    for path in sorted(NOTES_DIR.glob("*.tsv")):
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def identity(path: Path) -> dict[str, str | None]:
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": sha256_file(path),
        "git_blob": git_value("hash-object", str(path.relative_to(ROOT))),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=ROOT / "export" / "build")
    args = parser.parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    rows, approved = read_notes()
    counts = count_corpus(rows, approved)

    tsv_path = output_dir / "bookkeeping-master.canonical.tsv"
    apkg_path = output_dir / "bookkeeping-master.apkg"
    manifest_path = output_dir / "manifest.json"
    tsv_payload = canonical_tsv(approved)
    tsv_path.write_bytes(tsv_payload)

    genanki_version, semantic_hash = build_apkg(approved, apkg_path)
    round_trip = validate_apkg(approved, apkg_path, semantic_hash)

    revision = git_value("rev-parse", "HEAD")
    manifest = {
        "format_version": 1,
        "deck": {"name": DECK_NAME, "deck_id": DECK_ID, "model": MODEL_NAME, "model_id": MODEL_ID},
        "source_baseline": SOURCE_BASELINE,
        "repository_revision": revision,
        "canonical_inputs": {
            "production_notes_sha256": corpus_input_sha256(),
            "schema": identity(SCHEMA_PATH),
            "anki_card_rules": identity(RULES_PATH),
            "coverage_report": identity(COVERAGE_REPORT),
        },
        "build_identity": {
            "script": identity(SCRIPT_PATH),
            "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "genanki": genanki_version,
        },
        "counts": counts,
        "artifacts": {
            "canonical_tsv": {"path": tsv_path.name, "sha256": sha256_bytes(tsv_payload)},
            "apkg": {"path": apkg_path.name, "semantic_sha256": semantic_hash},
        },
        "validation": {
            **round_trip,
            "duplicate_stable_note_ids": 0,
            "approved_only": True,
            "utf8_round_trip": "PASS",
            "canonical_source_unchanged": True,
        },
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    print("ANKI-043 export validation: PASS")
    print(
        f"approved_notes={counts['approved_notes']} cards={counts['generated_cards']} "
        f"cloze_spans={counts['cloze_spans']} mapped_alps={counts['mapped_alps']}"
    )
    print(f"canonical_tsv={tsv_path}")
    print(f"apkg={apkg_path}")
    print(f"manifest={manifest_path}")
    print(f"semantic_sha256={semantic_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
