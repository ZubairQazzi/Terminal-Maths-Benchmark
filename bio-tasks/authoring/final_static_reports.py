from pathlib import Path
import argparse,importlib.util,json,subprocess,sys,tomllib
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--task',type=int,required=True);p.add_argument('--suffix',required=True);a=p.parse_args()
base=ROOT/f'biology-task-{a.task}';task=base/'task';reports=base/'authoring/reports'
manifest=json.loads((reports/'package_manifest.json').read_text());staged=base/'authoring/package';canonical=staged/manifest['canonical_path']
other=ROOT/f'biology-task-{3-a.task}'/'task'
tool=staged/'ci_checks/check-similarity.py'
args=[sys.executable,str(tool),str(canonical),str(ROOT/'authoring/sources/terminal-bench/tasks'),str(ROOT/'authoring/sources/terminal-bench/lite'),str(other)]
r=subprocess.run(args,capture_output=True,text=True,timeout=120)
(reports/f'upstream_instruction_similarity_{a.suffix}.log').write_text('COMMAND '+json.dumps(args)+'\n'+r.stdout+r.stderr+'\nEXIT '+str(r.returncode),encoding='utf-8')
spec=importlib.util.spec_from_file_location('pinned_similarity',tool);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
refs={}
for directory in (ROOT/'authoring/sources/terminal-bench/tasks',ROOT/'authoring/sources/terminal-bench/lite',other):
    refs.update({str(directory)+':'+key:value for key,value in mod.load_instructions(directory,exclude_task=canonical.name).items()})
value,closest=mod.check_similarity((task/'instruction.md').read_text(),refs)
(reports/f'upstream_similarity_{a.suffix}.json').write_text(json.dumps({'similarity_pct':value*100,'closest':closest,'references':len(refs),'threshold_pct':mod.SIMILARITY_THRESHOLD*100,'exit_code':r.returncode,'method':'Actual pinned check-similarity.py, raw instructions, max_features5000 unigram/bigram TF-IDF fitted on references, including other task'},indent=2))
lint_path=reports/f'harbor_lint_all_{a.suffix}.log'
lint_text=lint_path.read_text();lint_clean='\n[]\n' in lint_text and 'EXIT 0 ' in lint_text
required=['instruction.md','task.toml','environment/Dockerfile','solution/solve.sh','tests/test.sh']
rows=[{'id':'entry-files','requirement':'All five required entry files exist.','status':'PASS' if all((task/n).is_file() for n in required) else 'FAIL','evidence':'Direct existence check: '+', '.join(required),'file':'task.toml','line':1},
{'id':'config-fields','requirement':'Supported Harbor schema fields and structure.','status':'PASS' if lint_clean else 'FAIL','evidence':lint_path.name+'; actual Harbor0.27 lint --select ALL includes invalid-task-config/unknown-config-field','file':'task.toml','line':2}]
requirements={}
checklist=(ROOT/'authoring/QC-CHECKLIST.md').read_text()
import re
for line in checklist.splitlines():
    m=re.match(r'- \*\*(.*?)\*\* \(`([^`]+)`\)\. (.*)',line)
    if m:requirements[m[2]]=m[1]+': '+m[3]
shell=json.loads((reports/f'upstream_static_{a.suffix}.json').read_text())
file_for={'task-fields':'task.toml','task-path':'task.toml','task-structure':'task.toml','task-slug':'task.toml','task-readme':'README.md','canary':'instruction.md','task-absolute-path':'instruction.md','instruction-suffix':'instruction.md','test-file-references':'instruction.md','dockerfile-references':'environment/Dockerfile','dockerfile-sanity':'environment/Dockerfile','dockerfile-platform':'environment/Dockerfile','allow-internet':'task.toml','separate-verifier':'task.toml','compose-host-binds':'environment/Dockerfile','task-timeout':'task.toml','gpu-types':'task.toml','task-resources':'task.toml','verifier-resources':'task.toml','nproc':'environment/Dockerfile','verifier-tooling-baked':'tests/Dockerfile','trial-network-fetch':'tests/test.sh','pip-pinning':'environment/requirements.txt','pytest-version':'tests/requirements.txt','test-sh-sanity':'tests/test.sh','binary-reward':'tests/test.sh'}
for x in shell:
    file=file_for[x['id']]
    rows.append({'id':x['id'],'requirement':requirements.get(x['id'],x['id']),'status':x['status'],'evidence':f"upstream_static_{a.suffix}.json, rule {x['id']}; exact pinned shell exit {x['exit_code']}",'file':file,'line':1,'stdout_stderr':x['output'],'warning_present':bool(re.search(r'\bWARN\b',x['output']))})
rows.append({'id':'instruction-similarity','requirement':requirements['instruction-similarity'],'status':'PASS' if r.returncode==0 and refs else 'FAIL','evidence':f'Actual pinned similarity rule: {value*100:.6f}% against {len(refs)} reference instructions; closest {closest}; substantive30% audit separately recorded.','file':'instruction.md','line':1})
assert len(rows)==29 and len({x['id'] for x in rows})==29
for row in rows:
    row['correction']='None required in this final snapshot' if row['status']=='PASS' else 'Investigate and correct failing requirement'
    row['post_correction_result']=row['status']
    row['absolute_file']=str(task/row['file'])
data={'task':a.task,'profile':'Supplied local QC checklist; pinned customized upstream scripts from existing workspace; actualHarbor0.27.0 lintALL','canonical_task_path':str(canonical),'note':'Canonical package bytes match the user-facing task runtime via package_manifest.json. Original nested task folder remains independently runnable. Local static results are not external QC panel approval. Earlierfailedchecks/logs retained.','counts':{s:sum(x['status']==s for x in rows) for s in ('PASS','FAIL','WARNING','NOT TESTED')},'checks':rows}
(reports/'static_qc.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
lines=['# Final static QC:29 independent checks','',data['note'],'',f"PASS {data['counts']['PASS']}/29; FAIL {data['counts']['FAIL']}; WARNING {data['counts']['WARNING']}; NOT TESTED {data['counts']['NOT TESTED']}.",'','| ID | Requirement | Status | File:line | Evidence / correction / recheck |','|---|---|---|---|---|']
for x in rows:lines.append('| '+x['id']+' | '+x['requirement'].replace('|','/')+' | '+x['status']+' | '+x['file']+':'+str(x['line'])+' | '+x['evidence'].replace('|','/')+'; '+x['correction']+'; recheck '+x['post_correction_result']+' |')
(reports/'static_qc.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(a.task,data['counts'],'raw pinned max instruction similarity',value*100)
