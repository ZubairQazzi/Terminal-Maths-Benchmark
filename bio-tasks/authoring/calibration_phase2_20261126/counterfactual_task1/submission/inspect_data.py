import pandas as pd
import numpy as np
import json
import gzip

print("Loading metadata...")
meta = pd.read_csv('/app/data/sample_metadata.csv')
sample_ids = meta['sample_id'].tolist()
print("Sample IDs count:", len(sample_ids))

print("Loading counts...")
counts_df = pd.read_csv('/app/data/GSE273600_Control_Conditions_Raw_Counts.txt.gz', compression='gzip', sep='\t')
print("Counts shape:", counts_df.shape)
id_col = counts_df.columns[0]
print("ID column name in counts:", id_col)

count_matrix = counts_df.iloc[:, 1:].to_numpy(dtype=np.float64)
frac_diff = np.abs(count_matrix - np.round(count_matrix))
fractional_count_entries = int(np.sum(frac_diff > 1e-8))
print("Fractional count entries:", fractional_count_entries)

lib_sizes = count_matrix.sum(axis=0)
library_sizes = {counts_df.columns[1+i]: float(lib_sizes[i]) for i in range(len(counts_df.columns)-1)}
print("Sample library sizes sample 0:", list(library_sizes.items())[:3])

print("Loading TPMs...")
tpms_df = pd.read_csv('/app/data/GSE273600_Control_Conditions_TPMs.txt.gz', compression='gzip', sep='\t')
print("TPMs shape:", tpms_df.shape)
tpm_matrix = tpms_df.iloc[:, 2:].to_numpy(dtype=np.float64)
tpm_floor = float(np.min(tpm_matrix))
tpm_floor_entries = int(np.sum(tpm_matrix == tpm_floor))
print("TPM floor:", tpm_floor, "Entries:", tpm_floor_entries)

