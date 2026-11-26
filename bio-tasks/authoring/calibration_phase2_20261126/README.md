# Next Biology calibration phase: review and approval package

Prepared 26 November 2026, Asia/Karachi. **Review/proposals complete; frozen-task modifications and ten new model trials await explicit user approval.** No new Gemini/provider API calls were made in this phase. Only offline counterfactual checks and a small public RNG-component exercise were run.

Read:

1. [Trajectory and failed-requirement review](TRAJECTORY_AND_REQUIREMENT_REVIEW.md): detailed error classification, ambiguity/strictness assessment and narrow offline corrections.
2. [Task 2 seed repair](SEED_FIX_PROPOSAL.md): OS-backed generation, private exact replay, concrete draft code/diffs and required QC.
3. [Rights and source-only acquisition strategy](DATA_ACQUISITION_AND_RIGHTS_STRATEGY.md): primary-source findings, unresolved permissions and proposed packaging boundary.
4. [Five-per-task protocol and budget](CALIBRATION_PROTOCOL.md): frozen targets, independence/retry rules, expected consumption, $6 allowance, storage and reporting.

Evidence: `historical_metrics.{json,csv}`, all individual historical check outcomes, executed-command/terminal-observation extracts, `counterfactual_results.json`, component selfcheck, `resource_estimate.json`, source-acquisition manifest and proposed cohort registry. Counterfactual copies pass 11/11 after only the identified corrections; official historical rewards stay 0.

Provisional recommendation: retain Task 1 as a rigorous statistical implementation/conditional-inference benchmark with qualified difficulty claims. Improve Task 2 before formal retention by removing predictable generation and clarifying scale/tolerance handling in v0.2.0. Neither observed failure establishes broad biological inability. Neither task is currently cleared for unrestricted public data/image redistribution.

The old direct/canonical packages and every initial-trajectory file are hashed in `preservation_manifest.json`. Re-running `inspect_evidence.py` checks preservation without overwriting the snapshot. Drafts under `proposal/` are not installed in a task or image; the public component selfcheck contains no RNA-seq fixture or planted task truth.

Approval requested under the user's explicit items 1 and 5: create the separately versioned Task 2 repair, run its stated QC, then five new Gemini trials each for Task 1 v0.1.0 and Task 2 v0.2.0 under the stated usage allowance. No publishing, external rights inquiry, billing upgrade, paid-only fallback or original-version overwrite is included. All new project files/caches are on F; existing Docker engine scratch storage is disclosed in the protocol.
