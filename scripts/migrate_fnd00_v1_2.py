#!/usr/bin/env python3
"""Apply ANKI-AUDIT-002 FND-00 v1.2 rotation/Cloze migration deterministically.

The migration is idempotent: running it on the already migrated corpus produces
no diff and still verifies the intended 58-card shape.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "production" / "notes" / "FND-00.tsv"
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")

SAME_INDEX_IDS = {
    "BK-FND-00-0003",
    "BK-FND-00-0009",
    "BK-FND-00-0014",
    "BK-FND-00-0017",
    "BK-FND-00-0019",
    "BK-FND-00-0024",
    "BK-FND-00-0025",
    "BK-FND-00-0026",
    "BK-FND-00-0027",
    "BK-FND-00-0039",
    "BK-FND-00-0043",
    "BK-FND-00-0047",
    "BK-FND-00-0048",
    "BK-FND-00-0053",
    "BK-FND-00-0055",
    "BK-FND-00-0058",
    "BK-FND-00-0062",
    "BK-FND-00-0064",
    "BK-FND-00-0074",
    "BK-FND-00-0078",
    "BK-FND-00-0079",
    "BK-FND-00-0090",
    "BK-FND-00-0092",
}

TEXT_OVERRIDES = {
    'BK-FND-00-0010': '各勘定の借方・貸方の合計を集計するのは {{c1::合計試算表}}、各勘定の残高を集計するのは {{c1::残高試算表}}、両方を集計するのは {{c1::合計残高試算表}} である。',
    'BK-FND-00-0011': '試算表の借方合計と貸方合計が一致していても、同額を借貸双方で誤記した誤りは {{c1::試算表では発見できない}}。',
    'BK-FND-00-0015': '訂正仕訳は {{c1::誤仕訳の逆仕訳＋正しい仕訳}} で考える。すでに誤仕訳が存在するため、訂正仕訳そのものは正しい仕訳と同じになるとは限らない。',
    'BK-FND-00-0018': '会社の日々の取引を帳簿へ記帳し、その記録を集約して財務諸表を作成するまでの一連の仕組みを {{c1::簿記}} という。',
    'BK-FND-00-0032': '資金の運用形態を {{c1::資産}}、返済義務のある調達源泉を {{c1::負債}}、返済義務のない調達源泉を {{c1::純資産}} という。',
    'BK-FND-00-0037': '簿記上の取引は、簿記の5要素を増減させる活動・事象である。火災・盗難による資産喪失は {{c1::簿記上の取引}}、5要素が変化しない契約締結だけなら {{c1::簿記上の取引ではない}}。',
    'BK-FND-00-0044': '総勘定元帳の各勘定を集計し、借方合計と貸方合計の一致を確認して転記の正確性を検証する一覧表を {{c1::試算表}} という。',
    'BK-FND-00-0050': '一時的に預かった金額は、預り金を {{c1::貸方}} に計上して増加させ、返金時は預り金を {{c1::借方}} に計上して減少させる。',
    'BK-FND-00-0051': '給料から立替金を控除して回収する場合も、給料は {{c1::総額}} を費用計上し、控除額は {{c1::従業員立替金（または立替金）の回収}} として処理する。',
    'BK-FND-00-0054': '源泉所得税を税務署へ納付するとき、所得税預り金は {{c1::借方}} に計上して減少させ、支払手段は貸方で減少させる。',
    'BK-FND-00-0068': '取引を発生順に記録する補助簿を {{c1::補助記入帳}}、取引先別・品目別など対象別に記録する補助簿を {{c1::補助元帳}} という。',
    'BK-FND-00-0069': '現金出納帳では、前月繰越を {{c1::収入欄}}、次月繰越を {{c1::支出欄}} に記入し、月末は収入・支出の合計を一致させる。',
    'BK-FND-00-0073': '売上帳・仕入帳は各勘定の増減を発生順に記録し、返品があれば {{c1::売上戻り・仕入戻し}} を反映する。',
    'BK-FND-00-0075': '総勘定元帳の売掛金・買掛金残高は、それぞれ {{c1::各補助元帳残高の合計}} と一致する。',
    'BK-FND-00-0080': '一部現金取引には、{{c1::現金部分と非現金部分に分割して起票}} する方法と、{{c1::全額を掛取引とした後に一部現金決済とみなして起票}} する方法がある。',
    'BK-FND-00-0084': '合計転記では、{{c1::総勘定元帳は集計表から合計転記}} し、{{c1::補助元帳は各伝票から個別転記}} する。個別転記は各伝票からその都度行う。',
    'BK-FND-00-0086': '証ひょうは取引内容を示し、仕訳推定の根拠となる。納品した商品等の明細を示すのは {{c1::納品書}}、請求金額の明細は {{c1::請求書}}、支払金額とその内容は {{c1::領収書}}、当座預金の入出金明細は {{c1::当座勘定照合表}} である。',
    'BK-FND-00-0088': '証ひょうから仕訳を推定するとき、原本・控えから判断するのは {{c1::当社の立場}}。一方、{{c1::決済方法は証ひょうだけでは確定しない}} ため、問題文等で確認する。',
    'BK-FND-00-0089': '納品書兼請求書が販売側の手掛かりになるのは {{c1::控え}}。前受金がある場合は、売上時に {{c1::前受金を充当}} する仕訳を検討する。',
    'BK-FND-00-0091': '会計略語では、F/S＝{{c1::財務諸表}}、B/S＝{{c1::貸借対照表}}、P/L＝{{c1::損益計算書}}、S/S＝{{c1::株主資本等変動計算書}}、T/B＝{{c2::試算表}}、前T/B＝{{c2::決算整理前残高試算表}}、後T/B＝{{c2::決算整理後残高試算表}} と対応づける。',
}

FIELDS = [
    "ID", "Text", "Extra", "SourceRepo", "SourceCommit", "SourcePath",
    "Part", "Chapter", "Section", "Topic", "Type", "ALP_IDs",
    "Difficulty", "Tags", "Status", "QA",
]


def main() -> int:
    with NOTES.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        rows = list(reader)
        if list(reader.fieldnames or []) != FIELDS:
            raise SystemExit("FND-00 header mismatch")

    changed = 0
    for row in rows:
        note_id = row["ID"]
        if row["Status"] != "approved":
            continue
        old = row["Text"]
        if note_id in SAME_INDEX_IDS:
            row["Text"] = re.sub(r"\{\{c[1-9][0-9]*::", "{{c1::", row["Text"])
        if note_id in TEXT_OVERRIDES:
            row["Text"] = TEXT_OVERRIDES[note_id]
        if row["Text"] != old:
            changed += 1

    approved = [row for row in rows if row["Status"] == "approved"]
    generated_cards = 0
    for row in approved:
        indices = {int(index) for index, _ in CLOZE_RE.findall(row["Text"])}
        expected = {1, 2} if row["ID"] == "BK-FND-00-0091" else {1}
        if indices != expected:
            raise SystemExit(f"{row['ID']}: migrated indices {sorted(indices)} != {sorted(expected)}")
        generated_cards += len(indices)

    if len(approved) != 57 or generated_cards != 58:
        raise SystemExit(f"unexpected final shape: approved={len(approved)} generated_cards={generated_cards}")

    with NOTES.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"FND-00 v1.2 migration: changed_notes={changed} approved=57 generated_cards=58")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
