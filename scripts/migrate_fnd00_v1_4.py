#!/usr/bin/env python3
"""Apply ANKI-AUDIT-004 FND-00 v1.4 balanced/context-preserving migration."""

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
    "BK-FND-00-0018",
    "BK-FND-00-0022",
    "BK-FND-00-0003",
    "BK-FND-00-0024",
    "BK-FND-00-0025",
    "BK-FND-00-0026",
    "BK-FND-00-0027",
    "BK-FND-00-0002",
    "BK-FND-00-0004",
    "BK-FND-00-0005",
    "BK-FND-00-0037",
    "BK-FND-00-0009",
    "BK-FND-00-0044",
    "BK-FND-00-0010",
    "BK-FND-00-0011",
    "BK-FND-00-0012",
    "BK-FND-00-0047",
    "BK-FND-00-0053",
    "BK-FND-00-0054",
    "BK-FND-00-0055",
    "BK-FND-00-0014",
    "BK-FND-00-0058",
    "BK-FND-00-0015",
    "BK-FND-00-0062",
    "BK-FND-00-0068",
    "BK-FND-00-0075",
    "BK-FND-00-0078",
    "BK-FND-00-0086",
    "BK-FND-00-0088",
}

TEXT_OVERRIDES = {
    "BK-FND-00-0018": "簿記の基本では、会社の取引を記録する媒体を {{c1::帳簿}}、そこへ書き込むことを {{c1::記帳}} といい、取引を記録・集計して財務諸表を作成する仕組みを {{c1::簿記}} という。",
    "BK-FND-00-0022": "複数の会社が登場しても、仕訳は {{c1::当社}} の立場で判断する。",
    "BK-FND-00-0003": "資金調達・運用の基本用語では、株主から返済義務のない資金を受け取るのが {{c1::出資}}、返済義務のある資金を受け取るのが {{c1::借入}}、他者へ資金を貸すのが {{c1::貸付}} である。",
    "BK-FND-00-0024": "商品売買の基本用語では、販売先を {{c1::得意先}}、購入先を {{c1::仕入先}}、代金後払いを {{c1::掛け}} という。",
    "BK-FND-00-0025": "簿記の記録過程では、取引を借方・貸方に分けて記録するのが {{c1::仕訳}}、科目別の集計単位が {{c1::勘定}}、仕訳を各勘定へ移すのが {{c1::転記}} である。",
    "BK-FND-00-0026": "勘定残高では、借方合計が貸方合計を上回ると {{c1::借}}方残高、貸方合計が上回ると {{c1::貸}}方残高となる。",
    "BK-FND-00-0027": "会計期間の表記では、「X年Y月期」はY月に {{c1::終わる}} 1年間、「X年度」はX年から {{c1::始まる}} 1年間を表す。",
    "BK-FND-00-0002": "簿記の5要素では、財産や権利は {{c1::資産}}、返済義務は {{c1::負債}}、返済義務のない調達源泉は {{c1::純資産}}、会社の儲けの原因は {{c1::収益}}、収益を得るための消費は {{c1::費用}} に分類する。",
    "BK-FND-00-0004": "5要素の増加の定位置は、資産・費用が {{c1::借}}方、負債・純資産・収益が {{c1::貸}}方で、減少は反対側に記入する。",
    "BK-FND-00-0005": "1つの仕訳では、借方合計と貸方合計が必ず {{c1::一致}} する。",
    "BK-FND-00-0037": "簿記上の取引判定では、火災・盗難で資産が減少すれば簿記上の {{c1::取引}} となる。5要素が変化しない契約締結は、簿記上の取引に {{c1::ならない}}。",
    "BK-FND-00-0009": "簿記の一巡では、{{c1::期首}}手続 → {{c1::期中}}の仕訳・転記 → {{c1::期末}}の試算表・決算 → 財務諸表作成の順で進む。",
    "BK-FND-00-0044": "総勘定元帳の各勘定を集計し、貸借一致を確認する一覧表を {{c1::試算表}} という。",
    "BK-FND-00-0010": "試算表の種類では、借方・貸方の合計を集計するのは {{c1::合計}}試算表、残高を集計するのは {{c1::残高}}試算表、合計と残高を集計するのは {{c1::合計残高}}試算表である。",
    "BK-FND-00-0011": "借貸双方を同額誤記しても、試算表の借方合計と貸方合計は {{c1::一致}} してしまう。",
    "BK-FND-00-0012": "基本的な費用仕訳では、給料100,000円を現金で支払った場合、借方は {{c1::給料}} 100,000円、貸方は {{c1::現金}} 100,000円となる。",
    "BK-FND-00-0047": "費用科目の選択では、電車運賃は {{c1::旅費交通費}}、電話・郵便は {{c1::通信費}}、広告掲載は {{c1::広告宣伝費}} とする。",
    "BK-FND-00-0053": "給与の源泉徴収では、給与は手取額ではなく {{c1::総額}} を費用計上し、控除した所得税は {{c1::所得税預り金}} で処理する。",
    "BK-FND-00-0054": "源泉所得税を税務署へ納付するとき、所得税預り金は {{c1::借}}方に計上する。",
    "BK-FND-00-0055": "社会保険料の給与処理では、従業員負担分は {{c1::社会保険料預り金}}、会社負担分は {{c1::法定福利費}} で処理する。",
    "BK-FND-00-0014": "支払内容・金額が未確定なら {{c1::仮払金}} で処理し、内容確定後は仮払金を {{c1::貸}}方で取り崩す。",
    "BK-FND-00-0058": "入金内容が不明なら {{c1::仮受金}} で処理し、内容判明後は仮受金を {{c1::借}}方で取り崩す。",
    "BK-FND-00-0015": "訂正仕訳では、誤仕訳を取り消す仕訳を {{c1::逆仕訳}} といい、その後に正しい仕訳を行う。",
    "BK-FND-00-0062": "主要簿では、取引を発生順に記録する {{c1::仕訳帳}} と、勘定科目別に記録する {{c1::総勘定元帳}} を使う。転記の参照欄は、仕訳帳の {{c1::元丁}} が転記先、総勘定元帳の {{c1::仕丁}} が転記元を示す。",
    "BK-FND-00-0068": "補助簿では、取引を発生順に記録する {{c1::補助記入帳}} と、対象別に記録する {{c1::補助元帳}} を使う。売掛金元帳は {{c1::得意先}} 別、買掛金元帳は {{c1::仕入先}} 別に管理する。",
    "BK-FND-00-0075": "売掛金・買掛金の補助元帳照合では、総勘定元帳の残高は各補助元帳残高の {{c1::合計}} と一致する。",
    "BK-FND-00-0078": "3伝票制では、現金が増える取引に {{c1::入金}}伝票、現金が減る取引に {{c1::出金}}伝票、現金が増減しない取引に {{c1::振替}}伝票を用いる。入金・出金伝票の科目欄には現金の {{c1::相手科目}} を記入する。",
    "BK-FND-00-0086": "証ひょうの種類では、納品明細は {{c1::納品書}}、請求金額の明細は {{c1::請求書}}、支払の証明は {{c1::領収書}}、当座預金の入出金明細は {{c1::当座勘定照合表}} である。",
    "BK-FND-00-0088": "証ひょうから仕訳を判断するとき、原本・控えは当社の {{c1::立場}} の手掛かりで、証ひょうだけでは {{c1::決済方法}} を確定しない。納品書兼請求書の {{c1::控え}} は販売側の手掛かりとなる。",
}

ALP_OVERRIDES = {
    "BK-FND-00-0062": "ALP-FND-00-0060 ALP-FND-00-0061 ALP-FND-00-0062 ALP-FND-00-0063 ALP-FND-00-0064",
    "BK-FND-00-0068": "ALP-FND-00-0065 ALP-FND-00-0066 ALP-FND-00-0073 ALP-FND-00-0075",
    "BK-FND-00-0078": "ALP-FND-00-0076 ALP-FND-00-0077 ALP-FND-00-0078",
    "BK-FND-00-0088": "ALP-FND-00-0086 ALP-FND-00-0087 ALP-FND-00-0088",
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
        if note_id in ALP_OVERRIDES:
            row["ALP_IDs"] = ALP_OVERRIDES[note_id]

        if old_status == "deprecated" and target_status == "approved" and "ANKI-AUDIT-004でactive direct recallへ復帰" not in row["Extra"]:
            suffix = "ANKI-AUDIT-004で重要度スクリーニングを緩和し、統合されたactive direct recallへ復帰。"
            row["Extra"] = (row["Extra"].rstrip() + " " + suffix).strip()

    with NOTES.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    cloze_re = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
    approved = [r for r in rows if r["Status"] == "approved"]
    cards = sum(len({int(i) for i, _ in cloze_re.findall(r["Text"])}) for r in approved)
    spans = sum(len(cloze_re.findall(r["Text"])) for r in approved)
    active_alps = {alp for r in approved for alp in r["ALP_IDs"].split()}
    print(
        f"FND-00 v1.4 migration applied: approved={len(approved)} "
        f"cards={cards} cloze_spans={spans} active_alps={len(active_alps)}"
    )
    if len(approved) != 29 or cards != 29 or spans != 70 or len(active_alps) != 61:
        raise SystemExit("unexpected v1.4 target metrics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
