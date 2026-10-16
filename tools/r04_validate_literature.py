"""Validate citations, source pointers and unchanged RQ wording for r04 prose."""
import csv
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'proposal/researchwrite/nckh-ids'

def main():
    draft=P/'drafts/sections/tong_quan_luan_cu_r04.md'
    text=draft.read_text(encoding='utf-8')
    with (ROOT/'literature/resume_r04_2026_10_16/legacy_verification_ledger.csv').open(encoding='utf-8-sig') as f:
        records={r['id']:r for r in csv.DictReader(f)}
    required=['L01','L02','L04','L05','L06','L07','L08','L09','L11','L12']
    checks={i+'_metadata_verified':records[i]['metadata_status']=='VERIFIED_METADATA' for i in required}
    paths=list(dict.fromkeys(re.findall(r'`([^`]+)`',text)))
    checks.update({p+'_exists':(ROOT/p).is_file() for p in paths})
    frozen=(ROOT/'notebook/phase01/phase1_frozen_research_design_v1.md').read_text(encoding='utf-8')
    mapped=(P/'06_rq_method_output_gates.md').read_text(encoding='utf-8')
    for i in range(1,6):
        match=re.search(r'^### RQ'+str(i)+r'[^\n]*\n([^\n]+)',frozen,re.M)
        checks['RQ'+str(i)+'_parsed']=match is not None
        checks['RQ'+str(i)+'_unchanged']=bool(match and match[1].strip() in mapped)
    checks['not_final_review_claim']='chưa phải systematic review' in text
    checks['gap_file_matches']=(ROOT/'literature/gap_matrix.md').read_bytes()==(ROOT/'literature/resume_r04_2026_10_16/GAP_MATRIX_R04.md').read_bytes()
    checks['source_read_validation']=json.loads((ROOT/'literature/resume_r04_2026_10_16/reading_validation.json').read_text())['passed']
    out=P/'qa_logs/r04_literature_validation.json'
    out.write_text(json.dumps(dict(checks=checks,passed=all(checks.values()),scope='Source/metadata/RQ and text-boundary checks only; substantive specialist reviews separate'),indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(dict(passed=sum(checks.values()),total=len(checks))))
    if not all(checks.values()):raise SystemExit(1)

if __name__=='__main__':main()
