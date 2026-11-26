# Actual native Docker/Harbor validation

Only completed exception-free trials with binary reward files count as graded. Infrastructure failures and superseded versions are retained and excluded. Deterministic controls are not empirical AI-model trials.

Final valid trials: 12. Native oracle repeats: 2; artifacts byte-identical: True.

| Job | Final version scope | Valid | Reward | CTRF passed/total | Separate verifier |
|---|---|---|---:|---|---|
| bio2-alternative-v011 / transcript-provenance-audit__cALXCDD | True | True | 1.0 | 11/11 | True |
| bio2-constant-v011 / transcript-provenance-audit__poiFRV8 | True | True | 0.0 | 3/11 | True |
| bio2-hardcoded-v011 / transcript-provenance-audit__7Y7Es5B | True | True | 0.0 | 0/11 | True |
| bio2-incomplete-v011 / transcript-provenance-audit__zstgRki | True | True | 0.0 | 5/11 | True |
| bio2-invalid_claims-v011 / transcript-provenance-audit__GVZgEEv | True | True | 0.0 | 10/11 | True |
| bio2-nop-v010 / transcript-provenance-audit__KRt4BZM | False | True | 0.0 | 0/1 | True |
| bio2-nop-v011 / transcript-provenance-audit__xdeXMsZ | True | True | 0.0 | 0/11 | True |
| bio2-oracle-v010 / transcript-provenance-audit__43Zqv2D | False | True | 1.0 | 1/1 | True |
| bio2-oracle-v010 / transcript-provenance-audit__XA39ENa | False | True | 1.0 | 1/1 | True |
| bio2-oracle-v011 / transcript-provenance-audit__dybfyBZ | True | True | 1.0 | 11/11 | True |
| bio2-oracle-v011 / transcript-provenance-audit__yd6KNzd | True | True | 1.0 | 11/11 | True |
| bio2-unsupported_forced_pair-v011 / transcript-provenance-audit__us3aHZx | True | True | 0.0 | 9/11 | True |
| bio2-wrong_alignment-v011 / transcript-provenance-audit__5Uty76D | True | True | 0.0 | 8/11 | True |
| bio2-wrong_contrast-v011 / transcript-provenance-audit__Ee9iX68 | True | True | 0.0 | 8/11 | True |
| bio2-wrong_statistics-v011 / transcript-provenance-audit__mrJ2teX | True | True | 0.0 | 9/11 | True |

Full per-test outcomes, exceptions, timings, task checksums, artifact hashes and exact trial directories are in `native_summary.json`; console commands are preserved in `harbor_*.log`. External QC NOT RUN; Gemini NOT RUN.
