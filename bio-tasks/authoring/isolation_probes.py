"""Observed Docker isolation and offline execution probes, outside task runtime."""
from pathlib import Path
import argparse,json,subprocess,time,os
ROOT=Path(__file__).resolve().parents[1]
DOCKER=r'C:\Users\zubai\AppData\Local\Programs\DockerDesktop\resources\bin\docker.exe'
p=argparse.ArgumentParser();p.add_argument('--task',type=int,required=True);p.add_argument('--suffix',required=True);a=p.parse_args()
base=ROOT/f'biology-task-{a.task}';report=base/'authoring/reports';rows=[]
def execute(label,args):
    start=time.monotonic();r=subprocess.run([DOCKER]+args,capture_output=True,text=True,timeout=240)
    row={'label':label,'command':[DOCKER]+args,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'seconds':time.monotonic()-start};rows.append(row)
    print(label,r.returncode,flush=True)
    return r
solver=f'local-bio{a.task}-agent:{a.suffix}';verifier=f'local-bio{a.task}-verifier:{a.suffix}'
script="""import json,os,pathlib,socket
p=pathlib.Path('/app/data');first=next(x for x in p.iterdir() if x.is_file())
write_blocked=False
try:
 with first.open('ab'):pass
except PermissionError:write_blocked=True
out=pathlib.Path('/app/submission/probe.txt');out.write_text('probe');out.unlink()
result={'uid':os.getuid(),'private_tests_absent':not pathlib.Path('/tests').exists(),'private_solution_absent':not pathlib.Path('/solution').exists(),'data_not_writable':write_blocked,'output_writable':True}
assert result['uid']!=0 and all(v for k,v in result.items() if k!='uid'),result
print(json.dumps(result))
"""
execute('unprivileged_solver_no_private_material',['run','--rm','--network','none','--cpus','2','--memory','4g','--user','agent',solver,'python3','-c',script])
script2="""import json,pathlib,socket
paths=[pathlib.Path('/tests'),pathlib.Path('/logs/verifier')]
result={'private_directories_mode700':all((p.stat().st_mode&0o077)==0 for p in paths),'score_absent_before_grading':not pathlib.Path('/logs/verifier/reward.txt').exists()}
try:socket.create_connection(('1.1.1.1',443),timeout=1);result['egress_blocked']=False
except OSError:result['egress_blocked']=True
assert all(result.values()),result
print(json.dumps(result))
"""
execute('verifier_private_and_no_egress',['run','--rm','--network','none',verifier,'python3','-c',script2])
source=(base/'task/solution').as_posix()
r=execute('oracle_executes_offline',['run','--rm','--network','none','--cpus','2','--memory','8g','--user','agent','--mount','type=bind,source='+source+',target=/solution,readonly',solver,'bash','/solution/solve.sh'])
data={'task':a.task,'image_suffix':a.suffix,'passed':all(row['exit_code']==0 for row in rows),'probes':rows,'scope':'Docker observed capability/file permissions and fully offline oracle. Harbor separate-verifier artifacts and clean reset assessed additionally from native trial results; no credential injection or malicious submitted-code execution is used.'}
(report/f'isolation_{a.suffix}.json').write_text(json.dumps(data,indent=2))
assert data['passed'],'Isolation/offline probe failed; inspect report'
