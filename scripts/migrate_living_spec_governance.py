#!/usr/bin/env python3
"""Apply ANKI-GOV-001 living-spec governance migration.

This migration is intentionally idempotent. It converts current-authority
references from a permanent v1.0 freeze model to reviewed living-spec
governance while preserving the historical pilot baseline as history.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def save(rel: str, text: str) -> None:
    (ROOT / rel).write_text(text, encoding="utf-8")


def replace(rel: str, old: str, new: str) -> None:
    text = load(rel)
    if old in text:
        text = text.replace(old, new)
        save(rel, text)


def prepend_once(rel: str, marker: str, block: str) -> None:
    text = load(rel)
    if marker not in text:
        save(rel, block + text)


# Current general rules: v1.0 is historical baseline, not permanent authority.
replace(
    "rules/cloze_rules.md",
    "Status: **v1.0 — frozen after representative pilot (ANKI-PILOT-006)**",
    "Status: **Current authoritative Cloze rules — living specification**\nGovernance: `GOVERNANCE.md`",
)
replace(
    "rules/cloze_rules.md",
    "v1.0 は `pilot/review.md` に記録された ANKI-PILOT-003/004 の実測結果だけを根拠として v0.9 を改訂し、ANKI-PILOT-006 で凍結した。schema/tag/source/TSV contract は pilot 上の摩擦がなかったため意味変更せず、version/lifecycle metadata のみ v1.0 freeze に整合させる。",
    "v1.0 は `pilot/review.md` に記録された ANKI-PILOT-003/004 の実測結果を根拠として成立した初期production baselineである。現在はliving specificationとして、pilot・production audit・後続chapterの実測結果に基づき本ルール自体を明示的に更新する。schema/tag/source/TSVのlineage要件は、変更不要だったというv1.0時点の判断を履歴として保持しつつ、将来のreviewed changeを妨げない。",
)
replace(
    "rules/cloze_rules.md",
    "## 26. v1.0 pilot validation gate",
    "## 26. Historical v1.0 pilot validation gate",
)
replace(
    "rules/cloze_rules.md",
    "Pilot corpus は freeze evidence として `Status=pilot` / `QA=pending` のまま保持してよい。production へ再利用する場合は frozen v1.0 contract に対する production QA と stable ID/mapping 要件を満たしたものだけを昇格させる。",
    "Pilot corpus は historical baseline evidence として `Status=pilot` / `QA=pending` のまま保持してよい。production へ再利用する場合は、再利用時点のcurrent authoritative rulesとstable ID/source-mapping要件を満たしたものだけを昇格させる。",
)
replace(
    "rules/cloze_rules.md",
    "ANKI-PILOT-006 ではこれらの semantics を変更せず、schema version/lifecycle metadata のみ v1.0/frozen に更新した。",
    "ANKI-PILOT-006 ではこれらの semantics を変更せず、schema version/lifecycle metadata を当時のv1.0 production baselineとして記録した。この判断はhistorical evidenceであり、後続のreviewed schema/rule変更を禁止しない。",
)
replace(
    "rules/cloze_rules.md",
    "## 28. ANKI-PILOT-006 freeze decision\n\nThe final pilot gate passes and this authoring contract is frozen as **v1.0** for chapter-wide production.",
    "## 28. Historical ANKI-PILOT-006 baseline decision\n\nThe final pilot gate passed and established **v1.0** as the initial chapter-wide production baseline. Under current governance this is a historical milestone, not a permanent semantic freeze.",
)
replace(
    "rules/cloze_rules.md",
    "- `rules/coverage_rules.md`, `schema/note_schema.yaml`, and `SPEC.md` identify the same v1.0 frozen contract.\n\nANKI-007 onward is explicitly authorized to generate production Notes under this frozen v1.0 contract. Any later semantic contract change requires a separately reviewed post-freeze migration rather than silent local deviation.",
    "- `rules/coverage_rules.md`, `schema/note_schema.yaml`, and `SPEC.md` were aligned at the historical v1.0 production gate.\n\nANKI-007 onward was authorized by that historical gate. Current and future generation must use the latest merged authoritative rules. Semantic changes must still be explicit, reviewed, validated, and migrated where necessary, but no permanent v1.0 freeze or special post-freeze exception mechanism applies.",
)

replace(
    "rules/coverage_rules.md",
    "Status: **v1.0 — frozen after representative pilot (ANKI-PILOT-006)**",
    "Status: **Current authoritative coverage rules — living specification**\nGovernance: `GOVERNANCE.md`",
)
replace(
    "rules/coverage_rules.md",
    "Those contracts remain unchanged for the v1.0 freeze gate.",
    "Those items were unchanged at the historical v1.0 pilot gate. Later reviewed changes remain permitted under `GOVERNANCE.md`.",
)
replace(
    "rules/coverage_rules.md",
    "## 16. ANKI-PILOT-006 freeze decision\n\nThe v1.0 candidate passed the final pilot gate and is frozen for Phase C production.\n\nFreeze evidence:\n\n- corrected pilot: **40 Notes / 62 generated cards**;\n- accounting failures: **0**;\n- source-traceability failures: **0**;\n- major findings: **0**;\n- blocking findings: **0**;\n- recurring/minor finding families are governed by explicit v1.0 rules or documented no-change decisions;\n- canonical ALP IDs and source mappings remain unchanged.\n\nChapter-wide generation from ANKI-007 onward must use this frozen v1.0 coverage contract unless a separately reviewed post-freeze migration is explicitly approved.",
    "## 16. Historical ANKI-PILOT-006 baseline decision\n\nThe v1.0 candidate passed the final pilot gate and established the initial Phase C production baseline.\n\nHistorical gate evidence:\n\n- corrected pilot: **40 Notes / 62 generated cards**;\n- accounting failures: **0**;\n- source-traceability failures: **0**;\n- major findings: **0**;\n- blocking findings: **0**;\n- recurring/minor finding families had explicit v1.0 rules or documented no-change decisions;\n- canonical ALP IDs and source mappings remained unchanged.\n\nChapter-wide generation from ANKI-007 onward was originally authorized by this gate. Current generation and explicit migrations use the latest merged coverage rules under `GOVERNANCE.md`.\n\n## 17. Rule evolution\n\nCoverage rules are revised when later chapter work or QA reveals an omission, duplicate, over-compression, or better retrieval design. Preserve historical metrics and source lineage, but update this file rather than keeping a known-bad rule solely because it existed in v1.0.",
)

# Chapter QA should describe its audited state while pointing to current governance.
replace(
    "production/qa/FND-00.md",
    "Contracts:\n- frozen v1.0 source/schema/stable-ID baseline;\n- current v1.6 post-freeze integration / completeness / Cloze overlay: `rules/exam_yield_rules.md`.",
    "Governance and contracts:\n- repository governance: `GOVERNANCE.md`;\n- current general specification/rules/schema: latest merged `SPEC.md`, `rules/*.md`, and `schema/note_schema.yaml`;\n- this chapter's applied audit state: FND-00 through v1.6 / ANKI-AUDIT-006 (#70).",
)
replace(
    "production/qa/COM-01.md",
    "- frozen v1.0 source/schema/stable-ID baseline: `FREEZE.md`, `rules/cloze_rules.md`, `rules/coverage_rules.md`, `schema/note_schema.yaml`\n- current v1.6 post-freeze active-deck / recall-design overlay: `rules/exam_yield_rules.md`",
    "- repository governance: `GOVERNANCE.md`\n- current general specification/rules/schema: latest merged `SPEC.md`, `rules/*.md`, and `schema/note_schema.yaml`\n- this chapter's applied audit state includes the v1.6 recall-design / formula-itemization audit",
)
replace(
    "production/qa/COM-02.md",
    "Contract: frozen v1.0 source/schema/Cloze/coverage rules plus the v1.2 exam-yield and generated-card-efficiency overlay in `rules/exam_yield_rules.md`.",
    "Governance: `GOVERNANCE.md`. COM-02 retains its explicitly audited chapter state from ANKI-009; current general rules are authoritative for new work, while this existing batch is migrated when a newer rule is explicitly applied to it.",
)

# Validator descriptions should not encode obsolete governance.
replace(
    "scripts/validate_com01_production.py",
    '"""Validate the COM-01 production batch under frozen v1.0 + v1.2 overlay."""',
    '"""Validate the COM-01 production batch under its current explicitly audited state."""',
)
replace(
    "scripts/validate_com02_production.py",
    '"""Validate the COM-02 production batch under frozen v1.0 + v1.2 overlay."""',
    '"""Validate the COM-02 production batch under its current explicitly audited state."""',
)

# Structure is source-pinned, not rule-frozen.
replace(
    "inventory/structure.md",
    "Status: **ANKI-002 complete / frozen**",
    "Status: **ANKI-002 complete / source-pinned snapshot**",
)
replace(
    "inventory/structure.md",
    "structure inventory frozen for ANKI-003 decomposition",
    "structure inventory recorded as the source-pinned snapshot for ANKI-003 decomposition",
)
replace("inventory/structure.md", "## Freeze rule", "## Snapshot / update rule")

# Mechanical validator messages use source-pinning terminology.
path = ROOT / "scripts/validate_topic_inventory.py"
text = path.read_text(encoding="utf-8")
text = text.replace("frozen structure", "pinned structure snapshot")
path.write_text(text, encoding="utf-8")

# Historical pilot files keep chronology but explicitly disclaim current authority.
historical_banner = (
    "> **Historical pilot artifact.** References in this file to a v1.0 freeze describe the original pre-production gate. "
    "They do not define current repository governance; current authority is `GOVERNANCE.md` and the latest merged specification/rules/schema.\n\n"
)
for rel in ("pilot/PLAN.md", "pilot/VALIDATION.md", "pilot/review.md"):
    prepend_once(rel, "**Historical pilot artifact.**", historical_banner)

# TASKS preserves historical task meaning while recording the governance change.
replace("TASKS.md", "## Phase B — Pilot and rule freeze", "## Phase B — Pilot and initial production baseline")
replace("TASKS.md", "**ANKI-PILOT-006** Freeze v1.0 before full generation", "**ANKI-PILOT-006** Establish v1.0 initial production baseline")
replace("TASKS.md", "`FREEZE.md`: final gate evidence and production authorization", "`FREEZE.md`: historical gate evidence and original production authorization")
replace("TASKS.md", "`SPEC.md`, `rules/cloze_rules.md`, `rules/coverage_rules.md`: v1.0 frozen", "`SPEC.md`, `rules/cloze_rules.md`, `rules/coverage_rules.md`: v1.0 baseline recorded (later superseded by living-spec governance)")
replace("TASKS.md", "`schema/note_schema.yaml`: v1.0 / production / frozen; semantic schema contract unchanged", "`schema/note_schema.yaml`: v1.0 production baseline recorded; semantic schema contract was unchanged at that gate")

tasks = load("TASKS.md")
gov_entry = """- [x] **ANKI-GOV-001** Living-spec governance / retire permanent v1.0 freeze authority (#73)\n  - latest merged `SPEC.md`, `rules/*.md`, schema, and applicable QA/validators are the current authority\n  - `FREEZE.md` retained as historical v1.0 baseline evidence only\n  - stable IDs, source traceability, pinned batch provenance, and deterministic lineage remain persistent invariants\n  - schema lifecycle changed from frozen v1.0 metadata to reviewed living-spec governance\n  - governance CI prevents reintroduction of active `frozen v1.0` / `post-freeze` authority language\n"""
if "**ANKI-GOV-001**" not in tasks:
    anchor = "\n### Commercial bookkeeping\n"
    tasks = tasks.replace(anchor, "\n" + gov_entry + anchor)
    save("TASKS.md", tasks)

# Production CI should run for governance/current-rule changes and run governance QA.
workflow = load(".github/workflows/validate-production.yml")
old_watch = "      - 'schema/note_schema.yaml'\n      - 'rules/exam_yield_rules.md'"
new_watch = "      - 'GOVERNANCE.md'\n      - 'README.md'\n      - 'SPEC.md'\n      - 'FREEZE.md'\n      - 'schema/note_schema.yaml'\n      - 'rules/cloze_rules.md'\n      - 'rules/coverage_rules.md'\n      - 'rules/exam_yield_rules.md'"
workflow = workflow.replace(old_watch, new_watch)
old_scripts = "      - 'scripts/validate_fnd00_production.py'"
new_scripts = "      - 'scripts/migrate_living_spec_governance.py'\n      - 'scripts/validate_governance.py'\n      - 'scripts/validate_fnd00_production.py'"
workflow = workflow.replace(old_scripts, new_scripts)
if "validate-governance:" not in workflow:
    job = """\n  validate-governance:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with:\n          python-version: '3.12'\n      - name: Validate living-spec governance\n        run: python scripts/validate_governance.py\n"""
    workflow = workflow.replace("\njobs:\n", "\njobs:\n" + job)
save(".github/workflows/validate-production.yml", workflow)

# ANKI-GOV-001 final terminology cleanup
for rel in ("rules/cloze_rules.md", "production/README.md"):
    current = load(rel)
    current = current.replace("post-freeze", "later reviewed")
    current = current.replace("permanently frozen v1.0 contract", "v1.0 as a permanent authority")
    save(rel, current)

print("ANKI-GOV-001 living-spec governance migration applied")
