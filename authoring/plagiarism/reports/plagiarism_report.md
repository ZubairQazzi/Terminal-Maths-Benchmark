# Scoped originality audit

This is a real comparison against browser-returned source windows. It is not a full-corpus clearance.

Reference documents compared: 12.
Maximum weighted similarity: 3.82%.
Heuristic originality: 96.18%.

Weights: 60% word five-gram Jaccard, 25% normalized-line Jaccard, 15% code-structure three-gram Jaccard. Exact normalized equality scores 100% similarity. Comments/canaries are removed from word and line comparisons. Review warning: similarity above 30%; target heuristic originality at least 70%.

Only reports, hashes, and coverage counts are saved. Raw reference source is never written to disk.

| Reference | Captured/total lines | Max similarity |
|---|---|---|
| [amr-poisson-instruction](https://raw.githubusercontent.com/harbor-framework/terminal-bench-science/main/tasks/mathematical-sciences/applied-mathematics/amr-poisson-optimize/instruction.md) | 25/25 | 2.02% |
| [cilia-instruction](https://raw.githubusercontent.com/harbor-framework/terminal-bench-science/main/tasks/life-sciences/biology/cilia-segmentation/instruction.md) | 59/59 | 2.11% |
| [cilia-oracle](https://raw.githubusercontent.com/harbor-framework/terminal-bench-science/main/tasks/life-sciences/biology/cilia-segmentation/solution/run_analysis.py) | 245/245 | 3.47% |
| [cilia-tests](https://raw.githubusercontent.com/harbor-framework/terminal-bench-science/main/tasks/life-sciences/biology/cilia-segmentation/tests/test_outputs.py) | 484/484 | 2.80% |
| [mendota-instruction](https://raw.githubusercontent.com/harbor-framework/terminal-bench-science/main/tasks/earth-sciences/geosciences/mendota-ice-phenology/instruction.md) | 35/35 | 1.84% |
| [mendota-oracle](https://raw.githubusercontent.com/harbor-framework/terminal-bench-science/main/tasks/earth-sciences/geosciences/mendota-ice-phenology/solution/ice_phenology_pipeline.py) | 499/499 | 3.27% |
| [mendota-tests](https://raw.githubusercontent.com/harbor-framework/terminal-bench-science/main/tasks/earth-sciences/geosciences/mendota-ice-phenology/tests/test_outputs.py) | 106/106 | 3.82% |
| [pencil-toolkit-readme](https://raw.githubusercontent.com/Tewf/tensor-rank-toolkit/main/README.md) | 168/168 | 0.00% |
| [silicon-instruction](https://raw.githubusercontent.com/harbor-framework/terminal-bench-science/main/tasks/physical-sciences/materials-science/si-fracture-fbc/instruction.md) | 22/22 | 3.42% |
| [silicon-oracle](https://raw.githubusercontent.com/harbor-framework/terminal-bench-science/main/tasks/physical-sciences/materials-science/si-fracture-fbc/solution/oracle/oracle_emit_prod.py) | 294/338 | 3.07% |
| [silicon-tests](https://raw.githubusercontent.com/harbor-framework/terminal-bench-science/main/tasks/physical-sciences/materials-science/si-fracture-fbc/tests/test_outputs.py) | 402/519 | 3.09% |
| [sympy-normalforms](https://raw.githubusercontent.com/sympy/sympy/sympy-1.14.0/sympy/matrices/normalforms.py) | 145/145 | 2.34% |

Manual conceptual assessment: the three references solve distinct scientific problems. No imagery/materials algorithm, dataset, expected value, or distinctive solution logic is reused. Shared Harbor protocol and general Python constructs are acknowledged scaffolding. The mathematical theory itself is standard and credited; global task novelty and independent domain assessment remain uncertain.

Code review: the oracle uses polynomial Smith forms and convolution kernels; the evaluator uses canonical construction plus rational certificates. The reference workflows instead use geospatial inference, microscopy geometry, and atomistic/continuum computation. The structure score is a shallow syntax comparison; no embedding model or automated semantic originality score was used.

Limitations: incomplete browser windows, mutable URLs/revision drift, and no complete public-task corpus. Do not present the scoped percentage as proof of originality.

Related public implementation: [tensor-rank-toolkit](https://github.com/Tewf/tensor-rank-toolkit) shares the classical structural-analysis objective. Its README was included in the comparison, but the code was not copied. Conceptual overlap remains an explicit WARNING; lexical scores do not establish global novelty.
