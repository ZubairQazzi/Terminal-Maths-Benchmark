"""Independent reviewer calculation. No oracle/evaluator imports; writes only here.

Moments use pairwise-difference variance, Student probabilities use special.stdtr,
and correction uses an independently constructed rank envelope. Existing reference
output is read only after the independent result is complete, for comparison.
"""
import hashlib
import itertools
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.special import stdtr

OUT = Path(__file__).resolve().parent
BIO = OUT.parents[3]
TASK = BIO / "biology-task-1/task"
COUNTS = BIO / "shared-inputs/original-read-only-data/GSE273600_Control_Conditions_Raw_Counts.txt.gz"
TPM = BIO / "shared-inputs/original-read-only-data/GSE273600_Control_Conditions_TPMs.txt.gz"
METADATA = BIO / "authoring/sample_metadata.csv"
COMPONENTS = ["p_interaction", "p_parent_equivalence", "p_dmr_minimum"]
QUANTILES = [0, .001, .01, .05, .1, .25, .5, .75, .9, .95, .99, 1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def moments(values):
    n = values.shape[1]
    mean = np.sum(values, axis=1) / n
    pair_ss = sum(np.square(values[:, j] - values[:, k])
                  for j, k in itertools.combinations(range(n), 2))
    # sum_pair(xj-xk)^2 = n*sum(x-mean)^2
    sample_variance = pair_ss / (n * (n - 1))
    return mean, sample_variance / n, n


def contrast(moment_list, coefficients):
    effects = np.stack([m[0] for m in moment_list])
    vm = np.stack([m[1] for m in moment_list])
    n = np.array([m[2] for m in moment_list])[:, None]
    c = np.array(coefficients)[:, None]
    effect = np.sum(c * effects, axis=0)
    variance = np.sum(c * c * vm, axis=0)
    denominator = np.sum(c ** 4 * vm ** 2 / (n - 1), axis=0)
    df = np.full_like(variance, 1e12)
    np.divide(variance ** 2, denominator, out=df, where=denominator != 0)
    return effect, np.sqrt(variance), df


def probabilities(d, sd, fd, a, sa, fa, interaction, si, fi):
    with np.errstate(divide="ignore", invalid="ignore"):
        p_i = np.minimum(1., 2 * stdtr(fi, -np.abs(interaction) / si))
        p_a = np.maximum(stdtr(fa, -(a + .3) / sa), stdtr(fa, (a - .3) / sa))
        p_d = np.minimum(1., 2 * stdtr(fd, -((np.abs(d) - .5) / sd)))
    p_i = np.where(si == 0, np.where(interaction == 0, 1., 0.), p_i)
    p_a = np.where(sa == 0, np.where(np.abs(a) < .3, 0., 1.), p_a)
    p_d = np.where(sd == 0, np.where(np.abs(d) > .5, 0., 1.), p_d)
    return p_i, p_a, p_d


def describe(x):
    x = np.asarray(x)
    return {
        "quantiles": {str(q): float(np.quantile(x, q)) for q in QUANTILES},
        "counts_le": {str(t): int(np.sum(x <= t)) for t in [1e-6, 1e-5, 1e-4, .001, .01, .05, .1, .5]},
        "exact_zero": int(np.sum(x == 0)), "exact_one": int(np.sum(x == 1)),
        "below_one": int(np.sum(x < 1)),
    }


def masks_table(p_values, threshold=.05):
    mask = (p_values <= threshold).astype(np.int64) @ np.array([1, 2, 4])
    return [{"pass_pattern": " & ".join(COMPONENTS[j] for j in range(3) if k & (1 << j)) or "none",
             "mask": k, "count": int(np.sum(mask == k))} for k in range(8)]


def main():
    counts = pd.read_csv(COUNTS, sep="\t", index_col=0)
    meta = pd.read_csv(METADATA)
    assert len(meta) == 120 and meta.sample_id.nunique() == 120
    assert set(meta.sample_id) == set(counts.columns)
    values = counts.to_numpy(dtype=np.float64)
    libraries = np.sum(values, axis=0)
    cpm = values / libraries[None, :] * 1_000_000
    eligible = np.sum(cpm >= 1, axis=1) >= 6
    genes = counts.index.to_numpy()[eligible]
    y = np.log1p(cpm[eligible]) / math.log(2)
    lookup = {name: j for j, name in enumerate(counts.columns)}
    group_moments = {}
    for key, records in meta.groupby(["cell_line", "treatment", "time_h"], sort=True):
        indices = [lookup[name] for name in records.sample_id]
        assert len(indices) == 3
        group_moments[key] = moments(y[:, indices])
    assert len(group_moments) == 40 and ("DmrPERK", "UT", 2) not in group_moments

    frames = []
    for treatment, time_h in itertools.product(["Dim", "Ars", "Tg"], [4, 8, 16, 24]):
        g = [group_moments[key] for key in [
            ("DmrPERK", treatment, time_h), ("DmrPERK", "UT", time_h),
            ("Parental", treatment, time_h), ("Parental", "UT", time_h)]]
        d, sd, fd = contrast(g[:2], [1, -1])
        a, sa, fa = contrast(g[2:], [1, -1])
        interaction, si, fi = contrast(g, [1, -1, -1, 1])
        pi, pa, pdm = probabilities(d, sd, fd, a, sa, fa, interaction, si, fi)
        frames.append(pd.DataFrame({
            "gene_id": genes, "treatment": treatment, "time_h": time_h,
            "dmr_effect": d, "parent_effect": a, "interaction": interaction,
            "se_dmr": sd, "df_dmr": fd, "se_parent": sa, "df_parent": fa,
            "se_interaction": si, "df_interaction": fi,
            COMPONENTS[0]: pi, COMPONENTS[1]: pa, COMPONENTS[2]: pdm,
        }))
    frame = pd.concat(frames, ignore_index=True)
    p = frame[COMPONENTS].to_numpy()
    joint = np.max(p, axis=1)
    assert np.isfinite(p).all() and ((p >= 0) & (p <= 1)).all()
    frame["p_joint"] = joint
    order = np.argsort(joint, kind="stable")
    ranked = joint[order]
    m = len(joint)
    ranks = np.arange(1, m + 1, dtype=float)
    harmonic = math.fsum(1. / int(r) for r in ranks)
    base_ratio = m * ranked / ranks
    raw_ratio = harmonic * base_ratio
    suffix = np.minimum.accumulate(raw_ratio[::-1])[::-1]
    q = np.empty(m)
    q[order] = np.minimum(1., suffix)
    frame["q_joint"] = q
    frame["certified"] = q <= .05
    best_position = int(np.argmin(raw_ratio))
    rank_threshold = .05 * ranks / (m * harmonic)

    exact_max = p == joint[:, None]
    max_mask = exact_max.astype(np.int64) @ np.array([1, 2, 4])
    nominal = p <= .05
    all_pass = nominal.all(axis=1)
    only_preventer = {
        COMPONENTS[j]: int(np.sum((~nominal[:, j]) & nominal[:, [k for k in range(3) if k != j]].all(axis=1)))
        for j in range(3)
    }
    by_condition = []
    for (treatment, time_h), rows in frame.groupby(["treatment", "time_h"], sort=True):
        cp = rows[COMPONENTS].to_numpy()
        cj = rows.p_joint.to_numpy()
        by_condition.append({"treatment": treatment, "time_h": int(time_h), "hypotheses": len(rows),
            **{name + "_le_0.05": int(np.sum(rows[name] <= .05)) for name in COMPONENTS},
            "joint_le_0.05": int(np.sum(cj <= .05)), "minimum_joint_p": float(cj.min()),
            "exact_max_counts_including_ties": {name: int(np.sum(cp[:, j] == cj)) for j, name in enumerate(COMPONENTS)}})
    label = lambda mask: " | ".join(COMPONENTS[j] for j in range(3) if mask & (1 << j))
    rank_samples = sorted(set([1, 10, 100, 1000, 10_000, m, best_position + 1]))
    audit = {
        "method": "Independent computation from immutable original counts and shared authoritative metadata. Pairwise-difference group variance; general contrast moments; scipy.special.stdtr; independent BY rank envelope. No solution/evaluator imports.",
        "inputs_sha256": {str(path): sha(path) for path in [COUNTS, TPM, METADATA, Path(__file__)]},
        "runtime": {"python": sys.version, "platform": platform.platform(), "numpy": np.__version__, "pandas": pd.__version__, "scipy": scipy.__version__},
        "gene_count": len(counts), "sample_count": len(meta), "groups": len(group_moments),
        "group_size": 3, "eligible_gene_count": len(genes), "M": m,
        "probabilities": {name: describe(frame[name]) for name in COMPONENTS + ["p_joint", "q_joint"]},
        "nominal_gate_patterns_at_0.05": masks_table(p),
        "all_three_nominal_pass": int(all_pass.sum()),
        "unique_genes_with_nominal_conjunction": int(frame.loc[all_pass, "gene_id"].nunique()),
        "only_component_preventing_nominal_conjunction": only_preventer,
        "exact_joint_max_patterns": [{"components": label(k), "count": int(np.sum(max_mask == k))} for k in range(1, 8)],
        "exact_max_counts_including_ties": {name: int(exact_max[:, j].sum()) for j, name in enumerate(COMPONENTS)},
        "observed_effect_and_precision_gates": {
            "parent_abs_effect_strictly_below_0.3": int((np.abs(frame.parent_effect) < .3).sum()),
            "parent_inside_margin_but_equivalence_p_above_0.05": int(((np.abs(frame.parent_effect) < .3) & (frame.p_parent_equivalence > .05)).sum()),
            "dmr_abs_effect_strictly_above_0.5": int((np.abs(frame.dmr_effect) > .5).sum()),
            "dmr_beyond_margin_but_minimum_p_above_0.05": int(((np.abs(frame.dmr_effect) > .5) & (frame.p_dmr_minimum > .05)).sum()),
            "both_observed_margins": int(((np.abs(frame.parent_effect) < .3) & (np.abs(frame.dmr_effect) > .5)).sum()),
        },
        "multiplicity": {
            "H_M": harmonic, "M_times_H_M": m * harmonic, "alpha": .05,
            "rank1_cutoff": float(rank_threshold[0]), "rankM_cutoff": float(rank_threshold[-1]),
            "any_rank_crosses_BY_stepup_line": bool(np.any(ranked <= rank_threshold)),
            "uncapped_minimum_M_H_p_over_rank": float(raw_ratio.min()),
            "minimum_ratio_over_BY_significance_cutoff": float((raw_ratio / .05).min()),
            "best_rank_for_uncapped_ratio": best_position + 1,
            "p_at_best_ratio_rank": float(ranked[best_position]),
            "BY_threshold_at_best_ratio_rank": float(rank_threshold[best_position]),
            "minimum_clipped_q": float(q.min()), "maximum_clipped_q": float(q.max()),
            "certificates": int(frame.certified.sum()),
            "diagnostic_only_BH_same_family": {"note": "No grading requirement or threshold is changed. This isolates the harmonic penalty diagnostically.", "minimum_uncapped_M_p_over_rank": float(base_ratio.min()), "number_q_le_0.05": int(np.sum(np.minimum(1., np.minimum.accumulate(base_ratio[::-1])[::-1]) <= .05))},
            "sampled_ranks": [{"rank": r, "p_sorted": float(ranked[r-1]), "BY_threshold": float(rank_threshold[r-1]), "M_H_p_over_rank": float(raw_ratio[r-1])} for r in rank_samples],
        },
        "condition_summaries": by_condition,
    }
    frame.to_csv(OUT / "independent_statistics.tsv.gz", sep="\t", index=False, float_format="%.16g", compression={"method": "gzip", "mtime": 0})
    rank_frame = frame.iloc[order][["gene_id", "treatment", "time_h", *COMPONENTS, "p_joint"]].reset_index(drop=True)
    rank_frame["rank"] = ranks.astype(int)
    rank_frame["BY_threshold_at_0.05"] = rank_threshold
    rank_frame["M_H_p_over_rank_uncapped"] = raw_ratio
    rank_frame["suffix_minimum_uncapped"] = suffix
    rank_frame.to_csv(OUT / "independent_rank_audit.tsv.gz", sep="\t", index=False, float_format="%.16g", compression={"method": "gzip", "mtime": 0})
    rank_frame.head(30).to_csv(OUT / "lowest_joint_p.tsv", sep="\t", index=False, float_format="%.16g")
    rank_frame.iloc[[best_position]].to_csv(OUT / "best_BY_ratio_row.tsv", sep="\t", index=False, float_format="%.16g")
    pd.DataFrame(by_condition).drop(columns="exact_max_counts_including_ties").to_csv(OUT / "condition_summary.tsv", sep="\t", index=False)

    # Only now compare the completed independent computation with existing output.
    reference = pd.read_csv(TASK.parent / "authoring/reports/oracle_output/matched.tsv", sep="\t")
    keys = ["gene_id", "treatment", "time_h"]
    actual = frame.set_index(keys).sort_index()
    reference = reference.set_index(keys).sort_index()
    assert actual.index.equals(reference.index)
    differences = {}
    for col in actual.columns:
        if col == "certified":
            differences[col] = {"exact_agreement": bool(np.array_equal(actual[col], reference[col]))}
            continue
        x, z = actual[col].to_numpy(float), reference[col].to_numpy(float)
        tolerance = 2e-7 + 2e-5 * np.abs(z)
        if col.startswith("p_") or col.startswith("q_"):
            tolerance = np.where(z < 1e-10, 1e-10, tolerance)
        differences[col] = {"maximum_absolute_difference": float(np.max(np.abs(x-z))), "outside_published_tolerance": int(np.sum(np.abs(x-z) > tolerance))}
    audit["posthoc_reference_comparison"] = differences
    audit["reference_matched_sha256"] = sha(TASK.parent / "authoring/reports/oracle_output/matched.tsv")
    audit["all_numeric_fields_within_published_tolerance"] = all(v.get("outside_published_tolerance", 0) == 0 for v in differences.values())
    (OUT / "independent_null_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps({"eligible": len(genes), "M": m, "nominal_conjunctions": int(all_pass.sum()), "multiplicity": audit["multiplicity"], "only_component_preventing_nominal_conjunction": only_preventer, "reference_agreement": audit["all_numeric_fields_within_published_tolerance"]}, indent=2), flush=True)


if __name__ == "__main__":
    main()
