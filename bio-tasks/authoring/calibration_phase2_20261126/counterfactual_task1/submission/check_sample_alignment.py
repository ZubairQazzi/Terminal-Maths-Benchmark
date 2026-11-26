import pandas as pd

meta = pd.read_csv('/app/data/sample_metadata.csv')
sample_ids_meta = meta['sample_id'].tolist()

counts_df = pd.read_csv('/app/data/GSE273600_Control_Conditions_Raw_Counts.txt.gz', compression='gzip', nrows=1, sep='\t')
sample_ids_counts = list(counts_df.columns[1:])

tpms_df = pd.read_csv('/app/data/GSE273600_Control_Conditions_TPMs.txt.gz', compression='gzip', nrows=1, sep='\t')
sample_ids_tpms = list(tpms_df.columns[2:])

print("Counts columns match metadata exactly?", sample_ids_meta == sample_ids_counts)
print("TPMs columns match metadata exactly?", sample_ids_meta == sample_ids_tpms)

if sample_ids_meta != sample_ids_counts:
    print("Counts mismatch:", set(sample_ids_meta) ^ set(sample_ids_counts))
if sample_ids_meta != sample_ids_tpms:
    print("TPMs mismatch:", set(sample_ids_meta) ^ set(sample_ids_tpms))
