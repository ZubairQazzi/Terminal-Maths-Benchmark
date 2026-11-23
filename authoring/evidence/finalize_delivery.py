"""Local delivery consistency/inventory/credential audit; no API or container calls."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import tomllib
import winreg

ROOT=Path(__file__).resolve().parents[2]
REPORTS=ROOT/'authoring/reports'
TASK=ROOT/'tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure'

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write_json(path,value):
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')

def files():
    return [p for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']

def main():
    required=['README.md','REPRODUCING.md','authoring/project_brief.md',
        'authoring/task_proposal.md','authoring/reference_analysis.md',
        'authoring/math_research_review.md','authoring/originality_assessment.md',
        'authoring/plagiarism/reports/plagiarism_report.md',
        'authoring/plagiarism/reports/plagiarism_report.json',
        'authoring/reports/evaluator_coverage.md','authoring/reports/harbor_validation.md',
        'authoring/reports/qc_audit.md','authoring/reports/implementation_rubric_audit.md',
        'authoring/reports/trajectory_analysis.md','authoring/reports/final_delivery_status.json',
        'authoring/trajectories/trajectory_summary.json',
        'authoring/trajectories/trajectory_summary.csv','authoring/trajectories/calibration_manifest.json']
    checks=[]
    def check(name,condition):
        checks.append({'check':name,'status':'PASS' if condition else 'FAIL'})
        assert condition,name
    check('required_deliverables_exist',all((ROOT/p).is_file() for p in required))
    check('exactly_one_task',len(list((ROOT/'tasks').rglob('task.toml')))==1)
    check('final_task_version',tomllib.loads((TASK/'task.toml').read_text())['task']['version']=='0.1.3')
    expected=load(ROOT/'authoring/task_file_manifest.json')
    actual={p.relative_to(TASK).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(TASK.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    check('task_file_hashes_unchanged_since_validation',actual==expected)
    framed=hashlib.sha256()
    for name in sorted(actual):
        framed.update(name.encode()+b'\0'+(TASK/name).read_bytes()+b'\0')
    # Use the original platform Path ordering for the author-framed batch digest.
    framed=hashlib.sha256()
    for p in sorted(TASK.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':
            framed.update(p.relative_to(TASK).as_posix().encode()+b'\0'+p.read_bytes()+b'\0')
    manifest=load(ROOT/'authoring/trajectories/calibration_manifest.json')
    check('frozen_calibration_digest',framed.hexdigest()==manifest['task_digest'])
    qc=load(REPORTS/'qc_audit.json')
    summary=load(ROOT/'authoring/trajectories/trajectory_summary.json')
    final=load(REPORTS/'final_delivery_status.json')
    check('five_actual_native_validation_trials',len(qc['trials'])==5)
    check('all_native_task_checksums_match',all(t['task_checksum']==final['harbor_task_checksum'] for t in qc['trials']))
    check('calibration_reports_consistent',summary['completed_trials']==final['completed_valid_calibration_trials']==qc['calibration_completed']==0)
    check('interruption_not_counted_as_mathematical_failure',summary['failed_trials']==0 and summary['interrupted_trials']==1 and summary['success_percentage'] is None)
    native=load(Path(summary['trials'][0]['result_path']))
    check('native_exception_policy_invalidates_raw_reward',native['exception_info']['policy']['has_valid_reward'] is False)
    check('native_agent_result_has_no_usable_model_steps',summary['trials'][0]['steps']==0)
    check('eight_commands_planned_not_fabricated_results',len(manifest['commands'])==8 and len(summary['trials'])==1)
    (REPORTS/'task_directory_tree.txt').touch(exist_ok=True)
    links=re.findall(r'\]\(([^)]+)\)',(ROOT/'README.md').read_text(encoding='utf-8'))
    check('readme_local_links_resolve',all((ROOT/link).exists() for link in links if '://' not in link))
    for name in ['run_fresh_flash_calibration.py','refresh_reports.py','finish_docs.py','finalize_delivery.py']:
        path=ROOT/'authoring/evidence'/name
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check('report_and_future_batch_utilities_compile_without_execution',True)
    secrets=set()
    names=['GEMINI_API_KEY','GOOGLE_API_KEY','MSWEA_API_KEY']
    for name in names:
        if os.environ.get(name):
            secrets.add(os.environ[name])
    for hive,subkey in [(winreg.HKEY_CURRENT_USER,'Environment'),
        (winreg.HKEY_LOCAL_MACHINE,r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment')]:
        try:
            with winreg.OpenKey(hive,subkey) as registry:
                for name in names:
                    try:
                        value,_=winreg.QueryValueEx(registry,name)
                        if isinstance(value,str) and value:
                            secrets.add(value)
                    except FileNotFoundError:
                        pass
        except FileNotFoundError:
            pass
    check('configured_credentials_available_for_literal_scan',bool(secrets))
    needles={s.encode(encoding) for s in secrets for encoding in ['utf-8','utf-16le','utf-16be']}
    scanned=files()
    matches=[]
    unreadable=[]
    generic=[]
    for path in scanned:
        try:
            data=path.read_bytes()
            if any(needle in data for needle in needles):
                matches.append(path.relative_to(ROOT).as_posix())
            if re.search(rb'AIza[0-9A-Za-z_-]{30,}',data):
                generic.append(path.relative_to(ROOT).as_posix())
        except OSError:
            unreadable.append(path.relative_to(ROOT).as_posix())
    credential={'generated_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'All regular project files excluding Python caches; configured Gemini/Google/MSWEA credentials checked literally in UTF-8 and UTF-16 plus Google-key pattern.',
        'files_scanned':len(scanned),'configured_values_checked':len(secrets),
        'literal_matches':matches,'google_key_pattern_matches':generic,'unreadable_files':unreadable,
        'passed':not(matches or generic or unreadable),'secret_values_logged':False}
    write_json(REPORTS/'credential_exposure_audit.json',credential)
    check('no_project_credential_matches_or_unreadable_files',credential['passed'])
    report={'generated_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS',
        'checks':checks,'api_calls_made':False,'docker_runs_made':False,
        'calibration_complete':False,'remaining_blocker':'Official provider HTTP 503; zero of eight valid primary trials completed.'}
    write_json(REPORTS/'delivery_consistency_audit.json',report)
    inventory=REPORTS/'task_directory_tree.txt'
    inventory.touch(exist_ok=True)
    file_manifest=REPORTS/'delivery_file_manifest.json'
    file_manifest.touch(exist_ok=True)
    all_files=files()
    tree=['F:/rl/math-benchmark/','',f'Total files: {len(all_files)} (Python caches excluded).','']
    tree.extend(p.relative_to(ROOT).as_posix() for p in all_files)
    inventory.write_text('\n'.join(tree)+'\n',encoding='utf-8')
    (ROOT/'authoring/task_directory_tree.txt').write_text('\n'.join(tree)+'\n',encoding='utf-8')
    hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in all_files if p!=file_manifest}
    write_json(file_manifest,{'generated_utc':datetime.now(timezone.utc).isoformat(),
        'algorithm':'SHA-256','scope':'Every regular project file except this self-referential manifest and Python caches.',
        'file_count':len(hashes),'files':hashes})
    print(json.dumps({'consistency_checks':len(checks),'status':'PASS','project_files':len(all_files),
        'credential_files_scanned':len(scanned),'credential_matches':0,
        'task_digest_unchanged':True,'calibration_completed_valid':0,'calibration_requested':8}))

if __name__=='__main__':
    main()