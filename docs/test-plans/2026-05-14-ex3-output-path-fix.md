# Human Test Plan: Example 3 OUTPUT_PATH Fix

**Implementation plan:** `docs/implementation-plans/2026-05-14-ex3-output-path-fix/`
**HEAD SHA:** `dceef688cb1d795f328659ff97df081bbd94061a`
**Automated coverage:** 8/8 acceptance criteria PASS

---

## Prerequisites

- Repository checked out at commit `dceef688cb1d795f328659ff97df081bbd94061a` (or a branch containing it)
- Python 3.10+ available with `pyyaml` installed (for re-running automated checks if desired)
- Familiarity with Merlin variable resolution semantics (pass-1 `env.variables` substitution vs. pass-2 `$(WORKSPACE)` expansion)

---

## Phase 1: Verify spec.yaml structural correctness (visual inspection)

| Step | Action | Expected |
|------|--------|----------|
| 1.1 | Open `03-merlin/example3-massive-scale/spec.yaml` | File opens without error |
| 1.2 | Locate the `env:` block (lines 6-8). Confirm `OUTPUT_PATH: ./output` appears under `variables:` alongside `N_SAMPLES: 1000` | `OUTPUT_PATH` is a sibling of `N_SAMPLES` under `env.variables`, value is exactly `./output` |
| 1.3 | Locate the `train` step `cmd:` block (lines 29-33). Confirm `mkdir -p $(OUTPUT_PATH)` is the first command line, before `echo` and `python -c` | The mkdir line appears at the top of the cmd block, ensuring the output directory exists before any writes |
| 1.4 | Confirm the `python -c` line writes to `$(OUTPUT_PATH)/metrics.txt` (line 33) | Output path uses the variable, not a hardcoded absolute path |
| 1.5 | Locate the `aggregate` step `cmd:` block (lines 39-42). Confirm `mkdir -p $(OUTPUT_PATH)` is the first command line | mkdir precedes the echo and find commands |
| 1.6 | Confirm the echo line writes to `$(OUTPUT_PATH)/summary.txt` and the find line pipes to `$(OUTPUT_PATH)/summary.txt` | Both output lines use the relative variable |

---

## Phase 2: Verify README.md documentation (visual inspection)

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | Open `03-merlin/example3-massive-scale/README.md` | File opens without error |
| 2.2 | Scroll to the `## Running` section (line 19). Confirm it contains the `merlin run` and `merlin run-workers` commands | Running instructions are intact and unmodified |
| 2.3 | Scroll past Running to find `## Expected Output` (line 40). Confirm it appears after the Running section, not before it or inserted mid-section | Section ordering is correct |
| 2.4 | Read the directory tree in the Expected Output section. Confirm it shows: `massive_scale_<timestamp>/` as root, `train/` with numbered subdirectories each containing `output/metrics.txt`, and `aggregate/output/summary.txt` | Tree accurately reflects the output structure described by the spec |
| 2.5 | Read the explanatory text below the tree. Confirm it explains what `metrics.txt` and `summary.txt` contain | Prose matches the spec's `python -c` output and the echo/find aggregation |

---

## Phase 3: Logical correctness of find + OUTPUT_PATH interaction (AC2.2 human portion)

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | In `spec.yaml`, read the aggregate step's `find` command: `find $(WORKSPACE)/../ -name "metrics.txt"` | Command is present and unchanged from pre-fix version |
| 3.2 | Reason about Merlin's workspace layout: the aggregate step runs in `<study_root>/aggregate/<task_id>/`. Therefore `$(WORKSPACE)/../` resolves to `<study_root>/aggregate/`. `find` is recursive, so `find <study_root>/aggregate/../ ...` is equivalent to searching from `<study_root>/` | The find command reaches the study root |
| 3.3 | Confirm that the study root contains `train/` with all per-sample subdirectories (`00000001/` through `00001000/`) | Per the spec structure, all train task workspaces are under `<study_root>/train/` |
| 3.4 | Trace the train step output: each train task writes to `$(OUTPUT_PATH)/metrics.txt` which resolves to `./output/metrics.txt` relative to its workspace, producing `<study_root>/train/<sample_id>/output/metrics.txt` | Per-task files are in per-task directories, not a shared location |
| 3.5 | Confirm: `find <study_root>/ -name "metrics.txt"` will recursively find `train/<sample_id>/output/metrics.txt` for all 1000 samples | The find command will locate all per-task metric files |
| 3.6 | Cross-reference: Open `03-merlin/example1-distributed/spec.yaml`. Confirm it also uses `OUTPUT_PATH: ./output` in `env.variables` (line 7) | Same pattern used in example1, providing precedent |
| 3.7 | Cross-reference: Open `03-merlin/example2-fault-tolerance/spec.yaml`. Confirm it also uses `OUTPUT_PATH: ./output` in `env.variables` (line 7) | Same pattern used in example2, providing further precedent |

---

## End-to-End: Diff review

**Purpose:** Verify the diff contains exactly the intended changes and nothing else.

| Step | Action | Expected |
|------|--------|----------|
| E.1 | Run `git diff 58823d2..dceef68` from the repository root | Diff displays changes to exactly 2 files |
| E.2 | In `spec.yaml`: confirm exactly 3 lines added: (1) `OUTPUT_PATH: ./output` under `env.variables`, (2) `mkdir -p $(OUTPUT_PATH)` in train cmd, (3) `mkdir -p $(OUTPUT_PATH)` in aggregate cmd | Three insertions, no deletions, no modifications to existing lines |
| E.3 | In `README.md`: confirm the addition begins after the "~96 tasks execute in parallel" line and adds the complete `## Expected Output` section with directory tree | One contiguous block appended to the end of the file |
| E.4 | Confirm no whitespace-only changes, no changes to YAML indentation of existing lines, no changes to the `batch:`, `merlin:`, or `description:` blocks | Only the targeted structural additions are present |

---

## Human Verification Required

| Criterion | Why Manual | Steps |
|-----------|------------|-------|
| AC2.2 (logical correctness) | The automated check confirms the `find` command structure exists, but correctness requires reasoning about Merlin's runtime workspace layout — specifically that `$(WORKSPACE)/../` from the aggregate task reaches the study root containing all `train/<sample>/` directories. This is a semantic property of Merlin's directory structure that cannot be verified by static file inspection alone. | Phase 3, Steps 3.1-3.7 |

---

## Traceability

| Acceptance Criterion | Automated Test | Manual Step |
|----------------------|----------------|-------------|
| AC1.1 — OUTPUT_PATH in env.variables | YAML parse check: value is `./output` in `env.variables` | Phase 1, Step 1.2 |
| AC1.2 — mkdir in train step cmd | YAML parse check: mkdir index < python index | Phase 1, Steps 1.3-1.4 |
| AC1.3 — mkdir in aggregate step cmd | YAML parse check: mkdir index < echo index | Phase 1, Steps 1.5-1.6 |
| AC2.1 — OUTPUT_PATH expands to ./output | YAML parse check: variable defined + referenced in both cmds | Phase 3, Steps 3.1-3.4 |
| AC2.2 — find locates per-task files | Structure check: find pattern present in aggregate cmd | Phase 3, Steps 3.1-3.7 (full logical trace) |
| AC3.1 — Expected Output after Running | String position check: Running pos < Expected Output pos | Phase 2, Steps 2.2-2.3 |
| AC3.2 — Directory tree in Expected Output | String presence check: all required path elements present | Phase 2, Steps 2.4-2.5 |
| AC4.1 — No files outside example3 | Git diff name filter: no paths outside `03-merlin/example3-massive-scale/` | End-to-End, Steps E.1-E.4 |
