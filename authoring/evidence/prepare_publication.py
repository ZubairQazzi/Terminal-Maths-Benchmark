"""Prepare a static, credential-checked publication snapshot; never alter the task."""
from datetime import datetime,timedelta,timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import time
import winreg

SOURCE=Path(r'F:/rl/math-benchmark')
DEST=Path(r'F:/rl/Task-1-maths')
TASK=Path('tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure')
EXPECTED='28b89df5a40a09efbaa8eec4fa36e2458960b18020aff314bfcb6634ceb076f5'

def sha(data): return hashlib.sha256(data).hexdigest()
def load(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def dump(path,value): path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def frozen_digest(root):
    h=hashlib.sha256()
    for p in sorted(root.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':
            h.update(p.relative_to(root).as_posix().encode()+b'\0'+p.read_bytes()+b'\0')
    return h.hexdigest()

def omitted(rel):
    names=set(rel.parts)
    if names & {'.git','__pycache__','.pytest_cache','.venv','.vscode'}: return True
    if rel.name.startswith('.env') or rel.suffix.lower() in {'.pem','.key','.pyc','.pyo','.log','.cast'}: return True
    if rel.name.lower() in {'credentials.json','secrets.json','token.json','github_access_check.json'}: return True
    s=rel.as_posix()
    if s.startswith('authoring/reports/harbor-jobs/'): return True
    if s.startswith('authoring/trajectories/') and 'jobs' in rel.parts: return True
    if 'flash_v012_operator_snapshot' in rel.parts: return True
    if s.startswith('authoring/trajectories/connection-recovery-20261123/'): return True
    return False

def clean_metadata(value):
    if isinstance(value,dict):
        return {k:('[omitted from public snapshot; original retained locally]' if k in {'exception_traceback','thoughtSignature','thought_signature'} else clean_metadata(v)) for k,v in value.items()}
    if isinstance(value,list): return [clean_metadata(v) for v in value]
    return value

def main():
    assert (DEST/'.git').is_dir()
    assert frozen_digest(SOURCE/TASK)==EXPECTED,'Source task differs from validated v0.1.3.'
    assert not (DEST/'PUBLICATION_MANIFEST.json').exists(),'Refusing to overwrite a prepared snapshot.'
    started=datetime.now(timezone.utc).isoformat(); copied=[]; excluded=[]
    for path in sorted(SOURCE.rglob('*')):
        if not path.is_file(): continue
        rel=path.relative_to(SOURCE)
        if omitted(rel): excluded.append(rel.as_posix());continue
        data=path.read_bytes(); projected=False
        if path.suffix=='.json' and TASK not in rel.parents:
            for attempt in range(4):
                try:
                    obj=json.loads(data.decode('utf-8-sig'));break
                except (UnicodeDecodeError,json.JSONDecodeError):
                    if attempt==3: raise
                    time.sleep(0.1);data=path.read_bytes()
            cleaned=clean_metadata(obj)
            if cleaned!=obj:
                published=(json.dumps(cleaned,indent=2)+'\n').encode();projected=True
            else: published=data
        else: published=data
        target=DEST/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(published)
        copied.append({'path':rel.as_posix(),'source_sha256':sha(data),'published_sha256':sha(published),'metadata_projection':projected})
    assert frozen_digest(DEST/TASK)==EXPECTED,'Snapshot changed the task bytes.'
    evidence=DEST/'authoring/public_evidence';evidence.mkdir(parents=True,exist_ok=True)
    qc=load(SOURCE/'authoring/reports/qc_audit.json'); native=[]
    for row in qc['trials']:
        path=Path(row['result_path']); raw=path.read_bytes(); result=json.loads(raw)
        ctrf_path=path.parent/'verifier/ctrf.json'; ctrf=load(ctrf_path)['results']
        native.append({'job':row['job'],'trial_name':result['trial_name'],'task_checksum':result['task_checksum'],
            'started_at':result['started_at'],'finished_at':result['finished_at'],'agent_info':result['agent_info'],
            'verifier_environment_mode':result['verifier_environment_mode'],'verifier_result':result['verifier_result'],
            'exception_info':result['exception_info'],'ctrf_summary':ctrf['summary'],
            'original_native_result_sha256':sha(raw),'original_ctrf_sha256':sha(ctrf_path.read_bytes())})
    dump(evidence/'native_validation_results.json',{'projection':'Selected exact native fields; raw local logs retained. No model prompts or package source excerpts copied.','trials':native})
    diagnostics=[]
    folder=SOURCE/'authoring/trajectories/connection-recovery-20261123'
    for path in sorted(folder.glob('*.json')):
        if path.name=='model_catalog_and_configuration.json': continue
        doc=load(path)
        for row in doc.get('attempts',doc.get('requests',[])):
            body=row.get('response',{})
            diagnostics.append({'source_report':path.name,'source_sha256':sha(path.read_bytes()),
                'utc':row.get('utc'),'endpoint_path':row.get('path'),'status':row.get('status'),
                'elapsed_sec':row.get('elapsed_sec'),'error_status':body.get('error',{}).get('status'),
                'error_message':body.get('error',{}).get('message',body.get('message')),'usage_metadata':body.get('usageMetadata')})
    dump(evidence/'connection_diagnostics.json',{'raw_diagnostics_retained_locally':True,'observations':diagnostics})
    pointer=load(SOURCE/'authoring/trajectories/latest_calibration.json'); current=load(SOURCE/pointer['live_summary'])
    now=datetime.now(timezone(timedelta(hours=5))).isoformat()
    readme=f'''# Certified Kronecker Structure of Singular Matrix Pencils

One Mathematics benchmark task, **v0.1.3**, for Harbor and Terminal-Bench Science.

The agent must recover exact normal rank, finite Smith invariant factors, infinite elementary divisors, left/right minimal indices, and polynomial minimal-basis certificates for singular rectangular integer matrix pencils.

[Open the task](tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure/) · [Instructions](tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure/instruction.md) · [Full specification](tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure/environment/spec.md)

```text
tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure/
  task.toml
  instruction.md
  README.md
  environment/    # pinned Docker environment, specification and examples
  solution/       # mathematical reference solution
  tests/          # independent separate verifier and hidden-case construction
authoring/        # research, proposal, originality, validation and calibration reports
REPRODUCING.md
```

## Validation

Local Docker/Harbor validation passed: two oracle repeats and a correct executable-helper solution each passed **9/9 batches covering 36 pencils**. No-op and partial baselines scored **0**; the partial passed one batch. Isolation, leakage and lint checks passed. [Validation report](authoring/reports/harbor_validation.md) · [Native result projection](authoring/public_evidence/native_validation_results.json) · [QC audit](authoring/reports/qc_audit.md)

The validated task bytes are unchanged. Native Harbor checksum: `99a8da66bc504372c791300e6504ce522f6453cd90ad40dc9ce0ab971ae02cbe`. Author framing SHA-256: `{EXPECTED}`.

## Calibration status

**Incomplete.** Snapshot time: {now} (Asia/Karachi). Latest configured model: `{current['model']}` with Terminus-2 2.0.0. Recorded valid calibration trials: **{current['completed_valid_trials']}/8**. Recorded separate valid smoke attempts: **{current['smoke_valid_completed']}**. No 40-60% measured success-rate claim is made.

Earlier runs encountered Google HTTP 503 and a 20-requests/day free-tier quota. Infrastructure interruptions are not counted as Mathematics failures. [Connection diagnosis](authoring/reports/connection_recovery.md) · [Calibration report](authoring/reports/calibration_report.md) · [Latest batch pointer](authoring/trajectories/latest_calibration.json)

This is a static publication snapshot. Raw agent/session logs, live job directories and credential/access diagnostics remain in the original local project. Curated summaries, transport events and verifier-result projections are included. Prior local-only statements in historical reports reflect the earlier authorization; the user subsequently requested publication to this repository. See [publication scope](PUBLICATION.md).

## Supporting work

- [Task proposal](authoring/task_proposal.md)
- [Reference comparison](authoring/reference_analysis.md) and [mathematical research](authoring/math_research_review.md)
- [Originality assessment](authoring/originality_assessment.md) and [scoped similarity audit](authoring/plagiarism/reports/plagiarism_report.md)
- [Evaluator coverage](authoring/reports/evaluator_coverage.md)
- [Implementation rubric](authoring/reports/implementation_rubric_audit.md)
- [Reproduction on the original PC](REPRODUCING.md)

Originality percentages are scoped heuristics, not proof of global novelty. Independent domain review and demonstrated extreme difficulty remain open audit warnings. The project does not claim maintainer approval or independent expert authorship.
'''
    (DEST/'README.md').write_text(readme,encoding='utf-8')
    (DEST/'PUBLICATION.md').write_text(f'''# Publication scope

On 2026-11-23 the user explicitly requested a commit/push to https://github.com/zubairtariq174-design/Task-1-maths and confirmed the GitHub account zubairtariq174-design. This supersedes earlier no-GitHub/local-only scope statements; those are retained as historical records. No additional repository, hosted benchmark submission, container publication or paid API is requested.

Task v0.1.3, its mathematical reference solution and its hidden evaluator are preserved byte for byte. The prior Mathematics calibration goal is paused; this publication operation does not start a new agent trial. The earlier process-stop request was declined, so locally running job files can change after this static snapshot.

The snapshot contains the complete task and supporting authoring code/reports, curated calibration summaries and verifier results. Raw agent transcripts, full runtime job folders, console/build logs, package-source excerpts, local caches, access diagnostics and credentials are excluded. Full originals remain in F:/rl/math-benchmark. Published JSON metadata omits encrypted thought signatures and long exception tracebacks; source and published SHA-256 values in PUBLICATION_MANIFEST.json identify projections.

Snapshot started UTC: {started}. Snapshot completed Asia/Karachi: {now}.

The reference/hidden-evaluator files are part of the authoring repository. The task Docker build contexts continue to exclude them from the evaluated agent image. Publication does not change that runtime isolation.
''',encoding='utf-8')
    (DEST/'.gitignore').write_text('''__pycache__/
*.py[cod]
.pytest_cache/
.venv/
.vscode/
.env
.env.*
!.env.example
*.pem
*.key
credentials.json
secrets.json
token.json
*.log
*.cast
authoring/reports/github_access_check.json
authoring/reports/harbor-jobs/
authoring/trajectories/**/jobs/
authoring/trajectories/jobs/
authoring/trajectories/connection-recovery-20261123/
authoring/trajectories/flash_v012_operator_snapshot/
''',encoding='utf-8')
    (DEST/'.gitattributes').write_text('# Preserve byte-for-byte task and evidence hashes on every platform.\n* -text\n',encoding='utf-8')
    secrets=set()
    for name in ['GEMINI_API_KEY','GOOGLE_API_KEY','MSWEA_API_KEY','GITHUB_TOKEN','GH_TOKEN']:
        if os.environ.get(name): secrets.add(os.environ[name])
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER,'Environment') as registry:
        for name in ['GEMINI_API_KEY','GOOGLE_API_KEY','MSWEA_API_KEY','GITHUB_TOKEN','GH_TOKEN']:
            try:
                value,_=winreg.QueryValueEx(registry,name)
                if isinstance(value,str) and value: secrets.add(value)
            except FileNotFoundError: pass
    needles={s.encode(enc) for s in secrets for enc in ['utf-8','utf-16le','utf-16be']}
    matches=[];scanned=0
    for path in DEST.rglob('*'):
        if not path.is_file() or '.git' in path.relative_to(DEST).parts: continue
        data=path.read_bytes();scanned+=1
        if any(n in data for n in needles) or re.search(rb'AIza[0-9A-Za-z_-]{30,}|\b(?:ghp_|github_pat_|sk-proj-|sk-ant-)[0-9A-Za-z_-]{20,}',data): matches.append(path.relative_to(DEST).as_posix())
    assert not matches,'Credential-like content found in: '+', '.join(matches)
    audit={'checked_utc':datetime.now(timezone.utc).isoformat(),'files_scanned':scanned,'literal_and_pattern_matches':[],
        'credentials_logged':False,'task_digest_matches_validated_v013':True,'passed':True}
    dump(evidence/'publication_audit.json',audit)
    dump(DEST/'PUBLICATION_MANIFEST.json',{'snapshot_started_utc':started,'snapshot_completed_utc':datetime.now(timezone.utc).isoformat(),
        'task_author_digest':EXPECTED,'copied_source_files':copied,'excluded_local_files':excluded,
        'note':'README and publication/audit files are newly authored publication metadata. Raw originals stay local.'})
    print(json.dumps({'files_scanned':scanned,'copied_source_files':len(copied),'excluded_local_files':len(excluded),
        'credential_matches':0,'task_bytes_unchanged':True,'valid_calibration_trials_at_snapshot':current['completed_valid_trials']}))

if __name__=='__main__': main()