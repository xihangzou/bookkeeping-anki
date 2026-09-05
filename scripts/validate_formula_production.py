#!/usr/bin/env python3
"""Corpus-wide formula/calculation QA for ANKI-040.

The audited population is reconstructed from the normalized active corpus as the
union of:
1) every approved Note whose primary Type is ``formula`` or ``measurement``;
2) every approved Note mapped from an INCLUDE ALP whose canonical type is
   ``formula`` or ``measurement``;
3) every approved Note mapped from a cost-accounting ALP whose canonical summary
   contains a calculation/allocation/valuation signal; and
4) every approved Note whose active Text itself contains an equation/arithmetic
   relation or a material calculation/allocation/valuation signal.

The deliberately redundant selection prevents a mistyped Note or ALP from
silently escaping the audit. The validator checks reproducible population
coverage, source traceability, source-summary operator/sign consistency,
formula-Cloze atomicity, visible operators, and retained worked arithmetic.
"""

from __future__ import annotations

import csv
import math
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
EQUATION_RE = re.compile(r"[＝=]")
ARITHMETIC_RE = re.compile(r"[＋+－−\-×÷*/]")
FORBIDDEN_OPERATOR_IN_CLOZE_RE = re.compile(r"[＝=＋+－−×÷*/]")
NUMERIC_EQUATION_RE = re.compile(
    r"(?P<expr>(?:\d[\d,]*(?:\.\d+)?\s*(?:円|個|kg|時間|h|％|%)?\s*"
    r"[＋+－−\-×÷*/]\s*)+\d[\d,]*(?:\.\d+)?\s*(?:円|個|kg|時間|h|％|%)?)"
    r"\s*[＝=]\s*(?P<result>\d[\d,]*(?:\.\d+)?)"
)

# Signals are intentionally broader than canonical primary Type. They select
# formula-dependent procedures (allocation, equivalent units, tax/depreciation,
# CVP, variances, etc.) even if their primary classification is not ``formula``.
CALC_SIGNALS = (
    "計算", "算定", "求め", "配賦", "按分", "換算", "評価", "測定", "差異",
    "償却", "利息", "税額", "税率", "課税所得", "原価標準", "標準原価",
    "予定配賦率", "配賦率", "賃率", "消費価格", "完成品換算量", "進捗度",
    "等価係数", "度外視法", "非度外視法", "CVP", "損益分岐", "貢献利益",
    "限界利益", "安全余裕", "営業レバレッジ", "加工換算量", "加工費換算量",
    "単価", "率を乗じ", "率を掛け", "％", "%",
)

# Short timing/relationship qualifiers should normally remain visible when they
# uniquely identify an operand role. This is a warning-level structural defect
# only when the entire qualifier+operand is hidden and the visible text does not
# already state the same qualifier immediately before the Cloze.
ROLE_PREFIXES = (
    "期首", "期末", "当期", "当月", "前月", "翌月", "切替時", "取得時", "決算時",
    "商品受渡時", "手付金授受時", "取引発生時", "予約時", "実際", "標準", "予定",
)

BROAD_FORMULA_ANSWERS = {
    "計算式", "算式", "公式", "計算する", "求める", "計算", "あり", "なし",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def strip_cloze(text: str) -> str:
    return CLOZE_RE.sub(lambda m: m.group(2), text)


def normalize_ops(text: str) -> str:
    return (
        text.replace("=", "＝")
        .replace("+", "＋")
        .replace("−", "－")
        .replace("-", "－")
        .replace("*", "×")
        .replace("/", "÷")
    )


def operator_signature(text: str) -> tuple[str, ...]:
    text = normalize_ops(strip_cloze(text))
    return tuple(ch for ch in text if ch in "＝＋－×÷")


def is_subsequence(needle: tuple[str, ...], haystack: tuple[str, ...]) -> bool:
    if not needle:
        return True
    it = iter(haystack)
    return all(any(ch == candidate for candidate in it) for ch in needle)


def has_calc_signal(text: str) -> bool:
    normalized = strip_cloze(text)
    return bool(EQUATION_RE.search(normalized) and ARITHMETIC_RE.search(normalized)) or any(
        signal in normalized for signal in CALC_SIGNALS
    )


def numeric_value(token: str) -> float:
    cleaned = re.sub(r"(?:円|個|kg|時間|h|％|%)", "", token)
    return float(cleaned.replace(",", "").strip())


def eval_numeric_expr(expr: str) -> float | None:
    # Normalize a retained simple arithmetic example to a safe Python expression.
    s = expr.replace("＋", "+").replace("−", "-").replace("－", "-").replace("×", "*").replace("÷", "/")
    s = re.sub(r"(?:円|個|kg|時間|h|％|%)", "", s)
    s = s.replace(",", "")
    if not re.fullmatch(r"[0-9.\s+\-*/()]+", s):
        return None
    try:
        return float(eval(s, {"__builtins__": {}}, {}))
    except (ZeroDivisionError, SyntaxError, ValueError):
        return None


def visible_prefix_before(text: str, start: int, prefix: str) -> bool:
    before = text[max(0, start - len(prefix) - 3):start]
    return prefix in strip_cloze(before)


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

    inventory: dict[str, dict[str, str]] = {}
    mandatory_alps: set[str] = set()
    calc_cost_alps: set[str] = set()
    for path in sorted(INVENTORY_DIR.glob("*.tsv")):
        for row in read_tsv(path):
            if row.get("status") != "INCLUDE":
                continue
            alp = row["alp_id"]
            inventory[alp] = row
            if row.get("type") in {"formula", "measurement"}:
                mandatory_alps.add(alp)
            if row.get("type") == "cost_accounting" and has_calc_signal(row.get("summary", "")):
                calc_cost_alps.add(alp)

    population: set[str] = set()
    selection_reasons: defaultdict[str, set[str]] = defaultdict(set)

    for nid, row in all_active.items():
        text = row.get("Text", "")
        if row.get("Type") in {"formula", "measurement"}:
            population.add(nid)
            selection_reasons[nid].add(f"note_type:{row.get('Type')}")
        if has_calc_signal(text):
            population.add(nid)
            selection_reasons[nid].add("text_calc_signal")

    for alp in sorted(mandatory_alps | calc_cost_alps):
        mapped = alp_to_notes.get(alp, [])
        if not mapped:
            errors.append(f"calculation ALP is not actively mapped: {alp}")
            continue
        for nid in mapped:
            population.add(nid)
            selection_reasons[nid].add(
                "alp_type:" + inventory[alp].get("type", "")
            )

    by_batch: Counter[str] = Counter(note_batch[nid] for nid in population)
    mapped_mandatory_alps: set[str] = set()
    mapped_calc_cost_alps: set[str] = set()
    formula_notes = 0
    measurement_notes = 0
    equations_checked = 0
    cloze_operands_checked = 0
    source_formula_relations_checked = 0
    recalculated_examples = 0

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

        if row.get("Type") == "formula":
            formula_notes += 1
        if row.get("Type") == "measurement":
            measurement_notes += 1

        mapped = set(row.get("ALP_IDs", "").split())
        mapped_mandatory_alps.update(mapped & mandatory_alps)
        mapped_calc_cost_alps.update(mapped & calc_cost_alps)

        plain = strip_cloze(text)
        has_equation = bool(EQUATION_RE.search(plain))
        if has_equation:
            equations_checked += 1

        cloze_matches = list(CLOZE_RE.finditer(text))
        for match in cloze_matches:
            answer = match.group(2).strip()
            cloze_operands_checked += 1
            if answer in BROAD_FORMULA_ANSWERS:
                errors.append(f"{nid}: broad/abstract formula Cloze answer {answer!r}")
            if FORBIDDEN_OPERATOR_IN_CLOZE_RE.search(answer):
                errors.append(f"{nid}: arithmetic/formula operator is hidden inside Cloze {answer!r}")
            if has_equation:
                for prefix in ROLE_PREFIXES:
                    if answer.startswith(prefix) and len(answer) > len(prefix) + 1:
                        if not visible_prefix_before(text, match.start(), prefix):
                            errors.append(
                                f"{nid}: timing/role modifier {prefix!r} is bundled into formula operand {answer!r}"
                            )
                            break

        # For canonical formula ALPs with an explicit formula in the inventory
        # summary, preserve the source operator/sign relationship. We compare as
        # an ordered subsequence so a Note may integrate multiple equivalent or
        # parallel formulas without being falsely rejected.
        for alp in sorted(mapped & mandatory_alps):
            inv = inventory[alp]
            summary = inv.get("summary", "")
            if inv.get("type") != "formula" or "＝" not in normalize_ops(summary):
                continue
            expected = operator_signature(summary)
            actual = operator_signature(text)
            if expected:
                source_formula_relations_checked += 1
                if not is_subsequence(expected, actual):
                    errors.append(
                        f"{nid}: operator/sign relationship for {alp} differs from canonical source summary "
                        f"expected={''.join(expected)} actual={''.join(actual)}"
                    )

        # Recalculate retained simple numerical equations. This intentionally
        # checks only expressions that can be parsed without accounting-specific
        # symbolic assumptions; symbolic formulas are validated above.
        for m in NUMERIC_EQUATION_RE.finditer(plain):
            value = eval_numeric_expr(m.group("expr"))
            if value is None:
                continue
            result = numeric_value(m.group("result"))
            recalculated_examples += 1
            if not math.isclose(value, result, rel_tol=1e-9, abs_tol=1e-9):
                errors.append(
                    f"{nid}: retained numerical application does not recalculate: "
                    f"{m.group('expr')} = {m.group('result')} (computed {value:g})"
                )

        validator = SCRIPTS_DIR / f"validate_{batch.lower().replace('-', '')}_production.py"
        if not validator.exists():
            errors.append(f"{nid}: missing chapter production validator for {batch}")

    missing_mandatory = sorted(mandatory_alps - mapped_mandatory_alps)
    if missing_mandatory:
        errors.append(f"formula/measurement ALPs missing from audited population: {missing_mandatory}")
    missing_calc_cost = sorted(calc_cost_alps - mapped_calc_cost_alps)
    if missing_calc_cost:
        errors.append(f"calculation-dependent cost ALPs missing from audited population: {missing_calc_cost}")

    print("ANKI-040 formula/calculation population")
    for batch in sorted(by_batch):
        ids = sorted(nid for nid in population if note_batch[nid] == batch)
        print(f"{batch}: {len(ids)} :: {' '.join(ids)}")
    print(
        f"audited_notes={len(population)} formula_notes={formula_notes} measurement_notes={measurement_notes} "
        f"mandatory_formula_measurement_alps={len(mandatory_alps)} mapped_mandatory_alps={len(mapped_mandatory_alps)} "
        f"calculation_cost_alps={len(calc_cost_alps)} mapped_calculation_cost_alps={len(mapped_calc_cost_alps)} "
        f"equations_checked={equations_checked} cloze_operands_checked={cloze_operands_checked} "
        f"source_formula_relations_checked={source_formula_relations_checked} "
        f"recalculated_examples={recalculated_examples}"
    )

    if errors:
        print(f"defects={len(errors)} unresolved={len(errors)}", file=sys.stderr)
        print("ANKI-040 formula/calculation validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("defects=0 unresolved=0")
    print("ANKI-040 formula/calculation validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
