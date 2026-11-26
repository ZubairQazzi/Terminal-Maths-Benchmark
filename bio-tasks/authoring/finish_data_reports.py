from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'authoring'
audit=json.loads((OUT/'data_audit.json').read_text())
raw=ROOT/'shared-inputs/original-read-only-data'
c=pd.read_csv(raw/'GSE273600_Control_Conditions_Raw_Counts.txt.gz',sep='\t',index_col=0)
t=pd.read_csv(raw/'GSE273600_Control_Conditions_TPMs.txt.gz',sep='\t',index_col=0)
x=c.to_numpy(float);y=t[c.columns].to_numpy(float)
floor=float(y.min())
more={'aligned_sample_columns':c.columns.tolist()==t.columns[1:].tolist(),'gene_order_equal':c.index.equals(t.index),'sample_id_duplicates':int(c.columns.duplicated().sum()),'ensembl_ids_unique':bool(c.index.is_unique),'ensembl_unversioned_duplicates':int(pd.Index(c.index.str.replace(r'\.\d+$','',regex=True)).duplicated().sum()),'gene_symbol_duplicates':int(t.gene_name.duplicated().sum()),'gene_symbols_missing':int(t.gene_name.isna().sum()),'tpm_floor':floor,'tpm_floor_cells':int((y==floor).sum()),'floor_on_count_zero_fraction':float((y[x==0]==floor).mean()),'positive_tpm_on_zero_count_cells':int(((x==0)&(y>0)).sum()),'library_size_min':float(x.sum(0).min()),'library_size_max':float(x.sum(0).max()),'library_size_ratio':float(x.sum(0).max()/x.sum(0).min()),'tpm_sum_min':float(y.sum(0).min()),'tpm_sum_max':float(y.sum(0).max()),'all_zero_count_genes':int((x.sum(1)==0).sum())}
audit['extended']=more
(OUT/'data_audit.json').write_text(json.dumps(audit,indent=2))
meta=pd.read_csv(OUT/'sample_metadata.csv')
text=f'''# Physical data audit

Authoring date: 25 November 2026. Script: `audit_data.py`, extended by `finish_data_reports.py`; both gzip streams were fully decompressed by pandas, which checks the gzip trailer.

Both matrices have **57,665 genes × 120 expression samples**. The count table has one identifier column; the TPM table has identifier and gene-name columns. Sample columns match exactly after excluding annotation columns; identifiers match in order. Comparing the complete table columns directly produces false because TPM has an extra annotation column, not because samples differ.

| Property | Estimated counts | Supplied TPM |
|---|---:|---:|
| Missing / nonfinite / negative | 0 / 0 / 0 | 0 / 0 / 0 |
| Fractional numeric entries (>1e-8 from integer) | {audit['counts']['fractional']:,} | {audit['tpm']['fractional']:,} |
| Zero entries | {audit['counts']['zeros']:,} | {audit['tpm']['zeros']:,} |
| Minimum | 0 | {floor} |

Ensembl identifiers include version suffixes and are unique; unversioned collisions: {more['ensembl_unversioned_duplicates']}. Duplicate gene names: {more['gene_symbol_duplicates']}; missing names: {more['gene_symbols_missing']}. Names are annotations, never primary keys. Duplicate sample IDs: {more['sample_id_duplicates']}.

Count library sums range {more['library_size_min']:.3f}–{more['library_size_max']:.3f}, a {more['library_size_ratio']:.3f}-fold range. All-zero count genes: {more['all_zero_count_genes']:,}. Full distributions, per-sample sums, checksums and audit values are in `data_audit.json`.

**TPM technical artifact:** {more['tpm_floor_cells']:,} cells equal the exact positive floor {floor}; {more['positive_tpm_on_zero_count_cells']:,} cells have zero count but positive TPM. Fraction of zero-count cells at that floor: {more['floor_on_count_zero_fraction']:.4%}. TPM sums span {more['tpm_sum_min']:.3f}–{more['tpm_sum_max']:.3f}, not exactly one million. The source names this file TPM, but the observed floor must not be interpreted as measured low expression. No undocumented inverse transform is asserted. The authoring audit does not establish the exact origin of the floor. Treat it as a supplied processed representation and exclude censored entries from log-ratio integrity checks.

Counts are Salmon estimated assignments and are not integer observations; no rounding was performed. TPM and count matrices represent the same biological libraries and are not independent replication. Effective transcript/gene lengths, bootstrap uncertainty, read-level quality and explicit sequencing batch are unavailable in the supplied tables. Within-gene count changes may include effective-length effects; do not present relative-count associations as direct transcript-copy or mechanistic estimates.
'''
(OUT/'data_audit.md').write_text(text,encoding='utf-8')
(OUT/'experimental_design.md').write_text('''# Verified experimental design

Official GEO family SOFT includes 120 GSM records, GSM8433606–GSM8433725. `reconcile_metadata.py` joins each expression column to one unique official GSM title; `sample_metadata.csv` preserves both identifiers and the original title. Each line×treatment×time group contains three samples. Replicate numbering alone does not establish longitudinal pairing or a shared batch; analyses must treat libraries as independent unless stated as a sensitivity assumption.

Two U2OS backgrounds: Parental and engineered DmrPERK. Untreated (UT): 0,4,8,16,24h. Dimerizer (Dim), arsenite (Ars), thapsigargin (Tg): 2,4,8,16,24h. GSM titles give Dim .195nM, Ars .05mM, Tg100nM; series summary rounds Dim to .2nM. Preserve the title dose rather than inventing a second dose. There are 40 groups ×3=120 libraries.

Matched treatment–UT associations within each cell line and four-cell line×treatment interactions are estimable at4,8,16,24h. UT0 is a baseline measurement, not a matched untreated2h sample. A2h effect requires assumptions on unobserved UT2; report a sensitivity set or abstain. Treatment-specific effects do not alone identify molecular ISR mediation, ATF4 dependence, eIF2α phosphorylation levels or physiological outcomes. GSE273600 lacks ATF4 knockout interventions present in a separate GEO series; those cannot be invented here.

The engineered construct permits selective ISR initiation; arsenite and thapsigargin have broader effects. Cell-line differences, clone selection, library composition and effective-length changes limit causal interpretation of transcriptional contrasts. No batch covariate is fabricated.
''',encoding='utf-8')
lines=['# Data provenance','', 'Local originals are immutable source copies. Each runnable task contains its own verified copy or documented deterministic derivative, with no cross-task runtime dependency.','', '| File | SHA-256 |','|---|---|']
for k in ('counts','tpm'):
    r=audit[k];lines.append(f"| {r['filename']} | `{r['sha256']}` |")
lines.extend(['','Official metadata: [GEO GSE273600](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273600); [family SOFT](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE273nnn/GSE273600/soft/GSE273600_family.soft.gz). SOFT SHA-256: `'+audit['soft']['sha256']+'`. Downloaded25 November2026.','', 'Source publication: Labbé, LeBon, King et al. Nature Communications15,8301(2024), DOI [10.1038/s41467-024-52538-5](https://doi.org/10.1038/s41467-024-52538-5). Attribute the original experimental authors and GEO deposit. Public deposition permits access; it is not a declaration that third-party code or every derivative has an unrestricted license. No ownership of the experimental data is claimed.','', 'SOFT processing: FastQC0.11.5; Salmon0.9.1 pseudo-alignment without adapter trimming; Ensembl humanGRCh38 transcriptome. These describe the depositor workflow, not a re-run from FASTQ by this project. Gene-level aggregation details and TPM floor mechanism are not fully recoverable from these two tables.','', 'Original downloads in C:/Users/zubai/Downloads were read/copied only. The paired expression representations are one experiment. Authoring downloads are cached; grading must not retrieve metadata or data over the network.'])
(OUT/'data_provenance.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(more,indent=2))
