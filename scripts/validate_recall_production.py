#!/usr/bin/env python3
"""Corpus-wide Cloze recall-quality QA for ANKI-041.

Audits every active production Note as rendered Anki cards. Chapter validators
remain the source-semantic backstop; ANKI-039 and ANKI-040 remain the journal
and formula/calculation backstops. This layer enforces corpus-wide recall
invariants and a severe recall-load ceiling.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "production" / "notes"
SCRIPTS_DIR = ROOT / "scripts"

SOURCE = (
    "xihangzou/bookkeeping-integrated",
    "569ed7b82e729334e1472286eaca7c4352e6fbdb",
    "merged/textbook.md",
)
EXPECTED_BATCHES = 31
EXPECTED_ACTIVE_NOTES = 735
EXPECTED_ACTIVE_CARDS = 748
EXPECTED_ACTIVE_CLOZE_SPANS = 2008

CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)(?:::[^{}]*?)?\}\}")
SPACE_RE = re.compile(r"\s+")
SEMANTIC_RE = re.compile(r"[0-9A-Za-z一-龯ぁ-んァ-ヶ々〆ヶ]+")

BROAD_ANSWERS = {
    "仕訳を行う", "仕訳を行わない", "処理する", "計上する", "計上しない",
    "増加させる", "減少させる", "振り替える", "修正する", "調整する",
    "計算する", "算定する", "求める", "あり", "なし",
}
PLACEHOLDER_ANSWERS = {
    "適切な勘定科目", "本来の勘定科目", "正しい勘定科目", "正しい処理",
    "適切な処理", "本来の科目", "正しい仕訳", "適切な仕訳",
}
PLACEHOLDER_EXCEPTIONS = {
    # Canonical operand in the correction-entry relationship, reconciled in
    # ANKI-040 rather than a prompt placeholder.
    ("BK-FND-00-0015", "正しい仕訳"),
}
ALLOWED_PARALLEL_TERMS = {
    # Fixed canonical accounting labels; punctuation is lexical, not a list of
    # independently removable targets.
    "子会社株式・関連会社株式",
    "ファイナンス・リース",
    "オペレーティング・リース",
    "評価・換算差額等",
    "法人税、住民税及び事業税",
}
LEAKAGE_EXCEPTIONS = {
    # IND-06 chapter QA explicitly retains the compound source-category cue
    # 「各補助部門費」 while testing the classification label 「補助部門」.
    ("BK-IND-06-0016", "補助部門"),
}

EXPECTED_MULTI_INDEX = {
    "BK-FND-00-0047": {"1", "2"},
    "BK-FND-00-0068": {"1", "2", "3"},
    "BK-FND-00-0091": {"1", "2", "3"},
    "BK-IND-04-0003": {"1", "2", "3"},
    "BK-COM-15-0023": {"1", "2", "3"},
    "BK-COM-15-0024": {"1", "2", "3"},
    "BK-COM-15-0044": {"1", "2", "3"},
}
EXPECTED_RETAINED_SEMANTIC_PAIRS = {
    frozenset(("BK-IND-10-0008", "BK-IND-12-0005")),
    frozenset(("BK-IND-05-0005", "BK-IND-06-0021")),
    frozenset(("BK-COM-13-0018", "BK-IND-12-0006")),
    frozenset(("BK-IND-03-0003", "BK-IND-04-0002")),
}
ACCOUNTING_ABBREVIATIONS = ("B/S", "P/L", "S/S", "T/B", "F/S", "CVP")
GENERIC_CONTEXT_TOKENS = {
    "である", "という", "とは", "場合", "とき", "もの", "こと", "する",
    "した", "として", "それぞれ", "次", "以下", "上記",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def strip_cloze(text: str) -> str:
    return CLOZE_RE.sub(lambda m: m.group(2), text)


def visible_card(text: str, target_index: str) -> str:
    def repl(match: re.Match[str]) -> str:
        return " □ " if match.group(1) == target_index else match.group(2)
    return CLOZE_RE.sub(repl, text)


def compact(text: str) -> str:
    return re.sub(r"[^0-9A-Za-z一-龯ぁ-んァ-ヶ々〆ヶ]", "", text).lower()


def compact_semantic(text: str) -> str:
    return compact(strip_cloze(text))


def bigrams(text: str) -> set[str]:
    return {text[i:i + 2] for i in range(len(text) - 1)} if len(text) >= 2 else ({text} if text else set())


def similarity(a: str, b: str) -> float:
    aa, bb = bigrams(a), bigrams(b)
    return len(aa & bb) / len(aa | bb) if aa and bb else 0.0


def batch_of(note_id: str) -> str:
    m = re.match(r"BK-(FND|COM|IND)-(\d{2})-", note_id)
    return f"{m.group(1)}-{m.group(2)}" if m else "UNKNOWN"


def has_sufficient_visible_context(card: str) -> bool:
    plain = card.replace("□", " ")
    if any(abbrev in plain for abbrev in ACCOUNTING_ABBREVIATIONS):
        return True
    tokens = [t for t in SEMANTIC_RE.findall(plain) if t not in GENERIC_CONTEXT_TOKENS]
    return any(len(t) >= 2 for t in tokens)


def repeated_fixed_head(text: str, match: re.Match[str]) -> str | None:
    """Return a literal visible head redundantly repeated in the answer.

    Only the literal segment immediately before this Cloze is considered. This
    avoids treating an earlier same-index answer, a formula number/operator, or
    punctuation-separated canonical term as a fixed visible head.
    """
    answer = compact(match.group(2))
    if len(answer) < 4:
        return None
    literal_before = text[:match.start()].rsplit("}}", 1)[-1]
    found = re.search(r"([0-9A-Za-z一-龯ぁ-んァ-ヶ々〆ヶの]{3,12})$", literal_before)
    if not found:
        return None
    head = compact(found.group(1))
    return head if answer.startswith(head) else None


def main() -> int:
    defects: list[tuple[str, str]] = []
    counts: Counter[str] = Counter()

    def defect(category: str, message: str) -> None:
        defects.append((category, message))
        counts[category] += 1

    note_paths = sorted(NOTES_DIR.glob("*.tsv"))
    if len(note_paths) != EXPECTED_BATCHES:
        defect("population", f"expected {EXPECTED_BATCHES} production batches, found {len(note_paths)}")

    active: dict[str, dict[str, str]] = {}
    note_batch: dict[str, str] = {}
    for path in note_paths:
        for row in read_tsv(path):
            if row.get("Status") != "approved":
                continue
            nid = row["ID"]
            if nid in active:
                defect("population", f"duplicate active Note ID: {nid}")
                continue
            active[nid] = row
            note_batch[nid] = path.stem

    if len(active) != EXPECTED_ACTIVE_NOTES:
        defect("population", f"expected {EXPECTED_ACTIVE_NOTES} active Notes, found {len(active)}")

    generated_cards = 0
    total_spans = 0
    multi_index_actual: dict[str, set[str]] = {}
    high_load_cards: list[tuple[int, int, str, str]] = []
    by_type: Counter[str] = Counter()
    by_batch: Counter[str] = Counter()
    exact_plain: defaultdict[str, list[str]] = defaultdict(list)

    for nid in sorted(active):
        row = active[nid]
        text = row.get("Text", "")
        by_type[row.get("Type", "")] += 1
        by_batch[note_batch[nid]] += 1

        if (row.get("SourceRepo"), row.get("SourceCommit"), row.get("SourcePath")) != SOURCE:
            defect("traceability", f"{nid}: source traceability drift")
        if row.get("QA") != "pass":
            defect("qa_state", f"{nid}: QA must be pass")

        matches = list(CLOZE_RE.finditer(text))
        if not matches:
            defect("cloze_structure", f"{nid}: approved Note has no valid Cloze target")
            continue

        indices = {m.group(1) for m in matches}
        generated_cards += len(indices)
        total_spans += len(matches)
        if len(indices) > 1:
            multi_index_actual[nid] = indices

        answer_indices: defaultdict[str, set[str]] = defaultdict(set)
        for m in matches:
            idx = m.group(1)
            answer_raw = m.group(2)
            answer = answer_raw.strip()
            if answer_raw != answer:
                defect("lexical_scope", f"{nid}: Cloze answer has boundary whitespace {answer_raw!r}")
            if not answer:
                defect("lexical_scope", f"{nid}: empty Cloze answer")
                continue
            if answer in BROAD_ANSWERS:
                defect("broad_action", f"{nid}: broad/abstract action answer {answer!r}")
            if answer in PLACEHOLDER_ANSWERS and (nid, answer) not in PLACEHOLDER_EXCEPTIONS:
                defect("ambiguous_placeholder", f"{nid}: placeholder answer {answer!r}")
            if ("・" in answer or "、" in answer) and answer not in ALLOWED_PARALLEL_TERMS:
                defect("parallel_atomicity", f"{nid}: parallel terms are bundled in one Cloze {answer!r}")
            head = repeated_fixed_head(text, m)
            if head:
                defect("redundant_fixed_head", f"{nid}: visible fixed head {head!r} is repeated inside answer {answer!r}")
            answer_indices[compact(answer)].add(idx)

        for ans, idxs in answer_indices.items():
            if ans and len(idxs) > 1:
                defect("index_grouping", f"{nid}: same answer is split across Cloze indices {sorted(idxs)}: {ans!r}")

        for idx in sorted(indices, key=int):
            card = visible_card(text, idx)
            if not has_sufficient_visible_context(card):
                defect("context_sufficiency", f"{nid} c{idx}: target hidden leaves no identifiable retrieval subject: {card!r}")

            visible_norm = compact(card.replace("□", ""))
            target_answers = [m.group(2).strip() for m in matches if m.group(1) == idx]
            for answer in target_answers:
                ans = compact(answer)
                if len(ans) >= 2 and ans in visible_norm and (nid, answer) not in LEAKAGE_EXCEPTIONS:
                    defect("visible_sibling_leakage", f"{nid} c{idx}: answer remains visible elsewhere on generated card: {answer!r}")

            span_count = len(target_answers)
            answer_chars = sum(len(compact(a)) for a in target_answers)
            if span_count >= 9:
                defect("recall_load", f"{nid} c{idx}: {span_count} targets hidden together; split into semantic groups")
            elif span_count >= 6 or answer_chars >= 40:
                high_load_cards.append((span_count, answer_chars, nid, idx))

        exact_plain[SPACE_RE.sub(" ", strip_cloze(text)).strip()].append(nid)

        validator = SCRIPTS_DIR / f"validate_{note_batch[nid].lower().replace('-', '')}_production.py"
        if not validator.exists():
            defect("chapter_backstop", f"{nid}: missing chapter production validator for {note_batch[nid]}")

    if generated_cards != EXPECTED_ACTIVE_CARDS:
        defect("population", f"expected {EXPECTED_ACTIVE_CARDS} generated cards, found {generated_cards}")
    if total_spans != EXPECTED_ACTIVE_CLOZE_SPANS:
        defect("population", f"expected {EXPECTED_ACTIVE_CLOZE_SPANS} active Cloze spans, found {total_spans}")
    if multi_index_actual != EXPECTED_MULTI_INDEX:
        defect("index_grouping", f"multi-index Note set drift: expected={EXPECTED_MULTI_INDEX} actual={multi_index_actual}")

    duplicate_groups = [ids for ids in exact_plain.values() if len(ids) > 1]
    if duplicate_groups:
        defect("duplicate_retrieval", f"exact duplicate active retrieval propositions: {duplicate_groups[:30]}")

    semantic_pairs: set[frozenset[str]] = set()
    compact_cache = {nid: compact_semantic(row["Text"]) for nid, row in active.items()}
    ids = sorted(active)
    for i, left in enumerate(ids):
        a = compact_cache[left]
        if len(a) < 18:
            continue
        for right in ids[i + 1:]:
            if batch_of(left) == batch_of(right):
                continue
            b = compact_cache[right]
            if len(b) < 18:
                continue
            if min(len(a), len(b)) / max(len(a), len(b)) < 0.55:
                continue
            if similarity(a, b) >= 0.50:
                semantic_pairs.add(frozenset((left, right)))

    new_semantic = semantic_pairs - EXPECTED_RETAINED_SEMANTIC_PAIRS
    missing_semantic = EXPECTED_RETAINED_SEMANTIC_PAIRS - semantic_pairs
    if new_semantic:
        defect("duplicate_retrieval", f"new cross-batch semantic similarity candidates: {sorted(map(sorted, new_semantic))}")
    if missing_semantic:
        defect("duplicate_retrieval", f"documented retained semantic pairs changed below audit threshold: {sorted(map(sorted, missing_semantic))}")

    print("ANKI-041 recall-quality population")
    print(
        f"batches={len(note_paths)} audited_notes={len(active)} generated_cards={generated_cards} "
        f"cloze_spans={total_spans} multi_index_notes={len(multi_index_actual)}"
    )
    print("by_batch=" + " ".join(f"{k}:{by_batch[k]}" for k in sorted(by_batch)))
    print("by_type=" + " ".join(f"{k}:{by_type[k]}" for k in sorted(by_type)))
    print(f"retained_semantic_pairs_rechecked={len(semantic_pairs)}")

    high_load_cards.sort(reverse=True)
    print(f"moderate_high_load_cards_review_set={len(high_load_cards)}")
    for spans, chars, nid, idx in high_load_cards:
        print(f"HIGH_LOAD_REVIEWED {nid} c{idx} spans={spans} answer_chars={chars}")

    if defects:
        print(f"defects={len(defects)} unresolved={len(defects)}", file=sys.stderr)
        print("defects_by_category=" + " ".join(f"{k}:{counts[k]}" for k in sorted(counts)), file=sys.stderr)
        print("ANKI-041 recall-quality validation: FAIL", file=sys.stderr)
        for category, message in defects:
            print(f"- [{category}] {message}", file=sys.stderr)
        return 1

    print("defects=0 unresolved=0")
    print("ANKI-041 recall-quality validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
