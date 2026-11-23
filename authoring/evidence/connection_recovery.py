"""Secret-safe official Gemini REST diagnostics, outside the frozen task."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import random
import time
import urllib.error
import urllib.parse
import urllib.request
import winreg

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'authoring/trajectories/connection-recovery-20261123'
TASK=ROOT/'tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure'
EXPECTED='28b89df5a40a09efbaa8eec4fa36e2458960b18020aff314bfcb6634ceb076f5'

def key():
    value=os.environ.get('GEMINI_API_KEY')
    if not value:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,'Environment') as registry:
            value=winreg.QueryValueEx(registry,'GEMINI_API_KEY')[0]
    assert value, 'No configured Gemini key; do not log or paste it.'
    return value

def freeze():
    h=hashlib.sha256()
    for p in sorted(TASK.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':
            h.update(p.relative_to(TASK).as_posix().encode()+b'\0'+p.read_bytes()+b'\0')
    assert h.hexdigest()==EXPECTED, 'Task changed since v0.1.3 validation.'
    return h.hexdigest()

def request(path,payload=None):
    started=time.monotonic()
    req=urllib.request.Request('https://generativelanguage.googleapis.com/'+path,
        data=None if payload is None else json.dumps(payload).encode(),
        headers={'x-goog-api-key':key(),'Content-Type':'application/json'},
        method='GET' if payload is None else 'POST')
    headers={}
    try:
        with urllib.request.urlopen(req,timeout=60) as response:
            body=json.loads(response.read())
            status=response.status
            headers=dict(response.headers)
    except urllib.error.HTTPError as error:
        status=error.code
        headers=dict(error.headers)
        raw=error.read().decode('utf-8',errors='replace').replace(key(),'[REDACTED]')
        try: body=json.loads(raw)
        except json.JSONDecodeError: body={'non_json_error':raw[:3000]}
    except Exception as error:
        status=None
        body={'transport_exception':type(error).__name__,'message':str(error).replace(key(),'[REDACTED]')}
    return {'utc':datetime.now(timezone.utc).isoformat(),'path':path,'status':status,
        'elapsed_sec':time.monotonic()-started,
        'response_headers':{k:v for k,v in headers.items() if k.lower() in ('server','content-type','retry-after','x-request-id','x-goog-request-id')},
        'response':body}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--list-only',action='store_true')
    p.add_argument('--model',default='gemini-3.8-flash')
    p.add_argument('--api-version',choices=['v1beta','v1alpha'],default='v1beta')
    p.add_argument('--attempts',type=int,default=3)
    args=p.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    freeze()
    if args.list_only:
        rows=[]
        token=''
        while True:
            row=request('v1beta/models?pageSize=100'+('&pageToken='+urllib.parse.quote(token) if token else ''))
            assert row['status']==200, 'Model listing failed: '+str(row['status'])
            rows+=row['response'].get('models',[])
            token=row['response'].get('nextPageToken','')
            if not token: break
        env_names=['GEMINI_API_BASE','GOOGLE_API_BASE','GOOGLE_GENAI_USE_VERTEXAI','GOOGLE_CLOUD_PROJECT',
            'GOOGLE_CLOUD_LOCATION','OPENAI_API_BASE','LITELLM_PROXY_API_BASE','HTTP_PROXY','HTTPS_PROXY','ALL_PROXY']
        env_state={name:bool(os.environ.get(name)) for name in env_names}
        report={'utc':datetime.now(timezone.utc).isoformat(),'endpoint':'https://generativelanguage.googleapis.com/v1beta/models',
            'task_digest':freeze(),'model_count':len(rows),'models':rows,
            'configuration_variable_presence':env_state,
            'configured_proxy_hosts':{name:urllib.parse.urlsplit(value).hostname for name,value in urllib.request.getproxies().items()},
            'credentials_logged':False}
        (OUT/'model_catalog_and_configuration.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'model_count':len(rows),'text_generation_models':[r['name'] for r in rows if 'generateContent' in r.get('supportedGenerationMethods',[])],
            'configuration_variable_presence':env_state,'proxy_configured':bool(urllib.request.getproxies())}),flush=True)
        return
    payload={'contents':[{'role':'user','parts':[{'text':'Reply with the single word READY.'}]}],
        'generationConfig':{'maxOutputTokens':512}}
    rows=[]
    destination=OUT/(args.model+'-'+args.api_version+'-probe.json')
    assert not destination.exists(), 'Preserve earlier probes; use a separate destination/version.'
    for i in range(args.attempts):
        print(json.dumps({'event':'probe_started','model':args.model,'api_version':args.api_version,'attempt':i+1}),flush=True)
        row=request(args.api_version+'/models/'+args.model+':generateContent',payload)
        rows.append(row)
        (destination).write_text(json.dumps({'request_body':payload,'attempts':rows,'task_digest':freeze()},indent=2)+'\n',encoding='utf-8')
        body=row['response']
        text=''.join(part.get('text','') for c in body.get('candidates',[]) for part in c.get('content',{}).get('parts',[]) if not part.get('thought'))
        print(json.dumps({'event':'probe_result','model':args.model,'status':row['status'],'elapsed_sec':row['elapsed_sec'],
            'error_status':body.get('error',{}).get('status'),'response_text':text[:120],
            'model_version':body.get('modelVersion'),'usage':body.get('usageMetadata')}),flush=True)
        if row['status']==200 or row['status'] in (400,401,402,403,404): break
        if row['status']==429 and any(x in json.dumps(body).lower() for x in ['perday','per_day','daily','limit: 0']): break
        if i+1<args.attempts:
            delay=min(60,20*(2**i))+random.uniform(0,3)
            print(json.dumps({'event':'backoff','seconds':delay}),flush=True)
            time.sleep(delay)
    freeze()

if __name__=='__main__': main()