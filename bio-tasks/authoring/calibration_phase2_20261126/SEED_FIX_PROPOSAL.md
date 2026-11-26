# Task 2 predictable-generation repair proposal

Status: **DRAFT — approval required before any frozen-task change or new fixture generation.** Proposed new version: v0.2.0 in `F:/rl/bio/versions/biology-task-2-v0.2.0/`. Existing v0.1.1 and all historical runs remain untouched.

## Threat and root cause

The old authoring function defaults to `np.random.default_rng(273600)`, the public accession digits. Its single deterministic stream generates the atlas permutation/scales and subsequent donor choices, pair fractions, assay noise and query permutation. With known or guessed generator conventions, accession replay recovers labels and weights without expression inference. The previous seed-only probe passed 7/11 check families but received reward 0 because its invented physical and numerical certificates were wrong. This partial rejection does not make the generation scheme robust: an attacker could obtain correct support cheaply and compute the remaining certificates from those supports, bypassing support discovery. No full such attack is asserted to have been executed.

The threat model assumes the generator source and all scientific distributions are public. Security must not depend on hiding NumPy draw order. Merely replacing the accession with another public constant, timestamp, hash, UUID with little entropy or a secret-seeded non-cryptographic PRNG is not the recommended repair. Public atlas/scaling draws should not be usable to reconstruct later planted truth.

## Proposed implementation

Use Python's OS-backed `secrets.SystemRandom` for **every** fixture-generating draw. Remove the seed parameter and seed field. The proposal provides NumPy-compatible `permutation`, `uniform`, `integers` and `normal` methods; permutations use the standard system-random shuffle, integers use unbiased system-random range selection, and Gaussian transforms use system-random uniforms. No new cryptographic primitive is invented. Python documents `secrets` for secure randomness and distinguishes it from simulation PRNGs: [Python secrets](https://docs.python.org/3/library/secrets.html).

Archive the complete drawn values in an immutable **private** replay record outside the entire runnable task tree and both Docker build contexts. It is answer-bearing material. Never ship it as provenance, seed, image build argument/environment variable, Docker layer, agent volume, model prompt, source-only release or public audit log. Actual planted truth remains only in the separate verifier as required; the replay record is not needed by either runtime image. Exact fixture files and their hashes define the frozen benchmark instance. Authorized maintainers can rebuild with the private record and pinned software; a replay-sequence mismatch must fail rather than fall back to fresh randomness.

Explicit source, metadata, destination, truth, protected-root and private-record paths replace implicit writes. Generation refuses existing nonempty destinations and protected old package/history paths. Truth must be outside the agent build context. New image tags and package/checksum manifests distinguish v0.2.0.

The unchanged scientific design is 120 source identities and 24 queries, with 6 pure, 12 pair and 6 unsupported-three-source cases; the same source data, donor admissibility rules, pair fraction distribution, Gaussian perturbation distribution, normalization, gene splits, fitting problem and category thresholds. Models still infer from expression values. One private fixture is frozen for all five trials; trial-to-trial randomness is model sampling, not new scientific instances.

## Additional narrow quality changes

The reviewable diffs clarify that `atlas_minimum_by_column` measures the supplied scaled `atlas_tpm.tsv.gz` before normalization. They make the four published numerical absolute-tolerance comparisons inclusive and add a useful raw-minimum failure message. Scientific thresholds, the all-checks-required reward, sample counts, schemas, resources and timeouts are unchanged. Task 1 is unchanged.

Draft artifacts are under `proposal/`: the secure RNG component, proposed builder, and four unified diffs. These are **not** applied to either frozen package. Tiny public component checks demonstrate valid permutations, exact replay, mismatch rejection and exclusion of private records from an example agent context. They are not task QC or a cryptographic proof.

## Acceptance gates after approval, before model trials

1. Build exactly one new private fixture using OS randomness; record source hashes and version before model evaluation. If scientific QC fails, report the defect and stop; do not search fixtures for model failure.
2. Independently recompute identities, weights/support adequacy and disjoint-gene residuals from the new visible data. Confirm all old scientific tolerances/categories and complete schemas. Preserve original distributional settings.
3. Run two deterministic oracle repeats, an independently implemented equivalent solver, existing incorrect/empty/constant controls, renamed/permuted inputs and mismatched old-output controls through the native separate verifier.
4. Re-execute accession-seed reconstruction against the new fixture. Report actual mapping/donor agreement and verifier outcomes, rather than declaring security from a single failed guess. The architecture, absence of seedable state and context exclusions are the main defense.
5. Inspect actual agent/verifier build contexts, image files/layers, visible metadata, mounted paths and logs for any replay record, seed, map, donor truth or oracle outputs. Run solver as UID1000 with immutable inputs, no credentials and no private authoring mounts.
6. Freeze and hash v0.2.0 and run all five model trials on those exact bytes. Do not modify inputs or checks after seeing results. Document any public-source matching risk that remains; no scheme can promise universal attack resistance.

Existing copies and all historical results are protected by `preservation_manifest.json`. Approval authorizes creating a separate version; it does not authorize overwriting the original packages or publishing datasets.
