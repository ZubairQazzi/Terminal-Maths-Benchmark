# Independent local QC review: certified-pencil-structure v0.2.0

Verdict: **PASS with warnings as a local independent reviewer opinion.** All 29 static and 38 supplied rubric IDs were evaluated. No confirmed active-package defect or required correction was identified. This is not an external QC panel, independent human review or frontier-model approval.

The reviewed package is `tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure`. Its point-in-time package SHA-256 is `77f1da70c5c59673b77bf0631d700e486c9f17d562daf6c384558f63dc8942e6`. The hash is SHA-256 of canonical sorted compact JSON mapping every POSIX-relative package filename to its byte SHA-256, including dotfiles. `initial_findings.json` and `independent_qc_criteria.json` retain every file hash; the final package matches the initial snapshot exactly.

## Independence and method

The reviewer first inspected the authoritative 29+38 checklist, active public contract/examples, manifest/images, private generator, exact checker, oracle/frames and raw native r3 logs. `initial_findings.json` was written before reading the creator README, proofs, design explanations or QC-verdict reports. Creator explanations and controls were consulted afterward and treated as secondary evidence. The reviewer did not edit the active task, touch original/Task 2/Task 3 files, commit, push, publish, install tools or invoke provider APIs.

Reviewer-owned code is under `authoring/evidence/independent_*.py`; all output/cache/temp locations remain in the F: audit project. Existing C: Python/Harbor/Docker binaries were used with required sandbox escalation and process-local F: settings. No host HOME/CODEX_HOME changes or API-key reads were performed.

The reviewer independently reran the 26 pinned shell checks, checked the five entry files, reran installed Harbor ALL lint, and recomputed pinned-corpus TF-IDF. All **29 static checks passed**. All 97 saved corpus file hashes and completeness against the saved tree were verified. Maximum instruction similarity was 0.16791452110672503, below 0.8; substantive similarity was 0.16450251628306747. This finite corpus cannot establish global originality.

`independent_probe_results.json` records **280 passed, 0 failed** mathematical probes, including all 48 original-oracle certificates, all 48 independently changed valid alternatives and independent exact coefficient-map RREF checks of selected right/left Hilbert dimensions. Hand-derived certificates for a C((z-2)^2) + R1 + L0 pencil establish polynomial, inconsistent, pole-order-one and pole-order-two responses; wrong exponents and missing bounds are rejected. Legal signed/positive-denominator strings and 5,001-digit integers are accepted; invalid scalar forms are rejected. The first expression-level RREF experiment was stopped after 16 pencils because symbolic simplification was slow; the completed run uses exact domain-matrix RREF and is the reported 280-check evidence. This was a reviewer-computation issue, not a package defect.

`independent_runtime_results.json` records **5 passed, 0 failed** own native harness probes. The candidate asserts UID/GID 65534, empty supplementary groups, no provider-secret environment names, denied reads of tests, denied writes of rewards and copied source, and availability of a regular helper under a cache-named directory. Exact signed scalars and finite-float extras pass; scientific floats, booleans, negative denominators and NaN extras fail. The image's seven checker/script fingerprints match the reviewed active files. Independent agent-image inspection finds only `spec.md` and `data/examples.json` under `/app`, SymPy 1.14.0/mpmath 1.3.0, and no oracle, tests or solution directory.

## Mathematical correctness and fairness

For P=A-zB, the public companion convention, zero-size singular blocks, reversal/infinity definition and polynomial encodings agree with the checker. Empty dimensions are retained by explicit polynomial-matrix shapes; the full-family probes include zero pencils and regular pencils with empty left/right modules.

The saturation requirements are valid: k polynomial kernel columns with the expected degree multiset, independent highest coefficients and a polynomial dual form a reduced saturated basis of the full rank-k polynomial kernel module. Constant strict equivalence independently certifies all advertised Kronecker block dimensions/structure. Redundant checks make errors detectable rather than force a particular basis.

The minimum-pole proof is sound. Let G=N/D satisfy the submitted identities and GP be polynomial. For any solution Px=f and polynomial t with tx polynomial, tGf=GP(tx) is polynomial. Thus the denominator of Gf divides every possible solution denominator, including solutions changed by rational kernel vectors. For compatible f, P(Gf)=f supplies attainability. Cancelling gcd(D, components of Nf) therefore yields the intrinsic least monic denominator.

For p^a dividing that denominator and E=valuation_p(D), a row of N with response valuation E-a provides wP divisible by p^E and wf of valuation E-a. For every denominator t, wP(tx)=t(wf), hence valuation_p(t)>=a. The checker verifies these properties directly and requires exactly all primes of delta. Hand-derived intermediate-pole tests confirm the distinction between forcing compatibility over Q(z) and polynomial solvability. Infinity is intentionally unrestricted in the polynomial part; delta records finite poles.

The independent alternatives reverse arbitrary block orders (including zero-sized contributions), rescale frames rationally, apply degree-compatible nonconstant unimodular kernel-basis shears, add degree-11 annihilators to duals, change reflexive inverses through polynomial kernel/cokernel maps, recompute projector factors, add degree-seven kernel solutions, and add unreduced degree-twelve multiples of p^E to pole-witness rows. All 48 pass. These are reviewer-authored transformations, not imports of creator controls. These full-family checks run in-process; the raw native author alternative supplies separate process-budget/transfer evidence. No requirement to match oracle normalizations was found.

## Thirteen connected obligations

| Stage | Obligation | Independent assessment | Active evidence |
|---|---|---|---|
| 01 | Normal rank / minor | Nonzero specialization minor establishes the lower bound; full equivalence and expected rank establish the upper bound. | `tests/constructive.py:38` |
| 02 | Smith invariant factors | Exact monic coefficient lists equal canonical-source invariant factors, including units. | `tests/constructive.py:47` |
| 03 | Primary blocks | Primary multiset equals independently generated irreducible elementary divisors; block order is free. | `tests/constructive.py:50` |
| 04 | Infinity | Separate reversal valuations/sizes, Weyr profile and canonical pair identity prevent finite-zero confusion. | `tests/constructive.py:54` |
| 05 | Right filtration | Expected degree multiplicities/Hilbert function and actual basis identities agree; own coefficient-map RREF checks selected degrees. | `tests/constructive.py:58` |
| 06 | Left filtration | Transpose-side checks preserve rectangular dimensions and repeated/zero indices. | `tests/constructive.py:60` |
| 07 | Strict equivalence | Both constant frames must be invertible and satisfy both pair identities. Reversed block orders pass. | `tests/constructive.py:64` |
| 08 | Saturated bases / duals | Kernel identities, exact degrees, independent leading vectors and polynomial left inverses establish a minimal saturated basis. | `tests/constructive.py:69` |
| 09 | Reflexive generalized inverse | Both reflexive identities and divisibility of PN/NP exclude artificial finite projector poles. | `tests/constructive.py:76` |
| 10 | Projector factors | Four identities connect independently chosen bases to independently chosen inverse/complements. | `tests/constructive.py:83` |
| 11 | Forcing compatibility | Left-basis obstruction is necessary/sufficient over Q(z); inconsistent responses name a genuinely nonzero component. | `tests/constructive.py:92` |
| 12 | Attainable denominator | Monic delta divides D and Py=delta f supplies the matching upper bound. Own hand cases distinguish polynomial/full/reduced poles. | `tests/constructive.py:99` |
| 13 | Intrinsic lower bounds | For every p dividing delta, wP=0 mod p^E and valuation(wf)=E-a force valuation(t)>=a for every solution denominator t. | `tests/constructive.py:103` |

The five scientific layers are coherent: (1) exact disguised integer pairs feed every stage; (2) primary/infinite/singular module structure determines canonical dimensions; (3) constant pair equivalence certifies the classification; (4) saturated kernels, duals and polynomial splitting connect solution complements; (5) local prime-power obstructions certify the optimal forced response. These are connected certificate obligations, not thirteen sequential algorithmic steps. Some valid methods can compute them in another order; the grader accepts that freedom.

## Native r3 evidence

The following rows are read from raw result/reward/CTRF files, not taken from creator verdict summaries. Each named native test is a four-pencil batch. Author controls are not LLM attempts.

| Job / trial | Reward | Passed tests | Raw result |
|---|---|---|---|
| v020-r3-alternative / certified-pencil-structure__gQLZKsd | 1 | 12/12 | `authoring\reports\harbor-jobs\v020-r3-alternative\certified-pencil-structure__gQLZKsd\result.json` |
| v020-r3-hardcoder / certified-pencil-structure__Lzfjnt7 | 0 | 0/12 | `authoring\reports\harbor-jobs\v020-r3-hardcoder\certified-pencil-structure__Lzfjnt7\result.json` |
| v020-r3-mutant / certified-pencil-structure__8egCpYM | 0 | 0/12 | `authoring\reports\harbor-jobs\v020-r3-mutant\certified-pencil-structure__8egCpYM\result.json` |
| v020-r3-nop / certified-pencil-structure__V4tNL3Q | 0 | 0/12 | `authoring\reports\harbor-jobs\v020-r3-nop\certified-pencil-structure__V4tNL3Q\result.json` |
| v020-r3-oracle / certified-pencil-structure__6xyEy2H | 1 | 12/12 | `authoring\reports\harbor-jobs\v020-r3-oracle\certified-pencil-structure__6xyEy2H\result.json` |
| v020-r3-oracle / certified-pencil-structure__bPnnvbc | 1 | 12/12 | `authoring\reports\harbor-jobs\v020-r3-oracle\certified-pencil-structure__bPnnvbc\result.json` |
| v020-r3-partial / certified-pencil-structure__wtUcnmk | 0 | 0/12 | `authoring\reports\harbor-jobs\v020-r3-partial\certified-pencil-structure__wtUcnmk\result.json` |
| v020-r3-trivial / certified-pencil-structure__YfmY4ra | 0 | 0/12 | `authoring\reports\harbor-jobs\v020-r3-trivial\certified-pencil-structure__YfmY4ra\result.json` |

Both oracle repeats and the changed valid construction pass 12/12. Finite-only partial, non-reflexive inverse mutant, public-example hardcoder, shape-aware universal-zero-structure control (`v020-r3-trivial`) and no-op all receive valid zero rewards and fail 12/12. The literal constant-output baseline was tested separately in-process on all 48 pencils, not as that native trivial trial. Distinct CTRF names preserve the twelve batch results. Raw job checksums use Harbor's own algorithm; the independent file-manifest hash above is a different explicitly documented hash, not an attempted equality to Harbor's checksum.

## Discrimination across all 48 pencils

The suite's explicit easy cases are 000-003 and 030-031: six zero/scalar convention controls. The other 42 are structural cases. Three queries per pencil give 144 forcing queries. Constant and universal-zero guesses cannot pass the suite. The author numerical spectral-block heuristic fails 40/48, universal-zero structure is accepted only on the three genuine zero pencils, and literal constant output is accepted on 0/48. Numerical rank alone happens to be correct on all 48 and is honestly excluded as discrimination evidence. The sixteen output mutants test isolated semantic mistakes inside otherwise correct certificates, not independent full solvers or empirical model performance.

The table independently cross-references the detailed per-pencil author mutant records and additional heuristic results with the reviewer's own shape and alternative-acceptance results. An unchanged mutation passing an unaffected case is mathematically legitimate.

| Pencil | Role | Shape | Author semantic mutants rejected | Numerical spectral guess | Own alternative |
|---|---|---|---|---|---|
| case-000 | easy | [2, 3] | 7/16 | accept | PASS |
| case-001 | easy | [1, 1] | 7/16 | accept | PASS |
| case-002 | easy | [1, 1] | 4/16 | accept | PASS |
| case-003 | easy | [1, 1] | 6/16 | accept | PASS |
| case-004 | structural | [1, 2] | 8/16 | reject | PASS |
| case-005 | structural | [2, 1] | 9/16 | reject | PASS |
| case-006 | structural | [5, 5] | 10/16 | reject | PASS |
| case-007 | structural | [5, 5] | 10/16 | reject | PASS |
| case-008 | structural | [2, 2] | 9/16 | reject | PASS |
| case-009 | structural | [2, 2] | 7/16 | accept | PASS |
| case-010 | structural | [4, 4] | 9/16 | reject | PASS |
| case-011 | structural | [4, 4] | 7/16 | accept | PASS |
| case-012 | structural | [4, 4] | 6/16 | reject | PASS |
| case-013 | structural | [4, 4] | 6/16 | reject | PASS |
| case-014 | structural | [4, 4] | 6/16 | reject | PASS |
| case-015 | structural | [7, 7] | 14/16 | reject | PASS |
| case-016 | structural | [12, 12] | 15/16 | reject | PASS |
| case-017 | structural | [8, 9] | 15/16 | reject | PASS |
| case-018 | structural | [8, 9] | 11/16 | reject | PASS |
| case-019 | structural | [8, 8] | 10/16 | reject | PASS |
| case-020 | structural | [5, 5] | 14/16 | reject | PASS |
| case-021 | structural | [6, 6] | 14/16 | reject | PASS |
| case-022 | structural | [6, 6] | 13/16 | reject | PASS |
| case-023 | structural | [10, 10] | 15/16 | reject | PASS |
| case-024 | structural | [7, 7] | 13/16 | reject | PASS |
| case-025 | structural | [6, 6] | 13/16 | reject | PASS |
| case-026 | structural | [12, 12] | 15/16 | reject | PASS |
| case-027 | structural | [10, 10] | 14/16 | reject | PASS |
| case-028 | structural | [18, 18] | 15/16 | reject | PASS |
| case-029 | structural | [15, 15] | 14/16 | reject | PASS |
| case-030 | easy | [1, 18] | 7/16 | accept | PASS |
| case-031 | easy | [18, 1] | 7/16 | accept | PASS |
| case-032 | structural | [12, 12] | 15/16 | reject | PASS |
| case-033 | structural | [9, 8] | 15/16 | reject | PASS |
| case-034 | structural | [7, 7] | 14/16 | reject | PASS |
| case-035 | structural | [8, 8] | 10/16 | reject | PASS |
| case-036 | structural | [10, 11] | 14/16 | reject | PASS |
| case-037 | structural | [6, 6] | 11/16 | reject | PASS |
| case-038 | structural | [12, 11] | 15/16 | reject | PASS |
| case-039 | structural | [14, 13] | 14/16 | reject | PASS |
| case-040 | structural | [15, 15] | 15/16 | reject | PASS |
| case-041 | structural | [15, 15] | 15/16 | reject | PASS |
| case-042 | structural | [14, 14] | 14/16 | reject | PASS |
| case-043 | structural | [14, 14] | 14/16 | reject | PASS |
| case-044 | structural | [15, 15] | 15/16 | reject | PASS |
| case-045 | structural | [15, 15] | 14/16 | reject | PASS |
| case-046 | structural | [15, 15] | 14/16 | reject | PASS |
| case-047 | structural | [15, 15] | 15/16 | reject | PASS |

## All 67 supplied criteria

The full requirement text, rationale and exact evidence for each ID are in `independent_qc_criteria.json`. PASS is the reviewer's local judgment. The machine checks settle the static observations; this file does not pretend to supply two independent panel votes.

| Kind | ID | Result | Rationale / evidence |
|---|---|---|---|
| static | `entry-files` | PASS | All five required files exist. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=entry-files]` |
| static | `config-fields` | PASS | TOML parses; independent installed Harbor ALL lint returned []. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=config-fields]` |
| static | `task-fields` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=task-fields]` |
| static | `task-path` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=task-path]` |
| static | `task-structure` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=task-structure]` |
| static | `task-slug` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=task-slug]` |
| static | `task-readme` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=task-readme]` |
| static | `canary` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=canary]` |
| static | `task-absolute-path` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=task-absolute-path]` |
| static | `instruction-suffix` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=instruction-suffix]` |
| static | `instruction-similarity` | PASS | All 97 manifest hashes and saved-tree coverage verified; independently recomputed maximum instruction TF-IDF cosine 0.16791452110672503 < 0.8 (substantive 0.16450251628306747). Finite corpus only. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=instruction-similarity]` |
| static | `test-file-references` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=test-file-references]` |
| static | `dockerfile-references` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=dockerfile-references]` |
| static | `dockerfile-sanity` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=dockerfile-sanity]` |
| static | `dockerfile-platform` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=dockerfile-platform]` |
| static | `allow-internet` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=allow-internet]` |
| static | `separate-verifier` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=separate-verifier]` |
| static | `compose-host-binds` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=compose-host-binds]` |
| static | `task-timeout` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=task-timeout]` |
| static | `gpu-types` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=gpu-types]` |
| static | `task-resources` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=task-resources]` |
| static | `verifier-resources` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=verifier-resources]` |
| static | `nproc` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=nproc]` |
| static | `verifier-tooling-baked` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=verifier-tooling-baked]` |
| static | `trial-network-fetch` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=trial-network-fetch]` |
| static | `pip-pinning` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=pip-pinning]` |
| static | `pytest-version` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=pytest-version]` |
| static | `test-sh-sanity` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=test-sh-sanity]` |
| static | `binary-reward` | PASS | Independently reran the pinned upstream shell implementation in the existing offline Linux image; exit code 0. Source inspection found no conflicting behavior. Evidence: `authoring/reports/independent/independent_static_results.json#checks[id=binary-reward]` |
| rubric | `well_specified` | PASS | The public contract gives the executable, paths, exact encodings, complete output schema, limits and all-or-nothing scoring. Evidence: `instruction.md:6`; `environment/spec.md:6`; `environment/spec.md:62` |
| rubric | `test_instruction_alignment` | PASS | All thirteen stated scientific obligations map to named exact checker stages. No extra normalization was found; arbitrary valid alternatives passed. Evidence: `tests/constructive.py:38`; `tests/constructive.py:103`; `authoring/reports/independent/independent_probe_results.json` |
| rubric | `instruction_clarity` | PASS | The instructions state required outcomes and delegate detailed conventions to one solver-visible specification. The minimum-pole proof explains the certificate meaning without prescribing an implementation. Evidence: `instruction.md:4`; `environment/spec.md:66` |
| rubric | `structured_data_schema` | PASS | Case and forcing IDs, dimensional encodings, exact scalars, empty dimensions and ignored extras match the parser; own native positive and negative grammar probes passed. Evidence: `environment/spec.md:8`; `environment/spec.md:10`; `tests/harness.py:94`; `authoring/reports/independent/independent_runtime_results.json` |
| rubric | `typos` | PASS | Referenced runtime paths exist; subdiagonal companion, signs, transpose conventions and section cross-references agree with code and hand calculations. Evidence: `environment/spec.md:26`; `tests/constructive.py:15`; `solution/oracle.py:71` |
| rubric | `hint_discoverability` | PASS | Conditional applicability: no separate hint mechanism is supplied. Treating the public conventions as guidance, the block definitions, finite/infinite distinction, scalar grammar and certificate identities are discoverable. No private hint is required. Evidence: `environment/spec.md:22`; `environment/spec.md:28`; `environment/Dockerfile:6` |
| rubric | `scientifically_grounded` | PASS | Exact Kronecker/module classification, saturation and forced descriptor-system poles form a coherent symbolic linear-algebra workflow. Own proof audit validates the intrinsic denominator claim. Evidence: `environment/spec.md:4`; `environment/spec.md:66`; `authoring/reports/mathematical_correctness.md` |
| rubric | `scope` | PASS | The work is applied mathematics, specifically exact symbolic matrix-pencil and polynomial-module computation. Evidence: `task.toml:11`; `task.toml:12`; `instruction.md:4` |
| rubric | `essential_difficulty` | PASS | The hard steps are constant matrix-pair equivalence, polynomial splittings and local pole obstructions. Exact arithmetic, rather than arbitrary tolerance, is scientifically needed. Evidence: `README.md:28`; `environment/spec.md:36`; `environment/spec.md:62` |
| rubric | `novel` | PASS | The instance requires input-driven constructive computations. Independent pinned-corpus comparison is below threshold; this does not prove global code or mathematical novelty. Evidence: `authoring/reports/independent/independent_static_results.json`; `solution/oracle.py:99`; `authoring/reports/source_provenance.md` |
| rubric | `agentic` | PASS | A complete solver must compute matrix/polynomial invariants, construct and verify transformations, and generate exact forcing certificates over multiple fresh invocations. Evidence: `solution/oracle.py:99`; `tests/harness.py:68`; `authoring/reports/independent/independent_probe_results.json` |
| rubric | `verifiable` | PASS | Independent standard-library identity checks, expected canonical invariants and explicit lower-bound witnesses distinguish scientific mistakes from valid alternatives. Evidence: `tests/constructive.py:37`; `tests/exact.py:38`; `authoring/reports/independent/independent_probe_results.json` |
| rubric | `solvable` | PASS | Two native oracle runs each pass all twelve batches within process budgets. The input-driven reference imports no hidden generator, and independent transformed outputs pass all 48 pencils. Evidence: `authoring/reports/independent/independent_static_results.json`; `solution/oracle.py:10`; `authoring/reports/independent/independent_probe_results.json` |
| rubric | `outcome_verified` | PASS | Full-family independent alternatives passed with reversed block order, rational frame rescaling, nonconstant unimodular basis changes, high-degree duals/inverses/projectors/witnesses and kernel-added particular solutions. Evidence: `authoring/reports/independent/independent_probe_results.json`; `authoring/evidence/independent_probes.py:independent_alternative`; `authoring/reports/independent/independent_static_results.json` |
| rubric | `functional_verification` | PASS | The checker evaluates actual scientific identities. Native partial, resolvent mutant, example hardcoder, shape-aware universal-zero control and no-op receive reward zero; the literal constant baseline is rejected in-process on all 48. Evidence: `tests/constructive.py:68`; `tests/constructive.py:80`; `tests/constructive.py:102`; `authoring/reports/independent/independent_static_results.json`; `authoring/reports/additional_negative_controls.json` |
| rubric | `ground_truth_provenance` | PASS | Expected invariants follow known canonical blocks under explicitly tracked invertible integer shears/scalings. The reference instead computes Smith data from matrices; selected Hilbert nullities were independently recomputed. Evidence: `tests/cases.py:87`; `tests/cases.py:60`; `solution/oracle.py:38`; `authoring/reports/independent/independent_probe_results.json` |
| rubric | `graded_instances_discriminate` | PASS | The suite contains 48 pencils, with six disclosed easy controls and 42 structural cases. Per-case mutant records and separate zero/constant/numerical heuristics show discrimination; numerical rank alone correctly survives all cases and is not misrepresented. Evidence: `tests/cases.py:165`; `authoring/reports/control_audit.json`; `authoring/reports/additional_negative_controls.json`; `authoring/reports/independent/independent_probe_results.json` |
| rubric | `solution_quality` | PASS | The shipped oracle derives invariants and certificates from INPUT, never from IDs or expected data. The homomorphism-frame search checks both pair identities exactly. Its finite fallback is complete but has no practical worst-case guarantee. Evidence: `solution/oracle.py:99`; `solution/frames.py:59`; `README.md:32` |
| rubric | `do_not_modify_enforced` | PASS | The candidate runs from a root-owned copied source tree and cannot write that source, tests or reward. Protected source and symlink rules are explicit; own native assertions passed. Evidence: `tests/harness.py:54`; `tests/harness.py:29`; `instruction.md:6`; `authoring/reports/independent/independent_runtime_results.json` |
| rubric | `deterministic_reproducible` | PASS | Seeded matrices, forcings, opaque IDs and reproducible exact frame search produce repeated oracle successes. Both image bases and package versions are pinned. Evidence: `tests/cases.py:165`; `solution/frames.py:91`; `authoring/reports/independent/independent_static_results.json`; `environment/Dockerfile:2` |
| rubric | `separate_verifier_configured` | PASS | The manifest selects a separate no-network verifier, with its own baked dependencies and only the submission artifact handed over. Evidence: `task.toml:27`; `task.toml:30`; `tests/Dockerfile:5`; `authoring/reports/independent/independent_static_results.json` |
| rubric | `verifier_execution_isolation` | PASS | No candidate import occurs in the grader. Fresh subprocesses drop groups and UID/GID; tests/logs and source are inaccessible. Own native assertions verify the active image, whose checker file hashes match the reviewed package. Evidence: `tests/harness.py:71`; `tests/harness.py:27`; `tests/test.sh:7`; `authoring/reports/independent/independent_runtime_results.json` |
| rubric | `anti_cheat_robustness` | PASS | Runtime input is private and only public spec/examples enter the agent image. Fresh offline UID-limited processes, exact certificates and failed no-op/hardcoder/constant controls prevent observed shortcuts from full reward. Evidence: `authoring/reports/independent/independent_runtime_results.json`; `tests/harness.py:44`; `authoring/reports/independent/independent_static_results.json` |
| rubric | `task_security` | PASS | No runtime credentials, provider integrations, host binds or unexplained external operations were found. The verifier has no network and candidate environment is rebuilt from an allowlist. Evidence: `tests/harness.py:59`; `task.toml:30`; `authoring/reports/independent/independent_runtime_results.json` |
| rubric | `resource_configuration` | PASS | The 2 CPU/4 GiB environments, 2 GiB candidate process limit, 180-second invocation budget and 3600-second verifier budget comfortably cover measured native solutions. General worst-case runtime remains unproved. Evidence: `task.toml:31`; `tests/harness.py:23`; `tests/harness.py:74`; `authoring/reports/independent/independent_static_results.json` |
| rubric | `task_toml_schema` | PASS | Independent installed-Harbor all-rule lint returns an empty issue list, TOML parses, and all required metadata/settings pass the pinned local profile checks. Evidence: `authoring/reports/independent/independent_static_results.json`; `task.toml:2`; `task.toml:10` |
| rubric | `environment_hygiene` | PASS | Independent inspection of the actual agent image finds exactly spec.md and data/examples.json under /app, pinned math packages, and no oracle/test/solution exposure. Evidence: `authoring/reports/independent/independent_runtime_results.json`; `environment/Dockerfile:7`; `environment/requirements.txt:2` |
| rubric | `artifact_efficiency` | PASS | Only /app/submission transfers; each invocation copies it into fresh read-only source/work locations, rejects symlinks, and requires a newly created output. Regular helpers in cache-named directories remain usable. Evidence: `task.toml:3`; `tests/harness.py:47`; `tests/harness.py:39`; `authoring/reports/independent/independent_runtime_results.json`; `authoring/reports/independent/independent_static_results.json` |
| rubric | `ctrf_reporting` | PASS | All twelve discrete tests have distinct names and raw CTRF records. Each is a four-case batch, so CTRF is not per-pencil reporting; per-pencil author and reviewer files provide that finer evidence. Evidence: `tests/test_outputs.py:14`; `authoring/reports/independent/independent_static_results.json`; `authoring/reports/independent/independent_probe_results.json` |
| rubric | `task_authoring_dir` | PASS | Review scripts, trajectories, reports, controls and corpus are outside the active package under authoring/. Only the reviewer README remains as intended task documentation. Evidence: `README.md:32`; `authoring/reports/independent/independent_static_results.json`; `authoring/reports/independent/initial_findings.json` |
| rubric | `no_extraneous_files` | PASS | All 22 active files have runtime, configuration, image-build or reviewer-documentation roles. certificates.py supplies the parser/rank/basis primitives used by constructive.py; no report or cached answer is shipped. Evidence: `tests/constructive.py:4`; `tests/.dockerignore:1`; `authoring/reports/independent/initial_findings.json#file_sha256` |
| rubric | `reviewable` | PASS | Public definitions, canonical generator, exact checker, input-driven oracle, raw logs and reviewer-owned probes permit end-to-end tracing. Initial findings and unchanged hash establish the reviewed point in time. Evidence: `environment/spec.md:14`; `tests/constructive.py:37`; `authoring/reports/independent/independent_static_results.json`; `authoring/reports/independent/independent_probe_results.json` |
| rubric | `difficulty_explanation_quality` | PASS | README identifies why Smith-only, numerical, nonsaturated-basis and nonminimal-denominator approaches are insufficient, while disclosing easy controls and unmeasured frontier difficulty. Evidence: `README.md:26`; `README.md:28` |
| rubric | `solution_explanation_quality` | PASS | README correctly describes invariants, homomorphism-space frames, polynomial splitting, gcd cancellation and local pole witnesses; the implementation and own proof review support those claims. Evidence: `README.md:30`; `solution/oracle.py:127`; `solution/frames.py:98` |
| rubric | `verification_explanation_quality` | PASS | README identifies exact checks, independent expected data, valid alternative controls, negative mutants and process isolation, and explicitly excludes historical API interruptions from difficulty evidence. Evidence: `README.md:34`; `authoring/reports/independent/independent_static_results.json`; `authoring/reports/independent/independent_probe_results.json` |
| rubric | `category_and_tags` | PASS | Tags accurately identify mathematics, pencils, exact arithmetic, minimal bases and Smith form; metadata matches actual work. Evidence: `task.toml:9`; `task.toml:21` |
| rubric | `task_name` | PASS | certified-pencil-structure is a descriptive three-token kebab-case slug and the task name uses the required terminal-bench-science namespace. Evidence: `task.toml:5`; `authoring/reports/independent/independent_static_results.json` |
| rubric | `task_readme` | PASS | README header matches the manifest and its difficulty/reference/verification prose matches reviewed behavior. Claims of scientific difficulty are qualified by explicit calibration limits. Evidence: `README.md:2`; `README.md:26`; `README.md:30`; `README.md:34`; `authoring/reports/independent/independent_static_results.json` |

## Warnings and limits

- **W1:** Empirical difficulty for frontier models is unmeasured. Oracle, mutated and transformed controls are deterministic author/reviewer programs, not model attempts. Historical Gemini trials were infrastructure interrupted and supply zero verified graded successes, not scientific failures.
- **W2:** Originality is supported only against the pinned 97-instruction corpus and a limited saved code reference. It is not a web-wide plagiarism or mathematical-novelty proof.
- **W3:** The reference frame search has an algebraically complete finite fallback but exponentially large worst-case search space. Measured native shipped-family solvability is strong; a universal 180-second runtime guarantee is not established.
- **W4:** CTRF reports 12 four-case batches. A failed batch stops at its first failing pencil; per-pencil discrimination is therefore established by separate author/reviewer computations, not native CTRF alone. Numerical rank alone is correct on all 48 and provides no discrimination evidence.
- **W5:** This is one fresh-context AI reviewer opinion, not independent human domain review, a two-vote panel, an external QC service approval, publication readiness certification or frontier-model approval.

No confirmed defect required a package correction. No fix recheck is pending. A final byte-hash comparison confirms that the package reviewed here remains exactly the package first inspected. Any later active-file change invalidates that unchanged-package statement and requires a scoped recheck.
