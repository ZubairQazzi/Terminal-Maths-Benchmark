# Detailed review of initial trajectories and failed requirements

26 November 2026, Asia/Karachi. This is a new root-agent review of executed commands, terminal observations, original artifacts, instructions and unchanged native checks. It is not an external blinded human review. No hidden model reasoning is used as evidence about a model's intentions. Existing packages, historical trajectories and official rewards remain unchanged.

## Observed outcomes

| Task / run | Official binary reward | Checks passed | Verifier pass rate | Steps / tools | Wall / agent seconds | Input / output / cache tokens |
|---|---:|---:|---:|---|---|---|
| Task 1, bio1-initial-01 | 0 | 0/11 | 0% | 10 / 9 | 566.80 / 517.01 | 100,964 / 8,196 / 65,163 |
| Task 1, bio1-initial-02 | 0 | 10/11 | 90.91% | 22 / 23 | 965.04 / 919.09 | 549,119 / 24,132 / 464,968 |
| Task 2, bio2-initial-01 | 0 | 10/11 | 90.91% | 23 / 22 | 594.61 / 550.56 | 415,118 / 17,331 / 282,828 |

The first Task 1 run was interrupted by exhausted provider HTTP 503 retries. Its submission was unfinished. It is an infrastructure interruption, excluded from the scientific success-rate denominator. The completed diagnostic cohort is 0/1 contract successes for each task; this is insufficient to estimate extreme difficulty. Cache counts are subsets of input counts, not additional consumption. Historical provider-error counts were 11, 17 and 4 respectively; only the first run ended on a provider error.

All individual verifier outcomes are copied without reinterpretation to `historical_individual_verifier_results.csv`. Historical metrics are in `historical_metrics.{json,csv}`. Executed commands and terminal observations are extracted to separate per-run JSON files; source trajectories remain in the initial batch.

## Task 1: specificity-envelope v0.1.0

The completed run inspected metadata and calibration inputs, measured fractional counts and the positive TPM floor, computed full-library CPM eligibility, checked sample-column alignment and built explicit cell-line/treatment/time groups. Its final script calculated transformed relative-count effects and independent-group Welch uncertainties, equivalence/minimum-effect component probabilities, the complete joint BY family and early missing-control sensitivity envelopes. Tests 1–10 accepted all real-data artifacts and interpretation flags.

Relevant executed-command steps:

- Steps 3–4 inspected the authoritative design and calibration panel. Step 5 attempted a write to protected `/app`; steps 6–8 moved scratch work to a writable location.
- Steps 10–11 measured input properties and inspected synthetic groups. Recovered scratch errors included indexing `dict_items` and an undefined `se_d` name. One malformed XML response was recovered.
- Steps 12–13 developed the degenerate-case branch. The submitted code used `abs(d) >= 0.5` to assign probability zero when SE was zero.
- Steps 14–17 checked BY implementation, eligibility, sample alignment and group labels. Step 18 wrote the final complete calculation. Steps 19–23 waited for completion and inspected artifacts.

The failed `test_11_synthetic_positive_and_degenerate_controls` has a synthetic case with exactly `d=0.5` and `SE=0`. The result should be `p_dmr_minimum=1`, hence `p_joint=1`, and no certificate. The model instead reported zero and certified the boundary, also changing the eight-case BY ranks/q values. This is observable statistical null-boundary semantics implemented incorrectly, combined with failure to follow the explicit limiting convention. It is not a broad experimental-design or biology failure. There is no observed floating-point-precision cause: 0.5 is exactly representable, and the probability mismatch is 1.

The wording initially describes a minimum effect of 0.5, which can colloquially suggest “at least.” The subsequent explicit zero-SE paragraph resolves that: probability is zero strictly beyond the margin and one on or inside it. The checker matches that paragraph and the limit of the prescribed nonzero-SE formula at equality. Relaxing this requirement after the run would incorrectly accept a null-boundary certificate. Retain it unchanged. Synthetic cases are explicitly labeled and scientifically useful because the real family has saturated q values and no certificates; removing them would weaken verification of substantive branches.

The all-or-nothing reward appropriately measures full contract completion, but 0 must not be described as failure to understand all of RNA-seq or specificity inference. Difficulty claims should report the 10/11 result and the narrow failure. The small-n working model, technical-replicate limitations, selected universe, absent length offsets and non-confidence early bounds remain scientific limitations, independent of this model error.

## Task 2: transcript-provenance-audit v0.1.1

The run aligned versioned gene IDs, normalized complete atlas/query columns, checked that eligible values admitted logarithms without a pseudocount, removed gene/sample nuisance offsets, computed split correlations and used discovery-only linear assignment for a bijection. It searched one-source and exhaustive two-source supports, used bounded linear weighted projections, ordered the larger fraction first and evaluated validation residuals on disjoint genes.

Relevant executed-command steps:

- Steps 3–4 inspected provenance, gene splits and matrix dimensions; a protected-directory write was corrected by moving to `/tmp`.
- Steps 6–9 checked scaling and zeros. Step 10 implemented discovery-based assignment and held-out margins.
- A command for a missing scratch script was recovered. Four XML parser failures occurred across the run.
- Steps 15–16 constructed the final submission with exhaustive pair fitting. The long-running script was invoked twice, adding operational work without changing the scientific method. Later steps inspected artifacts and completed the task.

All identity, discovery/validation score, mixture, unsupported-rejection, residual and optimality checks passed. The only failure was `test_physical_audit`: code populated `atlas_minimum_by_column` using normalized `A[col].min()` instead of the supplied scaled atlas minimum. All 120 minima violate the declared raw-scale tolerance. For A000 the submitted value was approximately 0.0630178480934 while the supplied minimum is 0.05053822693. The errors reach approximately 0.118458, vastly exceeding 1e-7. They match normalized minima within 1.32e-13.

Primary category: representation/units instruction-following error, implemented in one audit field. It is not failure of donor inference, mixture optimization, validation or numerical precision. The instruction's final audit paragraph explicitly requires the supplied scaled minimum; thus the observed failure is justified. The generic field name can nevertheless invite confusion after the earlier normalization section. A new version should name the raw matrix explicitly in that paragraph, preserving the field/schema and scientific requirements.

One minor tolerance-boundary issue was found: the checker uses strict `< tolerance`, while ordinary reading of “absolute tolerance” is inclusive. This did not cause the observed failure. The proposed new version makes the four published numerical certificate comparisons inclusive and improves the failed raw-minimum assertion message. It does not change scientific acceptance margins, donor tolerances, null rules or official historical rewards. There is no scientific reason to require more precision than the published tolerances.

No seed replay, private-answer access or online retrieval was observed in the executed commands. Actual expression-based calculations were performed. This observation does not remove the separately demonstrated seed risk.

## Narrow offline counterfactuals

Copied submissions outside the frozen trees were corrected only as described below, then run against original offline verifier images with pinned runtimes:

| Diagnostic copy | Only correction | Result |
|---|---|---|
| Task 1 | Correct the zero-SE minimum-effect boundary and derived synthetic joint/BY values | 11/11, diagnostic reward 1 |
| Task 2 | Measure supplied-scale atlas minima in the audit JSON | 11/11, diagnostic reward 1 |

These are researcher-created diagnostic copies, not additional model trials and not official rescoring. Original rewards stay 0. Commands, individual checks and logs are in `counterfactual_results.json` and `counterfactual_task*/`. They support the narrow failure diagnoses; they do not prove that a model would independently repair itself.

## Recommendations before the new cohort

- **Task 1: retain** as a well-defined statistical implementation and conditional-inference audit. Preserve v0.1.0 for the five-trial cohort. Keep the valid boundary control; qualify the expert-time/extreme-difficulty claims and report scientific versus bookkeeping failures separately.
- **Task 2: improve before formal retention.** Remove predictable generation, isolate the private replay record, clarify the raw-scale field and honor inclusive numerical tolerances in a separate v0.2.0. Run scientific and isolation QC before its five trials. Preserve v0.1.1 as historical evidence; do not pool it with v0.2.0 outcomes.
- Neither task is rejected on current scientific evidence. Neither is established as extremely difficult. A rigid binary reward alone is insufficient evidence when the main calculations pass.

Passing prescribed formulas and Boolean interpretation flags also does not independently demonstrate open-ended biological reasoning. These tasks substantially assess faithful quantitative implementation under stated biological/design limits. Future recommendations must distinguish that construct from unconstrained discovery or mechanistic interpretation.
