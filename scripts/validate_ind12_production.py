#!/usr/bin/env python3
"""Validate IND-12 production Notes under the current living recall rules."""
from __future__ import annotations
import csv, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NOTES=ROOT/"production"/"notes"/"IND-12.tsv"
INVENTORY=ROOT/"inventory"/"topic_inventory"/"IND-12.tsv"
FIELDS=['ID','Text','Extra','SourceRepo','SourceCommit','SourcePath','Part','Chapter','Section','Topic','Type','ALP_IDs','Difficulty','Tags','Status','QA']
CLOZE_RE=re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE=re.compile(r"^BK-IND-12-[0-9]{4}$")
ALP_RE=re.compile(r"^ALP-IND-12-[0-9]{4}$")
EXPECTED_IDS=[f"BK-IND-12-{n:04d}" for n in range(1,17)]
EXPECTED_SPANS=51
SOURCE=("xihangzou/bookkeeping-integrated","569ed7b82e729334e1472286eaca7c4352e6fbdb","merged/textbook.md")
ALLOWED_TYPES={"definition","classification","recognition","measurement","journal_entry","formula","procedure","comparison","exception","reasoning","ledger","financial_statement","cost_accounting"}
BROAD={"仕訳を行う","仕訳を行わない","処理する","計上する","減少させる","増加させる","あり","なし"}
FORBIDDEN_BROAD_TARGETS={
    "すべての製造原価",
    "変動製造原価のみ",
    "直接原価計算の固定製造費用化額",
    "直接原価計算営業利益",
    "期首棚卸資産に含まれる製造固定費",
    "期末棚卸資産に含まれる製造固定費",
}
ARITH=("＝","+","＋","-","－","×","÷","／")
EXPECTED_ALP_MAP={
'BK-IND-12-0001':['ALP-IND-12-0001','ALP-IND-12-0002','ALP-IND-12-0006'],
'BK-IND-12-0002':['ALP-IND-12-0003'],
'BK-IND-12-0003':['ALP-IND-12-0004'],
'BK-IND-12-0004':['ALP-IND-12-0005'],
'BK-IND-12-0005':['ALP-IND-12-0007'],
'BK-IND-12-0006':['ALP-IND-12-0008'],
'BK-IND-12-0007':['ALP-IND-12-0009'],
'BK-IND-12-0008':['ALP-IND-12-0010'],
'BK-IND-12-0009':['ALP-IND-12-0011'],
'BK-IND-12-0010':['ALP-IND-12-0012'],
'BK-IND-12-0011':['ALP-IND-12-0013'],
'BK-IND-12-0012':['ALP-IND-12-0014'],
'BK-IND-12-0013':['ALP-IND-12-0015','ALP-IND-12-0019'],
'BK-IND-12-0014':['ALP-IND-12-0016'],
'BK-IND-12-0015':['ALP-IND-12-0017','ALP-IND-12-0018'],
'BK-IND-12-0016':['ALP-IND-12-0020']}
REQUIRED={
'BK-IND-12-0001':('{{c1::すべての}}製造原価','変動製造原価{{c1::のみ}}','{{c1::固定製造原価}}','{{c1::期間原価}}'),
'BK-IND-12-0004':('{{c1::変動費}}','{{c1::固定費}}','{{c1::貢献利益}}','{{c1::営業利益}}'),
'BK-IND-12-0005':('売上原価＝{{c1::期首製品棚卸高}}＋{{c1::当期製品製造原価}}－{{c1::期末製品棚卸高}}',),
'BK-IND-12-0007':('変動売上原価＝{{c1::期首製品棚卸高}}（変動原価）＋{{c1::当期製品製造原価}}（変動原価）－{{c1::期末製品棚卸高}}（変動原価）',),
'BK-IND-12-0008':('変動製造マージン＝{{c1::売上高}}－{{c1::変動売上原価}}',),
'BK-IND-12-0009':('貢献利益＝{{c1::変動製造マージン}}－{{c1::変動販売費}}',),
'BK-IND-12-0010':('営業利益＝{{c1::貢献利益}}－{{c1::固定費}}','{{c1::固定製造原価}}','{{c1::固定販売費及び一般管理費}}'),
'BK-IND-12-0012':('＝{{c1::直接原価計算}}の固定製造費用化額＋{{c1::期首棚卸資産}}に含まれる製造固定費－{{c1::期末棚卸資産}}に含まれる製造固定費',),
'BK-IND-12-0013':('全部原価計算営業利益＝{{c1::直接原価計算}}営業利益－{{c1::期首棚卸資産}}に含まれる製造固定費＋{{c1::期末棚卸資産}}に含まれる製造固定費',),
'BK-IND-12-0014':('全部原価計算営業利益－直接原価計算営業利益＝{{c1::期末棚卸資産}}に含まれる製造固定費－{{c1::期首棚卸資産}}に含まれる製造固定費',),
'BK-IND-12-0016':('{{c1::期末棚卸資産}}','{{c1::加算}}','{{c1::期首棚卸資産}}','{{c1::減算}}')}

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
        if row['Part']!='industrial' or row['Chapter']!='12 直接原価計算': errors.append(f'{nid}: chapter')
        if row['Type'] not in ALLOWED_TYPES: errors.append(f'{nid}: type')
        if row['Difficulty'] not in {'1','2','3','4','5'}: errors.append(f'{nid}: difficulty')
        tags=sorted(['bookkeeping::industrial','chapter::industrial::12',f"difficulty::{row['Difficulty']}",'status::approved',f"topic::{row['Topic'].strip().replace(' ','_')}",f"type::{row['Type']}"])
        if row['Tags'].split()!=tags: errors.append(f'{nid}: tags')
        text=row['Text']; ms=CLOZE_RE.findall(text); spans+=len(ms)
        if not ms or {int(i) for i,_ in ms}!={1}: errors.append(f'{nid}: c1-only')
        visible=CLOZE_RE.sub('',text)
        for _,a in ms:
            a=a.strip()
            if len(a)>=2 and a in visible: errors.append(f'{nid}: visible leakage {a!r}')
            if a in BROAD: errors.append(f'{nid}: broad answer {a!r}')
            if a in FORBIDDEN_BROAD_TARGETS: errors.append(f'{nid}: over-broad target {a!r}')
            if '・' in a: errors.append(f'{nid}: parallel phrase should use separate clozes {a!r}')
            if any(x in a for x in ARITH): errors.append(f'{nid}: operator hidden {a!r}')
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
    if len(rows)!=16: errors.append(f'notes={len(rows)}')
    if spans!=EXPECTED_SPANS: errors.append(f'spans={spans}')
    if len(included)!=20: errors.append(f'included={len(included)}')
    if len(exc)!=1 or exc[0].get('exclude_reason')!='DECORATIVE_EXAMPLE': errors.append('exclusions')
    for alp in included:
        if len(alp_to_notes[alp])!=1: errors.append(f'{alp} mapped {alp_to_notes[alp]}')
    if any(r.get('note_ids') not in ('',None) or r.get('qa_status')!='pending' for r in inv): errors.append('inventory mutated')
    if any(v>1 for v in rendered.values()): errors.append('duplicate rendered text')
    if errors:
        print('IND-12 production validation: FAIL')
        for e in errors: print('-',e)
        return 1
    multi=sum(len(v)>1 for v in EXPECTED_ALP_MAP.values())
    formulas=sum(r['Type']=='formula' for r in rows)
    print('IND-12 production validation: PASS')
    print(f'notes={len(rows)} cards={len(rows)} cloze_spans={spans} included_alps={len(included)} mapped={len(included)} unmapped=0')
    print(f'multi_alp_notes={multi} formula_notes={formulas} canonical_exclusions={len(exc)}')
    print('direct_costing_logic=pass fixed_cost_adjustment=pass formula_atomicity=pass minimal_cloze_scope=pass visible_answer_leakage=0 deterministic_order=pass')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
