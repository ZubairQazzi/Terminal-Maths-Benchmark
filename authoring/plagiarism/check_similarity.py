"""Local browser-only similarity audit. Raw reference text arrives on stdin, never saved."""
import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
TASK=ROOT/"tasks"/"mathematical-sciences"/"applied-mathematics"/"certified-pencil-structure"
REPORTS=ROOT/"authoring"/"plagiarism"/"reports"
PATTERN=r"[A-Za-z_][A-Za-z_0-9]*|\d+|[^\w\s]"
KEYWORDS=set("def class for while if elif else try except finally with return yield import from as assert in is not and or lambda pass raise None True False async await".lower().split())


def normalize(text):
    lines=[]
    for line in text.splitlines():
        line=line.strip()
        if not line or "harbor-canary" in line or line.startswith(("#","<!--","//")):
            continue
        lines.append(" ".join(re.findall(r"[a-z_][a-z_0-9]*|\d+",line.lower())))
    return [line for line in lines if line]


def grams(tokens,n):
    return {" ".join(tokens[i:i+n]) for i in range(max(0,len(tokens)-n+1))}


def features(text):
    lines=normalize(text)
    tokens=" ".join(lines).split()
    code=re.findall(PATTERN,text.lower(),flags=re.ASCII)
    structure=[t if t in KEYWORDS or not re.fullmatch(r"[a-z_][a-z_0-9]*",t) else "ID" for t in code]
    return {"normalized":" ".join(tokens),"lines":set(lines),
            "words":grams(tokens,5),"structure":grams(structure,3),
            "tokens":len(tokens)}


def jaccard(a,b):
    return len(a&b)/len(a|b) if a|b else 0.0


def compare(a,b,kind):
    exact=a["normalized"]==b["normalized"] and bool(a["normalized"])
    word=jaccard(a["words"],b["words"])
    line=jaccard(a["lines"],b["lines"])
    structure=jaccard(a["structure"],b["structure"]) if kind=="code" else 0.0
    score=1.0 if exact else (0.6*word+0.25*line+0.15*structure)
    return {"exact_normalized_match":exact,"word_5gram_jaccard":word,
            "normalized_line_jaccard":line,"code_structure_3gram_jaccard":structure,
            "weighted_similarity":score}


def candidates(kind):
    paths=[TASK/"instruction.md"] if kind=="instruction" else [
        TASK/"solution"/"solve.py",TASK/"tests"/"cases.py",
        TASK/"tests"/"certificates.py",TASK/"tests"/"harness.py",TASK/"tests"/"test_outputs.py"]
    return [(p.relative_to(ROOT).as_posix(),p.read_text()) for p in paths]


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--url")
    p.add_argument("--kind",choices=["instruction","code"])
    p.add_argument("--total-lines",type=int)
    p.add_argument("--captured-lines",type=int)
    p.add_argument("--label")
    p.add_argument("--aggregate",action="store_true")
    args=p.parse_args()
    REPORTS.mkdir(parents=True,exist_ok=True)
    if args.aggregate:
        comparisons=[json.loads(f.read_text()) for f in sorted(REPORTS.glob("comparison-*.json"))]
        scores=[x["weighted_similarity"] for r in comparisons for x in r["comparisons"]]
        maximum=max(scores,default=None)
        report={"scope":"browser-returned source windows only; not a downloaded corpus",
                "reference_documents":len(comparisons),"full_corpus_audit":"NOT TESTED",
                "maximum_weighted_similarity":maximum,
                "heuristic_originality":None if maximum is None else 1-maximum,
                "warning_threshold":0.30,"originality_target":0.70,
                "meets_scoped_heuristic":None if maximum is None else maximum<=0.30,
                "semantic_embedding_model":"NOT USED",
                "raw_reference_text_saved":False,"comparisons":comparisons,
                "limitations":["Reference windows may omit substantial source content.",
                    "Public main URLs are mutable and browser caches may mix revisions.",
                    "Low lexical similarity is not proof of mathematical originality.",
                    "Code structure is a coarse token metric, not a plagiarism verdict.",
                    "Standard mathematics, canary/protocol scaffolding, and generic imports are not substantive copying."]}
        (REPORTS/"plagiarism_report.json").write_text(json.dumps(report,indent=2)+"\n")
        lines=["# Scoped originality audit","",
               "This is a real comparison against browser-returned source windows. It is not a full-corpus clearance.",
               "",f"Reference documents compared: {len(comparisons)}.",
               f"Maximum weighted similarity: {maximum:.2%}." if maximum is not None else "No reference comparisons.",
               f"Heuristic originality: {1-maximum:.2%}." if maximum is not None else "Originality unmeasured.",
               "","Weights: 60% word five-gram Jaccard, 25% normalized-line Jaccard, 15% code-structure three-gram Jaccard. Exact normalized equality scores 100% similarity. Comments/canaries are removed from word and line comparisons. Review warning: similarity above 30%; target heuristic originality at least 70%.",
               "","Only reports, hashes, and coverage counts are saved. Raw reference source is never written to disk.",
               "","| Reference | Captured/total lines | Max similarity |","|---|---|---|"]
        for r in comparisons:
            mx=max(x["weighted_similarity"] for x in r["comparisons"])
            lines.append(f"| [{r['label']}]({r['url']}) | {r['captured_lines']}/{r['total_lines']} | {mx:.2%} |")
        lines+=["","Manual conceptual assessment: the three references solve distinct scientific problems. No imagery/materials algorithm, dataset, expected value, or distinctive solution logic is reused. Shared Harbor protocol and general Python constructs are acknowledged scaffolding. The mathematical theory itself is standard and credited; global task novelty and independent domain assessment remain uncertain.","",
                "Code review: the oracle uses polynomial Smith forms and convolution kernels; the evaluator uses canonical construction plus rational certificates. The reference workflows instead use geospatial inference, microscopy geometry, and atomistic/continuum computation. The structure score is a shallow syntax comparison; no embedding model or automated semantic originality score was used.","",
                "Limitations: incomplete browser windows, mutable URLs/revision drift, and no complete public-task corpus. Do not present the scoped percentage as proof of originality."]
        (REPORTS/"plagiarism_report.md").write_text("\n".join(lines)+"\n")
        print(json.dumps({k:v for k,v in report.items() if k!="comparisons"},indent=2))
        return
    reference=sys.stdin.buffer.read().decode("utf-8")
    assert args.url and args.kind and args.label and reference.strip()
    b=features(reference)
    comparisons=[]
    for name,text in candidates(args.kind):
        a=features(text)
        comparisons.append({"candidate":name,"candidate_sha256":hashlib.sha256(text.encode()).hexdigest(),
                            **compare(a,b,args.kind)})
    record={"label":args.label,"url":args.url,"kind":args.kind,
            "total_lines":args.total_lines,"captured_lines":args.captured_lines,
            "reference_window_sha256":hashlib.sha256(reference.encode()).hexdigest(),
            "normalized_tokens":b["tokens"],"comparisons":comparisons}
    (REPORTS/("comparison-"+args.label+".json")).write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps({"label":args.label,"max_similarity":max(x["weighted_similarity"] for x in comparisons),
                      "captured_lines":args.captured_lines,"total_lines":args.total_lines}))


if __name__=="__main__":
    main()
