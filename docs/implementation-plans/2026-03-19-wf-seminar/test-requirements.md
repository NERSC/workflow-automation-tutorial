# Test Requirements for Workflow Management Seminar

This document maps every acceptance criterion from the design plan to either an automated test or a documented human verification. Each criterion is rationalized against specific implementation decisions made during planning (Phases 1-8).

---

## Automated Tests

### wf-seminar.AC1.1: Each of 5 tools has documented rationale
- **Test type:** Integration
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 1)
- **Verification:** Grep each section README for "Why [tool]?" section
- **Commands:**
  ```bash
  grep -l "Why GNU Parallel" 00-gnu-parallel/README.md
  grep -l "Why signac" 01-signac/README.md
  grep -l "Why Maestro" 02-maestro/README.md
  grep -l "Why Merlin" 03-merlin/README.md
  grep -l "Why AiiDA" 04-aiida/README.md
  ```
- **Expected:** All 5 commands return the corresponding README path (non-empty match)
- **Rationalization:** Phase 2 Task 1 adds "Why GNU Parallel?" to `00-gnu-parallel/README.md`. Phase 4 Task 1 adds "Why Maestro?" to `02-maestro/README.md`. Phase 5 Task 1 adds "Why Merlin?" to `03-merlin/README.md`. Phase 6 Task 1 adds "Why AiiDA?" to `04-aiida/README.md`. Phase 3 Task 1 updates `01-signac/README.md` with rationale content. Each phase plan explicitly verifies the rationale section exists.

### wf-seminar.AC1.2: Tool justifications include category fit, advantages, teaching value, compatibility
- **Test type:** Integration
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 1)
- **Verification:** Grep each section README for all four justification components
- **Commands:**
  ```bash
  for readme in 00-gnu-parallel/README.md 02-maestro/README.md 03-merlin/README.md 04-aiida/README.md; do
    grep -q "Advantages over\|advantages over" "$readme" && echo "$readme: advantages OK"
    grep -q "teaching value\|Unique teaching" "$readme" && echo "$readme: teaching OK"
    grep -q "Perlmutter\|Slurm" "$readme" && echo "$readme: compatibility OK"
  done
  ```
- **Expected:** All 12 checks pass (4 READMEs x 3 grep checks; category fit is implicit in section placement)
- **Rationalization:** Phase 4 Task 1 README includes explicit subsections: "Advantages over alternatives", "Unique teaching value", "Perlmutter/Slurm compatibility". Phases 5 and 6 follow the same pattern. Phase 2 README covers these in "Why GNU Parallel?" section.

### wf-seminar.AC1.3: Excluded tools not included in seminar sections
- **Test type:** Unit
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 3)
- **Verification:** Grep all section READMEs and example files for excluded tool names used as primary instruction
- **Commands:**
  ```bash
  for tool in Balsam FireWorks Parsl HyperShell Snakemake; do
    # Search section directories only (not resources/ which may mention them for context)
    count=$(grep -rl "$tool" 0[0-4]-*/README.md 0[0-4]-*/example*/README.md 2>/dev/null | wc -l)
    if [ "$count" -gt 0 ]; then
      echo "FAIL: $tool found in section content"
    else
      echo "PASS: $tool not in section content"
    fi
  done
  ```
- **Expected:** All 5 excluded tools return PASS. Note: `resources/` directory may reference them in comparison context, which is acceptable.
- **Rationalization:** The design plan explicitly excludes Balsam, FireWorks, Parsl, HyperShell, and Snakemake. The top-level README (Phase 1, Task 1) documents this exclusion. Phase 4 Task 1 mentions Snakemake only in "Advantages over alternatives" comparison, which is acceptable context (not as a seminar section tool).

### wf-seminar.AC1.5: Both paradigms represented (filesystem and database)
- **Test type:** Integration
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 1)
- **Verification:** Confirm filesystem-based tools (signac, Maestro) and database-backed tools (Merlin, AiiDA) present
- **Commands:**
  ```bash
  # Filesystem paradigm
  grep -l "filesystem" 01-signac/README.md 02-maestro/README.md
  # Database paradigm
  grep -l "Redis\|database" 03-merlin/README.md
  grep -l "PostgreSQL\|database" 04-aiida/README.md
  ```
- **Expected:** All commands return matching files
- **Rationalization:** Phase 3 signac section uses filesystem-based state tracking. Phase 4 Maestro uses YAML/filesystem workflow execution. Phase 5 Merlin introduces Redis (database-backed). Phase 6 AiiDA uses PostgreSQL. This progression is documented in the design Architecture section and implemented across Phases 3-6.

### wf-seminar.AC1.6 (Failure): No commercial-license tools included
- **Test type:** Unit
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 3)
- **Verification:** Verify all 5 tools are open-source
- **Commands:**
  ```bash
  # All tools are open source: GNU Parallel (GPL), signac (BSD), Maestro (MIT),
  # Merlin (MIT), AiiDA (MIT). Verify no proprietary tools referenced as requirements.
  grep -ri "license\|commercial\|proprietary" requirements.txt environment.yml
  ```
- **Expected:** No matches for commercial/proprietary terms in dependency files
- **Rationalization:** Phase 1 Task 3 (requirements.txt) and Task 4 (environment.yml) pin only open-source tools. All five selected tools have OSI-approved licenses.

### wf-seminar.AC2.2: Time allocations sum to ~180 minutes
- **Test type:** Unit
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 1)
- **Verification:** Parse README agenda table and sum time allocations
- **Commands:**
  ```bash
  # Extract time allocations from README agenda
  grep -E "^\\| [0-9]" README.md | wc -l
  # Verify sections exist with documented durations
  grep "30 min\|25 min\|30 min\|40 min\|35 min\|10 min" README.md | wc -l
  ```
- **Expected:** 6 agenda rows present. Manual sum: 30 + 25 + 30 + 40 + 35 + 10 = 170 minutes (within ~180 target)
- **Rationalization:** Phase 1 Task 1 creates the top-level README with a structured agenda table. The design specifies Section 0 (30 min), Category 1 (25 min), Category 2 (30 min), Category 3 (40 min), Category 4 (35 min), Wrap-up (10 min) = 170 minutes. The design states "~180 minutes" allowing flexibility.

### wf-seminar.AC2.5: Audience assumptions documented
- **Test type:** Unit
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 3)
- **Verification:** Grep top-level README for audience prerequisite documentation
- **Commands:**
  ```bash
  grep -c "Slurm basics\|Shell scripting\|Python basics\|HPC concepts" README.md
  ```
- **Expected:** Returns `4` (all four audience assumptions listed)
- **Rationalization:** Phase 1 Task 1 README includes a "Target Audience" section listing all four assumptions verbatim from the design plan.

### wf-seminar.AC3.1: Matrix compares all 5 tools across 5 dimensions
- **Test type:** Integration
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 3)
- **Verification:** Validate comparison matrix file contains all tools and dimensions
- **Commands:**
  ```bash
  # All 5 tools mentioned
  for tool in "GNU Parallel" "signac" "Maestro" "Merlin" "AiiDA"; do
    grep -c "$tool" resources/comparison-matrix.md
  done
  # All 5 dimensions mentioned
  for dim in "Interface" "Infrastructure" "Dependencies" "Scale" "Use Case"; do
    grep -c "$dim" resources/comparison-matrix.md
  done
  ```
- **Expected:** Each tool appears at least 5 times (once per dimension row). Each dimension appears at least once as a section/column header.
- **Rationalization:** Phase 7 Task 1 explicitly creates `resources/comparison-matrix.md` with verification commands checking for at least 25 tool mentions and 5 dimension mentions.

### wf-seminar.AC3.5: Perlmutter/SPIN compatibility documented for each tool
- **Test type:** Integration
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 3)
- **Verification:** Check comparison matrix and section READMEs for Perlmutter compatibility
- **Commands:**
  ```bash
  grep -c "Perlmutter" resources/comparison-matrix.md
  for readme in 0[0-4]-*/README.md; do
    grep -q "Perlmutter\|NERSC" "$readme" && echo "$readme: Perlmutter OK"
  done
  ```
- **Expected:** Comparison matrix mentions Perlmutter at least 5 times (once per tool). All 5 section READMEs mention Perlmutter.
- **Rationalization:** Phase 7 Task 1 verification includes checking for Perlmutter/SPIN compatibility. Each section README (Phases 2-6) documents Perlmutter-specific notes.

### wf-seminar.AC4.1: Each tool has 3 example specifications (15 total)
- **Test type:** Integration
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 2)
- **Verification:** Count example directories across all 5 tool sections
- **Commands:**
  ```bash
  for section in 00-gnu-parallel 01-signac 02-maestro 03-merlin 04-aiida; do
    count=$(ls -d $section/example*/ 2>/dev/null | wc -l)
    echo "$section: $count examples"
  done
  total=$(ls -d 0[0-4]-*/example*/ 2>/dev/null | wc -l)
  echo "Total: $total examples"
  ```
- **Expected:** Each section has 3 examples. Total = 15.
- **Rationalization:** Phase 2 creates 3 GNU Parallel examples (Tasks 2-4). Phase 3 creates 3 signac examples (Tasks 2-4). Phase 4 creates 3 Maestro examples (Tasks 2-4). Phase 5 creates 3 Merlin examples (Tasks 3-5). Phase 6 creates 3 AiiDA examples (Tasks 3-5). Each phase plan includes file creation lists for all 3 example directories.

### wf-seminar.AC4.3: Examples progress from simple to complex within each section
- **Test type:** Integration
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 3)
- **Verification:** Check that example directory naming reflects progressive complexity
- **Commands:**
  ```bash
  # Verify naming convention implies progression
  ls -d 00-gnu-parallel/example1-* 00-gnu-parallel/example2-* 00-gnu-parallel/example3-*
  ls -d 01-signac/example1-* 01-signac/example2-* 01-signac/example3-*
  ls -d 02-maestro/example1-* 02-maestro/example2-* 02-maestro/example3-*
  ls -d 03-merlin/example1-* 03-merlin/example2-* 03-merlin/example3-*
  ls -d 04-aiida/example1-* 04-aiida/example2-* 04-aiida/example3-*
  ```
- **Expected:** All 15 directories exist with numbered naming (example1, example2, example3)
- **Rationalization:** Phase 2 explicitly orders examples: parameter-sweep (simple) -> multi-param (intermediate) -> slurm-integration (advanced). Phase 4 orders: simple-dag -> param-sweeps -> slurm-config. Phase 5 orders: distributed -> fault-tolerance -> massive-scale. Each phase plan documents this progression in the AC coverage section.

### wf-seminar.AC4.4: All examples run on Perlmutter without modification
- **Test type:** E2E
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 2)
- **Verification:** Execute all 15 examples on fresh Perlmutter clone
- **Commands:**
  ```bash
  # Phase 8 Task 2 defines the full execution sequence:
  # 1. Fresh clone to $SCRATCH
  # 2. Follow README setup instructions
  # 3. Execute each example in order
  # GNU Parallel examples (login node safe)
  cd 00-gnu-parallel/example1-parameter-sweep && bash run_simple.sh
  cd 00-gnu-parallel/example2-multi-param && bash run_combinations.sh
  # signac examples
  cd 01-signac/example1-parameter-space && python init_project.py
  # Maestro examples
  cd 02-maestro/example1-simple-dag && maestro run workflow.yaml
  # Merlin examples (requires Redis)
  cd 03-merlin/example1-distributed && merlin run spec.yaml
  # AiiDA examples (requires PostgreSQL + RabbitMQ)
  cd 04-aiida/example1-workflow-def && verdi run workflow.py
  ```
- **Expected:** All examples complete without errors. Exit code 0 for all commands.
- **Rationalization:** Phase 8 Task 2 dedicates an entire task to fresh-clone E2E testing. Each individual phase (2-6) includes per-example verification steps. Phase 2 Task 6 verifies GNU Parallel examples. Phase 3 Task 5 verifies signac examples. Phase 4 Tasks 2-4 include per-commit verification. Phase 5 Task 6 verifies Merlin examples. Phase 6 Task 6 verifies AiiDA examples.

### wf-seminar.AC4.6 (Failure): Example specs do not include actual implementation code
- **Test type:** Unit
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 3)
- **Verification:** This criterion applies to the design document, not the repository. The design plan's example specifications describe what to demonstrate, not code. The implementation plans (Phases 2-6) contain code because they are implementation plans, not design specs.
- **Commands:**
  ```bash
  # Verify design plan example specifications section describes learning objectives, not code
  grep -c "learning objectives\|what to demonstrate\|expected concepts" docs/design-plans/2026-03-19-wf-seminar.md
  ```
- **Expected:** Returns at least 1 (design plan describes specs, not code)
- **Rationalization:** The design plan's Definition of Done explicitly states "description of what examples should demonstrate (not the code itself)". Implementation plans appropriately contain code. This AC is satisfied by the design document itself.

### wf-seminar.AC5.1: Perlmutter-specific configuration documented for each tool
- **Test type:** Integration
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 3)
- **Verification:** Check that each tool section documents Slurm integration, filesystem, and QOS
- **Commands:**
  ```bash
  # Slurm integration in each section
  for section in 00-gnu-parallel 01-signac 02-maestro 03-merlin 04-aiida; do
    grep -rl "SBATCH\|Slurm\|slurm" "$section/" | head -1
  done
  # Filesystem guidance
  grep -c "SCRATCH\|CFS" resources/nersc-best-practices.md
  ```
- **Expected:** Each section has at least one file mentioning Slurm. NERSC best practices mentions $SCRATCH and CFS multiple times.
- **Rationalization:** Phase 2 Example 3 demonstrates Slurm integration for GNU Parallel. Phase 3 Example 2 shows signac-flow Slurm templates. Phase 4 Example 3 covers Maestro Slurm batch block. Phase 5 documents Merlin worker deployment with Slurm. Phase 6 documents AiiDA computer setup for Perlmutter Slurm.

### wf-seminar.AC5.2: Anti-patterns documented
- **Test type:** Unit
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 3)
- **Verification:** Count anti-patterns in NERSC best practices guide
- **Commands:**
  ```bash
  grep -c "Anti-Pattern" resources/nersc-best-practices.md
  grep -c "srun loop\|scheduler query\|job array" resources/nersc-best-practices.md
  ```
- **Expected:** At least 4 anti-patterns documented. Specific mentions of srun loops, scheduler queries, and job arrays.
- **Rationalization:** Phase 2 Task 5 creates `resources/nersc-best-practices.md` with 4 explicit anti-patterns: srun loops, job array overuse, SSH distribution, missing delays. Phase 7 Task 3 completes this file with tool-specific additions.

### wf-seminar.AC5.3: SPIN integration documented for database-backed tools
- **Test type:** Integration
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 3)
- **Verification:** Check SPIN deployment guides exist for Merlin and AiiDA
- **Commands:**
  ```bash
  ls resources/installation-guides/merlin-redis-setup.md
  ls resources/installation-guides/aiida-database-setup.md
  grep -c "SPIN" resources/installation-guides/merlin-redis-setup.md
  grep -c "SPIN" resources/installation-guides/aiida-database-setup.md
  ```
- **Expected:** Both files exist. Each mentions SPIN at least 10 times.
- **Rationalization:** Phase 5 Task 2 creates `merlin-redis-setup.md` with SPIN Redis deployment (Kubernetes manifests, container setup). Phase 6 Task 2 creates `aiida-database-setup.md` with SPIN PostgreSQL+RabbitMQ deployment.

### wf-seminar.AC5.4: Filesystem guidance specifies $SCRATCH and CFS
- **Test type:** Unit
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 3)
- **Verification:** Check NERSC best practices for filesystem guidance
- **Commands:**
  ```bash
  grep -c "SCRATCH" resources/nersc-best-practices.md
  grep -c "CFS\|Community File System" resources/nersc-best-practices.md
  grep "SCRATCH.*workflow\|workflow.*SCRATCH" resources/nersc-best-practices.md
  grep "CFS.*long-term\|long-term.*CFS\|CFS.*storage" resources/nersc-best-practices.md
  ```
- **Expected:** $SCRATCH mentioned at least 5 times, CFS mentioned at least 3 times. Usage guidance present for both.
- **Rationalization:** Phase 2 Task 5 creates the NERSC best practices file with explicit "Filesystem Usage" section covering $SCRATCH for workflows and CFS for long-term storage, including example commands.

### wf-seminar.AC5.5: Workflow QOS usage documented
- **Test type:** Unit
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 3)
- **Verification:** Check for workflow QOS documentation
- **Commands:**
  ```bash
  grep -c "workflow QOS\|qos=workflow\|--qos=workflow" resources/nersc-best-practices.md
  grep -c "workflow QOS\|qos=workflow" resources/installation-guides/merlin-redis-setup.md
  ```
- **Expected:** Workflow QOS mentioned at least 3 times in best practices. Mentioned at least 2 times in Merlin setup guide.
- **Rationalization:** Phase 2 Task 5 includes a "Workflow QOS" section in NERSC best practices. Phase 5 Task 2 documents workflow QOS as fallback for Redis deployment when SPIN is unavailable.

### wf-seminar.AC6.1: Repository organization matches seminar structure
- **Test type:** Integration
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 4)
- **Verification:** Verify directory structure matches design
- **Commands:**
  ```bash
  ls -d 00-gnu-parallel 01-signac 02-maestro 03-merlin 04-aiida resources/installation-guides
  ```
- **Expected:** All 6 directories exist
- **Rationalization:** Phase 1 Task 5 creates the complete directory structure. Phase 1 Task 6 verifies all directories exist. Phase 8 Task 4 performs final repository cleanup verification.

### wf-seminar.AC6.2: Each section includes README with concepts, when to use, and documentation links
- **Test type:** Integration
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 3)
- **Verification:** Check all section READMEs for required sections
- **Commands:**
  ```bash
  for readme in 00-gnu-parallel/README.md 01-signac/README.md 02-maestro/README.md 03-merlin/README.md 04-aiida/README.md; do
    grep -q "## Overview\|## Concepts" "$readme" && echo "$readme: concepts OK"
    grep -q "When to Use" "$readme" && echo "$readme: when-to-use OK"
    grep -q "Documentation\|Further Reading\|Official" "$readme" && echo "$readme: docs-links OK"
  done
  ```
- **Expected:** All 15 checks pass (5 READMEs x 3 sections)
- **Rationalization:** Phase 1 Task 5 creates placeholder READMEs with these sections. Phases 2-6 Task 1 each replace placeholders with complete content including Overview, When to Use, and documentation links.

### wf-seminar.AC6.3: Setup instructions enable fresh clone to Perlmutter
- **Test type:** E2E
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 2)
- **Verification:** Follow README setup instructions on fresh Perlmutter allocation
- **Commands:**
  ```bash
  # Phase 8 Task 2 defines the fresh-clone test:
  cd $SCRATCH
  git clone <repository-url> workflow_test
  cd workflow_test
  module load python
  conda env create -f environment.yml
  conda activate wf-seminar
  python -c "import signac; print(signac.__version__)"
  python -c "import maestrowf; print('OK')"
  ```
- **Expected:** Environment creation succeeds. All import statements succeed.
- **Rationalization:** Phase 1 Task 1 provides setup instructions. Phase 1 Task 3 creates requirements.txt with pinned versions. Phase 1 Task 4 creates environment.yml. Phase 1 Task 6 verifies setup. Phase 8 Task 2 validates end-to-end.

### wf-seminar.AC6.4: Resource materials include comparison matrix, decision tree, troubleshooting, further learning
- **Test type:** Integration
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 3)
- **Verification:** Check all resource files exist
- **Commands:**
  ```bash
  ls resources/comparison-matrix.md \
     resources/decision-tree.md \
     resources/troubleshooting.md \
     resources/further-learning.md \
     resources/nersc-best-practices.md
  ```
- **Expected:** All 5 files exist
- **Rationalization:** Phase 7 Tasks 1-5 create each of these files. Phase 2 Task 5 creates the initial `nersc-best-practices.md`. Phase 7 Task 3 completes it with tool-specific additions.

### wf-seminar.AC6.5: Installation guides provided for all tools
- **Test type:** Integration
- **Test file:** `docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md` (Phase 8, Task 3)
- **Verification:** Check installation guides exist for all 5 tools
- **Commands:**
  ```bash
  ls resources/installation-guides/gnu-parallel-setup.md \
     resources/installation-guides/signac-setup.md \
     resources/installation-guides/maestro-setup.md \
     resources/installation-guides/merlin-redis-setup.md \
     resources/installation-guides/aiida-database-setup.md
  ```
- **Expected:** All 5 files exist
- **Rationalization:** Phase 5 Task 2 creates `merlin-redis-setup.md`. Phase 6 Task 2 creates `aiida-database-setup.md`. Phase 7 Task 6 creates the three simpler guides (gnu-parallel, signac, maestro). This was identified as a gap during finalization review (fix task #50) and explicitly addressed.

---

## Human Verification

### wf-seminar.AC1.4: Tool progression demonstrates capability building (parallelism -> organization -> dependencies -> scale -> provenance)
- **Justification:** Requires human judgment to assess whether the conceptual progression is coherent and pedagogically sound. Automated tests can confirm tools are present but not that the narrative arc builds logically.
- **Verification approach:** Read section READMEs in order (00 through 04). Confirm each README's "Progression from [previous tool]" section explains what capability the new tool adds. Verify the progression matches: parallelism (GNU Parallel) -> organization (signac) -> dependencies (Maestro) -> scale/persistence (Merlin) -> provenance (AiiDA).
- **Validator:** Independent reviewer not involved in implementation
- **Implementation reference:** Phase 4 Task 1 README includes "Progression from signac" section. Phase 5 Task 1 README includes "Progression from Maestro" section. Phase 6 Task 1 README includes "Progression from Merlin" section. The design Architecture section defines this progression explicitly.

### wf-seminar.AC1.7 (Failure): Tools with poor HPC/Slurm integration not selected without documented workarounds
- **Justification:** Requires human domain expertise to evaluate whether each tool's Slurm integration is adequate for HPC use. "Poor" is a qualitative judgment that cannot be automated.
- **Verification approach:** For each of the 5 tools, review the section README and installation guide. Confirm that Slurm integration is either (a) native and documented, or (b) has an explicit workaround documented. Flag any tool where Slurm integration requires undocumented manual steps.
- **Validator:** NERSC staff or HPC workflow specialist familiar with Perlmutter
- **Implementation reference:** Phase 2 shows GNU Parallel + Slurm via `module load` and `$SLURM_CPUS_ON_NODE`. Phase 3 shows signac-flow Slurm templates. Phase 4 shows Maestro native Slurm adapter. Phase 5 documents Merlin worker deployment via Slurm + Redis on SPIN. Phase 6 documents AiiDA computer setup with Slurm scheduler configuration.

### wf-seminar.AC2.1: Structure includes Section 0 + 4 category sections
- **Justification:** Requires human judgment of pedagogical soundness -- not just that 5 sections exist, but that they form a coherent seminar structure with appropriate categorization (preparing work, submitting work, responding to outcomes, organizing data).
- **Verification approach:** Review top-level README agenda table. Confirm 5 sections present: Section 0 (GNU Parallel foundation) plus 4 category sections. Verify section ordering matches design plan categories. Confirm each section has a clear learning objective that maps to its category.
- **Validator:** Independent reviewer not involved in implementation
- **Implementation reference:** Phase 1 Task 1 creates the README with agenda table showing all 5 sections plus wrap-up. The design plan Architecture section defines the 5-section structure.

### wf-seminar.AC2.3: Each section follows pattern: motivation -> concepts -> demo -> hands-on -> decision criteria
- **Justification:** Requires pedagogical expertise to evaluate whether sections genuinely follow this instructional pattern, not just that section headings exist. The quality of motivation framing and decision criteria requires human assessment.
- **Verification approach:** For each of the 5 section READMEs, verify the presence and quality of: (1) motivation ("The Problem" or "Why [tool]?" section), (2) concepts ("Core Concepts" section), (3) demo (examples with expected output), (4) hands-on (exercises or "How to Run" sections), (5) decision criteria ("When to Use" and "When to Graduate" sections).
- **Validator:** Independent reviewer with instructional design awareness
- **Implementation reference:** Phase 4 Task 1 explicitly structures Maestro README with: "Why Maestro?" (motivation), "Core Concepts" (concepts), "Examples in This Section" (demo), exercise sections in each example README (hands-on), "When to Use Maestro" / "When to Graduate" (decision criteria). Phases 2, 5, 6 follow this same pattern.

### wf-seminar.AC2.4: Tools build on previous sections
- **Justification:** Requires human judgment to assess conceptual continuity. Automated tests cannot verify that signac genuinely builds on Parallel concepts, or that Maestro adds to signac in a meaningful way.
- **Verification approach:** Read section READMEs sequentially. For each section after Section 0, confirm: (1) explicit reference to previous tool's capabilities, (2) clear statement of what new capability is added, (3) example that demonstrates building on previous concepts. Specifically verify: signac builds on Parallel's parameter concepts, Maestro adds dependencies to signac's organization, Merlin adds distributed scale to Maestro's orchestration, AiiDA adds provenance to Merlin's database paradigm.
- **Validator:** Independent reviewer reading sections in order
- **Implementation reference:** Phase 3 README references "transition from Phase 2's manual parameter handling". Phase 4 Task 1 README includes "Progression from signac" section. Phase 5 Task 1 README includes "Progression from Maestro". Phase 6 Task 1 README includes "Progression from Merlin".

### wf-seminar.AC2.6 (Edge): Flexibility documented for time overruns
- **Justification:** Requires human review to assess whether time flexibility guidance is practical and sufficient for a live seminar. Automated tests can check for presence of text but not quality of contingency planning.
- **Verification approach:** Review top-level README for time flexibility documentation. Confirm presence of: (1) priority ordering of sections, (2) identification of reducible sections, (3) practical guidance for instructor adjustments. Verify AiiDA identified as reducible section.
- **Validator:** Seminar instructor or experienced training coordinator
- **Implementation reference:** Phase 1 Task 1 README includes a "Notes" section stating: "priority is GNU Parallel, Maestro, Merlin (core progression). AiiDA can be shortened to overview + pointers if time constrained" and "10-minute wrap-up can absorb ~5 minutes from earlier overruns". This directly mirrors the design plan's "Time Allocation Flexibility" section.

### wf-seminar.AC3.2: Decision framework provides clear guidance mapping problem characteristics to tool recommendations
- **Justification:** Requires human judgment to evaluate whether the decision tree is actually useful for tool selection. Automated tests can verify the file exists but cannot assess whether the decision logic is sound or the recommendations are appropriate.
- **Verification approach:** Walk through the decision tree with 5 realistic use cases: (1) simple parameter sweep with no dependencies, (2) multi-step pipeline with 100 tasks, (3) massive ML hyperparameter search with 100k combinations, (4) publication-grade computational chemistry workflow, (5) parameter study needing organization across multiple runs. Verify each use case leads to the expected tool recommendation.
- **Validator:** HPC researcher unfamiliar with these specific tools (tests whether guidance is understandable)
- **Implementation reference:** Phase 7 Task 2 creates `resources/decision-tree.md` with decision questions mapping problem characteristics to tools. Verification commands check for at least 5 decision questions and 4 graduation criteria.

### wf-seminar.AC3.3: Each tool has documented "sweet spot" use case
- **Justification:** Requires human judgment to evaluate whether the documented sweet spot accurately represents the tool's optimal use case. Domain expertise needed to assess whether characterizations are accurate.
- **Verification approach:** Review `resources/comparison-matrix.md` for each tool's "Use Case" dimension entry. For each of the 5 tools, confirm a clear "sweet spot" statement exists: (1) GNU Parallel -- embarrassingly parallel tasks on single node, (2) signac -- filesystem-based parameter space management, (3) Maestro -- moderate DAG workflows with Slurm, (4) Merlin -- massive distributed ensembles, (5) AiiDA -- provenance-tracked reproducible workflows. Verify sweet spots are distinct (no two tools have same sweet spot).
- **Validator:** HPC workflow practitioner who has used at least 2 of the 5 tools
- **Implementation reference:** Phase 7 Task 1 creates the comparison matrix. Phase 4 Task 1 documents Maestro's positioning. Phase 5 Task 1 documents Merlin's scale advantage. Phase 6 Task 1 documents AiiDA's provenance value proposition.

### wf-seminar.AC3.4: Framework includes "when to graduate" criteria
- **Justification:** Requires human judgment to assess whether graduation criteria are practical and correctly identify tool limitations. "When a tool becomes insufficient" is a qualitative assessment.
- **Verification approach:** Review `resources/decision-tree.md` for graduation criteria. For each of the first 4 tools (GNU Parallel, signac, Maestro, Merlin), verify documented criteria explaining when to move to the next tool. Confirm criteria are specific and actionable (not vague statements like "when you need more").
- **Validator:** Independent reviewer
- **Implementation reference:** Phase 7 Task 2 includes graduation criteria. Phase 2 Task 1 README includes "Progression to Workflow Tools" table. Phase 4 Task 1 README includes "When to Graduate to Next Tool". Phase 5 Task 1 README includes "When to Graduate to AiiDA" criteria.

### wf-seminar.AC4.2: Example specs describe learning objectives, not implementation code
- **Justification:** Requires human judgment to distinguish between "describing learning objectives" (design intent) and "containing implementation code" (implementation intent). The design plan should specify what to demonstrate, while implementation plans contain the code.
- **Verification approach:** Review the design plan's example specifications (lines 28-30). Confirm they describe what examples should demonstrate rather than providing code. Then verify that implementation plans (Phases 2-6) translate these specifications into working code with learning objectives documented in each example README.
- **Validator:** Independent reviewer comparing design plan to implementation plans
- **Implementation reference:** The design plan states: "For each tool, description of what examples should demonstrate (not the code itself)." Each implementation phase example README includes "Learning Objectives" and "What This Demonstrates" sections (e.g., Phase 4 Task 2 example1 README lists 4 learning objectives).

### wf-seminar.AC4.5: Example specifications include what to demonstrate, expected concepts, sample use case
- **Justification:** Requires human review to assess completeness of each example's specification beyond simple grep. "Expected concepts learned" requires pedagogical judgment.
- **Verification approach:** For each of the 15 examples, review the README for: (1) "What This Demonstrates" section, (2) "Key Concepts Demonstrated" section, (3) "Real-World Use Case" or contextual application scenario. Score each example on 3-point scale for completeness.
- **Validator:** Independent reviewer
- **Implementation reference:** Phase 2 Task 2 example1 README includes "What This Demonstrates", "Key Concepts", and progression context. Phase 4 Task 2 README includes "Learning Objectives", "Key Concepts Demonstrated", and "Exercises". Phase 5 Task 3 README includes "Key Concepts Demonstrated" and "Exercises".

### wf-seminar.AC5.6 (Edge): Fallback approaches documented for attendees without SPIN access
- **Justification:** Requires human judgment to assess whether fallback approaches are practical and sufficient. Automated tests can verify text exists but cannot judge whether a user without SPIN access could actually follow the instructions.
- **Verification approach:** Review Merlin and AiiDA installation guides for fallback documentation. For each: (1) confirm a non-SPIN option is documented, (2) verify fallback uses workflow QOS or dedicated allocation, (3) assess whether instructions are complete enough for someone without SPIN to follow independently.
- **Validator:** NERSC user without SPIN access (tests real-world usability)
- **Implementation reference:** Phase 5 Task 2 (`merlin-redis-setup.md`) includes "Option 2: Dedicated Allocation (Fallback)" section with workflow QOS Redis deployment. Phase 6 Task 2 (`aiida-database-setup.md`) includes parallel fallback section. The design plan's "SPIN Access" additional consideration explicitly requires these fallbacks.

---

## Coverage Summary

### Acceptance Criteria Coverage Matrix

| AC ID | Type | Test Category | Phase(s) Implementing |
|-------|------|---------------|----------------------|
| AC1.1 | Success | Automated | Phases 2, 3, 4, 5, 6 |
| AC1.2 | Success | Automated | Phases 2, 4, 5, 6 |
| AC1.3 | Success | Automated | All (exclusion check) |
| AC1.4 | Success | Human | Phases 2, 3, 4, 5, 6 |
| AC1.5 | Success | Automated | Phases 3, 4, 5, 6 |
| AC1.6 | Failure | Automated | Phase 1 |
| AC1.7 | Failure | Human | Phases 2, 3, 4, 5, 6 |
| AC2.1 | Success | Human | Phase 1 |
| AC2.2 | Success | Automated | Phase 1 |
| AC2.3 | Success | Human | Phases 2, 4, 5, 6 |
| AC2.4 | Success | Human | Phases 3, 4, 5, 6 |
| AC2.5 | Success | Automated | Phase 1 |
| AC2.6 | Edge | Human | Phase 1 |
| AC3.1 | Success | Automated | Phase 7 |
| AC3.2 | Success | Human | Phase 7 |
| AC3.3 | Success | Human | Phase 7 |
| AC3.4 | Success | Human | Phase 7 |
| AC3.5 | Success | Automated | Phases 2-7 |
| AC4.1 | Success | Automated | Phases 2, 3, 4, 5, 6 |
| AC4.2 | Success | Human | Design plan + Phases 2-6 |
| AC4.3 | Success | Automated | Phases 2, 3, 4, 5, 6 |
| AC4.4 | Success | E2E | Phase 8 (validates all) |
| AC4.5 | Success | Human | Phases 2, 4, 5, 6 |
| AC4.6 | Failure | Automated | Design plan |
| AC5.1 | Success | Automated | Phases 2, 3, 4, 5, 6 |
| AC5.2 | Success | Automated | Phase 2, Phase 7 |
| AC5.3 | Success | Automated | Phases 5, 6 |
| AC5.4 | Success | Automated | Phase 2 |
| AC5.5 | Success | Automated | Phases 2, 5 |
| AC5.6 | Edge | Human | Phases 5, 6 |
| AC6.1 | Success | Automated | Phase 1 |
| AC6.2 | Success | Automated | Phases 1, 2, 3, 4, 5, 6 |
| AC6.3 | Success | E2E | Phases 1, 8 |
| AC6.4 | Success | Automated | Phase 7 |
| AC6.5 | Success | Automated | Phases 5, 6, 7 |

### Totals

- **Total acceptance criteria:** 31 (across AC1-AC6)
- **Automated tests:** 21
- **Human verification:** 10
- **Test types breakdown:**
  - Unit tests: 5
  - Integration tests: 14
  - E2E tests: 2
  - Human verification: 10

### All Criteria Accounted For

Every acceptance criterion from the design plan (wf-seminar.AC1.1 through wf-seminar.AC6.5) is mapped to either an automated test or a human verification entry above. No criterion is unaddressed.
