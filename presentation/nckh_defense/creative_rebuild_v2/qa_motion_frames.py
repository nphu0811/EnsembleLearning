from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
import numpy as np
O=Path(__file__).resolve().parent;D=O/'hero_animations';D.mkdir(exist_ok=True);src=O/'NCKH_Ensemble_IDS_Creative_Preview.mp4'
if not src.exists():src=O/'Creative_native_silent.mp4'
# All times within a single slide; no page transition counted as movement.
clips=[('network',20,20,[3.5,4.2,5.0]),('features',55,20,[1,5,9]),('stacking',150,20,[5,5.6,6.4]),('FP',190,20,[3.4,4.0,4.8]),('FN',210,25,[10,12.7,14.5]),('P21',235,25,[1,4,8]),('cost',310,25,[2,9,16])]
rows=[]
for name,start,duration,times in clips:
 ims=[]
 for j,t in enumerate(times):
  p=D/f'{name}_{j}.jpg';subprocess.run(['ffmpeg','-y','-v','error','-ss',str(start+t),'-i',str(src),'-frames:v','1',str(p)],check=True);ims.append(Image.open(p).convert('RGB'))
 diffs=[float(np.abs(np.asarray(ims[j],float)-np.asarray(ims[j+1],float)).mean()) for j in range(2)]
 strip=Image.new('RGB',(1440,295),'white');dr=ImageDraw.Draw(strip)
 for j,im in enumerate(ims):strip.paste(im.resize((480,270)),(j*480,0));dr.text((j*480+8,274),f'{start+times[j]:.1f}s',fill='black')
 strip.save(D/f'{name}_frames.jpg')
 subprocess.run(['ffmpeg','-y','-v','error','-ss',str(start),'-i',str(src),'-t',str(duration),'-c:v','libx264','-preset','fast','-crf','22','-c:a','aac',str(D/f'{name}.mp4')],check=True)
 rows.append(dict(hero=name,slide_start=start,times=times,mean_absolute_pixel_differences=diffs))
# Concepts are also actual native motion: save same-slide frame strips.
for name in 'ABC':
 ims=[]
 for j,t in enumerate([1.1,2.2,4.3]):
  p=D/f'concept_{name}_{j}.jpg';subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(O/f'concepts/Concept_{name}.mp4'),'-frames:v','1',str(p)],check=True);ims.append(Image.open(p))
 strip=Image.new('RGB',(1440,270))
 for j,im in enumerate(ims):strip.paste(im.resize((480,270)),(j*480,0))
 strip.save(D/f'concept_{name}_frames.jpg')
(O/'audit/motion_frame_evidence.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(rows)
