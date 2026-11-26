"""Serialize remaining heavy native validation, preserving per-command logs."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
commands=[
 ['native_validation.py','harbor','--task','1','--suffix','v010r2','--agents','wrong_sample_alignment'],
 ['native_validation.py','build','--task','2','--suffix','v011'],
 ['native_validation.py','harbor','--task','2','--suffix','v011','--agents','oracle,nop,constant,hardcoded,wrong_alignment,wrong_contrast,wrong_statistics,incomplete,unsupported_forced_pair,invalid_claims,alternative'],
 ['isolation_probes.py','--task','2','--suffix','v011'],
 ['native_validation.py','static','--task','1','--suffix','v010r2'],
 ['final_static_reports.py','--task','1','--suffix','v010r2'],
 ['native_validation.py','static','--task','2','--suffix','v011r1'],
 ['final_static_reports.py','--task','2','--suffix','v011r1'],
 ['summarize_native.py','--task','1','--final-prefix','v010'],
 ['summarize_native.py','--task','2','--final-prefix','v011'],
 ['final_originality_reports.py']]
for command in commands:
    print('PHASE',*command,flush=True)
    subprocess.run([sys.executable,'-X','utf8','-B',str(ROOT/'authoring'/command[0])]+command[1:],cwd=ROOT,check=True)
print('REMAINING NATIVE BATCH FINISHED',flush=True)
