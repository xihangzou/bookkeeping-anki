#!/usr/bin/env python3
"""Validate COM-13 production Notes under the current living recall rules."""
from __future__ import annotations
import csv, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NOTES=ROOT/"production"/"notes"/"COM-13.tsv"
INVENTORY=ROOT/"inventory"/"topic_inventory"/"COM-13.tsv"
FIELDS=['ID','Text','Extra','SourceRepo','SourceCommit','SourcePath','Part','Chapter','Section','Topic','Type','ALP_IDs','Difficulty','Tags','Status','QA']
CLOZE_RE=re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE=re.compile(r"^BK-COM-13-[0-9]{4}$")
ALP_RE=re.compile(r"^ALP-COM-13-[0-9]{4}$")
CROSS_CHAPTER_ALPS={"ALP-IND-10-0010"}
DEPRECATED_IDS={"BK-COM-13-0017"}
EXPECTED_IDS=[f"BK-COM-13-{n:04d}" for n in range(1,40)]
EXPECTED_SPANS=117
SOURCE=("xihangzou/bookkeeping-integrated","569ed7b82e729334e1472286eaca7c4352e6fbdb","merged/textbook.md")
ALLOWED_TYPES={"definition","classification","recognition","measurement","journal_entry","formula","procedure","comparison","exception","reasoning","ledger","financial_statement","cost_accounting"}
ENTRY_ACCOUNT_RE=re.compile(r"（(?:借|貸)）\{\{c1::([^}]+)\}\}")
FORBIDDEN_COMPACT=("{{c1::（借）","{{c1::（貸）","{{c1::借方：","{{c1::貸方：")
BROAD={"仕訳を行う","仕訳を行わない","処理する","計上する","減少させる","増加させる","あり","なし"}
ARITH=("＝","+","＋","-","－","×","÷","／")
EXPECTED_ALP_MAP={
'BK-COM-13-0001':['ALP-COM-13-0001'],
'BK-COM-13-0002':['ALP-COM-13-0002'],
'BK-COM-13-0003':['ALP-COM-13-0003'],
'BK-COM-13-0004':['ALP-COM-13-0004'],
'BK-COM-13-0005':['ALP-COM-13-0005'],
'BK-COM-13-0006':['ALP-COM-13-0006'],
'BK-COM-13-0007':['ALP-COM-13-0007'],
'BK-COM-13-0008':['ALP-COM-13-0008'],
'BK-COM-13-0009':['ALP-COM-13-0009'],
'BK-COM-13-0010':['ALP-COM-13-0010'],
'BK-COM-13-0011':['ALP-COM-13-0011'],
'BK-COM-13-0012':['ALP-COM-13-0012'],
'BK-COM-13-0013':['ALP-COM-13-0013'],
'BK-COM-13-0014':['ALP-COM-13-0014'],
'BK-COM-13-0015':['ALP-COM-13-0015'],
'BK-COM-13-0016':['ALP-COM-13-0016'],
'BK-COM-13-0017':['ALP-COM-13-0017'],
'BK-COM-13-0018':['ALP-COM-13-0017','ALP-COM-13-0018','ALP-IND-10-0010'],
'BK-COM-13-0019':['ALP-COM-13-0019'],
'BK-COM-13-0020':['ALP-COM-13-0020'],
'BK-COM-13-0021':['ALP-COM-13-0021'],
'BK-COM-13-0022':['ALP-COM-13-0022'],
'BK-COM-13-0023':['ALP-COM-13-0023'],
'BK-COM-13-0024':['ALP-COM-13-0024'],
'BK-COM-13-0025':['ALP-COM-13-0025'],
'BK-COM-13-0026':['ALP-COM-13-0026'],
'BK-COM-13-0027':['ALP-COM-13-0027'],
'BK-COM-13-0028':['ALP-COM-13-0028','ALP-COM-13-0029','ALP-COM-13-0030'],
'BK-COM-13-0029':['ALP-COM-13-0031'],
'BK-COM-13-0030':['ALP-COM-13-0032'],
'BK-COM-13-0031':['ALP-COM-13-0033'],
'BK-COM-13-0032':['ALP-COM-13-0034'],
'BK-COM-13-0033':['ALP-COM-13-0035'],
'BK-COM-13-0034':['ALP-COM-13-0036'],
'BK-COM-13-0035':['ALP-COM-13-0037'],
'BK-COM-13-0036':['ALP-COM-13-0038'],
'BK-COM-13-0037':['ALP-COM-13-0039'],
'BK-COM-13-0038':['ALP-COM-13-0040'],
'BK-COM-13-0039':['ALP-COM-13-0041']}
REQUIRED={
'BK-COM-13-0002':['{{c1::資産}}＝{{c1::負債}}＋{{c1::純資産}}','{{c1::当期純利益}}＝{{c1::収益}}－{{c1::費用}}'],
'BK-COM-13-0004':['{{c1::前T/B}}→{{c1::決算整理}}→{{c1::後T/B}}→{{c1::帳簿締切}}→{{c1::財務諸表作成}}'],
'BK-COM-13-0007':['（借）{{c1::損益}}／（貸）{{c1::繰越利益剰余金}}','（借）{{c1::繰越利益剰余金}}／（貸）{{c1::損益}}'],
'BK-COM-13-0011':['（借）{{c1::前払家賃}}／（貸）{{c1::支払家賃}}','（借）{{c1::受取家賃}}／（貸）{{c1::前受家賃}}'],
'BK-COM-13-0012':['（借）{{c1::支払家賃}}／（貸）{{c1::未払家賃}}','（借）{{c1::未収家賃}}／（貸）{{c1::受取家賃}}'],
'BK-COM-13-0017':['売上総利益＝{{c1::売上高}}－{{c1::売上原価}}'],
'BK-COM-13-0018':['売上総利益＝{{c1::売上高}}－{{c1::売上原価}}','営業利益＝売上総利益－{{c1::販売費及び一般管理費}}'],
'BK-COM-13-0019':['経常利益＝{{c1::営業利益}}＋{{c1::営業外収益}}－{{c1::営業外費用}}'],
'BK-COM-13-0020':['税引前利益＝{{c1::経常利益}}＋{{c1::特別利益}}－{{c1::特別損失}}','当期純利益＝{{c1::税引前当期純利益}}－{{c1::法人税等}}'],
'BK-COM-13-0025':['{{c1::正常営業循環基準}}','{{c1::一年基準}}'],
'BK-COM-13-0028':['1年以内満期→{{c1::有価証券}}','1年超→{{c1::投資有価証券}}','1年以内返済→{{c1::短期借入金}}','1年超→{{c1::長期借入金}}','1年超先対応分→{{c1::長期前払費用}}'],
'BK-COM-13-0031':['{{c1::株主資本等変動計算書（S/S）}}'],
'BK-COM-13-0036':['月次減価償却費＝{{c1::年間見積減価償却費}}÷{{c1::12}}','年度末追加額＝{{c1::年間確定減価償却費}}－{{c1::月次計上済減価償却費}}'],
'BK-COM-13-0038':['（借）{{c1::退職給付費用}}／（貸）{{c1::退職給付引当金}}'],
'BK-COM-13-0039':['（借）{{c1::前払家賃}}／（貸）{{c1::現金}}','（借）{{c1::支払家賃}}／（貸）{{c1::前払家賃}}','再振替仕訳は{{c1::不要}}']}

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
        expected_status='deprecated' if nid in DEPRECATED_IDS else 'approved'
        if row['Status']!=expected_status or row['QA']!='pass': errors.append(f'{nid}: lifecycle')
        if nid in DEPRECATED_IDS and '統合先: BK-COM-13-0018' not in row['Extra']: errors.append(f'{nid}: missing replacement lineage')
        if (row['SourceRepo'],row['SourceCommit'],row['SourcePath'])!=SOURCE: errors.append(f'{nid}: source')
        if row['Part']!='commercial' or row['Chapter']!='13 財務諸表': errors.append(f'{nid}: chapter')
        if row['Type'] not in ALLOWED_TYPES: errors.append(f'{nid}: type')
        if row['Difficulty'] not in {'1','2','3','4','5'}: errors.append(f'{nid}: difficulty')
        tags=sorted(['bookkeeping::commercial','chapter::commercial::13',f"difficulty::{row['Difficulty']}",f'status::{expected_status}',f"topic::{row['Topic'].strip().replace(' ','_')}",f"type::{row['Type']}"] )
        if row['Tags'].split()!=tags: errors.append(f'{nid}: tags')
        text=row['Text']; ms=CLOZE_RE.findall(text); spans+=len(ms)
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
            if alp in included_set and ALP_RE.fullmatch(alp):
                if row['Status']=='approved': alp_to_notes[alp].append(nid)
            elif alp in CROSS_CHAPTER_ALPS:
                pass
            else: errors.append(f'{nid}: invalid ALP {alp}')
        if alps and inv_by.get(alps[0]) and row['Section']!=inv_by[alps[0]]['source_section']: errors.append(f'{nid}: section')
    if ids!=EXPECTED_IDS: errors.append('stable IDs/order')
    if len(rows)!=39: errors.append(f'notes={len(rows)}')
    if spans!=EXPECTED_SPANS: errors.append(f'spans={spans}')
    if len(included)!=41: errors.append(f'included={len(included)}')
    if len(exc)!=1 or exc[0].get('exclude_reason')!='DECORATIVE_EXAMPLE': errors.append('exclusions')
    for alp in included:
        if len(alp_to_notes[alp])!=1: errors.append(f'{alp} mapped {alp_to_notes[alp]}')
    if any(r.get('note_ids') not in ('',None) or r.get('qa_status')!='pending' for r in inv): errors.append('inventory mutated')
    if any(v>1 for v in rendered.values()): errors.append('duplicate rendered text')
    if errors:
        print('COM-13 production validation: FAIL')
        for e in errors: print('-',e)
        return 1
    active=[r for r in rows if r['Status']=='approved']; active_spans=sum(len(CLOZE_RE.findall(r['Text'])) for r in active)
    multi=sum(len(v)>1 for v in EXPECTED_ALP_MAP.values())
    journals=sum(r['Type']=='journal_entry' for r in active); formulas=sum(r['Type']=='formula' for r in active)
    print('COM-13 production validation: PASS')
    print(f'rows={len(rows)} active_notes={len(active)} deprecated_notes={len(rows)-len(active)} active_cards={len(active)} active_cloze_spans={active_spans} included_alps={len(included)} mapped={len(included)} unmapped=0')
    print(f'multi_alp_notes={multi} journal_entry_notes={journals} formula_notes={formulas} canonical_exclusions={len(exc)}')
    print('account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass formula_atomicity=pass visible_answer_leakage=0 deterministic_order=pass')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
