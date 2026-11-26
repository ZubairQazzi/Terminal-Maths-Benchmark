"""Local Docker/Harbor execution only; no model credentials are forwarded."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,os,shutil,subprocess,time,tomllib
ROOT=Path(__file__).resolve().parents[1]
UPSTREAM=ROOT/'authoring/qc_profile'
DOCKER=r'C:\Users\zubai\AppData\Local\Programs\DockerDesktop\resources\bin\docker.exe'
HARBOR=r'C:\Users\zubai\.local\bin\harbor.exe'
def run(args,log,cwd,env=None,allow_fail=False):
    log.parent.mkdir(parents=True,exist_ok=True)
    if log.exists():raise RuntimeError('Refuse log overwrite: '+str(log))
    start=time.monotonic()
    with log.open('w',encoding='utf-8') as f:
        f.write('COMMAND '+json.dumps([str(a) for a in args])+'\n');f.flush()
        status=subprocess.call([str(a) for a in args],cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
        f.write(f'\nEXIT {status} ELAPSED_SECONDS {time.monotonic()-start:.3f}\n')
    print(log.name,'exit',status,flush=True)
    if status and not allow_fail:raise RuntimeError(str(log))
    return status
def stage(base):
    source=base/'task';cfg=tomllib.loads((source/'task.toml').read_text(encoding='utf-8'))
    slug=cfg['task']['name'].split('/')[-1]
    staged=base/'authoring/package';dest=staged/'tasks/life-sciences/biology'/slug
    dest.mkdir(parents=True,exist_ok=True)
    spec=importlib.util.spec_from_file_location('local_readme',UPSTREAM/'tools/task-readme/generate.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    readme=source/'README.md';text=readme.read_text(encoding='utf-8')
    body=text.split('<!-- END MANAGED HEADER -->')[-1].lstrip('\n')
    # render() names the card from its canonical directory basename.
    shutil.copy2(source/'task.toml',dest/'task.toml')
    readme.write_text(mod.render(dest)+'\n'+body,encoding='utf-8',newline='\n')
    for name in ('task.toml','instruction.md','README.md','environment','solution','tests'):
        p=source/name
        if p.is_dir():shutil.copytree(p,dest/name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        else:shutil.copy2(p,dest/name)
    for name in ('ci_checks','tools'):
        shutil.copytree(UPSTREAM/name,staged/name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('test-tasks','__pycache__','*.pyc'))
    for name in ('task-readme-template.md','.github/reviewer-pool.yml'):
        p=staged/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(UPSTREAM/name,p)
    manifest={p.relative_to(source).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(source.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    for rel,digest in manifest.items():assert hashlib.sha256((dest/rel).read_bytes()).hexdigest()==digest
    (base/'authoring/reports/package_manifest.json').write_text(json.dumps({'source':str(source),'canonical_path':str(dest.relative_to(staged)).replace('\\','/'),'files':manifest},indent=2))
    return staged,dest,slug
def main():
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','build','static','harbor']);p.add_argument('--task',type=int,required=True,choices=[1,2]);p.add_argument('--suffix',required=True);p.add_argument('--agents',default='oracle,nop');p.add_argument('--image-tag',help='Use an existing verifier-image tag for static checks; defaults to the task version.');a=p.parse_args()
    base=ROOT/f'biology-task-{a.task}';report=base/'authoring/reports';source=base/'task'
    cfg=tomllib.loads((source/'task.toml').read_text());slug=cfg['task']['name'].split('/')[-1]
    staged=base/'authoring/package';dest=staged/'tasks/life-sciences/biology'/slug
    env=dict(os.environ);env['PATH']=str(Path(DOCKER).parent)+os.pathsep+env.get('PATH','');env['PYTHONPATH']=str(ROOT);env['PYTHONUTF8']='1';env['PYTHONIOENCODING']='utf-8';env['LITELLM_LOCAL_MODEL_COST_MAP']='True'
    for key in list(env):
        if any(s in key.upper() for s in ('API_KEY','AUTH_TOKEN','ACCESS_TOKEN','SECRET_KEY')):env.pop(key)
    if a.phase=='stage':
        staged,dest,slug=stage(base);print(dest);return
    if a.phase=='build':
        for part,label in [('environment','agent'),('tests','verifier')]:run([DOCKER,'build','--no-cache','-t',f'local-bio{a.task}-{label}:{a.suffix}',dest/part],report/f'clean_build_{label}_{a.suffix}.log',ROOT,env)
    elif a.phase=='static':
        run([HARBOR,'lint',dest,'--select','ALL','--json'],report/f'harbor_lint_all_{a.suffix}.log',ROOT,env,True)
        image_version=a.image_tag or 'v'+cfg['task']['version'].replace('.','')
        run([DOCKER,'run','--rm','--network','none','--mount','type=bind,source='+ROOT.as_posix()+',target=/work','-w',f'/work/biology-task-{a.task}/authoring/package',f'local-bio{a.task}-verifier:'+image_version,'python3','/work/authoring/static_checks.py','--task',str(a.task),'--suffix',a.suffix],report/f'static_{a.suffix}.log',ROOT,env,True)
    else:
        baseline_map=json.loads((base/'authoring/reports/native_baselines.json').read_text()) if (base/'authoring/reports/native_baselines.json').exists() else {}
        for label in a.agents.split(','):
            localenv=env.copy()
            agent=label if label in ('oracle','nop') else 'authoring.native_agents:FixtureAgent'
            if label not in ('oracle','nop'):
                if a.task==1:
                    if label=='wrong_sample_alignment':
                        records=json.loads((base/'authoring/reports/native_baseline_directories.json').read_text())
                        localenv['BIO_FIXTURE_DIR']=records[label];localenv['BIO_FIXTURE_TARGET']='/app/submission';localenv['BIO_FIXTURE_LABEL']=label
                    else:
                        classes={'alternative':'AlternativeAgent','constant':'ConstantAgent','hardcoded':'HardcodedAgent','label_shift':'LabelShiftAgent','wrong_contrast':'IncorrectAgent','omitted_adjustment':'NoAdjustmentAgent','saturated_shortcut':'SaturatedAgent','incomplete':'IncompleteAgent','invalid_interpretation':'InvalidInterpretationAgent'}
                        agent='authoring.evidence.baseline_agent:'+classes[label];localenv['PYTHONPATH']=str(base)
                else:
                    record=baseline_map[label];localenv['BIO_FIXTURE_DIR']=str(base/record['path']);localenv['BIO_FIXTURE_TARGET']=record.get('target','/app/submission');localenv['BIO_FIXTURE_LABEL']=label
            for attempt in range(1,4):
                tag=a.suffix if attempt==1 else a.suffix+f'-infra-retry{attempt}'
                job=f'bio{a.task}-{label}-{tag}'
                status=run([HARBOR,'run','--path',dest,'--agent',agent,'-k','2' if label=='oracle' else '1','--n-concurrent','1','--job-name',job,'--jobs-dir',report/'harbor-jobs','--quiet'],report/f'harbor_{label}_{tag}.log',ROOT,localenv,True)
                trials=list((report/'harbor-jobs'/job).glob('*/result.json'))
                records=[json.loads(x.read_text()) for x in trials]
                valid=bool(records) and len(records)==(2 if label=='oracle' else 1) and all(x.get('exception_info') is None and (x.get('verifier_result') or {}).get('rewards') for x in records)
                if status==0 and valid:break
                print('Infrastructure/incomplete run, not scientific failure:',job,flush=True)
                if attempt==3:raise RuntimeError('Bounded native retries exhausted: '+job)
                time.sleep(5)
                health=subprocess.run([DOCKER,'info','--format','{{.ServerVersion}}'],env=localenv,capture_output=True,text=True,timeout=30)
                print('Docker health:',health.returncode,health.stdout.strip(),flush=True)
if __name__=='__main__':main()
