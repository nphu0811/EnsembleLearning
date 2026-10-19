import asyncio, json, subprocess,hashlib
from pathlib import Path
import edge_tts
from content import MAIN
OUT=Path(__file__).resolve().parent; A=OUT/'audio';A.mkdir(exist_ok=True)
def probe(p):
 return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],text=True).strip())
async def main():
 sem=asyncio.Semaphore(3)
 async def one(i,item):
  sc,dur,view,title,spoken=item;p=A/f'slide_{i:02}.mp3'
  async with sem:
   digest=hashlib.sha256(spoken.encode()).hexdigest(); stamp=p.with_suffix('.sha256')
   if not p.exists() or not stamp.exists() or stamp.read_text()!=digest:
    await edge_tts.Communicate(spoken,'vi-VN-NamMinhNeural',rate='-5%').save(str(p));stamp.write_text(digest)
  actual=probe(p)
  return {'slide':i,'scene':sc,'planned_seconds':dur,'voice_seconds':actual,'space_for_transition_and_pause':dur-actual,'rate':'-5%','voice':'vi-VN-NamMinhNeural','path':str(p)}
 rows=await asyncio.gather(*(one(i,x) for i,x in enumerate(MAIN,1)))
 (A/'voice_measurements.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 print(json.dumps({'total_speech_seconds':sum(x['voice_seconds'] for x in rows),'overruns':[x for x in rows if x['space_for_transition_and_pause']<1.5],'segments':len(rows)}))
asyncio.run(main())
