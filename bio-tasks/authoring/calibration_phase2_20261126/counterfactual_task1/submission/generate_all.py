import pandas as pd
import numpy as np
import scipy.stats as stats
import json

print("1. Loading metadata...")
meta = pd.read_csv('/app/data/sample_metadata.csv')
sample_ids = meta['sample_id'].tolist()

# Map sample_id to index 0..119
sample_id_to_idx = {sid: i for i, sid in enumerate(sample_ids)}

# Group sample indices by (cell_line, treatment, time_h)
# cell_line: Parental, DmrPERK
# treatment: UT, Dim, Ars, Tg
# time_h: 0, 2, 4, 8, 16, 24
group_indices = {}
for cl in ['Parental', 'DmrPERK']:
    for tr in ['UT', 'Dim', 'Ars', 'Tg']:
        for tm in [0, 2, 4, 8, 16, 24]:
            sub = meta[(meta['cell_line'] == cl) & (meta['treatment'] == tr) & (meta['time_h'] == tm)]
            idxs = [sample_id_to_idx[sid] for sid in sub['sample_id'].tolist()]
            group_indices[(cl, tr, tm)] = idxs

print("2. Loading counts...")
counts_df = pd.read_csv('/app/data/GSE273600_Control_Conditions_Raw_Counts.txt.gz', compression='gzip', sep='\t')
gene_ids = counts_df.iloc[:, 0].values
count_matrix = counts_df.iloc[:, 1:].to_numpy(dtype=np.float64)

gene_count = len(gene_ids)
frac_diff = np.abs(count_matrix - np.round(count_matrix))
fractional_count_entries = int(np.sum(frac_diff > 1e-8))

library_sizes = count_matrix.sum(axis=0) # shape (120,)
library_sizes_dict = {sample_ids[i]: float(library_sizes[i]) for i in range(120)}

print("3. Loading TPMs...")
tpms_df = pd.read_csv('/app/data/GSE273600_Control_Conditions_TPMs.txt.gz', compression='gzip', sep='\t')
tpm_matrix = tpms_df.iloc[:, 2:].to_numpy(dtype=np.float64)
tpm_floor = float(np.min(tpm_matrix))
tpm_floor_entries = int(np.sum(tpm_matrix == tpm_floor))

print("4. Computing CPM and eligible genes...")
# CPM_gs = 10^6 * C_gs / L_s
cpm_matrix = 1e6 * count_matrix / library_sizes[np.newaxis, :]
eligible_mask = np.sum(cpm_matrix >= 1.0, axis=1) >= 6
eligible_indices = np.where(eligible_mask)[0]
eligible_count = len(eligible_indices)
print(f"Eligible count: {eligible_count}")

# Precompute Y_gs = log2(1 + CPM_gs)
Y_matrix = np.log2(1.0 + cpm_matrix)

# Helper function for statistical metrics
def compute_stats(gene_idx):
    # returns list of dicts for each (treatment, time_h)
    results = []
    
    # Get Y values for this gene across groups
    # group_indices[(cl, tr, tm)] gives sample columns
    
    # Pre-extract group means and variances
    # We need Y values for the groups
    y_row = Y_matrix[gene_idx]
    
    # Helper to get group data
    def get_group_data(cl, tr, tm):
        idxs = group_indices[(cl, tr, tm)]
        vals = y_row[idxs]
        return vals

    treatments = ['Dim', 'Ars', 'Tg']
    matched_times = [4, 8, 16, 24]
    
    for tr in treatments:
        for tm in matched_times:
            # dmr treated: (DmrPERK, tr, tm)
            # dmr control: (DmrPERK, UT, tm)
            # parent treated: (Parental, tr, tm)
            # parent control: (Parental, UT, tm)
            dt = get_group_data('DmrPERK', tr, tm)
            dc = get_group_data('DmrPERK', 'UT', tm)
            pt = get_group_data('Parental', tr, tm)
            pc = get_group_data('Parental', 'UT', tm)
            
            n_dt, n_dc, n_pt, n_pc = len(dt), len(dc), len(pt), len(pc)
            mean_dt, mean_dc = np.mean(dt), np.mean(dc)
            mean_pt, mean_pc = np.mean(pt), np.mean(pc)
            
            var_dt = np.var(dt, ddof=1) if n_dt > 1 else 0.0
            var_dc = np.var(dc, ddof=1) if n_dc > 1 else 0.0
            var_pt = np.var(pt, ddof=1) if n_pt > 1 else 0.0
            var_pc = np.var(pc, ddof=1) if n_pc > 1 else 0.0
            
            d = mean_dt - mean_dc
            a = mean_pt - mean_pc
            i = d - a
            
            # dmr effect SE and df (groups: dt, dc)
            v_dt = var_dt / n_dt
            v_dc = var_dc / n_dc
            se_dmr = np.sqrt(v_dt + v_dc)
            if se_dmr == 0:
                df_dmr = 1e12
            else:
                num = (v_dt + v_dc)**2
                den = (v_dt**2 / (n_dt - 1) if n_dt > 1 else 0) + (v_dc**2 / (n_dc - 1) if n_dc > 1 else 0)
                df_dmr = num / den if den > 0 else 1e12
                
            # parent effect SE and df (groups: pt, pc)
            v_pt = var_pt / n_pt
            v_pc = var_pc / n_pc
            se_parent = np.sqrt(v_pt + v_pc)
            if se_parent == 0:
                df_parent = 1e12
            else:
                num = (v_pt + v_pc)**2
                den = (v_pt**2 / (n_pt - 1) if n_pt > 1 else 0) + (v_pc**2 / (n_pc - 1) if n_pc > 1 else 0)
                df_parent = num / den if den > 0 else 1e12

            # interaction SE and df (4 groups: dt, dc, pt, pc)
            v_dt_i = var_dt / n_dt
            v_dc_i = var_dc / n_dc
            v_pt_i = var_pt / n_pt
            v_pc_i = var_pc / n_pc
            se_interaction = np.sqrt(v_dt_i + v_dc_i + v_pt_i + v_pc_i)
            if se_interaction == 0:
                df_interaction = 1e12
            else:
                num = (v_dt_i + v_dc_i + v_pt_i + v_pc_i)**2
                den = ( (v_dt_i**2 / (n_dt - 1) if n_dt > 1 else 0) +
                        (v_dc_i**2 / (n_dc - 1) if n_dc > 1 else 0) +
                        (v_pt_i**2 / (n_pt - 1) if n_pt > 1 else 0) +
                        (v_pc_i**2 / (n_pc - 1) if n_pc > 1 else 0) )
                df_interaction = num / den if den > 0 else 1e12

            # p_interaction
            if se_interaction == 0:
                p_interaction = 1.0 if i == 0 else 0.0
            else:
                t_stat_i = abs(i) / se_interaction
                if df_interaction > 1e11:
                    p_interaction = min(1.0, 2 * stats.norm.sf(t_stat_i))
                else:
                    p_interaction = min(1.0, 2 * stats.t.sf(t_stat_i, df=df_interaction))

            # p_parent_equivalence
            if se_parent == 0:
                if -0.3 < a < 0.3:
                    p_parent_equivalence = 0.0
                else:
                    p_parent_equivalence = 1.0
            else:
                if df_parent > 1e11:
                    p1 = stats.norm.sf((a + 0.3) / se_parent)
                    p2 = stats.norm.cdf((a - 0.3) / se_parent)
                else:
                    p1 = stats.t.sf((a + 0.3) / se_parent, df=df_parent)
                    p2 = stats.t.cdf((a - 0.3) / se_parent, df=df_parent)
                p_parent_equivalence = max(p1, p2)

            # p_dmr_minimum
            if se_dmr == 0:
                if abs(d) >= 0.5:
                    p_dmr_minimum = 0.0
                else:
                    p_dmr_minimum = 1.0
            else:
                t_stat_d = (abs(d) - 0.5) / se_dmr
                if df_dmr > 1e11:
                    p_dmr_minimum = min(1.0, 2 * stats.norm.sf(t_stat_d))
                else:
                    p_dmr_minimum = min(1.0, 2 * stats.t.sf(t_stat_d, df=df_dmr))

            p_joint = max(p_interaction, p_parent_equivalence, p_dmr_minimum)
            
            results.append({
                'gene_id': gene_ids[gene_idx],
                'treatment': tr,
                'time_h': tm,
                'dmr_effect': d,
                'parent_effect': a,
                'interaction': i,
                'se_dmr': se_dmr,
                'df_dmr': df_dmr,
                'se_parent': se_parent,
                'df_parent': df_parent,
                'se_interaction': se_interaction,
                'df_interaction': df_interaction,
                'p_interaction': p_interaction,
                'p_parent_equivalence': p_parent_equivalence,
                'p_dmr_minimum': p_dmr_minimum,
                'p_joint': p_joint
            })
    return results

print("5. Computing matched table statistics for eligible genes...")
all_matched_records = []
for idx in eligible_indices:
    all_matched_records.extend(compute_stats(idx))

matched_df = pd.DataFrame(all_matched_records)
print(f"Matched rows count: {len(matched_df)}")

print("6. Applying Benjamini-Yekutieli correction to matched table...")
p_joints = matched_df['p_joint'].to_numpy(dtype=float)
M = len(p_joints)
H_M = np.sum(1.0 / np.arange(1, M + 1))

sorted_indices = np.argsort(p_joints)
sorted_p = p_joints[sorted_indices]
ranks = np.arange(1, M + 1)
vals = M * H_M * sorted_p / ranks
q_sorted = np.minimum.accumulate(vals[::-1])[::-1]
q_sorted = np.minimum(1.0, q_sorted)

q_values = np.zeros(M)
q_values[sorted_indices] = q_sorted

matched_df['q_joint'] = q_values
matched_df['certified'] = matched_df['q_joint'] <= 0.05
# format certified as true / false lowercase
matched_df['certified'] = matched_df['certified'].astype(str).str.lower()

print(f"True certificates count: {sum(matched_df['certified'] == 'true')}")

print("7. Computing early bounds (2h sensitivity analysis)...")
# For each eligible gene and treatment, compute D2 and bounds for expansions {0, 0.3, 0.6}
early_records = []
treatments = ['Dim', 'Ars', 'Tg']
expansions = [0, 0.3, 0.6]

for idx in eligible_indices:
    y_row = Y_matrix[idx]
    gid = gene_ids[idx]
    
    # Pre-extract UT0 and UT4 for Parental and DmrPERK
    p_ut0 = y_row[group_indices[('Parental', 'UT', 0)]]
    p_ut4 = y_row[group_indices[('Parental', 'UT', 4)]]
    d_ut0 = y_row[group_indices[('DmrPERK', 'UT', 0)]]
    d_ut4 = y_row[group_indices[('DmrPERK', 'UT', 4)]]
    
    mean_p_ut0, mean_p_ut4 = np.mean(p_ut0), np.mean(p_ut4)
    mean_d_ut0, mean_d_ut4 = np.mean(d_ut0), np.mean(d_ut4)
    
    for tr in treatments:
        # D2: observed difference of treated Dmr-PERK and parental means at 2h
        d_tr2 = y_row[group_indices[('DmrPERK', tr, 2)]]
        p_tr2 = y_row[group_indices[('Parental', tr, 2)]]
        D2 = np.mean(d_tr2) - np.mean(p_tr2)
        
        for e in expansions:
            lo_parental = min(mean_p_ut0, mean_p_ut4) - e
            hi_parental = max(mean_p_ut0, mean_p_ut4) + e
            lo_dmr = min(mean_d_ut0, mean_d_ut4) - e
            hi_dmr = max(mean_d_ut0, mean_d_ut4) + e
            
            lower = D2 - hi_dmr + lo_parental
            upper = D2 - lo_dmr + hi_parental
            
            if lower > 0.5:
                classification = 'positive'
            elif upper < -0.5:
                classification = 'negative'
            else:
                classification = 'unresolved'
                
            early_records.append({
                'gene_id': gid,
                'treatment': tr,
                'expansion': e,
                'treated_difference': D2,
                'lower': lower,
                'upper': upper,
                'classification': classification
            })

early_df = pd.DataFrame(early_records)

print("8. Processing calibration cases...")
with open('/app/data/calibration_cases.json') as f:
    calib = json.load(f)

calib_records = []
for case in calib['cases']:
    case_id = case['case_id']
    g = case['groups']
    dt = g['dmr_treated']
    dc = g['dmr_control']
    pt = g['parent_treated']
    pc = g['parent_control']
    
    # Run compute_stats logic on synthetic triplicates
    dt_arr = np.array(dt, dtype=float)
    dc_arr = np.array(dc, dtype=float)
    pt_arr = np.array(pt, dtype=float)
    pc_arr = np.array(pc, dtype=float)
    
    n_dt, n_dc, n_pt, n_pc = len(dt_arr), len(dc_arr), len(pt_arr), len(pc_arr)
    mean_dt, mean_dc = np.mean(dt_arr), np.mean(dc_arr)
    mean_pt, mean_pc = np.mean(pt_arr), np.mean(pc_arr)
    
    var_dt = np.var(dt_arr, ddof=1) if n_dt > 1 else 0.0
    var_dc = np.var(dc_arr, ddof=1) if n_dc > 1 else 0.0
    var_pt = np.var(pt_arr, ddof=1) if n_pt > 1 else 0.0
    var_pc = np.var(pc_arr, ddof=1) if n_pc > 1 else 0.0
    
    d = mean_dt - mean_dc
    a = mean_pt - mean_pc
    i = d - a
    
    v_dt = var_dt / n_dt
    v_dc = var_dc / n_dc
    se_dmr = np.sqrt(v_dt + v_dc)
    if se_dmr == 0:
        df_dmr = 1e12
    else:
        num = (v_dt + v_dc)**2
        den = (v_dt**2 / (n_dt - 1) if n_dt > 1 else 0) + (v_dc**2 / (n_dc - 1) if n_dc > 1 else 0)
        df_dmr = num / den if den > 0 else 1e12
        
    v_pt = var_pt / n_pt
    v_pc = var_pc / n_pc
    se_parent = np.sqrt(v_pt + v_pc)
    if se_parent == 0:
        df_parent = 1e12
    else:
        num = (v_pt + v_pc)**2
        den = (v_pt**2 / (n_pt - 1) if n_pt > 1 else 0) + (v_pc**2 / (n_pc - 1) if n_pc > 1 else 0)
        df_parent = num / den if den > 0 else 1e12

    v_dt_i = var_dt / n_dt
    v_dc_i = var_dc / n_dc
    v_pt_i = var_pt / n_pt
    v_pc_i = var_pc / n_pc
    se_interaction = np.sqrt(v_dt_i + v_dc_i + v_pt_i + v_pc_i)
    if se_interaction == 0:
        df_interaction = 1e12
    else:
        num = (v_dt_i + v_dc_i + v_pt_i + v_pc_i)**2
        den = ( (v_dt_i**2 / (n_dt - 1) if n_dt > 1 else 0) +
                (v_dc_i**2 / (n_dc - 1) if n_dc > 1 else 0) +
                (v_pt_i**2 / (n_pt - 1) if n_pt > 1 else 0) +
                (v_pc_i**2 / (n_pc - 1) if n_pc > 1 else 0) )
        df_interaction = num / den if den > 0 else 1e12

    if se_interaction == 0:
        p_interaction = 1.0 if i == 0 else 0.0
    else:
        t_stat_i = abs(i) / se_interaction
        if df_interaction > 1e11:
            p_interaction = min(1.0, 2 * stats.norm.sf(t_stat_i))
        else:
            p_interaction = min(1.0, 2 * stats.t.sf(t_stat_i, df=df_interaction))

    if se_parent == 0:
        if -0.3 < a < 0.3:
            p_parent_equivalence = 0.0
        else:
            p_parent_equivalence = 1.0
    else:
        if df_parent > 1e11:
            p1 = stats.norm.sf((a + 0.3) / se_parent)
            p2 = stats.norm.cdf((a - 0.3) / se_parent)
        else:
            p1 = stats.t.sf((a + 0.3) / se_parent, df=df_parent)
            p2 = stats.t.cdf((a - 0.3) / se_parent, df=df_parent)
        p_parent_equivalence = max(p1, p2)

    if se_dmr == 0:
        if abs(d) >= 0.5:
            p_dmr_minimum = 0.0
        else:
            p_dmr_minimum = 1.0
    else:
        t_stat_d = (abs(d) - 0.5) / se_dmr
        if df_dmr > 1e11:
            p_dmr_minimum = min(1.0, 2 * stats.norm.sf(t_stat_d))
        else:
            p_dmr_minimum = min(1.0, 2 * stats.t.sf(t_stat_d, df=df_dmr))

    p_joint = max(p_interaction, p_parent_equivalence, p_dmr_minimum)
    
    calib_records.append({
        'case_id': case_id,
        'dmr_effect': d,
        'parent_effect': a,
        'interaction': i,
        'se_dmr': se_dmr,
        'df_dmr': df_dmr,
        'se_parent': se_parent,
        'df_parent': df_parent,
        'se_interaction': se_interaction,
        'df_interaction': df_interaction,
        'p_interaction': p_interaction,
        'p_parent_equivalence': p_parent_equivalence,
        'p_dmr_minimum': p_dmr_minimum,
        'p_joint': p_joint,
        'p_joint_raw': p_joint
    })

calib_df = pd.DataFrame(calib_records)
# BY correction for calibration cases (M=8)
c_p = calib_df['p_joint_raw'].to_numpy(dtype=float)
c_M = len(c_p)
c_HM = np.sum(1.0 / np.arange(1, c_M + 1))
c_sorted_idx = np.argsort(c_p)
c_sorted_p = c_p[c_sorted_idx]
c_ranks = np.arange(1, c_M + 1)
c_vals = c_M * c_HM * c_sorted_p / c_ranks
c_q_sorted = np.minimum.accumulate(c_vals[::-1])[::-1]
c_q_sorted = np.minimum(1.0, c_q_sorted)
c_q_values = np.zeros(c_M)
c_q_values[c_sorted_idx] = c_q_sorted

calib_df['q_joint'] = c_q_values
calib_df['certified'] = (calib_df['q_joint'] <= 0.05).astype(str).str.lower()
calib_df = calib_df.drop(columns=['p_joint_raw'])

print("9. Writing artifacts...")

# 1. audit.json
audit_data = {
    "sample_count": 120,
    "gene_count": int(gene_count),
    "eligible_count": int(eligible_count),
    "fractional_count_entries": int(fractional_count_entries),
    "tpm_floor": float(tpm_floor),
    "tpm_floor_entries": int(tpm_floor_entries),
    "library_sizes": library_sizes_dict,
    "estimand": "relative_count_abundance",
    "causal_atf4_claim": False
}
with open('/app/submission/audit.json', 'w') as f:
    json.dump(audit_data, f, indent=2)

# 2. eligible_genes.tsv
# columns gene_id, gene_name; every eligible Ensembl ID once with its TPM annotation.
eligible_tpms = tpms_df.iloc[eligible_indices, :2].copy()
eligible_tpms.columns = ['gene_id', 'gene_name']
eligible_tpms.to_csv('/app/submission/eligible_genes.tsv', sep='\t', index=False)

# 3. matched.tsv
matched_df.to_csv('/app/submission/matched.tsv', sep='\t', index=False)

# 4. early_bounds.tsv
early_df.to_csv('/app/submission/early_bounds.tsv', sep='\t', index=False)

# 5. interpretation.json
cert_count = int(sum(matched_df['certified'] == 'true'))
interp_data = {
    "matched_times": [4, 8, 16, 24],
    "missing_control_times": [2],
    "early_result_type": "assumption_dependent_sensitivity_region",
    "early_envelope_verified": False,
    "replicates_paired": False,
    "effective_length_offsets_available": False,
    "independent_expression_datasets": 1,
    "certificate_count": cert_count
}
with open('/app/submission/interpretation.json', 'w') as f:
    json.dump(interp_data, f, indent=2)

# 6. calibration.tsv
# columns case_id, followed by every numeric and certified column of matched table starting at dmr_effect
calib_df.to_csv('/app/submission/calibration.tsv', sep='\t', index=False)

print("All artifacts generated successfully!")
