"""Prepare pending cohort/approval records, without launching anything."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def dump(name,x):(HERE/name).write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
sources=[]
for name,digest in {
 'GSE273600_Control_Conditions_Raw_Counts.txt.gz':'51f64fd0c058c60ab1c0f2c76a35ba00567d36baf06c9313b3b3dda8e42eab86',
 'GSE273600_Control_Conditions_TPMs.txt.gz':'40cc660c3e565e5070bd7e9ec6858bf348cc5e77188c99112d7239a38c940a2f'}.items():
 p=ROOT/'shared-inputs/original-read-only-data'/name
 sources.append({'filename':name,'official_url':'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE273nnn/GSE273600/suppl/'+name,'sha256':digest,'bytes':p.stat().st_size,'local_source':str(p),'license_for_unrestricted_redistribution':'NOT ESTABLISHED','required_before_use':'Operator verifies applicable source rights/terms and exact file integrity. Local acquisition is not a rights grant.'})
dump('source_acquisition_manifest.json',{'dataset':'GSE273600','client_date':'2026-11-26','mode':'PROPOSED SOURCE-ONLY RELEASE / OPERATOR LOCAL ACQUISITION','files':sources,'article_license':'CC BY-NC-ND 4.0; not automatically a matrix license','public_distribution_authorized':False,'derivatives_requiring_review':['anonymous scaled atlas','synthetic query mixtures','gene metadata','model trajectories containing expression excerpts'],'rights_sources':['https://www.ncbi.nlm.nih.gov/home/about/policies/','https://www.ncbi.nlm.nih.gov/geo/info/disclaimer.html','https://www.nature.com/articles/s41467-024-52538-5']})
slots=[]
for repetition in range(1,6):
 for task in (1,2):
  slots.append({'schedule_position':len(slots)+1,'task':task,'trial':repetition,'task_version':'0.1.0' if task==1 else '0.2.0-PROPOSED','status':'NOT_STARTED_PENDING_APPROVAL','attempts':[],'binary_reward':None,'verifier_results':None,'steps':None,'wall_seconds':None,'input_tokens':None,'output_tokens':None,'failure_category':None})
dump('cohort_registry.json',{'status':'PENDING_EXPLICIT_USER_APPROVAL','model_api_calls_this_phase':0,'new_completed_trials_by_task':{'1':0,'2':0},'new_success_rates':{'1':None,'2':None},'reason':'User explicitly requires approval before frozen-task changes (item 1) and ten new model trials after usage review (item 5).','slots':slots})
files=[p for p in (HERE/'proposal').glob('*.patch')]+[HERE/'proposal/secure_fixture_rng.py',HERE/'CALIBRATION_PROTOCOL.md',HERE/'SEED_FIX_PROPOSAL.md',HERE/'DATA_ACQUISITION_AND_RIGHTS_STRATEGY.md',HERE/'resource_estimate.json']
dump('approval_scope.json',{'created_utc':datetime.now(timezone.utc).isoformat(),'status':'PENDING_USER_APPROVAL','requested_actions':['Create Task 2 v0.2.0 in a separate directory; preserve v0.1.1 and all original runtime/canonical/history paths','Apply reviewed secure-draw/private-replay repair, raw-minimum clarification and inclusive published numerical tolerances','Run stated offline scientific/native/isolation QC before model trials; stop on a genuine fixture defect without selecting for model failure','Run five fresh Gemini Harbor trials on unchanged Task 1 v0.1.0 and five on newly frozen Task 2 v0.2.0','Use current account only, under the resource estimate and $6 estimated usage allowance; no billing upgrade or paid-only fallback','Keep new project data/logs/versions/caches on F; existing Docker engine scratch storage remains disclosed separately'],'not_authorized':['Overwriting old tasks or historical outcomes','Publishing any task/data/image/trajectory archive','Sending rights inquiries','Relaxing valid science to alter success rates','Changing global Docker storage settings'],'reviewed_artifact_sha256':{str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'budget_usd_estimated_allowance':6,'frozen_task_changes_applied':False,'new_model_trials_started':False,'approval_must_be_explicit':'A preselected UI option, elapsed time, previous initial-trial authorization or this file does not constitute approval.'})
print('Prepared source-only acquisition manifest and 10 pending slots; no model calls or task changes')
