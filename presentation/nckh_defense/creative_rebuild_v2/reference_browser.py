"""Isolated Playwright browser fallback: bundled browser runtime missing, no Chrome installed.
Public design pages only; no profile/cookie access, form submissions or auth bypass.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json,time
O=Path(__file__).resolve().parent;D=O/'references';D.mkdir(exist_ok=True)
urls=[('lollypop_designathon','https://lollypop.design/designathon2026/'),('lollypop_home','https://lollypop.design/'),('active_theory','https://activetheory.net/'),('locomotive','https://locomotive.ca/en'),('awwwards','https://www.awwwards.com/'),('behance','https://www.behance.net/search/projects/editorial%20motion')]
ledger=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
 for name,url in urls:
  row={'name':name,'url':url,'screens':[]}
  try:
   r=page.goto(url,wait_until='domcontentloaded',timeout=30000);row['status']=r.status if r else None;page.wait_for_timeout(2200)
   row['title']=page.title();row['text']=page.locator('body').inner_text(timeout=5000)[:20000]
   (D/(name+'_text.txt')).write_text(row['text'],encoding='utf-8')
   for i,scroll in enumerate([0,650,1500,2600] if name.startswith('lollypop') else [0,900]):
    page.evaluate('(y)=>window.scrollTo({top:y,behavior:"smooth"})',scroll);page.wait_for_timeout(1800)
    f=D/f'{name}_{i:02}.png';page.screenshot(path=str(f));row['screens'].append({'path':str(f.relative_to(O)),'scrollY':page.evaluate('window.scrollY')})
   row['visible_styles']=page.locator('h1,h2,h3').evaluate_all('(els)=>els.slice(0,12).map(e=>({text:e.innerText,font:getComputedStyle(e).fontFamily,size:getComputedStyle(e).fontSize,transform:getComputedStyle(e).transform}))')
  except Exception as e:row['error']=str(e)
  ledger.append(row);(D/'browser_ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8');print(name,row.get('status'),row.get('error',''),flush=True)
 browser.close()
