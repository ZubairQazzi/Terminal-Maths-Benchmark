"""Evidence-only reporting for the current smoke-plus-eight calibration batch."""
import argparse
import csv
from datetime import datetime,timezone
import json
from pathlib import Path
import statistics

ROOT=Path(__file__).resolve().parents[2]
REPORTS=ROOT/'authoring/reports'

def load(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def dump(path,value): path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def mean(values): return statistics.mean(values) if values else None

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--require-reviewed',action='store_true')
    args=parser.parse_args()
    pointer=load(ROOT/'authoring/trajectories/latest_calibration.json')
    folder=ROOT/pointer['batch_directory']
    summary=load(folder/'summary.json'); manifest=load(folder/'manifest.json')
    attempts=summary['all_attempts']
    valid=[r for r in attempts if r['phase']=='calibration' and r['status'] in ('PASS','FAIL')]
    smoke=[r for r in attempts if r['phase']=='smoke' and r['status'] in ('PASS','FAIL')]
    interrupted=[r for r in attempts if r['status']=='INTERRUPTED']
    reviews=load(folder/'reviews.json') if (folder/'reviews.json').exists() else {}
    rows=[]
    for row in attempts:
        item=dict(row)
        item['review']=reviews.get(row['run_id'],{'review_status':'PENDING','mathematical_mistakes':'Not yet reviewed.',
            'implementation_mistakes':'Not yet reviewed.','verification':'Not yet reviewed.','final_reason':row['failure_reason']})
        if row['result_path']:
            result=load(Path(row['result_path']))
            assert result['task_checksum']==manifest['native_checksum']
            assert result['agent_info']['version']=='2.0.0'
            if row['status'] in ('PASS','FAIL'):
                assert result.get('exception_info') is None or result['exception_info']['policy']['has_valid_reward']
                ctrf=load(Path(row['result_path']).parent/'verifier/ctrf.json')['results']
                assert ctrf['summary']['tests']==9
                assert row['reward']==(1.0 if row['status']=='PASS' else 0.0)
                assert (ctrf['summary']['passed']==9)==(row['status']=='PASS')
                item['test_details']=[{'name':t.get('name'),'status':t.get('status'),'message':t.get('message')} for t in ctrf.get('tests',[])]
        if row['trajectory_path']:
            trajectory=load(Path(row['trajectory_path']))
            assert trajectory['agent']['model_name']==manifest['model']
            item['runtime_model']=trajectory['agent']['model_name']
            item['runtime_parser']=trajectory['agent'].get('extra',{}).get('parser')
            item['cached_tokens']=trajectory.get('final_metrics',{}).get('total_cached_tokens',row.get('cached_tokens'))
        rows.append(item)
    complete=len(valid)==8 and len(smoke)==1 and summary['status']=='COMPLETED'
    if args.require_reviewed:
        assert complete,'Eight valid independent trials and separate valid smoke are not complete.'
        assert all(reviews.get(row['run_id'],{}).get('review_status')=='REVIEWED' for row in valid+smoke),'Manual per-trial review remains incomplete.'
    successes=sum(r['status']=='PASS' for r in valid)
    percent=100*successes/len(valid) if valid else None
    target='NOT DETERMINED: fewer than eight valid trials.'
    if complete:
        target=('MET: within the user-accepted approximate range of 3-5 successes.' if 3<=successes<=5 else 'NOT MET: outside the user-accepted approximate range of 3-5 successes.')
    report={'updated_utc':datetime.now(timezone.utc).isoformat(),'batch_directory':str(folder),
        'task_version':'0.1.3','task_digest':manifest['task_digest'],'native_task_checksum':manifest['native_checksum'],
        'model':manifest['model'],'agent':'terminus-2','agent_version':'2.0.0','parser_name':manifest.get('parser_name','json'),
        'smoke_valid_completed':len(smoke),'smoke_separate':True,'total_valid_trials':len(valid),
        'successful_trials':successes,'failed_trials':len(valid)-successes,
        'success_percentage':percent,'failure_percentage':100-percent if percent is not None else None,
        'mean_execution_time_sec':mean([r['duration_sec'] for r in valid]),
        'median_execution_time_sec':statistics.median([r['duration_sec'] for r in valid]) if valid else None,
        'mean_agent_execution_time_sec':mean([r['agent_execution_sec'] for r in valid if r['agent_execution_sec'] is not None]),
        'total_input_tokens':sum(r['input_tokens'] or 0 for r in valid),
        'total_output_tokens':sum(r['output_tokens'] or 0 for r in valid),
        'total_harness_estimated_cost_usd':sum(r['cost_usd'] or 0 for r in valid) if valid else None,
        'cost_is_billing_receipt':False,'paid_fallback_used':False,
        'infrastructure_interruptions_excluded':len(interrupted),
        'target_assessment':target,'strict_40_to_60_percent_met':complete and 40<=percent<=60,
        'approximate_3_to_5_out_of_8_range_met':complete and 3<=successes<=5,
        'status':'COMPLETED' if complete else summary['status'],'attempts':rows,
        'overall_analysis':reviews.get('_overall',{'common_failure_patterns':'Pending completed trials and manual review.',
            'hardest_mathematical_concepts':'Not established by valid trajectories yet.',
            'recommendations':'Do not modify the task from infrastructure errors.'})}
    dump(REPORTS/'calibration_report.json',report)
    lines=['# Mathematics task calibration report','',
        f"Task v0.1.3, unchanged: `{manifest['native_checksum']}`.",
        f"Model: **{manifest['model']}**; installed native Terminus-2 **2.0.0**; parser **{report['parser_name']}**.",'',
        f"Status: **{report['status']}**. Valid calibration trials: **{len(valid)}/8**. Separate valid smoke: **{len(smoke)}**."]
    lines += [f"Successes: {successes}; failures: {len(valid)-successes}. Observed success rate: {percent:.2f}%; failure rate: {100-percent:.2f}%." if percent is not None else 'Success/failure rates are undefined because no valid calibration trial has completed.',
        '',f"Target assessment: **{target}**",'',
        'The smoke is excluded from the calibration denominator. HTTP errors and interrupted infrastructure runs are excluded. No missing trials are invented. Eight observations have substantial sampling uncertainty and do not establish a population success rate.', '',
        '| Phase / trial | Run | Result | Elapsed sec | Agent steps | Input / output tokens | Harness cost estimate USD |',
        '|---|---|---|---:|---:|---:|---:|']
    for row in attempts:
        cost='unavailable' if row['cost_usd'] is None else f"{row['cost_usd']:.6f}"
        lines.append(f"| {row['phase']} / {row['trial_number']} | {row['run_id']} | {row['status']} | {row['duration_sec']:.3f} | {row['steps']} | {row['input_tokens']} / {row['output_tokens']} | {cost} |")
    if valid:
        lines += ['',f"Mean valid-trial total time: {report['mean_execution_time_sec']:.3f} sec; median: {report['median_execution_time_sec']:.3f} sec. Times include API wait/backoff, setup, execution and grading; they are not pure mathematical compute time."]
    lines += ['', 'Costs are native harness catalogue estimates, not invoices or proof of payment. The user-confirmed free-tier project is used, and no paid fallback or billing upgrade is authorized. Runtime model aliases and catalogue metadata are preserved; immutable backend revision pinning is not claimed.', '',
        'Every trial uses a fresh native Harbor job/container, the identical task checksum, fixed model and agent configuration, and the protected separate offline verifier. Reference solution and hidden tests are not supplied to the agent. The mathematical task, reference solution and hidden evaluator were not modified.', '', '## Per-attempt review','']
    for item in rows:
        review=item['review']
        lines += [f"### {item['run_id']} ({item['status']})",'',
            f"Review status: {review.get('review_status','PENDING')}.",
            f"Mathematical mistakes: {review.get('mathematical_mistakes','Pending')}",
            f"Debugging/implementation mistakes: {review.get('implementation_mistakes','Pending')}",
            f"Final-answer verification: {review.get('verification','Pending')}",
            f"Exact outcome reason: {review.get('final_reason',item['failure_reason'])}",
            f"Trajectory: `{item['trajectory_path']}`.",f"Native result: `{item['result_path']}`.",'']
    lines += ['## Overall analysis','',json.dumps(report['overall_analysis'],indent=2), '',
        'Full raw configurations, results, grader CTRF/pytest logs, submitted source artifacts, terminal observations, ATIF trajectories and transport events remain in the named batch directory. Earlier Hydrogen/Flash/3.6 configurations and interruptions remain separate and are not pooled. Connection evidence and official sources: connection_recovery.md.', '',
        'Flash-Lite is a smaller fallback model. These measurements apply to this model/agent configuration and do not establish performance for unavailable frontier Gemini models. All-pass/all-fail samples must be investigated before proposing any difficulty change; no change is performed automatically.']
    (REPORTS/'calibration_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['status','total_valid_trials','successful_trials','failed_trials','success_percentage','target_assessment']}))

if __name__=='__main__': main()