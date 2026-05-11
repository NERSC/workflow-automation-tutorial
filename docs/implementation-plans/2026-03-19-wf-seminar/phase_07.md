# Workflow Management Seminar Implementation Plan - Phase 7

**Goal:** Provide decision-making tools and reference materials enabling attendees to choose appropriate tools for their research

**Architecture:** Create five resource documents providing tool comparison, decision framework, best practices, troubleshooting, and further learning materials

**Tech Stack:**
- Markdown for documentation
- Comparison tables for tool selection
- Decision tree flowchart (Mermaid or ASCII)

**Scope:** Phase 7 of 8 phases from original design

**Codebase verified:** 2026-03-19 (Phases 1-6 will exist before this phase executes)

---

## Acceptance Criteria Coverage

This phase implements and tests:

### wf-seminar.AC3: Comparison framework enables tool selection decisions
- **wf-seminar.AC3.1 Success:** Matrix compares all 5 tools across 5 dimensions (interface, infrastructure, dependencies, scale, use case)
- **wf-seminar.AC3.2 Success:** Decision framework provides clear guidance mapping problem characteristics to tool recommendations
- **wf-seminar.AC3.3 Success:** Each tool has documented "sweet spot" use case where it's the best choice
- **wf-seminar.AC3.4 Success:** Framework includes "when to graduate" criteria (when tool becomes insufficient)
- **wf-seminar.AC3.5 Success:** Perlmutter/SPIN compatibility documented for each tool

---

<!-- START_TASK_1 -->
### Task 1: Create resources/comparison-matrix.md with 5-dimensional tool comparison

**Verifies:** wf-seminar.AC3.1, wf-seminar.AC3.3, wf-seminar.AC3.5

**Files:**
- Create: `resources/comparison-matrix.md`

**Implementation:**

Create comprehensive comparison matrix covering all 5 tools across 5 dimensions.

Matrix includes:
- **Interface:** CLI commands, YAML syntax, Python API complexity
- **Infrastructure:** Requirements (none/Redis/PostgreSQL+RabbitMQ), SPIN deployment
- **Dependencies:** How tools manage multi-step dependencies
- **Scale:** Proven capacity (hundreds/thousands/millions of tasks)
- **Use Case:** Best-fit scenarios for each tool

Each cell provides concise comparison enabling tool selection.

**Verification:**

Run: `grep -c "GNU Parallel\|signac\|Maestro\|Merlin\|AiiDA" resources/comparison-matrix.md`
Expected: Returns at least `25` (5 tools mentioned multiple times)

Run: `grep -c "Interface\|Infrastructure\|Dependencies\|Scale\|Use Case" resources/comparison-matrix.md`
Expected: Returns at least `5` (all dimensions covered)

**Commit:**

```bash
git add resources/comparison-matrix.md
git commit -m "feat(resources): add tool comparison matrix across 5 dimensions

- Compares GNU Parallel, signac, Maestro, Merlin, AiiDA
- Five dimensions: interface, infrastructure, dependencies, scale, use case
- Documents sweet spot for each tool
- Includes Perlmutter/SPIN compatibility for all tools
- Enables evidence-based tool selection"
```

<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: Create resources/decision-tree.md with problem-to-tool mapping

**Verifies:** wf-seminar.AC3.2, wf-seminar.AC3.4

**Files:**
- Create: `resources/decision-tree.md`

**Implementation:**

Create decision framework mapping problem characteristics to tool recommendations.

Decision tree questions:
1. Do you need multi-step dependencies? → If no: GNU Parallel / signac
2. Does workflow fit in single allocation? → If no: Merlin / AiiDA
3. Need provenance tracking? → If yes: AiiDA
4. Need massive scale (>10k tasks)? → If yes: Merlin
5. Need parameter organization? → signac vs Maestro

Includes "when to graduate" criteria showing limits of each tool.

**Verification:**

Run: `grep -c "Do you need\|Does\|Need" resources/decision-tree.md`
Expected: Returns at least `5` (decision questions)

Run: `grep -c "graduate" resources/decision-tree.md`
Expected: Returns at least `4` (graduation criteria for tools)

**Commit:**

```bash
git add resources/decision-tree.md
git commit -m "feat(resources): add decision tree for tool selection

- Maps problem characteristics to tool recommendations
- Includes decision questions guiding tool choice
- Documents graduation criteria (when to move to more capable tool)
- Covers workflow scale, dependencies, provenance, infrastructure
- Provides clear path from simple to complex tools"
```

<!-- END_TASK_2 -->

<!-- START_TASK_3 -->
### Task 3: Complete resources/nersc-best-practices.md with Perlmutter snippets

**Verifies:** wf-seminar.AC5.2, wf-seminar.AC5.4

**Files:**
- Modify: `resources/nersc-best-practices.md`

**Implementation:**

Complete the NERSC best practices file started in Phase 2 (which covered GNU Parallel and general patterns).

**Phase 7 additions (tool-specific Slurm snippets):**
- signac-flow submission templates for Perlmutter
- Maestro batch block examples (partitions, accounts, QOS)
- Merlin worker deployment patterns (workflow QOS for persistent workers)
- AiiDA computer configuration for Perlmutter Slurm
- Per-tool $SCRATCH workspace patterns
- GPU partition configuration for tools requiring GPUs

**Note:** Phase 2 Task 5 already covered:
- General anti-patterns (srun loops, scheduler query limits)
- Filesystem guidance ($SCRATCH vs CFS basics)
- Workflow QOS introduction

Phase 7 adds **tool-specific configuration snippets** that weren't known until after implementing each tool section.

**Verification:**

Run: `grep -c "$SCRATCH\|CFS" resources/nersc-best-practices.md`
Expected: Returns at least `5` (filesystem guidance)

Run: `grep -c "srun loop" resources/nersc-best-practices.md`
Expected: Returns at least `1` (anti-pattern documented)

**Commit:**

```bash
git add resources/nersc-best-practices.md
git commit -m "feat(resources): complete NERSC best practices with Perlmutter snippets

- Slurm configuration examples for all tools
- Filesystem usage patterns ($SCRATCH for workflows, CFS for storage)
- QOS selection guidance (regular/debug/workflow)
- Anti-patterns with corrections (srun loops, scheduler query limits)
- Perlmutter CPU/GPU partition specifics
- Allocation hour optimization strategies"
```

<!-- END_TASK_3 -->

<!-- START_TASK_4 -->
### Task 4: Create resources/further-learning.md with curated documentation links

**Verifies:** wf-seminar.AC6.4

**Files:**
- Create: `resources/further-learning.md`

**Implementation:**

Create curated link collection organized by tool:
- Official documentation (verified 2026 URLs)
- Tutorials and getting-started guides
- Community forums (Slack, Discourse, GitHub Discussions)
- Example repositories
- Academic papers for provenance/workflow concepts

Each link includes brief description of content.

**Verification:**

Run: `grep -c "http\|https" resources/further-learning.md`
Expected: Returns at least `30` (URLs for all tools)

Run: `grep -c "Maestro\|Merlin\|AiiDA" resources/further-learning.md`
Expected: Returns at least `15` (all tools covered)

**Commit:**

```bash
git add resources/further-learning.md
git commit -m "feat(resources): add further learning links for all tools

- Official documentation for all 5 tools (verified 2026 URLs)
- Tutorials and getting-started guides
- Community forums and support channels
- Example repositories demonstrating patterns
- Academic papers on workflow management and provenance
- NERSC-specific workflow resources"
```

<!-- END_TASK_4 -->

<!-- START_TASK_5 -->
### Task 5: Create resources/troubleshooting.md with common issues and solutions

**Verifies:** wf-seminar.AC6.4

**Files:**
- Create: `resources/troubleshooting.md`

**Implementation:**

Create troubleshooting guide organized by tool, covering:
- Installation issues
- Connection problems (Redis, PostgreSQL for Merlin/AiiDA)
- Slurm integration errors
- Permission/authentication issues
- Common workflow errors
- Performance problems

Each issue includes: symptom, diagnosis commands, solution.

**Verification:**

Run: `grep -c "Problem:\|Solution:" resources/troubleshooting.md`
Expected: Returns at least `20` (10+ problem/solution pairs)

Run: `grep -c "GNU Parallel\|signac\|Maestro\|Merlin\|AiiDA" resources/troubleshooting.md`
Expected: Returns at least `10` (all tools have troubleshooting entries)

**Commit:**

```bash
git add resources/troubleshooting.md
git commit -m "feat(resources): add troubleshooting guide for all tools

- Organized by tool with common issues and solutions
- Installation and setup problems
- Connection issues (Redis, PostgreSQL, RabbitMQ)
- Slurm integration errors and fixes
- Permission and authentication troubleshooting
- Performance tuning recommendations
- NERSC-specific gotchas and workarounds"
```

<!-- END_TASK_5 -->

<!-- START_TASK_6 -->
### Task 6: Create simplified installation guides for GNU Parallel, signac, Maestro

**Verifies:** wf-seminar.AC6.5

**Files:**
- Create: `resources/installation-guides/gnu-parallel-setup.md`
- Create: `resources/installation-guides/signac-setup.md`
- Create: `resources/installation-guides/maestro-setup.md`

**Implementation:**

Create simplified installation guides for tools that don't require complex infrastructure (contrast with Merlin/AiiDA guides which are comprehensive).

**File 1: `resources/installation-guides/gnu-parallel-setup.md`**

```markdown
# GNU Parallel Setup on Perlmutter

## Installation

GNU Parallel is pre-installed on Perlmutter — no module load or user installation required. It is available directly in `$PATH`:

```bash
parallel --version
```

## Verification

```bash
seq 1 4 | parallel echo "Test {}"
```

Expected output: "Test 1", "Test 2", "Test 3", "Test 4"

## See Also

- Section 0 examples: `00-gnu-parallel/`
- Official docs: https://www.gnu.org/software/parallel/
```

**File 2: `resources/installation-guides/signac-setup.md`**

```markdown
# signac Setup on Perlmutter

## Installation

Install via pip (included in requirements.txt):

```bash
module load python
pip install signac==2.3.0 signac-flow==0.28.0
```

## Verification

```bash
python -c "import signac; print(signac.__version__)"
```

Expected: 2.3.0

## See Also

- Section 1 examples: `01-signac/`
- Official docs: https://docs.signac.io/
```

**File 3: `resources/installation-guides/maestro-setup.md`**

```markdown
# Maestro Setup on Perlmutter

## Installation

Install via pip (included in requirements.txt):

```bash
module load python
pip install maestrowf==1.1.11
```

## Verification

```bash
maestro --version
```

Expected: 1.1.11

## See Also

- Section 2 examples: `02-maestro/`
- Official docs: https://maestrowf.readthedocs.io/
```

**Verification:**

Run: `ls resources/installation-guides/ | grep -E "gnu-parallel|signac|maestro"`
Expected: Shows all 3 files

Run: `grep -c "module load\|pip install" resources/installation-guides/gnu-parallel-setup.md resources/installation-guides/signac-setup.md resources/installation-guides/maestro-setup.md`
Expected: Returns at least `3` (installation commands present)

**Commit:**

```bash
git add resources/installation-guides/gnu-parallel-setup.md \
        resources/installation-guides/signac-setup.md \
        resources/installation-guides/maestro-setup.md
git commit -m "feat(resources): add installation guides for GNU Parallel, signac, Maestro

- GNU Parallel: module load instructions
- signac: pip install with version pinning
- Maestro: pip install with verification
- All guides link to example sections and official docs
- Completes AC6.5 (all 5 tools have installation guides)"
```

<!-- END_TASK_6 -->
