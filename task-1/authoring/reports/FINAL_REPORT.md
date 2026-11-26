# Task 1 v0.2.0 final non-model report

**Available non-model validation is complete.** The task is ready for separately authorized frontier-model testing. It is not certified to defeat models, achieve a 40–60% success rate, or have external QC approval. No provider API, paid API, Git commit/push or publication was performed.

Active task: `F:\rl\New folder\math-audit\tasks\mathematical-sciences\applied-mathematics\certified-pencil-structure`. Native Harbor checksum `0d9c54dfd0cb753e9dca38b78c1d9c8d89e649d4c5eea863e576898f75b7394d`. Author framing `c3f0390f31b44bce786267f5a6641bd41a33fd88a31356d0ad8bdc670cb4650d`. Independent JSON-manifest hash `77f1da70c5c59673b77bf0631d700e486c9f17d562daf6c384558f63dc8942e6`; the three algorithms are distinct and explicitly recorded.

| Item | Frozen v0.1.4 | Upgraded v0.2.0 |
|---|---|---|
| Version | 0.1.4 | 0.2.0 |
| Scope | Rank, finite/infinite structure, minimal indices and bases | Adds constructive constant frames, saturated modules, splitting and minimum finite-pole responses |
| Mathematical stages | Five natural obligation groups in this audit; not originally explicitly staged | 13 explicitly checked mathematical obligations |
| Dependency depth | Mostly rank feeding parallel invariants/bases; no formal old stage DAG | Eight-node longest displayed dependency path; algorithm order remains free |
| Complexity layers | Smith/reversal and bounded convolution-kernel algorithm families | Five connected scientific layers |
| Input dimensions | At most 18 by 18 | At most 18 by 18 |
| Minimal-index/infinity bounds | 4 / 6 | 8 / 8; explicit extra boundary probes pass |
| Graded pencils | 40 | 48; original 40 A/B pairs unchanged |
| Structural / easy cases | 34 / 6 | 42 / 6 |
| Forcing queries | None | 144, not counted as additional pencils |
| Fair traps | Repeated finite powers, infinity partitions, singular sides, exact scaling | Retains those; adds strict-vs-polynomial equivalence, saturation, projector consistency, rational-vs-polynomial response and intrinsic pole lower bounds |
| Oracle correctness | 4 archived final-checksum oracle repeats passed all 40 | 2 final-checksum fresh oracle repeats passed all 48; 40 regenerated +3 boundary inputs also pass |
| Negative baselines | Archived final-checksum negative controls denied full credit | Five native expected-zero controls, 16 per-pencil semantic mutants, constant/zero/numerical spectral guesses |
| Alternative acceptance | Archived helper and equivalent-rational native controls passed | Native changed construction passes; 48 author and 48 independently transformed alternatives pass |
| Docker / Harbor | Native PASS; redundant final no-cache rebuild had network interruption | Final two images build without cache; 8 final-checksum native trials all expected, no exceptions |
| Local static QC | 28 PASS, 1 NOT TESTED (pinned-corpus comparison) | 29 PASS, including complete saved 97-file pinned corpus |
| Local rubric QC | 36 PASS, 1 novelty WARNING, 1 N/A | 37 PASS, 1 justified N/A; scope limitations remain explicit |
| Independent QC | Archived local distinct review; external approval absent | Fresh-context local AI review: all 67 PASS, five limitations, no confirmed defect |
| Runtime | Archived raw timings preserved in frozen project | Mean final oracle grading 75.546 s; total native trial 97.979 s; largest batch 25.998 s below 180 s |
| Model success rate | Not established: reviewed Gemini runs interrupted, 0 valid | Not measured:0 provider calls and 0 valid model trials |
| External QC | Not run | Not run; no external service verdict claimed |

# Actual tests and results

| Check | Result | Evidence |
|---|---|---|
| Complete exact oracle/checker | 48/48 PASS | Final source per-file hashes and per-case timings: core_final_validation.json |
| Unseen regenerated inputs | 40/40 PASS | Two new seeds with opaque ids; regenerated_inputs.json |
| Additional public boundaries | 3/3 PASS | Infinity 8, both indices 8, maximum entry/forcing magnitudes; boundary_probes.json |
| Author changed valid certificates | 48/48 PASS | control_audit.json; includes nonconstant basis changes, changed inverse and particular solutions |
| Independent mathematical probes | 280/280 PASS | independent/independent_probe_results.json |
| Independent live verifier probes | 5/5 PASS | independent/independent_runtime_results.json |
| Final clean Docker builds | 2/2 images PASS | validation/r3-clean-*-build.log, with F: storage preflight |
| Native final-checksum trials | 8/8 expected results; 0 exceptions | Two oracle PASS, alternative PASS; partial/mutant/example/no-op/zero controls reward 0 |
| Fresh environment resets | 2/2 PASS | image_probe.json |
| Permission/network/resource/symlink boundary | PASS | isolation_probe.json |
| Scalar and required-field regressions | PASS | contract_regression.json; native and independent format probes complement this |
| Original/frozen preservation | 1426 files each, 0 differences | final_preservation.json |

# QC

| Audit | Actual result | Scope |
|---|---|---|
| Local static | {'PASS': 29} | All 29 supplied IDs, including actual pinned complete corpus comparison |
| Local rubric | {'PASS': 37, 'N/A': 1} | All 38 reviewed; separate hint mechanism absent, so creator marks that criterion N/A |
| Independent local AI | 29 static +38 rubric PASS; 0 fail; 5 warnings | Conditional hint criterion treated as satisfied with explicit applicability; same 67 IDs |
| External QC | NOT RUN | No external service/panel/human verdict is invented |

Independent reviewer initial findings were recorded before creator explanations. Its own 280 math checks, 5 native checks and 29 static checks passed. No confirmed active-package defect remains and no post-fix recheck is pending. See independent_qc_review.md and independent_qc_findings.json under independent/.

# Discrimination and alternatives

| Control | Actual result |
|---|---|
| Semantic wrong-answer controls | 16 variants evaluated per pencil; per-case first failure stages in control_audit.json |
| Numerical rank | Correct on all 48; 0 rejection, not presented as negative evidence |
| Numerical spectral-block heuristic | 40/48 rejected for primary-structure errors |
| Literal constant output | 0/48 accepted |
| Universal zero-structure guess | 3/48 accepted, precisely the zero pencils; native full reward 0 |
| Valid alternatives | 48 author and 48 independent transformed certificates accepted; native changed construction reward 1 |

All 42 declared structural cases reject at least one meaningful semantic wrong approach. These are author/reviewer controls, not independent AI attempts. Native CTRF is 12 four-case batches; separate per-pencil reports supply the finer discrimination evidence.

# Runtime and originality

Two final-checksum oracle repeats average 75.546 s in grader tests and 97.979 s total native trial wall time. Largest oracle batch 25.998 s versus the 180 s invocation cap. Maximum final portable per-pencil solver time 16.687 s. These are measured shipped-family results, not a worst-case runtime guarantee. The complete finite fallback can be exponentially expensive.

All 97 corpus files match hashes and the full saved tree. Maximum substantive instruction TF-IDF cosine is 16.450%, below the 30% requested finite-metric target; raw instruction maximum 16.791%. Own v0.1.4 inheritance is intentionally excluded from unrelated-plagiarism judgments. The code 12-token comparison covers one unrelated cached source task; this is not global plagiarism or theorem-novelty proof.

# Remaining limitations

| Item | Status |
|---|---|
| Empirical model difficulty / 40–60% target | NOT MEASURED:0 valid model trials; no success/failure percentage can be calculated |
| External/human QC | Not established; one local AI review is not external or human approval |
| Originality scope | Finite 97-instruction corpus and limited code reference |
| Worst-case runtime | Exponential finite fallback; observed margins apply to tested inputs |
| Batch reporting | 12 native batches complemented by per-pencil author/reviewer data |
| Expert time | 32 hours is an author estimate, not a measured human study |

# Actual storage

| Purpose | Actual path / record |
|---|---|
| Active package | `F:\rl\New folder\math-audit\tasks\mathematical-sciences\applied-mathematics\certified-pencil-structure` |
| All new project/supporting files | `F:\rl\New folder\math-audit` |
| Reports and native jobs | `F:\rl\New folder\math-audit\authoring\reports` |
| Configurable caches/temp/config | `F:\rl\New folder\math-audit\.local` |
| Docker VM storage | `F:\rl\New folder\DockerDesktopWSL` exclusively Docker, verified settings/registry/VHD paths |
| Originals | `F:\rl\math-benchmark` preserved |
| Existing C: binaries/system state | User-approved existing Python/Harbor/Docker; Windows/Codex/Docker may maintain system-managed logs/state |

The storage snapshot records 107.61 MiB of regular workspace files before the last small delivery reports. The Docker VHD is shared across projects; its size/growth must not be attributed solely to this upgrade. No VHD move/delete, global storage change or host installation was performed. See actual_storage.json for timestamps and sizes.

# Reproduction and next gate

[Exact reproduction commands](../../REPRODUCING.md), task_file_manifest.json, delivery_status.json, frozen_vs_upgraded.md, regression_report.md and the complete static/rubric/independent reports preserve the evidence. The original/frozen 1,426-file manifests remain intact.

Task 1's upgraded version has completed its available non-model validation and QC. Do you approve frontier-model testing now?
