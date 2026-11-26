"""Offline diagnostic copies only; never revise official model results."""
from pathlib import Path
from datetime import datetime,timezone
import csv,gzip,json,os,shutil,subprocess,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OLD=ROOT/'authoring/trajectories/initial-gemini35lite-high-20261126'
DOCKER=r'C:\Users\zubai\AppData\Local\Programs\DockerDesktop\resources\bin\docker.exe'
def main():
 record=HERE/'counterfactual_results.json'
 assert not record.exists(),'Refuse to overwrite diagnostic evidence'
 cases=[]
 for i,runid,image in [(1,'bio1-initial-02','local-bio1-verifier:v010'),(2,'bio2-initial-01','local-bio2-verifier:v011')]:
  trial=next((OLD/'jobs'/runid).glob('*/result.json')).parent
  dest=HERE/f'counterfactual_task{i}';sub=dest/'submission';logs=dest/'verifier';logs.mkdir(parents=True,exist_ok=False)
  shutil.copytree(trial/'artifacts/app/submission',sub)
  if i==1:
   path=sub/'calibration.tsv'
   with path.open(newline='',encoding='utf-8') as f:r=csv.DictReader(f,delimiter='\t');fields=r.fieldnames;rows=list(r)
   boundary=next(x for x in rows if x['case_id']=='minimum_effect_boundary')
   assert float(boundary['dmr_effect'])==.5 and float(boundary['se_dmr'])==0 and float(boundary['p_dmr_minimum'])==0
   boundary['p_dmr_minimum']='1';boundary['p_joint']='1'
   m=len(rows);h=sum(1/j for j in range(1,m+1));order=sorted(range(m),key=lambda j:float(rows[j]['p_joint']));running=1.
   for rank in range(m,0,-1):
    j=order[rank-1];running=min(running,m*h*float(rows[j]['p_joint'])/rank)
    rows[j]['q_joint']=format(running,'.17g');rows[j]['certified']='true' if running<=.05 else 'false'
   with path.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(rows)
   change='Correct only the zero-SE minimum-effect boundary p_dmr_minimum/p_joint and recalculate its prescribed eight-case BY q values/certified labels. All real-data artifacts copied unchanged.'
  else:
   source=ROOT/'biology-task-2/task/environment/data/atlas_tpm.tsv.gz'
   with gzip.open(source,'rt',newline='') as f:
    r=csv.reader(f,delimiter='\t');cols=next(r)[1:];mins=[float('inf')]*len(cols)
    for row in r:
     for j,value in enumerate(row[1:]):mins[j]=min(mins[j],float(value))
   path=sub/'audit.json';a=json.loads(path.read_text());a['atlas_minimum_by_column']=dict(zip(cols,mins));path.write_text(json.dumps(a,indent=2)+'\n')
   change='Replace only atlas_minimum_by_column with measured minima of the supplied scaled atlas. Alignment, queries, all other audit fields and scientific inference unchanged.'
  args=[DOCKER,'run','--rm','--network','none','--cpus','2','--memory','8g' if i==1 else '4g','--mount',f'type=bind,source={sub.as_posix()},target=/app/submission,readonly','--mount',f'type=bind,source={logs.as_posix()},target=/logs/verifier',image,'bash','/tests/test.sh']
  # No model keys or host authoring directories are mounted or forwarded.
  env={k:v for k,v in os.environ.items() if not any(s in k.upper() for s in ['API_KEY','SECRET_KEY','AUTH_TOKEN','ACCESS_TOKEN'])}
  start=time.monotonic()
  with (dest/'console.log').open('w',encoding='utf-8') as f:code=subprocess.call(args,cwd=HERE,env=env,stdout=f,stderr=subprocess.STDOUT)
  assert code==0,code
  c=json.loads((logs/'ctrf.json').read_text())['results'];reward=float((logs/'reward.txt').read_text())
  cases.append({'task':i,'original_run':runid,'official_original_reward':0,'official_original_checks_passed':10,'diagnostic_change':change,'unchanged_verifier_image':image,'diagnostic_reward':reward,'diagnostic_summary':c['summary'],'individual_results':c['tests'],'seconds':time.monotonic()-start,'source_model_artifacts_untouched':True,'command':args})
  assert reward==1 and c['summary']['passed']==11,c['summary']
  print('Offline diagnostic task',i,'11/11 after narrow correction; official model reward remains 0',flush=True)
 record.write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'scope':'Researcher-created counterfactual copies using original unchanged native verifier images; not independent model trajectories, not official rescoring, not task edits.','cases':cases},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
