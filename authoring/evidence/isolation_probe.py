"""Author-only Linux verifier isolation probe; run inside the built verifier image."""
import json
import os
from pathlib import Path
import subprocess
import sys

sys.path.insert(0,"/tests")
from harness import _limits

code = r"""
import json,os,resource
results={"uid":os.getuid(),"gid":os.getgid(),"groups":os.getgroups()}
for name,path,mode in [("read_tests","/tests/cases.py","r"),
                        ("write_reward","/logs/verifier/reward.txt","w")]:
    try:
        with open(path,mode) as f:
            pass
        results[name]="UNEXPECTED_SUCCESS"
    except PermissionError:
        results[name]="DENIED"
results["cpu_limit"]=resource.getrlimit(resource.RLIMIT_CPU)[0]
results["memory_limit"]=resource.getrlimit(resource.RLIMIT_AS)[0]
results["open_file_limit"]=resource.getrlimit(resource.RLIMIT_NOFILE)[0]
print(json.dumps(results))
"""
r=subprocess.run([sys.executable,"-c",code],cwd="/tmp",preexec_fn=_limits,
                 env={"PATH":"/usr/local/bin:/usr/bin:/bin"},text=True,capture_output=True,check=True)
data=json.loads(r.stdout)
assert data["uid"]==65534 and data["gid"]==65534 and data["groups"]==[]
assert data["read_tests"]=="DENIED" and data["write_reward"]=="DENIED"
assert data["cpu_limit"]==180 and data["memory_limit"]==2*1024**3
assert data["open_file_limit"]==128
print(json.dumps({"success":True,"probe":data},indent=2))
