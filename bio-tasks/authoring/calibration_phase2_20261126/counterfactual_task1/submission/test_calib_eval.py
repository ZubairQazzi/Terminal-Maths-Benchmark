import json
import numpy as np
import scipy.stats as stats

with open('/app/data/calibration_cases.json') as f:
    calib = json.load(f)

def compute_metrics(dt, dc, pt, pc):
    dt = np.array(dt, dtype=float)
    dc = np.array(dc, dtype=float)
    pt = np.array(pt, dtype=float)
    pc = np.array(pc, dtype=float)
    
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
    
    # dmr effect SE and df
    v_dt = var_dt / n_dt
    v_dc = var_dc / n_dc
    se_dmr = np.sqrt(v_dt + v_dc)
    if se_dmr == 0:
        df_dmr = 1e12
    else:
        num = (v_dt + v_dc)**2
        den = (v_dt**2 / (n_dt - 1) if n_dt > 1 else 0) + (v_dc**2 / (n_dc - 1) if n_dc > 1 else 0)
        df_dmr = num / den if den > 0 else 1e12
        
    # parent effect SE and df
    v_pt = var_pt / n_pt
    v_pc = var_pc / n_pc
    se_parent = np.sqrt(v_pt + v_pc)
    if se_parent == 0:
        df_parent = 1e12
    else:
        num = (v_pt + v_pc)**2
        den = (v_pt**2 / (n_pt - 1) if n_pt > 1 else 0) + (v_pc**2 / (n_pc - 1) if n_pc > 1 else 0)
        df_parent = num / den if den > 0 else 1e12

    # interaction SE and df (4 groups)
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
            p_dmr_minimum = 0.0 # Wait! Let's check if abs(d) >= 0.5 means p_dmr_minimum is 0 (significant minimum effect) or 1.
        else:
            p_dmr_minimum = 1.0
    else:
        t_stat_d = (abs(d) - 0.5) / se_dmr
        if df_dmr > 1e11:
            p_dmr_minimum = min(1.0, 2 * stats.norm.sf(t_stat_d))
        else:
            p_dmr_minimum = min(1.0, 2 * stats.t.sf(t_stat_d, df=df_dmr))
            
    p_joint = max(p_interaction, p_parent_equivalence, p_dmr_minimum)
    return d, a, i, se_dmr, df_dmr, se_parent, df_parent, se_interaction, df_interaction, p_interaction, p_parent_equivalence, p_dmr_minimum, p_joint

for case in calib['cases']:
    res = compute_metrics(case['groups']['dmr_treated'], case['groups']['dmr_control'],
                          case['groups']['parent_treated'], case['groups']['parent_control'])
    print(case['case_id'], 'p_joint:', res[-1])
