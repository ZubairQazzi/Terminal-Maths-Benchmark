"""Generate reviewable diffs and estimates; never apply to existing tasks."""
from pathlib import Path
from datetime import datetime,timezone
import difflib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OUT=HERE/'proposal'
def patch(rel,old,new):
    if old==new:raise ValueError('No change: '+rel)
    target=OUT/(rel.replace('/','__')+'.patch')
    target.write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='frozen-v0.1.1/'+rel,tofile='proposed-v0.2.0/'+rel)),encoding='utf-8')
def main():
    OUT.mkdir(exist_ok=True)
    p=ROOT/'biology-task-2/authoring/build_inputs.py';old=p.read_text();new=old.replace('import numpy as np','from secure_fixture_rng import SecureRecordedRNG\nimport numpy as np',1)
    new=new.replace("SOURCE=ROOT.parent/'shared-inputs/original-read-only-data'\n",'')
    new=new.replace('def build(seed=273600,target=None):\n    dest=Path(target) if target else ROOT/\'task/environment/data\'\n    dest.mkdir(parents=True,exist_ok=True)', '''def build(*, source_dir, metadata_path, target, truth_path,
          private_randomness_path, protected_roots, replay_record=None):
    SOURCE=Path(source_dir).resolve()
    dest=Path(target).resolve(); truth_path=Path(truth_path).resolve()
    # Only a separately approved versioned task is a valid target.
    if not protected_roots:
        raise ValueError('Explicit original/canonical/history protection roots required')
    for protected in protected_roots:
        for output in [dest,truth_path,Path(private_randomness_path).resolve()]:
            if output.is_relative_to(Path(protected).resolve()):
                raise ValueError('Refuse existing frozen/history output')
    if dest.exists() and any(dest.iterdir()):
        raise FileExistsError('Refuse nonempty fixture destination')
    if truth_path.is_relative_to(dest.parent):
        raise ValueError('Private truth must be outside agent build context')
    if Path(private_randomness_path).resolve().is_relative_to(dest.parent.parent):
        raise ValueError('Private draw record must be outside entire task tree')
    if replay_record is not None and Path(replay_record).resolve().is_relative_to(dest.parent.parent):
        raise ValueError('Private replay must be outside entire task tree')
    if truth_path.exists():
        raise FileExistsError('Refuse existing private truth')
    dest.mkdir(parents=True,exist_ok=True)''')
    new=new.replace("shutil.copy2(ROOT.parent/'authoring/sample_metadata.csv',dest/'sample_metadata.csv')", "shutil.copy2(metadata_path,dest/'sample_metadata.csv')")
    new=new.replace('rng=np.random.default_rng(seed)','rng=SecureRecordedRNG(replay_record=replay_record)')
    new=new.replace("private={'seed':seed,'mapping':", "private={'mapping':")
    new=new.replace("private_path=ROOT/'task/tests/fixture_truth.json' if target is None else dest.parent/'fixture_truth.json'",'private_path=truth_path')
    new=new.replace('    return private','    rng.save_private_record(private_randomness_path,forbidden_roots=[dest.parent,truth_path.parent])\n    return private')
    new=new.replace("if __name__=='__main__':build()",'''if __name__=='__main__':
    raise SystemExit('Call build with explicit approved versioned target, private truth and private draw-record paths')''')
    assert 'default_rng(seed)' not in new and "'seed':seed" not in new
    compile(new,'proposed-build_inputs.py','exec')
    patch('authoring/build_inputs.py',old,new)
    (OUT/'build_inputs.proposed.py').write_text(new,encoding='utf-8')
    p=ROOT/'biology-task-2/task/task.toml';old=p.read_text();patch('task/task.toml',old,old.replace('version = "0.1.1"','version = "0.2.0"',1))
    p=ROOT/'biology-task-2/task/instruction.md';old=p.read_text();new=old.replace("using the supplied scaled atlas's actual minimum (absolute tolerance `1e-7`).", "using each column's minimum in the **supplied scaled** `atlas_tpm.tsv.gz`, before normalization (absolute tolerance `1e-7`, inclusive). Do not use the minimum of normalized `A` for this audit field.")
    patch('task/instruction.md',old,new)
    p=ROOT/'biology-task-2/task/tests/checks.py';old=p.read_text();new=old.replace("for k in a.columns:assert abs(float(floor[k])-float(a[k].min()))<1e-7", "for k in a.columns:assert abs(float(floor[k])-float(a[k].min()))<=1e-7,('supplied atlas minimum',k,floor[k],float(a[k].min()),'tolerance',1e-7)")
    for before,after in [('abs(float(actual)-expect)<2e-6','abs(float(actual)-expect)<=2e-6'),('abs(float(row.validation_margin)-margin)<2e-6','abs(float(row.validation_margin)-margin)<=2e-6'),('abs(float(getattr(row,field))-expect)<2e-6','abs(float(getattr(row,field))-expect)<=2e-6')]:new=new.replace(before,after)
    compile(new,'proposed-checks.py','exec');patch('task/tests/checks.py',old,new)
    original=json.loads((ROOT/'authoring/trajectories/initial-gemini35lite-high-20261126/initial_comparison.json').read_text())
    runs=[r for r in original['attempts'] if r['status']!='INFRASTRUCTURE_INTERRUPTION'];est=[]
    for r in runs:
        n=5;prompt=n*r['input_tokens'];output=n*r['output_tokens'];cache=n*r['cached_tokens']
        est.append({'task':r['task'],'trials':n,'input_tokens':prompt,'output_tokens':output,'cache_read_tokens_subset':cache,'agent_steps':n*r['steps'],'successful_provider_calls':n*r['provider_successful_calls'],'recovered_provider_errors_replay':n*len(r['provider_errors']),'wall_seconds_replay':n*r['wall_seconds'],'cost_usd_with_historical_cache_fraction':((prompt-cache)*.30+cache*.03+output*2.50)/1e6,'cost_usd_without_cache_discount':(prompt*.30+output*2.50)/1e6})
    totals={k:sum(r[k] for r in est) for k in ['input_tokens','output_tokens','cache_read_tokens_subset','agent_steps','successful_provider_calls','recovered_provider_errors_replay','wall_seconds_replay','cost_usd_with_historical_cache_fraction','cost_usd_without_cache_discount']}
    result={'client_date':'2026-11-26','method':'Five times each single completed historical trajectory; only a planning scenario, not a distributional forecast. Task 2 new fixture may change runtime. Provider failures and errors with no usage receipts are not assigned invented token counts.','pricing_usd_per_million':{'uncached_input':.30,'cached_input':.03,'output_including_reported_thinking':2.50},'source':'https://aistudio.google.com/docs/pricing#gemini-3.5-flash-lite','per_task':est,'total':totals,'proposed_usage_allowance':{'input_tokens':12000000,'output_tokens':750000,'instrumented_provider_request_attempts':900,'conservative_uncached_text_cost_usd':5.475,'budget_requested_usd':6.0,'billing_caveat':'Planning guard on accounted/estimated token use, not a guaranteed invoice cap; actual project tier, tax, failed-request accounting and implicit cache treatment are not verified. Do not change billing or use paid-only fallback. Pause on budget/quota limit and label interrupted runs censored, not scientific failures.'},'resources':{'serial_concurrency':1,'cpus':2,'task1_memory_mb':8192,'task2_memory_mb':4096,'per_task_storage_mb':10240,'original_agent_timeout_seconds':28800,'original_verifier_timeout_seconds':3600,'gpus':0,'expected_serial_hours_replay':totals['wall_seconds_replay']/3600,'planning_hours_including_QC_and_availability': '3–5, uncertain; original task limits remain unchanged','F_project_storage_reserve_gib':10,'docker_observed_memory_bytes':16609280000,'docker_observed_cpus':20,'docker_root':'/var/lib/docker','docker_host_storage':'Existing Docker Desktop virtual disk, previously on C; not relocated by this proposal. New project files/logs/trajectories/configurable host caches use F.'}}
    (HERE/'resource_estimate.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(totals,indent=2));print('Draft diffs generated only; no frozen changes or provider calls')
if __name__=='__main__':main()
