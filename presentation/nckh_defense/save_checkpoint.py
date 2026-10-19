from pathlib import Path
import json,hashlib,shutil,csv,zipfile
O=Path(__file__).resolve().parent;R=O.parents[1];M=R/'.research_memory';C=M/'presentation_2026_10_19';C.mkdir(exist_ok=True)
validation=json.loads((O/'audit/delivery_validation.json').read_text(encoding='utf-8'));assert validation['status']=='PASS'
statefile=M/'STATE.json'
if not (C/'STATE_at_entry.json').exists():shutil.copy2(statefile,C/'STATE_at_entry.json')
state=json.loads(statefile.read_text(encoding='utf-8-sig'))
paths=['NCKH_Ensemble_IDS_Final.pptx','NCKH_Ensemble_IDS_Preview.mp4','NCKH_Ensemble_IDS_Static.pdf','Kich_ban_thuyet_trinh_6_phut.md','QnA_4_phut.md','Storyboard.md','Skill_Decision_Matrix.md','Asset_Manifest.md','Scientific_Evidence_Map.md','QA_Report.md','NCKH_Ensemble_IDS_Delivery.zip']
items=[]
for n in paths:
 p=O/n;assert p.is_file();items.append({'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
checkpoint={'date':'2026-10-19','timezone':'Asia/Saigon','task':'DEFENSE_8_SCENES_360S_NATIVE_PPTX_AND_VIDEO','status':'DONE_ARTIFACT_VALIDATED','validation':validation,'artifacts':items,'no_training_or_test_raw_access':True,'next_action':'Human rehearsal using actual presenters and venue projector; no automatic background work.'}
(C/'checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2),encoding='utf-8')
state['last_updated']='2026-10-19';state['local_session_date']='2026-10-19';state['phase']=state.get('phase','')+';DEFENSE_PPTX_VIDEO_360S_ARTIFACT_QA_PASS'
state['current_task']='DEFENSE_DELIVERY_COMPLETE_48_CHECKS_PASS_NATIVE_PPTX_VIDEO_360S'
state.setdefault('completed_tasks',[]).append('DEFENSE_2026_10_19_8_SCENES_360S_NATIVE_PPTX_MP4_PDF_QA48')
state.setdefault('artifact_manifest',[]).extend(items)
state['next_action']='Open presentation/nckh_defense/NCKH_Ensemble_IDS_Preview.mp4 and rehearse with actual presenters; use hidden slides21–32 for Q&A. Do not retrain/tune from these findings.'
state['last_gate_status']='DEFENSE_ARTIFACT_48_OF_48_PASS;INDEPENDENT_STATIC_QA_PASS;HUMAN_VOICE_AND_PROJECTOR_NOT_TESTED'
state['resume_command']='python presentation/nckh_defense/validate_delivery.py'
tmp=M/'STATE.presentation.tmp.json';tmp.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');tmp.replace(statefile)
handoff='''# Presentation checkpoint — 19/10/2026 (latest)

Completed the explicitly requested defense presentation; no model training or raw TEST reads. Outputs in `presentation/nckh_defense/`:
- Editable final PPTX:32slides,20technical keyframes forming8scenes/360s,12hidden Q&A.
- Actual MP4:360.000s1080p30,H.264/AAC,Vietnamese synthetic voice-over; native PowerPoint Morph, FFmpeg timestamp normalization0.996263182845.
-20-page static main PDF; exact script/storyboard/Q&A/evidence/skill/asset/QA docs;112-file ZIP and checksums.
-48/48 artifact checks PASS; independent static QA fixed/rechecked slides2,10,12,13,18.20main stable video states in order, appendix physically excluded.10actual motion sample frames viewed, full decode clean. Six editable text-frame bounds fixed;32render hashes unchanged. See QA_Report.md for honest limits/initial failed checks.

**Resume read-only:** `python presentation/nckh_defense/validate_delivery.py` then open MP4/PPTX. Human next step: rehearse with actual voice and venue projector; do not claim these tests occurred. Native audio is external preview voice-over, not an embedded lecturer recording. UsePowerPoint desktop supportingMorph; static viewers may flatten transitions. A1–A12 on closing or21…32+Enter opens Q&A; notes/doc explain navigation.

Source V6 SHA remains40b35c9a5c7f228ee91bbba94cfb0ccd701d52dd707a6f5b184171412ce6afc3. P9CSV/P21aggregate/protocol/code hashes unchanged. EntrySTATE18/10 was stale relative to V6+fullP21; old phase status retained as history, current task field reflects completed presentation. Do not restart P21 or infer independent external tests. No work continues after the session.

Artifacts+SHA: `.research_memory/presentation_2026_10_19/checkpoint.json`. Build instructions in presentation README; sources content.py/build_deck.py/animate_export.py/finalize_video.py. Avoid overwriting finalized user edits on a future rebuild.

---
Previous handoff preserved below:

'''
hf=M/'HANDOFF.md';hf.write_text(handoff+hf.read_text(encoding='utf-8-sig'),encoding='utf-8')
append={
'TASK_BOARD.md':'\n\n## 19/10/2026 — Defense presentation\nDONE_ARTIFACT_VALIDATED: presentation/nckh_defense/ all10required outputs + code/SVG/ZIP. Evidence: QA_Report.md, audit/delivery_validation.json48/48PASS, audit/independent_visual_qa.md.20mainkeyframes/8scenes360s;12Q&Ahidden. Human rehearsal/projector check remain user follow-through, not a fabricated acceptance.\n',
'DECISIONS.md':'\n\n## 19/10/2026 — Presentation decisions\nUse actual PowerPoint16COM for native Morph and export; no OfficeCLI binary falsely claimed. White/blue native geometry, motionStudio ideas without copiedstylepack. Keep TEST/P21 on separate scenes; costs include selector. MP4 native361.3503s uniformly normalized to360s withFFmpeg, narration unstretched. Editable text frame repair preserves all32renderhashes. No researchresults modified.\n',
'SKILL_USAGE_LOG.md':'\n\n## DEFENSE_2026_10_19\nRead exact local officecli-pptx/morph-ppt/visual-ppt-builder/ppt-masterSKILL.md; Presentations skill+style_guidelines; PDF skill; superpowers using-superpowers+brainstorming; write-like-me. Remote MotionStudioSKILL and research-protocol/motion-grammar/speech-craft/craft/qa-checklist fetched and read. Actual applied techniques: !!Morph names, native shapes, timed voice measurement, independently delegated Gate3visualQA. OfficeCLI not installed/run; PPTMaster integrityguard exit0 surveyed only, exporter not run; Visual local references/scripts missing, remote schema read, not falsely executed. Nature Skills not used this turn. Exact paths, versions, sources, license/dependency caveats and applied-vs-surveyed status in presentation/nckh_defense/Skill_Decision_Matrix.md; QA48/48PASS.\n',
'CHANGELOG.md':'\n\n##19/10/2026 — Defense artifacts\nAdded isolated presentation/nckh_defense/ deliverable workspace with native PPTX/PDF/360s narrated MP4,10requiredproducts, sourceSVG/code, independentQA and checksummedZIP. Preserved scientificresults and originaltemplates. Reconciled staleSTATE against V6/P21 evidence; saved precise handoff.\n'
}
for name,txt in append.items():
 with (M/name).open('a',encoding='utf-8') as f:f.write(txt)
# Check saved current artifacts and ZIP CRC once more; memory itself is not evidence.
for x in items:assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256']
with zipfile.ZipFile(O/'NCKH_Ensemble_IDS_Delivery.zip') as z:assert z.testzip() is None
print(json.dumps({'saved_checkpoint':str(C/'checkpoint.json'),'artifacts':len(items),'status':'PASS'}))
