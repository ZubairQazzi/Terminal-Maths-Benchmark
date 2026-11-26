# Reviewer recheck log

Reviewer `/root/qc_a`, distinct from creator `/root/creator_a`. Initial findings are preserved in `independent_qc_review.md` and their status history is in JSON. **The interim review was incomplete pending native/static and completed baseline evidence; final closure is recorded below.**

**Final closing status: PASS WITH LIMITATIONS.** All material findings have now been resolved and independently rechecked. Pending statements in dated/interim sections below are preserved as history and are superseded by the final native-evidence section.

## Source remediation and local evidence recheck — 2026-11-25

- **A1 remains open.** Parent coordinator will supply actual Harbor builds/oracle/no-op/clean reset/artifact-transfer/isolation/resource results and exact 29 static results. Host pytest alone does not establish native compatibility.
- **A2 source coverage resolved.** `task/instruction.md:26,35` defines an explicitly synthetic eight-case panel on the transformed Y scale, with its own separate BY family and no biological interpretation. `task/tests/test_outputs.py:161-188` independently derives all effects, uncertainties and probabilities from triplicates. The known positive and null cases exercise both certificate branches and zero-SE conventions; the minimum-effect boundary is noncertified. The real-data all-q1/all-false result is retained and documented. `oracle_output/calibration.tsv` has positive-case p_joint=1.637993e-6 and q_joint=1.187155e-5, a difference well outside the stated 2e-7 tolerance; BY is now numerically discriminating in the panel. Complete measured incorrect-control outcomes still await the running sweep.
- **A3 resolved.** `authoring/evidence/alternative_solver.py:9-85` constructs a 120×40 incidence matrix, computes group residual variance through matrix products, derives effects through contrast matrices, uses SciPy BY, and enumerates four early control corners. It imports neither oracle nor evaluator. Independent alternative and oracle logs/CTRF both show **11/11 pass** (`alternative.log`, `oracle.log`). Reversed gene/treatment/time row order is accepted. This is independent equivalent computation of the prescribed estimand, not agreement of unrelated inferential targets.
- **A4 documented accurately.** `authoring/reports/test_discrimination_audit.md` and `task/README.md:46` call fixed interpretation fields context checks; they do not count as proof of understanding or advanced biological difficulty. Monotonicity is also identified as a redundant invariant. Synthetic controls are numerical calibration, not extra biological samples.
- **A5 resolved.** `task/instruction.md:37` now requires six named regular data deliverables without promising rejection of harmless extra directory entries. This agrees with the named-artifact parser.
- **Additional README drift resolved.** After new controls, README initially retained five artifacts/ten tests and described the old summation-only variant. The reviewer raised this and re-read `task/README.md:44-46`: it now accurately states six artifacts, eleven test families and the independent incidence/matrix alternative. Both affected rubric IDs are locally PASS.

## Independently inspected data evidence

Both shipped count copies hash to `51f64fd0c058c60ab1c0f2c76a35ba00567d36baf06c9313b3b3dda8e42eab86`; both TPM copies hash to `40cc660c3e565e5070bd7e9ec6858bf348cc5e77188c99112d7239a38c940a2f`; solver/verifier/shared metadata copies hash to `9d30a73eb7950c4ce2bd1468f5bdc4683643976c10a94bb91b5018032eef2e65`. Synthetic input copies also match. Direct decompression and title/GSM reconciliation of original SOFT found 120 sample records, 120 exact metadata-title matches, 40 groups of size3, and zero untreated2h records.

A separate streaming audit of oracle artifacts found20,803 eligible genes and249,636 matched rows. All real q_joint values are1 and all certificates false. Nevertheless,89,598 interaction probabilities,89,578 parental-equivalence probabilities,52,932 minimum-effect probabilities and6,018 joint probabilities are below.05. There are82,500 joint probabilities below1. Early classifications are nonconstant: at expansion0 there are331positive and91negative ranges; at.3 there are23positive and6negative; at.6 there is1positive. Remaining ranges are unresolved. These observations substantiate numerical discrimination potential; they are not a substitute for actually measured flawed methods.

## Remaining limits

Native Harbor and exact static evidence have not yet been inspected, full baseline sweep is running, and model difficulty calibration is not authorized. Do not report final independent PASS or external QC approval from this interim report. The dedicated 38-ID rubric audit is complete as a review inventory, with untested evidence explicitly marked.

## Subsequent static/build/isolation/control evidence recheck

The earlier pending-evidence statements above are historical. I have now directly inspected:

- `static_qc.json`:29distinct exact checklist IDs, allPASS. `upstream_static_v010.json` contains26pinned shell invocations, every exit0; actual Harbor0.27 `lint --select ALL --json` returns`[]` exit0. The remaining entry/schema/similarity checks are explicitly recorded. The pinned rawsimilarity check's80% threshold is separate from the project's substantive30% investigation.
- Both `clean_build_*_v010.log` commands use`docker build --no-cache`, end exit0, and take52.329s/59.296s. This is actual clean-image evidence, not a Python syntax check.
- `isolation_v010.json` records executed assertions: solverUID1000; no`/tests` or`/solution` in public image; root-owned data append denied; submission writable; private verifier directories700; no preexisting reward; blocked network egress. Reference executes entirely offline under2CPUs/8GB in19.672s. The oracle mount in this author-only probe is explicitly read-only and does not appear in the ordinary solver image.
- `test_results_summary.json` and individual local CTRF/log evidence show oracle11/11 and independent alternative11/11. All9incorrect controls return binary0: no-op0/11, constant7/11, short hardcoded list6/11, labelshift7/11, wrongcontrast10/11, omittedadjustment10/11, saturatedshortcut10/11, incomplete7/11, invalidinterpretation10/11. Wrongcontrast fails effects; omittedadjustment fails correction. The saturatedshortcut fails solely test11, with q-error up to1, demonstrating that the added synthetic panel rejects the otherwise passing all-q1/all-negative shortcut. Fixed-context interpretation rejection is counted as a context control.
- I independently recomputed hashes for all40files in the canonical package, their user-facing task originals and`package_manifest.json`; there are no mismatches. I also independently hashed every one of the6fresh repeated output artifacts against its original and recorded checksum; all agree. This verifies the reviewed source is the staged/runtime source and confirms the reported byte repeatability.

The source/input/control findings are resolved. **A1 remains open solely for completed actual Harbor batch, separate-image transfer/reset and final native score evidence**, which the coordinator is running sequentially. Local evidence is not substituted for that final integration gate.

The raw35.6906%/37.2336% cross-task TF-IDF and98.9149%/99.1936% generic AST-histogram signals were also independently investigated and retained in `conceptual_review.md/json`. All22shared rawfive-word passages were enumerated; they concern requiredsuffix, publicsame-experiment/DmrPERK facts and artifact paths. Task objectives, statistics and evaluators remain distinct after the predeclared exclusions. No cosmetic wording change was made or requested.

## Additional control-provenance finding

**A6 — OPEN validation coverage:** source inspection of `authoring/evidence/validate_local.py:51-53` and `prepare_native_controls.py:40` shows that the existing `label_shift` mutation shifts numeric result fields by one gene row. It is a valid gene/result-association control, but it does not actually permute sample labels or metadata. The original project brief explicitly requests a wrong sample-label alignment baseline. The coordinator and creator have been asked to preserve the existing control with accurate scope and add a true metadata/sample swap control, recompute its output, and show evaluator rejection. This is an authoring-evidence gap rather than a new defect in the task's formulas or evaluator. A1 also remains open for completed valid native trials; Docker HTTP500/preflight incidents reported by the coordinator are infrastructure failures and must not be counted as scientific baseline rejections.

## True sample-alignment control recheck — A6 resolved

I independently inspected `wrong_sample_alignment.py`, its source and derived metadata, provenance, recomputation log, six full output files, and evaluator log/CTRF. Comparing metadata by GSM found exactly **24 changed sample-ID assignments**, no changes to the other fields, the same set of **120 distinct sample IDs**, and **40 groups of three**. Dmr-PERK Dim and UT assignments are exchanged at each matched time. The original metadata hash remains `9d30a73e…eef2e65`; the derived metadata hash is `593cbee6…d35aaf`, both matching provenance. I independently rehashed both original/derived matrices: counts remain `51f64fd0…eab86`, TPM remains `40cc660c…40a2f`.

The generation log executes the unchanged reference against the derived metadata directory rather than mutating scientific output rows. All six artifacts are present. A spot check of the first Dim 4h row confirms exactly the expected sign reversal of its Dmr effect, −0.342971647932148 to +0.342971647932148, with the parental effect unchanged. The original evaluator using correct private metadata reports **7/11 pass, 4/11 fail**, specifically tests 04, 05, 06 and 08. Thus a genuine sample-label misalignment is detected independently of the older gene-row shift. A6 is closed; local evidence now includes **ten** incorrect controls with binary zero. The native run for this added control is still part of the remaining A1 integration gate.

The generated plagiarism report was also directly inspected. It preserves the 25% maximum substantive rating, the raw 35.6906% warning, the earlier duplicate-reference result, and the limitations of AST histograms and adjusted lexical scores. The latest evaluator code metrics are 99.3022303% AST cosine and 0.2780868% token Jaccard; earlier snapshots remain historical. No task wording was altered for similarity screening.

## Final native-evidence recheck — A1 resolved

I directly opened the actual result, reward and CTRF files for every one of the **13 valid native trials**, rather than relying only on the summary. Every valid result has `reward_valid=true`, no exception, `verifier_environment_mode=separate`, an exact binary reward file consistent with its result, eleven named CTRF results, and the same frozen task checksum `38e6e643672a56ff4e2d30619b0ec5ccdfa6bcfd75d80cd79c099159ea26ae36`. I rehashed all **81** recorded artifact files and found **zero mismatches**. Both native oracle artifact maps match exactly. The no-op artifact directory contains only `manifest.json`, confirming an empty handoff rather than stale oracle reuse.

| Native case | Reward | Actual CTRF pass/total |
|---|---:|---:|
| Oracle, first clean trial | 1 | 11/11 |
| Oracle, second clean trial | 1 | 11/11 |
| Independent alternative artifacts | 1 | 11/11 |
| No-op | 0 | 0/11 |
| Constant | 0 | 7/11 |
| Hardcoded short output | 0 | 7/11 |
| Incomplete output | 0 | 2/11 |
| Invalid interpretation | 0 | 10/11 |
| Gene-row shift | 0 | 10/11 |
| Omitted correction | 0 | 10/11 |
| Saturated-output shortcut | 0 | 10/11 |
| Wrong contrast | 0 | 10/11 |
| Genuine sample-label misalignment | 0 | 7/11 |

The independent alternative was computed by its separate authoring implementation and its data artifacts uploaded for native grading; this is acceptance of equivalent scientific output, not a claim that the alternative computation itself was run by a model inside Harbor. The oracle trials actually execute the reference in the solver environment. These deterministic controls are not empirical AI-agent attempts.

The earlier invalid no-op trial has an actual Docker egress-sidecar startup HTTP500 exception and no valid score/CTRF. The nine preflight interruptions likewise did not produce scientific trial outcomes. They are preserved and excluded, and valid bounded retries now cover every required case. They are not counted as biological failures or baseline rejections.

The valid-order regression is additional positive evidence: fixed seed `27360020261125` independently shuffles count gene/sample orders, TPM gene/sample orders and metadata rows. Its inspected script checks keyed string-token preservation for every matrix row; provenance hashes match the retained original/derived inputs. I independently rehashed both permuted matrices, all six output files, and the 40 frozen runtime files without mismatch. The unchanged original evaluator's actual CTRF has **11/11 pass** and the log reports success. This is storage-order invariance of the same experiment, not a new biological replicate or model calibration.

The creator/coordinator remediation report accurately records the dispositions. A wording precision was requested for its A2 row: the reviewer inspected independent calibration derivation/output and agreement, rather than executing a separately written full calibration implementation. The final originality report correctly preserves this review's source rationale and raw metric limitations.

**Final result:** A1 and A6 are closed; A2/A3/A5 were corrected and rechecked, and A4 is retained as an explicit limitation. No material finding remains. The final 38-ID audit contains **37 PASS and one nonblocking difficulty WARNING**. External automated QC and Gemini/provider evaluation remain **NOT RUN**; empirical expert/model difficulty remains **NOT MEASURED**. This is a local independent sign-off, not an external certification.

