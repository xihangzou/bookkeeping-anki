#!/usr/bin/env python3
"""Validate COM-10 production Notes under the current living recall rules."""
from __future__ import annotations
import csv, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NOTES=ROOT/"production"/"notes"/"COM-10.tsv"
INVENTORY=ROOT/"inventory"/"topic_inventory"/"COM-10.tsv"
FIELDS=['ID','Text','Extra','SourceRepo','SourceCommit','SourcePath','Part','Chapter','Section','Topic','Type','ALP_IDs','Difficulty','Tags','Status','QA']
CLOZE_RE=re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE=re.compile(r"^BK-COM-10-[0-9]{4}$")
ALP_RE=re.compile(r"^ALP-COM-10-[0-9]{4}$")
EXPECTED_IDS=[f"BK-COM-10-{n:04d}" for n in range(1,32)]
EXPECTED_SPANS=93
SOURCE=("xihangzou/bookkeeping-integrated","569ed7b82e729334e1472286eaca7c4352e6fbdb","merged/textbook.md")
ALLOWED_TYPES={"definition","classification","recognition","measurement","journal_entry","formula","procedure","comparison","exception","reasoning","ledger","financial_statement","cost_accounting"}
ENTRY_ACCOUNT_RE=re.compile(r"（(?:借|貸)）\{\{c1::([^}]+)\}\}")
FORBIDDEN_COMPACT=("{{c1::（借）","{{c1::（貸）","{{c1::借方：","{{c1::貸方：")
BROAD={"仕訳を行う","仕訳を行わない","処理する","計上する","減少させる","増加させる"}
ARITH=("＝","+","＋","-","－","×","÷","／")
EXPECTED_ALP_MAP={
'BK-COM-10-0001':['ALP-COM-10-0001','ALP-COM-10-0002'],'BK-COM-10-0002':['ALP-COM-10-0003'],'BK-COM-10-0003':['ALP-COM-10-0004'],'BK-COM-10-0004':['ALP-COM-10-0005'],'BK-COM-10-0005':['ALP-COM-10-0006'],'BK-COM-10-0006':['ALP-COM-10-0007'],'BK-COM-10-0007':['ALP-COM-10-0008'],'BK-COM-10-0008':['ALP-COM-10-0009'],'BK-COM-10-0009':['ALP-COM-10-0010'],'BK-COM-10-0010':['ALP-COM-10-0011'],'BK-COM-10-0011':['ALP-COM-10-0012','ALP-COM-10-0013'],'BK-COM-10-0012':['ALP-COM-10-0014'],'BK-COM-10-0013':['ALP-COM-10-0015'],'BK-COM-10-0014':['ALP-COM-10-0016'],'BK-COM-10-0015':['ALP-COM-10-0017'],'BK-COM-10-0016':['ALP-COM-10-0018'],'BK-COM-10-0017':['ALP-COM-10-0019'],'BK-COM-10-0018':['ALP-COM-10-0020'],'BK-COM-10-0019':['ALP-COM-10-0021'],'BK-COM-10-0020':['ALP-COM-10-0022'],'BK-COM-10-0021':['ALP-COM-10-0023'],'BK-COM-10-0022':['ALP-COM-10-0024'],'BK-COM-10-0023':['ALP-COM-10-0025'],'BK-COM-10-0024':['ALP-COM-10-0026','ALP-COM-10-0027'],'BK-COM-10-0025':['ALP-COM-10-0028'],'BK-COM-10-0026':['ALP-COM-10-0029'],'BK-COM-10-0027':['ALP-COM-10-0030'],'BK-COM-10-0028':['ALP-COM-10-0031'],'BK-COM-10-0029':['ALP-COM-10-0032'],'BK-COM-10-0030':['ALP-COM-10-0033'],'BK-COM-10-0031':['ALP-COM-10-0034']}
REQUIRED={
'BK-COM-10-0001':('{{c1::株式}}','{{c1::返済義務}}','{{c1::有限責任}}'),'BK-COM-10-0002':('正味財産額＝{{c1::資産}}－{{c1::負債}}',),'BK-COM-10-0007':('（貸）{{c1::資本金}}',),'BK-COM-10-0008':('{{c1::1/2以上}}','{{c1::資本準備金}}'),'BK-COM-10-0009':('（借）{{c1::別段預金}}／（貸）{{c1::株式申込証拠金}}',),'BK-COM-10-0010':('（貸）{{c1::別段預金}}','（借）{{c1::株式申込証拠金}}','{{c1::資本準備金}}'),'BK-COM-10-0011':('{{c1::創立費}}','{{c1::開業費}}','{{c1::株式交付費}}'),'BK-COM-10-0013':('{{c1::元手}}','{{c1::利益剰余金}}','{{c1::不可}}'),'BK-COM-10-0014':('{{c1::資本金}}','{{c1::繰越利益剰余金}}'),'BK-COM-10-0015':('（借）{{c1::繰越利益剰余金}}／（貸）{{c1::損益}}',),'BK-COM-10-0017':('（借）{{c1::資本金}}／（貸）{{c1::繰越利益剰余金}}',),'BK-COM-10-0019':('配当金総額＝{{c1::1株当たり配当額}}×{{c1::発行済株式総数}}',),'BK-COM-10-0020':('（借）{{c1::繰越利益剰余金}}／（貸）{{c1::未払配当金}}','（借）{{c1::未払配当金}}／（貸）当座預金等'),'BK-COM-10-0021':('{{c1::利益準備金}}',),'BK-COM-10-0022':('{{c1::新築積立金}}','{{c1::修繕積立金}}','{{c1::配当平均積立金}}','{{c1::別途積立金}}','（借）{{c1::繰越利益剰余金}}／（貸）{{c1::新築積立金}}','（借）{{c1::新築積立金}}／（貸）{{c1::繰越利益剰余金}}'),'BK-COM-10-0023':('（借）その他資本剰余金／（貸）{{c1::未払配当金}}・{{c1::資本準備金}}',),'BK-COM-10-0024':('必要準備金積立額＝min（{{c1::配当金}}×{{c1::1/10}}, {{c1::資本金}}×{{c1::1/4}}－{{c1::既存準備金合計}}）',),'BK-COM-10-0025':('利益準備金積立額＝{{c1::必要準備金}}×{{c1::利益剰余金財源額}}÷{{c1::配当金総額}}',),'BK-COM-10-0027':('合併時の{{c1::時価}}','（貸）{{c1::現金}}','（貸）{{c1::資本金}}'),'BK-COM-10-0028':('受入純資産額＝{{c1::受入資産時価}}－{{c1::受入負債時価}}',),'BK-COM-10-0029':('のれん＝{{c1::合併対価}}－{{c1::受入純資産額}}',),'BK-COM-10-0030':('{{c1::無形固定資産}}','{{c1::20年}}','{{c1::のれん償却}}'),'BK-COM-10-0031':('（貸）{{c1::負ののれん発生益}}','{{c1::収益}}')}

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
        if row['Part']!='commercial' or row['Chapter']!='10 株式会社会計': errors.append(f'{nid}: chapter')
        if row['Type'] not in ALLOWED_TYPES: errors.append(f'{nid}: type')
        if row['Difficulty'] not in {'1','2','3','4','5'}: errors.append(f'{nid}: difficulty')
        tags=sorted(['bookkeeping::commercial','chapter::commercial::10',f"difficulty::{row['Difficulty']}",'status::approved',f"topic::{row['Topic'].strip().replace(' ','_')}",f"type::{row['Type']}"])
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
        for req in REQUIRED.get(nid,()):
            if req not in text: errors.append(f'{nid}: missing precision {req!r}')
        if row['Type']=='journal_entry' and not ENTRY_ACCOUNT_RE.search(text): errors.append(f'{nid}: missing account-level journal cloze')
        rendered[CLOZE_RE.sub('[…]',text)]+=1
        alps=row['ALP_IDs'].split()
        if alps!=EXPECTED_ALP_MAP.get(nid): errors.append(f'{nid}: ALP map')
        for alp in alps:
            if not ALP_RE.fullmatch(alp) or alp not in included_set: errors.append(f'{nid}: invalid ALP {alp}')
            else: alp_to_notes[alp].append(nid)
        if alps and inv_by.get(alps[0]) and row['Section']!=inv_by[alps[0]]['source_section']: errors.append(f'{nid}: section')
    if ids!=EXPECTED_IDS: errors.append('stable IDs/order')
    if len(rows)!=31: errors.append(f'notes={len(rows)}')
    if spans!=EXPECTED_SPANS: errors.append(f'spans={spans}')
    if len(included)!=34: errors.append(f'included={len(included)}')
    if len(exc)!=1 or exc[0].get('exclude_reason')!='DECORATIVE_EXAMPLE': errors.append('exclusions')
    for alp in included:
        if len(alp_to_notes[alp])!=1: errors.append(f'{alp} mapped {alp_to_notes[alp]}')
    if any(r.get('note_ids') not in ('',None) or r.get('qa_status')!='pending' for r in inv): errors.append('inventory mutated')
    if any(v>1 for v in rendered.values()): errors.append('duplicate rendered text')
    if errors:
        print('COM-10 production validation: FAIL')
        for e in errors: print('-',e)
        return 1
    multi=sum(len(v)>1 for v in EXPECTED_ALP_MAP.values())
    journals=sum(r['Type']=='journal_entry' for r in rows); formulas=sum(r['Type']=='formula' for r in rows)
    print('COM-10 production validation: PASS')
    print(f'notes={len(rows)} cards={len(rows)} cloze_spans={spans} included_alps={len(included)} mapped={len(included)} unmapped=0')
    print(f'multi_alp_notes={multi} journal_entry_notes={journals} formula_notes={formulas} canonical_exclusions={len(exc)}')
    print('account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass formula_atomicity=pass visible_answer_leakage=0 deterministic_order=pass')
    return 0

if __name__=='__main__':
    raise SystemExit(main())