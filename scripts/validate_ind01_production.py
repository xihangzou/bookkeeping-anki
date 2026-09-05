#!/usr/bin/env python3
"""Validate IND-01 production Notes under the current living recall rules."""
from __future__ import annotations
import csv, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NOTES=ROOT/"production"/"notes"/"IND-01.tsv"
INVENTORY=ROOT/"inventory"/"topic_inventory"/"IND-01.tsv"
FIELDS=['ID','Text','Extra','SourceRepo','SourceCommit','SourcePath','Part','Chapter','Section','Topic','Type','ALP_IDs','Difficulty','Tags','Status','QA']
CLOZE_RE=re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE=re.compile(r"^BK-IND-01-[0-9]{4}$")
ALP_RE=re.compile(r"^ALP-IND-01-[0-9]{4}$")
EXPECTED_IDS=[f"BK-IND-01-{n:04d}" for n in range(1,24)]
EXPECTED_SPANS=59
SOURCE=("xihangzou/bookkeeping-integrated","569ed7b82e729334e1472286eaca7c4352e6fbdb","merged/textbook.md")
ALLOWED_TYPES={"definition","classification","recognition","measurement","journal_entry","formula","procedure","comparison","exception","reasoning","ledger","financial_statement","cost_accounting"}
ENTRY_ACCOUNT_RE=re.compile(r"（(?:借|貸)）\{\{c1::([^}]+)\}\}")
FORBIDDEN_COMPACT=("{{c1::（借）","{{c1::（貸）","{{c1::借方：","{{c1::貸方：")
BROAD={"仕訳を行う","仕訳を行わない","処理する","計上する","減少させる","増加させる","あり","なし"}
ARITH=("＝","+","＋","-","－","×","÷","／")
EXPECTED_ALP_MAP={
'BK-IND-01-0001':['ALP-IND-01-0001'],
'BK-IND-01-0002':['ALP-IND-01-0002'],
'BK-IND-01-0003':['ALP-IND-01-0003'],
'BK-IND-01-0004':['ALP-IND-01-0004'],
'BK-IND-01-0005':['ALP-IND-01-0005'],
'BK-IND-01-0006':['ALP-IND-01-0006'],
'BK-IND-01-0007':['ALP-IND-01-0007'],
'BK-IND-01-0008':['ALP-IND-01-0008'],
'BK-IND-01-0009':['ALP-IND-01-0009','ALP-IND-01-0010','ALP-IND-01-0011','ALP-IND-01-0012'],
'BK-IND-01-0010':['ALP-IND-01-0013'],
'BK-IND-01-0011':['ALP-IND-01-0014'],
'BK-IND-01-0012':['ALP-IND-01-0015','ALP-IND-01-0016'],
'BK-IND-01-0013':['ALP-IND-01-0017'],
'BK-IND-01-0014':['ALP-IND-01-0018'],
'BK-IND-01-0015':['ALP-IND-01-0019','ALP-IND-01-0020','ALP-IND-01-0021'],
'BK-IND-01-0016':['ALP-IND-01-0022'],
'BK-IND-01-0017':['ALP-IND-01-0023'],
'BK-IND-01-0018':['ALP-IND-01-0024','ALP-IND-01-0030'],
'BK-IND-01-0019':['ALP-IND-01-0025'],
'BK-IND-01-0020':['ALP-IND-01-0026'],
'BK-IND-01-0021':['ALP-IND-01-0027'],
'BK-IND-01-0022':['ALP-IND-01-0028'],
'BK-IND-01-0023':['ALP-IND-01-0029']}
REQUIRED={
'BK-IND-01-0001':('{{c1::工業簿記}}','{{c1::製造活動}}'),
'BK-IND-01-0003':('{{c1::原価計算}}','{{c1::工業簿記}}','{{c1::財務諸表}}'),
'BK-IND-01-0004':('{{c1::財務諸表の作成}}',),
'BK-IND-01-0006':('総原価＝{{c1::製造原価}}＋{{c1::販売費及び一般管理費}}',),
'BK-IND-01-0007':('利益＝{{c1::売上高}}－{{c1::総原価}}',),
'BK-IND-01-0009':('材料の消費額＝{{c1::材料費}}','労働力の消費額＝{{c1::労務費}}','これら2区分以外＝{{c1::経費}}'),
'BK-IND-01-0010':('{{c1::製造直接費}}','{{c1::直接材料費}}','{{c1::直接労務費}}','{{c1::直接経費}}'),
'BK-IND-01-0011':('{{c1::製造間接費}}','{{c1::間接材料費}}','{{c1::間接労務費}}','{{c1::間接経費}}'),
'BK-IND-01-0012':('＝{{c1::賦課}}','＝{{c1::配賦}}'),
'BK-IND-01-0013':('製造原価＝{{c1::材料費}}＋{{c1::労務費}}＋{{c1::経費}}＝{{c1::製造直接費}}＋{{c1::製造間接費}}',),
'BK-IND-01-0014':('販売価格＝{{c1::総原価}}＋{{c1::利益}}',),
'BK-IND-01-0015':('{{c1::変動費}}','{{c1::固定費}}'),
'BK-IND-01-0016':('{{c1::財務諸表作成}}','{{c1::利益管理}}','{{c1::原価管理}}'),
'BK-IND-01-0017':('{{c1::原価計算期間}}','{{c1::1か月}}'),
'BK-IND-01-0018':('{{c1::材料}}','{{c1::労務費}}','{{c1::経費}}','直接費を{{c1::仕掛品}}へ賦課','間接費を{{c1::製造間接費}}へ集計後{{c1::仕掛品}}へ配賦','完成時に{{c1::製品}}','販売時に{{c1::売上原価}}'),
'BK-IND-01-0019':('第1次{{c1::費目別計算}}→第2次{{c1::部門別計算}}→第3次{{c1::製品別計算}}',),
'BK-IND-01-0020':('直接費を{{c1::仕掛品}}','間接費を{{c1::製造間接費}}'),
'BK-IND-01-0021':('{{c1::仕掛品}}へ振り替える',),
'BK-IND-01-0022':('{{c1::完成品}}','{{c1::月末仕掛品}}'),
'BK-IND-01-0023':('個別受注生産には{{c1::個別原価計算}}','大量反復生産には{{c1::総合原価計算}}')}

def main():
    errors=[]
    with NOTES.open(encoding='utf-8',newline='') as f:
        reader=csv.DictReader(f,delimiter='\t'); header=list(reader.fieldnames or []); rows=list(reader)
    with INVENTORY.open(encoding='utf-8',newline='') as f:
        inv=list(csv.DictReader(f,delimiter='\t'))
    if header!=FIELDS: errors.append('header mismatch')
    inc=[r for r in inv if r.get('status')=='INCLUDE']; exc=[r for r in inv if r.get('status')=='EXCLUDE']
    included=[r['alp_id'] for r in inc]; included_set=set(included); inv_by={r['alp_id']:r for r in inc}
    alp_to_notes=defaultdict(list); spans=0; ids=[]; rendered=Counter()
    for row in rows:
        nid=row['ID']; ids.append(nid)
        if not NOTE_RE.fullmatch(nid): errors.append(f'{nid}: invalid ID')
        if row['Status']!='approved' or row['QA']!='pass': errors.append(f'{nid}: lifecycle')
        if (row['SourceRepo'],row['SourceCommit'],row['SourcePath'])!=SOURCE: errors.append(f'{nid}: source')
        if row['Part']!='industrial' or row['Chapter']!='1 工業簿記の基礎': errors.append(f'{nid}: chapter')
        if row['Type'] not in ALLOWED_TYPES: errors.append(f'{nid}: type')
        if row['Difficulty'] not in {'1','2','3','4','5'}: errors.append(f'{nid}: difficulty')
        tags=sorted(['bookkeeping::industrial','chapter::industrial::01',f"difficulty::{row['Difficulty']}",'status::approved',f"topic::{row['Topic'].strip().replace(' ','_')}",f"type::{row['Type']}"])
        if row['Tags'].split()!=tags: errors.append(f'{nid}: tags')
        text=row['Text']; ms=CLOZE_RE.findall(text); spans+=len(ms)
        if not ms or {int(i) for i,_ in ms}!={1}: errors.append(f'{nid}: c1-only')
        visible=CLOZE_RE.sub('',text)
        for _,a in ms:
            a=a.strip()
            if len(a)>=2 and a in visible: errors.append(f'{nid}: visible leakage {a!r}')
            if a in BROAD: errors.append(f'{nid}: broad answer {a!r}')
            if '・' in a: errors.append(f'{nid}: parallel phrase should use separate clozes {a!r}')
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
    if len(rows)!=23: errors.append(f'notes={len(rows)}')
    if spans!=EXPECTED_SPANS: errors.append(f'spans={spans}')
    if len(included)!=30: errors.append(f'included={len(included)}')
    if len(exc)!=1 or exc[0].get('exclude_reason')!='DECORATIVE_EXAMPLE': errors.append('exclusions')
    for alp in included:
        if len(alp_to_notes[alp])!=1: errors.append(f'{alp} mapped {alp_to_notes[alp]}')
    if any(r.get('note_ids') not in ('',None) or r.get('qa_status')!='pending' for r in inv): errors.append('inventory mutated')
    if any(v>1 for v in rendered.values()): errors.append('duplicate rendered text')
    if errors:
        print('IND-01 production validation: FAIL')
        for e in errors: print('-',e)
        return 1
    multi=sum(len(v)>1 for v in EXPECTED_ALP_MAP.values())
    formulas=sum(r['Type']=='formula' for r in rows); cost=sum(r['Type']=='cost_accounting' for r in rows)
    print('IND-01 production validation: PASS')
    print(f'notes={len(rows)} cards={len(rows)} cloze_spans={spans} included_alps={len(included)} mapped={len(included)} unmapped=0')
    print(f'multi_alp_notes={multi} formula_notes={formulas} cost_accounting_notes={cost} canonical_exclusions={len(exc)}')
    print('cost_flow=pass formula_atomicity=pass account_level_masking=pass minimal_cloze_scope=pass visible_answer_leakage=0 deterministic_order=pass')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
