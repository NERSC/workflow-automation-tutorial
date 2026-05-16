# Human Test Plan: Merlin Cleanup Script

**Implementation plan:** `docs/implementation-plans/2026-05-15-merlin-cleanup/`
**HEAD commit:** `50e624c0fc49442554cad2d501b2737b8223b696`
**Automated coverage:** 14/14 ACs PASS

---

## Prerequisites

- Repository checked out at commit `50e624c` (or branch containing it)
- Access to the Perlmutter login node (for PSCRATCH-related real-environment confirmation)
- `03-merlin/cleanup.sh` exists and is executable (`chmod +x`)
- The composite verification script (from test-requirements.md) passes all 14 checks

---

## Phase 1: Style Conformance Review

| Step | Action | Expected |
|------|--------|----------|
| 1 | Open `03-merlin/cleanup.sh` and `02-maestro/cleanup.sh` side-by-side | Both files are visible for comparison |
| 2 | Verify `03-merlin/cleanup.sh` begins with `#!/bin/bash` on line 1 | Shebang present, matches other cleanup scripts |
| 3 | Verify comment block starts on line 2 with `# cleanup.sh - Remove runtime artifacts from 03-merlin examples` | Title line follows the `# cleanup.sh - Remove runtime artifacts from XX-name examples` pattern used by `00-gnu-parallel`, `01-signac`, and `02-maestro` |
| 4 | Verify the comment block includes a blank `#` line then describes restoration purpose: `# Restores the directory to its freshly-cloned state...` | Matches the phrasing in `01-signac/cleanup.sh` and `02-maestro/cleanup.sh` |
| 5 | Verify each artifact pattern is listed on its own commented line with a parenthetical explanation (e.g., `#   output/example1-distributed_<timestamp>/   (Merlin study workspace for example 1)`) | Five patterns listed: three output/ dirs, one PSCRATCH dir, one `__pycache__` |
| 6 | Verify `set -euo pipefail` appears AFTER the comment block, preceded by a blank line | Matches structural placement in all three existing cleanup scripts |
| 7 | Verify `SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)` appears on the line after `set -euo pipefail` | Same idiom used in `00-gnu-parallel`, `01-signac`, `02-maestro` |
| 8 | Verify the script ends with `echo "03-merlin cleaned."` as its final line | Matches the `echo "XX-name cleaned."` convention |
| 9 | Confirm overall comment density and spacing feel consistent with the three existing cleanup scripts | No excessive verbosity, no missing explanations; inline comments used sparingly for non-obvious logic (the PSCRATCH block and the `find` for `__pycache__` both have comments) |

---

## Phase 2: PSCRATCH Safety Review

| Step | Action | Expected |
|------|--------|----------|
| 1 | Read the PSCRATCH conditional block: `if [ -n "${PSCRATCH:-}" ]; then ... fi` | Guard uses `${PSCRATCH:-}` (parameter expansion with empty default) so `set -u` does not trigger |
| 2 | Mentally trace execution when `PSCRATCH=""`: the `-n` test evaluates to false, the `rm -rf` is never reached | No risk of `rm -rf /wf-seminar-merlin/...` when PSCRATCH is empty |
| 3 | Mentally trace execution when `PSCRATCH="/pscratch/sd/u/username"`: `rm -rf "$PSCRATCH/wf-seminar-merlin/example1-distributed_"*` expands correctly | Only removes timestamped subdirectories under the Merlin workspace; the `wf-seminar-merlin/` prefix prevents accidental broader deletion |
| 4 | Confirm the comment above the PSCRATCH block explains what OUTPUT_PATH in `example1-distributed/spec.yaml` generates there | The comment reads: `# Remove example1 scratch workspace on Perlmutter (OUTPUT_PATH in example1-distributed/spec.yaml)` |

---

## Phase 3: CLAUDE.md Update Review

| Step | Action | Expected |
|------|--------|----------|
| 1 | Run `git diff d2f982a 50e624c -- CLAUDE.md` | Shows two changes: "Last verified" date updated to 2026-05-16; new bullet about `cleanup.sh` in Conventions |
| 2 | Verify the new bullet reads: `- Sections 00-03 each have a 'cleanup.sh' that removes runtime artifacts to restore a freshly-cloned state` | Accurately reflects sections 00–03 having cleanup scripts (04-aiida does not) |
| 3 | Confirm the "Last verified" date update is appropriate for the scope of this change | Adding a new convention about cleanup scripts justifies a date bump |

---

## End-to-End: Fresh Clone Simulation

**Purpose:** Validate that the cleanup script restores `03-merlin/` to a state indistinguishable from a fresh clone after running all three examples.

| Step | Action | Expected |
|------|--------|----------|
| 1 | Create simulated artifacts: `mkdir -p 03-merlin/output/example1-distributed_20260515-100000 03-merlin/output/fault-tolerance-demo_20260515-100000 03-merlin/output/massive-scale_20260515-100000` | Three timestamped directories created |
| 2 | Create a nested `__pycache__`: `mkdir -p 03-merlin/example2-fault-tolerance/scripts/__pycache__ && touch 03-merlin/example2-fault-tolerance/scripts/__pycache__/foo.pyc` | Cache directory with a .pyc file present |
| 3 | Create a simulated PSCRATCH workspace: `export PSCRATCH_TEST=/tmp/e2e-merlin-$$; mkdir -p "$PSCRATCH_TEST/wf-seminar-merlin/example1-distributed_20260515-100000/steps"` | Scratch workspace with nested structure |
| 4 | Run: `PSCRATCH="$PSCRATCH_TEST" bash 03-merlin/cleanup.sh` | Script prints `03-merlin cleaned.` and exits 0 |
| 5 | Verify: `ls 03-merlin/output/` shows no timestamped directories | All example output removed |
| 6 | Verify: `find 03-merlin -name '__pycache__'` returns empty | All bytecode caches removed |
| 7 | Verify: `ls "$PSCRATCH_TEST/wf-seminar-merlin/"` shows the timestamped directory is gone | Scratch workspace cleaned |
| 8 | Cleanup: `rm -rf "$PSCRATCH_TEST"` | Test environment restored |

---

## Human Verification Required

| Criterion | Why Manual | Steps |
|-----------|------------|-------|
| merlin-cleanup.AC4.3 (comment format) | Scripted checks confirm all five patterns appear in the file but cannot verify formatting, ordering, or placement relative to `set -euo pipefail` | Open `03-merlin/cleanup.sh` and `02-maestro/cleanup.sh` side-by-side. Confirm: (a) comment block appears before `set -euo pipefail`, (b) each pattern is on its own commented line with alignment and parenthetical description, (c) the overall format matches the Maestro script's style |
| merlin-cleanup.AC4 (structural similarity) | "Style matches" is inherently subjective | Read all four cleanup scripts and confirm they follow the same structural template: shebang → comment block → `set -euo pipefail` → `SCRIPT_DIR` assignment → removal commands → optional `find` for `__pycache__` → final echo. The Merlin script adds a conditional PSCRATCH block, which is appropriate given its unique scratch-filesystem usage |

---

## Traceability

| Acceptance Criterion | Automated Test | Manual Step |
|----------------------|----------------|-------------|
| AC1.1 example1-distributed output removed | Composite check AC1.1 | End-to-End step 5 |
| AC1.2 fault-tolerance-demo output removed | Composite check AC1.2 | End-to-End step 5 |
| AC1.3 massive-scale output removed | Composite check AC1.3 | End-to-End step 5 |
| AC1.4 exits 0 with nothing to clean | Composite check AC1.4 | — |
| AC2.1 PSCRATCH workspace removed | Composite check AC2.1 | End-to-End step 7 |
| AC2.2 exits 0 with PSCRATCH unset | Composite check AC2.2 | — |
| AC2.3 exits 0 with PSCRATCH empty | Composite check AC2.3 | Phase 2 step 2 |
| AC3.1 \_\_pycache\_\_ removed recursively | Composite check AC3.1 | End-to-End step 6 |
| AC3.2 exits 0 with no \_\_pycache\_\_ | Composite check AC3.2 | — |
| AC4.1 invocable from any directory | Composite check AC4.1 | — |
| AC4.2 set -euo pipefail | Composite check AC4.2 | Phase 1 step 6 |
| AC4.3 patterns documented | Composite check AC4.3 | Phase 1 steps 3–5 (human format review) |
| AC4.4 final line prints message | Composite check AC4.4 | Phase 1 step 8 |
| AC4 (general style) | — | Phase 1 step 9, Human Verification row 2 |
