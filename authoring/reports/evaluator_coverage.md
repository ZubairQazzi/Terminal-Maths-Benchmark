# Evaluator coverage and independence

Current portable execution: authoring/reports/local_validation_v013.json, success=true. Real final Docker/Harbor execution is separately recorded in harbor_validation.md.

The graded suite contains 36 exact pencils in nine four-case subprocess invocations, within the public bound of twelve. It includes:
- Zero rectangular pencil and degree-zero left/right directions.
- Regular finite and constant/infinite pencils; finite zero versus infinity.
- Tall and wide pencils; left/right indices through degree four.
- Repeated real and irreducible quadratic primary factors; identical spectra/determinants with different block partitions.
- Rational finite factors with cleared-denominator integer inputs.
- Infinite blocks and different partitions of the same total infinite degree.
- Mixed finite, infinite, and both singular structures.
- Eight seeded randomly selected valid block combinations.
- Constant invertible row/column mixing and large exact scalings.
- Transpose and spectral-translation metamorphic pairs.

Expected invariant factors are assembled from primary powers with standard-library rational polynomial multiplication. The grader does not import the oracle, SymPy, or any candidate module. Polynomial nullspace identities and leading ranks are independently recomputed. A local normal-rank cross-check samples at min(m,n)+1 points; polynomial minor degree bounds make this exact.

The actual candidate process is called with the public input/output contract. Duplicate/missing ids, invalid rational types, wrong dimensions, wrong rank, finite factors, infinity sizes, minimal degrees, forged identities, and dependent leading vectors are rejected. Extra result keys and alternative basis normalizations are accepted.

Portable negative controls executed: wrong rank, wrong finite factor, wrong infinite sizes, wrong right and left degrees, forged certificate, float scalar, boolean rank. A genuinely rescaled correct basis was accepted. Broken all-zero and plausible finite-Smith-only programs were both rejected. A fresh invocation reproduced acceptance. See raw JSON for results and durations.

Real container checks have now passed; their evidence is separate from the portable harness: complete hidden pytest/CTRF execution; reward creation; permission and subprocess-limit enforcement; no-op oracle infrastructure checks; image-layer leakage checks; clean reset and rerun. The local portable mode deliberately does not pretend to enforce Linux UID/resource isolation. Finite sampled testing cannot prove behavior on every valid input; edge coverage is explicit rather than claimed exhaustive.



Final v0.1.3 execution-contract evidence: the independently reproduced supporting-executable rejection was corrected and a correct helper-based submission now passes 9/9 native tests. Both oracle repeats also pass 9/9, no-op 0/9, partial 1/9. Final isolation_probe_v013.json and agent_leakage_probe_v013.json pass. The copied program tree is root-owned/read-only to the candidate, with executable helpers; fresh work/output directories are writable. CPU/address-space/file limits are per process and file, as stated in the public spec. The suite includes 1x18 and 18x1 zero pencils, dimension 18 mixed structure, infinity size six, and higher-degree finite factors.
