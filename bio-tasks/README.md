# Two Biology benchmark tasks

Exactly two independently authored Biology tasks use the paired count/TPM representations of GEO GSE273600.

The [next calibration review and approval package](authoring/calibration_phase2_20261126/README.md) proposes a separately versioned Task 2 repair and five new trials per task. Its permission/usage review is complete; task changes and ten new model trials await explicit approval. Historical initial results remain as recorded below.

Latest status, 26 November 2026: the final pre-model audit and initial Gemini Harbor trajectories are complete. Read [FINAL_AUDIT_AND_INITIAL_GEMINI_RESULTS.md](FINAL_AUDIT_AND_INITIAL_GEMINI_RESULTS.md) for the current comparison and all limitations. Both completed trajectories received reward 0 with 10/11 checks; one earlier Task 1 attempt was interrupted by provider HTTP 503 errors and is excluded from scientific failure counts. Requirements and frozen task versions were unchanged. Public redistribution is not fully cleared; Task 2 retains a conditional predictable-seed shortcut warning. Intended extreme difficulty remains uncalibrated.

| Task | Scientific objective | Agent contract |
|---|---|---|
| Task1: specificity envelope | Parental-control equivalence, construct-associated responses and assumption-dependent early bounds. | [instruction.md](biology-task-1/task/instruction.md) |
| Task2: transcript provenance | Cross-representation identity, technical mixtures and held-out rejection. | [instruction.md](biology-task-2/task/instruction.md) |

Each `biology-task-N/task` is a self-contained Harbor package with its own image, data, private verifier, reference and tests. Beside it, `authoring/` holds proposals, independent QC, separate plagiarism reports, baselines and logs. Neither runnable task depends on the other. Original downloads were not modified.

Byte-verified canonical QC copies are in each `authoring/package/tasks/life-sciences/biology/<slug>`; these are copies of the same two tasks, not additional tasks. Harbor runs the direct `task` directories; canonical paths satisfy repository naming checks. Local rubric review is distinct from external QC.

The [original creation report](TWO_BIOLOGY_TASKS_FINAL_REPORT.md) records the historical pre-provider gate. Separate plagiarism reports are under each task's `authoring/originality`; the [cross-task report](authoring/originality/cross_task_similarity_report.md) retains raw/substantive measures and limitations.

Coordinator scripts under `authoring/` reproduce staging, clean builds, lint, deterministic Harbor controls, isolation/offline checks, reward/CTRF summaries and originality comparison. QC tooling is bundled in `authoring/qc_profile`; authoring needs Python/Docker/Harbor, with no model provider. Each task has `authoring/REPRODUCING.md`.

See [data_audit.md](authoring/data_audit.md) and [experimental_design.md](authoring/experimental_design.md) for fractional counts, positive TPM floor, missing UT2 and effective-length/replicate limits. All synthetic controls and aliquots are labeled. No code was committed, pushed or publicly published. Initial provider use was explicitly authorized after the final audit; settings, consumption, errors and artifacts are preserved under `authoring/trajectories/initial-gemini35lite-high-20261126`. One completed initial trajectory per task is diagnostic and does not calibrate a reliable success rate. New host reports, trajectories and configurable caches are on F; existing installations and Docker Desktop virtual-disk storage remain in their existing locations.
