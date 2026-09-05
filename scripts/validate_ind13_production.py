#!/usr/bin/env python3
"""Validate IND-13 production Notes under the current living recall rules."""
from __future__ import annotations
import csv, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NOTES=ROOT/"production"/"notes"/"IND-13.tsv"
INVENTORY=ROOT/"inventory"/"topic_inventory"/"IND-13.tsv"
FIELDS=['ID','Text','Extra','SourceRepo','SourceCommit','SourcePath','Part','Chapter','Section','Topic','Type','ALP_IDs','Difficulty','Tags','Status','QA']
CLOZE_RE=re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE=re.compile(r"^BK-IND-13-[0-9]{4}$")
ALP_RE=re.compile(r"^ALP-IND-13-[0-9]{4}$")
EXPECTED_IDS=[f"BK-IND-13-{n:04d}" for n in range(1,16)]
EXPECTED_SPANS=55
SOURCE=("xihangzou/bookkeeping-integrated","569ed7b82e729334e1472286eaca7c4352e6fbdb","merged/textbook.md")
ALLOWED_TYPES={"definition","classification","recognition","measurement","journal_entry","formula","procedure","comparison","exception","reasoning","ledger","financial_statement","cost_accounting"}
ARITH=("＝","+","＋","-","－","×","÷","／")
BROAD={"仕訳を行う","仕訳を行わない","処理する","計上する","あり","なし"}
EXPECTED_ALP_MAP={
'BK-IND-13-0001':['ALP-IND-13-0001','ALP-IND-13-0002'],
'BK-IND-13-0002':['ALP-IND-13-0003'],
'BK-IND-13-0003':['ALP-IND-13-0004','ALP-IND-13-0005','ALP-IND-13-0006'],
'BK-IND-13-0004':['ALP-IND-13-0007'],
'BK-IND-13-0005':['ALP-IND-13-0008','ALP-IND-13-0009'],
'BK-IND-13-0006':['ALP-IND-13-0010','ALP-IND-13-0011'],
'BK-IND-13-0007':['ALP-IND-13-0012'],
'BK-IND-13-0008':['ALP-IND-13-0013'],
'BK-IND-13-0009':['ALP-IND-13-0014'],
'BK-IND-13-0010':['ALP-IND-13-0015','ALP-IND-13-0016'],
'BK-IND-13-0011':['ALP-IND-13-0017','ALP-IND-13-0018'],
'BK-IND-13-0012':['ALP-IND-13-0019','ALP-IND-13-0020'],
'BK-IND-13-0013':['ALP-IND-13-0021','ALP-IND-13-0024'],
'BK-IND-13-0014':['ALP-IND-13-0022'],
'BK-IND-13-0015':['ALP-IND-13-0023']}
REQUIRED={
'BK-IND-13-0001':('{{c1::CVP分析}}','{{c1::変動費}}','{{c1::貢献利益}}','{{c1::固定費}}'),
'BK-IND-13-0002':('貢献利益＝{{c1::売上高}}－{{c1::変動費}}＝{{c1::固定費}}＋{{c1::営業利益}}',),
'BK-IND-13-0003':('{{c1::貢献利益率}}＝貢献利益÷売上高','{{c1::変動費率}}＝変動費÷売上高','合計は{{c1::100%}}'),
'BK-IND-13-0004':('営業利益が{{c1::0}}','貢献利益＝{{c1::固定費}}','{{c1::損益分岐点}}'),
'BK-IND-13-0005':('損益分岐点売上高＝{{c1::固定費}}÷{{c1::貢献利益率}}','損益分岐点販売量＝{{c1::固定費}}÷製品単位あたり{{c1::貢献利益}}'),
'BK-IND-13-0006':('必要売上高＝（{{c1::固定費}}＋{{c1::目標営業利益}}）÷{{c1::貢献利益率}}','必要販売量＝（{{c1::固定費}}＋{{c1::目標営業利益}}）÷製品単位あたり{{c1::貢献利益}}'),
'BK-IND-13-0007':('達成売上高＝{{c1::固定費}}÷（{{c1::貢献利益率}}－{{c1::目標営業利益率}}）',),
'BK-IND-13-0008':('損益分岐点比率＝{{c1::損益分岐点売上高}}÷{{c1::予想（計画）売上高}}',),
'BK-IND-13-0009':('安全余裕額＝{{c1::予想（計画）売上高}}－{{c1::損益分岐点売上高}}',),
'BK-IND-13-0010':('安全余裕率＝{{c1::安全余裕額}}÷{{c1::予想（計画）売上高}}＝{{c1::100%}}－{{c1::損益分岐点比率}}','{{c1::安全性}}'),
'BK-IND-13-0011':('経営レバレッジ係数＝{{c1::貢献利益}}÷{{c1::営業利益}}','固定費依存度が高いほど','売上高変化に対する{{c1::営業利益}}の変化'),
'BK-IND-13-0012':('{{c1::固変分解}}','{{c1::勘定科目精査法}}'),
'BK-IND-13-0013':('{{c1::高低点法}}','{{c1::正常操業圏内}}','{{c1::最高操業度点}}','{{c1::最低操業度点}}','{{c1::除外}}'),
'BK-IND-13-0014':('変動費率＝（{{c1::最高操業度時原価}}－{{c1::最低操業度時原価}}）÷（{{c1::最高操業度}}－{{c1::最低操業度}}）',),
'BK-IND-13-0015':('固定費＝いずれかの点の{{c1::原価}}－その点の{{c1::操業度}}×{{c1::変動費率}}',)}

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
        if row['Part']!='industrial' or row['Chapter']!='13 CVP分析': errors.append(f'{nid}: chapter')
        if row['Type'] not in ALLOWED_TYPES: errors.append(f'{nid}: type')
        if row['Difficulty'] not in {'1','2','3','4','5'}: errors.append(f'{nid}: difficulty')
        tags=sorted(['bookkeeping::industrial','chapter::industrial::13',f"difficulty::{row['Difficulty']}",'status::approved',f"topic::{row['Topic'].strip().replace(' ','_')}",f"type::{row['Type']}"])
        if row['Tags'].split()!=tags: errors.append(f'{nid}: tags')
        text=row['Text']; ms=CLOZE_RE.findall(text); spans+=len(ms); cards+=len({int(i) for i,_ in ms})
        if not ms or {int(i) for i,_ in ms}!={1}: errors.append(f'{nid}: c1-only')
        visible=CLOZE_RE.sub('',text)
        for _,a in ms:
            a=a.strip()
            if len(a)>=2 and a in visible: errors.append(f'{nid}: visible leakage {a!r}')
            if a in BROAD: errors.append(f'{nid}: broad answer {a!r}')
            if any(x in a for x in ARITH): errors.append(f'{nid}: operator hidden {a!r}')
            if any(x in a for x in ('・','／','、')): errors.append(f'{nid}: non-atomic parallel answer {a!r}')
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
    if len(rows)!=15: errors.append(f'notes={len(rows)}')
    if spans!=EXPECTED_SPANS: errors.append(f'spans={spans}')
    if cards!=15: errors.append(f'cards={cards}')
    if len(included)!=24: errors.append(f'included={len(included)}')
    if len(exc)!=1 or exc[0].get('exclude_reason')!='DECORATIVE_EXAMPLE': errors.append('exclusions')
    for alp in included:
        if len(alp_to_notes[alp])!=1: errors.append(f'{alp} mapped {alp_to_notes[alp]}')
    if any(r.get('note_ids') not in ('',None) or r.get('qa_status')!='pending' for r in inv): errors.append('inventory mutated')
    if any(v>1 for v in rendered.values()): errors.append('duplicate rendered text')
    if errors:
        print('IND-13 production validation: FAIL')
        for e in errors: print('-',e)
        return 1
    multi=sum(len(v)>1 for v in EXPECTED_ALP_MAP.values())
    formulas=sum(r['Type']=='formula' for r in rows); definitions=sum(r['Type']=='definition' for r in rows)
    print('IND-13 production validation: PASS')
    print(f'notes={len(rows)} cards={cards} cloze_spans={spans} included_alps={len(included)} mapped={len(included)} unmapped=0')
    print(f'multi_alp_notes={multi} formula_notes={formulas} definition_notes={definitions} canonical_exclusions={len(exc)}')
    print('atomic_formula_operands=pass parallel_term_atomicity=pass minimal_cloze_scope=pass visible_answer_leakage=0 duplicate_rendered_text=0 deterministic_order=pass')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
