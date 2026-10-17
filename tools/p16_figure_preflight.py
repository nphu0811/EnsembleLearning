"""Run installed Nature figure audits on saved PDFs, retaining every diagnostic."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory',type=Path,required=True)
    parser.add_argument('--skill-scripts',type=Path,required=True)
    parser.add_argument('--out-dir',type=Path,required=True)
    args=parser.parse_args()
    args.out_dir.mkdir(parents=True,exist_ok=False)
    root=Path(__file__).resolve().parents[1]
    inventory=json.loads(args.inventory.read_text(encoding='utf-8'))

    def run(item):
        pdf=root/item['path']; stem=pdf.stem
        commands={
            'text':[sys.executable,'-X','utf8',str(args.skill_scripts/'audit_pdf_text.py'),str(pdf),'--min-pt','5','--json'],
            'collision':[sys.executable,'-X','utf8',str(args.skill_scripts/'audit_figure_collisions.py'),str(pdf),'--json-out',str(args.out_dir/(stem+'.collision.json'))]}
        result={'path':item['path']}
        for key,command in commands.items():
            completed=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
            (args.out_dir/(stem+'.'+key+'.txt')).write_text(completed.stdout+completed.stderr,encoding='utf-8')
            result[key+'_exit']=completed.returncode
        return result

    with ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(run,inventory))
    (args.out_dir/'summary.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2))
    # Diagnostics are evidence even when an existing figure fails a guideline.
    # No redrawing or weakening thresholds in this read-only review.


if __name__=='__main__':
    main()
