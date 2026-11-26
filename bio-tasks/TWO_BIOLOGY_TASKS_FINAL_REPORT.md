> Historical creation-stage report: its no-provider/approval-pending statements describe the state before the user authorized initial Gemini trials. For the current audit, trajectories, rights/shortcut limitations and results, see [FINAL_AUDIT_AND_INITIAL_GEMINI_RESULTS.md](FINAL_AUDIT_AND_INITIAL_GEMINI_RESULTS.md).

# Two Biology tasks: final local validation report

Completed 26 November 2026. Exactly two independent creator agents and two fresh independent QC reviewers participated; roles/context separation are recorded in `authoring/agent_roles.json`. Heavy native runs were serialized. All source downloads and generated packages remain local. No commit, push, publication, remote upload or provider API call was made.

## Scientific comparison

| | Task 1: specificity-envelope | Task 2: transcript-provenance-audit |
|---|---|---|
| Research question | Which observed construct-associated changes satisfy affirmative parental-control evidence, and what early ranges remain under missing-control assumptions? | Which source libraries generated anonymous representations and technical aliquots, and which two-source explanations fail validation? |
| Hypothesis / decision | Parental equivalence plus interaction/minimum-effect evidence; abstain or give conditional ranges at 2 h | Recover provenance/support/representation fractions; reject unsupported sparse explanations |
| Methods | Relative-count logCPM, independent-group Welch uncertainty, TOST, joint-null BY, partial identification | Compositional scaling, nuisance-centered identity correlation, assignment, weighted convex deconvolution, disjoint-gene validation |
| Five linked layers | Representation/universe → matched factorial effects → heteroscedastic inference → joint certificate → missing-control envelope | Representation audit → identity calibration → bijection → sparse support/weights → held-out rejection |
| Outputs | Six full data artifacts including matched statistics, early bounds and synthetic calibration | Three artifacts: mapping, aliquot explanations and audit |
| Evaluation | Independent moments/contrasts, full families, positive/null/boundary controls | Source-derived identity/mixture truth, independently optimized residual certificates |

Both use one real experiment represented in two matrices: 57,665 genes × 120 samples. Full gzip inspections, fractional values, floor behavior, GSM-reconciled design and source checksums are in shared authoring reports. No untreated 2 h control was fabricated. No ATF4 causal claim is inferred from expression alone.

## Separate final task status

### Biology Task 1: specificity-envelope (v0.1.0)

- **Scientific Domain:** Biology / transcriptomics and statistical genomics.
- **Oracle:** PASS 11/11, two native repeats; native repeat artifacts byte-identical.
- **Negative Baselines:** PASS: 10 controls rejected locally and in valid native trials. Per-family local and native counts are separate in their reports.
- **Alternative / Hidden-Test Discrimination:** PASS 11/11 independently implemented/equivalent scientific reconstruction; PASS within documented error families; easy controls identified.
- **Docker/Harbor:** PASS actual clean builds and separate-verifier grading; 13 exception-free deterministic trials, one frozen checksum.
- **Static QC:** 29/29 PASS; remaining statuses: 0.
- **Rubric QC:** 37/38 PASS, 1 nonblocking difficulty WARNING; local independent assessment, external automated rubric panel NOT RUN; no local FAIL/NOT TESTED; any nonblocking warning retained.
- **Independent QC:** PASS WITH LIMITATIONS local fresh reviewer /root/qc_a; initial findings, corrections and rechecks retained.
- **Originality:** PASS within audited corpus; maximum reviewed substantive overlap 25%.
- **External QC:** NOT RUN. **Gemini Authorization:** PENDING explicit user approval at handoff; no API used.
- **Valid Agent Trials:** NOT RUN (0/8). **Observed Success Rate:** NOT MEASURED.
- **Scientific limits:** All real-data joint certificates are negative; transformed relative-count associations lack effective-length offsets. Early ranges condition on unverified control envelopes and observed anchors. Triplicate labels do not establish biological population replication.
- **Remaining Issues:** External automated/model judge QC has not been run; local 38-check review is not external approval. Expert/frontier-agent difficulty, 35–60% success and completion time remain unmeasured. Finite-corpus originality review cannot exclude unseen work.
- **Final Non-Gemini Status:** VALIDATED for available local non-model checks. **Final Verdict:** READY FOR EXTERNAL QC.

Evidence directory: `biology-task-1/authoring/reports/`: `static_qc.{md,json}`, `rubric_qc.{md,json}`, `independent_qc_review.md`, `independent_qc_findings.json`, `reviewer_recheck.md`, `qc_remediation.md`, `local_validation.json`, `native_summary.json`, `harbor_validation.md`, clean-build/Harbor logs, isolation JSON, CTRF and complete trials. Separate originality evidence is in `biology-task-1/authoring/originality/`.

### Biology Task 2: transcript-provenance-audit (v0.1.1)

- **Scientific Domain:** Biology / transcriptomic provenance and integrity.
- **Oracle:** PASS 11/11, two native repeats; native repeat artifacts byte-identical.
- **Negative Baselines:** PASS: 9 controls rejected locally and in valid native trials. Per-family local and native counts are separate in their reports.
- **Alternative / Hidden-Test Discrimination:** PASS 11/11 independently implemented/equivalent scientific reconstruction; PASS within documented error families; easy controls identified.
- **Docker/Harbor:** PASS actual clean builds and separate-verifier grading; 12 exception-free deterministic trials, one frozen checksum.
- **Static QC:** 29/29 PASS; remaining statuses: 0.
- **Rubric QC:** 38/38 PASS, 0 nonblocking difficulty WARNING; local independent assessment, external automated rubric panel NOT RUN; no local FAIL/NOT TESTED; any nonblocking warning retained.
- **Independent QC:** PASS local fresh reviewer /root/qc_b; initial findings, corrections and rechecks retained.
- **Originality:** PASS within audited corpus; maximum reviewed substantive overlap 25%.
- **External QC:** NOT RUN. **Gemini Authorization:** PENDING explicit user approval at handoff; no API used.
- **Valid Agent Trials:** NOT RUN (0/8). **Observed Success Rate:** NOT MEASURED.
- **Scientific limits:** Technical aliquots and provenance disruptions are synthetic. Feature holdout is not independent biological replication; fractions describe supplied expression representations, not cell fractions.
- **Remaining Issues:** External automated/model judge QC has not been run; local 38-check review is not external approval. Expert/frontier-agent difficulty, 35–60% success and completion time remain unmeasured. Finite-corpus originality review cannot exclude unseen work.
- **Final Non-Gemini Status:** VALIDATED for available local non-model checks. **Final Verdict:** READY FOR EXTERNAL QC.

Evidence directory: `biology-task-2/authoring/reports/`: `static_qc.{md,json}`, `rubric_qc.{md,json}`, `independent_qc_review.md`, `independent_qc_findings.json`, `reviewer_recheck.md`, `qc_remediation.md`, `local_validation.json`, `native_summary.json`, `harbor_validation.md`, clean-build/Harbor logs, isolation JSON, CTRF and complete trials. Separate originality evidence is in `biology-task-2/authoring/originality/`.

## Originality and similarity

Conservative cross-task substantive overlap is **2.5%**; each task external maximum is 25% under the disclosed six-dimension manual rubric. Rubric nonoverlap 75% meets the requested 70% target within the audited corpus, not as a universal originality guarantee. Raw pinned TF-IDF 35.690629%/37.233581%, initial 34.113431%, adjusted cross-task 8.217224%, and generic AST≈99% are all retained. High raw values were investigated directly; no wording was manipulated. See the separate task plagiarism reports, all 195 cached-source metric rows, independent matched-section reviews and `authoring/originality/cross_task_similarity_report.{md,json}`.

The generic AST histogram is not a substantive-copying measure; direct scientific-code inspection and 12-token fingerprints show distinct calculations/evaluators. Source publication specificity motivation is counted where genuinely shared. Manual additional primary-article/abstract comparisons have their reading limits stated. Unretrieved/private research remains outside the audit.

## Validation precision and limitations

The final Task 2 version 0.1.1 fixes actual CTRF parameter aggregation, so eleven distinct checks appear in its final native results. Version 0.1.0 results remain historical and are excluded from its final gate. Task 1 experienced one transient Docker HTTP 500 sidecar error and nine preflight interruptions; all are retained and excluded from scientific results, with successful clean retries. They are infrastructure incidents, not model failures.

Native no-op runs confirm no stale solution artifacts. Inputs are root-owned/read-only in the unprivileged solver, private solution/tests absent from its normal image, verifier directories private, verifier egress blocked, and fully offline oracle execution observed. Only static submission artifacts transfer; the privileged verifier executes no submitted code. Pinned wheels/inputs are bundled. Current tested host/container architecture is Windows host with Linux/amd64 Docker; other architectures were not validated.

The 29 static checks executed locally, including actual pinned shell rules and Harbor 0.27 lint ALL. The 38 rubric checks were separately assessed by fresh local reviewers with executable evidence; the external automated/model-judge pipeline was not invoked. No external QC PASS or calibrated extreme difficulty is claimed. No unapproved API key was used.

## Reproduction and handoff

Read each task authoring REPRODUCING.md. Coordinator scripts under `authoring/` reproduce staging, clean builds, deterministic Harbor controls, isolation, static reports, original/canonical integrity and originality metrics. Canonical staging contains byte-identical copies of the same two runtime tasks for repository path conventions. Original input hashes and 192 direct source/canonical file checks are recorded in `authoring/data_integrity_final.json`.

Gemini difficulty calibration is a separate optional step requiring explicit user approval under the attached brief. No API evaluation has begun.
