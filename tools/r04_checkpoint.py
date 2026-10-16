"""Checkpoint only declared task artifacts and explain changed hashes."""
import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MEM=ROOT/'.research_memory'

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):
            h.update(chunk)
    return h.hexdigest()

def atomic(path,value):
    temp=path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(value,indent=2,ensure_ascii=False),encoding='utf-8')
    temp.replace(path)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task',required=True)
    parser.add_argument('--status',required=True,choices=['DONE_SCOPED','PARTIAL','BLOCKED'])
    parser.add_argument('--note',required=True)
    parser.add_argument('--next-action',required=True)
    parser.add_argument('--artifact',action='append',default=[])
    args=parser.parse_args()
    session=MEM/'r04'
    session.mkdir(exist_ok=True)
    state_path=MEM/'STATE.json'
    state=json.loads(state_path.read_text(encoding='utf-8'))
    backup=session/'STATE_at_entry.json'
    if not backup.exists():
        backup.write_bytes(state_path.read_bytes())
    target=session/(args.task+'.json')
    if target.exists():
        raise FileExistsError(target)
    declared={}
    for raw in args.artifact:
        path=(ROOT/raw).resolve()
        path.relative_to(ROOT)
        if not path.exists():
            raise FileNotFoundError(path)
        files=[path] if path.is_file() else [p for p in path.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
        for p in files:
            declared[p.relative_to(ROOT).as_posix()]=digest(p)
    mutable={'.research_memory/'+n for n in ['HANDOFF.md','TASK_BOARD.md','SKILL_USAGE_LOG.md','DECISIONS.md','CHANGELOG.md','ISSUE_LOG.md','EVIDENCE_INDEX.csv']}
    changed=[]
    for item in state['artifact_manifest']:
        actual=digest(ROOT/item['path'])
        if actual!=item['sha256']:
            if item['path'] not in declared and item['path'] not in mutable:
                raise ValueError('Undeclared change: '+item['path'])
            changed.append(dict(path=item['path'],before=item['sha256'],after=actual))
    stamp=datetime.now(timezone.utc).isoformat()
    record=dict(task=args.task,status=args.status,note=args.note,timestamp=stamp,artifacts=declared,changed_prior_artifacts=changed,next_action=args.next_action)
    atomic(target,record)
    with (MEM/'TASK_BOARD.md').open('a',encoding='utf-8') as f:
        f.write('\n## r04 '+args.task+'\n\n'+args.status+' — '+args.note+'\n\nEvidence: `.research_memory/r04/'+target.name+'`.\n')
    with (MEM/'CHANGELOG.md').open('a',encoding='utf-8') as f:
        f.write('\nr04 '+args.task+': '+args.note+'\n')
    handoff=MEM/'HANDOFF.md'
    previous=handoff.read_text(encoding='utf-8')
    text='# Checkpoint r04 / '+args.task+' —16/10/2026\n\n'+args.status+': '+args.note+'\n\nEvidence `.research_memory/r04/'+target.name+'`. Next: '+args.next_action+'\n\nPreserve r03 canon/RQs/threshold/data/results. No background work after session. Full r04 ledger and task board are authoritative; older entries below are historical.\n\n---\n\n'
    handoff.write_text(text+previous,encoding='utf-8')
    manifests={i['path']:i for i in state['artifact_manifest']}
    for rel in list(declared)+[target.relative_to(ROOT).as_posix(),backup.relative_to(ROOT).as_posix(),'tools/r04_checkpoint.py']:
        manifests[rel]={'path':rel,'sha256':digest(ROOT/rel)}
    for rel in mutable:
        if (ROOT/rel).is_file():
            manifests[rel]={'path':rel,'sha256':digest(ROOT/rel)}
    evidence=MEM/'EVIDENCE_INDEX.csv'
    with evidence.open('a',encoding='utf-8',newline='') as f:
        w=csv.writer(f)
        for rel,sha in sorted(declared.items()):
            w.writerow([args.task,rel,sha,'Task-scoped artifact check; QA linked in task checkpoint','r04 workspace and actual source/tool results','2026-10-16',args.status])
    manifests['.research_memory/EVIDENCE_INDEX.csv']['sha256']=digest(evidence)
    state.update(last_updated=stamp,session_id='2026-10-16-r04',current_task=args.task,next_action=args.next_action,checkpoint_validation_path=target.relative_to(ROOT).as_posix())
    state['last_gate_status'][args.task]=args.status+': '+args.note
    if args.status=='DONE_SCOPED' and args.task not in state['completed_tasks']:
        state['completed_tasks'].append(args.task)
    state['artifact_manifest']=sorted(manifests.values(),key=lambda i:i['path'])
    atomic(state_path,state)
    count=sum(digest(ROOT/i['path'])==i['sha256'] for i in state['artifact_manifest'])
    assert count==len(manifests)
    print(json.dumps(dict(task=args.task,status=args.status,manifest_pass=count,manifest_total=len(manifests))))

if __name__=='__main__':
    main()
