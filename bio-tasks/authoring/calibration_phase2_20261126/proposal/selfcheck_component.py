"""Tiny public component checks, not generation of a Biology task fixture."""
from pathlib import Path
import json,random,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'final_audit_20261126'))
from trial_environment import configure
configure()
import numpy as np
from secure_fixture_rng import SecureRecordedRNG

def sample(r):
 return [r.permutation(120),r.uniform(-1.1,1.1,120),r.integers(120),r.uniform(.25,.75),r.normal(0,.001,1024),r.permutation(24)]
record=HERE/'public_component_selfcheck.json.gz'
assert not record.exists(),'Refuse to overwrite prior component check'
r=SecureRecordedRNG();first=sample(r);r.save_private_record(record,forbidden_roots=[HERE/'example-agent-context',HERE/'example-verifier-context'])
replay=SecureRecordedRNG(replay_record=record);second=sample(replay)
assert all(np.array_equal(a,b) for a,b in zip(first,second))
assert len(set(first[0]))==120 and len(set(first[-1]))==24
assert np.all(np.isfinite(first[4]))
replay.save_private_record(HERE/'public_component_replay_selfcheck.json.gz',forbidden_roots=[HERE/'example-agent-context',HERE/'example-verifier-context'])
random.seed(273600);np.random.seed(273600);a=sample(SecureRecordedRNG())
random.seed(273600);np.random.seed(273600);b=sample(SecureRecordedRNG())
assert not np.array_equal(a[0],b[0])
try:SecureRecordedRNG(replay_record=record).integers(120)
except ValueError:sequence_guard=True
else:sequence_guard=False
assert sequence_guard
try:SecureRecordedRNG().save_private_record(HERE/'example-agent-context/leak.json.gz',forbidden_roots=[HERE/'example-agent-context'])
except ValueError:context_guard=True
else:context_guard=False
assert context_guard
result={'status':'COMPONENT_CHECKS_PASS','scope':'Small public component exercise only; no RNA-seq data, no actual new task instance, no private planted answers. Not a cryptographic proof or full task QC.','exact_private_replay':True,'permutation_valid':True,'finite_normal_draws':True,'public_numpy_python_seed_does_not_reproduce_observed_draws':True,'wrong_replay_sequence_rejected':True,'agent_context_record_rejected':True,'next_requirement':'Approved versioned fixture generation and scientific/native isolation QC before any model trials.'}
(HERE/'component_selfcheck.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
