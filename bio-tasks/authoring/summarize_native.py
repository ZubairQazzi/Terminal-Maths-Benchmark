from pathlib import Path
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--task',type=int,required=True);p.add_argument('--final-prefix',required=True);a=p.parse_args()
base=ROOT/f'biology-task-{a.task}';reports=base/'authoring/reports'
rows=[]
for job in sorted((reports/'harbor-jobs').glob('*')):
    if not job.is_dir():continue
    for trial in sorted(job.glob('*/result.json')):
        result=json.loads(trial.read_text());v=trial.parent/'verifier';rewards=(result.get('verifier_result') or {}).get('rewards')
        reward_file=v/'reward.txt';ctrf=v/'ctrf.json';per=[];summary={}
        if ctrf.exists():
            c=json.loads(ctrf.read_text());summary=c.get('results',{}).get('summary',{})
            per=[{'name':t['name'],'status':t['status']} for t in c.get('results',{}).get('tests',[])]
        artifacts={x.relative_to(trial.parent/'artifacts').as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in (trial.parent/'artifacts').rglob('*') if x.is_file()}
        valid=result.get('exception_info') is None and rewards is not None and reward_file.exists() and reward_file.read_text().strip() in ('0','1')
        row={'job':job.name,'trial':result.get('trial_name'),'version_scope_final':a.final_prefix in job.name,'task_checksum':result.get('task_checksum'),'reward':(rewards or {}).get('reward'),'binary_reward_text':reward_file.read_text().strip() if reward_file.exists() else None,'valid_graded_trial':valid,'exception':result.get('exception_info'),'separate_verifier':result.get('verifier_environment_mode')=='separate','ctrf_summary':summary,'per_test':per,'artifact_sha256':artifacts,'started_at':result.get('started_at'),'finished_at':result.get('finished_at'),'trial_directory':str(trial.parent)}
        rows.append(row)
valid=[r for r in rows if r['valid_graded_trial'] and r['version_scope_final']]
oracle=[r for r in valid if f'bio{a.task}-oracle-' in r['job']]
repeat_equal=len(oracle)>=2 and oracle[0]['artifact_sha256']==oracle[1]['artifact_sha256']
preflight=[]
for log in sorted(reports.glob('harbor_*.log')):
    if log.name.startswith('harbor_lint'):continue
    text=log.read_text(encoding='utf-8',errors='replace')
    if 'EXIT 1 ' in text and 'Docker daemon is not running' in text:
        preflight.append({'log':str(log),'reason':'Docker preflight did not create a graded trial; transient infrastructure interruption, not a scientific failure.'})
result={'task':a.task,'final_job_prefix_filter':a.final_prefix,'valid_final_trials':len(valid),'infrastructure_errors':sum(not r['valid_graded_trial'] for r in rows)+len(preflight),'preflight_failures':preflight,'native_oracle_repeats':len(oracle),'native_oracle_artifacts_byte_identical':repeat_equal,'trials':rows,'scope':'Only completed exception-free trials with binary reward files count as graded. Infrastructure failures and superseded versions are retained and excluded. Deterministic controls are not empirical AI-model trials.'}
(reports/'native_summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
lines=['# Actual native Docker/Harbor validation','',result['scope'],'',f'Final valid trials: {len(valid)}. Native oracle repeats: {len(oracle)}; artifacts byte-identical: {repeat_equal}.','','| Job | Final version scope | Valid | Reward | CTRF passed/total | Separate verifier |','|---|---|---|---:|---|---|']
for r in rows:
    s=r['ctrf_summary'];lines.append(f"| {r['job']} / {r['trial']} | {r['version_scope_final']} | {r['valid_graded_trial']} | {r['reward']} | {s.get('passed','—')}/{s.get('tests','—')} | {r['separate_verifier']} |")
lines.extend(['','Full per-test outcomes, exceptions, timings, task checksums, artifact hashes and exact trial directories are in `native_summary.json`; console commands are preserved in `harbor_*.log`. External QC NOT RUN; Gemini NOT RUN.'])
(reports/'harbor_validation.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('trials','preflight_failures')},indent=2))
