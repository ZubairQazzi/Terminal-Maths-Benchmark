"""One initial native Gemini trajectory per frozen Biology task, serially.
Requires a written completed preflight audit gate. No secret is serialized.
"""
from trial_environment import ROOT,configure
configure()
from pathlib import Path
from datetime import datetime,timezone
import argparse,csv,hashlib,importlib.metadata,json,os,subprocess,sys,time

HERE=Path(__file__).resolve().parent
MODEL='gemini/gemini-3.5-flash-lite'
DOCKER=Path(r'C:/Users/zubai/AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe')
EXPECTED={1:'38e6e643672a56ff4e2d30619b0ec5ccdfa6bcfd75d80cd79c099159ea26ae36',2:'ba9ef45871ac057453dcdd1d4529f1eb2969a111763094d168c79c4a50c919ff'}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def verify(task):
    base=ROOT/f'biology-task-{task}'
    manifest=read(base/'authoring/reports/package_manifest.json')
    source=base/'authoring/package'/manifest['canonical_path']
    for rel,digest in manifest['files'].items():
        assert hashlib.sha256((source/rel).read_bytes()).hexdigest()==digest,('Frozen task changed',task,rel)
    return source
def command(task,runid,jobs):
    return [sys.executable,'-X','utf8','-B',str(HERE/'launch_harbor.py'),'run','--path',str(verify(task)),
      '--agent','terminus-2','--model',MODEL,'--api-key-name','GEMINI_API_KEY',
      '--ak','api_base=https://generativelanguage.googleapis.com/v1beta','--ak','parser_name=xml',
      '--ak','reasoning_effort=high','--ak','record_terminal_session=false','--ak','store_all_messages=true',
      '--ak','llm_call_kwargs='+json.dumps({'timeout':600,'num_retries':0,'max_tokens':32768}),
      '--n-concurrent','1','--max-retries','0','--jobs-dir',str(jobs),'--job-name',runid,'--quiet']
def elapsed(t):
    if not t or not t.get('started_at') or not t.get('finished_at'):return None
    return (datetime.fromisoformat(t['finished_at'].replace('Z','+00:00'))-datetime.fromisoformat(t['started_at'].replace('Z','+00:00'))).total_seconds()
def collect(task,runid,jobs,code,wall):
    paths=list((jobs/runid).glob('*/result.json'))
    row={'task':task,'run_id':runid,'requested_model':MODEL,'status':'INFRASTRUCTURE_INTERRUPTION','reward':None,'wall_seconds':wall,'process_exit_code':code,'steps':None,'tool_calls':None,'input_tokens':None,'output_tokens':None,'cached_tokens':None,'cost_usd_estimate':None,'billing_cost':'NOT VERIFIED; SDK estimate is not a receipt','scientific_failure_reason':None}
    if not paths:return row
    assert len(paths)==1
    p=paths[0];data=read(p);row['result_path']=str(p);row['exception']=data.get('exception_info');row['task_checksum']=data.get('task_checksum');assert row['task_checksum']==EXPECTED[task],('Unexpected task revision',task)
    row['wall_seconds']=elapsed(data) or wall;row['agent_execution_seconds']=elapsed(data.get('agent_execution'));row['agent_info']=data.get('agent_info')
    ar=data.get('agent_result') or {}
    for src,dst in [('n_input_tokens','input_tokens'),('n_output_tokens','output_tokens'),('n_cache_tokens','cached_tokens'),('cost_usd','cost_usd_estimate')]:row[dst]=ar.get(src)
    row['reward']=((data.get('verifier_result') or {}).get('rewards') or {}).get('reward')
    ctrf=p.parent/'verifier/ctrf.json'
    if ctrf.exists():
        c=read(ctrf)['results'];row['verifier_summary']=c.get('summary');row['individual_verifier_results']=c.get('tests');row['ctrf_path']=str(ctrf)
    trajectory=p.parent/'agent/trajectory.json'
    if trajectory.exists():
        t=read(trajectory);steps=t.get('steps') or [];row['steps']=sum(s.get('source')=='agent' for s in steps);row['tool_calls']=sum(len(s.get('tool_calls') or []) for s in steps);row['trajectory_path']=str(trajectory);row['trajectory_agent']=t.get('agent')
    exc=row['exception'];valid_timeout=(exc or {}).get('exception_type')=='AgentTimeoutError' and ((exc or {}).get('policy') or {}).get('has_valid_reward') is True
    if row['reward'] in (0,1) and (row.get('verifier_summary') or {}).get('tests')==11 and (exc is None or valid_timeout):
        row['status']='PASS' if row['reward']==1 else 'SCIENTIFIC_OR_SUBMISSION_FAILURE'
        row['scientific_failure_reason']='No verifier failures' if row['reward']==1 else 'Pending trajectory and individual verifier analysis; no fabricated scientific diagnosis.'
    return row
def main():
    p=argparse.ArgumentParser();p.add_argument('--batch',default='initial-gemini35lite-high-20261126');p.add_argument('--dry-run',action='store_true');a=p.parse_args()
    audit=read(HERE/'pre_model_gate.json');assert audit['audit_completed'] and audit['authorized_private_initial_trials'] and audit['local_trial_status']=='READY_WITH_DOCUMENTED_LIMITATIONS'
    out=ROOT/'authoring/trajectories'/a.batch;jobs=out/'jobs'
    if a.dry_run:
        print(json.dumps({'model':MODEL,'requested_trials_per_task':1,'commands':[command(i,f'bio{i}-initial-01',jobs) for i in (1,2)]},indent=2));return
    assert not out.exists(),'Refusing to overwrite any previous trajectory batch'
    jobs.mkdir(parents=True)
    env=dict(os.environ);env['PATH']=str(DOCKER.parent)+os.pathsep+env.get('PATH','');env['PYTHONPATH']=str(HERE)
    if not env.get('GEMINI_API_KEY'):
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,'Environment') as registry:env['GEMINI_API_KEY']=winreg.QueryValueEx(registry,'GEMINI_API_KEY')[0]
    # Keep the selected Gemini key host-side. Other providers are never fallback routes.
    for k in list(env):
        if any(s in k.upper() for s in ('API_KEY','AUTH_TOKEN','ACCESS_TOKEN','SECRET_KEY')) and k!='GEMINI_API_KEY':env.pop(k)
    from urllib.request import Request,urlopen
    from urllib.error import HTTPError,URLError
    catalog_url='https://generativelanguage.googleapis.com/v1beta/models/'+MODEL.split('/',1)[1]
    try:
        request=Request(catalog_url,headers={'x-goog-api-key':env['GEMINI_API_KEY'],'User-Agent':'local-biology-harbor-audit/1.0'})
        with urlopen(request,timeout=45) as response:catalog={'status':response.status,'metadata':json.loads(response.read())}
    except HTTPError as error:
        catalog={'status':error.code,'message':error.read().decode('utf-8','replace')[:3000]}
    except (URLError,TimeoutError) as error:catalog={'status':None,'message':type(error).__name__}
    dump(out/'model_catalog.json',catalog)
    manifest={'created_utc':datetime.now(timezone.utc).isoformat(),'authorization':'User explicitly requested initial Gemini Harbor trajectories after final audit','model':MODEL,'agent':'terminus-2','agent_version':'2.0.0','harbor_version':importlib.metadata.version('harbor'),'litellm_version':importlib.metadata.version('litellm'),'requested_valid_trials_per_task':1,'reasoning_effort':'high','parser':'xml','max_output_tokens':32768,'agent_max_turns':'Harbor default; no artificial turn cap','task_timeouts_unchanged':True,'resource_limits_unchanged':True,'task_science_changed':False,'public_free_tier_model':'Official pricing lists standard text input/output free tier; actual project billing tier not introspected','paid_only_fallback':False,'cache_locations':{k:env.get(k) for k in ('TEMP','TMP','TMPDIR','XDG_CACHE_HOME','UV_CACHE_DIR','PIP_CACHE_DIR','HF_HOME','PYTHONPYCACHEPREFIX','TIKTOKEN_CACHE_DIR')},'harbor_cache':str(ROOT/'runtime-cache/harbor'),'existing_installations_note':'Python and Harbor installations remain on C; existing Docker Desktop storage is not relocated. New configurable host caches/logs/tmp are on F.','commands':[command(i,f'bio{i}-initial-01',jobs) for i in (1,2)]}
    dump(out/'manifest.json',manifest)
    rows=[]
    for task in (1,2):
        for attempt in (1,2):
            runid=f'bio{task}-initial-{attempt:02d}';env['BIO_TRANSPORT_LOG']=str(out/(runid+'-transport.jsonl'))
            args=command(task,runid,jobs);dump(out/(runid+'-command.json'),args)
            print(json.dumps({'event':'initial_trial_started','task':task,'attempt':attempt,'run_id':runid}),flush=True)
            start=time.monotonic()
            with (out/(runid+'-console.log')).open('w',encoding='utf-8') as log:
                code=subprocess.call(args,cwd=out,env=env,stdout=log,stderr=subprocess.STDOUT)
            row=collect(task,runid,jobs,code,time.monotonic()-start);rows.append(row);verify(task)
            dump(out/'results.json',{'manifest':manifest,'attempts':rows,'note':'Initial diagnostic trajectories only; not eight-trial calibration or a reliable success-rate estimate.'})
            print(json.dumps({'event':'initial_trial_finished','task':task,'attempt':attempt,'status':row['status'],'reward':row['reward'],'seconds':row['wall_seconds'],'steps':row['steps']}),flush=True)
            if row['status']!='INFRASTRUCTURE_INTERRUPTION':break
            events=Path(env['BIO_TRANSPORT_LOG'])
            quota=events.exists() and any(json.loads(s).get('daily_or_zero_quota') for s in events.read_text().splitlines())
            if quota:break
            if attempt==1:time.sleep(15)
        # Even if one task meets a daily quota, preserve an initial Harbor attempt for the other.
    print('INITIAL GEMINI ATTEMPTS FINISHED',flush=True)
if __name__=='__main__':main()
