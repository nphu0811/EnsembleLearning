"""Check planned timing and actual evidence pointers, not presentation readiness."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    files=[ROOT/'defense'/name for name in ['Kich_ban_thuyet_trinh.md','Demo_runbook.md','Final_QA_Checklist.md']]
    checks={}
    for path in files:
        text=path.read_text(encoding='utf-8')
        for rel in set(re.findall(r'`([^`]+)`',text)):
            if '/' in rel:checks[path.name+':'+rel]=(ROOT/rel).is_file()
    script=files[0].read_text(encoding='utf-8')
    times=re.findall(r'^\|\d+\.[^|]+\|(\d+):(\d+)\|',script,re.M)
    seconds=sum(int(m)*60+int(s) for m,s in times)
    checks.update(twelve_planned_positions=len(times)==12,planned_twelve_minutes=seconds==720,runbook_actual_blocker='BLOCKED dependency' in files[1].read_text(encoding='utf-8'),checklist_not_release='chưa đạt release' in files[2].read_text(encoding='utf-8'))
    (ROOT/'defense/r04_content_validation.json').write_text(json.dumps(dict(checks=checks,passed=all(checks.values()),planned_duration_seconds=seconds,scope='Planned content/source/timing arithmetic; not PPTX/PDF,render,rehearsal or live inference'),indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),planned_seconds=seconds)))
    if not all(checks.values()):raise SystemExit(1)

if __name__=='__main__':main()
