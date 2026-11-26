"""Read-only runtime audit; write only new final-audit evidence files on F:."""
import csv
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import zipfile

sys.dont_write_bytecode = True
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
import numpy as np

ROOT = Path('F:/rl/bio')
OUT = ROOT/'biology-task-2/authoring/reports/final_audit_20261126'
SHARED = ROOT/'authoring/final_audit_20261126/provenance_originality'
OUT.mkdir(parents=True, exist_ok=True)
SHARED.mkdir(parents=True, exist_ok=True)

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()

def new_json(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2)

expected = {
    'GSE273600_Control_Conditions_Raw_Counts.txt.gz': '51f64fd0c058c60ab1c0f2c76a35ba00567d36baf06c9313b3b3dda8e42eab86',
    'GSE273600_Control_Conditions_TPMs.txt.gz': '40cc660c3e565e5070bd7e9ec6858bf348cc5e77188c99112d7239a38c940a2f'
}
hashes = []
for name, sha in expected.items():
    paths = [Path('C:/Users/zubai/Downloads')/name,
             ROOT/'shared-inputs/original-read-only-data'/name,
             ROOT/'biology-task-1/task/environment/data'/name,
             ROOT/'biology-task-1/task/tests/data'/name]
    if 'Raw_Counts' in name:
        paths += [ROOT/'biology-task-2/task/environment/data/estimated_counts.tsv.gz',
                  ROOT/'biology-task-2/task/tests/data/estimated_counts.tsv.gz']
    for path in paths:
        actual = digest(path)
        hashes.append({'path': str(path), 'bytes': path.stat().st_size,
                       'sha256': actual, 'matches_original': actual == sha})
assert all(r['matches_original'] for r in hashes)

canonical = []
for number, slug in [(1, 'specificity-under-missing-controls'), (2, 'transcript-provenance-audit')]:
    task = ROOT/f'biology-task-{number}/task'
    packages = ROOT/f'biology-task-{number}/authoring/package/tasks/life-sciences/biology'
    dirs = list(packages.iterdir())
    stage = dirs[0] if len(dirs) == 1 else packages/slug
    paths = sorted(p for p in task.rglob('*') if p.is_file())
    for path in paths:
        target = stage/path.relative_to(task)
        canonical.append({'task': number, 'relative_path': path.relative_to(task).as_posix(),
                          'sha256': digest(path), 'canonical_matches': target.is_file() and digest(path) == digest(target)})
assert all(r['canonical_matches'] for r in canonical)

contexts = []
for number in [1, 2]:
    env = ROOT/f'biology-task-{number}/task/environment'
    records = []
    for path in sorted(env.rglob('*')):
        if not path.is_file():
            continue
        record = {'path': path.relative_to(env).as_posix(), 'bytes': path.stat().st_size,
                  'sha256': digest(path), 'symlink': path.is_symlink()}
        if path.suffix == '.whl':
            with zipfile.ZipFile(path) as archive:
                names = archive.namelist()
                metadata_name = next(n for n in names if n.endswith('.dist-info/METADATA'))
                metadata = archive.read(metadata_name).decode('utf-8', 'replace')
                record['license_metadata'] = [line for line in metadata.splitlines()
                                              if line.startswith(('License:', 'License-Expression:', 'License-File:', 'Classifier: License'))]
                record['embedded_license_files'] = [n for n in names if 'license' in n.lower() or 'copying' in n.lower()]
                record['suspicious_private_names'] = [n for n in names if any(x in n.lower() for x in ('fixture_truth', 'bio2_reference', 'build_inputs.py'))]
        records.append(record)
    contexts.append({'task': number, 'context': str(env), 'files': records,
                     'private_oracle_or_fixture_paths': [r['path'] for r in records if any(x in r['path'].lower() for x in ('fixture_truth', 'solve.py', 'solution/', 'checks.py', 'test_outputs', 'build_inputs.py'))]})
assert not contexts[1]['private_oracle_or_fixture_paths']
assert not any(r.get('suspicious_private_names') for r in contexts[1]['files'])
new_json(SHARED/'source_and_runtime_checks.json', {'reviewer':'/root/qc_b','date':'2026-11-26','source_hash_checks':hashes,'canonical_runtime_checks':canonical,'build_contexts':contexts,'all_checks_pass':True,'scope':'Local source hashes, runtime/canonical identity and exact environment build-context inventory. Embedded software license metadata is recorded, not legal clearance.'})

data = ROOT/'biology-task-2/task/environment/data'
provenance = json.loads((data/'provenance.json').read_text())
with gzip.open(data/'estimated_counts.tsv.gz', 'rt') as stream:
    samples = next(csv.reader(stream, delimiter='\t'))[1:]
with (data/'sample_metadata.csv').open(newline='') as stream:
    metadata = list(csv.DictReader(stream))

# Conditional shortcut test: reproduce the non-public generation algorithm using
# the predictable accession-derived seed and visible dimensions/column labels.
# No expression entry is read or used in this section.
rng = np.random.default_rng(273600)
permutation = rng.permutation(len(samples))
scales = np.exp(rng.uniform(-1.1, 1.1, len(samples)))
mapping = {f'A{k:03d}': samples[j] for k,j in enumerate(permutation)}
groups = [tuple(sample.split('_')[:3]) for sample in samples]
chosen = []
for n in range(provenance['query_columns']):
    number = 1 if n < 6 else (2 if n < 18 else 3)
    donors = []
    while len(donors) < number:
        j = int(rng.integers(len(samples)))
        admissible = j not in donors and all(groups[j][1] != groups[k][1] for k in donors)
        if len(donors) == 1:
            admissible = admissible and groups[j][0] != groups[donors[0]][0]
        if admissible:
            donors.append(j)
    if number == 1:
        weights = [1.0]
    elif number == 2:
        alpha = float(rng.uniform(.25,.75))
        weights = [alpha,1-alpha]
    else:
        weights = [.38,.33,.29]
    rng.normal(0,.001,provenance['source_rows'])
    rng.uniform(-1.1,1.1)
    chosen.append({'class':'pure' if number == 1 else ('pair' if number == 2 else 'unsupported'),
                   'donors':[samples[j] for j in donors], 'weights':weights})
order = rng.permutation(len(chosen))
queries = [dict(chosen[i],query_id=f'Q{k:03d}') for k,i in enumerate(order)]
truth = json.loads((ROOT/'biology-task-2/task/tests/fixture_truth.json').read_text())
query_exact = queries == truth['queries']
atlas_exact = mapping == truth['mapping']
scales_exact = max(abs(float(scales[k])-truth['atlas_scales'][f'A{k:03d}']) for k in range(len(scales))) < 1e-14
assert query_exact and atlas_exact and scales_exact

visible = {'reviewer':'/root/qc_b','date':'2026-11-26',
 'provenance_keys':list(provenance), 'metadata_columns':list(metadata[0]),
 'metadata_rows':len(metadata),
 'explicit_seed_map_weights_fields_absent':not any(any(term in k.lower() for term in ('seed','mapping','weights','donors','permutation')) for k in provenance),
 'metadata_no_anonymous_atlas_query_join_keys':not any(k in metadata[0] for k in ('atlas_id','query_id','donor_1','donor_2')),
 'build_context_private_paths_absent':True,
 'image_observation_evidence':'authoring/reports/isolation_v011.json: actual UID1000 image probe found /tests and /solution absent, inputs not writable; Docker COPY is restricted to recorded context.',
 'predictable_seed_shortcut':{
   'status':'WARNING: predictable authoring seed / conditional shortcut',
   'assumption':'Attacker knows or correctly guesses non-public generator NumPy default_rng and draw/order conventions and seed equals accession digits273600.',
   'uses_expression_values':False,
   'visible_information_used':['GSE273600 accession','120 count sample column labels and order','57665 gene rows and24 queries from provenance','sample labels encode line/treatment/time groups'],
   'reconstructed_map_matches':atlas_exact,'reconstructed_120_map_entries':120,
   'reconstructed_query_labels_donors_weights_match':query_exact,'reconstructed_query_records':24,
   'reconstructed_atlas_scales_match':scales_exact,
   'limit':'Generation code/seed/map are absent from solver context. Accession alone does not specify RNG/order. This test demonstrates predictable-label weakness if conventions are known/guessed, not a literal answer field and not a complete passing answer: measured audit and numerical correlation/margin/residual certificates still require expression computations.',
   'action':'Preserve current validated task for authorized private trials; report shortcut limitation honestly. Any future anti-predictability redesign must be independently justified, versioned and revalidated, not tuned merely to force model failure.'}}
new_json(OUT/'task2_visible_inputs_and_shortcuts.json', visible)

# Exercise the actual trusted checker on new local fixtures. -B prevents writing
# caches to the immutable runtime. This execution is distinct from the oracle-
# independent scientific calculations preserved in the prior review.
spec = importlib.util.spec_from_file_location('final_b_checks', ROOT/'biology-task-2/task/tests/checks.py')
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)
checks.BASE = ROOT/'biology-task-2/task/tests/data'
checks.TRUTH = ROOT/'biology-task-2/task/tests/fixture_truth.json'
results = {}
for label in ['empty_files','header_only']:
    target = OUT/'trivial_cases'/label
    target.mkdir(parents=True,exist_ok=False)
    if label == 'empty_files':
        for name in ['alignment.tsv','queries.tsv','audit.json']:
            (target/name).write_text('')
    else:
        (target/'alignment.tsv').write_text('atlas_id\tsample_id\tdiscovery_correlation\tvalidation_correlation\tvalidation_margin\n')
        (target/'queries.tsv').write_text('query_id\tclassification\tdonor_1\tdonor_2\tfraction_1\tdiscovery_residual\tvalidation_residual\n')
        shutil.copyfile(ROOT/'biology-task-2/authoring/reports/oracle-output/audit.json',target/'audit.json')
    checks.SUB = target
    outcome = checks.evaluate()
    results[label] = {'passed':sum(v['passed'] for v in outcome.values()),'total':len(outcome),
                      'binary_reward':int(all(v['passed'] for v in outcome.values())), 'per_family':outcome}
    assert results[label]['binary_reward'] == 0
new_json(OUT/'trivial_submission_recheck.json', {'reviewer':'/root/qc_b','date':'2026-11-26','checker':'Current unchanged task/tests/checks.py; direct trusted evaluator execution; no submitted code executed','cases':results,'constant_and_noop_native_evidence':'Actual version0.1.1 native constant3/11,reward0 and no-op0/11,reward0; see final native trial directories.','vacuous_checks_note':'Empty tables may satisfy individual loop-only families vacuously. Mandatory schema/source-truth/completeness checks fail, so conjunctive binary reward remains0; no claim every family individually discriminates.'})
print(json.dumps({'original_hash_checks':len(hashes),'canonical_files':len(canonical),
                  'seed_replay_without_expression':atlas_exact and query_exact,
                  'trivial_cases':{k:{x:v[x] for x in ('passed','total','binary_reward')} for k,v in results.items()}}))
