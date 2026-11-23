"""Create a distinct future batch using the same frozen v0.1.3 configuration.
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
