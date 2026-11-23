# Local Mathematics benchmark

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

Scoped heuristic originality is 96.18% over twelve browser-returned documents, with explicit source coverage and hashes. It does not establish global novelty. Independent domain review, measured expert time, and empirical extreme difficulty remain open warnings.

Current connection recovery: a separate Gemini 3.5 Flash-Lite/native-XML smoke-plus-eight batch is now active; see [latest batch pointer](authoring/trajectories/latest_calibration.json) and [connection diagnosis](authoring/reports/connection_recovery.md). Previous Flash 3.8 results above are retained as historical infrastructure interruptions.
