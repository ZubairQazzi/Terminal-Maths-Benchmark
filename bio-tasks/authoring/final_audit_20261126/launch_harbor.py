"""Native Harbor CLI with F-drive caches and bounded transport-only retries.
No prompt, scientific task, output parser or evaluator changes.
"""
from trial_environment import configure,redirect_harbor_cache
configure();redirect_harbor_cache()
from datetime import datetime,timezone
from pathlib import Path
import asyncio,functools,json,os,re,time
import litellm
from tenacity import stop_after_attempt
from harbor.llms.lite_llm import LiteLLM
from harbor.agents.terminus_2.terminus_2 import Terminus2

LiteLLM.call.retry.stop=stop_after_attempt(1)
Terminus2._query_llm.retry.stop=stop_after_attempt(1)
ORIGINAL=litellm.acompletion
LOCK=asyncio.Lock();NEXT=0.
def event(**values):
    p=os.environ.get('BIO_TRANSPORT_LOG')
    if p:
        with Path(p).open('a',encoding='utf-8') as f:f.write(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),**values})+'\n')
def redact(error):
    text=str(error)
    for name in ('GEMINI_API_KEY','GOOGLE_API_KEY'):
        value=os.environ.get(name)
        if value:text=text.replace(value,'[REDACTED]')
    return re.sub(r'AIza[0-9A-Za-z_-]{25,}','[REDACTED]',text)[:5000]
@functools.wraps(ORIGINAL)
async def measured_call(*args,**kwargs):
    global NEXT
    for attempt in range(1,6):
        async with LOCK:
            delay=max(0.,NEXT-time.monotonic())
            if delay:await asyncio.sleep(delay)
            NEXT=time.monotonic()+20.
        start=time.monotonic()
        event(event='request_started',attempt=attempt,model=kwargs.get('model'),reasoning_effort=kwargs.get('reasoning_effort'),max_output_tokens=kwargs.get('max_tokens'))
        try:
            response=await ORIGINAL(*args,**kwargs)
            usage=getattr(response,'usage',None)
            if hasattr(usage,'model_dump'):usage=usage.model_dump()
            elif usage is not None:usage=str(usage)
            event(event='request_succeeded',attempt=attempt,seconds=time.monotonic()-start,response_model=getattr(response,'model',None),usage=usage)
            return response
        except Exception as error:
            message=redact(error);status=getattr(error,'status_code',None)
            daily=status==429 and any(x in message.lower() for x in ('perday','per_day','per day','daily','limit: 0','limit:0'))
            event(event='request_failed',attempt=attempt,status=status,error_type=type(error).__name__,seconds=time.monotonic()-start,message=message,daily_or_zero_quota=daily)
            transient=status in (408,429,500,502,503,504) or isinstance(error,(litellm.Timeout,litellm.APIConnectionError))
            if not transient or daily or attempt==5:raise
            delay=min(45.,10.*2**(attempt-1))
            match=re.search(r'(?:retry in|retryDelay[^0-9]*)([0-9]+(?:\.[0-9]+)?)',message,re.I)
            if match:delay=max(delay,min(60.,float(match.group(1))+1))
            event(event='bounded_backoff',seconds=delay)
            await asyncio.sleep(delay)
litellm.acompletion=measured_call
if __name__=='__main__':
    event(event='transport_configuration',minimum_interval_seconds=20,max_attempts_per_call=5,request_timeout_seconds=600,paid_only_fallback=False)
    from harbor.cli.main import app
    app()
