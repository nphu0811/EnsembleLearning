"""Read-only artifact acceptance checks, independent of drawing implementation."""
from pathlib import Path
import zipfile,json,csv,hashlib,math,re,subprocess
from lxml import etree
import pymupdf
from pptx import Presentation
O=Path(__file__).resolve().parent;R=O.parents[1]
fail=[];checks=[]
def ck(label,value,detail=None):
 checks.append({'check':label,'pass':bool(value),'detail':detail})
 if not value:fail.append(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=['NCKH_Ensemble_IDS_Final.pptx','NCKH_Ensemble_IDS_Preview.mp4','NCKH_Ensemble_IDS_Static.pdf','Kich_ban_thuyet_trinh_6_phut.md','QnA_4_phut.md','Storyboard.md','Skill_Decision_Matrix.md','Asset_Manifest.md','Scientific_Evidence_Map.md']
for n in files:ck('artifact_exists:'+n,(O/n).is_file() and (O/n).stat().st_size>0)
for path,h in json.loads((O/'audit/protected_sources_sha256.json').read_text()).items():ck('frozen_unchanged:'+path,sha(R/path)==h)
ck('v6_frozen_identity',sha(R/'exports/report_revision_v6_2026_10_19/Bao_cao_NCKH_EnsembleLearning_REVISION_V6.pdf')=='40b35c9a5c7f228ee91bbba94cfb0ccd701d52dd707a6f5b184171412ce6afc3')
p=Presentation(O/'NCKH_Ensemble_IDS_Final.pptx');ck('slide_count32',len(p.slides)==32)
full='\n'.join(q.text for s in p.slides for q in s.shapes if q.has_text_frame)
notes='\n'.join(s.notes_slide.notes_text_frame.text for s in p.slides)
ck('no_unrelated_project_or_placeholders',not re.search(r'neko|lorem|ipsum|<TODO>|click to add|Moyenne|\ufffd',full+'\n'+notes,re.I))
ck('all32_have_notes',all(len(s.notes_slide.notes_text_frame.text.strip())>50 for s in p.slides))
ck('appendix_hidden_only',all(s._element.get('show')=='0' for s in list(p.slides)[20:]) and all(s._element.get('show','1')!='0' for s in list(p.slides)[:20]))
ck('native_editable_not_flattened',sum(q.shape_type==13 for s in p.slides for q in s.shapes)==0 and sum(q.has_text_frame for s in p.slides for q in s.shapes)>200)
bounds=[];duplicate=[]
for i,s in enumerate(p.slides,1):
 names=[q.name for q in s.shapes]
 if len(names)!=len(set(names)):duplicate.append(i)
 for q in s.shapes:
  if q.left<0 or q.top<0 or q.left+q.width>p.slide_width+12700 or q.top+q.height>p.slide_height+12700:bounds.append([i,q.name])
ck('unique_shape_names',not duplicate,duplicate);ck('no_off_canvas_shapes',not bounds,bounds)
with zipfile.ZipFile(O/'NCKH_Ensemble_IDS_Final.pptx') as z:
 ck('zip_crc',z.testzip() is None)
 xml_errors=[]
 for n in z.namelist():
  if n.endswith(('.xml','.rels')):
   try:etree.fromstring(z.read(n))
   except Exception as e:xml_errors.append(n+':'+str(e))
 ck('all_package_xml_parses',not xml_errors,xml_errors)
 morph=[i for i in range(1,21) if b':morph' in z.read(f'ppt/slides/slide{i}.xml')]
 ck('native_morph_present',len(morph)>=10,morph)
 pres=etree.fromstring(z.read('ppt/presProps.xml'))
 ck('main_show_range1to20',bool(pres.xpath('//*[local-name()="sldRg" and @st="1" and @end="20"]')))
 # Slide jump links exist and every internal relationship resolves to an embedded slide.
 all_names=set(z.namelist());targets=[]
 import posixpath
 for n in z.namelist():
  if n.endswith('.rels'):
   doc=etree.fromstring(z.read(n))
   for a in doc:
    if a.get('Type','').endswith('/slide'):
     target=posixpath.normpath(posixpath.join(posixpath.dirname(posixpath.dirname(n)),a.get('Target')))
     targets.append(target in all_names)
 ck('internal_slide_links_resolve',all(targets) and len(targets)>12)
pdf=pymupdf.open(O/'NCKH_Ensemble_IDS_Static.pdf')
ck('static_pdf20_main_keyframes',len(pdf)==20)
# Content-based check: a sparse editable tree diagram legitimately contains
# only 138 text characters. A character-count floor is not a PDF text test.
plan=json.loads((O/'slide_plan.json').read_text(encoding='utf-8'))
compact=lambda s:re.sub(r'\s+','',s)
ck('pdf_selectable_titles',all(compact(plan[i]['title']) in compact(pg.get_text()) for i,pg in enumerate(pdf)))
ck('pdf_vietnamese_and_no_replacement',all('\ufffd' not in x.get_text() for x in pdf))
pdf_bounds=[]
for i,pg in enumerate(pdf,1):
 for w in pg.get_text('words'):
  if w[0]<-.5 or w[1]<-.5 or w[2]>pg.rect.width+.5 or w[3]>pg.rect.height+.5:pdf_bounds.append([i,w[4]])
ck('pdf_word_bounds',not pdf_bounds,pdf_bounds)
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(O/'NCKH_Ensemble_IDS_Preview.mp4')],text=True))
v=[s for s in meta['streams'] if s['codec_type']=='video'];a=[s for s in meta['streams'] if s['codec_type']=='audio']
ck('video_exact_360_seconds',abs(float(meta['format']['duration'])-360)<.05,meta['format']['duration'])
ck('video1080p30_h264',len(v)==1 and v[0]['codec_name']=='h264' and v[0]['width']==1920 and v[0]['height']==1080 and v[0]['r_frame_rate']=='30/1')
ck('audio_aac_present',len(a)==1 and a[0]['codec_name']=='aac' and abs(float(a[0]['duration'])-360)<.05)
ck('native_video_excluded_appendix',json.loads((O/'audit/powerpoint_video_export.json').read_text())['main_slide_count']==20)
ck('full_decode_clean',(O/'audit/full_video_decode.log').is_file() and not (O/'audit/full_video_decode.log').read_text().strip())
timeline=json.loads((O/'timeline.json').read_text())
ck('timeline360_8scenes',timeline[-1]['end']==360 and len(set(x['scene'] for x in timeline))==8)
ck('tts_within_each_slot',all(x['speech_start']>=x['start'] and x['speech_end']<x['end'] for x in timeline))
ck('tts_pause_available',min(x['silence_after'] for x in timeline)>.4,min(x['silence_after'] for x in timeline))
ck('independent_visual_qa_pass','Gate 3 PASS' in (O/'audit/independent_visual_qa.md').read_text(encoding='utf-8'))
vq=json.loads((O/'audit/video_state_inspection.json').read_text())
ck('video_all20_states_in_order',vq['order_pass'])
ck('video_no_stable_appendix_state',vq['appendix_absent_in_stable_states'])
ck('runtime_architecture_and_fn_motion',all(max(vq[k])>1 for k in ['architecture_motion_sample_differences','fn_grow_motion_sample_differences']))
r=subprocess.run(['python',str(R/'tools/p21_verify_full_five_seed.py')],capture_output=True,text=True)
ck('p21_readonly_verifier',r.returncode==0,r.stdout.strip())
result={'status':'PASS' if not fail else 'FAIL','checks_passed':sum(x['pass'] for x in checks),'checks_total':len(checks),'failures':fail,'checks':checks}
(O/'audit/delivery_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
raise SystemExit(1 if fail else 0)
