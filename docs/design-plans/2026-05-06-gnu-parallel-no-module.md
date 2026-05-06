# GNU Parallel No-Module Consistency Fix Design

## Summary

This design corrects a factual inconsistency in the GNU Parallel teaching materials: several files document `module load parallel` as the way to access GNU Parallel on Perlmutter, but GNU Parallel is pre-installed in the system OS image and available in `$PATH` on both login and compute nodes without any module load. The authoritative statement of this fact already appears in `resources/installation-guides/gnu-parallel-setup.md` and in the example1 and example2 shell scripts; this design brings four remaining files into agreement with it.

The fix is purely editorial — no new files, no structural changes, no runtime behavior. It consists of five surgical text edits across four files: removing one stale troubleshooting section, updating two phrases in the comparison matrix, removing one `module load` line from a Slurm job script, and removing one line and one bullet from an example README. The single acceptance gate is that `grep -r "module load parallel" 00-gnu-parallel/ resources/` returns no matches.

## Definition of Done

All live teaching materials consistently reflect that GNU Parallel is pre-installed on Perlmutter — no `module load parallel` required. Specifically:
- `resources/troubleshooting.md`: the "parallel: command not found" troubleshooting entry is removed entirely
- `resources/comparison-matrix.md`: two phrases updated to accurately reflect zero-setup (no module)
- `00-gnu-parallel/example3-slurm-integration/submit_parallel_job.sh`: `module load parallel` line removed
- `00-gnu-parallel/example3-slurm-integration/README.md`: `module load parallel` line in the code block removed, and the bullet point explaining it removed

`docs/implementation-plans/` historical files are left untouched.

## Acceptance Criteria

### gnu-parallel-no-module.AC1: Troubleshooting entry removed
- **gnu-parallel-no-module.AC1.1 Success:** `resources/troubleshooting.md` contains no "parallel: command not found" section heading
- **gnu-parallel-no-module.AC1.2 Success:** The first entry under `## GNU Parallel Troubleshooting` is "Problem: Output appears in wrong order..."
- **gnu-parallel-no-module.AC1.3 Failure:** No `module avail parallel` or `module load parallel` commands appear anywhere in the troubleshooting file's GNU Parallel section

### gnu-parallel-no-module.AC2: Comparison matrix updated
- **gnu-parallel-no-module.AC2.1 Success:** Setup Complexity table cell for GNU Parallel reads `None - pre-installed on Perlmutter`
- **gnu-parallel-no-module.AC2.2 Success:** Infrastructure Deep Dive bullet reads `Zero setup - pre-installed on Perlmutter`
- **gnu-parallel-no-module.AC2.3 Failure:** Neither `module load only` nor `uses \`module load parallel\`` appears anywhere in `resources/comparison-matrix.md`

### gnu-parallel-no-module.AC3: Slurm script cleaned
- **gnu-parallel-no-module.AC3.1 Success:** `00-gnu-parallel/example3-slurm-integration/submit_parallel_job.sh` contains no `module load parallel` line
- **gnu-parallel-no-module.AC3.2 Success:** The `chmod +x process_task.sh` line follows directly after the `#SBATCH` block with no orphaned blank lines

### gnu-parallel-no-module.AC4: Example3 README cleaned
- **gnu-parallel-no-module.AC4.1 Success:** The embedded script block in the README contains no `module load parallel` line
- **gnu-parallel-no-module.AC4.2 Success:** The Key features bullet list contains no bullet mentioning `module load parallel`

### gnu-parallel-no-module.AC5: Cross-cutting consistency
- **gnu-parallel-no-module.AC5.1 Success:** `grep -r "module load parallel" 00-gnu-parallel/ resources/` returns no matches

## Glossary

- **GNU Parallel**: A shell tool that executes jobs in parallel on one or more machines. In this project it is the first tool taught, serving as the baseline for parallelizing independent tasks without a workflow framework.
- **Perlmutter**: The CPU/GPU supercomputer at NERSC (National Energy Research Scientific Computing Center) used as the deployment target for all teaching materials.
- **Lmod / `module load`**: The environment module system installed on most HPC clusters. `module load <name>` prepends a software package's bin and lib directories to the user's shell environment. Perlmutter uses Lmod; GNU Parallel is available without it.
- **`$PATH`**: The shell environment variable that lists directories searched for executable commands. A program is "in `$PATH`" when it can be invoked by name without specifying its full filesystem location.
- **Slurm**: The workload manager (job scheduler) used on Perlmutter. Users submit batch jobs via `sbatch`; compute time and resource allocation are managed by Slurm.
- **`#SBATCH` block**: The header section of a Slurm batch script where resource requests (nodes, time, account, reservation) are declared as specially formatted comments read by `sbatch`.
- **comparison matrix**: The file `resources/comparison-matrix.md`, which tabulates all five taught tools side-by-side across dimensions such as setup complexity and infrastructure requirements. Used by attendees when choosing a tool after the seminar.
- **troubleshooting guide**: The file `resources/troubleshooting.md`, which documents known problems and their resolutions for each tool. Removing a stale entry here prevents attendees from following a fix path that no longer applies.
- **live teaching materials**: Files that are shown to or executed by seminar attendees during the event, as distinct from historical implementation plans in `docs/implementation-plans/` which record past decisions and are not shown to attendees.
- **Setup Complexity**: A specific column in the comparison matrix's summary table, characterizing the effort required to make each tool available on Perlmutter before first use.
- **Infrastructure Deep Dive**: A subsection of the comparison matrix that describes the underlying system requirements for each tool in more detail than the summary table.

## Architecture

A targeted content consistency fix across four live teaching files. GNU Parallel is pre-installed in Perlmutter login and compute node OS images and available in `$PATH` without any module load. Several files incorrectly document `module load parallel` as the access method. This design removes those references so all live materials agree with the authoritative source (`resources/installation-guides/gnu-parallel-setup.md`).

No new files, no new components. Five surgical edits: two deletions in shell/README, two phrase replacements in the comparison matrix, and one section removal in the troubleshooting guide.

## Existing Patterns

The correct fact is already stated in three places:

- `resources/installation-guides/gnu-parallel-setup.md`: "GNU Parallel is pre-installed on Perlmutter — no module load or user installation required."
- `00-gnu-parallel/example1-parameter-sweep/run_simple.sh`: comment states no module load needed
- `00-gnu-parallel/example2-multi-param/run_combinations.sh`: same comment

This design brings the four remaining files into alignment with that established pattern. No new patterns are introduced.

## Implementation Phases

<!-- START_PHASE_1 -->
### Phase 1: Remove all `module load parallel` references from live teaching materials

**Goal:** All four affected files updated; project has a single consistent statement that GNU Parallel is pre-installed on Perlmutter.

**Components:**
- `resources/troubleshooting.md` — remove entire "### Problem: 'parallel: command not found'" section (heading through verification code block); "### Problem: Output appears in wrong order..." becomes the new first GNU Parallel entry
- `resources/comparison-matrix.md` — replace `Trivial - module load only` (Setup Complexity table cell) with `None - pre-installed on Perlmutter`; replace `Zero setup - uses \`module load parallel\`` (Infrastructure Deep Dive bullet) with `Zero setup - pre-installed on Perlmutter`
- `00-gnu-parallel/example3-slurm-integration/submit_parallel_job.sh` — remove lines `# Load GNU Parallel module` and `module load parallel`
- `00-gnu-parallel/example3-slurm-integration/README.md` — remove `module load parallel` line from embedded script block; remove bullet `` `module load parallel` loads GNU Parallel `` from Key features list

**Dependencies:** None

**Done when:** `grep -r "module load parallel" 00-gnu-parallel/ resources/` returns no matches in any of the four files; all four files read correctly with no orphaned blank lines or broken lists
<!-- END_PHASE_1 -->

## Additional Considerations

No error handling, rollback, or compatibility concerns — these are documentation-only changes with no runtime behavior.
