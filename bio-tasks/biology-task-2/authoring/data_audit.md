# Physical data audit

Authoring date: 25 November 2026. Script: `audit_data.py`, extended by `finish_data_reports.py`; both gzip streams were fully decompressed by pandas, which checks the gzip trailer.

Both matrices have **57,665 genes × 120 expression samples**. The count table has one identifier column; the TPM table has identifier and gene-name columns. Sample columns match exactly after excluding annotation columns; identifiers match in order. Comparing the complete table columns directly produces false because TPM has an extra annotation column, not because samples differ.

| Property | Estimated counts | Supplied TPM |
|---|---:|---:|
| Missing / nonfinite / negative | 0 / 0 / 0 | 0 / 0 / 0 |
| Fractional numeric entries (>1e-8 from integer) | 2,188,385 | 6,919,796 |
| Zero entries | 2,996,877 | 0 |
| Minimum | 0 | 0.063122 |

Ensembl identifiers include version suffixes and are unique; unversioned collisions: 0. Duplicate gene names: 1666; missing names: 0. Names are annotations, never primary keys. Duplicate sample IDs: 0.

Count library sums range 12869311.000–56504690.000, a 4.391-fold range. All-zero count genes: 3,678. Full distributions, per-sample sums, checksums and audit values are in `data_audit.json`.

**TPM technical artifact:** 3,190,994 cells equal the exact positive floor 0.063122; 2,996,877 cells have zero count but positive TPM. Fraction of zero-count cells at that floor: 100.0000%. TPM sums span 1001149.512–1001825.198, not exactly one million. The source names this file TPM, but the observed floor must not be interpreted as measured low expression. No undocumented inverse transform is asserted. The authoring audit does not establish the exact origin of the floor. Treat it as a supplied processed representation and exclude censored entries from log-ratio integrity checks.

Counts are Salmon estimated assignments and are not integer observations; no rounding was performed. TPM and count matrices represent the same biological libraries and are not independent replication. Effective transcript/gene lengths, bootstrap uncertainty, read-level quality and explicit sequencing batch are unavailable in the supplied tables. Within-gene count changes may include effective-length effects; do not present relative-count associations as direct transcript-copy or mechanistic estimates.
