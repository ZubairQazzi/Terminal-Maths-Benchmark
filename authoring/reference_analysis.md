# Browser-based reference analysis

Research date: 2026-11-23 (Asia/Karachi). Actual repository: [harbor-framework/terminal-bench-science](https://github.com/harbor-framework/terminal-bench-science). The registry identifier terminal-bench-science/terminal-bench-science is a dataset name, not the verified GitHub owner/path.

No checkout existed in F:/rl. The user declined downloading a reference snapshot, so source inspection used browser-accessible public files. No binaries, large reference datasets, or repository snapshot were fetched locally. Browser results do not establish an immutable commit and sometimes expose different cached revisions; findings below are bounded accordingly.

| Reference | Substantive challenge | Verifier pattern | Lesson for this task |
|---|---|---|---|
| mendota-ice-phenology | Sensor interpretation, cloud/missing observations, temporal transition inference | Separate image checks dated outputs and exact internal duration consistency | Couple intermediate mathematical choices to final outcomes |
| cilia-segmentation | Anisotropic 3D geometry and chained segmentation/orientation decisions | Hidden masks and measured geometry, plus internal consistency | Check structural objects, not just an aggregate scalar |
| si-fracture-fbc | Continuum/atomistic coupling, branch continuation, instability evidence | Recomputes physical quantities from submitted configurations | Recompute certificate identities instead of trusting self-reported residuals |

Independent design: none of these workflows, datasets, distinct scientific algorithms, or expected answers are reused. Our inputs are exact matrices, the output is structural polynomial algebra, and the grader uses constructive canonical invariants.

## Inspected file availability

For each task, browser-accessible task.toml, instruction.md, README.md, environment/Dockerfile, solution/solve.sh, tests/Dockerfile, tests/test.sh, and tests/test_outputs.py were inspected. The referenced implementation entrypoints were also located and inspected through browser source windows. These were source inspections, not executions or full data audits.

Verified roots:
- [Mendota task](https://github.com/harbor-framework/terminal-bench-science/tree/main/tasks/earth-sciences/geosciences/mendota-ice-phenology)
- [Cilia task](https://github.com/harbor-framework/terminal-bench-science/tree/main/tasks/life-sciences/biology/cilia-segmentation)
- [Silicon task](https://github.com/harbor-framework/terminal-bench-science/tree/main/tasks/physical-sciences/materials-science/si-fracture-fbc)

Implementation entrypoints observed:
- Mendota: solution/ice_phenology_pipeline.py. Its Dockerfile specifies build-time imagery retrieval with an immutable external-data revision and checksum validation; the underlying imagery was not downloaded.
- Cilia: solution/run_analysis.py delegates to cilia_analysis.py. The independent code and raw TIFF stacks were not exhaustively read. The expected-summary CSV fetch was inaccessible through the browser.
- Silicon: solution/oracle/oracle_emit_prod.py and environment/spec.md were accessible. Its newer README/spec describe mixed-mode crossover and barrier outputs, while some cached task.toml/test files show the earlier eight-artifact task. This is revision drift, not evidence of a verified coherent snapshot. The exact expected NPZ reference was not obtained.

The Mendota expected-date references.json was accessible. Cilia curated masks/CSV and silicon reference arrays were not verified. Do not infer their contents from filenames. The supplied geometry.json was read and describes a silicon crack-frame geometry. The NPZ reference is a binary reference asset, not used by the new task. The large supplied checksum manifest lists imagery paths; it does not supply the imagery. No supplied scientific asset is a runtime dependency here.

## Authoring and QC documentation

Read actual [CONTRIBUTING.md](https://github.com/harbor-framework/terminal-bench-science/blob/main/CONTRIBUTING.md), [proposal rubric](https://github.com/harbor-framework/terminal-bench-science/blob/main/rubrics/task-proposal.md), [implementation rubric](https://github.com/harbor-framework/terminal-bench-science/blob/main/rubrics/task-implementation.toml), and [QC automation guide](https://github.com/harbor-framework/terminal-bench-science/blob/main/TASK_REVIEW_AUTOMATION.md). Source checks inspected include check-task-fields.sh, check-task-timeout.sh, check-canary.sh, and check-instruction-suffix.sh. The implementation rubric contains 40 criteria.

Local packaging follows tasks/mathematical-sciences/applied-mathematics/<slug>. Both environment images pin dependencies, and the verifier is separate and offline. The upstream 8-hour agent timeout is preserved. Upstream publication/submission/social workflows do not apply to this local-only authorization. Upstream's 10-20% target is a documented difference from the user's governing 40-60% goal.

Reference complexity includes genuine domain reasoning, numerical conventions, costly dependencies, and multistage failure propagation. We retain structural coupling and independent verification while replacing scientific imaging/materials content with pure mathematics. Comparable model difficulty is a hypothesis requiring the actual eight trials.
