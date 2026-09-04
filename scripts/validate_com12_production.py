#!/usr/bin/env python3
"""Validate COM-12 production Notes under the current living recall rules."""
from __future__ import annotations
import csv, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NOTES=ROOT/"production"/"notes"/"COM-12.tsv"
INVENTORY=ROOT/"inventory"/"topic_inventory"/"COM-12.tsv"
FIELDS=['ID', 'Text', 'Extra', 'SourceRepo', 'SourceCommit', 'SourcePath', 'Part', 'Chapter', 'Section', 'Topic', 'Type', 'ALP_IDs', 'Difficulty', 'Tags', 'Status', 'QA']
CLOZE_RE=re.compile(r"\{\{c([1-9][0-9]*)::(.+?)\}\}")
NOTE_RE=re.compile(r"^BK-COM-12-[0-9]{4}$")
ALP_RE=re.compile(r"^ALP-COM-12-[0-9]{4}$")
EXPECTED_IDS=[f"BK-COM-12-{n:04d}" for n in range(1,32)]
EXPECTED_SPANS=71
SOURCE=("xihangzou/bookkeeping-integrated","569ed7b82e729334e1472286eaca7c4352e6fbdb","merged/textbook.md")
ALLOWED_TYPES={"definition","classification","recognition","measurement","journal_entry","formula","procedure","comparison","exception","reasoning","ledger","financial_statement","cost_accounting"}
ENTRY_ACCOUNT_RE=re.compile(r"（(?:借|貸)）\{\{c1::([^}]+)\}\}")
FORBIDDEN_COMPACT=("{{c1::（借）","{{c1::（貸）","{{c1::借方：","{{c1::貸方：")
BROAD={"仕訳を行う","仕訳を行わない","処理する","計上する","減少させる","増加させる","あり","なし"}
ARITH=("＝","+","＋","-","－","×","÷","／")
EXPECTED_ALP_MAP={
'BK-COM-12-0001':['ALP-COM-12-0001', 'ALP-COM-12-0002'],
'BK-COM-12-0002':['ALP-COM-12-0003'],
'BK-COM-12-0003':['ALP-COM-12-0004'],
'BK-COM-12-0004':['ALP-COM-12-0005'],
'BK-COM-12-0005':['ALP-COM-12-0006'],
'BK-COM-12-0006':['ALP-COM-12-0007'],
'BK-COM-12-0007':['ALP-COM-12-0008'],
'BK-COM-12-0008':['ALP-COM-12-0009'],
'BK-COM-12-0009':['ALP-COM-12-0010'],
'BK-COM-12-0010':['ALP-COM-12-0011'],
'BK-COM-12-0011':['ALP-COM-12-0012'],
'BK-COM-12-0012':['ALP-COM-12-0013'],
'BK-COM-12-0013':['ALP-COM-12-0014', 'ALP-COM-12-0015', 'ALP-COM-12-0016'],
'BK-COM-12-0014':['ALP-COM-12-0017'],
'BK-COM-12-0015':['ALP-COM-12-0018'],
'BK-COM-12-0016':['ALP-COM-12-0019'],
'BK-COM-12-0017':['ALP-COM-12-0020'],
'BK-COM-12-0018':['ALP-COM-12-0021'],
'BK-COM-12-0019':['ALP-COM-12-0022'],
'BK-COM-12-0020':['ALP-COM-12-0023'],
'BK-COM-12-0021':['ALP-COM-12-0024'],
'BK-COM-12-0022':['ALP-COM-12-0025'],
'BK-COM-12-0023':['ALP-COM-12-0026'],
'BK-COM-12-0024':['ALP-COM-12-0027'],
'BK-COM-12-0025':['ALP-COM-12-0028'],
'BK-COM-12-0026':['ALP-COM-12-0029'],
'BK-COM-12-0027':['ALP-COM-12-0030'],
'BK-COM-12-0028':['ALP-COM-12-0031'],
'BK-COM-12-0029':['ALP-COM-12-0032'],
'BK-COM-12-0030':['ALP-COM-12-0033'],
'BK-COM-12-0031':['ALP-COM-12-0034']
}
REQUIRED={
'BK-COM-12-0001':('{{c1::租税公課}}', '{{c1::通信費}}'),
'BK-COM-12-0002':('（借）{{c1::貯蔵品}}／（貸）{{c1::通信費}}', '（借）{{c1::貯蔵品}}／（貸）{{c1::租税公課}}'),
'BK-COM-12-0003':('（借）{{c1::通信費}}／（貸）{{c1::貯蔵品}}', '（借）{{c1::租税公課}}／（貸）{{c1::貯蔵品}}'),
'BK-COM-12-0005':('（借）{{c1::法人税、住民税及び事業税}}', '（貸）{{c1::仮払法人税等}}', '（貸）{{c1::未払法人税等}}'),
'BK-COM-12-0006':('未払法人税等＝{{c1::法人税等確定額}}－中間納付済みの{{c1::仮払法人税等}}',),
'BK-COM-12-0008':('{{c1::仮払消費税}}（資産）', '{{c1::仮受消費税}}（負債）'),
'BK-COM-12-0009':('消費税納付額＝{{c1::仮受消費税}}－{{c1::仮払消費税}}',),
'BK-COM-12-0010':('（借）{{c1::仮受消費税}}／（貸）{{c1::仮払消費税}}、{{c1::未払消費税}}',),
'BK-COM-12-0011':('税引前当期純利益＝{{c1::収益}}－{{c1::費用}}', '課税所得＝{{c1::益金}}－{{c1::損金}}'),
'BK-COM-12-0012':('課税所得＝{{c1::税引前当期純利益}}＋{{c1::加算調整}}－{{c1::減算調整}}',),
'BK-COM-12-0013':('損金不算入→{{c1::加算}}', '損金算入→{{c1::減算}}', '益金不算入→{{c1::減算}}', '益金算入→{{c1::加算}}'),
'BK-COM-12-0015':('発生年度の{{c1::加算}}調整→解消年度の{{c1::減算}}調整', '発生年度の{{c1::減算}}調整→解消年度の{{c1::加算}}調整'),
'BK-COM-12-0016':('{{c1::一時差異}}に適用', '{{c1::永久差異}}には適用しない'),
'BK-COM-12-0018':('{{c1::法人税等調整額}}',),
'BK-COM-12-0019':('損益計算書上の{{c1::法人税等}}',),
'BK-COM-12-0020':('{{c1::繰延税金資産}}', '{{c1::繰延税金負債}}'),
'BK-COM-12-0021':('税効果額＝{{c1::一時差異}}×{{c1::法定実効税率}}',),
'BK-COM-12-0022':('（借）{{c1::繰延税金資産}}／（貸）{{c1::法人税等調整額}}',),
'BK-COM-12-0023':('（借）{{c1::法人税等調整額}}／（貸）{{c1::繰延税金負債}}',),
'BK-COM-12-0024':('（借）{{c1::法人税等調整額}}／（貸）{{c1::繰延税金資産}}', '（借）{{c1::繰延税金負債}}／（貸）{{c1::法人税等調整額}}'),
'BK-COM-12-0025':('{{c1::相殺}}', '{{c1::純額}}'),
'BK-COM-12-0026':('会計上は{{c1::時価評価}}', '税法上は{{c1::時価評価しない}}'),
'BK-COM-12-0027':('{{c1::法人税等調整額}}',),
'BK-COM-12-0028':('（貸）{{c1::繰延税金負債}}', '{{c1::その他有価証券評価差額金}}'),
'BK-COM-12-0029':('（借）{{c1::繰延税金資産}}', '{{c1::その他有価証券評価差額金}}'),
'BK-COM-12-0030':('{{c1::評価差額}}×（1－{{c1::法定実効税率}}）', '{{c1::その他有価証券評価差額金}}'),
'BK-COM-12-0031':('{{c1::洗替方式}}',)
}

def main():
    errors=[]
    with NOTES.open(encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f,delimiter="\t"); header=list(reader.fieldnames or []); rows=list(reader)
    with INVENTORY.open(encoding="utf-8",newline="") as f:
        inv=list(csv.DictReader(f,delimiter="\t"))
    if header!=FIELDS: errors.append("header mismatch")
    inc=[r for r in inv if r.get("status")=="INCLUDE"]; exc=[r for r in inv if r.get("status")=="EXCLUDE"]
    included=[r["alp_id"] for r in inc]; included_set=set(included); inv_by={r["alp_id"]:r for r in inc}
    alp_to_notes=defaultdict(list); spans=0; ids=[]; rendered=Counter()
    for row in rows:
        nid=row["ID"]; ids.append(nid)
        if not NOTE_RE.fullmatch(nid): errors.append(f"{nid}: invalid ID")
        if row["Status"]!="approved" or row["QA"]!="pass": errors.append(f"{nid}: lifecycle")
        if (row["SourceRepo"],row["SourceCommit"],row["SourcePath"])!=SOURCE: errors.append(f"{nid}: source")
        if row["Part"]!="commercial" or row["Chapter"]!="12 税・税効果会計": errors.append(f"{nid}: chapter")
        if row["Type"] not in ALLOWED_TYPES: errors.append(f"{nid}: type")
        if row["Difficulty"] not in {"1","2","3","4","5"}: errors.append(f"{nid}: difficulty")
        tags=sorted(["bookkeeping::commercial","chapter::commercial::12",f"difficulty::{row['Difficulty']}","status::approved",f"topic::{row['Topic'].strip().replace(' ','_')}",f"type::{row['Type']}"])
        if row["Tags"].split()!=tags: errors.append(f"{nid}: tags")
        text=row["Text"]; ms=CLOZE_RE.findall(text); spans+=len(ms)
        if not ms or {int(i) for i,_ in ms}!={1}: errors.append(f"{nid}: c1-only")
        visible=CLOZE_RE.sub("",text)
        for _,a in ms:
            a=a.strip()
            if len(a)>=2 and a in visible: errors.append(f"{nid}: visible leakage {a!r}")
            if a in BROAD: errors.append(f"{nid}: broad answer {a!r}")
            if any(x in a for x in ("（借）","（貸）","借方：","貸方：")): errors.append(f"{nid}: journal syntax hidden")
            if any(x in a for x in ARITH): errors.append(f"{nid}: operator hidden {a!r}")
        if any(x in text for x in FORBIDDEN_COMPACT): errors.append(f"{nid}: compact entry")
        if ("（借）" in text or "（貸）" in text) and not ENTRY_ACCOUNT_RE.search(text): errors.append(f"{nid}: journal syntax without account-level cloze")
        for req in REQUIRED.get(nid,()):
            if req not in text: errors.append(f"{nid}: missing precision {req!r}")
        rendered[CLOZE_RE.sub("[…]",text)]+=1
        alps=row["ALP_IDs"].split()
        if alps!=EXPECTED_ALP_MAP.get(nid): errors.append(f"{nid}: ALP map")
        for alp in alps:
            if not ALP_RE.fullmatch(alp) or alp not in included_set: errors.append(f"{nid}: invalid ALP {alp}")
            else: alp_to_notes[alp].append(nid)
        if alps and inv_by.get(alps[0]) and row["Section"]!=inv_by[alps[0]]["source_section"]: errors.append(f"{nid}: section")
    if ids!=EXPECTED_IDS: errors.append("stable IDs/order")
    if len(rows)!=31: errors.append(f"notes={len(rows)}")
    if spans!=EXPECTED_SPANS: errors.append(f"spans={spans}")
    if len(included)!=34: errors.append(f"included={len(included)}")
    if len(exc)!=1 or exc[0].get("exclude_reason")!="DECORATIVE_EXAMPLE": errors.append("exclusions")
    for alp in included:
        if len(alp_to_notes[alp])!=1: errors.append(f"{alp} mapped {alp_to_notes[alp]}")
    if any(r.get("note_ids") not in ("",None) or r.get("qa_status")!="pending" for r in inv): errors.append("inventory mutated")
    if any(v>1 for v in rendered.values()): errors.append("duplicate rendered text")
    if errors:
        print("COM-12 production validation: FAIL")
        for e in errors: print("-",e)
        return 1
    multi=sum(len(v)>1 for v in EXPECTED_ALP_MAP.values())
    journals=sum(r["Type"]=="journal_entry" for r in rows); formulas=sum(r["Type"]=="formula" for r in rows)
    print("COM-12 production validation: PASS")
    print(f"notes={len(rows)} cards={len(rows)} cloze_spans={spans} included_alps={len(included)} mapped={len(included)} unmapped=0")
    print(f"multi_alp_notes={multi} journal_entry_notes={journals} formula_notes={formulas} canonical_exclusions={len(exc)}")
    print("account_level_journal_cloze=pass canonical_label_priority=pass minimal_cloze_scope=pass formula_atomicity=pass visible_answer_leakage=0 deterministic_order=pass")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
