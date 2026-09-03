#!/usr/bin/env python3
"""Apply ANKI-AUDIT-003 FND-00 v1.3 minimal/atomic migration."""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "FND-00.tsv"

FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]

ACTIVE_IDS = {
    "BK-FND-00-0022",
    "BK-FND-00-0002",
    "BK-FND-00-0004",
    "BK-FND-00-0005",
    "BK-FND-00-0037",
    "BK-FND-00-0044",
    "BK-FND-00-0010",
    "BK-FND-00-0011",
    "BK-FND-00-0053",
    "BK-FND-00-0054",
    "BK-FND-00-0055",
    "BK-FND-00-0014",
    "BK-FND-00-0058",
    "BK-FND-00-0015",
    "BK-FND-00-0075",
    "BK-FND-00-0078",
    "BK-FND-00-0086",
    "BK-FND-00-0088",
}

TEXT_OVERRIDES = {
    "BK-FND-00-0022": "複数の会社が登場しても、仕訳は {{c1::当社}} の立場で判断する。",
    "BK-FND-00-0002": "財産や権利は {{c1::資産}}。返済義務は {{c2::負債}}。返済義務のない調達源泉は {{c3::純資産}}。会社の儲けの原因は {{c4::収益}}。収益を得るための消費は {{c5::費用}}。",
    "BK-FND-00-0004": "資産・費用の増加は {{c1::借方}} に記入する。負債・純資産・収益の増加は {{c2::貸方}} に記入する。減少は反対側に記入する。",
    "BK-FND-00-0005": "1つの仕訳では、借方合計と貸方合計が必ず {{c1::一致}} する。",
    "BK-FND-00-0037": "火災・盗難で資産が減少すれば、簿記上の {{c1::取引}} となる。5要素が変化しない契約締結は、簿記上の取引に {{c2::ならない}}。",
    "BK-FND-00-0044": "総勘定元帳の各勘定を集計し、貸借一致を確認する一覧表を {{c1::試算表}} という。",
    "BK-FND-00-0010": "借方・貸方の合計を集計するのは {{c1::合計試算表}}。残高を集計するのは {{c2::残高試算表}}。合計と残高を集計するのは {{c3::合計残高試算表}}。",
    "BK-FND-00-0011": "借貸双方を同額誤記しても、試算表の借方合計と貸方合計は {{c1::一致}} してしまう。",
    "BK-FND-00-0053": "給与は手取額ではなく {{c1::総額}} を費用計上する。控除した所得税は {{c2::所得税預り金}} で処理する。",
    "BK-FND-00-0054": "源泉所得税を税務署へ納付するとき、所得税預り金は {{c1::借方}} に計上する。",
    "BK-FND-00-0055": "従業員負担の社会保険料は {{c1::社会保険料預り金}} で処理する。会社負担分は {{c2::法定福利費}} で処理する。",
    "BK-FND-00-0014": "支払内容・金額が未確定なら {{c1::仮払金}} で処理する。内容確定後、仮払金は {{c2::貸方}} で取り崩す。",
    "BK-FND-00-0058": "入金内容が不明なら {{c1::仮受金}} で処理する。内容判明後、仮受金は {{c2::借方}} で取り崩す。",
    "BK-FND-00-0015": "誤仕訳を取り消す仕訳を {{c1::逆仕訳}} という。訂正では、逆仕訳の後に {{c2::正しい仕訳}} を行う。",
    "BK-FND-00-0075": "総勘定元帳の売掛金・買掛金残高は、各補助元帳残高の {{c1::合計}} と一致する。",
    "BK-FND-00-0078": "現金が増える取引は {{c1::入金伝票}}。現金が減る取引は {{c2::出金伝票}}。現金が増減しない取引は {{c3::振替伝票}}。",
    "BK-FND-00-0086": "納品明細は {{c1::納品書}}。請求金額の明細は {{c2::請求書}}。支払の証明は {{c3::領収書}}。当座預金の入出金明細は {{c4::当座勘定照合表}}。",
    "BK-FND-00-0088": "証ひょうの原本・控えから判断するのは当社の {{c1::立場}}。証ひょうだけでは {{c2::決済方法}} を確定しない。",
}


def lifecycle_tags(tags: str, status: str) -> str:
    parts = [t for t in tags.split() if not t.startswith("status::")]
    parts.append(f"status::{status}")
    return " ".join(sorted(set(parts)))


def main() -> int:
    with NOTES.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        rows = list(reader)
        if list(reader.fieldnames or []) != FIELDS:
            raise SystemExit("FND-00 header mismatch")

    seen = {row["ID"] for row in rows}
    missing = sorted(ACTIVE_IDS - seen)
    if missing:
        raise SystemExit(f"missing active IDs: {missing}")

    for row in rows:
        note_id = row["ID"]
        target_status = "approved" if note_id in ACTIVE_IDS else "deprecated"
        old_status = row["Status"]
        row["Status"] = target_status
        row["QA"] = "pass"
        row["Tags"] = lifecycle_tags(row["Tags"], target_status)

        if note_id in TEXT_OVERRIDES:
            row["Text"] = TEXT_OVERRIDES[note_id]

        if old_status == "approved" and target_status == "deprecated" and "ANKI-AUDIT-003" not in row["Extra"]:
            suffix = "ANKI-AUDIT-003でactive direct recallから退役。source traceabilityは履歴行とchapter QAで保持する。"
            row["Extra"] = (row["Extra"].rstrip() + " " + suffix).strip()

    with NOTES.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    # Defensive post-write metrics.
    cloze_re = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
    approved = [r for r in rows if r["Status"] == "approved"]
    cards = sum(len({int(i) for i, _ in cloze_re.findall(r["Text"])}) for r in approved)
    active_alps = {alp for r in approved for alp in r["ALP_IDs"].split()}
    print(f"FND-00 v1.3 migration applied: approved={len(approved)} cards={cards} active_alps={len(active_alps)}")
    if len(approved) != 18 or cards != 37 or len(active_alps) != 36:
        raise SystemExit("unexpected v1.3 target metrics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
