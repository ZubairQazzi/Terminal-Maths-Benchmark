"""Execute the26 available pinned shell rules; pipeline/missing rules audited separately."""
from pathlib import Path
import argparse,json,subprocess
p=argparse.ArgumentParser();p.add_argument('--task',type=int,required=True);p.add_argument('--suffix',required=True);a=p.parse_args()
ROOT=Path('/work');base=ROOT/f'biology-task-{a.task}'
manifest=json.loads((base/'authoring/reports/package_manifest.json').read_text());task=manifest['canonical_path']
rules=['task-fields','task-path','task-structure','task-slug','task-readme','canary','task-absolute-path','instruction-suffix','test-file-references','dockerfile-references','dockerfile-sanity','dockerfile-platform','allow-internet','separate-verifier','compose-host-binds','task-timeout','gpu-types','task-resources','verifier-resources','nproc','verifier-tooling-baked','trial-network-fetch','pip-pinning','pytest-version','test-sh-sanity','binary-reward']
rows=[]
for name in rules:
    command=['bash',str(Path('ci_checks')/('check-'+name+'.sh')),task]
    r=subprocess.run(command,capture_output=True,text=True,timeout=60)
    rows.append(dict(id=name,command=command,exit_code=r.returncode,output=r.stdout+r.stderr,status='PASS' if r.returncode==0 else 'FAIL'))
    print(name,r.returncode,flush=True)
(base/f'authoring/reports/upstream_static_{a.suffix}.json').write_text(json.dumps(rows,indent=2))
print('passed',sum(r['status']=='PASS' for r in rows),'/',len(rows))
