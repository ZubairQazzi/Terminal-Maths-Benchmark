"""Conditional seed shortcut with invented certificates; cannot prove full reward."""
import csv, gzip, importlib.util, json, os, sys
from pathlib import Path
sys.dont_write_bytecode=True
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import numpy as np

root=Path('F:/rl/bio/biology-task-2')
out=root/'authoring/reports/final_audit_20261126'
data=root/'task/environment/data'
meta=json.loads((data/'provenance.json').read_text())
with gzip.open(data/'estimated_counts.tsv.gz','rt') as stream:
    samples=next(csv.reader(stream,delimiter='\t'))[1:]
rng=np.random.default_rng(273600)
perm=rng.permutation(120)
rng.uniform(-1.1,1.1,120)
groups=[tuple(s.split('_')[:3]) for s in samples]
chosen=[]
for n in range(24):
    size=1 if n<6 else (2 if n<18 else 3)
    donors=[]
    while len(donors)<size:
        j=int(rng.integers(120))
        valid=j not in donors and all(groups[j][1]!=groups[k][1] for k in donors)
        if len(donors)==1:valid=valid and groups[j][0]!=groups[donors[0]][0]
        if valid:donors.append(j)
    if size==1:weights=[1.]
    elif size==2:
        f=float(rng.uniform(.25,.75));weights=[f,1-f]
    else:weights=[.38,.33,.29]
    rng.normal(0,.001,meta['source_rows']);rng.uniform(-1.1,1.1)
    chosen.append((size,donors,weights))
order=rng.permutation(24)
target=out/'trivial_cases/seed_only_invented_certificates'
target.mkdir(parents=True,exist_ok=False)
with (target/'alignment.tsv').open('w',newline='') as stream:
    writer=csv.writer(stream,delimiter='\t')
    writer.writerow(['atlas_id','sample_id','discovery_correlation','validation_correlation','validation_margin'])
    for k,j in enumerate(perm):writer.writerow([f'A{k:03d}',samples[j],1,1,1])
with (target/'queries.tsv').open('w',newline='') as stream:
    writer=csv.writer(stream,delimiter='\t')
    writer.writerow(['query_id','classification','donor_1','donor_2','fraction_1','discovery_residual','validation_residual'])
    for k,n in enumerate(order):
        size,donors,weights=chosen[n]
        if size==1:writer.writerow([f'Q{k:03d}','pure',samples[donors[0]],'',1,0,0])
        else:
            ranked=sorted(zip(weights,donors),reverse=True)
            fraction=ranked[0][0] if size==2 else ranked[0][0]/(ranked[0][0]+ranked[1][0])
            writer.writerow([f'Q{k:03d}','pair' if size==2 else 'unsupported',samples[ranked[0][1]],samples[ranked[1][1]],fraction,0,0 if size==2 else .1])
with (data/'genes.tsv').open(newline='') as stream:
    eligible=[r for r in csv.DictReader(stream,delimiter='\t') if r['eligible']=='1']
audit={'n_genes':meta['source_rows'],'n_count_samples':120,'n_atlas_samples':120,'n_queries':24,
       'fractional_count_entries':0,'eligible_discovery_genes':sum(r['split']=='discovery' for r in eligible),
       'eligible_validation_genes':sum(r['split']=='validation' for r in eligible),
       'atlas_minimum_by_column':{f'A{k:03d}':0 for k in range(120)},
       'biological_claims':{k:False for k in ['representations_are_independent_experiments','mixture_fraction_represents_cell_fraction','untreated_2h_control_exists','atf4_dependence_identified','original_series_contains_planted_contamination']}}
(target/'audit.json').write_text(json.dumps(audit))
# Only the trusted grader below reads expression values, as normal grading does.
spec=importlib.util.spec_from_file_location('seed_probe_checks',root/'task/tests/checks.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
checker.SUB=target
results=checker.evaluate()
report={'reviewer':'/root/qc_b','date':'2026-11-26','submission_reads_expression_values':False,
        'assumption':'Correctly guessed private generator RNG/draw conventions and accession-derived seed.',
        'certificates':'Invented fixed correlations/margins/residuals and unknown physical audit values; explicitly an incorrect negative probe.',
        'passed':sum(v['passed'] for v in results.values()),'total':len(results),
        'binary_reward':int(all(v['passed'] for v in results.values())), 'per_family':results,
        'conclusion':'Conditional seed replay reconstructs labels/weights, but full checker acceptance without expression analysis is NOT demonstrated. Scientific numerical certificates and audit checks reject these invented values.'}
assert report['binary_reward']==0
with (out/'seed_only_submission_probe.json').open('x') as stream:json.dump(report,stream,indent=2)
print(json.dumps({k:report[k] for k in ['passed','total','binary_reward','conclusion']}))
