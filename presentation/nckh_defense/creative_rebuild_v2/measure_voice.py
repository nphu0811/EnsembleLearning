import asyncio,json,hashlib,subprocess
from pathlib import Path
import edge_tts
from creative_content import MAIN
O=Path(__file__).resolve().parent;A=O/'audio';A.mkdir(exist_ok=True)
async def main():
 sem=asyncio.Semaphore(1)
 async def one(i,row):
  scene,sec,view,title,txt=row
  txt=txt.replace('UNSW-NB15','iu en ét đắp, en bê mười lăm')
  p=A/f'slide_{i:02}.mp3';h=p.with_suffix('.sha256');digest=hashlib.sha256(('HoaiMy-5%'+txt).encode()).hexdigest()
  async with sem:
   if not p.exists() or not h.exists() or h.read_text()!=digest:
    for attempt in range(3):
     try:
      await edge_tts.Communicate(txt,'vi-VN-HoaiMyNeural',rate='-5%').save(str(p));h.write_text(digest);print('VOICE',i,flush=True);break
     except Exception:
      if attempt==2:raise
      await asyncio.sleep(2)
  dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],text=True))
  return {'slide':i,'scene':scene,'planned':sec,'speech_seconds':dur,'remaining':sec-dur,'voice':'vi-VN-HoaiMyNeural','rate':'-5%'}
 rows=await asyncio.gather(*(one(i,r) for i,r in enumerate(MAIN,1)))
 (A/'measurements.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps({'total_speech':sum(x['speech_seconds'] for x in rows),'overruns':[x for x in rows if x['remaining']<1.3]}))
asyncio.run(main())
