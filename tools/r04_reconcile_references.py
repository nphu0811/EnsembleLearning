"""Apply manually reviewed r04 sources; keep unresolved conflicts visible."""
import csv
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'literature/resume_r04_2026_10_16'

def read_csv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def save_csv(path,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    target=OUT/'legacy_verification_ledger.csv'
    if target.exists():
        raise FileExistsError(target)
    rows=read_csv(ROOT/'literature/resume_r03_2026_10_16/legacy_verification_ledger.csv')
    notes={
      'L01':('VERIFIED_METADATA','https://scholarworks.unist.ac.kr/bitstream/201301/49260/2/000621106000011.pdf.pdf','Crossref DOI identity and UNIST publisher-PDF indexed first page agree title, ordered authors, venue, volume39, final2021 and article100357; DOI additionally indexed at the same primary PDF URL (capture7). Online2020 distinct from final2021. Direct PDF JS placeholder; no full-body reading.'),
      'L02':('VERIFIED_METADATA','https://intrusion-detection.distrinet-research.be/WTMC2021/','Crossref and author institutional project page exact BibTeX/IEEE citation agree title, Engelen/Rimmer/Joosen, SPW2021,7-12 and DOI. Captures5/6. Existing selected PDF reading retained; not a whole-paper review.'),
      'L03':('CHECK_SUGGESTED','https://intrusion-detection.distrinet-research.be/CNS2022/index.html','Fresh Crossref and author project BibTeX agree254-262; UNSW coauthor institutional record says254-263 and KU list10 pages. Publisher direct robot check; retain page conflict, do not certify full metadata. DBLP additionally has Timothy M. Lynar vs Crossref Timothy Lynar (middle-name warning); do not silently patch historical entry.'),
      'L09':('VERIFIED_METADATA','https://iris.unicas.it/handle/11580/110014','Crossref agrees title/ordered authors/year/DOI with IRIS indexed author PDF; volume12 and144489-144508 additionally agree with curated DBLP official metadata record (capture10). Direct institutional PDF403; primary full pagination not visually checked. Metadata verification only, no full-paper read.'),
      'L10':('VERIFIED_METADATA','https://ieeexplore.ieee.org/document/10193854/','Crossref plus IEEE publisher indexed record confirm title,journal21(1),finalFeb2024,1190-1212 and DOI. Ordered display names agree IEEE ComSoc digest saved in r03; preserve Crossref family token Heydari, given Shahram Shah. Online25Jul2023 is not final volume year; direct page robot check.'),
      'L12':('VERIFIED_METADATA','https://www.mdpi.com/2073-431X/14/3/82/xml','Crossref and publisher indexed Share and Cite block (capture7) agree full title, ordered authors, Computers2025,14(3),article82 and DOI. DOAJ corroborates. Direct MDPI429; only indexed metadata and selected methods, no whole-paper read.'),
    }
    checks={}
    for row in rows:
        if row['id'] in notes:
            status,url,note=notes[row['id']]
            row.update(metadata_status=status,primary_url=url,note=note,raw_crossref=(OUT/(row['id']+'_crossref.json')).relative_to(ROOT).as_posix())
        msg=json.loads((ROOT/row['raw_crossref']).read_text(encoding='utf-8'))['message']
        checks[row['id']+'_doi_title']=msg['DOI'].lower()==row['doi'].lower() and msg['title'][0]==row['title']
        checks[row['id']+'_volume_pages']=str(msg.get('volume',''))==row['volume'] and str(msg.get('page',''))==row['pages_or_article']
    save_csv(target,rows)
    matrix=read_csv(ROOT/'literature/literature_matrix.csv')
    for item in matrix:
        row=next(r for r in rows if r['id']==item['id'])
        item.update(verification_status=row['metadata_status'],source_url=row['primary_url'],reading_scope=row['reading_scope'],claim_limit=row['note'])
    save_csv(ROOT/'literature/literature_matrix.csv',matrix)
    bib=(ROOT/'literature/resume_r02_2026_10_16/legacy_working_references.bib').read_text(encoding='utf-8')
    entries=re.findall(r'@\w+\{legacyL\d+,.*?\n\}',bib,re.S)
    verified={r['id'] for r in rows if r['metadata_status']=='VERIFIED_METADATA'}
    subset=[e for e in entries if re.search(r'legacy(L\d+)',e)[1] in verified]
    (ROOT/'literature/refs_verified_subset.bib').write_text('% r04 metadata-verified subset; reading/source limits in r04 ledger. L03 unresolved page conflict excluded.\n\n'+'\n\n'.join(subset)+'\n',encoding='utf-8')
    checks.update(unique_12=len({r['doi'] for r in rows})==12,verified_subset_11=len(subset)==len(verified)==11,L03_conflict_not_promoted=next(r for r in rows if r['id']=='L03')['metadata_status']=='CHECK_SUGGESTED',matrix_matches=all(m['verification_status']==next(r for r in rows if r['id']==m['id'])['metadata_status'] for m in matrix))
    result=dict(checks=checks,passed=all(checks.values()),verified=sorted(verified),pending=['L03'],scope='Metadata/identity/bookkeeping; independent source coverage manually reviewed in FIELD_VERIFICATION_REPORT.md; not full-paper or final P18 gate')
    (OUT/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),verified=len(verified),pending=['L03'])))
    if not result['passed']:
        raise SystemExit(1)

if __name__=='__main__':
    main()
