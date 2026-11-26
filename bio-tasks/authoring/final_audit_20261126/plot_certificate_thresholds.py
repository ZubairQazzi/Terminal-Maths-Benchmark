from trial_environment import configure,ROOT
configure()
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
folder=ROOT/'biology-task-1/authoring/reports/final_audit_20261126'
df=pd.read_csv(folder/'independent_rank_audit.tsv.gz',sep='\t')
stats=json.loads((folder/'independent_null_audit.json').read_text());m=stats['multiplicity']
ix=np.unique(np.r_[np.arange(250),np.geomspace(251,len(df),1500).astype(int)-1,len(df)-1])
view=df.iloc[ix];rank=view['rank'].to_numpy();p=view.p_joint.to_numpy()
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(9,5.2),layout='constrained')
ax.loglog(rank,p,color='#1f4f8a',lw=2.2,label='Observed sorted joint p values')
ax.loglog(rank,.05*rank/len(df),color='#b85c00',ls='--',lw=1.7,label='BH rejection threshold (diagnostic only)')
ax.loglog(rank,.05*rank/(len(df)*m['H_M']),color='#4c7a44',ls=':',lw=2,label='Required BY rejection threshold')
r=m['best_rank_for_uncapped_ratio'];p0=m['p_at_best_ratio_rank'];cut=m['BY_threshold_at_best_ratio_rank']
ax.annotate('',xy=(r,p0),xytext=(r,cut),arrowprops={'arrowstyle':'<->','color':'#333','lw':1.4})
ax.annotate(f"Best BY rank: {r}\nObserved p / cutoff = {p0/cut:.1f}",xy=(r,np.sqrt(p0*cut)),xytext=(r*2.6,cut*2.7),fontsize=10,bbox={'facecolor':'white','edgecolor':'none','alpha':.95,'pad':3},arrowprops={'arrowstyle':'-','color':'#555'})
ax.set(xlabel='Rank among 249,636 joint hypotheses',ylabel='Probability / rejection threshold',ylim=(7e-9,1.8),xlim=(1,len(df)*1.1))
ax.set_title('Task 1: no joint certificate crosses the required threshold',loc='left',fontweight='bold',pad=12)
ax.grid(which='major',alpha=.16);ax.legend(loc='lower right',frameon=False,fontsize=9)
fig.text(.012,-.035,'6,018 nominal joint p ≤ 0.05; 0 BH/BY discoveries. BY q values clip to 1.\nWorking-model arithmetic, not proof of absent biological responses.',fontsize=9,color='#444')
fig.savefig(folder/'joint_certificate_thresholds.png',dpi=180,bbox_inches='tight')
fig.savefig(folder/'joint_certificate_thresholds.svg',bbox_inches='tight')
print(folder/'joint_certificate_thresholds.png')
