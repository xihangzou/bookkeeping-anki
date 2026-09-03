#!/usr/bin/env python3
"""Validate living-spec governance and prevent obsolete freeze authority from returning."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CURRENT_AUTHORITY_FILES = [
    "README.md",
    "SPEC.md",
    "rules/cloze_rules.md",
    "rules/coverage_rules.md",
    "rules/exam_yield_rules.md",
    "schema/note_schema.yaml",
    "production/README.md",
    "production/qa/FND-00.md",
    "production/qa/COM-01.md",
    "production/qa/COM-02.md",
    "scripts/validate_com01_production.py",
    "scripts/validate_com02_production.py",
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
            "latest merged",
            "stable Note IDs are immutable",
        ],
        "README.md": ["living specification", "GOVERNANCE.md"],
        "SPEC.md": ["Current authoritative specification", "living document", "GOVERNANCE.md"],
        "rules/cloze_rules.md": ["Current authoritative Cloze rules", "GOVERNANCE.md"],
        "rules/coverage_rules.md": ["Current authoritative coverage rules", "GOVERNANCE.md"],
        "rules/exam_yield_rules.md": ["Current authoritative rules", "living specification", "GOVERNANCE.md"],
        "schema/note_schema.yaml": [
            "version: 1.1",
            "policy: living_spec",
            "authority: latest_merged",
            "governance_document: GOVERNANCE.md",
            "revision_gate: reviewed_change",
        ],
        "production/README.md": ["latest merged", "GOVERNANCE.md", "historical v1.0 pilot-baseline record"],
        "FREEZE.md": [
            "Status: **HISTORICAL — not current authority**",
            "Current governance note",
            "GOVERNANCE.md",
        ],
        "scripts/migrate_living_spec_governance.py": [
            "ANKI-GOV-001 final terminology cleanup",
            "living-spec governance migration applied",
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
    print("authority=latest_merged governance=living_spec historical_v1_0=record_only")
    print("stable_ids=immutable source_lineage=preserved rule_evolution=reviewed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
