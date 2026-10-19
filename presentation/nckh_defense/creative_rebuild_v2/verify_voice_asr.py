from pathlib import Path
import json,sys
from faster_whisper import WhisperModel
O=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
m=WhisperModel('base',device='cpu',compute_type='int8',download_root=str(O/'runtime/whisper'))
rows=[]
for i in ([int(x) for x in sys.argv[1:]] or [3,4,8,9,10,11,12,13,14,15,16]):
 segs,info=m.transcribe(str(O/f'audio/slide_{i:02}.mp3'),language='vi',beam_size=3,vad_filter=True)
 text=' '.join(s.text for s in segs);rows.append(dict(slide=i,transcript=text));print(i,text,flush=True)
p=O/'audit/voice_asr.json'
prior={r['slide']:r for r in json.loads(p.read_text(encoding='utf-8'))} if p.exists() else {}
prior.update({r['slide']:r for r in rows})
p.write_text(json.dumps([prior[k] for k in sorted(prior)],ensure_ascii=False,indent=2),encoding='utf-8')
