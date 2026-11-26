"""Read historical evidence and freeze preservation hashes. No provider calls."""
from pathlib import Path
from datetime import datetime,timezone
import csv,gzip,hashlib,json,re,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OLD=ROOT/'authoring/trajectories/initial-gemini35lite-high-20261126'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
 return h.hexdigest()
def main():
 snapshot=HERE/'preservation_manifest.json'
 if snapshot.exists():
  before=read(snapshot)
  for p,h in before['files'].items():assert sha(p)==h,p
  print('Preservation PASS:',len(before['files']),'frozen runtime/historical files unchanged');return
 files=[]
 for i in (1,2):
  base=ROOT/f'biology-task-{i}';m=read(base/'authoring/reports/package_manifest.json')
  for tree in (base/'task',base/'authoring/package'/m['canonical_path']):
   for rel,h in m['files'].items():
    p=tree/rel;assert sha(p)==h,str(p);files.append(p)
  files.append(base/'authoring/reports/package_manifest.json')
 files.extend(p for p in OLD.rglob('*') if p.is_file())
 dump(snapshot,{'utc':datetime.now(timezone.utc).isoformat(),'scope':'Existing direct/canonical frozen packages, their manifests and every file in the initial Gemini batch. New proposals and counterfactual copies are outside all preserved paths.','files':{str(p):sha(p) for p in files}})
 data=read(OLD/'initial_comparison.json');reviews=[];metrics=[]
 for a in data['attempts']:
  t=read(a['trajectory_path']);commands=[];observations=[]
  for s in t.get('steps',[]):
   for call in s.get('tool_calls',[]):
    args=call.get('arguments',{})
    if isinstance(args,str):
     try:args=json.loads(args)
     except ValueError:args={'raw':args}
    commands.append({'step':s.get('step_id'),'function':call.get('function_name'),'arguments':args})
   for o in (s.get('observation') or {}).get('results',[]):
    observations.append({'step':s.get('step_id'),'terminal_output':o.get('content','')})
  dump(HERE/(a['run_id']+'-executed_commands.json'),commands)
  dump(HERE/(a['run_id']+'-terminal_observations.json'),observations)
  # Executed commands/observations only, never hidden model reasoning text.
  reviews.append({'run_id':a['run_id'],'task':a['task'],'status':a['status'],'failed_checks':a['failed_verifier_names'],'command_steps':[x['step'] for x in commands],'operational_error_excerpts':a.get('terminal_or_parser_error_excerpts',[]),'screen':a['trajectory_command_screen'],'prior_direct_diagnosis':a['scientific_failure_reason']})
  vs=a.get('verifier_summary') or {}
  metrics.append({**{k:a.get(k) for k in ['task','run_id','status','reward','wall_seconds','agent_execution_seconds','steps','tool_calls','input_tokens','output_tokens','cached_tokens','cost_usd_estimate']},'checks_passed':vs.get('passed'),'checks_total':vs.get('tests'),'verifier_pass_rate':vs.get('passed',0)/vs.get('tests',1),'provider_errors':len(a.get('provider_errors',[]))})
 dump(HERE/'historical_trajectory_review.json',reviews);dump(HERE/'historical_metrics.json',metrics)
 with (HERE/'historical_metrics.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(metrics[0]));w.writeheader();w.writerows(metrics)
 shutil.copy2(OLD/'individual_verifier_results.csv',HERE/'historical_individual_verifier_results.csv')
 soft=ROOT/'authoring/sources/GSE273600_family.soft.gz';text=gzip.open(soft,'rt',encoding='utf-8').read();terms=['license','licence','copyright','permission','redistribut','commercial']
 dump(HERE/'geo_rights_keyword_scan.json',{'file':str(soft),'sha256':sha(soft),'method':'Case-insensitive literal keyword scan of complete cached official family SOFT; absence does not establish a license.','matches':{term:[line for line in text.splitlines() if term in line.lower()] for term in terms},'series_links':[line for line in text.splitlines() if line.startswith('!Series_supplementary_file') or line.startswith('!Series_relation')]})
 sizes={}
 for p in [ROOT/'biology-task-1/task',ROOT/'biology-task-2/task',OLD]:
  fs=[x for x in p.rglob('*') if x.is_file()];sizes[str(p)]={'files':len(fs),'bytes':sum(x.stat().st_size for x in fs)}
 sizes['F_disk_usage']=dict(zip(['total','used','free'],shutil.disk_usage('F:/')))
 dump(HERE/'storage_observation.json',sizes)
 print('Saved evidence, historical metrics and preservation manifest:',len(files),'files; no frozen modifications or model API calls')
if __name__=='__main__':main()
