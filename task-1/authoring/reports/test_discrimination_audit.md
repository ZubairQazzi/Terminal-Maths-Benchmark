# Discrimination and alternative certificate audit

These results are author-side controlled certificate mutants. They isolate scientific mistakes inside otherwise correct outputs; they are not independent agents or measured AI failure rates. Generic and numerical rank values are independently computed guesses, but other fields in those two controls remain correct. Native partial/no-op/public-example controls are separately recorded. An accepted mutant on an unaffected case is legitimate and not a grader failure.

| Plausible flawed approach / mutant | Rejected pencils / 48 |
|---|---|
| generic-full-rank | 34 |
| no-infinity | 29 |
| split-primary-powers | 24 |
| ignore-right-indices | 29 |
| ignore-left-indices | 26 |
| nonminimal-basis | 36 |
| numerical-rank | 0 |
| invalid-frame | 48 |
| early-stages-only | 48 |
| noninvariant-frame | 43 |
| invalid-resolvent | 48 |
| inconsistent-projector | 36 |
| wrong-forcing-class | 43 |
| inflated-pole-denominator | 35 |
| missing-pole-proof | 35 |
| numerical-spectral-blocks | 40 |
| literal constant output | 48 |
| universal zero-structure guess | 45 |

Numerical rank alone matched all 48 exact ranks; this correct intermediate value is accepted. The independent floating-point spectral-block heuristic was rejected on 40/48 pencils for actual primary-structure errors, using exact rational output encodings. The shape-aware zero-structure baseline passed only the three zero pencils and still earned native reward 0; the literal constant output passed none. These findings are retained honestly rather than changing grading to force algorithm-specific failures.

All 42 structural cases reject at least one semantic wrong approach. This is measurable discrimination, not evidence of frontier-model difficulty. All 48 altered valid certificates pass, covering frame rescaling, degree-compatible polynomial unimodular basis changes, polynomial duals, different reflexive inverses, different particular solutions, p/+q syntax, JSON integer coefficients and ignored diagnostic floats. One small case exercises 5,001-digit scaling. Detailed first failing stages for every mutant/case and alternative timings are in control_audit.json.

| Case | Rejected mutants | Valid alternative |
|---|---|---|
| case-000 | 7/16 | PASS |
| case-001 | 7/16 | PASS |
| case-002 | 4/16 | PASS |
| case-003 | 6/16 | PASS |
| case-004 | 8/16 | PASS |
| case-005 | 9/16 | PASS |
| case-006 | 10/16 | PASS |
| case-007 | 10/16 | PASS |
| case-008 | 9/16 | PASS |
| case-009 | 7/16 | PASS |
| case-010 | 9/16 | PASS |
| case-011 | 7/16 | PASS |
| case-012 | 6/16 | PASS |
| case-013 | 6/16 | PASS |
| case-014 | 6/16 | PASS |
| case-015 | 14/16 | PASS |
| case-016 | 15/16 | PASS |
| case-017 | 15/16 | PASS |
| case-018 | 11/16 | PASS |
| case-019 | 10/16 | PASS |
| case-020 | 14/16 | PASS |
| case-021 | 14/16 | PASS |
| case-022 | 13/16 | PASS |
| case-023 | 15/16 | PASS |
| case-024 | 13/16 | PASS |
| case-025 | 13/16 | PASS |
| case-026 | 15/16 | PASS |
| case-027 | 14/16 | PASS |
| case-028 | 15/16 | PASS |
| case-029 | 14/16 | PASS |
| case-030 | 7/16 | PASS |
| case-031 | 7/16 | PASS |
| case-032 | 15/16 | PASS |
| case-033 | 15/16 | PASS |
| case-034 | 14/16 | PASS |
| case-035 | 10/16 | PASS |
| case-036 | 14/16 | PASS |
| case-037 | 11/16 | PASS |
| case-038 | 15/16 | PASS |
| case-039 | 14/16 | PASS |
| case-040 | 15/16 | PASS |
| case-041 | 15/16 | PASS |
| case-042 | 14/16 | PASS |
| case-043 | 14/16 | PASS |
| case-044 | 15/16 | PASS |
| case-045 | 14/16 | PASS |
| case-046 | 14/16 | PASS |
| case-047 | 15/16 | PASS |
