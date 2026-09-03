#!/usr/bin/env python3
"""Apply ANKI-AUDIT-005 FND-00 v1.5 maximal integration / anti-leak migration."""
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

TEXT_OVERRIDES = {
    "BK-FND-00-0018": "会社の取引を記録する媒体を {{c1::帳簿}}、そこへ書き込むことを {{c1::記帳}} といい、取引を記録・集計して財務諸表を作成する仕組みを {{c1::簿記}} という。作成した財務諸表は外部の {{c1::利害関係者}} への報告に用いられ、投資・融資・取引などの {{c1::意思決定}} に利用される。",
    "BK-FND-00-0027": "会計期間の表記では、「X年Y月期」はY月{{c1::に終わる}}1年間、「X年度」はX年{{c1::から始まる}}1年間を表す。",
    "BK-FND-00-0003": "資金調達・運用では、株主から返済義務のない資金を受け取るのが {{c1::出資}}、返済義務のある資金を受け取るのが {{c1::借入}}、他者へ資金を貸すのが {{c1::貸付}}。資金の運用形態は {{c1::資産}}、返済義務のある調達源泉は {{c1::負債}}、返済義務のない調達源泉は {{c1::純資産}}。",
    "BK-FND-00-0002": "簿記の5要素では、財産や権利は {{c1::資産}}、返済義務は {{c1::負債}}、返済義務のない調達源泉は {{c1::純資産}}、会社の儲けの原因は {{c1::収益}}、その獲得のための消費は {{c1::費用}} に分類する。利益が生じる場合、当期純利益＝{{c1::収益－費用}} で求める。",
    "BK-FND-00-0004": "5要素の増加の定位置は、資産・費用が {{c1::借}}方、負債・純資産・収益が {{c1::貸}}方で、減少は反対側に記入する。これに対応して、B/Sは資産が左、負債・純資産が右、P/Lは費用が左、収益が右に表示される。",
    "BK-FND-00-0025": "簿記の記録過程では、取引を借方・貸方に分ける記録を {{c1::仕訳}}、科目別の集計単位を {{c1::勘定}}、前者を科目別に移すことを {{c1::転記}} という。1つの取引に複数の科目が関係するものを {{c1::複合仕訳}} といい、この移し替えでは取引日・{{c1::相手科目}}・金額を記入し、相手が複数なら {{c1::諸口}} とすることがある。",
    "BK-FND-00-0009": "会社活動を一定期間に区切る単位を {{c1::会計期間}} といい、その最初の {{c1::期首}}手続 → 途中の {{c1::期中}}の仕訳・転記 → 最後の {{c1::期末}}の試算表・決算 → 財務諸表作成の順で進む。この期間の最終日を {{c1::決算日}} という。",
    "BK-FND-00-0037": "簿記上の記録対象の判定では、火災・盗難で資産が減少すれば簿記上の {{c1::取引}} となる。5要素が変化しない契約締結は対象に {{c1::ならない}}。",
    "BK-FND-00-0010": "試算表の種類では、各勘定の借貸それぞれの総額を並べるのが {{c1::合計}}試算表、差額だけを並べるのが {{c1::残高}}試算表、両方を並べるのが {{c1::合計残高}}試算表である。",
    "BK-FND-00-0012": "基本的な費用仕訳では、従業員への給与100,000円を現金で支払った場合、借方は {{c1::給料}} 100,000円、貸方は現金100,000円となる。",
    "BK-FND-00-0054": "立替金は一時立替額の回収権なので {{c1::資産}}、預り金は返還義務なので {{c1::負債}}。預り金は受入時に {{c1::貸}}方、返還・納付時に {{c1::借}}方で処理し、源泉所得税の税務署への納付も後者に当たる。",
    "BK-FND-00-0053": "給与関連では、給料日前の前貸しは {{c1::従業員立替金}} で処理する。給与から前貸し分を回収する場合も給与は {{c1::総額}} を費用計上し、控除した所得税は {{c1::所得税預り金}} で処理する。",
    "BK-FND-00-0055": "社会保険料の給与処理では、従業員負担分は {{c1::社会保険料預り金}}、会社負担分は {{c1::法定福利費}} で処理する。例：給料300,000円から所得税20,000円・社会保険料40,000円を控除して現金支給する場合、現金支払額は {{c1::240,000円}}。",
    "BK-FND-00-0014": "支払内容・金額が未確定なら {{c1::仮払金}} で処理し、内容確定後はこの仮勘定を {{c1::貸}}方で取り崩す。",
    "BK-FND-00-0058": "入金内容が不明なら {{c1::仮受金}} で処理し、内容判明後はこの仮勘定を {{c1::借}}方で取り崩す。",
    "BK-FND-00-0068": "補助簿では、取引を発生順に記録する {{c1::補助記入帳}} と、対象別に記録する {{c1::補助元帳}} を使う。現金出納帳は前月繰越を {{c1::収入}}欄、次月繰越を {{c1::支出}}欄に記入し、当座借越時の当座預金出納帳は {{c1::貸}}方残高となる。小口現金出納帳は一定期間分を {{c1::まとめて}} 仕訳でき、手形記入帳は {{c1::満期日}}・{{c1::支払場所}}・{{c1::てん末}} を追跡する。売掛金元帳は {{c1::得意先}}別、買掛金元帳は {{c1::仕入先}}別に管理し、相手先名を勘定科目とする方法を {{c1::人名勘定}} という。",
    "BK-FND-00-0075": "売上帳・仕入帳では、返品をそれぞれ {{c1::売上戻り}}・{{c1::仕入戻し}} として反映し、純売上高＝{{c1::総売上高－売上戻り高}}、純仕入高＝{{c1::総仕入高－仕入戻り高}} で求める。売掛金・買掛金の補助元帳照合では、総勘定元帳の残高は各補助元帳残高の {{c1::合計}} と一致する。",
    "BK-FND-00-0078": "3伝票制では、現金が増える取引に {{c1::入金}}伝票、減る取引に {{c1::出金}}伝票、増減しない取引に {{c1::振替}}伝票を用いる。現金増減を伴う2種類の伝票の科目欄には現金の {{c1::相手科目}} を記入する。一部現金取引では、{{c1::現金部分}}と{{c1::非現金部分}}に分けて起票する方法と、いったん全額を {{c1::掛け}}取引としてから一部を現金決済する方法がある。",
    "BK-FND-00-0062": "主要簿では、取引を発生順に記録する {{c1::仕訳帳}} と、科目別に記録する {{c1::総勘定元帳}} を使う。前者の参照欄 {{c1::元丁}} は転記先、後者の参照欄 {{c1::仕丁}} は転記元を示す。伝票からその都度転記するのが {{c1::個別}}転記、一定期間分を集計して転記するのが {{c1::合計}}転記。1日・1週・1月単位で用いる表は {{c1::仕訳日計表}}・{{c1::週計表}}・{{c1::月計表}} で、まとめる方法の流れは伝票→{{c1::集計表}}→勘定科目別の主要簿、補助元帳は各伝票からその都度転記する。",
    "BK-FND-00-0088": "証ひょうから仕訳を判断するとき、書類がどちらの当事者側に残るかは当社の {{c1::立場}} の手掛かりで、証ひょうだけでは {{c1::決済方法}} を確定しない。納品書兼請求書の {{c1::控え}} は販売側の手掛かりとなり、領収書や当座勘定照合表では {{c1::摘要}} と {{c1::入出金額}} を組み合わせて取引内容を特定する。",
    "BK-FND-00-0091": "簿記の略語・記号では、F/S＝{{c1::財務諸表}}、B/S＝{{c1::貸借対照表}}、P/L＝{{c1::損益計算書}}、S/S＝{{c1::株主資本等変動計算書}}、T/B＝{{c1::試算表}}、前T/B＝{{c1::決算整理前残高試算表}}、後T/B＝{{c1::決算整理後残高試算表}}、△＝{{c1::マイナス}}、@＝{{c1::単価}} と読む。",
}

ALP_ADDITIONS = {
    "BK-FND-00-0018": {"ALP-FND-00-0002", "ALP-FND-00-0003"},
    "BK-FND-00-0002": {"ALP-FND-00-0015"},
    "BK-FND-00-0004": {"ALP-FND-00-0013", "ALP-FND-00-0014"},
    "BK-FND-00-0003": {"ALP-FND-00-0018"},
    "BK-FND-00-0025": {"ALP-FND-00-0029", "ALP-FND-00-0030", "ALP-FND-00-0031"},
    "BK-FND-00-0009": {"ALP-FND-00-0033", "ALP-FND-00-0034"},
    "BK-FND-00-0054": {"ALP-FND-00-0043", "ALP-FND-00-0045"},
    "BK-FND-00-0053": {"ALP-FND-00-0044", "ALP-FND-00-0046"},
    "BK-FND-00-0055": {"ALP-FND-00-0052"},
    "BK-FND-00-0068": {"ALP-FND-00-0067", "ALP-FND-00-0068", "ALP-FND-00-0069", "ALP-FND-00-0070"},
    "BK-FND-00-0075": {"ALP-FND-00-0071", "ALP-FND-00-0072"},
    "BK-FND-00-0078": {"ALP-FND-00-0079"},
    "BK-FND-00-0062": {"ALP-FND-00-0080", "ALP-FND-00-0081", "ALP-FND-00-0082", "ALP-FND-00-0083"},
    "BK-FND-00-0088": {"ALP-FND-00-0089"},
    "BK-FND-00-0091": {"ALP-FND-00-0091"},
}

REACTIVATE = {"BK-FND-00-0091"}
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")

def alp_key(alp: str) -> int:
    return int(alp.rsplit('-', 1)[1])

def lifecycle_tags(tags: str, status: str) -> str:
    parts = [t for t in tags.split() if not t.startswith('status::')]
    parts.append(f'status::{status}')
    return ' '.join(sorted(set(parts)))

def main() -> int:
    with NOTES.open('r', encoding='utf-8', newline='') as fh:
        reader = csv.DictReader(fh, delimiter='\t')
        rows = list(reader)
        if list(reader.fieldnames or []) != FIELDS:
            raise SystemExit('FND-00 header mismatch')

    by_id = {r['ID']: r for r in rows}
    missing = sorted((set(TEXT_OVERRIDES) | set(ALP_ADDITIONS) | REACTIVATE) - set(by_id))
    if missing:
        raise SystemExit(f'missing IDs: {missing}')

    for note_id, text in TEXT_OVERRIDES.items():
        by_id[note_id]['Text'] = text

    for note_id, additions in ALP_ADDITIONS.items():
        current = set(by_id[note_id]['ALP_IDs'].split())
        by_id[note_id]['ALP_IDs'] = ' '.join(sorted(current | additions, key=alp_key))

    for note_id in REACTIVATE:
        row = by_id[note_id]
        row['Status'] = 'approved'
        row['QA'] = 'pass'
        row['Tags'] = lifecycle_tags(row['Tags'], 'approved')
        if 'ANKI-AUDIT-005' not in row['Extra']:
            row['Extra'] = (row['Extra'].rstrip() + ' ANKI-AUDIT-005で略語・記号を1枚へ統合してactive direct recallへ復帰。').strip()

    with NOTES.open('w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)

    approved = [r for r in rows if r['Status'] == 'approved']
    cards = sum(len({int(i) for i, _ in CLOZE_RE.findall(r['Text'])}) for r in approved)
    spans = sum(len(CLOZE_RE.findall(r['Text'])) for r in approved)
    active_alps = {a for r in approved for a in r['ALP_IDs'].split()}
    print(f'FND-00 v1.5 migration applied: approved={len(approved)} cards={cards} cloze_spans={spans} active_alps={len(active_alps)}')
    if len(approved) != 30 or cards != 30 or spans != 117 or len(active_alps) != 91:
        raise SystemExit('unexpected v1.5 target metrics')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
