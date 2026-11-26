# Actual native Docker/Harbor validation

Only completed exception-free trials with binary reward files count as graded. Infrastructure failures and superseded versions are retained and excluded. Deterministic controls are not empirical AI-model trials.

Final valid trials: 13. Native oracle repeats: 2; artifacts byte-identical: True.

| Job | Final version scope | Valid | Reward | CTRF passed/total | Separate verifier |
|---|---|---|---:|---|---|
| bio1-alternative-v010r1 / specificity-envelope__6BqchaR | True | True | 1.0 | 11/11 | True |
| bio1-constant-v010r1 / specificity-envelope__CFUcPeL | True | True | 0.0 | 7/11 | True |
| bio1-hardcoded-v010r1 / specificity-envelope__oMiR8K7 | True | True | 0.0 | 7/11 | True |
| bio1-incomplete-v010r1 / specificity-envelope__VRPNNKv | True | True | 0.0 | 2/11 | True |
| bio1-invalid_interpretation-v010r1 / specificity-envelope__aeftLa3 | True | True | 0.0 | 10/11 | True |
| bio1-label_shift-v010r1 / specificity-envelope__CMGvABo | True | True | 0.0 | 10/11 | True |
| bio1-nop-v010 / specificity-envelope__2NZQDh9 | True | False | None | —/— | True |
| bio1-nop-v010r1 / specificity-envelope__x9BidC4 | True | True | 0.0 | 0/11 | True |
| bio1-omitted_adjustment-v010r1 / specificity-envelope__RMmo9FL | True | True | 0.0 | 10/11 | True |
| bio1-oracle-v010 / specificity-envelope__3fkcPwt | True | True | 1.0 | 11/11 | True |
| bio1-oracle-v010 / specificity-envelope__PvRXmZg | True | True | 1.0 | 11/11 | True |
| bio1-saturated_shortcut-v010r1 / specificity-envelope__R3UYTvq | True | True | 0.0 | 10/11 | True |
| bio1-wrong_contrast-v010r1 / specificity-envelope__qBwirMf | True | True | 0.0 | 10/11 | True |
| bio1-wrong_sample_alignment-v010r2 / specificity-envelope__qmcCiwA | True | True | 0.0 | 7/11 | True |

Full per-test outcomes, exceptions, timings, task checksums, artifact hashes and exact trial directories are in `native_summary.json`; console commands are preserved in `harbor_*.log`. External QC NOT RUN; Gemini NOT RUN.
