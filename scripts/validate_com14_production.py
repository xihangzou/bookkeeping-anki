#!/usr/bin/env python3
"""Validate COM-14 production Notes under the current living recall rules."""
from __future__ import annotations
import csv, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NOTES=ROOT/"production"/"notes"/"COM-14.tsv"
INVENTORY=ROOT/"inventory"/"topic_inventory"/"COM-14.tsv"
FIELDS=['ID','Text','Extra','SourceRepo','SourceCommit','SourcePath','Part','Chapter','Section','Topic','Type','ALP_IDs','Difficulty','Tags','Status','QA']
CLOZE_RE=re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE=re.compile(r"^BK-COM-14-[0-9]{4}$")
ALP_RE=re.compile(r"^ALP-COM-14-[0-9]{4}$")
EXPECTED_IDS=[f"BK-COM-14-{n:04d}" for n in range(1,20)]
EXPECTED_SPANS=52
SOURCE=("xihangzou/bookkeeping-integrated","569ed7b82e729334e1472286eaca7c4352e6fbdb","merged/textbook.md")
ALLOWED_TYPES={"definition","classification","recognition","measurement","journal_entry","formula","procedure","comparison","exception","reasoning","ledger","financial_statement","cost_accounting"}
ENTRY_ACCOUNT_RE=re.compile(r"（(?:借|貸)）\{\{c1::([^}]+)\}\}")
FORBIDDEN_COMPACT=("{{c1::（借）","{{c1::（貸）","{{c1::借方：","{{c1::貸方：")
BROAD={"仕訳を行う","仕訳を行わない","処理する","計上する","減少させる","増加させる","あり","なし"}
ARITH=("＝","+","＋","-","－","×","÷","／")
EXPECTED_ALP_MAP={
'BK-COM-14-0001':['ALP-COM-14-0001'],
'BK-COM-14-0002':['ALP-COM-14-0002'],
'BK-COM-14-0003':['ALP-COM-14-0003','ALP-COM-14-0004'],
'BK-COM-14-0004':['ALP-COM-14-0005'],
'BK-COM-14-0005':['ALP-COM-14-0006'],
'BK-COM-14-0006':['ALP-COM-14-0007'],
'BK-COM-14-0007':['ALP-COM-14-0008'],
'BK-COM-14-0008':['ALP-COM-14-0009'],
'BK-COM-14-0009':['ALP-COM-14-0010'],
'BK-COM-14-0010':['ALP-COM-14-0011'],
'BK-COM-14-0011':['ALP-COM-14-0012'],
'BK-COM-14-0012':['ALP-COM-14-0013','ALP-COM-14-0015'],
'BK-COM-14-0013':['ALP-COM-14-0014'],
'BK-COM-14-0014':['ALP-COM-14-0016','ALP-COM-14-0019'],
'BK-COM-14-0015':['ALP-COM-14-0017'],
'BK-COM-14-0016':['ALP-COM-14-0018'],
'BK-COM-14-0017':['ALP-COM-14-0020','ALP-COM-14-0021'],
'BK-COM-14-0018':['ALP-COM-14-0022'],
'BK-COM-14-0019':['ALP-COM-14-0023']}
REQUIRED={
'BK-COM-14-0001':('{{c1::本支店会計}}',),
'BK-COM-14-0002':('{{c1::決算整理}}','その後の{{c1::残高試算表}}'),
'BK-COM-14-0003':('本部側で{{c1::支店}}勘定','営業拠点側で{{c1::本店}}勘定','{{c1::照合勘定}}'),
'BK-COM-14-0004':('残高額が{{c1::同額}}','借貸の側が{{c1::反対}}'),
'BK-COM-14-0005':('まず{{c1::会社全体}}','{{c1::本店}}側・{{c1::支店}}側'),
'BK-COM-14-0006':('本部側：（借）{{c1::支店}}／（貸）{{c1::売掛金}}','回収拠点側：（借）{{c1::現金}}／（貸）{{c1::本店}}'),
'BK-COM-14-0007':('本部側：（借）{{c1::買掛金}}／（貸）{{c1::支店}}','支払拠点側：（借）{{c1::本店}}／（貸）{{c1::現金}}'),
'BK-COM-14-0008':('本部側：（借）{{c1::支店}}／（貸）{{c1::現金}}','現地拠点側：（借）{{c1::営業費}}／（貸）{{c1::本店}}'),
'BK-COM-14-0009':('本部側：（借）{{c1::支店}}／（貸）{{c1::仕入}}','受入拠点側：（借）{{c1::仕入}}／（貸）{{c1::本店}}'),
'BK-COM-14-0010':('本部側＝{{c1::借方}}','営業拠点側＝{{c1::貸方}}','本部側＝{{c1::貸方}}','営業拠点側＝{{c1::借方}}'),
'BK-COM-14-0011':('{{c1::合併財務諸表}}',),
'BK-COM-14-0012':('②{{c1::合算}}','③内部相互勘定の{{c1::相殺消去}}','{{c1::会計帳簿の枠外}}'),
'BK-COM-14-0013':('（借）{{c1::本店}}／（貸）{{c1::支店}}',),
'BK-COM-14-0014':('{{c1::支店分散計算制度}}','{{c1::本店集中計算制度}}'),
'BK-COM-14-0015':('{{c1::相手支店}}勘定','記帳は{{c1::不要}}'),
'BK-COM-14-0016':('{{c1::本店経由}}','{{c1::各支店}}勘定','{{c1::本店}}勘定'),
'BK-COM-14-0017':('{{c1::損益}}勘定','{{c1::総合損益}}勘定'),
'BK-COM-14-0018':('本部側：（借）{{c1::支店}}／（貸）{{c1::総合損益}}','現地拠点側：（借）{{c1::損益}}／（貸）{{c1::本店}}'),
'BK-COM-14-0019':('（借）{{c1::総合損益}}／（貸）{{c1::繰越利益剰余金}}',)}

def main():
    errors=[]
    with NOTES.open(encoding='utf-8',newline='') as f:
        reader=csv.DictReader(f,delimiter='\t'); header=list(reader.fieldnames or []); rows=list(reader)
    with INVENTORY.open(encoding='utf-8',newline='') as f:
        inv=list(csv.DictReader(f,delimiter='\t'))
    if header!=FIELDS: errors.append('header mismatch')
    inc=[r for r in inv if r.get('status')=='INCLUDE']; exc=[r for r in inv if r.get('status')=='EXCLUDE']
    included=[r['alp_id'] for r in inc]; included_set=set(included); inv_by={r['alp_id']:r for r in inc}
    alp_to_notes=defaultdict(list); spans=0; cards=0; ids=[]; rendered=Counter()
    for row in rows:
        nid=row['ID']; ids.append(nid)
        if not NOTE_RE.fullmatch(nid): errors.append(f'{nid}: invalid ID')
        if row['Status']!='approved' or row['QA']!='pass': errors.append(f'{nid}: lifecycle')
        if (row['SourceRepo'],row['SourceCommit'],row['SourcePath'])!=SOURCE: errors.append(f'{nid}: source')
        if row['Part']!='commercial' or row['Chapter']!='14 本支店会計': errors.append(f'{nid}: chapter')
        if row['Type'] not in ALLOWED_TYPES: errors.append(f'{nid}: type')
        if row['Difficulty'] not in {'1','2','3','4','5'}: errors.append(f'{nid}: difficulty')
        tags=sorted(['bookkeeping::commercial','chapter::commercial::14',f"difficulty::{row['Difficulty']}",'status::approved',f"topic::{row['Topic'].strip().replace(' ','_')}",f"type::{row['Type']}"])
        if row['Tags'].split()!=tags: errors.append(f'{nid}: tags')
        text=row['Text']; ms=CLOZE_RE.findall(text); spans+=len(ms); cards+=len({int(i) for i,_ in ms})
        if not ms or {int(i) for i,_ in ms}!={1}: errors.append(f'{nid}: c1-only')
        visible=CLOZE_RE.sub('',text)
        for _,a in ms:
            a=a.strip()
            if len(a)>=2 and a in visible: errors.append(f'{nid}: visible leakage {a!r}')
            if a in BROAD: errors.append(f'{nid}: broad answer {a!r}')
            if any(x in a for x in ('（借）','（貸）','借方：','貸方：')): errors.append(f'{nid}: journal syntax hidden')
            if any(x in a for x in ARITH): errors.append(f'{nid}: operator hidden {a!r}')
        if any(x in text for x in FORBIDDEN_COMPACT): errors.append(f'{nid}: compact entry')
        if ('（借）' in text or '（貸）' in text) and not ENTRY_ACCOUNT_RE.search(text): errors.append(f'{nid}: journal syntax without account-level cloze')
        for req in REQUIRED.get(nid,()):
            if req not in text: errors.append(f'{nid}: missing precision {req!r}')
        rendered[CLOZE_RE.sub('[…]',text)]+=1
        alps=row['ALP_IDs'].split()
        if alps!=EXPECTED_ALP_MAP.get(nid): errors.append(f'{nid}: ALP map')
        for alp in alps:
            if not ALP_RE.fullmatch(alp) or alp not in included_set: errors.append(f'{nid}: invalid ALP {alp}')
            else: alp_to_notes[alp].append(nid)
        if alps and inv_by.get(alps[0]) and row['Section']!=inv_by[alps[0]]['source_section']: errors.append(f'{nid}: section')
    if ids!=EXPECTED_IDS: errors.append('stable IDs/order')
    if len(rows)!=19: errors.append(f'notes={len(rows)}')
    if spans!=EXPECTED_SPANS: errors.append(f'spans={spans}')
    if cards!=19: errors.append(f'cards={cards}')
    if len(included)!=23: errors.append(f'included={len(included)}')
    if len(exc)!=1 or exc[0].get('exclude_reason')!='DECORATIVE_EXAMPLE': errors.append('exclusions')
    for alp in included:
        if len(alp_to_notes[alp])!=1: errors.append(f'{alp} mapped {alp_to_notes[alp]}')
    if any(r.get('note_ids') not in ('',None) or r.get('qa_status')!='pending' for r in inv): errors.append('inventory mutated')
    if any(v>1 for v in rendered.values()): errors.append('duplicate rendered text')
    if errors:
        print('COM-14 production validation: FAIL')
        for e in errors: print('-',e)
        return 1
    multi=sum(len(v)>1 for v in EXPECTED_ALP_MAP.values())
    journals=sum(r['Type']=='journal_entry' for r in rows); formulas=sum(r['Type']=='formula' for r in rows)
    print('COM-14 production validation: PASS')
    print(f'notes={len(rows)} cards={cards} cloze_spans={spans} included_alps={len(included)} mapped={len(included)} unmapped=0')
    print(f'multi_alp_notes={multi} journal_entry_notes={journals} formula_notes={formulas} canonical_exclusions={len(exc)}')
    print('account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass procedure_precision=pass visible_answer_leakage=0 deterministic_order=pass')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
