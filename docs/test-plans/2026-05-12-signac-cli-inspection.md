# Human Test Plan: signac CLI Inspection

## Prerequisites

- NERSC Perlmutter login node or compute node
- Conda environment activated with `signac` installed and available on `$PATH`
- Repository cloned and working directory set to the project root
- `python3 test_examples.py` in `01-signac/` passes (confirms file existence and syntax)

## Phase 1: Script Execution (AC1.1, AC3.1)

| Step | Action | Expected |
|------|--------|----------|
| 1.1 | `cd 01-signac/example1-parameter-space` | Working directory changes successfully |
| 1.2 | `rm -rf workspace/ .signac/` | Clean state -- no pre-existing workspace |
| 1.3 | `python init_project.py` | Completes without error. Creates `.signac/` directory and `workspace/` with exactly 9 subdirectories |
| 1.4 | `ls workspace/ \| wc -l` | Output: `9` |
| 1.5 | `bash inspect_workspace.sh` | Script runs to completion with no error messages or Python tracebacks |
| 1.6 | `echo $?` | Output: `0` |

**Validates:** AC1.1 (script runs without errors), AC3.1 (script works with only `init_project.py` workspace, no other setup required)

## Phase 2: Script Output Inspection (AC1.2, AC1.3, AC1.4, AC1.5)

Capture the full output first:

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | `bash inspect_workspace.sh > /tmp/inspect_output.txt 2>&1` | File created with script output |

**AC1.2 -- Parameter Schema:**

| Step | Action | Expected |
|------|--------|----------|
| 2.2 | Examine the "1. Project Parameter Schema" section of the output | Section header "=== 1. Project Parameter Schema ===" is present |
| 2.3 | Look for `temperature` line | Line shows `temperature` with values `300`, `400`, `500` |
| 2.4 | Look for `pressure` line | Line shows `pressure` with values `1.0`, `10.0`, `100.0` |

**AC1.3 -- Filtered Job IDs:**

| Step | Action | Expected |
|------|--------|----------|
| 2.5 | Examine the "2. Find Jobs by Parameter Value" section of the output | Section header "=== 2. Find Jobs by Parameter Value ===" is present |
| 2.6 | Count lines that are 32-character hexadecimal strings | Exactly 3 job IDs appear (one per pressure value: 1.0, 10.0, 100.0, all with temperature=300) |
| 2.7 | Cross-validate: run `signac find temperature 300 \| wc -l` | Output: `3` |

**AC1.4 -- Directory Path:**

| Step | Action | Expected |
|------|--------|----------|
| 2.8 | Examine the "3. Look Up Directory" section of the output | Section header present |
| 2.9 | Look for a 32-character hex job ID printed by the script | A single 32-character hex string appears |
| 2.10 | Look for a line matching `workspace/<hex>/` | The path `workspace/<job_id>/` is printed |
| 2.11 | Verify the directory exists: `JOB_ID=$(signac job '{"temperature": 300, "pressure": 1.0}')` then `test -d "workspace/$JOB_ID" && echo PASS` | Output: `PASS` |

**AC1.5 -- Raw Statepoint JSON:**

| Step | Action | Expected |
|------|--------|----------|
| 2.12 | Examine the "4. Read the Raw Statepoint File" section of the output | Section header present |
| 2.13 | Verify the output contains valid JSON with `"temperature": 300` | JSON blob visible containing `"temperature": 300` |
| 2.14 | Verify the output contains `"pressure": 1.0` | JSON blob visible containing `"pressure": 1.0` |
| 2.15 | Cross-validate: `cat "workspace/$JOB_ID/signac_statepoint.json" \| python3 -m json.tool` | Valid JSON output with both key-value pairs |

## Phase 3: README Content Inspection (AC2.1, AC2.2, AC2.3, AC2.4)

File under test: `01-signac/example1-parameter-space/README.md`

**AC2.4 -- Step 4 in "Running This Example":**

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | Open README.md and locate the "Running This Example" section | Section exists with numbered steps |
| 3.2 | Verify steps 1-3 are unchanged | All three original steps are present and unmodified |
| 3.3 | Verify step 4 exists after step 3 | Step numbered `4.` is present |
| 3.4 | Verify step 4 contains `bash inspect_workspace.sh` in a code block | Code block with `bash inspect_workspace.sh` appears under step 4 |
| 3.5 | Verify step 4 has a description referencing CLI tools | Description text mentions `signac schema`, `signac find`, `signac job`, or "CLI tools" |

**AC2.1 -- "Inside the Workspace" section with on-disk structure:**

| Step | Action | Expected |
|------|--------|----------|
| 3.6 | Locate a section headed "Inside the Workspace" | Heading `## Inside the Workspace` exists |
| 3.7 | Look for file tree or structural description | A code block shows `.signac/config` as part of the directory structure |
| 3.8 | Verify statepoint file shown | Code block mentions `workspace/<hash>/signac_statepoint.json` |
| 3.9 | Verify hash explanation | Text explains that the hash is computed from the statepoint parameters |

**AC2.2 -- CLI commands reference:**

| Step | Action | Expected |
|------|--------|----------|
| 3.10 | Find a CLI commands code block in "Inside the Workspace" | A fenced code block with bash commands is present |
| 3.11 | Verify `signac schema` appears with description | Command shown with description of showing parameter keys and value ranges |
| 3.12 | Verify `signac find` appears with example | `signac find temperature 300` or equivalent is present |
| 3.13 | Verify `signac job` appears with example | `signac job '{"temperature": 300, "pressure": 1.0}'` or equivalent is present |

**AC2.3 -- `signac view` description:**

| Step | Action | Expected |
|------|--------|----------|
| 3.14 | Find a paragraph about `signac view` in "Inside the Workspace" | Text mentions the `signac view` command |
| 3.15 | Verify it describes symlinked hierarchy | Description mentions "symlinked" tree or "human-readable" directory hierarchy |
| 3.16 | Verify an example path structure is given | Text includes a path pattern like `view/temperature/300/pressure/1.0/job -> workspace/<hash>` |

## Phase 4: Section Ordering

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | Verify README section order | Sections appear in this order: "Running This Example" (4 steps), then "What Happens Under the Hood", then "Inside the Workspace", then "Next Steps" |

## End-to-End: Clean-State Full Walkthrough

**Purpose:** Validates that a user following the tutorial from scratch can run the inspection script with no hidden dependencies or prior state.

1. Start in a clean shell with the conda environment activated.
2. `cd 01-signac/example1-parameter-space`
3. `rm -rf workspace/ .signac/` to ensure clean state.
4. `python init_project.py` -- should complete without error and create 9 job directories.
5. `bash inspect_workspace.sh` -- should complete with exit code 0.
6. Visually inspect all four numbered output sections for correctness (schema shows temperature + pressure ranges, 3 filtered jobs, a valid directory path, and valid JSON).
7. No other scripts (`explore_workspace.py`, `simulate.py`) were required between steps 4 and 5.

**Pass:** All output criteria met. Exit code 0. No manual intervention between `init_project.py` and `inspect_workspace.sh`.

## Traceability

| Acceptance Criterion | Automated Test | Manual Step |
|----------------------|----------------|-------------|
| AC1.1 Script runs without errors | None (by design) | Phase 1 steps 1.5-1.6 |
| AC1.2 Output shows parameter schema | None (by design) | Phase 2 steps 2.2-2.4 |
| AC1.3 Output shows filtered job IDs | None (by design) | Phase 2 steps 2.5-2.7 |
| AC1.4 Output shows directory path | None (by design) | Phase 2 steps 2.8-2.11 |
| AC1.5 Output shows raw statepoint JSON | None (by design) | Phase 2 steps 2.12-2.15 |
| AC2.1 README describes on-disk structure | None (by design) | Phase 3 steps 3.6-3.9 |
| AC2.2 README includes CLI commands reference | None (by design) | Phase 3 steps 3.10-3.13 |
| AC2.3 README includes signac view description | None (by design) | Phase 3 steps 3.14-3.16 |
| AC2.4 README adds step 4 | None (by design) | Phase 3 steps 3.1-3.5 |
| AC3.1 Script works with only init_project.py workspace | None (by design) | End-to-End walkthrough |

**Estimated human verification time:** 5-10 minutes for the complete walkthrough.
