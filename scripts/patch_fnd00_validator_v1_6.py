#!/usr/bin/env python3
from pathlib import Path

# First make the permanent migration script itself idempotent with the reviewed final text.
migration = Path('scripts/migrate_fnd00_v1_6.py')
m = migration.read_text(encoding='utf-8')
replacements = {
    '"BK-FND-00-0002": "財務諸表に表示する名称を {{c1::勘定科目}} といい、各科目は5要素のいずれかに分類する。財産や権利は {{c1::資産}}、返済義務は {{c1::負債}}、返済義務のない調達源泉は {{c1::純資産}}。残る2要素は、当期純利益＝{{c1::収益}}－{{c1::費用}} の関係で捉える。",':
    '"BK-FND-00-0002": "簿記の5要素では、財務諸表に表示する名称を {{c1::勘定科目}} といい、各科目はいずれかの要素に分類する。財産や権利は {{c1::資産}}、返済義務は {{c1::負債}}、返済義務のない調達源泉は {{c1::純資産}}。残る2要素は、当期純利益＝{{c1::収益}}－{{c1::費用}} の関係で捉える。",',
    '"BK-FND-00-0009": "会社活動を一定期間に区切って損益・財政状態を把握する単位を {{c1::会計期間}} といい、その最初の {{c1::期首}}手続 → 途中の {{c1::期中}}の仕訳・転記 → 最後の {{c1::期末}}の試算表・決算 → 財務諸表作成の順で進む。この期間の最終日を {{c1::決算日}}、当期の1つ前を {{c1::前期}}、1つ後を {{c1::翌期}} という。",':
    '"BK-FND-00-0009": "会社活動を一定期間に区切る単位を {{c1::会計期間}} といい、損益・財政状態を把握するために用いる。その最初の {{c1::期首}}手続 → 途中の {{c1::期中}}の仕訳・転記 → 最後の {{c1::期末}}の試算表・決算 → 財務諸表作成の順で進む。この期間の最終日を {{c1::決算日}}、当期の1つ前を {{c1::前期}}、1つ後を {{c1::翌期}} という。",',
    '"BK-FND-00-0012": "基本的な費用仕訳では、現金等を支払って給料・諸経費が発生したら、支払内容に応じた費用を {{c1::借}}方に計上する。従業員への給与100,000円を現金で支払った場合、借方は {{c1::給料}} 100,000円、貸方は現金100,000円となる。",':
    '"BK-FND-00-0012": "基本的な費用仕訳では、現金等を支払って給与・諸経費が発生したら、支払内容に応じた費用を {{c1::借}}方に計上する。従業員への給与100,000円を現金で支払った場合、借方は {{c1::給料}} 100,000円、貸方は現金100,000円となる。",',
    '"BK-FND-00-0048": "立替金・預り金では、回収権の勘定に {{c1::立替金}}・{{c1::従業員立替金}} があり、分類は {{c1::資産}}。返還義務の勘定に {{c1::預り金}}・{{c1::従業員預り金}} があり、分類は {{c1::負債}}。給料日前の前貸しは通常の貸付金ではなく従業員向けの前者で処理し、給与から回収する場合も給与は {{c1::総額}} を費用計上する。後者は受入時に {{c1::貸}}方、返還時に {{c1::借}}方で処理する。",':
    '"BK-FND-00-0048": "立替金・預り金では、一時立替額の回収権は {{c1::資産}} で、従業員向けは {{c1::従業員立替金}} を用いる。一時的な返還義務は {{c1::負債}} で、従業員向けは {{c1::従業員預り金}} を用いる。給料日前の前貸しは通常の貸付金ではなく前者で処理し、給与から回収する場合も給与は {{c1::総額}} を費用計上する。後者は受入時に {{c1::貸}}方、返還時に {{c1::借}}方で処理する。",',
}
for old, new in replacements.items():
    if old in m:
        m = m.replace(old, new)
migration.write_text(m, encoding='utf-8')

# Then patch the production validator for v1.6.
path = Path('scripts/validate_fnd00_production.py')
text = path.read_text(encoding='utf-8')
text = text.replace('v1.5 maximal-integration / anti-leak audit', 'v1.6 completeness / itemized-formula audit')
text = text.replace('EXPECTED_CLOZE_SPANS = 120', 'EXPECTED_CLOZE_SPANS = 150')
text = text.replace('BANNED_ANSWER_PUNCTUATION = set("。、，；;／/→＋+・")', 'BANNED_ANSWER_PUNCTUATION = set("。、，；;／/→＋+・－−-=＝")')
text = text.replace('approved v1.5 Note must use only c1', 'approved v1.6 Note must use only c1')
text = text.replace('FND-00 v1.5 production validation:', 'FND-00 v1.6 production validation:')

marker = 'VISIBLE_CONTEXT_CUES = {'
insert_after = '''CONTENT_REQUIREMENTS = {\n    "BK-FND-00-0002": ("当期純利益＝{{c1::収益}}－{{c1::費用}}",),\n    "BK-FND-00-0047": (\n        "{{c1::給料}}", "{{c1::水道光熱費}}", "{{c1::旅費交通費}}",\n        "{{c1::広告宣伝費}}", "{{c1::消耗品費}}", "{{c1::通信費}}",\n        "{{c1::保険料}}", "{{c1::保管費}}", "{{c1::諸会費}}", "{{c1::雑費}}",\n    ),\n    "BK-FND-00-0062": ("{{c1::標準式}}", "{{c1::残高式}}", "日付・摘要・{{c1::仕丁}}・借方金額・貸方金額"),\n    "BK-FND-00-0075": (\n        "純売上高＝{{c1::総売上高}}－{{c1::売上戻り高}}",\n        "純仕入高＝{{c1::総仕入高}}－{{c1::仕入戻り高}}",\n    ),\n    "BK-FND-00-0084": ("各伝票から{{c1::個別転記}}する",),\n}\n\n'''
if 'CONTENT_REQUIREMENTS = {' not in text:
    text = text.replace(marker, insert_after + marker)

needle = '''            if note_id == "BK-FND-00-0018" and text.startswith("簿記の基本では、"):\n'''
block = '''            for required in CONTENT_REQUIREMENTS.get(note_id, ()):\n                if required not in text:\n                    fail(errors, f"{note_id}: required v1.6 content missing: {required!r}")\n\n'''
if block not in text:
    text = text.replace(needle, block + needle)

path.write_text(text, encoding='utf-8')
print('patched FND-00 migration + validator for v1.6')
