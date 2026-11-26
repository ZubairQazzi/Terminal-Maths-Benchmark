# Independent QC: Task 2

Reviewer: `/root/qc_b`, distinct from creator `/root/creator_b`; fresh task context. Local independent review, not an external QC pipeline or model calibration. Review started 2026-11-25.

## Initial findings recorded before creator explanations

Directly read the project brief and QC checklist, agent instruction, manifest, Dockerfiles, reference implementation, evaluator, preparation implementation and shared data/metadata audit. Creator proposal, README explanations, creator QC, handoff and remediation were not consulted for this initial assessment.

1. No confirmed scientific defect in the visible reconstruction contract. Counts remain fractional; TPM is normalized compositionally; centering removes nuisance offsets without claiming effective-length recovery; mixtures use the linear TPM scale. Unknown fractions refer to representations, not cells. The missing untreated 2-hour condition and limits on ATF4 claims are explicit (`task/instruction.md:7,13-28,32-44,72-82`).
2. Independent derivation and verification still required: source-to-anonymous mapping, planted fractions, separation from competing supports, held-out residuals, and frozen eligibility. A high oracle score alone cannot establish these. Marked **NOT TESTED at initial review**, to be resolved below.
3. Version-specific runtime evidence gap: manifest is 0.1.1 and `tests/test_outputs.py` now defines eleven uniquely named tests. Supplied native evidence at review start refers to 0.1.0, whose CTRF collapsed parametrized names. Final 0.1.1 native CTRF, oracle/reset, artifact and isolation evidence remains **NOT TESTED** until read. This is not a scientific failure and old runs will not be relabeled as current.
4. Interpretation limits, not defects: the validation genes are disjoint features in the same libraries, not independent biological replication. Eligibility uses all source columns but no anonymous labels or query outcomes; the source-publication floor is not an identified biological low-expression signal. The five Boolean interpretation flags are easy contract checks and cannot be counted as advanced biological discrimination.
5. Security inspection: verifier parses bounded TSV/JSON only and does not execute submitted code; private fixtures are absent from the solver Dockerfile. Native isolation and artifact checks remain pending. Solver network is declared `public` in the active package; the task itself needs no network and verifier is `no-network`.

## Independent numerical recheck

The reviewer ran an independent inline Python calculation from the original compressed matrices and official SOFT records. It imported neither `solution/solve.py` nor `tests/checks.py`. Source-to-atlas identities were derived by directly matching each normalized anonymous column to the original named TPM composition **before** comparing private labels. Correlations used `numpy.corrcoef`; mixture coefficients were cross-checked with bounded scalar minimization. Detailed per-query measurements are retained in `independent_qc_findings.json`.

- Original counts are 57,665 ×120, with 2,188,385 fractional entries; runtime count gzip is byte-identical to the original. Original TPM floor is 0.063122. Anonymous normalized compositions match their original source to maximum relative entry error5.09e-10.
- All120 direct source-derived mappings match the private fixture. Every official GSM title matches the reconciled metadata; untreated2h sample count is zero.
- Frozen count/TPM eligibility and SHA-256 gene-ID split exactly match the source calculation:5,670 discovery and5,659 validation genes. Neither query outcomes nor anonymous labels enter eligibility. Filtering all source columns is explicitly part of the frozen representation contract, not an unbiased independent biological selection procedure.
- Discovery and validation each independently recover120/120 exact identities. Minimum validation correlation0.949414690856 and margin0.006820138255 exceed required0.90/0.001. These are final hash-split measurements; the earlier pilot used a different alternating split and is not relabeled as the final certificate.
- All24 categories and accepted donor supports match direct-source reconstruction. Maximum accepted coefficient error is0.000180905141, below0.02. Held-out residual ranges: pure0.000912173–0.001093618; pair0.000897546–0.001093195; unsupported0.032267847–0.119296490. The six unsupported cases are separated from0.01, and accepted cases from0.005/0.01. Accepted pair alternatives have second-support discovery residuals around0.02–0.04, well above the accepted fits near0.001.
- All six verifier data files were independently SHA-256 compared with their solver counterparts; every pair is identical. The evaluator computes its own arithmetic and source-traceable labels, not cached oracle outputs.

## Scientific and evaluator conclusions

The transformed identity score is a defensible empirical fingerprint for these paired measurements; it is not an estimator of literal effective lengths. Actual source-derived separation demonstrates identifiability of this fixed fixture. Linear normalized TPM mixtures and coefficients are correct for the explicitly synthetic representation-level construction. No count likelihood, integer approximation, differential-expression result, MTC or natural-contamination conclusion is asserted. The design does not infer a new biological treatment effect.

Discovery alone determines the assignment and pair coefficient. The disjoint validation features check numerical model adequacy without being advertised as a new experiment. Coexpression, common libraries and full-column compositional normalization mean the split is not statistically independent biological replication or evidence of out-of-study generalization. The task makes no inferential probability claim requiring that independence.

The grader is a conjunction of checks: fabricated zero residuals can pass support optimality alone, but residual recomputation rejects them. The per-family negative evidence therefore matters. No-op0/11; constant3/11; fixed gene-list0/11; shifted alignment8/11; wrong donors8/11; half fractions9/11; incomplete5/11; forced unsupported pairs9/11; wrong cell-fraction claim10/11. Every negative has binary reward0. Schema, physical audit, claim flags and pure aliquots are intentionally easy controls. Changed-order/relabelled/split-swapped data pass11/11 with the data-driven solver; replayed original artifacts pass only the easy claims check. This is meaningful resistance to frozen answers, not a proof that hardcoding every answer of a public finite instance is impossible.

The verifier reads bounded regular TSV/JSON, rejects symlinks, executes no submitted program, recomputes scientific certificates from its own immutable copies and does not import the solution. Continuous coefficient/support tolerances make method-equivalent output acceptable; alternate local assignment/scalar enumeration passes11/11. The reviewer's separate scalar optimizer also reproduces a valid reconstruction.

## Originality investigation

Independent source comparison is recorded in `authoring/originality/conceptual_review.{json,md}`. Sixteen comparisons include actual Labbé and GDF15 fulltext, RNA-seq methods/workflows, SEQC, nearest frozen TBScience instructions and scientific code, existing RNA identity methods, Task1 and supplied math examples. The maximum six-dimension weighted substantive score is25%, below the requested30% threshold. This is a bounded manual judgment, not an embedding measurement or absolute originality claim.

The raw pinned TF-IDF **37.233581% Task2→Task1** and **35.690629% Task1→Task2** are retained as investigation signals; the initial34.113431% is also preserved by the coordinator. The final reference-corpus correction changed no task wording. Direct section inspection finds shared GEO facts, representation/interpretation safeguards, audit vocabulary and Harbor boilerplate. Task1's Welch/TOST/joint-null BY/missing-control inference and Task2's fingerprint assignment/convex aliquot/open-set reconstruction have different scientific objectives, methods, units of analysis and graded quantities. The generic Python AST histogram~99% is retained but cannot distinguish these algorithms. Low code shingle overlap alone also proves nothing. No cosmetic wording changes were made.

## Final package status — 26 November 2026, Asia/Karachi

The five previously pending native items are independently closed. All38 rubric IDs are individually assessed in `rubric_qc.{json,md}`: **38 PASS, zero pending, zero FAIL** for locally assessable implementation/science requirements. No confirmed mandatory local defect remains. The scientific `essential_difficulty` check remains PASS because the five layers require connected representation, provenance and model-adequacy reasoning. This does not establish an extreme model difficulty or a particular agent success rate.

The reviewer directly parsed each final trial's actual `result.json`, `lock.json`, `verifier/reward.txt`, `verifier/ctrf.json`, and `artifacts/manifest.json`, then independently hashed the artifact files and byte-compared the two oracle outputs. `native_summary.json` was not the sole evidence. All12 valid final trials use version0.1.1, task checksum `ba9ef45871ac057453dcdd1d4529f1eb2969a111763094d168c79c4a50c919ff` and lock digest `sha256:09b2629bb64d3bee4b962428d189900df9229c8b8573b008de93bc39b182908a`. No exception or infrastructure error was counted as a scientific failure.

| Final native case | Passed families | Binary reward |
|---|---:|---:|
| Oracle, two separate trials | 11/11 each | 1 each |
| Alternative valid method | 11/11 | 1 |
| No-op | 0/11 | 0 |
| Constant output | 3/11 | 0 |
| Fixed gene-list output | 0/11 | 0 |
| Shifted alignment | 8/11 | 0 |
| Wrong donor/contrast | 8/11 | 0 |
| Half-fraction statistical mutation | 9/11 | 0 |
| Incomplete output | 5/11 | 0 |
| Forced unsupported pairs | 9/11 | 0 |
| Invalid cell-fraction claim | 10/11 | 0 |

Every final CTRF contains **eleven distinct test names**, including actual failures for negative controls. The prior aggregation defect is closed from observed native output, not from the renamed functions alone. Both oracle artifacts are byte-identical: `alignment.tsv` SHA-256 `4d5309d035b4f9e134160b66c219cac1065773ab376220ea8bb94f124b48fa75`; `audit.json` `5579060138e461fe00bde0815436c96ef212371ca800bc32cd21be580d3888e4`; `queries.tsv` `ce4929a0b8a12d46067ffa4c8ce0530821532f4ff1fc99c7e32359bbf1424ce0`. Each manifest reports successful submission-directory collection. A fresh no-op has no submitted files and fails all11 tests, showing that prior outputs were not reused. The three oracle files total14,679bytes.

Final clean `--no-cache` agent and verifier image builds exit0 (50.000s and50.407s). `isolation_v011.json` records three actual passing probes: UID1000 solver, read-only inputs, writable output and absent private trees; private verifier directories with no egress and no preexisting score; complete offline oracle. The offline probe used an8GiB ceiling, while successful native Harbor trials use the manifest's4GiB limit; these are separate resource observations. Source/canonical integrity records192 matching checks with original downloads unchanged. Final shell checks in the task's own verifier image pass26/26, Harbor lintALL returns`[]`, and entry/config/similarity checks complete **29/29 static PASS**. The37.23% raw similarity passes the upstream80% static threshold separately from the completed30% substantive investigation.

Evidence correction: provisional reviewer text incorrectly described `local_pytest_v011.log` as a successful host pytest run. Direct rereading shows `No module named pytest`. The local checker11/11 evidence and actual final native pytest/CTRF11/11 evidence are distinct measured successes. No host pytest success is claimed. This correction affects the reviewer wording, not the scientific implementation.

Final independent verdict: **PASS for available local non-model validation**. Historical0.1.0 successes remain excluded from final native counts. No external automated/model QC, Gemini evaluation, provider approval, or calibrated agent success is claimed. Intended expert/extreme difficulty, the35–60% target and empirical model success rate remain **NOT MEASURED**.
