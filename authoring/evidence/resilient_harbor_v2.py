"""Bounded transport-only retries for unchanged native Harbor Terminus-2.
No task, prompt, model answer, parsing, terminal action or grader modifications.
"""
import asyncio
from datetime import datetime,timezone
import functools
import json
import os
from pathlib import Path
import random
import re
import time
import litellm
from tenacity import stop_after_attempt
from harbor.llms.lite_llm import LiteLLM
from harbor.agents.terminus_2.terminus_2 import Terminus2

# Centralize retries instead of multiplying three nested retry layers.
LiteLLM.call.retry.stop=stop_after_attempt(1)
Terminus2._query_llm.retry.stop=stop_after_attempt(1)
_ORIGINAL=litellm.acompletion
_LOCK=asyncio.Lock()
_NEXT=0.0
INTERVAL=20.0
ATTEMPTS=10

def event(**data):
    path=os.environ.get('BENCHMARK_TRANSPORT_LOG')
    data={'utc':datetime.now(timezone.utc).isoformat(),**data}
    if path:
        with Path(path).open('a',encoding='utf-8') as stream:
            stream.write(json.dumps(data)+'\n')

def safe_message(error):
    message=str(error)
    for name in ('GEMINI_API_KEY','GOOGLE_API_KEY','MSWEA_API_KEY'):
        value=os.environ.get(name)
        if value: message=message.replace(value,'[REDACTED]')
    return re.sub(r'AIza[0-9A-Za-z_-]{30,}','[REDACTED]',message)[:6000]

def exhausted_quota(message):
    text=message.lower()
    return any(x in text for x in ('perday','per_day','per day','daily quota','limit: 0','limit:0'))

@functools.wraps(_ORIGINAL)
async def resilient_acompletion(*args,**kwargs):
    global _NEXT
    for attempt in range(1,ATTEMPTS+1):
        async with _LOCK:
            wait=max(0.0,_NEXT-time.monotonic())
            if wait: await asyncio.sleep(wait)
            _NEXT=time.monotonic()+INTERVAL
        started=time.monotonic()
        event(event='request_started',attempt=attempt,model=kwargs.get('model'),reasoning_effort=kwargs.get('reasoning_effort'),max_tokens=kwargs.get('max_tokens'))
        try:
            result=await _ORIGINAL(*args,**kwargs)
            event(event='request_succeeded',attempt=attempt,elapsed_sec=time.monotonic()-started,
                  response_model=getattr(result,'model',None))
            return result
        except Exception as error:
            status=getattr(error,'status_code',None)
            message=safe_message(error)
            transient=status in (408,429,500,502,503,504) or isinstance(error,(litellm.Timeout,litellm.APIConnectionError))
            daily=status==429 and exhausted_quota(message)
            event(event='request_failed',attempt=attempt,status=status,error_type=type(error).__name__,
                  elapsed_sec=time.monotonic()-started,message=message,quota_exhausted=daily)
            if not transient or daily or attempt==ATTEMPTS:
                raise
            delay=min(120.0,10.0*(2**(attempt-1)))+random.uniform(0,3)
            response=getattr(error,'response',None)
            header=(getattr(response,'headers',{}) or {}).get('retry-after')
            try: delay=max(delay,float(header))
            except (TypeError,ValueError): pass
            match=re.search(r'(?:retry in|retryDelay[^0-9]*)([0-9]+(?:\.[0-9]+)?)',message,re.I)
            if match: delay=max(delay,float(match.group(1))+1)
            if delay>180:
                event(event='retry_deferred_beyond_session_policy',requested_delay_sec=delay)
                raise
            event(event='exponential_backoff',delay_sec=delay,following_attempt=attempt+1)
            await asyncio.sleep(delay)

litellm.acompletion=resilient_acompletion
if __name__=='__main__':
    event(event='transport_config',interval_sec=INTERVAL,max_attempts=ATTEMPTS,
          sdk_retries=0,native_nested_attempts=1,request_timeout_sec=600)
    from harbor.cli.main import app
    app()