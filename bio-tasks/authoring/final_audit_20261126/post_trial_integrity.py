"""Verify frozen source/canonical packages and pre-model evidence after trials."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
OUT=ROOT/'authoring/trajectories/initial-gemini35lite-high-20261126'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def digest(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest()
checks=[]
for i in (1,2):
    base=ROOT/f'biology-task-{i}';m=read(base/'authoring/reports/package_manifest.json')
    for directory in (base/'task',base/'authoring/package'/m['canonical_path']):
        for name,expected in m['files'].items():
            p=directory/name;actual=digest(p);assert actual==expected,str(p)
            checks.append({'path':str(p),'sha256':actual,'unchanged':True})
for name,expected in {
 'GSE273600_Control_Conditions_Raw_Counts.txt.gz':'51f64fd0c058c60ab1c0f2c76a35ba00567d36baf06c9313b3b3dda8e42eab86',
 'GSE273600_Control_Conditions_TPMs.txt.gz':'40cc660c3e565e5070bd7e9ec6858bf348cc5e77188c99112d7239a38c940a2f'}.items():
    for directory in (Path('C:/Users/zubai/Downloads'),ROOT/'shared-inputs/original-read-only-data'):
        p=directory/name;actual=digest(p);assert actual==expected,str(p)
        checks.append({'path':str(p),'sha256':actual,'unchanged':True})
gate=read(HERE/'pre_model_gate.json')
for name,expected in gate['evidence'].items():
    p=ROOT/name;actual=digest(p);assert actual==expected,str(p)
    checks.append({'path':str(p),'sha256':actual,'pre_model_evidence_preserved':True})
data=read(OUT/'initial_comparison.json');rows=data['attempts']
assert len(rows)==3
assert [sum(r['task']==i and r['status']!='INFRASTRUCTURE_INTERRUPTION' for r in rows) for i in (1,2)]==[1,1]
assert all((r.get('verifier_summary') or {}).get('tests')==11 for r in rows)
assert all(not r.get('exception') for r in rows if r['status']!='INFRASTRUCTURE_INTERRUPTION')
assert datetime.fromisoformat(gate['created_utc'])<datetime.fromisoformat(read(OUT/'manifest.json')['created_utc'])
assert all(str(value).upper().startswith('F:') for value in read(OUT/'manifest.json')['cache_locations'].values())
result={'utc':datetime.now(timezone.utc).isoformat(),'pass':True,'scope':'Frozen direct and canonical runtime file hashes, original downloads/shared inputs, pre-model evidence hashes, completed initial-run coverage and recorded configurable cache paths. This is integrity verification, not a new biological or originality certification.','checks':checks,'preserved_attempts':len(rows),'completed_diagnostic_trajectories_per_task':1,'scientific_requirements_changed':False,'release_status':'NOT FULLY CLEARED','conditional_task2_seed_warning_retained':True}
(HERE/'post_trial_integrity.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('Post-trial integrity PASS:',len(checks),'file/evidence hashes; 1 completed initial trajectory per task; 3 attempts preserved')
