# Run this task with Harbor and your own model key

This is a self-contained v0.2.0 task. Extract the ZIP, then change into the extracted directory containing `task.toml`. The other mathematics task is not required.

Use Linux or WSL2 with a running Docker Engine/Docker Desktop Linux backend, Python 3.12 or newer, and uv. Install the host harness version used for local validation:

```bash
uv tool install 'harbor==0.27.0'
harbor --help
docker info
```

The archive includes digest-pinned Docker build files, offline Python wheels, the public specification/example, complete reference solution and evaluator. Docker still needs network access to pull the base image initially. Harbor may install the selected agent, and the selected model requires provider network access. The separate verifier itself is offline.

For example, choose a supported Anthropic model that your own account can access, and use Harbor's `claude-code` agent. Set the two placeholders locally in your shell; never commit a key or put it inside the task ZIP:

```bash
export ANTHROPIC_API_KEY='YOUR_OWN_ANTHROPIC_KEY'
export MODEL_ID='YOUR_SUPPORTED_ANTHROPIC_MODEL_ID'

harbor run \
  --path . \
  --agent claude-code \
  --model "anthropic/${MODEL_ID}" \
  --n-concurrent 1 \
  --n-attempts 1 \
  --jobs-dir ../harbor-jobs
```

This user-initiated command makes model API calls using the user's credentials and may incur provider charges. Packaging and publishing did not run it. For another provider, select a compatible Harbor agent, model identifier and corresponding credential variable from [Harbor's agent documentation](https://docs.harborframework.com/agents/pre-integrated-agents); replacing only the API-key value is insufficient.

For an optional local reference-solution check without an LLM API, run:

```bash
harbor run \
  --path . \
  --agent oracle \
  --n-concurrent 1 \
  --n-attempts 1 \
  --jobs-dir ../harbor-oracle-jobs
```

Harbor writes job results and verifier artifacts under the selected jobs directory. Inspect the actual trial result and `verifier/ctrf.json`; reward 1 requires every mathematical case. Task 2 has 42 cases and a 14,400-second overall verifier allowance. Task 3 has 44 cases and a 16,200-second verifier allowance. Each task declares two CPUs and 4 GiB RAM per environment, with an eight-hour agent development budget. Run one task at a time on a machine with enough total memory for its agent and separate verifier containers.

The source files under `solution/` and `tests/` are included for reproducibility. Harbor's task-defined image build and artifact handoff keep them out of the solving agent's image. Evaluate through Harbor rather than exposing the full repository checkout to the agent.

Local non-model validation passed. Frontier-model success rates remain unmeasured. No Gemini or other model-provider API trial was run during this publication work.

References: [Harbor quick start](https://docs.harborframework.com/getting-started/quick-start), [supported agents](https://docs.harborframework.com/agents/pre-integrated-agents), and [Terminal-Bench Science run instructions](https://github.com/harbor-framework/terminal-bench-science/blob/main/CONTRIBUTING.md).
