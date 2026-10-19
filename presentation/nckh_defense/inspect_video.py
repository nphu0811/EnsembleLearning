"""Identify stable slide states and sample actual motion in delivered MP4."""
from pathlib import Path
import json,subprocess
import numpy as np
from PIL import Image,ImageDraw
O=Path(__file__).resolve().parent;F=O/'video_frames';F.mkdir(exist_ok=True)
video=O/'NCKH_Ensemble_IDS_Preview.mp4'
data=subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-vf','fps=5,scale=160:90:flags=area,format=gray','-f','rawvideo','-'])
frames=np.frombuffer(data,np.uint8).reshape(-1,90,160)
refs=np.stack([np.asarray(Image.open(O/f'renders/slide_{i:02}.png').convert('L').resize((160,90),Image.Resampling.BOX),dtype=np.int16) for i in range(1,33)])
labels=[];dist=[]
for f in frames:
 errors=np.mean(np.abs(refs-f.astype(np.int16)),axis=(1,2));labels.append(int(errors.argmin())+1);dist.append(float(errors.min()))
runs=[];start=0
for i in range(1,len(labels)+1):
 if i==len(labels) or labels[i]!=labels[start]:
  runs.append({'slide':labels[start],'start':start/5,'end':i/5,'seconds':(i-start)/5});start=i
stable=[x for x in runs if x['seconds']>=.8]
expected=list(range(1,21));observed=[x['slide'] for x in stable]
timing=json.loads((O/'timeline.json').read_text())
deltas=[{'slide':x['slide'],'actual_state_change':x['start'],'planned_slot_start':timing[x['slide']-1]['start'],'difference':round(x['start']-timing[x['slide']-1]['start'],3)} for x in stable if x['slide']<=20]
transient=[x for x in runs if x['slide']>20]
result={'fps_inspected':5,'frames_inspected':len(frames),'stable_runs':stable,'expected_order':expected,'observed_order':observed,'order_pass':observed==expected,'appendix_absent_at_5fps':not any(k>20 for k in labels),'appendix_absent_in_stable_states':not any(x['slide']>20 for x in stable),'transient_nearest_appendix_candidates':transient,'boundary_midpoint_differences':deltas,'note':'Nearest rendered-state classification; blank/partial fade frames can be falsely assigned a sparse appendix. Candidate frames are saved for visual inspection. Midpoint in Morph may lag incoming transition start. Not an audio listening or projector test.'}
for i,r in enumerate(transient):
 subprocess.run(['ffmpeg','-y','-v','error','-ss',str((r['start']+r['end'])/2),'-i',str(video),'-frames:v','1',str(F/f'transient_candidate_{i:02}.jpg')],check=True)
(O/'audit/video_state_inspection.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
# Locate the actual 12→13 FN-grow transition and architecture step 5→6.
for prefix,target in [('fn_grow',13),('architecture',6)]:
 boundary=next(x['start'] for x in stable if x['slide']==target)
 samples=[max(0,boundary-.6),boundary-.3,boundary,boundary+.3,boundary+.6]
 files=[]
 for i,t in enumerate(samples):
  p=F/f'{prefix}_{i}.jpg';subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(video),'-frames:v','1',str(p)],check=True);files.append(p)
 sheet=Image.new('RGB',(1200,730),'white');draw=ImageDraw.Draw(sheet)
 for i,p in enumerate(files):
  im=Image.open(p).resize((600,337));x=(i%2)*600;y=(i//2)*365;sheet.paste(im,(x,y));draw.text((x+10,y+340),f'{samples[i]:.2f}s',fill='black')
 # Five frames need three rows.
 sheet=Image.new('RGB',(1200,1095),'white');draw=ImageDraw.Draw(sheet)
 for i,p in enumerate(files):
  x=(i%2)*600;y=(i//2)*365;sheet.paste(Image.open(p).resize((600,337)),(x,y));draw.text((x+10,y+340),f'{samples[i]:.2f}s',fill='black')
 sheet.save(F/f'{prefix}_motion_sheet.jpg')
 # Runtime image changes in the moving semantic area.
 crop=(0,100,600,270) if prefix=='architecture' else (320,70,580,250)
 arrays=[np.asarray(Image.open(p).resize((600,337)).crop(crop),np.int16) for p in files]
 result[prefix+'_motion_sample_differences']=[float(np.mean(np.abs(a-b))) for a,b in zip(arrays,arrays[1:])]
# Hero sheet shown to user is sampled from final MP4, one image per scene.
sheet=Image.new('RGB',(1600,960),'#eef4fa');draw=ImageDraw.Draw(sheet)
for i in range(8):
 p=F/f'scene_{i+1:02}.jpg';x=(i%2)*800;y=(i//2)*240
 sheet.paste(Image.open(p).resize((800,450)).crop((0,0,800,210)),(x,y)) if False else None
 # Full 16:9 thumbnails, 2 rows ×4 columns.
sheet=Image.new('RGB',(1600,500),'#eef4fa');draw=ImageDraw.Draw(sheet)
for i in range(8):
 x=(i%4)*400;y=(i//4)*250;sheet.paste(Image.open(F/f'scene_{i+1:02}.jpg').resize((400,225)),(x,y));draw.text((x+8,y+230),f'Canh {i+1}',fill='#0d3560')
sheet.save(O/'Preview_8_canh.jpg')
(O/'audit/video_state_inspection.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'order_pass':result['order_pass'],'appendix_absent':result['appendix_absent_at_5fps'],'frames':len(frames),'stable_states':len(stable),'max_midpoint_difference':max(abs(x['difference']) for x in deltas),'motion':{k:v for k,v in result.items() if k.endswith('sample_differences')}}))
