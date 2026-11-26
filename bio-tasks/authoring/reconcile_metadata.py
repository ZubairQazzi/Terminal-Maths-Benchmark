from pathlib import Path
import gzip,json,re
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
counts=pd.read_csv(ROOT/'shared-inputs/original-read-only-data/GSE273600_Control_Conditions_Raw_Counts.txt.gz',sep='\t',nrows=0)
tpm=pd.read_csv(ROOT/'shared-inputs/original-read-only-data/GSE273600_Control_Conditions_TPMs.txt.gz',sep='\t',nrows=0)
gsm=pd.read_csv(ROOT/'authoring/gsm_metadata.csv')
rows=[]
for col in counts.columns[1:]:
    line,treat,h,rep=re.fullmatch(r'(Parental|DmrPERK)_(UT|Dim|Ars|Tg)_(\d+)h_rep(\d+)',col).groups()
    matches=gsm[gsm.title.str.startswith(line+', ') & gsm.title.str.contains(', '+h+'h, replicate '+rep+'$',regex=True)]
    matches=matches[matches.title.str.contains({'UT':', UT,','Dim':', Dim ','Ars':', Arsenite ','Tg':', Thapsigargin '}[treat],regex=False)]
    if len(matches)!=1:
        raise ValueError((col,matches.title.tolist()))
    record=matches.iloc[0]
    dose={'UT':0,'Dim':.195,'Ars':.05,'Tg':100}[treat]
    rows.append(dict(sample_id=col,gsm=record.gsm,cell_line=line,treatment=treat,time_h=int(h),replicate=int(rep),dose=dose,dose_unit={'UT':'none','Dim':'nM','Ars':'mM','Tg':'nM'}[treat],geo_title=record.title))
assert counts.columns[1:].tolist()==tpm.columns[2:].tolist()
pd.DataFrame(rows).to_csv(ROOT/'authoring/sample_metadata.csv',index=False)
print(pd.DataFrame(rows).groupby(['cell_line','treatment','time_h']).size().to_string())
