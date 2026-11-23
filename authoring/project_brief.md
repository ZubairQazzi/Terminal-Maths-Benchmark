# Governing user update: local-only deliverable

Objective 12 and all GitHub publishing deliverables are removed. Exactly one complete Harbor-compatible Mathematics task, supporting files, research, originality checks, hidden evaluator, real Harbor validation, Gemini trajectories, eight-trial calibration, and QC evidence are required locally. No remote repository, commits, pushes, publishing, registry uploads, or hosted submissions are permitted. Ask before installations and execution. Reference research is browser-only by the user's explicit choice. No changes to the original attachment are made; this is the amended local working brief.

# PROJECT: CREATE ONE EXTREMELY DIFFICULT MATHEMATICS TASK FOR TERMINAL-BENCH SCIENCE

## 1. YOUR ROLE AND PRIMARY OBJECTIVE

Act as a senior computational mathematician, mathematical research scientist, Terminal-Bench Science benchmark engineer, Harbor specialist, AI agent evaluator, and quality assurance auditor.

Your objective is to **design, implement, test, calibrate, and package ONE original, research-level Mathematics benchmark task** for autonomous terminal-based AI agents.

**Domain: MATHEMATICS ONLY.**

This is not a Reinforcement Learning, machine learning, or ordinary software debugging task.

The mathematical reasoning must be the central challenge. Programming, numerical computation, and terminal tools should support solving the mathematical problem, not replace it.

The task must be difficult enough to expose weaknesses in advanced coding agents while remaining objectively solvable.

**Target success rate: approximately 40–60% across 8 independent attempts using the same advanced agent and model.**

Aim for 4 successes out of 8. Because the sample is small, 3–5 successes can be considered a reasonable calibration range, but report the exact observed percentage.

Do not artificially manipulate difficulty, evaluation results, or environmental reliability to achieve this target.

**IMPORTANT: Actually create the complete working task. Do not stop at explaining an idea or writing a proposal.**

---

## 2. STUDY THE EXISTING TERMINAL-BENCH SCIENCE TASKS

I have provided screenshots and supporting materials from Harbor Hub.

Repository/dataset:

`terminal-bench-science/terminal-bench-science`

Reference tasks:

1. `terminal-bench-science/mendota-ice-phenology`
2. `terminal-bench-science/cilia-segmentation`
3. `terminal-bench-science/si-fracture-fbc`

Additional supporting files may include:

- `geometry.json`
- `healthy_reference.npz`
- `data_checksums.sha256`
- Other attached screenshots, research materials, and task files.

These files are references, not a requirement to reuse their scientific problems or datasets. A checksum manifest does not substitute for the underlying data.

### Your first action

Inspect the actual repository and its documentation.

For all three reference tasks, examine the available:

- `task.toml`
- `instruction.md`
- `README.md`
- `environment/Dockerfile`
- Input datasets and source files
- `solution/solve.sh` and reference implementation
- `tests/Dockerfile`
- `tests/test.sh`
- Hidden evaluator implementation
- Expected outputs
- Verification and reward logic

Also read the actual Terminal-Bench Science authoring guidelines, proposal rubric, implementation rubric, and QC documentation.

If the complete repository or a reference file is inaccessible, report that limitation and use only material you can verify. Never invent missing content.

### Reference analysis

Determine what makes these examples challenging:

- Mathematical and scientific reasoning
- Multistage problem solving
- Domain-specific knowledge
- Algorithm selection
- Numerical correctness
- Computational complexity
- Data and dependency handling
- Verification methodology
- Agent failure opportunities

Create:

`authoring/reference_analysis.md`

Explain how to achieve comparable scientific depth while creating a genuinely independent Mathematics task.

---

## 3. RESEARCH AND SELECT ONE ORIGINAL MATHEMATICS PROBLEM

Research relevant mathematical benchmarks, published problems, scientific computing workflows, and research implementations.

Consider advanced mathematical areas such as:

- Numerical analysis and numerical linear algebra
- Computational number theory
- Graph theory and combinatorics
- Discrete mathematics
- Optimization and constrained optimization
- Differential equations and boundary-value problems
- Inverse problems
- Computational geometry
- Algebra and symbolic computation
- Spectral methods and eigenvalue problems
- Probability theory and stochastic processes
- Rigorous numerical verification

Choose **ONE** area with the strongest combination of mathematical depth, objective verifiability, originality, and realistic terminal-based solvability.

The task should require more than applying a standard formula or calling an existing library function.

### Mandatory mathematical difficulty

Design a mathematical problem involving several genuinely interconnected challenges, such as:

1. Deriving or identifying the correct mathematical method.
2. Understanding constraints, assumptions, and mathematical structure.
3. Implementing a nontrivial algorithm.
4. Handling numerical stability, conditioning, or exact arithmetic where relevant.
5. Resolving multiple edge cases and degenerate configurations.
6. Validating intermediate mathematical properties.
7. Producing a correctly structured final result.
8. Independently verifying correctness.

Include meaningful mathematical dependencies: an incorrect intermediate calculation should potentially affect later results.

Require substantial reasoning and planning, but avoid artificial complexity or unnecessarily expensive computations.

### Originality requirements

The new task must NOT:

- Rename a public benchmark.
- Copy a public problem and change numbers.
- Replace an existing dataset while retaining the same solution.
- Reuse distinctive test cases or solution logic.
- Paraphrase an existing task to disguise its origin.
- Depend on memorized public benchmark answers.

Develop a new mathematical problem with an independently justified solution.

Create:

`authoring/math_research_review.md`

`authoring/originality_assessment.md`

---

## 4. PREPARE THE TASK PROPOSAL

Before implementation, create:

`authoring/task_proposal.md`

Include:

1. Task title and identifier.
2. Mathematics subdomain.
3. Research background.
4. Real mathematical problem being solved.
5. Precise mathematical formulation.
6. Definitions, assumptions, and constraints.
7. Input specification.
8. Required mathematical algorithm or properties.
9. Output specification.
10. Mathematical dependencies.
11. Important edge cases.
12. Computational environment.
13. Numerical accuracy requirements.
14. Independent verification strategy.
15. Oracle/reference solution methodology.
16. Expected agent failure modes.
17. Originality assessment.
18. Difficulty justification.
19. Expected expert completion time.
20. Expected junior completion time.
21. Comparison with the three reference tasks.

Evaluate this proposal using the actual Terminal-Bench Science proposal rubric.

**First display the planned directory hierarchy and summarize the selected problem. Then continue into implementation without stopping for confirmation unless essential authorization or missing access blocks the work.**

---

## 5. CREATE THE COMPLETE HARBOR TASK

Work directly in the provided repository.

Follow the actual repository directory conventions. Do not assume a layout without inspection.

The completed task should contain the equivalent of:

- `task.toml`
- `instruction.md`
- `README.md`
- `environment/Dockerfile`
- Required mathematical source code and supporting files
- `environment/data/` if applicable
- Dependency specifications
- `solution/solve.sh`
- Reference mathematical implementation
- `tests/Dockerfile` if required
- `tests/test.sh`
- `tests/test_outputs.py` or the repository's required evaluator
- Reproducibility instructions

Also create authoring reports, validation scripts, and trajectory records in the appropriate authoring directory.

### Environment requirements

- Reproducible Docker environment.
- Explicit and pinned dependencies where practical.
- No required internet access at evaluation time.
- No unavailable APIs or external services.
- CPU-compatible execution unless justified otherwise.
- Defined memory and runtime limits.
- Deterministic behavior where required.
- No missing datasets or broken infrastructure.
- No dependency on files unavailable to the agent.

### Agent instructions

Write a clear `instruction.md` explaining:

- The exact mathematical objective.
- Available inputs.
- Necessary mathematical definitions.
- Required operations and outputs.
- Input/output schemas and paths.
- Numerical tolerances and precision requirements.
- Constraints and permitted tools.
- Execution and verification requirements.
- How success is determined.

Avoid ambiguous instructions and undocumented evaluation requirements.

Do not expose hidden tests, oracle answers, or reference implementation details to the evaluated agent.

---

## 6. BUILD A GENUINE MATHEMATICAL REFERENCE SOLUTION

Implement a fully functional oracle solution.

The solution must:

- Use a mathematically justified algorithm.
- Solve the actual problem rather than hardcoding outputs.
- Work on different valid inputs.
- Respect computational limits.
- Handle edge cases and degenerate cases.
- Use appropriate precision.
- Produce all required files.
- Verify important intermediate invariants.
- Be deterministic where required.

The reference solution should demonstrate that the task is achievable by a knowledgeable agent.

Document the mathematical reasoning separately in author-only documentation.

**Do not weaken the task or change the evaluator simply to make the oracle pass.**

---

## 7. DEVELOP AN INDEPENDENT HIDDEN EVALUATOR

This is a critical requirement.

Build comprehensive tests checking actual mathematical correctness, not merely the presence of files or the use of particular functions.

Include:

- Standard functional tests.
- Difficult edge cases.
- Degenerate and boundary cases.
- Numerically sensitive cases.
- Randomized valid mathematical inputs.
- Regression tests.
- Mathematical invariant checks.
- Metamorphic or property-based tests where appropriate.
- Tests detecting hardcoded outputs.
- Tests detecting superficial solutions.
- Tests validating precision and tolerances.
- Tests ensuring reproducibility.

Prefer independent mathematical verification instead of comparing everything directly against one reference implementation.

For approximate outputs, justify tolerances mathematically and use appropriate absolute/relative error checks.

Where appropriate, use exact arithmetic, residual bounds, certificates, independent algorithms, or structural invariants.

The evaluator must accept alternative mathematically correct algorithms.

### Security and fairness

- Keep hidden tests and oracle files outside the agent environment.
- Ensure the Dockerfile does not accidentally copy them into the agent image.
- Prevent agent-controlled files from modifying grading logic.
- Avoid output-based shortcuts and evaluator leakage.
- Do not introduce undocumented hidden requirements.

Create an evaluator coverage report.

---

## 8. VALIDATE THE TASK BEFORE AGENT TESTING

Run the actual task using Docker and the installed Harbor CLI.

Inspect the installed Harbor version and supported commands first. Do not invent commands.

Perform:

1. Task configuration and discovery checks.
2. Clean Docker environment build.
3. Reference solution execution.
4. Complete hidden-test execution.
5. No-op/broken baseline execution.
6. Plausible incomplete solution execution.
7. Clean environment reset and repeatability verification.
8. Reward output verification.
9. Hidden-test isolation and leakage checks.

### Required validation conditions

- The oracle passes every mandatory evaluator test.
- The broken baseline fails relevant tests.
- At least one plausible partial implementation fails.
- Clean reruns produce consistent results.
- No essential dependencies are missing.
- Evaluation does not depend on agent self-reported success.

If validation fails, investigate the cause, correct the implementation, and rerun the relevant checks.

Create:

`authoring/reports/harbor_validation.md`

Include exact commands, logs, results, and remaining limitations.

Do not describe source-level tests as successful Docker/Harbor execution when the latter has not been performed.

---

## 9. RUN EIGHT INDEPENDENT AI AGENT TRIALS

The primary difficulty-calibration objective is an observed success rate of approximately **40–60%** on one selected advanced coding agent.

Harbor is already installed on my PC, so inspect the existing installation before attempting to reinstall anything.

Check:

- Harbor version and CLI.
- Python environment.
- Docker and Docker daemon.
- Supported agents.
- Available model integrations.
- Authentication configuration.

### Preferred model

Use a compatible Gemini model through Google's official API, ideally an available free-tier model.

Check official Gemini documentation for current model availability, rate limits, authentication, and free-tier restrictions.

Never invent API keys. Do not expose or commit credentials.

If authentication is required, clearly identify the necessary user action.

### Trial methodology

Run the **same agent and model on the task 8 times**.

Each trial must:

- Start from the same clean initial task state.
- Use the same instructions and evaluator version.
- Use the same model and agent configuration.
- Use equivalent resource and execution limits.
- Avoid accessing results from previous attempts.
- Record its results independently.

Use different random seeds only where appropriate, without changing the fairness of the evaluation.

Record for every trial:

- Run ID
- Agent and model
- Model version
- Task version
- Seed if applicable
- Execution duration
- Steps and tool calls
- Token usage and cost, if available
- Reward
- Success/failure
- Error or failure reason
- Trajectory/log location

### Calibration rules

If all 8 pass, investigate whether the task is too easy and increase legitimate mathematical complexity.

If all 8 fail, determine whether the reason is excessive difficulty, unclear instructions, missing dependencies, evaluator defects, or genuine model limitations.

Adjust the mathematical problem only when justified, and rerun the complete evaluation with a clearly recorded new task version.

Do not tune merely to overfit eight outcomes.

A sample of eight has substantial uncertainty; report the observed rate without claiming that it establishes the true population success rate.

If API limits prevent all eight runs, record exactly how many were actually completed. Do not fabricate the remaining trajectories or report interrupted trials as ordinary failures.

### Required calibration report

Create:

`authoring/trajectories/trajectory_summary.csv`

`authoring/trajectories/trajectory_summary.json`

`authoring/reports/trajectory_analysis.md`

Include:

- Total completed trials.
- Successful trials.
- Failed trials.
- Success and failure percentages.
- Average/median execution time.
- Step counts.
- Token usage and costs when available.
- Common failure patterns.
- Evidence identifying agent errors versus infrastructure or evaluator issues.
- Difficulty adjustments and retesting history.

Focus failure analysis on mathematical reasoning, planning, dependency tracking, implementation, numerical instability, error recovery, and independent verification.

---

## 10. RUN AN ORIGINALITY AND SIMILARITY AUDIT

Create a local originality-checking process under:

`authoring/plagiarism/`

Compare the new task with the three supplied reference tasks and other relevant public examples.

Analyze:

- Task instructions.
- Mathematical problem.
- Formulations and algorithms.
- Code.
- Dataset structure.
- Evaluator logic.
- Conceptual similarity.

Use exact matching, normalized comparison, n-grams, code/structure comparison, and semantic comparison where available.

Aim for at least 70% originality using the documented heuristic, with 30% similarity treated as a review-warning threshold.

These percentages are not proof of originality. Evaluate mathematical and conceptual similarity manually and distinguish standard mathematical notation from copied content.

Produce:

- `authoring/plagiarism/reports/plagiarism_report.md`
- `authoring/plagiarism/reports/plagiarism_report.json`

Do not conceal copied material merely to improve a similarity score.

---

## 11. COMPLETE TERMINAL-BENCH SCIENCE QC AND RUBRIC AUDITS

Read the repository's actual QC requirements and rubrics.

Audit:

**Mathematical validity:** Correct formulation, algorithms, assumptions, numerical precision, and verification.

**Task quality:** Realistic difficulty, complete instructions, solvability, originality, and reproducibility.

**Evaluator quality:** Independent tests, meaningful edge cases, hidden-test isolation, and alternative-solution acceptance.

**Infrastructure:** Docker, Harbor, dependencies, file paths, runtime constraints, and reproducibility.

**Benchmark integrity:** No leaked solutions, hardcoded outputs, copied task content, reward manipulation, or fabricated evidence.

For every applicable rubric requirement, assign:

- PASS
- FAIL
- WARNING
- NOT TESTED

Include supporting evidence and exact remediation for failures.

Create:

`authoring/reports/qc_audit.md`

`authoring/reports/implementation_rubric_audit.md`

Do not mark anything PASS without verifying it.

---

## 13. FINAL DELIVERABLES

Provide:

1. Final task title and mathematical domain.
2. Complete task directory hierarchy.
3. Reference-task comparison.
4. Mathematical research and originality assessment.
5. Task proposal.
6. Complete Harbor task implementation.
7. All necessary data and source files.
8. Reference mathematical solution.
9. Independent hidden evaluator.
10. Evaluator coverage report.
11. Broken/incomplete-solution validation.
12. Docker and Harbor validation results.
13. Eight real agent trajectories, if executable.
14. Calibration and failure analysis.
15. Originality/plagiarism reports.
16. Terminal-Bench Science QC audit.
17. Implementation rubric audit.
18. Complete local package and supporting reports.
19. Exact reproduction commands.
20. Clear outstanding limitations.

### NON-NEGOTIABLE RULES

- Create exactly ONE Mathematics task.
- Mathematics must be the primary challenge.
- The task must be original, difficult, objectively solvable, and fairly evaluated.
- Do not create a superficial variation of an existing task.
- Do not fabricate experiments, agent results, or success rates.
- Do not expose hidden evaluator data to the agent.
- Do not hardcode mathematical answers.
- Do not make evaluation depend on one specific implementation.
- Do not introduce intentionally unreliable infrastructure.
- Do not skip implementation, validation, or QC.
- Do not claim a 40–60% measured success rate without real agent trials.
- Do not create a remote repository, commit, push, or publish anything.

## START EXECUTION NOW

First inspect the repository, all accessible reference tasks, and the relevant QC documents.

Then:

1. Present the proposed task hierarchy.
2. Select ONE original, research-level Mathematics problem.
3. Produce the proposal and originality assessment.
4. Implement all required task files.
5. Implement the oracle and hidden tests.
6. Execute real validation.
7. Run agent trajectories and calibrate difficulty where possible.
8. Complete quality and originality audits.
9. Complete the local task package and detailed evidence-based report.

**Do not stop after proposing the idea. Continue implementing and verifying the complete task. Ask before installing or running software. Keep all files, reports, and results local.**