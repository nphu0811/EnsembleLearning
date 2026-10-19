"""Native Windows PowerPoint rendering; run after build_deck.py. No GUI input."""
import json,time,sys,subprocess
from pathlib import Path
import win32com.client
OUT=Path(__file__).resolve().parent
PLAN=json.loads((OUT/'slide_plan.json').read_text(encoding='utf-8'))
mode=sys.argv[1] if len(sys.argv)>1 else 'prepare'
app=win32com.client.DispatchEx('PowerPoint.Application')
p=None
try:
 p=app.Presentations.Open(str(OUT/'NCKH_Ensemble_IDS_Final.pptx'),False,False,False)
 if mode=='prepare':
  records=[]
  for i in range(1,p.Slides.Count+1):
   s=p.Slides(i);t=s.SlideShowTransition
   if i<=len(PLAN):
    # Morph for within-scene continuity, fade at scene boundaries.
    same=i>1 and PLAN[i-1]['scene']==PLAN[i-2]['scene']
    t.EntryEffect=3954 if same else (0 if i==1 else 1793)
    t.Duration=0.9 if same else .55
    t.AdvanceOnTime=True;t.AdvanceOnClick=True
    # Timing test: 2s+3s dwell +0.9s Morph produced 5.9733s.
    # Incoming transition belongs inside the planned wall-clock slot.
    t.AdvanceTime=PLAN[i-1]['seconds']-(float(t.Duration) if i>1 else 0)
    t.Hidden=False
   else:t.Hidden=True;t.AdvanceOnTime=False;t.AdvanceOnClick=True
   records.append({'slide':i,'entry_effect':t.EntryEffect,'duration':t.Duration,'advance':t.AdvanceTime,'hidden':bool(t.Hidden)})
  settings=p.SlideShowSettings;settings.RangeType=2;settings.StartingSlide=1;settings.EndingSlide=len(PLAN);settings.AdvanceMode=2
  p.Save()
  # Export static all slides, including clearly labelled appendix.
  p.SaveAs(str(OUT/'NCKH_Ensemble_IDS_Static.pdf'),32)
  for i in range(1,p.Slides.Count+1):
   out=OUT/'renders';out.mkdir(exist_ok=True);p.Slides(i).Export(str(out/f'slide_{i:02}.png'),'PNG',1600,900)
  (OUT/'audit/powerpoint_render.json').write_text(json.dumps({'version':app.Version,'slides':p.Slides.Count,'records':records},indent=2),encoding='utf-8')
  print('PREPARED native PowerPoint transitions, PDF and 32 PNGs',flush=True)
 elif mode=='test':
  for i in range(p.Slides.Count,2,-1):p.Slides(i).Delete()
  p.Slides(1).SlideShowTransition.AdvanceTime=2
  p.Slides(2).SlideShowTransition.AdvanceTime=3
  p.Slides(2).SlideShowTransition.Duration=.9
  p.Slides(2).SlideShowTransition.EntryEffect=3954
  dest=OUT/'audit/timing_test.mp4'
  p.CreateVideo(str(dest),True,5,720,30,80)
  while p.CreateVideoStatus in [1,2]:time.sleep(1)
  print(json.dumps({'status':p.CreateVideoStatus,'path':str(dest)}),flush=True)
 elif mode=='video':
  # Physical deletion only in an unsaved in-memory copy; appendix never enters MP4.
  for i in range(p.Slides.Count,len(PLAN),-1):p.Slides(i).Delete()
  p.SlideShowSettings.RangeType=1
  dest=OUT/'intermediate/PowerPoint_native_silent.mp4';dest.parent.mkdir(exist_ok=True)
  p.CreateVideo(str(dest),True,5,1080,30,90)
  start=time.time();last=0
  while p.CreateVideoStatus in [1,2]:
   time.sleep(2)
   elapsed=int(time.time()-start)
   if elapsed-last>=30:print(json.dumps({'export_seconds':elapsed,'status':p.CreateVideoStatus,'bytes':dest.stat().st_size if dest.exists() else 0}),flush=True);last=elapsed
  (OUT/'audit/powerpoint_video_export.json').write_text(json.dumps({'status':p.CreateVideoStatus,'elapsed_seconds':time.time()-start,'version':app.Version,'main_slide_count':p.Slides.Count,'path':str(dest)},indent=2),encoding='utf-8')
  print('VIDEO_STATUS',p.CreateVideoStatus,flush=True)
finally:
 if p is not None:p.Saved=True;p.Close()
 app.Quit()
