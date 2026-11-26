"""Focused data-only adversarial fixtures against the unchanged real checker.

No Docker or provider calls. Every write, pytest temp path and configurable cache
is inside this new audit directory. Correct artifacts are copied, never linked.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]
TASK = BASE / "task"
REFERENCE = BASE / "authoring/reports/oracle_output"
NAMES = ["audit.json", "eligible_genes.tsv", "matched.tsv", "early_bounds.tsv", "interpretation.json", "calibration.tsv"]
TABLES = [name for name in NAMES if name.endswith(".tsv")]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    case_root = OUT / "adversarial_cases"
    case_root.mkdir(exist_ok=True)
    tables = {name: pd.read_csv(REFERENCE / name, sep="\t") for name in TABLES}
    assert tables["matched.tsv"].certified.astype(str).str.lower().eq("true").sum() == 0
    descriptions = {
        "positive_correct": "Unmodified complete reference artifacts; runtime positive control.",
        "no_files": "Empty submission directory; no artifacts.",
        "zero_byte_files": "Six regular but zero-byte artifacts, including JSON.",
        "header_only_tables": "Correct JSON, but every TSV contains only its valid header.",
        "truncated_20_genes": "Correct JSON/calibration; 20 eligible genes and all their matched/early rows only.",
        "only_certified_matched": "Five correct artifacts; matched.tsv retains certified rows only, hence header-only.",
        "only_certified_genes": "Correct JSON/calibration; eligible/matched/early tables retain only genes with any certificate, hence empty.",
    }
    env = dict(os.environ)
    env.update({
        "PYTHONPATH": str(BASE / "authoring/runtime"),
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPYCACHEPREFIX": str(OUT / "pycache"),
        "TMP": str(OUT / "tmp"), "TEMP": str(OUT / "tmp"),
        "OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
    })
    env.pop("PYTEST_ADDOPTS", None)
    report = {
        "scope": "Host execution of unchanged task/tests/test_outputs.py using task-owned pinned pytest runtime. Binary mapping is the original test.sh success-to-1 rule. These are focused verifier tests, not additional native Harbor trials or agent trajectories.",
        "checker_sha256_before": sha(TASK / "tests/test_outputs.py"),
        "test_sh_sha256": sha(TASK / "tests/test.sh"),
        "cases": [],
    }
    for label, description in descriptions.items():
        destination = case_root / label
        destination.mkdir(exist_ok=True)
        if label not in ["no_files", "zero_byte_files"]:
            for name in NAMES:
                shutil.copy2(REFERENCE / name, destination / name)
        elif label == "zero_byte_files":
            for name in NAMES:
                (destination / name).write_bytes(b"")
        if label == "header_only_tables":
            for name in TABLES:
                tables[name].head(0).to_csv(destination / name, sep="\t", index=False)
        elif label == "truncated_20_genes":
            ids = set(tables["eligible_genes.tsv"].head(20).gene_id)
            for name in ["eligible_genes.tsv", "matched.tsv", "early_bounds.tsv"]:
                table = tables[name]
                table[table.gene_id.isin(ids)].to_csv(destination / name, sep="\t", index=False, float_format="%.16g")
        elif label in ["only_certified_matched", "only_certified_genes"]:
            matched = tables["matched.tsv"]
            selected = matched.certified.astype(str).str.lower().eq("true")
            ids = set(matched.loc[selected, "gene_id"])
            matched.loc[selected].to_csv(destination / "matched.tsv", sep="\t", index=False, float_format="%.16g")
            if label == "only_certified_genes":
                for name in ["eligible_genes.tsv", "early_bounds.tsv"]:
                    table = tables[name]
                    table[table.gene_id.isin(ids)].to_csv(destination / name, sep="\t", index=False, float_format="%.16g")
        env["BIO_SUBMISSION"] = str(destination)
        ctrf = OUT / (label + "_ctrf.json")
        log_path = OUT / (label + "_checker.log")
        command = [sys.executable, "-B", "-m", "pytest", "-p", "ctrf.main", "-p", "no:cacheprovider",
                   "--basetemp", str(OUT / "pytest" / label), "--ctrf", str(ctrf),
                   str(TASK / "tests/test_outputs.py"), "-rA"]
        started = time.perf_counter()
        with log_path.open("w", encoding="utf-8") as log:
            log.write("COMMAND " + json.dumps(command) + "\n"); log.flush()
            process = subprocess.run(command, env=env, cwd=OUT, stdout=log, stderr=subprocess.STDOUT)
        results = json.loads(ctrf.read_text(encoding="utf-8"))["results"] if ctrf.exists() else None
        valid = bool(results and results["summary"]["tests"] == 11 and process.returncode in [0, 1])
        record = {
            "case": label, "description": description, "directory": str(destination),
            "command": command, "returncode": process.returncode,
            "seconds": time.perf_counter() - started, "complete_checker_execution": valid,
            "binary_result_under_original_mapping": int(process.returncode == 0) if valid else None,
            "ctrf": str(ctrf), "log": str(log_path),
            "summary": results["summary"] if results else None,
            "per_test": {row["name"]: row["status"] for row in results["tests"]} if results else {},
            "artifact_sizes": {p.name: p.stat().st_size for p in destination.iterdir()},
        }
        report["cases"].append(record)
        (OUT / "adversarial_checker_audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({k: record[k] for k in ["case", "returncode", "complete_checker_execution", "binary_result_under_original_mapping", "summary"]}), flush=True)
    report["checker_sha256_after"] = sha(TASK / "tests/test_outputs.py")
    report["checker_unchanged"] = report["checker_sha256_before"] == report["checker_sha256_after"]
    report["all_expected_outcomes"] = all(row["complete_checker_execution"] and row["binary_result_under_original_mapping"] == int(row["case"] == "positive_correct") for row in report["cases"])
    (OUT / "adversarial_checker_audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    if not report["all_expected_outcomes"]:
        raise RuntimeError("Unexpected acceptance or incomplete checker execution; inspect actual evidence")


if __name__ == "__main__":
    main()
