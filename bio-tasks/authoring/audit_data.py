"""Physical matrix inspection and authoritative SOFT metadata reconciliation."""
from pathlib import Path
import gzip, hashlib, json, re
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'authoring'
matrices={}
report={}
for kind,suffix in [('counts','Raw_Counts'),('tpm','TPMs')]:
    p=ROOT/'shared-inputs/original-read-only-data'/f'GSE273600_Control_Conditions_{suffix}.txt.gz'
    with gzip.open(p,'rt') as f:
        df=pd.read_csv(f,sep='\t')
    matrices[kind]=df
    numeric=df.select_dtypes(include='number')
    x=numeric.to_numpy(float)
    report[kind]={'filename':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'shape':list(df.shape),'columns':df.columns.tolist(),'first_rows':df.iloc[:3,:5].to_dict('records'),'dtypes':df.dtypes.astype(str).value_counts().to_dict(),'numeric_shape':list(x.shape),'missing':int(df.isna().sum().sum()),'nonfinite':int((~np.isfinite(x)).sum()),'negative':int((x<0).sum()),'fractional':int((np.abs(x-np.rint(x))>1e-8).sum()),'zeros':int((x==0).sum()),'quantiles':np.quantile(x,[0,.25,.5,.75,.9,.99,1]).tolist(),'column_sums':dict(zip(numeric.columns,x.sum(axis=0).tolist())),'duplicate_first_identifier':int(df.iloc[:,0].duplicated().sum())}
soft=gzip.open(out/'sources/GSE273600_family.soft.gz','rt').read()
samples=[]
for block in soft.split('^SAMPLE = ')[1:]:
    gsm=block.splitlines()[0]
    fields={}
    for line in block.splitlines()[1:]:
        if line.startswith('!') and ' = ' in line:
            k,v=line.split(' = ',1); fields.setdefault(k,[]).append(v)
    samples.append({'gsm':gsm,'title':fields.get('!Sample_title',[''])[0],'characteristics':' | '.join(fields.get('!Sample_characteristics_ch1',[])),'source':fields.get('!Sample_source_name_ch1',[''])[0],'processing':' | '.join(fields.get('!Sample_data_processing',[]))})
pd.DataFrame(samples).to_csv(out/'gsm_metadata.csv',index=False)
report['soft']={'sha256':hashlib.sha256((out/'sources/GSE273600_family.soft.gz').read_bytes()).hexdigest(),'samples':len(samples),'first_samples':samples[:3]}
report['correspondence']={'same_columns':matrices['counts'].columns.tolist()==matrices['tpm'].columns.tolist(),'first_identifier_equal':matrices['counts'].iloc[:,0].equals(matrices['tpm'].iloc[:,0])}
(out/'data_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:{a:b for a,b in v.items() if a not in ('columns','column_sums','first_samples')} for k,v in report.items()},indent=2))
print(pd.DataFrame(samples).iloc[:8,:4].to_string(index=False))
