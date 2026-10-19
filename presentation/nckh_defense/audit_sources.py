from pathlib import Path
import json, hashlib, requests, concurrent.futures, subprocess
import pymupdf

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
AUD=OUT/'audit'; AUD.mkdir(exist_ok=True)
URLS={
 'motion_skill':'https://raw.githubusercontent.com/meiiie/meiiie_skillls/main/motion-pptx-studio/SKILL.md',
 'motion_tree':'https://api.github.com/repos/meiiie/meiiie_skillls/contents/motion-pptx-studio',
 'visual_skill':'https://raw.githubusercontent.com/Clockworkhg/visual-ppt-builder/main/SKILL.md',
 'visual_license':'https://api.github.com/repos/Clockworkhg/visual-ppt-builder/license',
 'pptmaster_license':'https://api.github.com/repos/hugohe3/ppt-master/license',
 'officecli_license':'https://api.github.com/repos/iOfficeAI/OfficeCLI/license',
 'anatomy':'https://skills.wheresryan.sh/anatomy',
 'manimgx':'https://manimgx.academa.ai/',
 'manimgx_license':'https://manimgx.academa.ai/license/',
 'openai_skills':'https://github.com/openai/skills',
 'openai_plugins':'https://github.com/openai/plugins',
 'codex_skills':'https://developers.openai.com/codex/skills',
 'ted':'https://storage.ted.com/tedx/manuals/tedx_speaker_guide.pdf',
 'toastmasters':'https://www.toastmasters.org/Magazine/Magazine%20Issues/2023/Sept/Storytelling%20Tips',
}
def fetch(kv):
 k,u=kv
 try:
  r=requests.get(u,timeout=35); b=r.content; p=AUD/(k+('.pdf' if k=='ted' else '.txt')); p.write_bytes(b)
  return {'id':k,'url':u,'status':r.status_code,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'path':str(p.relative_to(ROOT))}
 except Exception as e:return {'id':k,'url':u,'error':str(e)}
rows=list(concurrent.futures.ThreadPoolExecutor(8).map(fetch,URLS.items()))
(AUD/'source_fetch_ledger.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
source=ROOT/'exports/report_revision_v6_2026_10_19/Bao_cao_NCKH_EnsembleLearning_REVISION_V6.pdf'
d=pymupdf.open(source)
(AUD/'report_v6_extracted.txt').write_text('\n'.join(f'\n[PDF PAGE {i+1}]\n'+p.get_text() for i,p in enumerate(d)),encoding='utf-8')
state=json.loads((ROOT/'.research_memory/STATE.json').read_text(encoding='utf-8-sig'))
manifest=state.get('artifact_manifest',[])
checks=[]
for row in manifest:
 p=ROOT/row['path']; actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
 checks.append({'path':row['path'],'exists':p.is_file(),'sha_matches_stale_state':actual==row.get('sha256')})
(AUD/'entry_state_validation.json').write_text(json.dumps({'state_date':state.get('last_updated'),'note':'STATE is stale; current V6/P21 evidence takes precedence. Historical mismatches are not repaired by overwriting sources.','artifacts':checks,'v6_pages':len(d),'v6_sha256':hashlib.sha256(source.read_bytes()).hexdigest()},indent=2),encoding='utf-8')
r=subprocess.run(['python',str(ROOT/'tools/p21_verify_full_five_seed.py')],capture_output=True,text=True,encoding='utf-8')
(AUD/'p21_verifier.txt').write_text(r.stdout+r.stderr,encoding='utf-8')
print(json.dumps({'fetches':[{k:v for k,v in x.items() if k in ['id','status','error']} for x in rows],'p21_exit':r.returncode,'state_files':len(checks),'v6_pages':len(d)}))
