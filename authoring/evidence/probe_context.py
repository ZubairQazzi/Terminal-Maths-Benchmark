"""Two bounded, non-task REST requests to inspect context-size availability."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import time
from connection_recovery import request,freeze
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'authoring/trajectories/connection-recovery-20261123/context_size_probe.json'
assert not OUT.exists(),'Preserve earlier diagnostics.'
rows=[]
for label,words in [('short',0),('long',10000)]:
    started=time.monotonic()
    text='Reply with the word READY. The following is inert padding; do not summarize it.\n'+('padding '*words)+'\nReply READY.'
    result=request('v1beta/models/gemini-3.5-flash-lite:generateContent',
        {'contents':[{'role':'user','parts':[{'text':text}]}],'generationConfig':{'maxOutputTokens':128}})
    result['label']=label;result['prompt_characters']=len(text)
    result['prompt_sha256']=hashlib.sha256(text.encode()).hexdigest()
    rows.append(result)
    OUT.write_text(json.dumps({'task_digest':freeze(),'requests':rows,'no_math_task_content_sent':True,'outputs_not_supplied_to_any_agent':True},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'label':label,'status':result['status'],'elapsed_sec':result['elapsed_sec'],
        'usage':result['response'].get('usageMetadata'),'error_status':result['response'].get('error',{}).get('status')}),flush=True)
    if label=='short': time.sleep(max(0,60-(time.monotonic()-started)))