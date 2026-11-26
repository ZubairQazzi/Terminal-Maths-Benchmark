# QC Pipeline checklist

QC Pipeline reviews Harbor task packages with **29 static checks** and **38 automated rubric checks**. Static checks inspect task files before execution. The LLM judges use the task’s line-numbered files and available run evidence. A measured local result can settle a rubric check directly.

## Static checks

The Standard profile uses 27 upstream check implementations and two pipeline checks for required entry files and supported manifest fields. The Local profile applies its own publisher and identification marker. Check IDs match the IDs in QC reports.

### Task files and metadata

- **Required files** (`entry-files`). Check for `instruction.md`, `task.toml`, `environment/Dockerfile`, `solution/solve.sh`, and `tests/test.sh`.
- **Recognized settings** (`config-fields`). Parse the manifest and check its field names and table structure against the supported configuration.
- **Publication information** (`task-fields`). Check the publisher, task name, description, authors, keywords, and required metadata.
- **Folder matches the field** (`task-path`). Check that the task’s directory agrees with the domain and field in its manifest.
- **Folder layout** (`task-structure`). Check that instructions and configuration are at the root and that environment, solution, grading, and authoring files are in their expected locations.
- **Short task name** (`task-slug`). Check the folder name against the allowed format and length.
- **Reviewer guide** (`task-readme`). If a README is included, check its expected sections and whether its managed header matches the manifest.
- **Identification marker** (`canary`). Check that eligible source files carry the marker required by the active profile.

### Instructions and file references

- **Instruction paths** (`task-absolute-path`). Flag relative locations where the solver needs an absolute path to an input or deliverable.
- **Closing instructions** (`instruction-suffix`). Check the standard closing paragraph and compare its stated time allowance with `agent.timeout_sec`.
- **Similar wording** (`instruction-similarity`). Compare instruction text against the pinned main and lite task collections and flag close matches.
- **Files expected by the grader** (`test-file-references`). Look for submission paths shared by the tests and reference solution that are missing from the instructions or manifest.

### Container setup and isolation

- **Files copied into images** (`dockerfile-references`). Check that local sources referenced by supported `COPY` and `ADD` instructions exist in the build context.
- **Container build instructions** (`dockerfile-sanity`). Flag prohibited Dockerfile patterns that can make the image invalid or break packaging rules.
- **Processor settings** (`dockerfile-platform`). Flag `FROM --platform` settings that hardcode a processor architecture.
- **Network settings** (`allow-internet`). Check the solver and verifier network declarations against the active rules.
- **Separate grader setup** (`separate-verifier`). Check the verifier environment declaration and how the expected artifacts are handed over.
- **Host folder access** (`compose-host-binds`). Flag prohibited host-directory mounts in Docker Compose volumes.

### Time and computing limits

- **Time limits** (`task-timeout`). Check the configured timeouts against the standard rules and any additional local grader or build limit.
- **GPU requests** (`gpu-types`). Check GPU requests against the supported hardware types.
- **Solver resources** (`task-resources`). Check CPU, memory, storage, and GPU declarations against the package rules and any local caps.
- **Grader resources** (`verifier-resources`). Check that a separate verifier declares the resources it needs and flag suspicious differences from the solver’s allocation.
- **CPU usage** (`nproc`). Flag bare `nproc` calls that may count host processors and create too many workers.

### Repeatability and score output

- **Grader tools installed ahead of time** (`verifier-tooling-baked`). Check for dependencies that the verifier tries to install during grading.
- **Downloads during trials** (`trial-network-fetch`). Flag prohibited live network fetches in the inspected trial scripts.
- **Fixed Python package versions** (`pip-pinning`). Check that Python dependencies are pinned where repeatable installs require it.
- **Supported test tools** (`pytest-version`). When the task pins either test tool, check against the required versions `pytest==8.4.1` and `pytest-json-ctrf==0.3.5`.
- **Grading startup script** (`test-sh-sanity`). Check `tests/test.sh` for shell patterns and setup that conflict with grading conventions.
- **Binary reward** (`binary-reward`). Check score-writing code for patterns that can produce an invalid value in `/logs/verifier/reward.txt`. The grading contract uses `0` or `1`.

The dashboard supports additional local caps for grader time, solver-image build time, and solver and grader CPU and memory. Blank caps use the standard policy. The caps check the values declared in the task manifest.

## LLM judge checks

These 38 automated checks come from the pinned upstream task implementation rubric.

### The instructions

- **Clear deliverable** (`well_specified`). An independent expert can identify the goal, output path, format, grading metrics, and any convention or execution limit that changes the answer.
- **Instructions and tests agree** (`test_instruction_alignment`). Each scored requirement appears in the instructions, and the grader checks each promised requirement.
- **Clear, outcome-focused wording** (`instruction_clarity`). The instructions make the task easy to understand, give the necessary context, and state what the submission must achieve without giving away the method.
- **Structured output contract** (`structured_data_schema`). For structured submissions, the specified fields, types, and layout agree with what the grader reads.
- **Correct references** (`typos`). Names, paths, commands, and symbols point to the intended files or concepts.
- **Discoverable hints** (`hint_discoverability`). When a hint exists, its information can be traced to solver-visible evidence or established domain knowledge.

### The scientific work

- **Scientific grounding** (`scientifically_grounded`). The work reflects a real research workflow and produces a result useful for a scientific question or decision.
- **Scientific scope** (`scope`). The problem and deliverable fit the assigned domain and field.
- **Essential difficulty** (`essential_difficulty`). The challenge comes from the science or reasoning the solver must do. Formatting, repetition, and precision demands have a scientific purpose when required.
- **Novelty** (`novel`). The instance requires new reasoning or computation. The judge can use similarity findings to assess whether an earlier answer can be copied.
- **Meaningful tool use** (`agentic`). Reaching a correct answer requires work such as exploring data, testing a hypothesis, or running a computation.

### The answers and the grader

- **Verifiability** (`verifiable`). The grader can observe the required outcome and distinguish correct work from meaningful errors.
- **Solvability** (`solvable`). A correct approach can finish and pass using the data, tools, and resources available to the solver.
- **Alternative valid methods** (`outcome_verified`). A scientifically valid alternative can earn full credit by meeting the same result requirements.
- **Functional verification** (`functional_verification`). The grader checks the actual behavior or scientific output and catches answers that only look correct.
- **Ground truth provenance** (`ground_truth_provenance`). The expected values or scoring objective can be traced to their source, such as a generator, published data, or an independent calculation.
- **Discriminating test cases** (`graded_instances_discriminate`). Check per-case results from plausible trivial guesses when available, and account for any intentionally easy cases described in the documentation.
- **Reference solution quality** (`solution_quality`). The reference derives its answer from the supplied inputs, and reviewers can inspect the implementation that actually produces it.
- **Protected files** (`do_not_modify_enforced`). When the instructions protect a file, the verifier or execution boundary enforces that requirement.

### Reliable and safe runs

- **Reproducibility** (`deterministic_reproducible`). Builds and runs reproduce the expected data and score within the task’s stated rules for variation.
- **Separate verifier setup** (`separate_verifier_configured`). The verifier has the intended inputs and tools, including matching copies of any shared data required by both environments.
- **Submitted code isolation** (`verifier_execution_isolation`). When the verifier runs submitted code, the code cannot write the score, modify grading files, or read private answers.
- **Resistance to shortcuts** (`anti_cheat_robustness`). The grading setup and available controls show whether shortcuts can earn credit without solving the scientific problem.
- **Task security** (`task_security`). Build and runtime files avoid unsafe access to credentials, the host, and unrelated networks. Sensitive operations have a clear task purpose.
- **Resource suitability** (`resource_configuration`). Time, CPU, memory, storage, and other requested resources are reasonable and give valid approaches enough room to finish.

### The package

- **Manifest schema** (`task_toml_schema`). The manifest uses supported settings and supplies the naming, publisher, and metadata required by the active profile.
- **Solver image contents** (`environment_hygiene`). The solver image contains the needed tools and data. Reference solutions, private answers, and grading materials stay outside the solver’s view.
- **Artifact transfer** (`artifact_efficiency`). The verifier receives the files it needs, and collection handles failures without reusing stale outputs.
- **Individual test results** (`ctrf_reporting`). When the grader runs discrete tests, the review evidence shows the outcome of each applicable check.
- **Authoring material** (`task_authoring_dir`). Review-only material belongs in `authoring/`. Runtime files contain the material needed to build, solve, and grade the task.
- **Necessary files** (`no_extraneous_files`). Every shipped file has a required purpose or is covered by an exception in the rubric.

### Information for reviewers

- **Reviewability** (`reviewable`). Another reviewer can trace the assumptions, inputs, and calculations through to an expected result.
- **Difficulty explanation** (`difficulty_explanation_quality`). The documentation explains the specific scientific decisions that make the task challenging and where plausible simpler approaches fall short.
- **Reference explanation** (`solution_explanation_quality`). The documentation explains the reference approach and connects it to the implemented solution.
- **Verification explanation** (`verification_explanation_quality`). The documentation describes what the grader measures and why the checks suffice. Where the rubric requires it, calibration evidence shows how alternative correct methods and flawed methods scored.
- **Category and tags** (`category_and_tags`). The labels describe the actual science and methods clearly enough to find and group the task.
- **Published task name** (`task_name`). The name is descriptive and follows the active naming rules.
- **Reviewer README** (`task_readme`). When included, the README provides accurate, useful context and reflects the task as packaged.

## How QC decides the verdict

- The panel records a short reason and exact supporting citations for each verdict. Two valid failure votes can confirm the same issue when their wording differs. QC compares the cited facts and keeps distinct issues separate.
- A pass or a rubric-permitted exemption needs two agreeing votes and no conflicting vote, unless local evidence settles the check directly. Missing evidence or unresolved votes are marked **Needs review**.
- An upstream approval record gives judges context. Findings in the current review still require a concrete rule and supporting evidence.
- The overall result is **Fail** when a required check fails, **Incomplete** when required results remain unresolved, and **Pass** when all applicable required checks pass.
