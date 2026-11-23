"""Harbor CLI with transparent request pacing; agent/model messages are unchanged."""
import asyncio
import functools
import time
import litellm

_original=litellm.acompletion
_lock=asyncio.Lock()
_next_allowed=0.0
INTERVAL=16.0


@functools.wraps(_original)
async def paced_acompletion(*args,**kwargs):
    global _next_allowed
    async with _lock:
        delay=max(0.0,_next_allowed-time.monotonic())
        if delay:
            await asyncio.sleep(delay)
        _next_allowed=time.monotonic()+INTERVAL
    return await _original(*args,**kwargs)


litellm.acompletion=paced_acompletion

if __name__=="__main__":
    from harbor.cli.main import app
    app()
