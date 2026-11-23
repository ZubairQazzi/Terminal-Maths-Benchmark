"""Eight serial Harbor trials, frozen task, local-only logs, no secret serialization."""
import argparse
import csv
from datetime import datetime
import hashlib
import importlib.metadata
import json
from pathlib import Path
import statistics
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
TASK=ROOT/"tasks"/"mathematical-sciences"/"applied-mathematics"/"certified-pencil-structure"
OUT=ROOT/"authoring"/"trajectories"
JOBS=OUT/"jobs"
HARBOR=Path(r"C:\Users\zubai\.local\bin\harbor.exe")
AGENT="terminus-2"
MODEL="gemini/gemini-4-hydrogen"
COLUMNS=["run_id","agent","agent_version","model","model_version","task_version",
         "task_sha256","seed","duration_sec","steps","tool_calls","input_tokens",
         "output_tokens","cost_usd","cost_kind","reward","status","failure_reason","trajectory_path"]


def task_digest():
    h=hashlib.sha256()
    for p in sorted(TASK.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts and p.suffix!=".pyc":
            h.update(p.relative_to(TASK).as_posix().encode()+b"\0"+p.read_bytes()+b"\0")
    return h.hexdigest()


def elapsed(a,b):
    if not a or not b:
        return None
    return (datetime.fromisoformat(b.replace("Z","+00:00"))-
            datetime.fromisoformat(a.replace("Z","+00:00"))).total_seconds()


def command(index):
    return [str(HARBOR),"run","--path",str(TASK),"--agent",AGENT,"--model",MODEL,
            "--api-key-name","GEMINI_API_KEY","--ak","record_terminal_session=false",
            "--ak","store_all_messages=true","--n-concurrent","1","--max-retries","0",
            "--jobs-dir",str(JOBS),"--job-name","gemini-v012-%02d"%index]


def collect(index,return_code,wall_sec,console):
    job=JOBS/("gemini-v012-%02d"%index)
    found=[]
    if job.exists():
        for p in job.glob("*/result.json"):
            d=json.loads(p.read_text(encoding="utf-8"))
            if "trial_name" in d:
                found.append((p,d))
    row={"run_id":"gemini-v012-%02d"%index,"agent":AGENT,"agent_version":"2.0.0",
         "model":MODEL,"model_version":None,"task_version":"0.1.2",
         "task_sha256":None,"seed":None,"duration_sec":wall_sec,"steps":None,
         "tool_calls":None,"input_tokens":None,"output_tokens":None,
         "cost_usd":None,"cost_kind":"harness_estimate_not_billing_receipt",
         "reward":None,"status":"INTERRUPTED","failure_reason":"No completed trial result",
         "trajectory_path":None,"console_path":str(console),"process_return_code":return_code}
    if not found:
        return row
    assert len(found)==1
    p,d=found[0]
    row["result_path"]=str(p)
    row["task_sha256"]=d.get("task_checksum")
    info=d.get("agent_info") or {}
    row["agent_version"]=info.get("version")
    row["model_info"]=info.get("model_info")
    if isinstance(row["model_info"],dict):
        row["model_version"]=row["model_info"].get("version")
    ar=d.get("agent_result") or {}
    for key,target in [("n_input_tokens","input_tokens"),("n_output_tokens","output_tokens"),
                       ("cost_usd","cost_usd")]:
        row[target]=ar.get(key)
    row["duration_sec"]=elapsed(d.get("started_at"),d.get("finished_at")) or wall_sec
    execution=d.get("agent_execution") or {}
    row["agent_execution_sec"]=elapsed(execution.get("started_at"),execution.get("finished_at"))
    reward=((d.get("verifier_result") or {}).get("rewards") or {}).get("reward")
    row["reward"]=reward
    exception=d.get("exception_info")
    row["exception_info"]=exception
    if exception:
        row["failure_reason"]=str(exception.get("exception_type","infrastructure error"))
    elif reward is not None:
        row["status"]="SUCCESS" if reward==1 else "FAILURE"
        row["failure_reason"]="" if reward==1 else "Verifier rejected submission; manual trajectory analysis pending."
    trajectory=p.parent/"agent"/"trajectory.json"
    if trajectory.exists():
        row["trajectory_path"]=str(trajectory)
        t=json.loads(trajectory.read_text(encoding="utf-8"))
        steps=t.get("steps") or []
        row["steps"]=sum(x.get("source")=="agent" for x in steps)
        row["tool_calls"]=sum(len(x.get("tool_calls") or []) for x in steps)
        row["trajectory_model"]=(t.get("agent") or {}).get("model_name")
        row["trajectory_agent_version"]=(t.get("agent") or {}).get("version")
    return row


def save(rows,manifest,reason=None):
    valid=[r for r in rows if r["status"] in ("SUCCESS","FAILURE")]
    successes=sum(r["status"]=="SUCCESS" for r in valid)
    durations=[r["duration_sec"] for r in valid if r["duration_sec"] is not None]
    summary={"task_version":"0.1.2","task_digest":manifest["task_digest"],
        "agent":AGENT,"agent_version":"2.0.0","model":MODEL,
        "catalog_model_version":"3.0; alias metadata, not an immutable backend revision",
        "requested_trials":8,"attempted_trials":len(rows),"completed_trials":len(valid),
        "successful_trials":successes,"failed_trials":len(valid)-successes,
        "interrupted_trials":len(rows)-len(valid),
        "success_percentage":100*successes/len(valid) if valid else None,
        "failure_percentage":100*(len(valid)-successes)/len(valid) if valid else None,
        "mean_duration_sec":statistics.mean(durations) if durations else None,
        "median_duration_sec":statistics.median(durations) if durations else None,
        "status":"COMPLETED" if len(valid)==8 else "INCOMPLETE",
        "stop_reason":reason,"trials":rows}
    (OUT/"trajectory_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    with (OUT/"trajectory_summary.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=COLUMNS,extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return summary


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--dry-run",action="store_true")
    args=p.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    JOBS.mkdir(parents=True,exist_ok=True)
    manifest={"task_version":"0.1.2","task_digest":task_digest(),
              "harbor_version":importlib.metadata.version("harbor"),
              "litellm_version":importlib.metadata.version("litellm"),
              "agent":AGENT,"agent_version":"2.0.0","model":MODEL,
              "model_catalog_version":"3.0","free_tier_confirmed_by_user":True,
              "paid_fallback":False,"requested_trials":8,"concurrency":1,
              "agent_timeout_sec":28800,"record_terminal_session":False,
              "store_all_messages":True,"seed":None,"commands":[command(i) for i in range(1,9)],
              "model_version_limitation":"Provider model-list version is generic; preserve any more specific runtime model identity when available.",
              "file_sha256":{p.relative_to(TASK).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(TASK.rglob("*")) if p.is_file() and "__pycache__" not in p.parts}}
    if args.dry_run:
        print(json.dumps({"task_digest":manifest["task_digest"],"command":command(1)+["--dry-run"]}),flush=True)
        raise SystemExit(subprocess.call(command(1)+["--dry-run"]))
    assert not any(JOBS.glob("gemini-v012-*")), "Refusing to overwrite existing attempts."
    (OUT/"calibration_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    rows=[]
    for index in range(1,9):
        assert task_digest()==manifest["task_digest"], "Task changed during calibration."
        console=OUT/("gemini-v012-%02d-console.log"%index)
        print(json.dumps({"event":"trial_started","index":index,"total":8}),flush=True)
        started=time.monotonic()
        with console.open("w",encoding="utf-8") as f:
            process=subprocess.run(command(index),cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
        row=collect(index,process.returncode,time.monotonic()-started,console)
        rows.append(row)
        summary=save(rows,manifest)
        print(json.dumps({"event":"trial_finished","index":index,"status":row["status"],
                          "reward":row["reward"],"duration_sec":row["duration_sec"],
                          "completed":summary["completed_trials"]}),flush=True)
        logs=console.read_text(encoding="utf-8",errors="replace")
        job=JOBS/("gemini-v012-%02d"%index)
        for log in job.rglob("*.log"):
            logs+="\n"+log.read_text(encoding="utf-8",errors="replace")
        for log in job.rglob("exception.txt"):
            logs+="\n"+log.read_text(encoding="utf-8",errors="replace")
        quota=any(marker.lower() in logs.lower()
                  for marker in ("RESOURCE_EXHAUSTED","RateLimitError","quota exceeded","exceeded your current quota"))
        if quota or row["status"]=="INTERRUPTED":
            reason="Provider quota/rate limit; no further trials started." if quota else row["failure_reason"]
            save(rows,manifest,reason)
            print(json.dumps({"event":"calibration_stopped","reason":reason}),flush=True)
            return
        assert row["agent_version"]=="2.0.0", "Agent version changed."
        if index>1:
            assert row["task_sha256"]==rows[0]["task_sha256"], "Harbor task checksum changed."
    print(json.dumps({"event":"calibration_finished","summary":str(OUT/"trajectory_summary.json")}),flush=True)


if __name__=="__main__":
    main()
