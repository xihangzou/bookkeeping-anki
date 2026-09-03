#!/usr/bin/env python3
from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / 'production' / 'notes' / 'FND-00.tsv'
INV = ROOT / 'inventory' / 'topic_inventory' / 'FND-00.tsv'

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
