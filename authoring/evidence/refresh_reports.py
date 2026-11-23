"""Refresh local delivery reports from preserved actual evidence; no API calls."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUTH = ROOT / 'authoring'
REPORTS = AUTH / 'reports'
TRAJ = AUTH / 'trajectories'
TASK = ROOT / 'tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, value):
    path.write_text(value.rstrip() + '\n', encoding='utf-8')

def dump(path, value):
    write(path, json.dumps(value, indent=2))

def main():
    qc = read(REPORTS / 'qc_audit.json')
    summary = read(TRAJ / 'trajectory_summary.json')
    manifest = read(TRAJ / 'calibration_manifest.json')
    similarity = read(AUTH / 'plagiarism/reports/plagiarism_report.json')
    local = read(REPORTS / 'local_validation_v013.json')
    assert qc['task_version'] == summary['task_version'] == manifest['task_version'] == '0.1.3'
    digest = hashlib.sha256()
    for p in sorted(TASK.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc':
            digest.update(p.relative_to(TASK).as_posix().encode() + b'\0' + p.read_bytes() + b'\0')
    assert digest.hexdigest() == manifest['task_digest'] == summary['task_digest']
    assert {t['task_checksum'] for t in qc['trials']} == {qc['harbor_task_checksum']}
    rate = 'undefined (no valid completed trials)' if summary['success_percentage'] is None else f"{summary['success_percentage']:.2f}%"
    original = similarity['heuristic_originality'] * 100
    maxsim = similarity['maximum_weighted_similarity'] * 100
    status = {
        'generated_utc': datetime.now(timezone.utc).isoformat(),
        'task_title': 'Certified Kronecker Structure of Singular Matrix Pencils',
        'task_version': '0.1.3', 'harbor_task_checksum': qc['harbor_task_checksum'],
        'author_framed_sha256': digest.hexdigest(), 'one_task': True,
        'local_only': True, 'implementation_complete': True,
        'harbor_validation_passed': True,
        'calibration_complete': summary['completed_trials'] == 8,
        'requested_valid_calibration_trials': 8,
        'attempted_final_version_trials': summary['attempted_trials'],
        'completed_valid_calibration_trials': summary['completed_trials'],
        'interrupted_final_version_trials': summary['interrupted_trials'],
        'observed_success_percentage': summary['success_percentage'],
        'calibration_blocker': summary['stop_reason'],
        'overall_status': 'IMPLEMENTED_AND_VALIDATED_CALIBRATION_INCOMPLETE',
        'remaining_work': ['Complete eight valid independent model trials when the provider permits them.',
            'Assess legitimate mathematical difficulty from completed trajectories; target 3-5 successes out of 8.',
            'Obtain independent mathematical/domain review; extreme difficulty and global novelty are unverified.']}
    dump(REPORTS / 'final_delivery_status.json', status)

    lines = ['# Real local Harbor validation', '',
        'Date: 2026-11-23 Asia/Karachi. Existing Harbor 0.27.0; Docker Desktop 4.99.0, Engine/CLI 29.9.3, Compose 5.7.0, Buildx 0.38.1. No host software was reinstalled. The existing Docker Desktop was started after user approval.', '',
        f"Final task: **v0.1.3**. Native Harbor checksum: `{qc['harbor_task_checksum']}`. Author file-framing SHA-256: `{digest.hexdigest()}`. The two hashing schemes differ intentionally; individual task-file hashes are in authoring/task_file_manifest.json.", '',
        '| Actual job | Trial | Reward | Tests passed | Exceptions |',
        '|---|---|---:|---:|---:|']
    for t in qc['trials']:
        lines.append(f"| {t['job']} | {t['trial']} | {t['reward']} | {t['passed']}/{t['tests']} | 0 |")
    lines += ['', 'Both oracle repeats used clean containers and the same final checksum. Each evaluates all 36 pencils in nine distinct mandatory batches. The helper adapter submits a general correct source implementation that executes a supporting Python file; its 9/9 pass verifies acceptance of that permitted layout. The partial adapter submits the finite-Smith-only baseline and passes just one batch. No baseline is an AI calibration trial.', '',
        'Exact executed native commands, from F:/rl/math-benchmark with the installed Docker CLI on PATH:', '', '```powershell',
        'harbor lint .\\tasks\\mathematical-sciences\\applied-mathematics\\certified-pencil-structure --json',
        'harbor run --path .\\tasks\\mathematical-sciences\\applied-mathematics\\certified-pencil-structure --agent oracle -k 2 --job-name oracle-v013-repeat --jobs-dir .\\authoring\\reports\\harbor-jobs --n-concurrent 1',
        'harbor run --path .\\tasks\\mathematical-sciences\\applied-mathematics\\certified-pencil-structure --agent nop --job-name nop-v013-1 --jobs-dir .\\authoring\\reports\\harbor-jobs --n-concurrent 1',
        '$env:PYTHONPATH = (Get-Location).Path',
        'harbor run --path .\\tasks\\mathematical-sciences\\applied-mathematics\\certified-pencil-structure --agent authoring.evidence.baseline_agent:PartialAgent --job-name partial-v013-1 --jobs-dir .\\authoring\\reports\\harbor-jobs --n-concurrent 1',
        'harbor run --path .\\tasks\\mathematical-sciences\\applied-mathematics\\certified-pencil-structure --agent authoring.evidence.baseline_agent:ExecutableHelperAgent --job-name helper-v013-1 --jobs-dir .\\authoring\\reports\\harbor-jobs --n-concurrent 1',
        '```', '',
        'Raw config.json/result.json/lock.json, agent records, verifier pytest.log/ctrf.json/reward.txt, and console logs are retained in harbor-jobs/ and sibling log files. The first v0.1.0 oracle command used --force-build and built both environments successfully; later builds reused valid Docker layer cache. Final v0.1.3 agent/verifier build logs are agent_build_v013.log and verifier_build_v013.log. No additional --no-cache build is claimed.', '',
        'Final isolation_probe_v013.json and agent_leakage_probe_v013.json both pass: candidate UID/GID 65534 with empty supplementary groups; access to hidden tests and reward writes denied; CPU 180 sec, address-space 2147483648 bytes, FD limit 128. The agent image has only /app/spec.md and /app/data/examples.json as application files, without /tests/cases.py or /solution/solve.py. The offline separate verifier installs dependencies at build time and derives rewards from pytest exit status.', '',
        f"Portable source validation is independently labeled in local_validation_v013.json: {len(local['results'])} checks passed in {local['seconds']:.3f} seconds. Its docker_validated/harbor_validated flags deliberately remain false; the actual native results above provide those distinct proofs. Final Harbor lint returned [].", '',
        'History: v0.1.1 repaired CTRF parameter aggregation by assigning distinct test names; v0.1.2 added previously public dimension-18, infinity-size-six, and higher-degree finite-factor coverage. v0.1.3 repaired an independently reproduced fairness defect: the old harness removed execute access from valid supporting source files. The final copied program files are executable but root-owned/read-only to the candidate. The spec also clarifies writable paths and per-process/per-file limits. Old rejection evidence is executable_helper_probe_before.json, and prior harness/spec sources are preserved under authoring/provenance/. No mathematical instance, invariant, certificate, or acceptance criterion changed in v0.1.3; no completed model outcome informed a change.', '',
        'This validates the implementation and local infrastructure. It does not establish empirical model difficulty, a 40-60% success rate, independent expert approval, or upstream maintainer acceptance.']
    write(REPORTS / 'harbor_validation.md', '\n'.join(lines))

    history = []
    for name, file in [('Hydrogen preliminary v0.1.2', 'hydrogen_interrupted_summary.json'),
                       ('Flash preliminary v0.1.2', 'flash_v012_interrupted_summary.json'),
                       ('Flash primary v0.1.3', 'trajectory_summary.json')]:
        data = read(TRAJ / file)
        history.append({'label': name, 'summary_path': str(TRAJ / file), 'task_version': data['task_version'],
            'model': data['model'], 'attempted_trials': data['attempted_trials'],
            'completed_valid_trials': data['completed_trials'], 'interrupted_trials': data['interrupted_trials'],
            'stop_reason': data.get('stop_reason')})
    dump(TRAJ / 'calibration_history.json', {'pooling_permitted': False, 'batches': history})
    row = summary['trials'][0]
    native = read(Path(row['result_path']))
    assert native['exception_info']['policy']['has_valid_reward'] is False
    analysis = f'''# Calibration and trajectory analysis

Final task v0.1.3; same installed Terminus-2 2.0.0 agent, requested model gemini/gemini-3.8-flash, Harbor 0.27.0. The primary batch is **INCOMPLETE due to provider unavailability**. Requested: 8 independent valid trials. Actually attempted on the final version: {summary['attempted_trials']}. Valid completions: {summary['completed_trials']}; successes: {summary['successful_trials']}; ordinary failures: {summary['failed_trials']}; infrastructure interruptions: {summary['interrupted_trials']}. Observed success/failure rates and valid-trial mean/median time are undefined. The requested 40-60% difficulty target is unmeasured.

| Run | Elapsed sec | Agent steps / tool calls | Input / output tokens | Native raw reward | Classification |
|---|---:|---:|---:|---:|---|
| {row['run_id']} | {row['duration_sec']:.6f} | {row['steps']} / {row['tool_calls']} | {row['input_tokens']} / {row['output_tokens']} | {row['reward']} | INTERRUPTED: ServiceUnavailableError |

Google returned repeated HTTP 503 UNAVAILABLE/high-demand responses through its official generateContent endpoint. The native final exception policy explicitly records has_valid_reward=false. Therefore the raw 0.0 is excluded from mathematical success/failure statistics. No usable agent solution or graded mathematical trajectory was produced; the ATIF file, exception trace, console and native result are preserved. The runner stopped before starting trials 2-8 under its recorded infrastructure-error rule. Missing trials are not fabricated or counted as failures.

Configuration is preserved in calibration_manifest.json, including all eight planned commands, per-file hashes, final author digest {digest.hexdigest()}, and native task checksum {qc['harbor_task_checksum']}. Containers are fresh and serial; agent budget 28800 sec, 2 CPU / 4 GiB. The wrapper spaces outer LiteLLM calls by at least 16 sec without changing messages or the agent. All planned trials use request timeout 300 sec and SDK retry count zero; installed Harbor retry layers remain native. Full messages/pane logs/ATIF are enabled; terminal .cast recording is disabled. Model-catalog version 3.0 is generic alias metadata, not an immutable deployment pin. No paid fallback, billing change, or publication occurred. Cost for this primary interrupted attempt is unavailable; token zeros from the harness do not prove zero billed cost.

Preliminary attempts are retained separately and never pooled into the primary sample:

- Hydrogen v0.1.2, gemini-v012-01: 636.184729 sec, 8 agent steps / 3 tool calls, 14943 input / 383 output tokens. Repeated HTTP 503 followed by HTTP 429/free-tier 5 RPM led to native RateLimitError; raw reward 0.0 is invalid. Harness cost USD 0.023589825 is an estimate, not a billing receipt. Zero valid completions. The user then approved switching to Flash.
- Flash v0.1.2, flash-v012-01: 1293.391 sec, provider-stalled with no saved usable response. The operator stopped its exact own processes/container before grading to repair an independently confirmed executable-helper fairness defect. There is no native final trial result; operator snapshots and flash_v012_operator_interruption.json preserve the event. No mathematical outcome was observed. This batch is retired after the v0.1.3 repair.

The final v0.1.3 fairness repair was validated by two oracle passes, a correct executable-helper pass, no-op/partial rejection, and renewed isolation probes before primary calibration. No completed model result was available to tune against; mathematics was unchanged by this repair.

There is no evidence to attribute these interruptions to mathematical reasoning, planning, exact arithmetic, or implementation failure. Such analysis requires valid completed trajectories. Resume only when the same approved free-tier provider/model is available, retain the frozen task and agent configuration, preserve existing jobs, and collect eight valid independent trials. A later resumed sample must document its dates and provider alias limitations. Then report exact observed counts, uncertainty, common mathematical failure modes, and any justified new-version retesting. Independent domain review remains outstanding.
'''
    write(REPORTS / 'trajectory_analysis.md', analysis)

    original_text = (AUTH / 'originality_assessment.md').read_text(encoding='utf-8')
    original_text = original_text.split('\nExecuted scoped audit:')[0]
    original_text = original_text.replace('A reproducible local audit process will compare', 'The implemented reproducible local audit process compares')
    original_text = original_text.replace('and must remain unmeasured until an actual scoped audit executes.', 'and are reported only for the executed scope below.')
    write(AUTH / 'originality_assessment.md', original_text + f'\n\nExecuted scoped audit on final source: twelve browser-returned documents, maximum weighted similarity {maxsim:.6f}%, heuristic originality {original:.6f}%. This clears the documented numerical review threshold only on that scope. Two silicon source windows are incomplete. Full-corpus clearance and a semantic embedding model were not performed. The related tensor-rank-toolkit was found after implementation and is acknowledged in reports/data_provenance.md; the canonical-form objective is classical, so low textual similarity does not establish conceptual uniqueness.')
    similarity['manual_conceptual_review'] = {
        'related_public_implementation': 'https://github.com/Tewf/tensor-rank-toolkit',
        'assessment': 'Classical exact matrix-pencil structural analysis is a shared conceptual objective. The new benchmark contract, constructive evaluator, and certificate rules were independently implemented before this library was inspected. No source/data reused.',
        'global_novelty_status': 'WARNING', 'independent_domain_review': 'OUTSTANDING'}
    dump(AUTH / 'plagiarism/reports/plagiarism_report.json', similarity)
    plag_md = (AUTH / 'plagiarism/reports/plagiarism_report.md').read_text(encoding='utf-8')
    if 'Related public implementation:' not in plag_md:
        write(AUTH / 'plagiarism/reports/plagiarism_report.md', plag_md + '\nRelated public implementation: [tensor-rank-toolkit](https://github.com/Tewf/tensor-rank-toolkit) shares the classical structural-analysis objective. Its README was included in the comparison, but the code was not copied. Conceptual overlap remains an explicit WARNING; lexical scores do not establish global novelty.')

    write(ROOT / 'README.md', f'''# Local Mathematics benchmark

Exactly one implemented task: **Certified Kronecker Structure of Singular Matrix Pencils**, mathematical-sciences/applied-mathematics, version **0.1.3**. Task path: [certified-pencil-structure](tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure/). It requires exact normal rank, finite Smith factors, infinite block sizes, left/right minimal indices, and independently checkable polynomial minimal bases.

Local Docker/Harbor validation passed. Both oracle repeats and a correct executable-helper implementation scored 1.0, each passing all nine batches / 36 exact pencils. No-op and partial baselines scored 0.0; the partial passed only one batch. Final isolation/leakage probes and lint also passed. See [native validation](authoring/reports/harbor_validation.md).

**The overall requested project is not fully calibrated.** The approved Flash batch on the final version made one real attempt, which ended after 742.800616 sec with Google HTTP 503 before any valid mathematical grading. Zero of eight requested valid trials completed; success rate is undefined. The batch stopped under its infrastructure-error rule. Earlier Hydrogen and Flash v0.1.2 interruptions are separately retained. No 40-60% measured rate or demonstrated extreme difficulty is claimed. See [trajectory analysis](authoring/reports/trajectory_analysis.md) and [machine-readable final status](authoring/reports/final_delivery_status.json).

All work is local. Objective 12 and publishing requirements are removed in authoring/project_brief.md. No remote repository, commit, push, publication, registry upload, or hosted submission was performed. Public references were inspected through browser-accessible sources only.

Supporting records:

- [Complete project file hierarchy](authoring/reports/task_directory_tree.txt)
- [Proposal](authoring/task_proposal.md), [reference comparison](authoring/reference_analysis.md), [mathematical research](authoring/math_research_review.md)
- [Originality assessment](authoring/originality_assessment.md), [scoped similarity audit](authoring/plagiarism/reports/plagiarism_report.md)
- [Evaluator coverage](authoring/reports/evaluator_coverage.md), [QC](authoring/reports/qc_audit.md), [40-criterion audit](authoring/reports/implementation_rubric_audit.md)
- [Trial summaries and native evidence](authoring/trajectories/), [reproduction commands](REPRODUCING.md)

Scoped heuristic originality is {original:.2f}% over twelve browser-returned documents, with explicit source coverage and hashes. It does not establish global novelty. Independent domain review, measured expert time, and empirical extreme difficulty remain open warnings.
''')
    coverage = (REPORTS / 'evaluator_coverage.md').read_text(encoding='utf-8').replace('local_validation_v012.json', 'local_validation_v013.json')
    coverage = coverage.split('\nFinal v0.1.3 execution-contract evidence:')[0]
    write(REPORTS / 'evaluator_coverage.md', coverage + '\n\nFinal v0.1.3 execution-contract evidence: the independently reproduced supporting-executable rejection was corrected and a correct helper-based submission now passes 9/9 native tests. Both oracle repeats also pass 9/9, no-op 0/9, partial 1/9. Final isolation_probe_v013.json and agent_leakage_probe_v013.json pass. The copied program tree is root-owned/read-only to the candidate, with executable helpers; fresh work/output directories are writable. CPU/address-space/file limits are per process and file, as stated in the public spec. The suite includes 1x18 and 18x1 zero pencils, dimension 18 mixed structure, infinity size six, and higher-degree finite factors.')
    scope = (REPORTS / 'PROJECT_SCOPE.md').read_text(encoding='utf-8').split('\nLatest authorized state:')[0]
    scope = scope.replace('This is not yet a validated final deliverable.', 'This initial scope was recorded before execution; the latest state below supersedes its pending approvals.')
    write(REPORTS / 'PROJECT_SCOPE.md', scope + '\n\nLatest authorized state: local solver/test/QC/originality runs, start of the existing Docker Desktop, container builds/dependency downloads, full local Harbor validation, Gemini model availability checks, and free-tier serial calibration were explicitly approved. The user authorized container tmux setup and a switch from Hydrogen to eight fresh Flash trials; no paid fallback was allowed. These authorized actions were carried out to the extent provider availability permitted. Final v0.1.3 implementation and Harbor validation pass; calibration remains incomplete after one primary HTTP 503 interruption with zero valid completions. No host reinstall or publishing operation was performed.')
    protocol = (REPORTS / 'calibration_protocol.md').read_text(encoding='utf-8')
    protocol = protocol.replace('Task v0.1.2 is frozen at', 'Historical preliminary task v0.1.2 was frozen at', 1)
    protocol = protocol.split('\nFinal primary batch v0.1.3:')[0]
    write(REPORTS / 'calibration_protocol.md', protocol + f'\n\nFinal primary batch v0.1.3: native checksum {qc["harbor_task_checksum"]}, author framing digest {digest.hexdigest()}. The independently confirmed executable-helper permissions defect was fixed before this batch; all mathematical inputs and acceptance conditions stayed fixed. Two native oracle repeats and a correct helper submission passed before launch. The per-request timeout is 300 sec, SDK retries zero, with native Harbor retry layers unchanged; this configuration is fixed for all eight planned trials. flash-v013-01 ended with ServiceUnavailableError/HTTP 503 after 742.800616 sec, no valid reward, zero agent steps, and zero valid completions. The runner stopped under the previously recorded infrastructure-error rule and did not launch trials 2-8. This is an incomplete calibration, not a 0% mathematical success rate. Existing jobs and preliminary summaries remain preserved; no task changes or unapproved model fallback followed this outcome.')
    print(json.dumps({'final_version': '0.1.3', 'native_checksum': qc['harbor_task_checksum'], 'calibration': summary['status'], 'valid_completed': summary['completed_trials'], 'scoped_originality_percent': original}))

if __name__ == '__main__':
    main()