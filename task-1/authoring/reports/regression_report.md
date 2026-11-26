# Full regression and validation results

| Check | Actual result | Evidence |
|---|---|---|
| Complete exact oracle/checker | 48/48 PASS | Final source per-file hashes and per-case timings: core_final_validation.json |
| Unseen regenerated inputs | 40/40 PASS | Two new seeds with opaque ids; regenerated_inputs.json |
| Additional public boundaries | 3/3 PASS | Infinity 8, both indices 8, maximum entry/forcing magnitudes; boundary_probes.json |
| Author changed valid certificates | 48/48 PASS | control_audit.json; includes nonconstant basis changes, changed inverse and particular solutions |
| Independent mathematical probes | 280/280 PASS | independent/independent_probe_results.json |
| Independent live verifier probes | 5/5 PASS | independent/independent_runtime_results.json |
| Final clean Docker builds | 2/2 images PASS | validation/r3-clean-*-build.log, with F: storage preflight |
| Native final-checksum trials | 8/8 expected results; 0 exceptions | Two oracle PASS, alternative PASS; partial/mutant/example/no-op/zero controls reward 0 |
| Fresh environment resets | 2/2 PASS | image_probe.json |
| Permission/network/resource/symlink boundary | PASS | isolation_probe.json |
| Scalar and required-field regressions | PASS | contract_regression.json; native and independent format probes complement this |
| Original/frozen preservation | 1426 files each, 0 differences | final_preservation.json |

Native CTRF contains 12 distinct four-pencil batches, not 48 individual native test records. A failed batch stops at its first incorrect pencil. Separate exact per-pencil reports establish the remaining case-specific evidence. Correct numerical ranks are accepted: numerical rank alone has 0 rejections; the numerical spectral-block approximation has 40. No infrastructure error or deterministic author control is counted as an LLM failure.
