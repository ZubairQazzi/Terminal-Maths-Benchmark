"""Post-run diagnosis only. Never imported into the solver environment."""
from pathlib import Path
import csv,gzip,json

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'authoring/trajectories/initial-gemini35lite-high-20261126'
trial=next((OUT/'jobs/bio2-initial-01').glob('*/result.json')).parent
submitted=json.loads((trial/'artifacts/app/submission/audit.json').read_text())
source=ROOT/'biology-task-2/task/environment/data/atlas_tpm.tsv.gz'
with gzip.open(source,'rt',newline='') as f:
    reader=csv.reader(f,delimiter='\t');columns=next(reader)[1:]
    minimum=[float('inf')]*len(columns);totals=[0.0]*len(columns);n=0
    for row in reader:
        n+=1
        for i,text in enumerate(row[1:]):
            value=float(text);minimum[i]=min(minimum[i],value);totals[i]+=value
rows=[]
for i,col in enumerate(columns):
    actual=float(submitted['atlas_minimum_by_column'][col]);expected=minimum[i]
    normalized=expected*1e6/totals[i]
    rows.append({'atlas_id':col,'submitted_minimum':actual,'required_supplied_minimum':expected,'normalized_minimum':normalized,'absolute_error_vs_required':abs(actual-expected),'absolute_error_vs_normalized':abs(actual-normalized),'fails_required_1e_7_tolerance':abs(actual-expected)>=1e-7})
with (OUT/'bio2-initial-01-minimum_diagnostic.tsv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');writer.writeheader();writer.writerows(rows)
result={'run_id':'bio2-initial-01','source':str(source),'submission':str(trial/'artifacts/app/submission/audit.json'),'rows_read':n,'atlas_columns':len(columns),'columns_failing_supplied_minimum':sum(r['fails_required_1e_7_tolerance'] for r in rows),'max_error_vs_normalized_minimum':max(r['absolute_error_vs_normalized'] for r in rows),'max_error_vs_required_minimum':max(r['absolute_error_vs_required'] for r in rows),'example':rows[0],'diagnosis':'The submitted source explicitly uses A[col].min() after normalizing atlas columns, while the published audit contract requires the supplied scaled atlas minimum. All identity, mixture, support and residual-certificate checks passed. This is representation bookkeeping, not evidence of failed mixture inference.'}
assert result['columns_failing_supplied_minimum']==120
assert result['max_error_vs_normalized_minimum']<1e-12
(OUT/'bio2-initial-01-minimum_diagnostic.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
