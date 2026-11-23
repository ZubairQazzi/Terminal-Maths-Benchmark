# Mathematics task calibration report

Task v0.1.3, unchanged: `99a8da66bc504372c791300e6504ce522f6453cd90ad40dc9ce0ab971ae02cbe`.
Model: **gemini/gemini-3.5-flash-lite**; installed native Terminus-2 **2.0.0**; parser **xml**.

Status: **SMOKE_IN_PROGRESS**. Valid calibration trials: **0/8**. Separate valid smoke: **0**.
Success/failure rates are undefined because no valid calibration trial has completed.

Target assessment: **NOT DETERMINED: fewer than eight valid trials.**

The smoke is excluded from the calibration denominator. HTTP errors and interrupted infrastructure runs are excluded. No missing trials are invented. Eight observations have substantial sampling uncertainty and do not establish a population success rate.

| Phase / trial | Run | Result | Elapsed sec | Agent steps | Input / output tokens | Harness cost estimate USD |
|---|---|---|---:|---:|---:|---:|

Costs are native harness catalogue estimates, not invoices or proof of payment. The user-confirmed free-tier project is used, and no paid fallback or billing upgrade is authorized. Runtime model aliases and catalogue metadata are preserved; immutable backend revision pinning is not claimed.

Every trial uses a fresh native Harbor job/container, the identical task checksum, fixed model and agent configuration, and the protected separate offline verifier. Reference solution and hidden tests are not supplied to the agent. The mathematical task, reference solution and hidden evaluator were not modified.

## Per-attempt review

## Overall analysis

{
  "common_failure_patterns": "Pending completed trials and manual review.",
  "hardest_mathematical_concepts": "Not established by valid trajectories yet.",
  "recommendations": "Do not modify the task from infrastructure errors."
}

Full raw configurations, results, grader CTRF/pytest logs, submitted source artifacts, terminal observations, ATIF trajectories and transport events remain in the named batch directory. Earlier Hydrogen/Flash/3.6 configurations and interruptions remain separate and are not pooled. Connection evidence and official sources: connection_recovery.md.

Flash-Lite is a smaller fallback model. These measurements apply to this model/agent configuration and do not establish performance for unavailable frontier Gemini models. All-pass/all-fail samples must be investigated before proposing any difficulty change; no change is performed automatically.
