# Final audit and initial Gemini trajectory comparison

Completed 26 November 2026 (Asia/Karachi). The user authorized initial Gemini trajectories after the final audit. No scientific requirements, thresholds, source fixtures or private evaluator rules were changed to force model failure. This is one requested initial diagnostic trajectory per task, not an eight-trial calibration.

## Audit outcomes

| Audit item | Task 1 | Task 2 |
|---|---|---|
| Scientific implementation | Independent full original-data calculation agrees within published tolerances | Independent original-source identities/weights/adequacy checks agree |
| Empty/incomplete outputs | Six focused adversarial cases rejected; correct control 11/11 | Empty/header-only/constant rejected; seed-only probe reward 0 |
| Direct oracle/answer-file leakage | No private code, tests or expected outputs in normal/live solver images | No private code, tests or truth fields observed; conditional predictable-seed risk retained |
| Originality | Source-specificity motivation overlaps; bounded manual max 25% | Prior sample-integrity/mixture methods overlap; bounded manual max 25% |
| Intended extreme difficulty | Warning retained; prescribed formulas, empirical difficulty uncalibrated | Coherent reconstruction problem; extreme difficulty uncalibrated |
| Dataset integrity | Original 57,665 × 120 matrices and 120 GSM metadata verified | Same experiment; anonymous profiles/aliquots explicitly synthetic |
| Public redistribution | **NOT FULLY CLEARED** | **NOT FULLY CLEARED** |

The original publication uses **CC BY-NC-ND 4.0**, not unrestricted CC BY. Its article/figure license is distinct from independently deposited numerical data. NCBI does not impose repository restrictions but does not transfer submitter rights or provide unrestricted third-party permission. No explicit matrix-specific unrestricted license or complete third-party software redistribution clearance was established. No public release is cleared or performed. See [Nature rights](https://www.nature.com/articles/s41467-024-52538-5#rightslink), [NCBI policy](https://www.ncbi.nlm.nih.gov/home/about/policies/) and the detailed local rights audit.

Independent QC was performed by separate AI-agent contexts with executable evidence; it was not an external blind human scientific review or independent experimental replication. This new audit independently recalculated Task 1 from the original full matrix, strengthening prior inspection/log evidence. Technical triplicates, approximate small-n inference, selection and absent effective-length offsets limit biological claims. The early sensitivity interval omits anchor sampling uncertainty and rests on unverified control-envelope assumptions.

## Why Task 1 produces no certificates

There are 20,803 eligible genes and 249,636 joint gene/treatment/time hypotheses. A joint p value must satisfy interaction evidence, parental equivalence and a minimum engineered-line effect simultaneously. 6,018 rows pass all three nominal p≤.05 tests, but no row survives full-family correction.

For BY, H_M=13.0049768 and M×H_M=3,246,510.39. The best rank 196 has p=.0004335715 versus cutoff 0.000003018626, about 143.63 times above the significance threshold. Its uncapped adjusted ratio is 7.1816038, so clipping gives 1 for every q. Diagnostic BH on the same joint family also finds 0 discoveries, minimum adjusted ratio 0.55222. Therefore this is not a coding/clipping bug or solely BY conservatism. Equivalence and minimum-effect evidence are major bottlenecks; small replicate groups and a broad joint family limit affirmative certification. This does not mean the experiment has no biological responses.

![Observed joint probabilities and rejection thresholds](F:/rl/bio/biology-task-1/authoring/reports/final_audit_20261126/joint_certificate_thresholds.png)

Empty discoveries are an allowed scientific conclusion, but empty result tables are not: complete eligible universes, effects, uncertainty, probabilities, early bounds and synthetic calibration outputs are required and checked. The focused unchanged-checker audit rejected no-files 0/11, zero-byte 1/11, header-only 3/11, 20-gene truncation 4/11, only-certified matched 7/11 and only-certified universe 4/11; all binary 0.

## Isolation, shortcut and originality limits

Fresh normal solver-image probes verified UID 1000, immutable intended data, protected parent directories, empty submissions, absent private paths and absent provider credentials. Live Task 1 and Task 2 Gemini container probes independently confirmed no /tests, /solution, /app/authoring or provider key. The separate privileged verifier parses static artifacts and does not execute submitted code.

Task 2’s default authoring seed equals accession digits 273600. Given the non-public RNG/draw conventions, replay can reconstruct 120 atlas labels and24 donor/weight records without expression values. The explicit seed-only probe passes 7/11 families but earns 0 because physical audit and numerical score/margin/residual certificates fail. No full reward without expression analysis was demonstrated. This is a genuine conditional shortcut warning, not a literal shipped-answer leak; it remains documented in the frozen diagnostic task.

Manual substantive ratings 25% external and conservative 2.5% cross-task are ordinal bounded judgments, not measured copied-content fractions or proof of 75% originality. Raw cross-task TF-IDF 35.69–37.23%, adjusted 8.2172% and generic AST≈99% remain visible with matching-section/code investigations. No cosmetic changes were made to reduce those scores.

## Initial Gemini execution

Model: `gemini/gemini-3.5-flash-lite`; agent: `terminus-2` 2.0.0; high reasoning setting; XML parser; 32768 maximum output tokens/request; native default turn allowance; original task timeout/resource limits. Each task begins from a clean environment without previous trajectory/oracle access. Transport-only retries are bounded and separately recorded. Model availability was confirmed by catalog metadata. Official [model/pricing](https://aistudio.google.com/docs/models/gemini-3.5-flash-lite) lists a standard free tier; actual project billing tier/invoice is not verified, and SDK costs are estimates. No billing upgrade or paid-only fallback occurred.

| Task / attempt | Status | Reward | Verifier passed/total | Wall seconds | Agent seconds | Agent steps / tools | Input / output / cache tokens | Provider errors |
|---|---|---:|---|---:|---:|---|---|---:|
| 1 / bio1-initial-01 | INFRASTRUCTURE_INTERRUPTION | 0.0 | 0/11 | 566.80 | 517.01 | 10 / 9 | 100964 / 8196 / 65163 | 11 |
| 1 / bio1-initial-02 | SCIENTIFIC_OR_SUBMISSION_FAILURE | 0.0 | 10/11 | 965.04 | 919.09 | 22 / 23 | 549119 / 24132 / 464968 | 17 |
| 2 / bio2-initial-01 | SCIENTIFIC_OR_SUBMISSION_FAILURE | 0.0 | 10/11 | 594.61 | 550.56 | 23 / 22 | 415118 / 17331 / 282828 | 4 |

Native token fields and provider-returned sums are both preserved in `initial_comparison.json`/CSV. Cache reads are a subset of input tokens, not extra inputs. Null reasoning counts mean not reported; non-null sums cover only calls that returned a reasoning-token field, and the reporting-call count is provided below. These reasoning tokens must not be added to output-token totals. Only successful requests return token usage; error-side consumption/invoice cannot be invented. Provider failures, retries, model aliases and exceptions are not scientific failures.

### Individual verifier outcomes

#### Task 1 — bio1-initial-01

| Verifier check | Result |
|---|---|
| test_outputs.py::test_01_complete_handoff | failed |
| test_outputs.py::test_02_fractional_representation_audit | failed |
| test_outputs.py::test_03_unselected_complete_gene_universe | failed |
| test_outputs.py::test_04_matched_factorial_effects | failed |
| test_outputs.py::test_05_heteroscedastic_uncertainty | failed |
| test_outputs.py::test_06_affirmative_equivalence_and_minimum_effect | failed |
| test_outputs.py::test_07_joint_family_multiplicity | failed |
| test_outputs.py::test_08_early_partial_identification | failed |
| test_outputs.py::test_09_envelope_expansion_invariants | failed |
| test_outputs.py::test_10_interpretation_limits | failed |
| test_outputs.py::test_11_synthetic_positive_and_degenerate_controls | failed |

Scientific/submission diagnosis: Provider ServiceUnavailableError after bounded 503 retries interrupted the agent at 10 steps. Successful requests consumed 100,964 input and 8,196 output tokens. The submission was unfinished, so all 11 checks failed and reward was 0. This interrupted attempt is excluded from scientific success/failure counts; no conclusion about biological/statistical capability is justified. Recorded operational errors included protected-directory writes, one XML parser failure and an import of unprovided statsmodels. These were not the terminal cause: the provider interruption ended the trajectory. No seed/private-file probes or online-fetch commands were observed in the executed-command review.

#### Task 1 — bio1-initial-02

| Verifier check | Result |
|---|---|
| test_outputs.py::test_01_complete_handoff | passed |
| test_outputs.py::test_02_fractional_representation_audit | passed |
| test_outputs.py::test_03_unselected_complete_gene_universe | passed |
| test_outputs.py::test_04_matched_factorial_effects | passed |
| test_outputs.py::test_05_heteroscedastic_uncertainty | passed |
| test_outputs.py::test_06_affirmative_equivalence_and_minimum_effect | passed |
| test_outputs.py::test_07_joint_family_multiplicity | passed |
| test_outputs.py::test_08_early_partial_identification | passed |
| test_outputs.py::test_09_envelope_expansion_invariants | passed |
| test_outputs.py::test_10_interpretation_limits | passed |
| test_outputs.py::test_11_synthetic_positive_and_degenerate_controls | failed |

Scientific/submission diagnosis: Completed valid trajectory, reward 0 and 10/11 checks. All real-data contract families 1–10 passed. Synthetic minimum_effect_boundary has d=0.5, SE=0; the submitted source uses abs(d)>=0.5 to assign p=0, whereas the prespecified null includes equality and requires p=1. It consequently reports p_joint=0,q_joint=0,certified=true for this null boundary; expected p_dmr_minimum,p_joint,q_joint=1 and certified=false. This also changes synthetic BY rank adjustment. This is a documented boundary/null-handling error, not a floating-point tolerance failure or proof of broad biological inability. Recovered operational errors included a protected-directory write, one XML parser failure, a dict_items indexing error and an undefined variable. No grader or task change was made after observing it.

#### Task 2 — bio2-initial-01

| Verifier check | Result |
|---|---|
| test_outputs.py::test_schema | passed |
| test_outputs.py::test_physical_audit | failed |
| test_outputs.py::test_biological_limits | passed |
| test_outputs.py::test_sample_identity | passed |
| test_outputs.py::test_discovery_alignment_scores | passed |
| test_outputs.py::test_heldout_identity_certificates | passed |
| test_outputs.py::test_pure_aliquots | passed |
| test_outputs.py::test_two_source_aliquots | passed |
| test_outputs.py::test_open_set_rejection | passed |
| test_outputs.py::test_residual_certificates | passed |
| test_outputs.py::test_support_optimality | passed |

Scientific/submission diagnosis: Completed valid trajectory, reward 0 and 10/11 checks. Only test_physical_audit failed. All 120 identities, discovery scores, held-out identity margins, pure/pair assignments, unsupported-query rejection, residual certificates and support optimality passed. The submitted source uses A[col].min() after normalizing columns, while the published audit contract requires minima of the supplied scaled atlas. All 120 reported minima fail the required raw-scale tolerance; they agree with normalized minima within 1.32e-13. For A000, submitted 0.0630178480934 versus required 0.05053822693. This is a representation/bookkeeping failure, not failed mixture inference or a tolerance artifact. Four XML parser failures, a protected-directory write and a missing scratch-script command were recovered; four provider 503 errors were also recovered. Direct executed-command review found actual expression-based centering, assignment, weighted exhaustive pair fitting and disjoint-gene residual calculation, with no seed replay, private-answer path access or online fetch observed. This observation does not remove the task's independently demonstrated conditional seed shortcut risk. No task or grader was changed.

## What the initial results establish

Each task has one completed diagnostic trajectory, both reward 0 and 10/11 checks. Task 1 passed every real-data calculation and failed a prespecified zero-variance minimum-effect boundary case. Task 2 passed the complete identity/mixture inference and failed one supplied-versus-normalized scale audit field. These narrow failures do not demonstrate extremely difficult biological reasoning or validate the intended frontier-model success-rate range. The failed checks were present before the run and scientifically coherent; neither task was tightened after seeing these results.

Task 1 attempt 1 ended on an exhausted provider 503 retry sequence. Its unfinished-artifact reward 0 is preserved but excluded from scientific failure counts. Recovered 503s also occurred in the completed runs. Wall time includes startup, model latency, terminal execution, transport backoff, artifact transfer and grading; agent time is the native execution-phase duration. Steps count agent responses, including parser-error responses; tools include completion calls.

| Attempt | Successful provider calls | HTTP 503 errors | XML error observations | SDK cost estimate USD | Reported reasoning tokens |
|---|---:|---:|---:|---:|---:|
| bio1-initial-01 | 10 | 11 | 1 | 0.03318519 | 4365 (from 3 calls) |
| bio1-initial-02 | 22 | 17 | 1 | 0.09952434 | 415 (from 4 calls) |
| bio2-initial-01 | 23 | 4 | 4 | 0.09149934 | 1089 (from 7 calls) |

Terminal/parser error excerpts and all provider error timestamps, types, statuses and messages are recorded per attempt in `initial_comparison.json`. They include protected-directory writes corrected by using /tmp, malformed XML, scratch-code errors and one unprovided-library import in the interrupted attempt. Four XML errors occurred in Task 2. These operational errors were distinguished from the final scientific/submission diagnoses. No quota, authentication, out-of-memory or task-timeout failure was observed.

## Reasoning and potential model failures

**Task 1:** preserve fractional counts; align versioned gene/sample identities; compute full-library normalization and a complete eligible universe; construct valid contemporaneous factorial contrasts; carry independent-group uncertainty into equivalence/minimum-effect/intersection-union tests and global adjustment; bound unmeasured controls conditionally; distinguish no certificate from no response. Plausible failures include TPM/count substitution, false pairing, invented UT2, nonsignificance-as-equivalence, local corrections, omitted complete rows and missing positive/boundary calibration.

**Task 2:** calibrate nuisance gene/sample scales, recover a bijection across count/TPM representations, fit bounded sparse mixtures on the correct linear composition scale, validate numerical certificates on disjoint genes and reject inadequate supports. Plausible failures include abundant-gene correlations, row-position alignment, log-space mixing, donor/weight mistakes, forced two-donor attribution, validation leakage and interpreting representation weights as cell fractions.

Direct executed-command review found no seed replay, private-answer paths or online fetch in these trajectories. Task 2 actually computed gene/sample centering, a discovery-based assignment, weighted exhaustive donor-pair fits and validation residuals from expression values. This does not negate its independently demonstrated conditional seed shortcut. The scientific failure conclusions use individual test outcomes, submitted artifacts and executed commands; provider/setup failures are not assigned biological explanations.

## Evidence and storage

Pre-model audit: [audit report](F:/rl/bio/authoring/final_audit_20261126/PRE_MODEL_FINAL_AUDIT.md), [dated gate](F:/rl/bio/authoring/final_audit_20261126/pre_model_gate.json), [Task 1 independent review](F:/rl/bio/biology-task-1/authoring/reports/final_audit_20261126/final_pre_model_audit.md), [Task 2 science/isolation review](F:/rl/bio/biology-task-2/authoring/reports/final_audit_20261126/science_leakage_audit.md) and [provenance/rights/originality audit](F:/rl/bio/authoring/final_audit_20261126/provenance_originality/provenance_rights_originality_audit.md). Separate original plagiarism reports: [Task 1](F:/rl/bio/biology-task-1/authoring/originality/plagiarism_report.md), [Task 2](F:/rl/bio/biology-task-2/authoring/originality/plagiarism_report.md), and [cross-task comparison](F:/rl/bio/authoring/originality/cross_task_similarity_report.md). These include comparison methods and matched sections. The [post-trial integrity report](F:/rl/bio/authoring/final_audit_20261126/post_trial_integrity.json) verifies 192 file/evidence hashes against frozen manifests; the [credential-log scan](F:/rl/bio/authoring/trajectories/initial-gemini35lite-high-20261126/credential_log_scan.json) found no configured key values in the scanned trajectory logs. The [current outcome](F:/rl/bio/authoring/final_audit_20261126/final_outcome.json) distinguishes completed work from retained release and shortcut limitations.

Trajectories: [comparison JSON](F:/rl/bio/authoring/trajectories/initial-gemini35lite-high-20261126/initial_comparison.json), [metrics CSV](F:/rl/bio/authoring/trajectories/initial-gemini35lite-high-20261126/initial_comparison.csv) and [all individual checks CSV](F:/rl/bio/authoring/trajectories/initial-gemini35lite-high-20261126/individual_verifier_results.csv). The same directory retains settings/catalog metadata, provider events, all native attempts/results/CTRF, artifacts, trajectories, command extracts, scientific review and numerical mismatch diagnostics.

All new host outputs and configurable caches/tmp are on F under this project; `runtime-cache/` contains cache locations recorded in the manifest. Installed Python/Harbor and existing Docker Desktop virtual-disk storage remain in their existing locations; relocating global engine state was outside this task. No task files were published or uploaded to a repository.

Final disposition: computational/scientific task contracts remain locally verified with explicit limitations. Public redistribution remains NOT FULLY CLEARED, and Task 2 retains a conditional shortcut warning. The essential_difficulty warning remains unresolved by these initial results. A blanket no-shortcut or public-release certification is therefore not issued. Before broader benchmark release, address the Task 2 predictable-seed risk in a versioned fixture with fresh QC and establish the applicable redistribution permissions; these are integrity/rights issues, not reasons to tighten valid scientific thresholds. No requirements were changed to force failure and no target success rate was claimed.
