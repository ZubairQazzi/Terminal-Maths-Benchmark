# Frozen Biology task source distributions

Publication date: 2026-11-26.

**These are source-and-local-acquisition ZIPs, not self-contained runnable Harbor
archives.** Unresolved data and wheel redistribution permissions prevent shipping
the complete payload. Each ZIP prominently documents this limitation and includes
a fail-closed, checksum-verified preparation script. Exact preparation currently
requires an authorized complete local frozen task. GEO downloads alone cannot
recreate all frozen fixtures. Do not run Harbor on the unprepared source directory.

| Task | Version | Scientific objective | Fresh offline reference/verifier | ZIP |
|---|---|---|---|---|
| Specificity Envelope | 0.2.1 | Relative-abundance specificity, parental equivalence and sensitivity to an absent early control; joint certificates and coupled robust envelopes. | 64/64, derived binary reward 1 | [Download](biology-task-1-specificity-envelope-v0.2.1.zip) |
| Transcript Provenance Audit | 0.3.1 | Cross-representation identity and technical-mixture provenance, assignment stability and complete sparse compatibility regions. | 63/63, derived binary reward 1 | [Download](biology-task-2-transcript-provenance-audit-v0.3.1.zip) |

## Contents and preparation

Both archives include unchanged frozen instructions, task.toml, README, environment
Dockerfile/requirements, reference solution algorithms and separate verifier code.
They exclude all data directories, derived/control/metadata payloads, wheel binaries,
Task 2 private evaluator truth, generation records, caches, credentials, logs and
trajectories. Complete per-file SHA-256 and size manifests identify the missing
payload explicitly. No altered scientific implementation or dummy input replaces it.

Extract the ZIP on Windows F: and read README_DISTRIBUTION.md. With Python 3.12+
run distribution/prepare.py --check: it must refuse the unprepared task. Supply
--frozen-source pointing to a lawfully held complete exact frozen version and
--output pointing to a new directory on F:. Preparation validates every input
before writing, refuses existing output and verifies the entire reconstructed
45-file / 51-file task against the frozen aggregate. It has no network, shell,
deletion, package installation or fixture-regeneration mode. Original frozen
copies remain unchanged. Original GEO acquisition URLs/checksums are provided
as provenance; they do not imply a complete public regeneration route.

## Validation evidence

See [VALIDATION_SUMMARY.json](VALIDATION_SUMMARY.json) and
[SHA256SUMS.txt](SHA256SUMS.txt). Packaging rechecked archive CRCs, safe extraction,
required Harbor components, exact versions, all included code hashes, complete
offline local restoration, Python AST/TOML parsing and frozen-source preservation.
The independent archive audit passed 12 checks per task, including refusal of
missing/tampered payloads, pre-existing output and C-drive output.

Fresh offline reference solutions and graders used existing pinned Docker images
with network disabled and the extracted/restored solution, data and verifier
directories mounted. Results were 64/64 and 63/63; the reward above is derived from
full pytest success, not a new native Harbor trajectory. Earlier frozen-version
native Harbor oracle and alternative runs each achieved reward 1; scientific
negative controls, boundary tests and environment isolation passed in that phase.
Fresh packaging tests do not claim to repeat that entire earlier QC suite.
No Gemini, external model, external QC model or model API was called.

## Permissions, isolation and known limitations

GSE273600 original matrices and related derivatives are not included because
unrestricted redistribution permission has not been established. The associated
cached publication's CC BY-NC-ND 4.0 label is not treated as a license for all
deposited matrices or derivatives. NCBI availability does not itself settle
third-party rights: https://www.ncbi.nlm.nih.gov/home/about/policies/ . Specific
wheel-binary redistribution/license review is incomplete, so only dependency
requirements and exact checksum metadata are published. No new blanket source,
dataset or third-party license is granted by this upload. Obtain rights clearance
before distributing hydrated tasks/images or transferring data to an external
model provider. External-provider processing permissions remain unresolved.

Task 2 exact fixed randomized fixtures depend on private generation records that
are deliberately excluded. Public-only reconstruction of its frozen bytes is not
established. Public TPM matching also provides a documented partial identity route:
a source-assisted identity-only complete submission passed 14/63 checks and received
reward 0. Of 49 controlled panels, 32 are conservatively counted as advanced after
excluding 9 intentional easy and 8 null-passing rejection controls. These are local
control results, not external model-difficulty measurements.

The public source intentionally contains solution/ and verifier algorithms for
review, as requested. Their files are absent from the agent Docker build context;
tests use a separate verifier image. A solver who can access this repository can
read reference algorithms, so public-source access must be excluded in a hidden
benchmark evaluation. No private answer vectors or fixture truth are uploaded.
Official human acceptance and empirical frontier-model difficulty are unmeasured;
no claim of extreme difficulty is made. Previous task versions and trajectories
are preserved locally and are not part of this publication.
