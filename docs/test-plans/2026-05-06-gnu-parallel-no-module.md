# Human Test Plan: GNU Parallel No-Module Consistency Fix

**Implementation plan:** `docs/implementation-plans/2026-05-06-gnu-parallel-no-module/`
**HEAD SHA tested:** `e98c2bff8c2c4b8c12d1d4762a0d42d4644e404a`

## Prerequisites

- Repository checked out at commit `e98c2bff8c2c4b8c12d1d4762a0d42d4644e404a` (or later, if no further changes to these files)
- Access to a terminal at the repository root (`/global/u1/w/warndt/workflow_tutorial_research`)
- The complete verification script from test-requirements.md has been run and reports `ALL CHECKS PASSED`

---

## Phase 1: Troubleshooting Document Coherence

| Step | Action | Expected |
|------|--------|----------|
| 1.1 | Open `resources/troubleshooting.md` and navigate to `## GNU Parallel Troubleshooting` | Section exists and is the first tool-specific section in the file |
| 1.2 | Read the first subsection heading under `## GNU Parallel Troubleshooting` | It is `### Problem: Output appears in wrong order or seems scrambled` -- there is no "command not found" entry before it |
| 1.3 | Scan the entire GNU Parallel section (from `## GNU Parallel Troubleshooting` to `## signac Troubleshooting`) | There are exactly 3 subsections: "Output appears in wrong order", "Parallel not using all available cores", "Out of memory or Cannot fork error". No mention of `module load`, `module avail`, or "command not found" appears anywhere |
| 1.4 | Verify narrative flow of the 3 remaining entries | Each entry follows the symptom/diagnosis/solution pattern. No steps reference loading a module. The section reads naturally without gaps or abrupt transitions |

---

## Phase 2: Comparison Matrix Consistency

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | Open `resources/comparison-matrix.md` and find the "Dimension 2: Infrastructure Requirements" table | The GNU Parallel row shows `None` for Required Backend, `No special handling` for SPIN Deployment, `None` for Node Dependencies, and `None - pre-installed on Perlmutter` for Setup Complexity |
| 2.2 | Scroll to "Infrastructure Deep Dive" and find the "GNU Parallel Infrastructure" subsection | The first bullet reads `Zero setup - pre-installed on Perlmutter`. The other two bullets are `Tasks run in current shell/node` and `No background services needed` |
| 2.3 | Search the entire file for the word "module" | The word "module" may appear in the context of signac/Maestro/Merlin/AiiDA (e.g., `module load python`, `module load redis`). Confirm it never appears in a GNU Parallel context, and the phrases `module load only` and `module load parallel` do not appear anywhere in the file |
| 2.4 | Read the SPIN Compatibility Notes below the table | The GNU Parallel note reads `Runs within allocation, no special SPIN setup needed` -- no reference to module loading |
| 2.5 | Read the "Key Insight" paragraph at the bottom of the SPIN section | Confirm GNU Parallel is listed among the tools that "fit naturally within SPIN constraints" |

---

## Phase 3: Slurm Script Structural Review

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | Open `00-gnu-parallel/example3-slurm-integration/submit_parallel_job.sh` | File starts with `#!/bin/bash` followed by `#SBATCH` directives (lines 2-8) |
| 3.2 | Read lines 9-14 | Line 9 is blank (separator after SBATCH block). Lines 10-11 are comment lines describing the example. Line 12 is blank. Line 13 is `# Make sure process script is executable`. Line 14 is `chmod +x process_task.sh` |
| 3.3 | Confirm there is no `module load parallel` line anywhere in the file | The script goes directly from the descriptive comments to `chmod +x` and then to the parallel invocation. No module loading occurs |
| 3.4 | Read the `parallel` command invocation (lines 34-39) | It uses `-j $SLURM_CPUS_ON_NODE`, `--joblog`, `--resume-failed`, `--delay 0.2`, and reads from `task_list.txt`. No module prerequisite is implied |

---

## Phase 4: README Content Review

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | Open `00-gnu-parallel/example3-slurm-integration/README.md` and find "Sbatch Script Breakdown" | The embedded code block shows the script without any `module load parallel` line |
| 4.2 | Find the "Key features" bullet list under the embedded code block | The bullets are: `#SBATCH directives configure Slurm allocation`, `-j $SLURM_CPUS_ON_NODE uses all allocated cores (128)`, `--joblog parallel_job.log tracks task completion`, `--resume-failed skips completed tasks on resubmission`, `--delay 0.2 reduces Slurm controller load`, `< task_list.txt reads tasks from file`. There is no bullet about `module load parallel`. The list has no orphaned blank lines between bullets |
| 4.3 | Search the entire README for "module load" | The phrase does not appear anywhere. The README references GNU Parallel as available without module loading |

---

## End-to-End: Narrative Consistency Walkthrough

**Purpose:** Verify that an attendee following the tutorial from start to finish never encounters instructions to load a parallel module, and the pre-installed nature of GNU Parallel is consistently communicated.

| Step | Action | Expected |
|------|--------|----------|
| E2E.1 | Open `resources/comparison-matrix.md`, read the GNU Parallel entries across all 5 dimensions | Setup is described as "None - pre-installed on Perlmutter" in the table and "Zero setup" in the deep dive. No module loading mentioned |
| E2E.2 | Open `resources/troubleshooting.md`, read the GNU Parallel section | No "command not found" entry exists. No troubleshooting step involves loading a module. The troubleshooting assumes GNU Parallel is already available |
| E2E.3 | Open `00-gnu-parallel/example3-slurm-integration/README.md`, follow the "How to Run" instructions mentally | The instructions go from `cd example3-slurm-integration` to `./submit.sh` (or `sbatch submit_parallel_job.sh`). No step involves `module load parallel` |
| E2E.4 | Open `00-gnu-parallel/example3-slurm-integration/submit_parallel_job.sh`, read as an attendee would | The script uses `parallel` directly without loading a module first. This is consistent with the comparison matrix claim of "pre-installed" |
| E2E.5 | Run `grep -r "module load parallel" 00-gnu-parallel/ resources/` from the repo root | Zero matches. The entire teaching material set is consistent |

---

## Traceability

| Acceptance Criterion | Automated Verification | Manual Step |
|----------------------|------------------------|-------------|
| AC1.1 -- No "command not found" heading | grep returns no match | Phase 1, Step 1.2 |
| AC1.2 -- First entry is "Output appears in wrong order" | grep -A2 confirms heading + first subsection | Phase 1, Step 1.2 |
| AC1.3 -- No module commands in troubleshooting | grep returns no match | Phase 1, Step 1.3 |
| AC2.1 -- Setup Complexity updated | grep confirms new phrase | Phase 2, Step 2.1 |
| AC2.2 -- Infrastructure Deep Dive updated | grep confirms new phrase | Phase 2, Step 2.2 |
| AC2.3 -- No old phrases in comparison matrix | grep returns no match | Phase 2, Step 2.3 |
| AC3.1 -- No module load in submit script | grep returns no match | Phase 3, Step 3.3 |
| AC3.2 -- No orphaned blank line before chmod | grep -B1 confirms comment precedes chmod | Phase 3, Step 3.2 |
| AC4.1 -- No module load in example3 README | grep returns no match | Phase 4, Step 4.3 |
| AC4.2 -- No orphaned blank lines in Key features | sed + grep confirms count = 1 | Phase 4, Step 4.2 |
| AC5.1 -- Cross-cutting: no matches in live materials | recursive grep returns no match | E2E, Step E2E.5 |
