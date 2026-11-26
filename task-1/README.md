# Task 1 — Certified Kronecker Structure of Singular Matrix Pencils v0.2.0

This bundle contains the complete validated 22-file Harbor task and 38 current mathematical, validation and QC reports. The benchmark files are preserved byte-for-byte from the reviewed v0.2.0 package.

| Component | Location |
|---|---|
| Complete Harbor task | [certified-pencil-structure](tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure/) |
| Task instructions | [instruction.md](tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure/instruction.md) |
| Reference solution and hidden evaluator | Included in the complete task, under solution/ and tests/ |
| Full non-model report | [FINAL_REPORT.md](authoring/reports/FINAL_REPORT.md) |
| All 29 static criteria | [static_qc_audit.md](authoring/reports/static_qc_audit.md) |
| All 38 rubric criteria | [rubric_qc_audit.md](authoring/reports/rubric_qc_audit.md) |
| Independent local AI review | [independent_qc_review.md](authoring/reports/independent/independent_qc_review.md) |
| Running and verifying | [REPRODUCING.md](REPRODUCING.md), [SHA256SUMS](SHA256SUMS) |

The task has 13 connected mathematical obligations, five complexity layers, 48 graded pencils (42 structural cases and six convention controls), and 144 forcing queries. Two fresh final-version oracle runs passed all 48 pencils; all eight final-version native Harbor validation runs produced their expected outcomes. Local static QC passed 29/29; local rubric QC records 37 PASS plus one justified N/A. One separate fresh-context AI reviewer passed all 67 criteria with five explicit limitations.

Frontier-agent difficulty is unmeasured: zero valid model calibration trials. External QC and independent human domain review have not been established. Finite originality coverage, worst-case reference-search runtime and batch-level native reporting remain documented limitations.

## Publication record

The user authorized publication to https://github.com/ZubairQazzi/Terminal-Maths-Benchmark after non-model validation. The included reports preserve the earlier validation record; statements that no publication had occurred or was authorized describe that earlier phase. The present request authorizes this publication, while model-provider testing remains a separate approval gate. The validated scientific files and their author metadata have not been rewritten.

Raw local Harbor job directories, model trajectories, caches, credentials, frozen originals and host inventories are retained locally and are outside this publication bundle. Some reports cite those local raw files. The included records preserve their reported results and limitations; their presence is not an external QC approval.

Native Harbor task checksum: `0d9c54dfd0cb753e9dca38b78c1d9c8d89e649d4c5eea863e576898f75b7394d`.
Author-framed source SHA-256: `c3f0390f31b44bce786267f5a6641bd41a33fd88a31356d0ad8bdc670cb4650d`.
