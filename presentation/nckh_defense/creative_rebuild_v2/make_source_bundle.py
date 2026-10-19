from pathlib import Path
import importlib.util,shutil,json
O=Path(__file__).resolve().parent;R=O.parents[2]
spec=importlib.util.spec_from_file_location('original_content',O.parent/'content.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
p=O/'creative_qna.py';s=p.read_text(encoding='utf-8');metadata=[(title,q,source) for title,q,a,source in m.QA]
if '\nQA_METADATA=' not in s:
 s+='\nQA_METADATA='+repr(metadata)+'\nQA=[(t,q,ANSWERS[i],src) for i,(t,q,src) in enumerate(QA_METADATA)]\n';p.write_text(s,encoding='utf-8')
for n in ['Scientific_Evidence_Map.md','Skill_Decision_Matrix.md']:shutil.copy2(O.parent/n,O/'audit'/('Inherited_'+n))
S=O/'audit/skill_survey_legacy';S.mkdir(exist_ok=True)
for n in ['motion_skill.txt','research-protocol.md','motion-grammar.md','speech-craft.md','craft.md','qa-checklist.md','visual_skill.txt','visual-schema.md','visual_license.txt','pptmaster_license.txt','officecli_license.txt','anatomy.txt','manimgx.txt','manimgx_license.txt','codex_skills.txt','openai_skills.txt','openai_plugins.txt','source_fetch_ledger.json']:
 if (O.parent/'audit'/n).exists():shutil.copy2(O.parent/'audit'/n,S/n)
S=O/'audit/scientific_sources';S.mkdir(exist_ok=True)
for name in json.loads((O.parent/'audit/protected_sources_sha256.json').read_text(encoding='utf-8')):
 src=R/name
 if src.suffix.lower()!='.pdf':shutil.copy2(src,S/src.name)
print('SELF_CONTAINED_METADATA_AND_SNAPSHOTS')
