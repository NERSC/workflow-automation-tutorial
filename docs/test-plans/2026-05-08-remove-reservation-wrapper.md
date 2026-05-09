# Human Test Plan: remove-reservation-wrapper

Generated: 2026-05-08
Implementation plan: docs/implementation-plans/2026-05-08-remove-reservation-wrapper/

## Prerequisites

- Access to the repository at `/global/u1/w/warndt/workflow_tutorial_research`
- Repository checked out at commit `2c7e348` or later on `master`
- Run the combined verification script from test-requirements.md and confirm all 11 checks print `PASS`

## Phase 1: File Deletion Verification

| Step | Action | Expected |
|------|--------|----------|
| 1.1 | Run `ls 00-gnu-parallel/example3-slurm-integration/` and inspect the listing | `submit.sh` and `verify_reservation_support.sh` are absent. `submit_parallel_job.sh`, `process_task.sh`, `task_list.txt`, and `README.md` are present. |
| 1.2 | Run `git log --oneline -1 -- 00-gnu-parallel/example3-slurm-integration/submit.sh` | Shows commit `432a3ed` with message about deleting the wrapper. |
| 1.3 | Run `git show --stat 432a3ed` | Confirms both `submit.sh` and `verify_reservation_support.sh` are deleted in the same commit. |

## Phase 2: README Structure Verification

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | Open `00-gnu-parallel/example3-slurm-integration/README.md` and locate the "## How to Run" section. | Section contains a single code block with `sbatch submit_parallel_job.sh`. No "### Option 1" or "### Option 2" sub-headings. No branching flow. |
| 2.2 | Read the line immediately after the code block ending with `cat slurm-*.out`. | A bold inline note reads: `**Training event?** Pass '-A ntrain4 --reservation=<name>' as CLI flags: 'sbatch -A ntrain4 --reservation=<name> submit_parallel_job.sh'` |
| 2.3 | Search the entire README for `NERSC_TRAINING_RESERVATION`, `./submit.sh`, and `export NERSC`. | Zero matches for any of these strings. |
| 2.4 | Locate the "## Files in This Example" section. | Lists `submit_parallel_job.sh`, `process_task.sh`, and `task_list.txt`. Does NOT list `submit.sh`. |
| 2.5 | Search the README for `## Training Event Setup`. | Not found. This entire section has been removed. |
| 2.6 | Scan all `##` headings in the README. | The following 9 non-modified headings are present: What This Demonstrates, The Problem, The Solution, Key Concepts, Sbatch Script Breakdown, Task List Format, Recovery Workflow, Progression, Real-World Use Case. |

## Phase 3: CLAUDE.md Verification

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | Open `CLAUDE.md` and locate the "## Conventions" section. | The reservation line reads: `Training event reservation: attendees pass '-A ntrain4 --reservation=<name>' directly as CLI flags to 'sbatch'` |
| 3.2 | Search CLAUDE.md for `NERSC_TRAINING_RESERVATION` and `submit.sh`. | Zero matches. No references to the deleted wrapper or env-var approach. |
| 3.3 | Count total lines in CLAUDE.md (`wc -l < CLAUDE.md`). | Exactly 40 lines. |
| 3.4 | Verify all 5 section headers are present: Tech Stack, Project Structure, Conventions, Invariants, Boundaries. | All 5 present. No sections added or removed. |

## Phase 4: Commit History Coherence

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | Run `git log --oneline e4d807c..2c7e348`. | Shows 4 commits: (1) delete wrapper files, (2) simplify README, (3) update CLAUDE.md reservation line, (4) update CLAUDE.md freshness date. |
| 4.2 | Run `git diff --name-status e4d807c..2c7e348`. | Shows exactly: `M README.md`, `D submit.sh`, `D verify_reservation_support.sh`, `M CLAUDE.md`. No other files touched. |
| 4.3 | Verify no unrelated changes crept into the README by running `git diff e4d807c..2c7e348 -- 00-gnu-parallel/example3-slurm-integration/README.md` and reading the diff. | Diff shows only: removal of the "Training Event Setup" section, removal of "submit.sh" from the Files list, simplification of How to Run from two-option to single-path with inline training note. No changes to Key Concepts, Sbatch Script Breakdown, or other sections. |

## End-to-End: New Attendee Experience

**Purpose:** Validate that a training attendee following the README instructions encounters a coherent, single-path workflow with no references to deleted files or removed concepts.

| Step | Action | Expected |
|------|--------|----------|
| E2E.1 | Navigate to `00-gnu-parallel/example3-slurm-integration/`. | Directory contains `submit_parallel_job.sh`, `process_task.sh`, `task_list.txt`, `README.md`. No `submit.sh` or `verify_reservation_support.sh`. |
| E2E.2 | Open `README.md` and follow the "How to Run" section. Read the instructions top-to-bottom. | Instructions present a single path: `sbatch submit_parallel_job.sh`. No decision point, no "choose between Option 1 and Option 2". |
| E2E.3 | If at a training event, note the training event callout. | A single bold line after the code block provides the exact flags to add: `-A ntrain4 --reservation=<name>`. The complete command `sbatch -A ntrain4 --reservation=<name> submit_parallel_job.sh` is shown inline. |
| E2E.4 | Search the README for any mention of environment variables (`export`, `NERSC_TRAINING_RESERVATION`). | None found. The env-var approach has been completely removed. |
| E2E.5 | Open `CLAUDE.md` and read the Conventions section. | The training reservation convention matches the README approach: direct CLI flags, not env-var wrappers. |

## Traceability

| Acceptance Criterion | Automated Check | Manual Step |
|----------------------|-----------------|-------------|
| AC1.1: submit.sh removed | Combined script AC1.1: `test ! -f` | Phase 1, Step 1.1 |
| AC1.2: verify_reservation_support.sh removed | Combined script AC1.2: `test ! -f` | Phase 1, Step 1.1 |
| AC2.1: Single-path How to Run | Combined script AC2.1: zero Option headers | Phase 2, Step 2.1 |
| AC2.2: Training event inline note | Combined script AC2.2: grep for note + flags | Phase 2, Step 2.2 |
| AC2.3: No wrapper artifacts in README | Combined script AC2.3: grep for artifacts | Phase 2, Step 2.3 |
| AC3.1: Training Event Setup absent | Combined script AC3.1: grep for heading | Phase 2, Step 2.5 |
| AC3.2: submit.sh absent from Files list | Combined script AC3.2: sed/grep | Phase 2, Step 2.4 |
| AC3.3: Other README sections intact | Combined script AC3.3: header count = 9 | Phase 2, Step 2.6 |
| AC4.1: CLAUDE.md CLI flags | Combined script AC4.1: grep | Phase 3, Step 3.1 |
| AC4.2: No wrapper artifacts in CLAUDE.md | Combined script AC4.2: grep | Phase 3, Step 3.2 |
| AC4.3: CLAUDE.md unchanged | Combined script AC4.3: line count + headers | Phase 3, Steps 3.3-3.4 |
