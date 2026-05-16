# Merlin Cleanup Script Design

## Summary

This document specifies a `cleanup.sh` script for the `03-merlin/` tutorial section. When attendees run the Merlin examples, Merlin creates timestamped study workspace directories both inside the repository (`03-merlin/output/`) and, for example 1, on the Perlmutter scratch filesystem under `$PSCRATCH/wf-seminar-merlin/`. Without a cleanup script, these runtime artifacts accumulate between runs and must be removed by hand. The script removes all of them in one step, returning the section directory to its freshly-cloned state.

The implementation follows the pattern already established by `00-gnu-parallel/cleanup.sh`, `01-signac/cleanup.sh`, and `02-maestro/cleanup.sh`: a short Bash script with `set -euo pipefail`, a `SCRIPT_DIR` anchor so it is safe to invoke from any working directory, named glob patterns per study directory, and a `find`-based sweep for Python bytecode caches. The only addition specific to Merlin is a guarded block that removes the `$PSCRATCH` scratch workspace when that environment variable is set — a guard required because `$PSCRATCH` is a NERSC-specific variable that is absent in non-Perlmutter environments and must be handled safely under Bash's `nounset` option.

## Definition of Done

A single `03-merlin/cleanup.sh` script that:
- Removes timestamped study workspace directories from `output/` for all three examples (`example1-distributed_*`, `fault-tolerance-demo_*`, `massive-scale_*`)
- Removes `$PSCRATCH/wf-seminar-merlin/example1-distributed_*` (guarded: only runs if `$PSCRATCH` is set)
- Removes `__pycache__` directories recursively
- Follows the exact same style as the existing cleanup scripts for `00-gnu-parallel`, `01-signac`, and `02-maestro`

## Acceptance Criteria

### merlin-cleanup.AC1: Local output directories are removed
- **merlin-cleanup.AC1.1 Success:** `output/example1-distributed_<timestamp>/` directories under `03-merlin/` are removed
- **merlin-cleanup.AC1.2 Success:** `output/fault-tolerance-demo_<timestamp>/` directories under `03-merlin/` are removed
- **merlin-cleanup.AC1.3 Success:** `output/massive-scale_<timestamp>/` directories under `03-merlin/` are removed
- **merlin-cleanup.AC1.4 Edge:** Script exits 0 when no matching output directories exist (nothing to clean)

### merlin-cleanup.AC2: PSCRATCH scratch directories are removed (when set)
- **merlin-cleanup.AC2.1 Success:** `$PSCRATCH/wf-seminar-merlin/example1-distributed_<timestamp>/` directories are removed when `$PSCRATCH` is set and non-empty
- **merlin-cleanup.AC2.2 Edge:** Script exits 0 and skips the PSCRATCH block when `$PSCRATCH` is unset
- **merlin-cleanup.AC2.3 Edge:** Script exits 0 and skips the PSCRATCH block when `$PSCRATCH` is empty string

### merlin-cleanup.AC3: Python bytecode caches are removed
- **merlin-cleanup.AC3.1 Success:** All `__pycache__/` directories under `03-merlin/` are removed recursively
- **merlin-cleanup.AC3.2 Edge:** Script exits 0 when no `__pycache__/` directories exist

### merlin-cleanup.AC4: Script style matches existing cleanup scripts
- **merlin-cleanup.AC4.1 Success:** Script is invocable from any working directory (uses `SCRIPT_DIR`)
- **merlin-cleanup.AC4.2 Success:** Script uses `set -euo pipefail`
- **merlin-cleanup.AC4.3 Success:** Comment block at top lists all artifact patterns with descriptions
- **merlin-cleanup.AC4.4 Success:** Final line prints `03-merlin cleaned.`

## Glossary

- **`set -euo pipefail`**: A Bash option triple that makes scripts fail fast: `-e` exits on any error, `-u` treats unset variables as errors, `-o pipefail` propagates failures through pipelines. Standard defensive practice for shell scripts.
- **`SCRIPT_DIR`**: A variable computed at runtime from `$(dirname "$0")` (the directory containing the script itself), used to anchor all paths so the script works correctly regardless of the caller's current working directory.
- **study workspace directory**: The output directory Merlin creates for each workflow run, named `<study-name>_<timestamp>/`. Contains step logs, parameter files, and worker output. Timestamped so successive runs do not overwrite each other.
- **`$PSCRATCH`**: A NERSC environment variable pointing to the user's high-performance scratch filesystem (`/pscratch/sd/<u>/<username>`). Set automatically on Perlmutter login nodes and compute nodes; absent in other environments.
- **`${PSCRATCH:-}` parameter expansion**: Bash syntax that evaluates to the value of `$PSCRATCH` if set, or to an empty string if unset. Prevents the script from aborting under `-u` (nounset) when `$PSCRATCH` is not defined.
- **`nullglob`**: A Bash shell option that makes unmatched glob patterns expand to nothing (empty list) instead of being passed literally to the command. The design notes that `rm -rf` with `-f` makes `nullglob` unnecessary here because `rm -f` already returns exit 0 for non-existent paths.
- **`__pycache__`**: A directory Python creates automatically to store compiled bytecode (`.pyc` files). Generated whenever Python imports a `.py` file; not a source artifact and safe to delete.
- **`OUTPUT_PATH`**: The field in a Merlin spec YAML (`spec.yaml`) that controls where the study workspace is written. For example 1 this is set to `$PSCRATCH/wf-seminar-merlin/`, which is why the cleanup script targets that specific path.
- **Merlin spec / `spec.yaml`**: A YAML file that defines a Merlin workflow: the steps to run, parameter spaces, and environment settings (including `OUTPUT_PATH`). Merlin reads this file when `merlin run` is invoked.
- **`app.yaml`**: Merlin's application configuration file, which specifies the message broker (Redis) and results backend connection details. Merlin searches for `./app.yaml` before `~/.merlin/app.yaml`.

## Architecture

A single Bash script at `03-merlin/cleanup.sh`. No coordination between components — one file, one responsibility: remove runtime artifacts.

The script uses `set -euo pipefail` and computes `SCRIPT_DIR` from `$(dirname "$0")` so it is safe to invoke from any working directory. Artifacts are removed with named glob patterns per study name (not `rm -rf output/` wholesale), making it self-documenting and consistent with the other section cleanup scripts.

The `$PSCRATCH` block is guarded with `[ -n "${PSCRATCH:-}" ]`. The `${PSCRATCH:-}` parameter expansion returns an empty string when `$PSCRATCH` is unset, making it safe under `set -u` (nounset). If `$PSCRATCH` is set and non-empty, the example1 scratch workspace directories are removed.

Unmatched globs are safe without `nullglob` because `rm -rf` with the `-f` flag returns exit code 0 for non-existent paths.

## Existing Patterns

All three existing cleanup scripts (`00-gnu-parallel/cleanup.sh`, `01-signac/cleanup.sh`, `02-maestro/cleanup.sh`) share an identical structure:

- `#!/bin/bash` shebang
- Comment block listing all artifacts with short explanations
- `set -euo pipefail`
- `SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)`
- `rm -rf "$SCRIPT_DIR/..."` with named glob patterns per timestamped output directory
- `find "$SCRIPT_DIR" -name '__pycache__' -type d -exec rm -rf {} +` for Python caches
- `echo "NN-section cleaned."` as the final line

This design follows that pattern exactly. The only addition is the `$PSCRATCH` guard block, which is a Merlin-specific requirement not present in the other sections.

## Implementation Phases

<!-- START_PHASE_1 -->
### Phase 1: Write cleanup.sh

**Goal:** Create `03-merlin/cleanup.sh` matching the established pattern.

**Components:**
- `03-merlin/cleanup.sh` — new file, executable

**Dependencies:** None

**Done when:** Script exists, is executable (`chmod +x`), and the following manual checks pass:
- Running `bash -n 03-merlin/cleanup.sh` (syntax check) exits 0
- Running the script on a system without `$PSCRATCH` set does not error
- Running the script removes all artifact patterns listed in the comment block
<!-- END_PHASE_1 -->

## Additional Considerations

**Redis and Celery state:** Merlin's message broker state (task queues, results) lives in a running Redis server process, not in files within the project directory. `~/.merlin/` contains user-level Merlin config (not a project artifact). Neither requires cleanup from this script.

**$PSCRATCH path:** The path `$PSCRATCH/wf-seminar-merlin/` is the `OUTPUT_PATH` value in `example1-distributed/spec.yaml`. If that value changes in the spec, this script must be updated to match.
