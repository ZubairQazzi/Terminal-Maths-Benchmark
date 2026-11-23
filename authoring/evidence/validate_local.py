"""Author-only portable checks. Real Docker/Harbor validation is separate."""
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT/"tasks"/"mathematical-sciences"/"applied-mathematics"/"certified-pencil-structure"
sys.path.insert(0,str(TASK/"tests"))
from cases import suite
from certificates import verify, rank
from harness import run_batch


def digest():
    h = hashlib.sha256()
    for p in sorted(TASK.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc":
            h.update(p.relative_to(TASK).as_posix().encode()+b"\0"+p.read_bytes()+b"\0")
    return h.hexdigest()


def direct_answers(oracle, batch):
    return [oracle.solve_case(c) for c,e in batch]


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default=str(ROOT/"authoring"/"reports"/"local_validation.json"))
    args=p.parse_args()
    report={"kind":"portable-author-checks","task_sha256":digest(),
            "docker_validated":False,"harbor_validated":False,"results":[]}
    started=time.monotonic()
    spec=importlib.util.spec_from_file_location("author_oracle",TASK/"solution"/"solve.py")
    oracle=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(oracle)
    batches=suite()
    for i,batch in enumerate(batches):
        record={"check":"oracle-batch-"+str(i),"status":"FAIL"}
        try:
            record.update(run_batch(TASK/"solution",batch,portable=True))
            record["status"]="PASS"
        except Exception as exc:
            record["error"]=repr(exc)
        report["results"].append(record)
        print(json.dumps(record),flush=True)
        Path(args.output).parent.mkdir(parents=True,exist_ok=True)
        Path(args.output).write_text(json.dumps(report,indent=2))
    # Deterministic rerun of the same fresh source and inputs.
    repeat=run_batch(TASK/"solution",batches[0],portable=True)
    report["results"].append({"check":"fresh-repeat","status":"PASS",**repeat})
    # Independent exact normal-rank check: every pencil minor has
    # degree <= min(m,n); min(m,n)+1 samples establish the maximum rank exactly.
    for case,expected in [item for batch in batches for item in batch]:
        A,B=case["A"],case["B"]
        r=expected["normal_rank"]
        sampled=max(rank([[a-t*b for a,b in zip(ar,br)] for ar,br in zip(A,B)])
                    for t in range(min(len(A),len(A[0]))+1))
        assert sampled == r, case["id"]+": generator normal rank mismatch"
    report["results"].append({"check":"independent-generator-normal-rank","status":"PASS"})
    # Exact checker rejection controls: corrupt each semantic output family.
    batch=batches[4]
    answers=direct_answers(oracle,batch)
    controls=[
        ("wrong-rank",lambda x:x.__setitem__("normal_rank",x["normal_rank"]+1)),
        ("wrong-finite-factor",lambda x:x["smith_factors"][-1].__setitem__(0,"12345")),
        ("wrong-infinity",lambda x:x.__setitem__("infinite_sizes",[6])),
        ("wrong-right-degree",lambda x:x.__setitem__("right_indices",[4])),
        ("wrong-left-degree",lambda x:x.__setitem__("left_indices",[4])),
        ("forged-basis",lambda x:x["right_basis"][0][0].__setitem__(0,"12345")),
        ("float-scalar",lambda x:x["smith_factors"][0].__setitem__(0,1.0)),
        ("boolean-rank",lambda x:x.__setitem__("normal_rank",True)),
    ]
    case,expected=batch[0]
    for name,mutate in controls:
        altered=deepcopy(answers[0])
        mutate(altered)
        try:
            verify(case,expected,altered)
        except (AssertionError,ValueError,TypeError,KeyError):
            report["results"].append({"check":name,"status":"PASS","incorrect_submission_rejected":True})
        else:
            report["results"].append({"check":name,"status":"FAIL","error":"corrupt output accepted"})
    # Accept genuinely different bases: nonzero rational rescaling, no pivot convention.
    altered=deepcopy(answers[0])
    from fractions import Fraction
    for key in ("right_basis","left_basis"):
        altered[key]=[[[str(Fraction(x)*Fraction(3,7)) for x in v] for v in cert]
                      for cert in altered[key]]
    verify(case,expected,altered)
    report["results"].append({"check":"alternative-basis","status":"PASS"})
    for name in ("broken","partial"):
        try:
            run_batch(ROOT/"authoring"/"evidence"/"baselines"/name,batches[4],portable=True)
        except (AssertionError,KeyError,ValueError,TypeError) as exc:
            report["results"].append({"check":name+"-baseline","status":"PASS",
                                      "incorrect_submission_rejected":True,"reason":str(exc)})
        else:
            report["results"].append({"check":name+"-baseline","status":"FAIL"})
    report["seconds"]=time.monotonic()-started
    report["success"]=all(x["status"]=="PASS" for x in report["results"])
    Path(args.output).write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2),flush=True)
    raise SystemExit(0 if report["success"] else 1)


if __name__=="__main__":
    main()
