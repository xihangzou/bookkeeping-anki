#!/usr/bin/env python3
from __future__ import annotations
import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / 'production' / 'notes' / 'FND-00.tsv'
INV = ROOT / 'inventory' / 'topic_inventory' / 'FND-00.tsv'
CLOZE_RE = re.compile(r'\{\{c([1-9][0-9]*)::(.+?)\}\}')

with NOTES.open(encoding='utf-8', newline='') as fh:
    notes = list(csv.DictReader(fh, delimiter='\t'))
with INV.open(encoding='utf-8', newline='') as fh:
    inv = list(csv.DictReader(fh, delimiter='\t'))

included = [r for r in inv if r.get('status') == 'INCLUDE']
active = {a for r in notes if r['Status'] == 'approved' for a in r['ALP_IDs'].split()}
by_alp = defaultdict(list)
for r in notes:
    for a in r['ALP_IDs'].split():
        by_alp[a].append(r)

missing = [r for r in included if r['alp_id'] not in active]
print(f'active={len(active)} inactive={len(missing)} total={len(included)}')
for r in missing:
    alp = r['alp_id']
    print('\n===', alp, '===')
    print('section:', r.get('source_section',''))
    print('topic:', r.get('topic',''))
    for n in by_alp.get(alp, []):
        print('note:', n['ID'], 'status=', n['Status'])
        print('text:', n['Text'])
        print('extra:', n['Extra'])

print('\n=== VISIBLE ANSWER LEAKS (answers length >= 2) ===')
leak_count = 0
for n in notes:
    if n['Status'] != 'approved':
        continue
    matches = CLOZE_RE.findall(n['Text'])
    visible = CLOZE_RE.sub('□', n['Text'])
    leaks = []
    for _, answer in matches:
        answer = answer.strip()
        if len(answer) >= 2 and answer in visible:
            leaks.append(answer)
    if leaks:
        leak_count += 1
        print(n['ID'], '->', sorted(set(leaks)))
        print('visible:', visible)
print('leak_notes=', leak_count)
