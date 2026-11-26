import pandas as pd

meta = pd.read_csv('/app/data/sample_metadata.csv')
print("Cell lines:", meta['cell_line'].unique())
print("Treatments:", meta['treatment'].unique())
print("Times:", meta['time_h'].unique())
print("Replicates:", meta['replicate'].unique())
