# Terminal Maths Benchmark

- [Task 1 archive](./task%201.zip)
- [Download bio.zip](https://github.com/ZubairQazzi/Terminal-Maths-Benchmark/releases/download/biology-2026-11-26/bio.zip) (1.91 GB)

The biology archive is provided unchanged as a release download.

SHA-256: 822651cf160f91da2cfd64848c31b57e5514e1c7b9f94b010b428fc6587c873f


## Mathematics Task 2 and Task 3 — v0.2.0

Two separate, complete Harbor task packages are available. Download either ZIP, extract it, and change into the extracted task folder. Neither requires the other task.

| Task | Download | Source and run instructions |
|---|---|---|
| Task 2: Certified Parametric Quadratic Optimizer Atlas | [task-2-v0.2.0.zip](https://github.com/ZubairQazzi/Terminal-Maths-Benchmark/raw/refs/heads/main/task-2-v0.2.0.zip) | [Task 2](./task-2/) · [Run with your own key](./task-2/RUNNING.md) |
| Task 3: Certified Joint p-adic Valuation Census | [task-3-v0.2.0.zip](https://github.com/ZubairQazzi/Terminal-Maths-Benchmark/raw/refs/heads/main/task-3-v0.2.0.zip) | [Task 3](./task-3/) · [Run with your own key](./task-3/RUNNING.md) |

Use Linux or WSL2, Docker with Linux containers, and Harbor 0.27.0. Each package includes the Docker environments, pinned offline Python dependency wheels, instructions, public data, reference solution, full evaluator and mathematical inputs. Follow its RUNNING.md to choose a supported Harbor agent/model and supply your own provider API key locally. Do not commit credentials.

The packages preserve all 30 validated runtime files per task without changing mathematics, oracle or grading logic. Task 2 has 42 graded inputs; Task 3 has 44. Prior local non-model validation and independent QC passed; the public ZIPs also undergo extraction/hash checks and native reference-oracle grading. No model API trial is performed during publication, and frontier-model success rates remain unmeasured.

Reference/evaluator sources are included for reproducibility and run behind Harbor's task-defined isolation. Local environments, machine-specific authoring records and historical trajectories are preserved locally and excluded from these portable downloads. Required third-party license texts are included. Tasks 2 and 3 are MIT-licensed; their dependency licenses are retained separately. This grant does not change Task 1 or other existing repository material. This update does not change Task 1 or the earlier downloads.

Verify downloaded archives against [SHA256SUMS.txt](./SHA256SUMS.txt). Package versions, sizes and hashes are also recorded in [PUBLICATION_MANIFEST.json](./PUBLICATION_MANIFEST.json).
