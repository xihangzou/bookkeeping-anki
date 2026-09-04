#!/usr/bin/env python3
"""Validate living-spec governance and the consolidated Anki-card rule authority."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CURRENT_AUTHORITY_FILES = [
    "README.md",
    "SPEC.md",
    "GOVERNANCE.md",
    "rules/anki_card_rules.md",
    "schema/note_schema.yaml",
    "production/README.md",
]

LEGACY_RULE_POINTERS = [
    "rules/cloze_rules.md",
    "rules/coverage_rules.md",
    "rules/exam_yield_rules.md",
    "rules/recall_precision_rules.md",
]

BANNED_ACTIVE_AUTHORITY = [
    "post-freeze",
    "frozen v1.0 contract",
    "v1.0 frozen contract",
    "Status: **v1.0 — frozen",
    "frozen_after_representative_pilot",
    "frozen: true",
    "frozen v1.0 source/schema",
    "source/schema/stable-ID baseline remains frozen",
    "must use this frozen v1.0",
]


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        raise FileNotFoundError(rel)
    return path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []

    for rel in CURRENT_AUTHORITY_FILES:
        try:
            text = read(rel)
        except FileNotFoundError:
            errors.append(f"missing current-authority file: {rel}")
            continue
        lower = text.lower()
        for phrase in BANNED_ACTIVE_AUTHORITY:
            if phrase.lower() in lower:
                errors.append(f"{rel}: obsolete freeze-authority phrase remains: {phrase!r}")

    required = {
        "GOVERNANCE.md": [
            "Status: **Current authoritative governance**",
            "living specification",
            "rules/anki_card_rules.md",
            "sole current Markdown authority",
            "stable Note IDs are immutable",
        ],
        "README.md": ["living specification", "rules/anki_card_rules.md", "GOVERNANCE.md"],
        "SPEC.md": [
            "Current authoritative specification",
            "living document",
            "rules/anki_card_rules.md",
            "GOVERNANCE.md",
        ],
        "rules/anki_card_rules.md": [
            "Sole authoritative Anki card-design, coverage, active-deck, and recall rule set",
            "ANKI-GOV-002 / #98",
            "Cloze account names, not the whole tuple",
            "smallest uniquely recoverable accounting unit",
            "generated-card / retrieval-unit level",
            "Do not create a new current rule Markdown",
        ],
        "schema/note_schema.yaml": [
            "version: 1.1",
            "policy: living_spec",
            "authority: latest_merged",
            "governance_document: GOVERNANCE.md",
            "revision_gate: reviewed_change",
        ],
        "production/README.md": ["rules/anki_card_rules.md", "GOVERNANCE.md", "historical v1.0 pilot-baseline record"],
        "FREEZE.md": [
            "Status: **HISTORICAL — not current authority**",
            "Current governance note",
            "GOVERNANCE.md",
        ],
    }

    for rel, needles in required.items():
        try:
            text = read(rel)
        except FileNotFoundError:
            errors.append(f"missing governance file: {rel}")
            continue
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: required governance marker missing: {needle!r}")

    for rel in LEGACY_RULE_POINTERS:
        try:
            text = read(rel)
        except FileNotFoundError:
            errors.append(f"missing legacy rule compatibility path: {rel}")
            continue
        for needle in (
            "Historical/compatibility path; not an independent current authority",
            "rules/anki_card_rules.md",
            "Do not add new rule content here",
        ):
            if needle not in text:
                errors.append(f"{rel}: compatibility marker missing: {needle!r}")
        if "Current authoritative" in text:
            errors.append(f"{rel}: legacy pointer still claims current authority")

    schema = read("schema/note_schema.yaml")
    if "frozen:" in schema:
        errors.append("schema/note_schema.yaml: lifecycle must not carry a frozen flag under living-spec governance")

    freeze = read("FREEZE.md")
    if "not current authority" not in freeze:
        errors.append("FREEZE.md: historical-only status is not explicit")

    if errors:
        print("Living-spec governance validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Living-spec governance validation: PASS")
    print("authority=rules/anki_card_rules.md governance=living_spec historical_v1_0=record_only")
    print("legacy_rule_paths=compatibility_only stable_ids=immutable source_lineage=preserved rule_evolution=reviewed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
