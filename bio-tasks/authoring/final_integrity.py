from pathlib import Path
import hashlib,json,tomllib
ROOT=Path(__file__).resolve().parents[1]
records=[]
def record(path,expected=None,label=None):
    p=Path(path);digest=hashlib.sha256(p.read_bytes()).hexdigest()
    if expected is not None:assert digest==expected,(p,digest,expected)
    row={'path':str(p),'bytes':p.stat().st_size,'sha256':digest,'label':label,'matches_expected':True if expected else None};records.append(row);return digest
for name in ('GSE273600_Control_Conditions_Raw_Counts.txt.gz','GSE273600_Control_Conditions_TPMs.txt.gz'):
    original=Path('C:/Users/zubai/Downloads')/name;digest=record(original,label='User supplied original')
    record(ROOT/'shared-inputs/original-read-only-data'/name,digest,'Preserved shared source')
    for part in ('environment','tests'):
        record(ROOT/'biology-task-1/task'/part/'data'/name,digest,'Task1 independent runnable copy')
    if 'Raw_Counts' in name:
        record(ROOT/'biology-task-2/task/environment/data/estimated_counts.tsv.gz',digest,'Task2 source counts')
        record(ROOT/'biology-task-2/task/tests/data/estimated_counts.tsv.gz',digest,'Task2 verifier source counts')
for i in (1,2):
    base=ROOT/f'biology-task-{i}';source=base/'task'
    manifest=json.loads((base/'authoring/reports/package_manifest.json').read_text())
    stage=base/'authoring/package'/manifest['canonical_path']
    for rel,expected in manifest['files'].items():
        record(source/rel,expected,'Runtime source frozen');record(stage/rel,expected,'Canonical byte-equivalent package')
    cfg=tomllib.loads((source/'task.toml').read_text());assert cfg['verifier']['environment_mode']=='separate';assert cfg['verifier']['environment']['network_mode']=='no-network';assert cfg['artifacts']==['/app/submission']
profile=ROOT/'authoring/qc_profile'
profile_hashes={p.relative_to(profile).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in profile.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
(ROOT/'authoring/qc_profile_manifest.json').write_text(json.dumps(profile_hashes,indent=2))
data={'date':'2026-11-26','pass':True,'records':records,'task2_tpm_note':'Original TPM preserved in shared sources; runnable Task2 uses deterministic anonymous/scaled compositional derivatives and explicit synthetic aliquots. Source and transformation hashes are in its provenance records; no unmodified labeled TPM is leaked to its solver.','scope':'Original downloads, all direct count/TPM copies, frozen source/canonical runtime hashes, separate verifier declarations and artifact paths checked. Logs/reviewer reports are not disguised as runtime inputs.'}
(ROOT/'authoring/data_integrity_final.json').write_text(json.dumps(data,indent=2))
print('Final source/canonical integrity PASS;',len(records),'file checks;',len(profile_hashes),'QC tooling hashes')
