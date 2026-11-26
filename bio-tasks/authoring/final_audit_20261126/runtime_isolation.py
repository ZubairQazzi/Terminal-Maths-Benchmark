"""Fresh solver-image inventory and permissions audit. No model calls."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,time
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
DOCKER=r'C:\Users\zubai\AppData\Local\Programs\DockerDesktop\resources\bin\docker.exe'
script="""import hashlib,json,os,pathlib
base=pathlib.Path('/app/data')
files={str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest() for p in base.rglob('*') if p.is_file()}
private_paths=['/solution','/tests','/app/solution','/app/tests','/app/authoring','/app/fixture_truth.json']
blocked={}
for label,path in [('append_input',next(p for p in base.iterdir() if p.is_file())),('create_input',base/'should_not_exist'),('rename_input_dir',base)]:
 try:
  if label=='append_input':
   with path.open('ab'):pass
  elif label=='create_input':path.write_text('probe')
  else:path.rename('/app/data_renamed_probe')
  blocked[label]=False
 except PermissionError:blocked[label]=True
credential_names=['GEMINI_API_KEY','GOOGLE_API_KEY','OPENAI_API_KEY','ANTHROPIC_API_KEY']
result={'uid':os.getuid(),'input_files_sha256':files,'private_paths_absent':{p:not pathlib.Path(p).exists() for p in private_paths},'input_mutation_blocked':blocked,'provider_credentials_absent':{k:not bool(os.environ.get(k)) for k in credential_names},'initial_submission_empty':not any(pathlib.Path('/app/submission').iterdir()),'app_parent_write_protected':not os.access('/app',os.W_OK)}
print(json.dumps(result));assert result['uid']==1000 and all(result['private_paths_absent'].values()) and all(blocked.values()) and all(result['provider_credentials_absent'].values()) and result['initial_submission_empty'] and result['app_parent_write_protected']
"""
rows=[]
for task,tag in [(1,'v010'),(2,'v011')]:
    image=f'local-bio{task}-agent:{tag}'
    args=[DOCKER,'run','--rm','--network','none','--user','agent',image,'python3','-c',script]
    start=time.monotonic();p=subprocess.run(args,capture_output=True,text=True,timeout=60)
    item={'task':task,'image':image,'command':args,'exit_code':p.returncode,'seconds':time.monotonic()-start,'stderr':p.stderr}
    if p.stdout.strip():item['observed']=json.loads(p.stdout)
    source=ROOT/f'biology-task-{task}/task/environment/data'
    expected={p.relative_to(source).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in source.rglob('*') if p.is_file()}
    item['matches_frozen_solver_data']=item.get('observed',{}).get('input_files_sha256')==expected
    rows.append(item);print('Task',task,'image isolation exit',p.returncode,'source data match',item['matches_frozen_solver_data'],flush=True)
report={'created_utc':datetime.now(timezone.utc).isoformat(),'passed':all(r['exit_code']==0 and r['matches_frozen_solver_data'] for r in rows),'tasks':rows,'scope':'Fresh normal solver images only, without mounting source, oracle, private tests or user home. Private data/answer content also inspected in separate provenance/originality audit. Public calibration inputs are intentionally visible, not private biological answers.'}
(OUT/'runtime_isolation.json').write_text(json.dumps(report,indent=2))
assert report['passed']
