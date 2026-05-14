# Example 3 OUTPUT_PATH Fix Design

## Summary

The `example3-massive-scale` spec.yaml has a latent bug in how it uses `$(OUTPUT_PATH)`. Merlin resolves variable references in two passes: first it substitutes user-defined variables from `env.variables`, then it substitutes built-in special variables (like `$(WORKSPACE)`) using absolute paths derived at execution time. Because `OUTPUT_PATH` is absent from `env.variables` in example 3, Merlin's second pass treats it as an unknown built-in and resolves it to the absolute current working directory at the time `merlin run` was invoked. Every task — all 1000 of them — therefore writes to the same shared directory, creating a race condition where concurrent workers overwrite each other's `metrics.txt`. The downstream `aggregate` step then cannot reliably find any per-task output.

The fix is a one-line addition: placing `OUTPUT_PATH: ./output` in `env.variables` so that Merlin's first pass substitutes `$(OUTPUT_PATH)` with the literal string `./output` before the second pass runs. Because each task executes with its own task workspace as its current working directory, `./output/metrics.txt` resolves to a unique path per task. Prepending `mkdir -p $(OUTPUT_PATH)` to both the `train` and `aggregate` step commands ensures the subdirectory exists before either step writes to it. This brings example 3 into conformance with the pattern already used in examples 1 and 2, and a new Expected Output section in the README makes the resulting directory layout explicit for attendees.

## Definition of Done

- `example3-massive-scale/spec.yaml`: `OUTPUT_PATH: ./output` added to `env.variables`; `mkdir -p $(OUTPUT_PATH)` added to the `train` step cmd; `mkdir -p $(OUTPUT_PATH)` added to the `aggregate` step cmd
- Both the race condition and the broken `find` are fixed — each train task writes to its own `<task_workspace>/output/metrics.txt`, and the aggregate locates all of them
- `example3-massive-scale/README.md`: Expected Output section added documenting the resulting directory structure
- No changes to examples 1 or 2, or any other files

## Acceptance Criteria

### ex3-output-path-fix.AC1: spec.yaml contains correct OUTPUT_PATH definition
- **ex3-output-path-fix.AC1.1 Success:** `env.variables` block contains `OUTPUT_PATH: ./output`
- **ex3-output-path-fix.AC1.2 Success:** `train` step cmd contains `mkdir -p $(OUTPUT_PATH)` before the `python -c` line
- **ex3-output-path-fix.AC1.3 Success:** `aggregate` step cmd contains `mkdir -p $(OUTPUT_PATH)` before the `echo` line

### ex3-output-path-fix.AC2: Fix resolves the race condition and broken find
- **ex3-output-path-fix.AC2.1 Success:** `$(OUTPUT_PATH)` in both cmds expands to `./output` (relative), not an absolute shared path
- **ex3-output-path-fix.AC2.2 Success:** `aggregate` step's `find $(WORKSPACE)/../ -name "metrics.txt"` can locate all per-task output files

### ex3-output-path-fix.AC3: README documents expected output structure
- **ex3-output-path-fix.AC3.1 Success:** README contains an Expected Output section positioned after the Running section
- **ex3-output-path-fix.AC3.2 Success:** Expected Output section includes directory tree showing per-task `output/metrics.txt` paths and `aggregate/output/summary.txt`

### ex3-output-path-fix.AC4: Scope is limited to example 3
- **ex3-output-path-fix.AC4.1 Success:** No files outside `03-merlin/example3-massive-scale/` are modified

## Glossary

- **`env.variables`**: The user-defined variable block in a Merlin spec file. Variables defined here are substituted as literal strings in pass 1 of Merlin's variable resolution, before any built-in special variables are expanded.
- **pass 1 / pass 2 (Merlin variable resolution)**: Merlin resolves spec variables in two sequential passes. Pass 1 replaces `$(VAR)` tokens that appear in `env.variables` with their literal values. Pass 2 replaces built-in special tokens (`$(WORKSPACE)`, `$(SPECROOT)`, etc.) with absolute paths computed at runtime. A variable absent from `env.variables` is not touched in pass 1 and may be misidentified or left unresolved in pass 2.
- **`$(WORKSPACE)`**: A Merlin built-in variable that expands to the absolute path of the current task's working directory, unique per task instance (e.g., `<study_root>/train/00000001/`).
- **`$(SPECROOT)`**: A Merlin built-in variable that expands to the directory containing the spec.yaml file. Shared across all tasks in a study.
- **`$(MERLIN_INFO)`**: A Merlin built-in variable pointing to the study's metadata directory, used here to store the generated samples file.
- **`merlin.samples`**: The block in a Merlin spec that defines a parameter-space fan-out. Merlin generates a sample file (here `.npy`) and launches one task per row, injecting column values (e.g., `$(lr)`, `$(batch_size)`) as per-task variables.
- **task workspace**: The private directory Merlin creates for each individual task instance. The task process runs with this directory as its CWD, so relative paths like `./output/` are isolated per task.
- **race condition**: A concurrency defect where the correct outcome depends on the order in which independent concurrent processes access a shared resource. Here, 1000 tasks writing to the same absolute path produce unpredictable final file contents.
- **`find` (shell command)**: Used in the `aggregate` step to recursively locate all `metrics.txt` files produced by the fan-out tasks. Relies on `$(WORKSPACE)/../` — the parent of the aggregate step's workspace — to reach the study root where all per-task directories reside.
- **fan-out**: A workflow pattern where a single logical step spawns many parallel task instances, each operating on a different set of parameters. Merlin's `merlin.samples` block drives the fan-out in this example.
- **`global.parameters` vs `merlin.samples`**: Two distinct Merlin mechanisms for parameter fan-out. `global.parameters` enumerates a small, explicit list of values; `merlin.samples` reads from a generated file and supports large combinatorial sweeps (here, 1000 combinations).

## Architecture

`example3-massive-scale` uses Merlin's `merlin.samples` block to fan out 1000 hyperparameter combinations across distributed workers. The bug is in variable substitution: Merlin processes `env.variables` in pass 1 (literal string replacement) and built-in special vars in pass 2 (absolute path injection). `OUTPUT_PATH` absent from `env.variables` falls through to pass 2, where it resolves to `os.path.abspath("")` — the absolute CWD at `merlin run` invocation time, shared by all tasks.

Fix: add `OUTPUT_PATH: ./output` to `env.variables`. Pass 1 substitutes `$(OUTPUT_PATH)` with the literal string `./output` before pass 2 runs. Each task executes in its own workspace directory (CWD = `<study_root>/train/<sample_index>/`), so `./output/metrics.txt` is unique per task.

The `aggregate` step's `find $(WORKSPACE)/../ -name "metrics.txt"` already points to the study root and will locate all per-task `metrics.txt` files once they are written to task workspaces. No change to the `find` command is needed.

## Existing Patterns

Examples 1 and 2 in `03-merlin/` already use `OUTPUT_PATH: ./output` in `env.variables` and `mkdir -p $(OUTPUT_PATH)` in step cmds. Example 3 inconsistently omitted both. This fix brings example 3 into alignment with the established pattern for the section.

## Implementation Phases

<!-- START_PHASE_1 -->
### Phase 1: Fix spec.yaml and README.md

**Goal:** Correct the OUTPUT_PATH variable definition and document the resulting output structure.

**Components:**
- `03-merlin/example3-massive-scale/spec.yaml` — add `OUTPUT_PATH: ./output` to `env.variables`; prepend `mkdir -p $(OUTPUT_PATH)` to `train` step cmd; prepend `mkdir -p $(OUTPUT_PATH)` to `aggregate` step cmd
- `03-merlin/example3-massive-scale/README.md` — add Expected Output section after the Running block showing the `massive_scale_<timestamp>/` directory tree

**Dependencies:** None

**Done when:** `spec.yaml` contains `OUTPUT_PATH: ./output` in `env.variables`, both cmds contain `mkdir -p $(OUTPUT_PATH)`, and `README.md` contains the Expected Output section
<!-- END_PHASE_1 -->
