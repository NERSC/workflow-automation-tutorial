# SLURM Reservation Support for Example3 Design

## Summary

This design adds SLURM reservation support to the GNU Parallel tutorial's batch submission example (`example3-slurm-integration`) to streamline NERSC training events. A new wrapper script (`submit.sh`) detects the presence of the `NERSC_TRAINING_RESERVATION` environment variable and automatically constructs the appropriate `sbatch` command with reservation and training account flags when in training mode, or a standard `sbatch` command for regular usage. This approach follows the established NERSC training event pattern (observed in SC24 and Deep Learning at Scale events) where attendees run a simplified command instead of manually specifying reservation details. The wrapper provides full transparency by printing the exact `sbatch` command before execution, serving the educational purpose of the seminar.

The implementation maintains strict backward compatibility — the existing batch script (`submit_parallel_job.sh`) remains unchanged and can still be invoked directly via `sbatch`. Examples 1 and 2 are unaffected, preserving their login-node-safe design. Invalid or expired reservations fail immediately with clear Slurm error messages, preventing silent wrong-queue submissions. The README documentation is updated to present both training event and regular usage workflows, with the wrapper approach recommended for its simplicity during training sessions.

## Definition of Done

Add SLURM reservation support to `00-gnu-parallel/example3-slurm-integration` for NERSC training events. When `NERSC_TRAINING_RESERVATION` environment variable is set, jobs automatically use the specified reservation and ntrain4 training account. When unset, jobs submit in regular mode. Implementation uses a helper wrapper script (`submit.sh`) that constructs the appropriate sbatch command with full transparency. Invalid/expired reservations fail immediately with clear Slurm errors. Examples 1 and 2 remain unchanged (login-node-safe). All changes are backward compatible with existing workflows. README documentation updated to show both training event and regular usage paths.

## Acceptance Criteria

### slurm-reservation-support.AC1: Reservation detection and usage
- **slurm-reservation-support.AC1.1 Success:** When `NERSC_TRAINING_RESERVATION` is set, submit.sh adds `--reservation=$NERSC_TRAINING_RESERVATION` to sbatch command
- **slurm-reservation-support.AC1.2 Success:** When `NERSC_TRAINING_RESERVATION` is set, submit.sh adds `--account=ntrain4` to sbatch command
- **slurm-reservation-support.AC1.3 Success:** When `NERSC_TRAINING_RESERVATION` is unset, submit.sh omits `--reservation` flag
- **slurm-reservation-support.AC1.4 Success:** When `NERSC_TRAINING_RESERVATION` is unset, submit.sh omits `--account` flag (user must provide via script)
- **slurm-reservation-support.AC1.5 Edge:** When `NERSC_TRAINING_RESERVATION=""` (empty string), treated as unset (no reservation flag)

### slurm-reservation-support.AC2: Transparent operation
- **slurm-reservation-support.AC2.1 Success:** submit.sh prints "Training event mode detected" message when reservation is set
- **slurm-reservation-support.AC2.2 Success:** submit.sh prints reservation name and account when in training mode
- **slurm-reservation-support.AC2.3 Success:** submit.sh prints "Regular submission mode" message when reservation is unset
- **slurm-reservation-support.AC2.4 Success:** submit.sh prints exact sbatch command before executing it
- **slurm-reservation-support.AC2.5 Success:** User can see what sbatch command will run before submission completes

### slurm-reservation-support.AC3: Error handling
- **slurm-reservation-support.AC3.1 Failure:** Invalid reservation name causes sbatch to fail with "Invalid reservation name" error
- **slurm-reservation-support.AC3.2 Failure:** Expired reservation causes sbatch to fail with "Reservation ... is not usable" error
- **slurm-reservation-support.AC3.3 Success:** Wrapper propagates sbatch exit code to caller (non-zero on failure)

### slurm-reservation-support.AC4: Backward compatibility
- **slurm-reservation-support.AC4.1 Success:** Direct `sbatch submit_parallel_job.sh` continues to work unchanged
- **slurm-reservation-support.AC4.2 Success:** submit_parallel_job.sh requires no modifications (unchanged file)
- **slurm-reservation-support.AC4.3 Success:** Examples 1 and 2 remain unchanged (no wrapper added)
- **slurm-reservation-support.AC4.4 Success:** Existing workflows using direct sbatch are unaffected by NERSC_TRAINING_RESERVATION variable

### slurm-reservation-support.AC5: Documentation completeness
- **slurm-reservation-support.AC5.1 Success:** README includes "Training Event Setup" section with environment variable export example
- **slurm-reservation-support.AC5.2 Success:** README "How to Run" presents wrapper option first, direct sbatch second
- **slurm-reservation-support.AC5.3 Success:** README "Files in This Example" lists submit.sh
- **slurm-reservation-support.AC5.4 Success:** README explains expected output for both training and regular modes
- **slurm-reservation-support.AC5.5 Success:** README documents fail-fast behavior for invalid reservations

## Glossary

- **SLURM**: Simple Linux Utility for Resource Management, the workload manager and job scheduler used on NERSC's Perlmutter supercomputer
- **Reservation**: A SLURM feature that reserves compute resources for specific users or groups during a defined time window, commonly used for training events to guarantee resource availability
- **sbatch**: SLURM command for submitting batch job scripts to the scheduler
- **ntrain4**: NERSC's training account used across educational events, grants access to reserved resources during training sessions
- **Wrapper script**: A script that encapsulates another command with additional logic (here, `submit.sh` wraps `sbatch` with reservation detection)
- **Login node**: Interactive node where users log in to NERSC systems; safe for light tasks but not for parallel computation
- **Batch submission**: Process of submitting computational jobs to SLURM's queue for execution on compute nodes
- **Fail-fast**: Design principle where errors are detected and reported immediately at the point of occurrence rather than silently continuing
- **Backward compatibility**: Property where new changes do not break existing workflows or require modifications to existing code
- **Environment variable**: Shell variable (like `NERSC_TRAINING_RESERVATION`) that controls program behavior without modifying code

## Architecture

Helper wrapper script pattern that detects reservation environment variable and constructs appropriate sbatch command.

**Components:**
- `submit.sh` — wrapper script in `00-gnu-parallel/example3-slurm-integration/` that checks `$NERSC_TRAINING_RESERVATION` and builds sbatch command with conditional flags
- `submit_parallel_job.sh` — existing batch script, unchanged for backward compatibility
- Updated README.md — documentation showing both training event and regular workflows

**Data Flow:**
1. User sets `NERSC_TRAINING_RESERVATION=<name>` (optional, one-time for training events)
2. User executes `./submit.sh`
3. Wrapper detects environment variable state
4. If set: constructs `sbatch --reservation=$NERSC_TRAINING_RESERVATION --account=ntrain4 submit_parallel_job.sh`
5. If not set: constructs `sbatch submit_parallel_job.sh` (user provides account via script or flag)
6. Wrapper prints exact sbatch command for transparency
7. Wrapper executes sbatch command
8. Slurm validates reservation (if specified) and either accepts job or fails with clear error

**Key Architectural Decisions:**
- **Wrapper abstraction** matches NERSC training event pattern (SC24, DL-at-Scale) for minimal participant friction
- **Transparent operation** (always print sbatch command) serves educational purpose of seminar
- **Fail-fast** on invalid reservations prevents silent wrong-queue submissions
- **Zero modification** to submit_parallel_job.sh preserves backward compatibility
- **Scoped to example3** keeps examples 1 and 2 login-node-safe as intended

## Existing Patterns

**NERSC Training Event Pattern (from research):**
Investigation of NERSC training repositories (SC24 Deep Learning Tutorial, Deep Learning at Scale Training) found consistent wrapper abstraction pattern:
- Wrapper scripts handle reservation and account details
- Users run simplified command (`./submit.sh` vs `sbatch --reservation=... --account=... script.sh`)
- Training account `ntrain4` used across events
- Reservation names follow descriptive patterns: `sc24_dl_tutorial_1`, `dlscale_training_1`

**Tutorial Conventions:**
- Examples 1 and 2 use `NJOBS=${SLURM_CPUS_ON_NODE:-2}` defensive pattern for login node safety
- Example 3 designed for batch submission only (no login node fallback)
- Account placeholder `<your_account>` in scripts prompts manual replacement

**This design follows:**
- NERSC training wrapper abstraction (reduces friction for attendees)
- Tutorial's ntrain4 account specification (from CLAUDE.md)
- Transparent operation principle (educational context)

**This design diverges:**
- Introduces wrapper script (examples 1-2 have no submission wrapper)
- Justification: Example3 is batch-only; wrapper serves training event use case without breaking regular workflow

## Implementation Phases

<!-- START_PHASE_1 -->
### Phase 1: Wrapper Script Creation

**Goal:** Create submit.sh wrapper with reservation detection and transparent sbatch command construction

**Components:**
- `00-gnu-parallel/example3-slurm-integration/submit.sh` — bash wrapper script with environment variable detection logic, conditional flag construction, command printing, and sbatch execution

**Dependencies:** None (first phase)

**Done when:**
- submit.sh exists and is executable
- Script correctly detects `$NERSC_TRAINING_RESERVATION` (set vs unset vs empty)
- With variable set: constructs `sbatch --reservation=$NERSC_TRAINING_RESERVATION --account=ntrain4 submit_parallel_job.sh`
- With variable unset: constructs `sbatch submit_parallel_job.sh`
- Prints mode detection message and full sbatch command before execution
- Executes sbatch command and propagates exit code
<!-- END_PHASE_1 -->

<!-- START_PHASE_2 -->
### Phase 2: Documentation Updates

**Goal:** Update README with training event setup section and revised usage instructions

**Components:**
- `00-gnu-parallel/example3-slurm-integration/README.md` — add "Training Event Setup" section, update "How to Run" with two-option structure (wrapper vs direct sbatch), update "Files in This Example" to include submit.sh

**Dependencies:** Phase 1 (submit.sh must exist to document)

**Done when:**
- README includes "Training Event Setup" section with NERSC_TRAINING_RESERVATION export example
- "How to Run" section presents "Option 1: Using submission wrapper (recommended)" first, "Option 2: Direct sbatch submission" second
- "Files in This Example" lists submit.sh with description
- Example commands show expected output for both training and regular modes
- Documentation explains fail-fast behavior for invalid/expired reservations
<!-- END_PHASE_2 -->

<!-- START_PHASE_3 -->
### Phase 3: Testing and Validation

**Goal:** Verify wrapper behavior across all edge cases and validate backward compatibility

**Components:**
- Manual testing of submit.sh with various environment states
- Verification that submit_parallel_job.sh still works via direct sbatch
- Edge case validation (empty string, invalid reservation name, expired reservation)

**Dependencies:** Phases 1 and 2 (wrapper and documentation complete)

**Done when:**
- Wrapper tested with `NERSC_TRAINING_RESERVATION` set to valid name (prints training mode, constructs correct command)
- Wrapper tested with `NERSC_TRAINING_RESERVATION` unset (prints regular mode, constructs sbatch without flags)
- Wrapper tested with `NERSC_TRAINING_RESERVATION=""` empty string (correctly treats as unset)
- Direct `sbatch submit_parallel_job.sh` still works (backward compatibility confirmed)
- README examples match actual output
- All changes committed to git
<!-- END_PHASE_3 -->

## Additional Considerations

**Error Handling:**
Invalid or expired reservations fail immediately at sbatch submission with Slurm's native error messages:
- Invalid name: `sbatch: error: Batch job submission failed: Invalid reservation name`
- Expired reservation: `sbatch: error: Batch job submission failed: Reservation ... is not usable`

This fail-fast behavior is intentional — it prevents silent wrong-queue submissions and provides clear feedback at the point of error.

**Backward Compatibility:**
- Existing workflows using `sbatch submit_parallel_job.sh` continue to work unchanged
- submit_parallel_job.sh requires no modifications
- Placeholder `<your_account>` still prompts manual replacement for non-training users
- No breaking changes to examples 1 or 2 (remain login-node-safe, no wrapper introduced)

**Training Event Integration:**
Instructors can provide one-time setup instruction in training materials:
```bash
export NERSC_TRAINING_RESERVATION=wf_seminar_2026
```
This can be added to attendees' `.bashrc` or run at session start. All subsequent submissions use `./submit.sh` with no additional configuration.
