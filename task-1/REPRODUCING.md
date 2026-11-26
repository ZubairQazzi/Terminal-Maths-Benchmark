# Running Task 1

The complete task is `tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure`. Use an existing Harbor 0.27.0 installation and Docker. Both task images declare their pinned mathematics/test dependencies and the pinned Python base image. No frontier-model key is needed to run the reference oracle.

From this bundle's root:

```sh
harbor lint tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure --select ALL --json
harbor run --path tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure --agent oracle --n-concurrent 1
harbor run --path tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure --agent nop --n-concurrent 1
```

Expected reference reward is 1; expected no-op reward is 0. The reference and tests are author-side files: agents solving the benchmark receive only the public environment and instructions through Harbor. Details of the mathematical contract are in the task's public environment/spec.md.

The validation host uses process-local F: storage and a restricted Harbor storage wrapper, retained in the original local audit workspace. Configure your own tool/cache storage before executing commands; the generic examples above do not change global storage settings. The evidence reports preserve the original host's commands, file hashes, native outcomes and scope. A complete raw authoring-workspace replay additionally requires the locally retained scripts/raw logs/corpus; those are not claimed to be contained in this compact publication.

`SHA256SUMS` verifies every bundle file except the checksum file itself. From a shell with sha256sum, run `sha256sum -c SHA256SUMS`. The scientific source manifest is also included at authoring/reports/task_file_manifest.json. The archive and expanded folder contain the same bundle bytes. A repository-level task-1.sha256 verifies task 1.zip.

Model trials, paid APIs and difficulty calibration are separate from these reference/no-op commands. The published evidence contains no valid model success percentage.
