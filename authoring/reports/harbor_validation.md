# Real local Harbor validation

Date: 2026-11-23 Asia/Karachi. Existing Harbor 0.27.0; Docker Desktop 4.99.0, Engine/CLI 29.9.3, Compose 5.7.0, Buildx 0.38.1. No host software was reinstalled. The existing Docker Desktop was started after user approval.

Final task: **v0.1.3**. Native Harbor checksum: `99a8da66bc504372c791300e6504ce522f6453cd90ad40dc9ce0ab971ae02cbe`. Author file-framing SHA-256: `28b89df5a40a09efbaa8eec4fa36e2458960b18020aff314bfcb6634ceb076f5`. The two hashing schemes differ intentionally; individual task-file hashes are in authoring/task_file_manifest.json.

| Actual job | Trial | Reward | Tests passed | Exceptions |
|---|---|---:|---:|---:|
| oracle-v013-repeat | certified-pencil-structure__DeD9Mqk | 1.0 | 9/9 | 0 |
| oracle-v013-repeat | certified-pencil-structure__PQc7sRF | 1.0 | 9/9 | 0 |
| nop-v013-1 | certified-pencil-structure__7rqEo6w | 0.0 | 0/9 | 0 |
| partial-v013-1 | certified-pencil-structure__iKebXYx | 0.0 | 1/9 | 0 |
| helper-v013-1 | certified-pencil-structure__gMNakHj | 1.0 | 9/9 | 0 |

Both oracle repeats used clean containers and the same final checksum. Each evaluates all 36 pencils in nine distinct mandatory batches. The helper adapter submits a general correct source implementation that executes a supporting Python file; its 9/9 pass verifies acceptance of that permitted layout. The partial adapter submits the finite-Smith-only baseline and passes just one batch. No baseline is an AI calibration trial.

Exact executed native commands, from F:/rl/math-benchmark with the installed Docker CLI on PATH:

```powershell
harbor lint .\tasks\mathematical-sciences\applied-mathematics\certified-pencil-structure --json
harbor run --path .\tasks\mathematical-sciences\applied-mathematics\certified-pencil-structure --agent oracle -k 2 --job-name oracle-v013-repeat --jobs-dir .\authoring\reports\harbor-jobs --n-concurrent 1
harbor run --path .\tasks\mathematical-sciences\applied-mathematics\certified-pencil-structure --agent nop --job-name nop-v013-1 --jobs-dir .\authoring\reports\harbor-jobs --n-concurrent 1
$env:PYTHONPATH = (Get-Location).Path
harbor run --path .\tasks\mathematical-sciences\applied-mathematics\certified-pencil-structure --agent authoring.evidence.baseline_agent:PartialAgent --job-name partial-v013-1 --jobs-dir .\authoring\reports\harbor-jobs --n-concurrent 1
harbor run --path .\tasks\mathematical-sciences\applied-mathematics\certified-pencil-structure --agent authoring.evidence.baseline_agent:ExecutableHelperAgent --job-name helper-v013-1 --jobs-dir .\authoring\reports\harbor-jobs --n-concurrent 1
```

Raw config.json/result.json/lock.json, agent records, verifier pytest.log/ctrf.json/reward.txt, and console logs are retained in harbor-jobs/ and sibling log files. The first v0.1.0 oracle command used --force-build and built both environments successfully; later builds reused valid Docker layer cache. Final v0.1.3 agent/verifier build logs are agent_build_v013.log and verifier_build_v013.log. No additional --no-cache build is claimed.

Final isolation_probe_v013.json and agent_leakage_probe_v013.json both pass: candidate UID/GID 65534 with empty supplementary groups; access to hidden tests and reward writes denied; CPU 180 sec, address-space 2147483648 bytes, FD limit 128. The agent image has only /app/spec.md and /app/data/examples.json as application files, without /tests/cases.py or /solution/solve.py. The offline separate verifier installs dependencies at build time and derives rewards from pytest exit status.

Portable source validation is independently labeled in local_validation_v013.json: 22 checks passed in 28.453 seconds. Its docker_validated/harbor_validated flags deliberately remain false; the actual native results above provide those distinct proofs. Final Harbor lint returned [].

History: v0.1.1 repaired CTRF parameter aggregation by assigning distinct test names; v0.1.2 added previously public dimension-18, infinity-size-six, and higher-degree finite-factor coverage. v0.1.3 repaired an independently reproduced fairness defect: the old harness removed execute access from valid supporting source files. The final copied program files are executable but root-owned/read-only to the candidate. The spec also clarifies writable paths and per-process/per-file limits. Old rejection evidence is executable_helper_probe_before.json, and prior harness/spec sources are preserved under authoring/provenance/. No mathematical instance, invariant, certificate, or acceptance criterion changed in v0.1.3; no completed model outcome informed a change.

This validates the implementation and local infrastructure. It does not establish empirical model difficulty, a 40-60% success rate, independent expert approval, or upstream maintainer acceptance.
