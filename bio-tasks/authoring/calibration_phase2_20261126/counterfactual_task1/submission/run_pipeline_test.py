import pandas as pd
import numpy as np

print("Loading metadata...")
meta = pd.read_csv('/app/data/sample_metadata.csv')
sample_ids = meta['sample_id'].tolist()

print("Loading counts...")
counts_df = pd.read_csv('/app/data/GSE273600_Control_Conditions_Raw_Counts.txt.gz', compression='gzip', sep='\t')
gene_ids = counts_df.iloc[:, 0].values
count_matrix = counts_df.iloc[:, 1:].to_numpy(dtype=np.float64)

print("Computing library sizes...")
library_sizes = count_matrix.sum(axis=0) # shape (120,)

print("Computing CPM...")
# CPM_gs = 10^6 * C_gs / L_s
# count_matrix is (G, 120), library_sizes is (120,)
cpm_matrix = 1e6 * count_matrix / library_sizes[np.newaxis, :]

print("Checking eligibility (at least 6 samples have CPM >= 1)...")
eligible_mask = np.sum(cpm_matrix >= 1.0, axis=1) >= 6
eligible_count = np.sum(eligible_mask)
print("Total genes:", len(gene_ids))
print("Eligible genes:", eligible_count)

