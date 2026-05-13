# Human Test Plan: Maestro Perlmutter Slurm Fix

**Implementation plan:** `docs/implementation-plans/2026-05-13-maestro-120-upgrade/`
**Test requirements:** `docs/implementation-plans/2026-05-13-maestro-120-upgrade/test-requirements.md`
**Generated:** 2026-05-13

## Prerequisites

- Perlmutter login node access (SSH to `perlmutter.nersc.gov`)
- Active NERSC account with allocation (the workflow uses `ntrain4` by default)
- Python environment with `maestrowf` installed:
  ```bash
  module load conda
  conda activate wf-seminar
  ```
- Repository cloned at `/global/u1/w/warndt/workflow_tutorial_research`

## Phase 1: Pre-flight and Dry-Run Verification (~5 minutes)

| Step | Action | Expected |
|------|--------|----------|
| 1.1 | `cd /global/u1/w/warndt/workflow_tutorial_research/02-maestro/example3-slurm-config` | Working directory changes successfully |
| 1.2 | `grep 'bank:' workflow.yaml` | Output: `bank: ntrain4` (single line) |
| 1.3 | Remove any prior dry-run directories: `rm -rf slurm-config_*` | Clean slate for fresh dry-run |
| 1.4 | `maestro run --dry --autoyes workflow.yaml` | Command exits 0, creates `slurm-config_<timestamp>/` directory |
| 1.5 | `LATEST=$(ls -td slurm-config_* \| head -1)` | Variable set to the new timestamped directory |
| 1.6 | `grep '#SBATCH --qos=debug' "$LATEST/compute/compute.slurm.sh"` | Prints line containing `#SBATCH --qos=debug` |
| 1.7 | `grep '#SBATCH --constraint=cpu' "$LATEST/compute/compute.slurm.sh"` | Prints line containing `#SBATCH --constraint=cpu` |
| 1.8 | `grep '#SBATCH --account=ntrain4' "$LATEST/compute/compute.slurm.sh"` | Prints line containing `#SBATCH --account=ntrain4` |
| 1.9 | `sbatch --test-only "$LATEST/compute/compute.slurm.sh"` | Exits 0 or prints job submission estimate. No "does not match any supported policy" error. |

## Phase 2: No-Regression Verification (~3 minutes)

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | `cd /global/u1/w/warndt/workflow_tutorial_research` | Return to repo root |
| 2.2 | `git diff HEAD -- 02-maestro/example1-simple-dag/workflow.yaml` | No output (empty diff) |
| 2.3 | `git diff HEAD -- 02-maestro/example2-param-sweeps/workflow.yaml` | No output (empty diff) |
| 2.4 | `cd 02-maestro/example1-simple-dag && maestro run --dry --autoyes workflow.yaml && echo "example1 OK"` | Prints "example1 OK", exits 0 |
| 2.5 | `cd /global/u1/w/warndt/workflow_tutorial_research/02-maestro/example2-param-sweeps && maestro run --dry --autoyes workflow.yaml && echo "example2 OK"` | Prints "example2 OK", exits 0 |

## Phase 3: Documentation Verification (~2 minutes)

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | `grep 'qos: debug' 02-maestro/example3-slurm-config/README.md` | At least one match in the batch block snippet |
| 3.2 | `grep 'does not match any supported policy' 02-maestro/example3-slurm-config/README.md` | At least one match in the troubleshooting section |
| 3.3 | Cross-reference bank, qos, and constraint values between README and workflow.yaml | All values match between the two files |

## Phase 4: Negative Test -- Constraint Removal (~5 minutes)

Purpose: Confirm that omitting `#SBATCH --constraint=cpu` causes Slurm rejection on Perlmutter.

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | `cd /global/u1/w/warndt/workflow_tutorial_research/02-maestro/example3-slurm-config` | Enter example3 directory |
| 4.2 | `cp workflow.yaml workflow.yaml.bak` | Backup created |
| 4.3 | Edit `workflow.yaml`: remove the `#SBATCH --constraint=cpu` line from the compute step's cmd block | Line removed, file saved |
| 4.4 | `maestro run --dry --autoyes workflow.yaml` | Dry-run succeeds (Maestro does not validate Slurm policies) |
| 4.5 | `LATEST=$(ls -td slurm-config_* \| head -1)` | Variable set to new dry-run directory |
| 4.6 | `grep 'constraint' "$LATEST/compute/compute.slurm.sh"` | No output (constraint directive is absent) |
| 4.7 | `sbatch --test-only "$LATEST/compute/compute.slurm.sh"` | Fails with "does not match any supported policy" or similar rejection |
| 4.8 | `mv workflow.yaml.bak workflow.yaml` | Original file restored |
| 4.9 | `rm -rf "$LATEST"` | Clean up test dry-run directory |

## Phase 5: Live Slurm Submission (~10 minutes including queue wait)

Purpose: End-to-end validation that the workflow actually runs on Perlmutter through Slurm.

| Step | Action | Expected |
|------|--------|----------|
| 5.1 | `cd /global/u1/w/warndt/workflow_tutorial_research/02-maestro/example3-slurm-config` | Enter example3 directory |
| 5.2 | Verify or update `bank` in `workflow.yaml` to your active NERSC account | `bank:` line shows your account |
| 5.3 | `maestro run --autoyes workflow.yaml` | Maestro launches study, prints submission info |
| 5.4 | `squeue -u $USER` | Compute job appears in queue (PENDING or RUNNING) |
| 5.5 | Wait for job to complete (debug QOS typically schedules within 1-2 minutes) | Job disappears from `squeue` output |
| 5.6 | `LATEST=$(ls -td slurm-config_* \| head -1)` | Variable set to latest run directory |
| 5.7 | `ls "$LATEST/setup/"` | Contains `input.txt` |
| 5.8 | `ls "$LATEST/compute/"` | Contains `compute.slurm.sh`, `result.txt`, `compute.out`, `compute.err` |
| 5.9 | `ls "$LATEST/postprocess/"` | Contains `summary.txt` |
| 5.10 | `cat "$LATEST/postprocess/summary.txt"` | Contains result line with input sample count and computed result |
| 5.11 | `cat "$LATEST/compute/compute.err"` | Empty or contains only non-error messages |
| 5.12 | `cat "$LATEST/compute/compute.out"` | Contains "Starting computation" and "Computation complete" messages |

## Human Verification Required

| Criterion | Why Manual | Steps |
|-----------|------------|-------|
| AC1.5: Omitting `--constraint=cpu` causes Slurm rejection | Requires destructive edit, Slurm interaction, and file restoration | Phase 4 steps 4.1-4.9 |
| AC2.2: README explains constraint workaround | Requires reading comprehension for technical accuracy | Read README "Constraint Workaround" section, verify it covers: (1) Perlmutter requires constraint, (2) error without it, (3) Maestro has no native field, (4) cmd embedding workaround, (5) why it works |
| AC4.1: Test plan covers dry-run for all three examples | Meta-criterion about this document | Confirm Phase 1 covers example3, Phase 2 covers examples 1 and 2 |
| AC4.2: Test plan includes live Slurm submission | Meta-criterion about this document | Confirm Phase 5 provides full submission steps |
| AC4.3: Test plan verifies generated Slurm directives | Meta-criterion about this document | Confirm Phase 1 steps 1.6-1.9 check all directives |
| AC4.4: All steps completable within 30 minutes | Requires timing full execution | Estimated total: ~25 minutes |

## Traceability

| Acceptance Criterion | Test Phase |
|----------------------|------------|
| AC1.1: `#SBATCH --qos=debug` in generated script | Phase 1, step 1.6 |
| AC1.2: `#SBATCH --constraint=cpu` in generated script | Phase 1, step 1.7 |
| AC1.3: `sbatch --test-only` accepts script | Phase 1, step 1.9 |
| AC1.4: `bank: ntrain4` in workflow.yaml | Phase 1, step 1.2 |
| AC1.5: Omitting constraint causes rejection | Phase 4, steps 4.1-4.9 |
| AC2.1: README has `qos: debug` | Phase 3, step 3.1 |
| AC2.2: README explains constraint workaround | Human Verification |
| AC2.3: README troubleshooting has policy error | Phase 3, step 3.2 |
| AC2.4: README snippets match workflow.yaml | Phase 3, step 3.3 |
| AC3.1: example1 zero diff | Phase 2, step 2.2 |
| AC3.2: example2 zero diff | Phase 2, step 2.3 |
| AC3.3: Dry-run succeeds for examples 1 and 2 | Phase 2, steps 2.4-2.5 |
| AC4.1: Test plan covers all three dry-runs | Human Verification |
| AC4.2: Test plan includes live submission | Phase 5 |
| AC4.3: Test plan verifies Slurm directives | Human Verification |
| AC4.4: All steps under 30 minutes | Human Verification |
