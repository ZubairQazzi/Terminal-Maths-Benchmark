"""Write final local reproduction docs and batch utility; no model/container runs."""
from pathlib import Path
ROOT=Path(r'F:/rl/math-benchmark')

def write(path,text):
    path.write_text(text.rstrip()+'\n',encoding='utf-8')

write(ROOT/'authoring/evidence/run_fresh_flash_calibration.py', '''"""Create a distinct future batch using the same frozen v0.1.3 configuration.
Running this file makes real API calls unless --dry-run is passed.
No past evidence is overwritten. New-batch evidence stays in its own directory.
"""
import argparse
import json
from pathlib import Path
import re
import sys
import run_flash_v013_calibration as frozen

p=argparse.ArgumentParser()
p.add_argument('--batch-name',required=True)
p.add_argument('--dry-run',action='store_true')
args=p.parse_args()
if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}',args.batch_name):
    p.error('Use 1-64 letters, digits, underscores or hyphens for batch name.')
original_manifest=json.loads((frozen.OUT/'calibration_manifest.json').read_text(encoding='utf-8'))
assert frozen.task_digest()==original_manifest['task_digest'], 'Task differs from the validated primary batch.'
frozen.OUT=frozen.OUT/'calibration_batches'/args.batch_name
frozen.JOBS=frozen.OUT/'jobs'
assert not frozen.OUT.exists(), 'Refusing to overwrite an existing batch.'
sys.argv=[sys.argv[0]]+(['--dry-run'] if args.dry_run else [])
frozen.main()
''')
write(ROOT/'REPRODUCING.md', r'''# Reproduction on this PC

The user required approval before runs or installations. Existing scopes were approved in this session; commands here document reproduction and do not authorize new API spending, installations, model changes, or publication.

Existing tools, verified before use:

- Base Python 3.12.10: C:/Users/zubai/AppData/Local/Programs/Python/Python312/python.exe (SymPy 1.14.0, mpmath 1.3.0).
- Harbor 0.27.0: C:/Users/zubai/.local/bin/harbor.exe.
- Harbor's Python: C:/Users/zubai/AppData/Roaming/uv/tools/harbor/Scripts/python.exe.
- Docker CLI: C:/Users/zubai/AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe.
- Existing Docker Desktop: C:/Users/zubai/AppData/Local/Programs/DockerDesktop/Docker Desktop.exe.

No host reinstall is needed. Use fresh job names if the example names already exist; preserve previous evidence.

```powershell
Set-Location F:\rl\math-benchmark
$env:PATH = 'C:\Users\zubai\AppData\Local\Programs\DockerDesktop\resources\bin;' + $env:PATH
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
harbor --version
docker version
& 'C:\Users\zubai\AppData\Local\Programs\Python\Python312\python.exe' -B .\authoring\evidence\validate_local.py --output .\authoring\reports\local_validation_reproduction.json
harbor lint .\tasks\mathematical-sciences\applied-mathematics\certified-pencil-structure --json
harbor run --path .\tasks\mathematical-sciences\applied-mathematics\certified-pencil-structure --agent oracle -k 2 --n-concurrent 1 --job-name oracle-reproduction --jobs-dir .\authoring\reports\harbor-jobs
harbor run --path .\tasks\mathematical-sciences\applied-mathematics\certified-pencil-structure --agent nop --n-concurrent 1 --job-name nop-reproduction --jobs-dir .\authoring\reports\harbor-jobs
$env:PYTHONPATH = (Get-Location).Path
harbor run --path .\tasks\mathematical-sciences\applied-mathematics\certified-pencil-structure --agent authoring.evidence.baseline_agent:PartialAgent --n-concurrent 1 --job-name partial-reproduction --jobs-dir .\authoring\reports\harbor-jobs
harbor run --path .\tasks\mathematical-sciences\applied-mathematics\certified-pencil-structure --agent authoring.evidence.baseline_agent:ExecutableHelperAgent --n-concurrent 1 --job-name helper-reproduction --jobs-dir .\authoring\reports\harbor-jobs
```

Actual final validation used the *-v013-* job names and checksum 99a8da66bc504372c791300e6504ce522f6453cd90ad40dc9ce0ab971ae02cbe. Exact original commands, raw logs and prior version history are in authoring/reports/harbor_validation.md. The task contains exactly one task.toml; author-side adapters are supporting evidence, not additional tasks.

Current primary calibration is incomplete: flash-v013-01 ended with provider HTTP 503 and no valid reward; zero of eight requested valid trials completed. Do not interpret its raw reward 0.0 as an ordinary model failure. The primary summary/manifest and all preliminary attempts are preserved under authoring/trajectories. The original runner refuses to overwrite that evidence.

When provider availability permits an authorized fresh batch on the same free-tier project, the following new-batch wrapper retains the exact v0.1.3 task, agent, model, prompts, resource limits, 16-second request pacing and timeout settings. Choose a unique batch name. It stores new evidence under authoring/trajectories/calibration_batches/<batch-name>; it does not replace or pool the primary sample. No seed is injected where the integration has not demonstrated support. Backend alias metadata is not immutable version pinning.

```powershell
$env:GEMINI_API_KEY = [Environment]::GetEnvironmentVariable('GEMINI_API_KEY', 'User')
& 'C:\Users\zubai\AppData\Roaming\uv\tools\harbor\Scripts\python.exe' -B .\authoring\evidence\run_fresh_flash_calibration.py --batch-name flash-v013-future-unique
Remove-Item Env:\GEMINI_API_KEY
```

The command makes real API calls. Do not print the key, add it to source, change billing, or silently substitute a paid model/account. The runner stops before further trials on quota or infrastructure errors. Every new batch requires eight valid independent trials to establish a complete calibration sample. Interrupted attempts stay separate. Reports for a later batch must explicitly name its folder and task/model configuration rather than silently overwriting prior evidence.

Reporting utilities (no API calls):

```powershell
& 'C:\Users\zubai\AppData\Local\Programs\Python\Python312\python.exe' -B .\authoring\evidence\audit_qc.py
& 'C:\Users\zubai\AppData\Local\Programs\Python\Python312\python.exe' -B .\authoring\evidence\refresh_reports.py
```

These report the preserved primary v0.1.3 sample and named native validation jobs. The similarity process reads browser text on stdin and saves only hashes/counts/metrics, honoring the user's browser-only reference restriction. Public URLs and source-window coverage in plagiarism_report.json permit retracing the scope, subject to mutable URLs and cache drift.
''')
qc=ROOT/'authoring/evidence/audit_qc.py'
text=qc.read_text(encoding='utf-8')
text=text.replace('completed model-trajectory evidence is still being collected.', 'completed mathematical model-trajectory evidence is unavailable because the primary provider attempt was interrupted.')
text=text.replace('Added missing public-contract boundaries before model calibration; no evaluator criterion was relaxed.', 'Added missing public-contract boundaries before model calibration. An independently reproduced supporting-executable defect was repaired in v0.1.3 and a correct helper submission passed; mathematical acceptance criteria were unchanged.')
write(qc,text)
print('Updated reproduction documentation and isolated future-batch utility; made no API calls.')