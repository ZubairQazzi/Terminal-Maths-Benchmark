# Proposed five-trial-per-task calibration protocol

Status: **PENDING EXPLICIT USER APPROVAL. No new model trials started.** The user expressly requires approval for the Task 2 frozen-task repair and for five trials per task after resource/API review. Existing authorization for initial trajectories does not authorize this batch.

## Frozen targets and independence

- Task 1: original specificity-envelope v0.1.0, unchanged.
- Task 2: proposed transcript-provenance-audit v0.2.0 only after approval, versioned fixture construction, scientific/isolation QC and a new checksum manifest. Existing v0.1.1 is preserved.
- Five new completed trials per task; ten total. A single new Task 2 fixture is frozen before the cohort. This evaluates repeated model attempts on fixed tasks, not robustness across ten different datasets.
- Order: Task 1 trial 1, Task 2 trial 1, then the same alternating order through trial 5. One container/trajectory executes at a time. Every attempt has a new conversation and clean container; no prior commands, trajectories, oracle outputs, authoring directories or researcher hints are accessible. Do not reuse provider conversations/session IDs. Implicit provider prompt caching is accounting, not permission to supply previous answers.
- Same model and scaffold throughout: `gemini/gemini-3.5-flash-lite`, Terminus-2 2.0.0, Harbor 0.27.0, LiteLLM 1.110.2, XML parser, high reasoning, explicitly recorded temperature 1.0, 32768 output tokens per request, native turn allowance. Initial runs left temperature unspecified; the new setting is declared in advance rather than retroactively equated with an unverified provider default.
- Original task resources/timeouts remain: 2 CPUs; Task 1 8192 MiB, Task 2 4096 MiB; 10240 MiB storage per task; no GPU; 28800-second agent and 3600-second verifier limits. No artificial shortening of a scientifically valid attempt.

Fresh conversations plus stochastic sampling reduce answer carryover; they do not prove population-level statistical independence from a shared provider/model/infrastructure. Report this limit.

## Availability, retries and budget handling

Use the previously recorded transport-only policy: at least 20 seconds between provider request starts, at most five tries per call, bounded transient-error backoff, no nested retry multiplication. Permit at most one clean fresh restart per scheduled slot **only** for infrastructure interruption. Never retry a legitimate graded failure to improve its score. Preserve every attempt and exception. At most twenty fresh attempts for ten slots; resource allowance can stop the batch earlier.

Stop on daily/zero quota, authorization error or exhausted budget allowance. Pause before further usage rather than upgrading billing or falling back to another model. A provider failure, quota exhaustion or administrative budget stop is a censored attempt, not evidence of scientific failure. A genuine agent timeout at the unchanged task limit is classified separately and included as a valid failure only when native grading/policy supports a valid reward.

Before approved launch, read the available model metadata/current project quota/tier information where accessible and validate the exact task checksums. Do not infer a free account from a model's advertised free tier. Do not inspect or print key values. If account/quota information is inaccessible, disclose that and rely on bounded stop conditions; no silent billing changes.

## Resource and API estimate

Five-times replay of each completed historical run gives:

| Planning quantity | Task 1, five trials | Task 2, five trials | Total |
|---|---:|---:|---:|
| Input tokens | 2,745,595 | 2,075,590 | 4,821,185 |
| Output tokens | 120,660 | 86,655 | 207,315 |
| Cache-read tokens, subset of input | 2,324,840 | 1,414,140 | 3,738,980 |
| Agent steps / successful provider calls | 110 | 115 | 225 |
| Recovered provider errors, historical replay scenario | 85 | 20 | 105 |
| Wall minutes, including historical backoff | 80.42 | 49.55 | 129.97 |

This is a planning scenario from one completed run per task, not a confidence interval or a bound. The repaired Task 2 fixture and variable model/provider behavior may change usage. Plan roughly **3–5 hours including QC and availability delays**, with no guaranteed duration.

The published standard paid rates are $0.30 per million uncached input tokens, $0.03 per million cache-read tokens and $2.50 per million output tokens including reported thinking. The scenario costs approximately **$0.96 with the observed cache fractions, or $1.96 without cache discounts**. Free-tier input/output is advertised but actual project billing is unverified. These are text-token estimates, not receipts; no explicit paid cache storage, grounding or paid-only fallback is proposed. [Gemini pricing](https://aistudio.google.com/docs/pricing#gemini-3.5-flash-lite).

Proposed approval allowance: **$6 USD in estimated/accounted text API usage**, with planning guards at 12 million input tokens, 750,000 output tokens and 900 instrumented request attempts. At uncached listed text rates the token allowances correspond to $5.475. Check guards before provider calls, reserve the next request's output allowance and pause when insufficient. An interrupted attempt is censored, never counted as model scientific failure merely because a guard stopped it. This is not a guaranteed invoice cap: error-side consumption, provider tokenization/cache billing, taxes and account settings can differ. Request new approval before expanding the allowance or changing provider/model. No billing upgrade is authorized by accepting this plan.

Current F free space was about 72.76 GiB; reserve 10 GiB for new project files, versioned fixtures, logs and caches. Existing full packages are approximately 191 MiB and 225 MiB; the entire initial trajectory batch is approximately 83 MiB, so the reserve is conservative for host artifacts. Observed Docker capacity is about 15.47 GiB memory and 20 CPUs; serial 8/4 GiB workloads fit. These are observations, not guaranteed peak memory measurements.

All new project files, versioned packages, artifacts, trajectories, temporary files and configurable host caches will be rooted on F. Use the prior F-drive cache setup without repurposing HOME. Existing tool installations remain where installed. Docker Desktop's existing virtual disk/container scratch was previously on C and is not relocated by this proposal; literal F-only engine storage would require a separate engine relocation decision. No global engine settings are changed without approval.

## Reporting and analysis fixed before outcomes

Record each scheduled slot, every infrastructure attempt, model/version/task checksum, original command/configuration, binary reward, all eleven individual check outcomes/durations, verifier pass rate, wall and agent/verifier execution time, agent steps/tool calls, provider-request counts/errors/retries and native/provider token fields. Preserve submitted artifacts and terminal observations. Keep provider-reported cache/partial reasoning counts separate; never add them to total tokens twice. Preserve raw sanitized exceptions and operational errors.

For each task report the success rate `successful completed trials / valid completed trials`, requested/completed/censored counts and a 95% Wilson interval with small-sample limitations. If fewer than five valid trials finish within allowance, report the actual denominator and seek additional approval rather than inventing five outcomes. At n=5, even uniform success/failure is weak evidence about broader difficulty. Do not combine Task 2 v0.1.1 with v0.2.0. Keep historical initial results separate; Task 1 pooling, if shown, is secondary and clearly labeled.

Classify failures using executed artifacts and checks, with a primary cause and optional secondary tags: biological/design reasoning, statistical inference/null semantics, numerical precision, implementation, instruction/schema/units, parser/terminal operations, infrastructure, and administrative quota/budget censoring. A binary zero does not by itself identify the category. Describe central scientific checks separately from audit/schema checks as descriptive results, without replacing or silently relaxing the official all-checks-required binary reward.

Preserve every old version and trajectory. Never alter checks, inputs, thresholds or constraints in response to the new outcomes. Report recommendations as retain/improve/reject with evidence and qualification; do not claim extreme difficulty from this single model and small cohort.
