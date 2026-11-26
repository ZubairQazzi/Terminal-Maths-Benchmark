"""Read the completed independent audit only; summarize low-variance limits."""
import json
from pathlib import Path
import numpy as np
import pandas as pd

root = Path(__file__).resolve().parent
frame = pd.read_csv(root / "independent_statistics.tsv.gz", sep="\t")
components = ["p_interaction", "p_parent_equivalence", "p_dmr_minimum"]
nominal = frame.p_joint <= .05
zero_se = {}
for label in ["dmr", "parent", "interaction"]:
    zero = frame["se_" + label] == 0
    df = frame.loc[~zero, "df_" + label]
    zero_se[label] = {
        "rows_zero_SE": int(zero.sum()),
        "nominal_conjunction_rows_zero_SE": int((zero & nominal).sum()),
        "nonzero_SE_df_quantiles": {str(q): float(np.quantile(df, q)) for q in [0, .05, .5, .95, 1]},
    }
tail_max = {}
order = np.argsort(frame.p_joint.to_numpy(), kind="stable")
for name, indices in [("lowest_100_joint_p", order[:100]), ("lowest_1000_joint_p", order[:1000]), ("all_nominal_conjunctions", np.where(nominal)[0])]:
    rows = frame.iloc[indices]
    p = rows[components].to_numpy()
    joint = rows.p_joint.to_numpy()
    tail_max[name] = {column: int(np.sum(p[:, j] == joint)) for j, column in enumerate(components)}
record = {
    "zero_SE_and_df": zero_se,
    "equivalence_p_exact_zero": int((frame.p_parent_equivalence == 0).sum()),
    "nominal_conjunction_with_equivalence_p_zero": int(((frame.p_parent_equivalence == 0) & nominal).sum()),
    "tail_exact_max_counts_including_ties": tail_max,
    "nominal_conjunctions_by_treatment": {key: int(value) for key, value in frame.loc[nominal].groupby("treatment").size().items()},
    "note": "Zero-SE handling is a contract convention, not empirical validation of p-value calibration for zero-inflated count-derived measurements. No requirements are changed.",
}
(root / "followup_descriptives.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
print(json.dumps(record, indent=2))
