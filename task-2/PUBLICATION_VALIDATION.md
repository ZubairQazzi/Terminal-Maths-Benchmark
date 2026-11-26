# Publication validation: Task 2 v0.2.0

The 30 runtime files are byte-identical to the completed local version0.2.0. Mathematics, oracle, generated inputs and grading logic are unchanged. This archive contains the complete Harbor task: manifest, solver instructions, Docker build contexts, pinned offline dependency wheels, public data/specification, reference solution and private evaluator inputs/checks. The other task is not required.

| Local non-model check | Result |
|---|---|
| Graded cases | 42 |
| Conservatively substantive cases | 34 |
| Mathematical stages / layers | 13 / 5 |
| Static QC | 29/29 PASS |
| Rubric QC | 37 PASS; 1 justified N/A |
| Independent review | All67criteria reviewed; no open findings |
| General oracle and accepted alternatives | PASS |
| Incorrect controls | Denied full credit |
| Docker / Harbor | Clean builds and native grading PASS |
| External model-panel QC | NOT RUN |
| Frontier-model success rate | NOT MEASURED |

The bundled mathematical cases were generated for this benchmark. Local seeds, machine-specific orchestration, authoring research snapshots, historical trajectories, cached environments and workstation metadata are preserved locally and excluded from this public runtime package. No excluded item is needed to build, solve or grade the task.

Follow RUNNING.md to evaluate using your own supported Harbor agent/model and your own API key. Publication verification uses only the reference oracle and never calls an LLM provider. Public reference/evaluator sources are included for reproducibility; use Harbor's isolated agent environment when measuring model performance.
