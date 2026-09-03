#!/usr/bin/env python3
from pathlib import Path

path = Path('scripts/validate_fnd00_production.py')
text = path.read_text(encoding='utf-8')
text = text.replace('v1.5 maximal-integration / anti-leak audit', 'v1.6 completeness / itemized-formula audit')
text = text.replace('EXPECTED_CLOZE_SPANS = 120', 'EXPECTED_CLOZE_SPANS = 152')
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
print('patched FND-00 validator for v1.6')
