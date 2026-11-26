"""Prevent configured key values from remaining in newly generated trial logs.
Only reports counts/relative paths, never the key or matching text.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,os
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'authoring/trajectories/initial-gemini35lite-high-20261126'
keys=[os.environ[k] for k in ('GEMINI_API_KEY','GOOGLE_API_KEY') if os.environ.get(k)]
assert keys,'Credential availability required for exact-value scanning; never print values'
checked=0;changed=[]
for p in OUT.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in ('.json','.jsonl','.txt','.log','.yaml','.yml','.csv','.md'):continue
    raw=p.read_bytes();new=raw
    for value in keys:new=new.replace(value.encode(),b'[REDACTED_CONFIGURED_KEY]')
    checked+=1
    if new!=raw:
        p.write_bytes(new);changed.append(p.relative_to(OUT).as_posix())
report={'utc':datetime.now(timezone.utc).isoformat(),'files_scanned':checked,'exact_configured_key_matches_redacted':len(changed),'changed_relative_paths':changed,'scope':'New trajectory text/log/config files only; no task input, evaluator, scientific output or checksum was modified. Report contains no secret value.'}
(OUT/'credential_log_scan.json').write_text(json.dumps(report,indent=2))
print('Trial credential scan:',checked,'files;',len(changed),'files needed redaction')
