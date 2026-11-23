"""One separate graded smoke plus eight independent valid native agent trials.
Preserves all failures/interruptions; never changes the Mathematics task.
"""
import argparse
import csv
from datetime import datetime,timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import time
import winreg
from connection_recovery import freeze,request

ROOT=Path(__file__).resolve().parents[2]
TASK=ROOT/'tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure'
PYTHON=Path(r'C:/Users/zubai/AppData/Roaming/uv/tools/harbor/Scripts/python.exe')
DOCKER_DIR=r'C:\Users\zubai\AppData\Local\Programs\DockerDesktop\resources\bin'
MODEL='gemini/gemini-3.5-flash-lite'
PREFIX='g35lite-high-v013'
OUT=ROOT/'authoring/trajectories/calibration-v013-gemini35lite-high-r2-20261123'
JOBS=OUT/'jobs'
COLUMNS=['phase','trial_number','attempt_number','run_id','model','task_version','status','reward',
    'duration_sec','agent_execution_sec','steps','tool_calls','input_tokens','output_tokens','cached_tokens',
    'cost_usd','cost_kind','failure_reason','result_path','trajectory_path']

def stamp(): return datetime.now(timezone.utc).isoformat()
def dump(path,value): path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def load(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def duration(timing):
    a=timing.get('started_at'); b=timing.get('finished_at')
    if not(a and b): return None
    return (datetime.fromisoformat(b.replace('Z','+00:00'))-datetime.fromisoformat(a.replace('Z','+00:00'))).total_seconds()

def command(run_id):
    return [str(PYTHON),'-B',str(ROOT/'authoring/evidence/resilient_harbor_v2.py'),'run','--path',str(TASK),
        '--agent','terminus-2','--model',MODEL,'--api-key-name','GEMINI_API_KEY',
        '--ak','api_base=https://generativelanguage.googleapis.com/v1beta',
        '--ak','parser_name=xml','--ak','reasoning_effort=high','--ak','record_terminal_session=false','--ak','store_all_messages=true',
        '--ak','llm_call_kwargs='+json.dumps({'timeout':600,'num_retries':0,'max_tokens':32768}),
        '--n-concurrent','1','--max-retries','0','--jobs-dir',str(JOBS),'--job-name',run_id]

def collect(phase,number,attempt,run_id,code,elapsed):
    job=JOBS/run_id
    found=[(p,load(p)) for p in job.glob('*/result.json') if 'trial_name' in load(p)]
    row={'phase':phase,'trial_number':number,'attempt_number':attempt,'run_id':run_id,'model':MODEL,
        'task_version':'0.1.3','status':'INTERRUPTED','reward':None,'duration_sec':elapsed,
        'agent_execution_sec':None,'steps':None,'tool_calls':None,'input_tokens':None,'output_tokens':None,
        'cached_tokens':None,'cost_usd':None,'cost_kind':'harness_estimate_not_billing_receipt',
        'failure_reason':'No completed native trial result','result_path':None,'trajectory_path':None,
        'process_return_code':code,'console_path':str(OUT/(run_id+'-console.log'))}
    if not found: return row
    assert len(found)==1
    path,data=found[0]
    row['result_path']=str(path)
    row['duration_sec']=duration(data) or elapsed
    row['agent_execution_sec']=duration(data.get('agent_execution') or {})
    row['task_checksum']=data.get('task_checksum')
    assert row['task_checksum']=='99a8da66bc504372c791300e6504ce522f6453cd90ad40dc9ce0ab971ae02cbe'
    row['agent_info']=data.get('agent_info')
    assert (row['agent_info'] or {}).get('version')=='2.0.0'
    agent=data.get('agent_result') or {}
    for key,target in [('n_input_tokens','input_tokens'),('n_output_tokens','output_tokens'),
        ('n_cache_tokens','cached_tokens'),('cost_usd','cost_usd')]: row[target]=agent.get(key)
    row['reward']=((data.get('verifier_result') or {}).get('rewards') or {}).get('reward')
    row['exception_info']=data.get('exception_info')
    ctrf=path.parent/'verifier/ctrf.json'
    if ctrf.exists(): row['verifier_summary']=load(ctrf).get('results',{}).get('summary',{})
    exception=row['exception_info']
    if exception:
        row['failure_reason']=exception.get('exception_type','Unknown infrastructure exception')
    policy=(exception or {}).get('policy') or {}
    legitimate_timeout=(exception or {}).get('exception_type')=='AgentTimeoutError' and policy.get('has_valid_reward') is True
    grading=(row.get('verifier_summary') or {}).get('tests')==9
    if row['reward'] in (0,1) and grading and (exception is None or legitimate_timeout):
        row['status']='PASS' if row['reward']==1 else 'FAIL'
        row['failure_reason']='' if row['status']=='PASS' else 'Agent timeout with valid grading' if legitimate_timeout else 'Hidden verifier rejected independent agent submission; inspect trajectory.'
    trajectory=path.parent/'agent/trajectory.json'
    if trajectory.exists():
        row['trajectory_path']=str(trajectory)
        data=load(trajectory)
        steps=data.get('steps') or []
        row['steps']=sum(s.get('source')=='agent' for s in steps)
        row['tool_calls']=sum(len(s.get('tool_calls') or []) for s in steps)
        row['runtime_agent']=data.get('agent')
    return row

def save(rows,state,reason=None):
    valid=[r for r in rows if r['phase']=='calibration' and r['status'] in ('PASS','FAIL')]
    smoke=[r for r in rows if r['phase']=='smoke' and r['status'] in ('PASS','FAIL')]
    passes=sum(r['status']=='PASS' for r in valid)
    times=[r['duration_sec'] for r in valid]
    summary={'updated_utc':stamp(),'task_version':'0.1.3','task_digest':freeze(),
        'model':MODEL,'agent':'terminus-2','agent_version':'2.0.0','requested_valid_trials':8,
        'smoke_valid_completed':len(smoke),'smoke_separate_from_calibration':True,
        'completed_valid_trials':len(valid),'successful_trials':passes,'failed_trials':len(valid)-passes,
        'success_percentage':100*passes/len(valid) if valid else None,
        'failure_percentage':100*(len(valid)-passes)/len(valid) if valid else None,
        'mean_duration_sec':statistics.mean(times) if times else None,
        'median_duration_sec':statistics.median(times) if times else None,
        'infrastructure_interruptions':sum(r['status']=='INTERRUPTED' for r in rows),
        'status':state,'stop_reason':reason,'all_attempts':rows}
    dump(OUT/'summary.json',summary)
    with (OUT/'all_attempts.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=COLUMNS,extrasaction='ignore')
        writer.writeheader();writer.writerows(rows)
    return summary

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--dry-run',action='store_true');args=parser.parse_args()
    freeze()
    if args.dry_run:
        print(json.dumps({'command':command(PREFIX+'-smoke-01'),'task_digest':freeze()}),flush=True)
        return
    assert not OUT.exists(),'Refusing to overwrite an existing recovery/calibration batch.'
    JOBS.mkdir(parents=True)
    env=os.environ.copy()
    if not env.get('GEMINI_API_KEY'):
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,'Environment') as registry:
            env['GEMINI_API_KEY']=winreg.QueryValueEx(registry,'GEMINI_API_KEY')[0]
    env['PATH']=DOCKER_DIR+os.pathsep+env.get('PATH','')
    env['PYTHONUTF8']='1';env['PYTHONIOENCODING']='utf-8'
    manifest={'created_utc':stamp(),'task_version':'0.1.3','task_digest':freeze(),
        'native_checksum':'99a8da66bc504372c791300e6504ce522f6453cd90ad40dc9ce0ab971ae02cbe',
        'harbor_version':importlib.metadata.version('harbor'),'litellm_version':importlib.metadata.version('litellm'),
        'agent':'terminus-2','agent_version':'2.0.0','model':MODEL,'parser_name':'xml',
        'api_base':'https://generativelanguage.googleapis.com/v1beta','user_confirmed_free_tier_project':True,
        'paid_fallback':False,'smoke_excluded_from_calibration':True,
        'agent_timeout_sec':28800,'request_timeout_sec':600,'reasoning_effort':'high','max_output_tokens':32768,'min_request_interval_sec':20,
        'transport_max_attempts':10,'backoff_sec':'10,20,40,80,120,120,120,120,120 plus U(0,3) jitter, Retry-After honored',
        'sdk_retries':0,'nested_native_retry_attempts':1,'fresh_infrastructure_attempt_cap_per_slot':2,
        'mathematical_task_changed':False,'prompts_changed':False,
        'wrapper_sha256':hashlib.sha256((ROOT/'authoring/evidence/resilient_harbor_v2.py').read_bytes()).hexdigest(),
        'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'commands':[command(PREFIX+'-smoke-01')]+[command(PREFIX+'-trial-%02d-attempt-01'%i) for i in range(1,9)]}
    dump(OUT/'manifest.json',manifest)
    rows=[];save(rows,'SMOKE_IN_PROGRESS')
    for phase,number in [('smoke',0)]+[('calibration',i) for i in range(1,9)]:
        valid=False
        for attempt in (1,2):
            freeze()
            run_id=PREFIX+('-smoke-%02d'%attempt if phase=='smoke' else '-trial-%02d-attempt-%02d'%(number,attempt))
            env['BENCHMARK_TRANSPORT_LOG']=str(OUT/(run_id+'-transport.jsonl'))
            print(json.dumps({'event':'trial_started','phase':phase,'number':number,'attempt':attempt,'run_id':run_id}),flush=True)
            started=time.monotonic()
            with (OUT/(run_id+'-console.log')).open('w',encoding='utf-8') as console:
                result=subprocess.run(command(run_id),cwd=ROOT,env=env,stdout=console,stderr=subprocess.STDOUT)
            freeze()
            row=collect(phase,number,attempt,run_id,result.returncode,time.monotonic()-started)
            rows.append(row)
            save(rows,'SMOKE_IN_PROGRESS' if phase=='smoke' else 'CALIBRATION_IN_PROGRESS')
            print(json.dumps({'event':'trial_finished','phase':phase,'number':number,'attempt':attempt,
                'status':row['status'],'reward':row['reward'],'duration_sec':row['duration_sec'],'steps':row['steps']}),flush=True)
            if row['status'] in ('PASS','FAIL'):
                valid=True;break
            transport=Path(env['BENCHMARK_TRANSPORT_LOG'])
            events=[json.loads(line) for line in transport.read_text(encoding='utf-8').splitlines()] if transport.exists() else []
            if any(e.get('quota_exhausted') for e in events):
                save(rows,'BLOCKED','Provider daily/zero quota exhausted; no paid fallback.')
                return
            if attempt==1:
                print(json.dumps({'event':'infrastructure_recovery_backoff','seconds':45}),flush=True)
                time.sleep(45)
                diagnostic=request('v1beta/models/'+MODEL.split('/',1)[1]+':generateContent',
                    {'contents':[{'parts':[{'text':'Reply READY.'}]}],'generationConfig':{'maxOutputTokens':512}})
                dump(OUT/(run_id+'-recovery-probe.json'),diagnostic)
                if diagnostic['status']!=200:
                    save(rows,'BLOCKED','Infrastructure interruption and same-model recovery probe did not succeed.');return
        if not valid:
            save(rows,'BLOCKED','Two fresh infrastructure interruptions in the same required slot; investigate before resuming.');return
        if phase=='smoke':
            save(rows,'CALIBRATION_IN_PROGRESS')
            print(json.dumps({'event':'smoke_validly_graded','result':row['status'],'starting_eight_independent_trials':True}),flush=True)
    summary=save(rows,'COMPLETED')
    print(json.dumps({'event':'calibration_completed','valid_trials':summary['completed_valid_trials'],
        'passes':summary['successful_trials'],'failures':summary['failed_trials'],'success_percentage':summary['success_percentage']}),flush=True)

if __name__=='__main__': main()