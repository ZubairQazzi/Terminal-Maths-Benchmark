"""Update current handoff pointers without rewriting historical validation claims."""
from pathlib import Path
from datetime import datetime,timezone
import json
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
OUT=ROOT/'authoring/trajectories/initial-gemini35lite-high-20261126'
data=json.loads((OUT/'initial_comparison.json').read_text());rows=data['attempts']
auth_path=ROOT/'authoring/gemini_authorization.json';prior=json.loads(auth_path.read_text())
previous=prior.get('historical_pre_authorization_record',prior)
auth={'status':'AUTHORIZED INITIAL TRAJECTORIES COMPLETED','client_date':'2026-11-26','authorization_record':str(HERE/'authorization.json'),'audit_gate':str(HERE/'pre_model_gate.json'),'latest_report':str(ROOT/'FINAL_AUDIT_AND_INITIAL_GEMINI_RESULTS.md'),'model':data['model'],'completed_diagnostic_trajectories_per_task':{str(i):sum(r['task']==i and r['status']!='INFRASTRUCTURE_INTERRUPTION' for r in rows) for i in (1,2)},'preserved_attempts':len(rows),'instrumented_generate_content_requests':sum(r['provider_successful_calls']+len(r['provider_errors']) for r in rows),'successful_generate_content_requests':sum(r['provider_successful_calls'] for r in rows),'instrumented_provider_failures':sum(len(r['provider_errors']) for r in rows),'catalog_get_requests':1,'empirical_success_rate':'NOT CALIBRATED; one completed diagnostic trajectory per task is insufficient','frozen_scientific_requirements_unchanged':True,'public_redistribution_status':'NOT FULLY CLEARED','task2_conditional_seed_shortcut_warning':True,'actual_billing_invoice':'UNVERIFIED; SDK estimates are not receipts','historical_pre_authorization_record':previous}
auth_path.write_text(json.dumps(auth,indent=2)+'\n',encoding='utf-8')
historical=ROOT/'TWO_BIOLOGY_TASKS_FINAL_REPORT.md';text=historical.read_text(encoding='utf-8')
banner='> Historical creation-stage report: its no-provider/approval-pending statements describe the state before the user authorized initial Gemini trials. For the current audit, trajectories, rights/shortcut limitations and results, see [FINAL_AUDIT_AND_INITIAL_GEMINI_RESULTS.md](FINAL_AUDIT_AND_INITIAL_GEMINI_RESULTS.md).\n\n'
if not text.startswith('> Historical creation-stage report:'):historical.write_text(banner+text,encoding='utf-8')
outcome={'utc':datetime.now(timezone.utc).isoformat(),'client_date':'2026-11-26','audit_completed':True,'initial_trials_completed':True,'source_integrity':'PASS: 192 post-trial file/evidence hashes','completed_runs':[r['run_id'] for r in rows if r['status']!='INFRASTRUCTURE_INTERRUPTION'],'infrastructure_interruptions':[r['run_id'] for r in rows if r['status']=='INFRASTRUCTURE_INTERRUPTION'],'model_results_do_not_establish_extreme_difficulty':True,'public_redistribution':'NOT FULLY CLEARED','unqualified_task2_no_shortcut_certification':False,'latest_report':str(ROOT/'FINAL_AUDIT_AND_INITIAL_GEMINI_RESULTS.md'),'metrics':str(OUT/'initial_comparison.json'),'individual_checks':str(OUT/'individual_verifier_results.csv')}
(HERE/'final_outcome.json').write_text(json.dumps(outcome,indent=2)+'\n',encoding='utf-8')
print('Updated current authorization, historical-report pointer and final outcome')
