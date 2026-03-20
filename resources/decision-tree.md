# Workflow Tool Decision Tree

A guided framework for selecting the right workflow tool based on your problem characteristics.

## Quick Decision Tree

Start here if you need fast answers:

```
┌─ Do you need multi-step workflows?
│  ├─ NO (single parallelization task)
│  │  ├─ Need parameter organization?
│  │  │  ├─ YES → signac
│  │  │  └─ NO → GNU Parallel (simplest)
│  │
│  │  Does workflow fit in single Perlmutter allocation?
│  │  ├─ NO (multi-step across allocations) → Maestro
│  │  └─ YES (single allocation scope)
│  │
│  ├─ YES (complex multi-step dependencies)
│  │  ├─ Need massive scale (>100k tasks)?
│  │  │  ├─ YES → Merlin
│  │  │  └─ NO
│  │  │     ├─ Need full provenance tracking?
│  │  │     │  ├─ YES → AiiDA
│  │  │     │  └─ NO → Maestro
│  │  │
│  │  └─ Need publication-ready reproducibility?
│  │     ├─ YES → AiiDA
│  │     └─ NO → Maestro
```

---

## Decision Questions

Answer these questions in sequence to narrow your choices:

### Question 1: Do you need multi-step dependencies?

**Explanation:** Can your workflow be expressed as a single command, or does it require multiple steps where some tasks depend on outputs of earlier tasks?

**Examples:**
- **NO:** "Run this command 1000 times with different parameters"
- **YES:** "Run preprocessing, then main analysis on each result, then merge outputs"

| Answer | Best Tools | Why |
|--------|-----------|-----|
| NO | GNU Parallel, signac | Single-level execution is sufficient |
| YES | Maestro, Merlin, AiiDA | Need explicit dependency tracking |

### Question 2: Does your workflow fit within a single Perlmutter allocation?

**Explanation:** Can all your tasks complete within one job allocation (typically 1-24 hours), or do you need to span multiple allocations?

**Examples:**
- **YES:** "All 10,000 tasks finish in 2 hours"
- **NO:** "Preprocessing takes 4 hours, then analysis takes 8 hours, need allocation management"

| Answer | Implications |
|--------|-------------|
| YES | GNU Parallel, signac, Maestro all work well |
| NO | Need Maestro (multi-step submission) or Merlin (persistent workers) |

### Question 3: Do you need provenance tracking and publication-ready reproducibility?

**Explanation:** Is it critical for your research to have complete audit trails of what ran, with what inputs, and what outputs were produced? Are you publishing results that need to be fully reproducible?

**Examples:**
- **NO:** "Internal analysis, reproducibility nice-to-have"
- **YES:** "Publishing materials science results, peer review requires full provenance"

| Answer | Impact |
|--------|--------|
| NO | Can use GNU Parallel, signac, Maestro, or Merlin |
| YES | AiiDA is the only choice with automatic provenance tracking |

### Question 4: How many total tasks will your workflow have?

**Explanation:** Estimate the total number of independent tasks (jobs, simulations, processing steps) your workflow will execute.

| Task Count | Recommended Tools | Reasoning |
|------------|------------------|-----------|
| <100 | GNU Parallel, signac | Simple and overhead-free |
| 100-1,000 | GNU Parallel, signac, Maestro | Good scaling for standard systems |
| 1,000-10,000 | signac, Maestro | Need better parameter/task organization |
| 10,000-100,000 | Maestro, Merlin | DAG efficiency becomes important |
| >100,000 | Merlin | Built specifically for massive scale |

### Question 5: Do you need systematic parameter organization?

**Explanation:** Will you be exploring a parameter space systematically (e.g., trying different simulation parameters, machine learning hyperparameters)? Do you need to compare results across parameter combinations?

**Examples:**
- **NO:** "Just running one script with different data files"
- **YES:** "Testing 100 different parameter combinations, comparing results"

| Answer | Recommendation |
|--------|-----------------|
| NO | GNU Parallel, Maestro, Merlin |
| YES | signac (excellent parameter organization) |

### Question 6: Is persistent worker infrastructure available?

**Explanation:** Does your deployment environment support long-running worker processes (outside allocations), or must all processes complete within job allocations?

**Examples:**
- **Available:** NERSC persistent computing resources or standalone cluster
- **NOT Available:** SPIN system with strict allocation boundaries

| Answer | Impact |
|--------|--------|
| YES | All tools work (Merlin and AiiDA can use workers effectively) |
| NO | Avoid Merlin and AiiDA; use GNU Parallel, signac, or Maestro |

---

## Decision Workflows

### Workflow A: Quick Parameter Sweep (100 tasks, 2 hours)

**Your situation:**
- Need to run command with 100 different parameter sets
- All complete in one allocation
- Results just need to be organized

**Decision path:**
1. Multi-step dependencies? → NO
2. Parameter organization needed? → YES
3. **RECOMMENDATION: signac**

**Why:** Parameter directories provide natural organization, no complex infrastructure, fits in single allocation.

---

### Workflow B: Multi-Step Simulation Pipeline (5,000 tasks)

**Your situation:**
- Preprocessing → main simulation → post-processing
- Each step depends on previous step
- Tasks scale from thousands in preprocessing to hundreds in post-processing
- Need completion guarantees

**Decision path:**
1. Multi-step dependencies? → YES
2. Fits in single allocation? → NO (5k tasks + dependencies)
3. Massive scale (>100k)? → NO
4. Provenance required? → NO
5. **RECOMMENDATION: Maestro**

**Why:** Multi-step support with dependencies, DAG awareness, works across allocations via multi-step submission.

---

### Workflow C: Machine Learning Hyperparameter Search (100k tasks)

**Your situation:**
- Grid search over hyperparameters
- 100,000 model training tasks
- Need to scale across multiple allocation resubmissions
- Results must be comparable across runs

**Decision path:**
1. Multi-step dependencies? → Partially (task submission, not complex DAGs)
2. Massive scale (>100k)? → YES
3. **RECOMMENDATION: Merlin**

**Why:** Built for massive task volumes, efficient queuing, designed for exactly this pattern.

---

### Workflow D: Publication-Ready Materials Science Study

**Your situation:**
- DFT calculations on multiple materials and structures
- Complex multi-step workflows
- Need complete audit trail for peer review
- Must show exact parameters and outputs for reproducibility

**Decision path:**
1. Multi-step dependencies? → YES (complex DAG)
2. Provenance required? → YES (critical for publication)
3. **RECOMMENDATION: AiiDA**

**Why:** Only tool with automatic provenance tracking and publication-ready audit trails; type system ensures reproducibility.

---

### Workflow E: Quick One-Time Parallelization

**Your situation:**
- "I have 1000 files and want to process them in parallel"
- No complex workflows
- Everything happens in one command/script
- Just want maximum speed

**Decision path:**
1. Multi-step dependencies? → NO
2. Parameter organization? → NO
3. **RECOMMENDATION: GNU Parallel**

**Why:** Simplest tool, zero setup overhead, perfect for embarrassingly parallel problems.

---

## Graduation Criteria: When to Move to Next Tool

Each tool has a limit. Know the signs it's time to graduate to a more capable tool.

### Graduating from GNU Parallel

Move to a different tool when you encounter:

- **Multi-step workflows:** Need to coordinate dependent tasks
  - *Sign:* Writing shell scripts that wait for outputs from previous parallel runs
  - *Graduate to:* signac (small/medium scale) or Maestro (large scale)

- **Parameter organization:** Need to track which result came from which parameters
  - *Sign:* Hand-managing directories for different parameter sets
  - *Graduate to:* signac

- **Scale issues:** Performance degradation beyond ~1,000 tasks
  - *Sign:* Noticeable memory growth or task spawning slowdown
  - *Graduate to:* signac (thousands) or Maestro (tens of thousands)

- **Complex scheduling:** Need to control task resource allocation
  - *Sign:* Some tasks need GPUs, others don't; need fine-grained control
  - *Graduate to:* Maestro or Merlin

### Graduating from signac

Move to a different tool when:

- **Dependencies become complex:** Beyond simple job condition pre/post conditions
  - *Sign:* Writing intricate Python logic to coordinate job execution order
  - *Graduate to:* Maestro (good DAG support)

- **Scale exceeds 50,000 parameters:** Filesystem directory tree becomes bottleneck
  - *Sign:* Slowdowns in directory listing or job status queries
  - *Graduate to:* Maestro or Merlin

- **Workflow spans allocations:** Can't do all work in one job request
  - *Sign:* Trying to chain multiple signac job submissions, losing state
  - *Graduate to:* Maestro

- **Multi-allocation campaigns:** Need to coordinate across multiple job submissions
  - *Sign:* Writing scripts to resubmit and continue jobs between allocations
  - *Graduate to:* Maestro

### Graduating from Maestro

Move to a different tool when:

- **Massive scale (>100k tasks):** DAG traversal becomes slow
  - *Sign:* Noticeable delays in workflow planning/scheduling
  - *Graduate to:* Merlin

- **Distributed worker systems:** Need persistent long-running workers
  - *Sign:* Want to submit tasks from control node without blocking allocations
  - *Graduate to:* Merlin (distributed) or AiiDA (if provenance matters)

- **Complex provenance requirements:** Need full audit trails
  - *Sign:* Publishing research, peer review requires reproducibility proof
  - *Graduate to:* AiiDA

- **Fault tolerance at massive scale:** Need automatic task recovery
  - *Sign:* Long-running workflows with tasks that occasionally fail
  - *Graduate to:* Merlin

### Graduating from Merlin

Move to a different tool when:

- **Provenance becomes critical:** Need publication-ready audit trails
  - *Sign:* Journals asking "how was this exactly calculated?"
  - *Graduate to:* AiiDA

- **Research reproducibility:** Need to run exact same workflow years later
  - *Sign:* Reproducing research, verifying claims
  - *Graduate to:* AiiDA

*Note:* Merlin is generally the largest-scale non-provenance tool. Most users at massive scale don't need to graduate further unless provenance requirements emerge.

### Graduating from AiiDA

AiiDA is the final tool in the progression - it has no graduation path within this toolkit. If you outgrow AiiDA, you'd need:

- **Federated computing:** Work with collaborators running different tools
  - *Solution:* Multi-tool orchestration layer (beyond this seminar scope)

- **Real-time interactive analysis:** Need sub-second latency
  - *Solution:* Different category of tool (interactive analysis, not batch workflows)

---

## Infrastructure Constraints and Tool Suitability

### Running on NERSC Perlmutter (SPIN-constrained system)

SPIN (Shifter in Place) enforces allocation boundaries. Tools respond differently:

| Tool | Can Run Within Allocation | Persistent Workers? | SPIN Friendly |
|------|---------------------------|-------------------|--------------|
| **GNU Parallel** | ✓ Yes | N/A | ✓ Excellent |
| **signac** | ✓ Yes | No | ✓ Excellent |
| **Maestro** | ✓ Yes (or multi-step) | Optional | ✓ Excellent |
| **Merlin** | ✓ Can, but limited | Yes - required | ⚠ Complex |
| **AiiDA** | ✗ No (daemon required) | Yes - required | ✗ Problematic |

**Guidance:**
- If you're on SPIN with strict allocation boundaries: **Use GNU Parallel, signac, or Maestro**
- Merlin and AiiDA need workarounds for SPIN constraints

### Running on systems with persistent infrastructure

If you have access to persistent services (Redis, PostgreSQL, persistent job allocations):

| Tool | Recommended? | Why |
|------|-------------|-----|
| **GNU Parallel** | ✓ Still good | No infrastructure overhead |
| **signac** | ✓ Still good | No infrastructure overhead |
| **Maestro** | ✓ Still good | Works better with multi-step submission |
| **Merlin** | ✓✓ Excellent | Can fully leverage persistent workers |
| **AiiDA** | ✓✓ Excellent | Can set up proper daemon infrastructure |

---

## Decision Matrix Summary

Quick reference table for all scenarios:

| Scenario | Scale | Dependencies | Provenance | Allocation | Recommendation |
|----------|-------|--------------|-----------|------------|-----------------|
| Parameter sweep | <1k | No | No | Single | signac |
| One-time parallel | <1k | No | No | Single | GNU Parallel |
| Multi-step sim | 1k-10k | Yes | No | Multi | Maestro |
| Provenance study | 1k-100k | Yes | Yes | Multi | AiiDA |
| ML hyperparameter | >100k | Partial | No | Multi | Merlin |
| Large campaign | >100k | Yes | No | Multi | Merlin |
| Complex DAG | 10k-100k | Complex | No | Multi | Maestro |
| Reproducible research | Any | Yes | Yes | Any | AiiDA |

---

## How to Use This Decision Tree

### Step 1: Understand Your Problem

Ask yourself:
- How many tasks will I have?
- Do tasks depend on each other?
- How long will everything take?
- Do I need full reproducibility?

### Step 2: Follow the Decision Questions

Start with Question 1 and work through in order. Your answers eliminate tools from consideration.

### Step 3: Check Graduation Criteria

If you've used a tool before, confirm you haven't outgrown it by reviewing the graduation section.

### Step 4: Verify with Comparison Matrix

Use the [Comparison Matrix](comparison-matrix.md) to dive deeper into your recommended tool(s).

### Step 5: Check Installation Guides

Start with the appropriate [Installation Guide](installation-guides/):
- [GNU Parallel Setup](installation-guides/gnu-parallel-setup.md)
- [signac Setup](installation-guides/signac-setup.md)
- [Maestro Setup](installation-guides/maestro-setup.md)
- Merlin and AiiDA have detailed setup guides in their respective phase sections

---

## Examples: Tool Selection by Real Use Cases

### Example 1: "Process 500 data files"

**Questions:**
1. Multi-step? NO
2. Allocation-bounded? YES
3. Parameter organization? MAYBE

**Analysis:** Sounds like embarrassingly parallel work.

**Recommendation:** GNU Parallel (if very simple) or signac (if files map to parameter sets)

### Example 2: "Run CFD simulation 1000 times with varying parameters"

**Questions:**
1. Multi-step? MAYBE (setup → run → postprocessing)
2. Scale? ~1000 tasks
3. Allocation-bounded? Probably not (too much work)
4. Parameter tracking? YES

**Analysis:** Classic parameter sweep with dependencies.

**Recommendation:** signac (if simple) or Maestro (if setup/postprocessing is complex)

### Example 3: "Train ML model with 50,000 hyperparameter combinations"

**Questions:**
1. Multi-step? DEPENDS (training is single task, but grid search needs coordination)
2. Scale? 50,000 tasks
3. Allocation-bounded? NO
4. Need distributed workers? PROBABLY

**Analysis:** Large-scale embarrassingly parallel with no dependencies.

**Recommendation:** Merlin (if distributed workers available) or Maestro (if single allocations resubmitted)

### Example 4: "Publish DFT study with materials database"

**Questions:**
1. Multi-step? YES (structure optimization → property calculation)
2. Scale? 100-1000
3. Provenance critical? YES (for publication)
4. Allocation-bounded? NO

**Analysis:** Provenance is the deciding factor.

**Recommendation:** AiiDA (despite complexity, provenance requirements drive choice)

### Example 5: "Reprocess experimental data with different algorithms"

**Questions:**
1. Multi-step? Partially (algorithm selection affects output)
2. Scale? 10-100
3. Need reproducibility? YES (same data, different algorithms)
4. Need full audit trail? MAYBE

**Analysis:** Reproducibility important but not necessarily full provenance.

**Recommendation:** signac (excellent for tracking algorithm variants) or Maestro (if complex pipelines)

---

## Troubleshooting Your Decision

**"I'm torn between two tools"**

Create a minimal test workflow with one tool, then with another. Measure:
- Time to first results
- Effort to add a new task variant
- Ease of checking task status
- How intuitive the tool feels for your problem

The tool that feels natural is the right choice.

**"My needs keep changing"**

That's normal! Use graduation criteria to identify when to switch. No tool is final - you can always migrate:
- Start simple (GNU Parallel or signac)
- Graduate to Maestro as complexity grows
- Move to Merlin or AiiDA only when necessary

This progression maximizes time before infrastructure overhead becomes significant.

**"My team has different preferences"**

Start with what your team knows, graduating when the tool becomes a bottleneck. Familiarity is worth something - the time cost of learning a new tool is real.

That said, choosing the wrong tool for the scale can cost far more time than the learning curve.

**"This doesn't match my situation"**

Reach out to the seminar organizers or tool communities. Your problem may be:
- Unusual enough to warrant custom orchestration
- Better solved by combining tools
- A gap this seminar should document

---

## See Also

- [Comparison Matrix](comparison-matrix.md) - Detailed technical comparison
- [NERSC Best Practices](nersc-best-practices.md) - Perlmutter-specific guidance
- [Troubleshooting Guide](troubleshooting.md) - Common issues and solutions
- [Further Learning](further-learning.md) - Documentation and tutorials
