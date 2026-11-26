# Task 1: final pre-model audit, 26 November 2026

Reviewer: `/root/qc_a`. This is a new evidence-driven audit; previous reviews and all runtime files are preserved. No provider API, Docker run, package installation or threshold change was performed in this audit. All new task files, logs, artifacts, pytest temporary paths and configurable Python caches are under this directory on F:.

**Conclusion:** no new material numerical or checker defect was found in the assessed scope. Empty and discovery-only outputs cannot pass. The frozen task is ready for the coordinator's authorized initial model trajectories **with the difficulty and scientific limitations below**. This is not a claim that expert difficulty, real-world error control, or biological originality has been empirically established.

## Why the certificate list is empty

I recalculated the statistics from the immutable original count matrix and authoritative metadata, without importing the oracle or evaluator. The calculation uses pairwise-difference identities for sample variances, a general contrast calculation, `scipy.special.stdtr` for Student probabilities, and an independently constructed BY rank envelope. Only after completing the calculation did it read existing reference output for comparison. All numerical fields agree within the public tolerances; the largest observed discrepancies are about 2e−12 for probabilities and 1.2e−12 for degrees of freedom. These are independent computations of the **same prescribed model**, not independent evidence that its assumptions hold.

There are 57,665 source genes, 120 libraries, 40 groups of three, 20,803 eligible genes and **249,636 real hypotheses**. The three component probabilities are nonconstant:

| Probability | Minimum | 1st percentile | 5th percentile | Median | Count ≤ .05 |
|---|---:|---:|---:|---:|---:|
| Interaction | 4.83318e−12 | 3.61774e−6 | .000161201 | .144399 | 89,598 |
| Parental equivalence | 0, under the zero-SE convention | .0000330510 | .000573652 | .162031 | 89,578 |
| Minimum Dmr effect | 4.02250e−10 | .00000832005 | .000265181 | 1 | 52,932 |
| Joint maximum | 4.77198e−6 | .0101257 | .285710 | 1 | 6,018 |

Exactly 167,136 joint probabilities equal 1. All **249,636 adjusted q values equal 1**, and every real-data certificate is false. This does not mean the unadjusted evidence is all zero, that every observed effect is zero, or that no early sensitivity range is informative.

The nominal conjunction is restrictive before correction. With I=interaction, E=parental equivalence and D=minimum Dmr effect, these are the **exact** pass patterns at .05:

| Components passing | Rows |
|---|---:|
| None | 86,802 |
| I only | 26,342 |
| E only | 49,994 |
| D only | 23,242 |
| I and E, but not D | 33,566 |
| I and D, but not E | 23,672 |
| E and D, but not I | 0 |
| All three | 6,018 |

Thus, among rows where the other two nominal gates pass, minimum-effect evidence alone prevents 33,566 conjunctions and equivalence alone prevents 23,672. Interaction alone prevents none. Among the 6,018 nominal conjunctions, equivalence is the largest component probability for 3,407 and minimum effect for 2,611. Among the lowest 100 joint p values, equivalence limits 60 and minimum effect limits 40. These are statistical bottlenecks, not mechanistic attributions.

Across the entire family, the unique largest component is minimum effect for 179,902 rows, equivalence for 68,497, and interaction for 629; another 608 tie between interaction and minimum effect. This global count is heavily influenced by saturated minimum-effect p values. The raw observed margins and precision requirements should also be distinguished:

- 152,507 rows have an observed parental effect strictly inside ±.3; 62,929 of those nevertheless fail nominal equivalence. Another 97,129 are outside that observed margin.
- 82,500 rows have an observed absolute Dmr effect strictly above .5; 29,568 of those nevertheless fail nominal minimum-effect evidence. The remaining 167,136 do not exceed the observed effect margin.
- Only 20,205 rows satisfy both observed effect margins. The nominal conjunction has 5,491 Dim, 350 Ars and 177 Tg rows. Its condition-specific counts are retained in `condition_summary.tsv`.

The BY calculation explains complete saturation, rather than merely asserting that correction is conservative:

| Quantity | Independent value |
|---|---:|
| M | 249,636 |
| Harmonic factor H_M | 13.0049768037 |
| M × H_M | 3,246,510.38936 |
| Rank-1 BY cutoff at .05 | 1.5401152e−8 |
| Rank-M BY cutoff | .00384468198 |
| Smallest joint p | 4.7719776e−6 |
| Minimum uncapped M × H_M × p_(r) / r | **7.18160380** |
| Rank attaining that minimum | **196** |
| p at rank 196 | .000433571490 |
| BY cutoff at rank 196 | .00000301862579 |
| Minimum ratio to the BY significance cutoff | **143.632076** |

No rank crosses the BY step-up boundary. Even the smallest uncapped adjusted ratio is greater than 1, so clipping produces q=1 everywhere. As a diagnostic that isolates the harmonic penalty, the same family's minimum uncapped M×p/r is .552219655: ordinary BH on these same joint probabilities would also have no .05 discoveries. This diagnostic does **not** replace BY or propose changing the task. The lack of certificates is not caused only by the 13-fold harmonic factor, and it is not evidence that equivalence or biological absence has been established.

Complete independently derived rows and ranks are in `independent_statistics.tsv.gz` and `independent_rank_audit.tsv.gz`. The top rows and best-ratio row are also provided as small TSVs. Definitions, quantiles, exact gate/max patterns, source hashes, software versions and reference differences are in `independent_null_audit.json`.

## What the inference does and does not support

The contract treats three expression observations per group as independent for a working calculation. The metadata does not establish longitudinal pairing, three independent donors, or an available batch covariate. The publication calls some RNA-seq panels technical triplicates; the control-comparison heatmap caption says three replicates without settling every replication level. Culture-well replication, library technical replication and donor/population replication are not interchangeable. The dataset must not be described as 120 independent biological experiments or as establishing population-level variability. No pairing or batch was invented here.

With n=3, distributional assumptions are consequential. Nonzero-SE two-group degrees of freedom range from approximately 2 to 4, with medians about 3.12 for Dmr and 3.09 for parental effects; the interaction median is about 5.09. Normality and independence of transformed measurements were not empirically established by the prior review or this arithmetic audit. The narrow equivalence margin, minimum-effect margin, small samples and large conjunction family all matter. Some failures reflect observed effects outside the margins; others reflect inadequate precision. Calling all non-discoveries simply “no biology” or simply “low power” would both overstate the evidence.

There are 1,250 parental zero-SE rows, all assigned equivalence p=0 by the explicit deterministic convention; three enter the nominal conjunction and none yields a corrected certificate. Zero-inflated count-derived observations are not the same as a noiseless normal population. The convention ensures reproducible numerical behavior; it is not empirical proof of perfectly known parental abundance. The additional zero-SE/df counts are in `followup_descriptives.json`. BY arithmetic does not, by itself, verify real-world p-value calibration or realized FDR under technical correlation, small samples, normalization, selection and distributional misspecification.

Salmon estimated counts remain fractional. They are neither integer read observations to round silently nor literal transcript-copy measurements. No effective-length offsets or Salmon inferential uncertainty are supplied. The task therefore concerns transformed **relative count abundance**, with composition and transcript-usage limitations. TPM is a second processed representation of the same libraries, with a positive floor, not independent replication. RNA-seq patterns here do not establish ATF4 dependence, molecular ISR mediation or a causal construct effect. Missing UT2 is handled only through the explicit conditional anchor envelope, not an observed early point estimate or confidence interval.

## Incomplete outputs cannot exploit the negative result

I ran the unchanged `task/tests/test_outputs.py` with its task-owned pinned pytest runtime. The six adversarial submissions were generated in new directories, retaining correct companion artifacts where appropriate. Each run collected all eleven tests; none was a collection/preflight failure. The binary column applies the unchanged `test.sh` rule, success→1 and otherwise→0. These are host checker executions, **not new native Harbor trials**.

| Submission | Tests passing | Binary result |
|---|---:|---:|
| Complete correct positive control | 11/11 | 1 |
| No files | 0/11 | 0 |
| Six zero-byte files | 1/11 | 0 |
| Valid JSON but all TSVs header-only | 3/11 | 0 |
| Coherent 20-gene truncation | 4/11 | 0 |
| Only certified matched rows; other five artifacts correct | 7/11 | 0 |
| Only genes with a certificate in all real tables | 4/11 | 0 |

The matched-only certificate case is especially informative: it preserves the correct non-matched deliverables, but its empty matched table fails complete-family checks. The negative final labels do not permit omitting effects, uncertainty, component probabilities or the full eligible universe. Handoff/interpretation tests passing in some bad cases are easy controls, not a full success. The prior native no-op and saturated-shortcut evidence remains separate supporting history. All new per-test results, exact commands, logs and file sizes are in `adversarial_checker_audit.json`; the checker hash is unchanged before/after.

## Essential difficulty and prior review limits

The warning is substantive: five linked layers do not demonstrate “Extremely High” agent difficulty. The task prescribes the normalization, filter, contrasts, variance model, tests, multiplicity procedure, bounds, schemas and tolerances. A strong agent can largely translate a precise formula contract into a vectorized program. There is little open-ended method selection or biological hypothesis discovery. The final real-data certificate classification is trivial once saturation is known; the synthetic positive/null panel verifies branches but is a small, transparent numerical control, not difficult biological inference. The task still requires a correct complete numerical analysis, but neither the 16-hour expert estimate nor the 35–60% model success target has been measured.

The prior independent review was independent of the creator in reviewer identity and initial context. It inspected source, formulas, original metadata/SOFT, finite primary-text corpus and actual validation evidence; it did not initially execute a separate full original-count calculation or independently rerun every native trial. Some conclusions used the creator/coordinator's preserved execution evidence, which was checked against actual files. The oracle and private evaluator were written within the same authoring project, so separate implementations alone cannot exclude shared conceptual mistakes. Today's new calculation reduces numerical circularity but retains the prescribed model and standard SciPy mathematics. Neither review is an external blinded QC panel, an exhaustive literature review, a biological validation experiment or a provider/model calibration. Prior 37 PASS + 1 WARNING describes the local rubric inventory, not 38 automated external judges or a calibrated probability of correctness.

The scientific workflow remains coherent: verify representations and metadata → normalize full libraries and freeze eligibility → form contemporaneous line/treatment contrasts → carry independent-group uncertainty into affirmative equivalence and minimum-effect evidence → correct the complete joint family → retain every result → quantify missing-control sensitivity without inventing UT2. Likely model errors include rounding estimated counts, using TPM as independent/count evidence, selected-only library sums, symbol-key collisions, assumed replicate pairing, UT0 substituted for UT2, Dmr effect confused with interaction, pooled or incomplete variance, non-significance mistaken for equivalence, wrong minimum-effect tail, separate-list correction or per-condition BH, omitted negative genes, inadequate precision and early intervals widened by e instead of 2e. Trajectories should distinguish these scientific/numerical errors from schema or execution failures.

## Original-publication overlap, stated frankly

The original publication already asks about selective Dmr-PERK/ISR responses versus pleiotropic stressors and already uses parental dimerizer controls to support specificity (`labbe_bioc.txt:86–94`, DOI10.1038/s41467-024-52538-5). That biological motivation is shared. Task 1 is better described as a new **operational statistical audit of that existing experimental question**, not a newly discovered biological hypothesis or a wholly unrelated research objective.

Its different contribution is affirmative equivalence/minimum-effect conjunctions, contemporaneous line-by-treatment estimates, complete uncertainty certificates and explicit missing-control partial identification. The publication instead uses baseline-relative time-course regressions, module clustering and biological follow-up (`labbe_bioc.txt:498–514`). These are meaningful differences, but much of the task's statistical machinery is established methodology. The prior manual 25% rubric score is an ordinal weighted reviewer judgment under selected exclusions. It is **not** a calibrated semantic percentage, a plagiarism probability, proof of 75% originality, or a precise boundary between 29% and 31%. A reasonable reviewer could assign different ratings.

Within the inspected corpus I found no direct reuse of a distinctive published implementation or an equivalent benchmark answer. That finite finding supports benchmark-formulation distinctness, while leaving substantial biological-motivation overlap and unsearched work outside the claim. The previous raw 35–37% cross-task TF-IDF and roughly 99% generic AST-histogram warnings remain disclosed in history; low adjusted scores were never sufficient evidence of novelty. No cosmetic wording edit or requirement change was made to reduce a score or force discoveries.

## Pre-model disposition

No new blocking checker or numerical defect was found. Retain the frozen task and these limitations for the authorized initial model trajectories. Do not infer an agent success rate from oracle/negative-control trials, count technical controls as advanced scientific reasoning, or call the proposed difficulty target achieved before actual model results. This reviewer made **no model API request**. The coordinator controls the separately authorized model stage.
