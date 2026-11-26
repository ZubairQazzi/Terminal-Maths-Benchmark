# Verified experimental design

Official GEO family SOFT includes 120 GSM records, GSM8433606–GSM8433725. `reconcile_metadata.py` joins each expression column to one unique official GSM title; `sample_metadata.csv` preserves both identifiers and the original title. Each line×treatment×time group contains three samples. Replicate numbering alone does not establish longitudinal pairing or a shared batch; analyses must treat libraries as independent unless stated as a sensitivity assumption.

Two U2OS backgrounds: Parental and engineered DmrPERK. Untreated (UT): 0,4,8,16,24h. Dimerizer (Dim), arsenite (Ars), thapsigargin (Tg): 2,4,8,16,24h. GSM titles give Dim .195nM, Ars .05mM, Tg100nM; series summary rounds Dim to .2nM. Preserve the title dose rather than inventing a second dose. There are 40 groups ×3=120 libraries.

Matched treatment–UT associations within each cell line and four-cell line×treatment interactions are estimable at4,8,16,24h. UT0 is a baseline measurement, not a matched untreated2h sample. A2h effect requires assumptions on unobserved UT2; report a sensitivity set or abstain. Treatment-specific effects do not alone identify molecular ISR mediation, ATF4 dependence, eIF2α phosphorylation levels or physiological outcomes. GSE273600 lacks ATF4 knockout interventions present in a separate GEO series; those cannot be invented here.

The engineered construct permits selective ISR initiation; arsenite and thapsigargin have broader effects. Cell-line differences, clone selection, library composition and effective-length changes limit causal interpretation of transcriptional contrasts. No batch covariate is fabricated.
