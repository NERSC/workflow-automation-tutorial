# Remove Reservation Wrapper Design

## Summary

This change removes a layer of automation that was introduced to simplify Slurm job submission for training-event attendees. The existing `submit.sh` wrapper reads a `NERSC_TRAINING_RESERVATION` environment variable and injects `--account=ntrain4` and `--reservation=<name>` flags into `sbatch` automatically; a companion script (`verify_reservation_support.sh`) tests that this mechanism works correctly. While convenient in isolation, this indirection adds custom machinery on top of a standard HPC workflow step, generating enough surface area to distract from what the example is actually teaching.

The replacement approach is purely subtractive. Both files are deleted, and two documents are updated: the example README's How to Run section is collapsed from a two-option branching structure into a single `sbatch` invocation with a short inline note for training attendees, and `CLAUDE.md` is updated to reflect the new manual-flag convention. Attendees at a training event pass `-A ntrain4 --reservation=<name>` directly on the `sbatch` command line — a pattern that Slurm supports natively and that teaches the actual mechanism rather than hiding it.

## Definition of Done

Remove the `submit.sh` env-var wrapper and `verify_reservation_support.sh` from `00-gnu-parallel/example3-slurm-integration/`. Replace the multi-option How to Run section in the example README with a single direct `sbatch` command, adding a brief note that training-event attendees supply `-A ntrain4 --reservation=<name>` as CLI flags. Update `CLAUDE.md` to reflect the manual-flag approach. All other files (including `submit_parallel_job.sh` and historical docs) remain unchanged.

## Acceptance Criteria

### remove-reservation-wrapper.AC1: Wrapper files are removed
- **remove-reservation-wrapper.AC1.1 Success:** `submit.sh` does not exist in `00-gnu-parallel/example3-slurm-integration/`
- **remove-reservation-wrapper.AC1.2 Success:** `verify_reservation_support.sh` does not exist in `00-gnu-parallel/example3-slurm-integration/`

### remove-reservation-wrapper.AC2: README How to Run is a single path
- **remove-reservation-wrapper.AC2.1 Success:** How to Run contains exactly one `sbatch submit_parallel_job.sh` invocation (no Option 1 / Option 2 split)
- **remove-reservation-wrapper.AC2.2 Success:** The inline training note `**Training event?**` with `-A ntrain4 --reservation=<name>` is present immediately after the main command block
- **remove-reservation-wrapper.AC2.3 Failure:** How to Run contains no reference to `NERSC_TRAINING_RESERVATION`, `./submit.sh`, or `export`

### remove-reservation-wrapper.AC3: README ancillary sections cleaned up
- **remove-reservation-wrapper.AC3.1 Success:** Training Event Setup section is absent from the README
- **remove-reservation-wrapper.AC3.2 Success:** `submit.sh` does not appear in the Files in This Example list
- **remove-reservation-wrapper.AC3.3 Success:** All other README sections (What This Demonstrates, Key Concepts, Sbatch Script Breakdown, etc.) are unchanged

### remove-reservation-wrapper.AC4: CLAUDE.md updated
- **remove-reservation-wrapper.AC4.1 Success:** CLAUDE.md line describing training reservation references `-A ntrain4 --reservation=<name>` CLI flags
- **remove-reservation-wrapper.AC4.2 Failure:** CLAUDE.md contains no reference to `NERSC_TRAINING_RESERVATION` or `submit.sh` wrappers
- **remove-reservation-wrapper.AC4.3 Success:** All other CLAUDE.md content is unchanged

## Glossary

- **sbatch**: The Slurm command for submitting a batch job script. Flags passed on the command line override matching `#SBATCH` directives inside the script.
- **#SBATCH directive**: A special comment line at the top of a job script (e.g., `#SBATCH --account=myaccount`) that Slurm reads as a submission flag. CLI flags take precedence over these.
- **Slurm**: The workload manager used on NERSC Perlmutter. It schedules, queues, and runs batch jobs on the cluster.
- **reservation**: A Slurm feature that pre-allocates a block of nodes for a specific time window, used at training events so attendees get immediate access to compute.
- **`--account` / `-A`**: The Slurm flag that specifies which project account to charge for compute time. Training events use the shared account `ntrain4`.
- **`NERSC_TRAINING_RESERVATION`**: An environment variable the deleted `submit.sh` wrapper reads to decide whether to append reservation flags to `sbatch`. Removed by this change.
- **env-var wrapper**: A shell script that inspects environment variables to conditionally modify a command before executing it — the pattern used by `submit.sh` and being eliminated here.
- **inline callout**: A formatting convention in this codebase — bold labels such as `**Training event?**` or `**IMPORTANT:**` placed inline in a README section to flag optional customizations without restructuring the surrounding prose.
- **acceptance criteria (AC)**: Named pass/fail conditions used in this project's design documents to define verifiable success or failure states for each change. Labeled with a short prefix (e.g., `remove-reservation-wrapper.AC1`).

## Architecture

The `submit.sh` wrapper was introduced to let training attendees set one environment variable (`NERSC_TRAINING_RESERVATION`) and have account and reservation flags injected automatically into `sbatch`. This created indirection — a custom script standing between the attendee and a standard Slurm command — and generated enough surface area (validation logic, two-mode output, an acceptance test suite) to become a distraction from the actual lesson content.

The replacement approach removes that indirection entirely. Attendees run `sbatch` directly. When at a training event, they append `-A ntrain4 --reservation=<name>` as CLI flags, which Slurm applies with higher precedence than the `#SBATCH --account=` directive already in the script. A single inline note in the README surfaces this for training-event attendees without restructuring the How to Run section into multiple options.

No new files are introduced. The change is purely subtractive: two files deleted, two files edited.

## Existing Patterns

Investigation found that the codebase uses bold inline callouts (`**IMPORTANT:**`, `**Training event?**`) for "customize this before running" notes — the strongest example is `02-maestro/example3-slurm-config/README.md`. Blockquotes are not used anywhere in the repo for this purpose.

The new training-event note follows this pattern: a bold inline label (`**Training event?**`) followed by the modified command on the same line.

## Implementation Phases

<!-- START_PHASE_1 -->
### Phase 1: Remove wrapper files

**Goal:** Delete the two files that implement the env-var automation.

**Components:**
- Delete `00-gnu-parallel/example3-slurm-integration/submit.sh`
- Delete `00-gnu-parallel/example3-slurm-integration/verify_reservation_support.sh`

**Dependencies:** None.

**Done when:** Neither file exists in the repository.
<!-- END_PHASE_1 -->

<!-- START_PHASE_2 -->
### Phase 2: Update documentation

**Goal:** Remove all references to the wrapper from user-facing and project-level docs.

**Components:**
- `00-gnu-parallel/example3-slurm-integration/README.md` — remove `submit.sh` from Files in This Example; delete the Training Event Setup section; replace the full How to Run section (~80 lines, two-option structure) with a single `sbatch submit_parallel_job.sh` block followed by the inline `**Training event?**` note
- `CLAUDE.md` — replace line 27 (env-var wrapper description) with the manual-flag description

**Dependencies:** Phase 1 (wrapper files must be gone before docs reference them as deleted).

**Done when:** README How to Run is a single path with inline training note; Training Event Setup section is absent; `submit.sh` is absent from Files in This Example; CLAUDE.md line 27 describes manual flags.
<!-- END_PHASE_2 -->
