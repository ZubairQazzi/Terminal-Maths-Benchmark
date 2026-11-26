import numpy as np

def benjamini_yekutieli(p_values):
    p_values = np.asarray(p_values, dtype=float)
    M = len(p_values)
    if M == 0:
        return p_values
    H_M = np.sum(1.0 / np.arange(1, M + 1))
    
    # Sort p-values ascending, keep track of indices
    sorted_indices = np.argsort(p_values)
    sorted_p = p_values[sorted_indices]
    
    q_sorted = np.zeros(M)
    # q_(r) = min(1, min_{j >= r} (M * H_M * p_(j) / j))
    # where rank j is 1-based (from 1 to M)
    # Let's compute M * H_M * sorted_p[j-1] / j for j=1..M
    ranks = np.arange(1, M + 1)
    vals = M * H_M * sorted_p / ranks
    
    # Cumulative minimum from right to left
    # min_{j >= r} vals[j-1]
    q_sorted = np.minimum.accumulate(vals[::-1])[::-1]
    q_sorted = np.minimum(1.0, q_sorted)
    
    # Map back to original order
    q_values = np.empty_val = np.zeros(M)
    q_values[sorted_indices] = q_sorted
    return q_values

p_test = [0.01, 0.04, 0.03, 0.5, 0.2]
q_test = benjamini_yekutieli(p_test)
print("p:", p_test)
print("q:", q_test)
