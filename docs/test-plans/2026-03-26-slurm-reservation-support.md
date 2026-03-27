# Human Test Plan: SLURM Reservation Support

**Feature:** SLURM reservation support for GNU Parallel example 3
**Implementation Plan:** docs/implementation-plans/2026-03-26-slurm-reservation-support/
**Test Requirements:** docs/implementation-plans/2026-03-26-slurm-reservation-support/test-requirements.md
**Automated Coverage:** 17/22 acceptance criteria (77%)
**Manual Coverage Required:** 5/22 acceptance criteria (23%)

## Prerequisites

- SSH access to NERSC Perlmutter (`ssh perlmutter.nersc.gov`)
- A valid NERSC project account (to replace `<your_account>` placeholder)
- Terminal access to the working directory: `/global/u1/w/warndt/workflow_tutorial_research/00-gnu-parallel/example3-slurm-integration/`
- Automated verification passing: `./verify_reservation_support.sh` exits 0

## Phase 1: Automated Verification Baseline

| Step | Action | Expected |
|------|--------|----------|
| 1.1 | `cd /global/u1/w/warndt/workflow_tutorial_research/00-gnu-parallel/example3-slurm-integration` | Directory exists and contains `submit.sh`, `submit_parallel_job.sh`, `verify_reservation_support.sh`, `README.md` |
| 1.2 | `chmod +x verify_reservation_support.sh submit.sh` | Both scripts become executable |
| 1.3 | `./verify_reservation_support.sh` | Script runs to completion, prints "ALL VERIFICATION CHECKS PASSED", exits with code 0 |

## Phase 2: Interactive Training Mode Observation (AC2.5)

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | `export NERSC_TRAINING_RESERVATION=nonexistent_test_12345` | Variable set in current shell |
| 2.2 | `./submit.sh` | Observe the following output **in this order**: (1) "Training event mode detected" banner with reservation name and account, (2) "Executing: sbatch --reservation=nonexistent_test_12345 --account=ntrain4 submit_parallel_job.sh" line appears **before** any sbatch error output, (3) sbatch error message about invalid reservation. The "Executing:" line must be visible before the sbatch result. |
| 2.3 | `unset NERSC_TRAINING_RESERVATION` | Clean up |

## Phase 3: Live SLURM Error Messages (AC3.1, AC3.2)

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | `export NERSC_TRAINING_RESERVATION=invalid_reservation_name_12345` | Variable set |
| 3.2 | `./submit.sh` | sbatch fails. stderr contains a message matching `Invalid reservation name` or similar SLURM reservation error. The wrapper's exit code is non-zero (`echo $?` confirms). |
| 3.3 | `unset NERSC_TRAINING_RESERVATION` | Clean up |
| 3.4 | (AC3.2) If an expired reservation name is available from a past training event, set it: `export NERSC_TRAINING_RESERVATION=<expired_name>` | Variable set |
| 3.5 | `./submit.sh` | sbatch fails. stderr contains `Reservation ... is not usable` or equivalent SLURM expiration message. If no expired reservation is available, document this as "deferred -- requires expired reservation" and note that SLURM documentation confirms this behavior. |
| 3.6 | `unset NERSC_TRAINING_RESERVATION` | Clean up |

## Phase 4: Backward Compatibility -- Live Submission (AC4.1, AC4.4)

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | Edit `submit_parallel_job.sh` line 7: replace `<your_account>` with your valid NERSC account (e.g., `m1234`) | Account placeholder replaced |
| 4.2 | `unset NERSC_TRAINING_RESERVATION` (ensure it is not set) | Variable cleared |
| 4.3 | `sbatch submit_parallel_job.sh` | Job submits successfully. Output: `Submitted batch job <JOBID>`. Confirm with `squeue -u $USER` that the job appears in the queue. |
| 4.4 | `export NERSC_TRAINING_RESERVATION=some_value` | Variable set in shell |
| 4.5 | `sbatch submit_parallel_job.sh` (direct sbatch, NOT `./submit.sh`) | Job submits successfully. The reservation variable does NOT affect direct sbatch because `NERSC_TRAINING_RESERVATION` is a custom variable that SLURM does not recognize. Confirm with `squeue -u $USER` that the job runs in the default partition, not a reservation. |
| 4.6 | `unset NERSC_TRAINING_RESERVATION` | Clean up |
| 4.7 | Restore `submit_parallel_job.sh` line 7 to `<your_account>` | Undo the edit to keep the repository clean |

## End-to-End: Full Training Event Workflow

**Purpose:** Validate the complete instructor-to-student workflow as described in the README, confirming that all pieces work together on a live Perlmutter session.

**Steps:**

1. Start a fresh login shell on Perlmutter.
2. Navigate to `00-gnu-parallel/example3-slurm-integration/`.
3. Read the "Training Event Setup" section of README.md. Follow the documented instructions exactly as a student would.
4. `export NERSC_TRAINING_RESERVATION=<actual_reservation_name>` (if a valid training reservation is available; otherwise use a fake name and expect sbatch failure).
5. Run `./submit.sh`.
6. Verify the training mode banner prints with the correct reservation name and `ntrain4` account.
7. Verify the "Executing:" line shows the complete sbatch command with `--reservation` and `--account` flags.
8. If a valid reservation was used, verify the job enters the queue with `squeue -u $USER` and confirm it runs against the reservation.
9. `unset NERSC_TRAINING_RESERVATION`.
10. Run `./submit.sh` again.
11. Verify the "Regular submission mode" banner prints and the sbatch command has no `--reservation` or `--account` flags.

## Human Verification Required

| Criterion | Why Manual | Steps |
|-----------|------------|-------|
| AC2.5 - User sees sbatch command before submission completes | Temporal ordering of output cannot be verified by capturing stdout as a string; requires interactive observation | Phase 2 steps 2.1-2.2: Run `./submit.sh` with a reservation set and visually confirm the "Executing:" line appears before the sbatch result (success or error) |
| AC3.1 - Invalid reservation produces SLURM "Invalid reservation name" error | The specific error string comes from the live SLURM scheduler, not from submit.sh | Phase 3 steps 3.1-3.3: Run with a nonexistent reservation name and check stderr for the SLURM error message |
| AC3.2 - Expired reservation produces SLURM "not usable" error | Requires an actual expired SLURM reservation that cannot be created on demand | Phase 3 steps 3.4-3.6: Run with an expired reservation name if one is available; otherwise document as deferred |
| AC4.1 - Direct sbatch still works unchanged | Automated test only validates bash syntax; actual sbatch acceptance requires live scheduler and valid account | Phase 4 steps 4.1-4.3: Replace account placeholder, submit directly with `sbatch submit_parallel_job.sh`, confirm job enters queue |
| AC4.4 - Direct sbatch unaffected by NERSC_TRAINING_RESERVATION variable | Requires live scheduler to confirm job does not land in a reservation queue when the env var is set | Phase 4 steps 4.4-4.6: Set env var, submit directly (bypassing wrapper), confirm job runs in default partition |

## Traceability

| Acceptance Criterion | Automated Test | Manual Step |
|----------------------|----------------|-------------|
| AC1.1 - reservation flag added | verify_reservation_support.sh line 104 | -- |
| AC1.2 - account flag added | verify_reservation_support.sh line 104 | -- |
| AC1.3 - no reservation when unset | verify_reservation_support.sh lines 137-142 | -- |
| AC1.4 - no account when unset | verify_reservation_support.sh lines 145-150 | -- |
| AC1.5 - empty string as unset | verify_reservation_support.sh lines 157-174 | -- |
| AC2.1 - training mode message | verify_reservation_support.sh lines 80-85 | -- |
| AC2.2 - reservation name and account printed | verify_reservation_support.sh lines 88-101 | -- |
| AC2.3 - regular mode message | verify_reservation_support.sh lines 121-126 | -- |
| AC2.4 - sbatch command printed | verify_reservation_support.sh lines 104, 129 | -- |
| AC2.5 - command visible before submission | -- | Phase 2, step 2.2 |
| AC3.1 - invalid reservation error | -- | Phase 3, steps 3.1-3.3 |
| AC3.2 - expired reservation error | -- | Phase 3, steps 3.4-3.6 |
| AC3.3 - exit code propagation | verify_reservation_support.sh lines 180-194 | -- |
| AC4.1 - direct sbatch works | verify_reservation_support.sh lines 214 (syntax only) | Phase 4, steps 4.1-4.3 |
| AC4.2 - submit_parallel_job.sh unchanged | verify_reservation_support.sh lines 28-40 | -- |
| AC4.3 - examples 1 and 2 unchanged | verify_reservation_support.sh lines 225-241 | -- |
| AC4.4 - direct sbatch unaffected by env var | verify_reservation_support.sh lines 256-270 (content only) | Phase 4, steps 4.4-4.6 |
| AC5.1 - README Training Event Setup section | verify_reservation_support.sh lines 282-294 | -- |
| AC5.2 - README wrapper option first | verify_reservation_support.sh lines 297-309 | -- |
| AC5.3 - README lists submit.sh | verify_reservation_support.sh lines 312-317 | -- |
| AC5.4 - README explains both mode outputs | verify_reservation_support.sh lines 320-332 | -- |
| AC5.5 - README documents fail-fast | verify_reservation_support.sh lines 335-340 | -- |
