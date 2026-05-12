# signac CLI Inspection - Workspace Visibility for Training

## Summary

This design adds a shell script and README section to help training attendees understand what signac creates on disk and how to navigate it from the command line. When attendees run `init_project.py`, signac generates a `workspace/` directory where each parameter combination gets its own subdirectory named by a hash of the statepoint. This naming is opaque by design, so a common training question is "where is the output for the run with temperature=300?" The new `inspect_workspace.sh` script answers this directly using signac's built-in CLI tools, walking through four commands in order: listing the project schema, filtering jobs by a single parameter, looking up the exact directory path for a full parameter set, and reading the raw statepoint file.

The approach is deliberately CLI-first rather than Python API-first. An existing script (`explore_workspace.py`) already covers the Python API perspective. The shell script fills the complementary gap: showing that signac ships with command-line tools that require no Python and no special knowledge of signac internals to use. The companion README section anchors the script in context by explaining the on-disk layout, providing a brief CLI reference, and noting `signac view` as a browsing alternative. Both deliverables are read-only and depend only on the workspace that `init_project.py` already produces.

## Definition of Done

1. A shell script in `01-signac/example1-parameter-space/` that uses signac CLI tools (`signac find`, `signac statepoint`, etc.) to demonstrate inspecting the workspace, including the key use case of finding a job directory given specific parameters.
2. A new README section in `01-signac/example1-parameter-space/README.md` with minimum viable explanation of: what signac creates on disk, how to use the CLI to inspect it, and how to answer "where is the output for these parameters?"
3. Both deliverables work against the workspace created by `init_project.py` (no additional setup).

## Acceptance Criteria

### signac-cli-inspection.AC1: Script demonstrates signac CLI inspection
- **signac-cli-inspection.AC1.1 Success:** `bash inspect_workspace.sh` runs without errors against an initialized workspace
- **signac-cli-inspection.AC1.2 Success:** Script output shows project parameter schema (all keys and value ranges)
- **signac-cli-inspection.AC1.3 Success:** Script output shows filtered job IDs for a specific parameter value
- **signac-cli-inspection.AC1.4 Success:** Script output shows the directory path for a specific parameter combination
- **signac-cli-inspection.AC1.5 Success:** Script output shows raw `signac_statepoint.json` content as plain JSON

### signac-cli-inspection.AC2: README explains workspace structure and CLI tools
- **signac-cli-inspection.AC2.1 Success:** README describes what signac creates on disk (`.signac/config`, `workspace/<hash>/signac_statepoint.json`)
- **signac-cli-inspection.AC2.2 Success:** README includes brief CLI commands reference (schema, find, job)
- **signac-cli-inspection.AC2.3 Success:** README includes minimal `signac view` description
- **signac-cli-inspection.AC2.4 Success:** README adds script execution as step 4 in "Running This Example"

### signac-cli-inspection.AC3: No additional setup required
- **signac-cli-inspection.AC3.1 Success:** Script works against workspace created by `init_project.py` with no other dependencies

## Glossary

- **signac**: A Python library and CLI for managing parameter spaces in computational workflows. Organizes jobs into a content-addressable workspace where each unique parameter combination maps to a directory.
- **statepoint**: The dictionary of parameters (e.g., `{"temperature": 300, "pressure": 1.0}`) that uniquely identifies a single job. Stored on disk as `signac_statepoint.json`.
- **workspace**: The directory (`workspace/`) that signac creates to hold all job subdirectories. Each subdirectory name is the MD5 hash of that job's statepoint.
- **job ID**: The MD5 hash signac computes from a statepoint dictionary. Used as the directory name for that job's workspace subdirectory.
- **`signac schema`**: CLI command that reports all parameter keys and value ranges across all jobs in a project.
- **`signac find`**: CLI command that filters jobs by parameter key-value pairs and prints matching job IDs.
- **`signac job`**: CLI command that accepts a full statepoint JSON and prints the job's workspace directory path.
- **`signac view`**: CLI command that creates a human-readable symlinked directory hierarchy organized by parameter values.

## Architecture

An annotated bash script demonstrates signac's CLI commands in a logical progression: project overview, parameter-based search, parameter-to-path lookup, and raw file inspection. A companion README section explains what signac creates on disk, references the CLI commands, adds `signac view` as a browsing alternative, and integrates the script into the existing "Running This Example" steps.

The script is read-only - it inspects the workspace without modifying it. It depends on the workspace created by `init_project.py` (same dependency as `explore_workspace.py`).

**Script command progression:**

1. `signac schema` - project-level overview of all parameters and value ranges
2. `signac find temperature 300` - filter jobs by parameter value, returns matching job IDs
3. `signac job '{"temperature": 300, "pressure": 1.0}'` - exact parameter-to-path lookup (the key use case)
4. `cat workspace/<id>/signac_statepoint.json` - raw file inspection showing plain JSON, no special tools required

**README content structure:**

1. "What signac creates on disk" - file tree description (`.signac/config`, `workspace/<hash>/signac_statepoint.json`)
2. "CLI commands" - brief reference of schema/find/job commands
3. "`signac view`" - minimal description of human-readable symlinked directory hierarchy
4. Step 4 added to "Running This Example" - `bash inspect_workspace.sh`

## Existing Patterns

Investigation found:
- **No existing `.sh` scripts** in any example directory (00-04). All examples use Python scripts. This design introduces the first shell script, justified because signac CLI is a shell tool and the user chose the CLI approach over Python API.
- **README CLI documentation pattern** is well-established: bash code blocks showing exact commands, consistent across all section READMEs. The new README section follows this pattern.
- **`explore_workspace.py`** already covers the Python API perspective (iterating all jobs, showing IDs/params/paths). The new script complements this with the CLI/command-line perspective and adds parameter-based lookup, which `explore_workspace.py` does not support.
- **Example scripts are 10-50 lines**, focused on one concept. The shell script follows this convention.

## Implementation Phases

<!-- START_PHASE_1 -->
### Phase 1: Shell Script

**Goal:** Create the annotated inspection script

**Components:**
- Create: `01-signac/example1-parameter-space/inspect_workspace.sh` - bash script demonstrating signac CLI commands with echo annotations explaining each step

**Dependencies:** None (workspace from `init_project.py` is a runtime dependency, not a build dependency)

**Done when:** `bash inspect_workspace.sh` runs successfully against an initialized workspace and produces output showing schema, filtered jobs, job path lookup, and raw statepoint JSON

**Covers:** signac-cli-inspection.AC1
<!-- END_PHASE_1 -->

<!-- START_PHASE_2 -->
### Phase 2: README Content

**Goal:** Add "Inside the Workspace" section to README

**Components:**
- Modify: `01-signac/example1-parameter-space/README.md` - insert new section between "What Happens Under the Hood" and "Next Steps", add step 4 to "Running This Example"

**Dependencies:** Phase 1 (script must exist to reference from README)

**Done when:** README contains "Inside the Workspace" section covering on-disk structure, CLI commands, signac view, and references the script. Step 4 appears in "Running This Example."

**Covers:** signac-cli-inspection.AC2, signac-cli-inspection.AC3
<!-- END_PHASE_2 -->

## Additional Considerations

**Signac CLI version compatibility:** The CLI commands used (`signac find`, `signac job`, `signac schema`) are stable across signac 2.x. The `signac view` command syntax should be verified at runtime on Perlmutter with signac 2.3.0 before documenting.

**No changes to other files:** This design does not modify `init_project.py`, `explore_workspace.py`, `simulate.py`, or any files outside `01-signac/example1-parameter-space/`.
