# AiiDA Low-Barrier Training Refactor Design

## Summary

The AiiDA section currently tells attendees to set up PostgreSQL, RabbitMQ, and a persistent daemon before running any examples — infrastructure that takes hours to configure and is not available interactively on Perlmutter. This makes AiiDA the only section in the tutorial where attendees cannot actually run the code during the seminar. The refactor fixes that by making `verdi presto` the default training path: one command creates a SQLite-backed AiiDA profile with a localhost computer, and all examples then run synchronously via `engine.run()` with no daemon required. Provenance tracking still works fully — `@calcfunction` captures the computation graph into SQLite just as it would into PostgreSQL.

The approach splits infrastructure concerns into two tiers rather than removing them. Tier 1 (examples 1-2, the visualization walkthrough in example 3) works entirely within `verdi presto`. Tier 2 is a "going further" section and a new production deployment resource doc that explain when SQLite becomes a bottleneck — multi-user deployments, high-throughput job submission, long-running daemons — and where to find the existing SPIN setup guide. The code changes are narrow: the `@calcfunction` and `@graph_builder` decorated functions need no edits; only the main execution block in `workflow.py`, the `load_profile()` call in `query_provenance.py`, and the documentation files change.

## Definition of Done

Refactor the AiiDA tutorial section (04-aiida) so that all examples run without PostgreSQL, RabbitMQ, or SPIN infrastructure by default. The training path uses `verdi presto` with SQLite and synchronous `run()` execution, making AiiDA accessible in interactive or short batch jobs. Production deployment with full infrastructure is documented separately as an upgrade path.

**Deliverables:**

1. **Examples 1-2 refactored** to run with `verdi presto` (SQLite, no daemon) using `run()` — attendees can execute them in an interactive session or short batch job with zero infrastructure setup beyond `verdi presto`.
2. **Example 3 refactored** to integrate an optional daemon/`submit()` tier alongside the existing visualization content — for attendees who want to try the full stack.
3. **Section README updated** — SQLite as default path, PostgreSQL as optional sidebar, infrastructure requirements demoted from "required" to "production-only".
4. **New `resources/aiida-production-deployment.md`** — bridges the training setup to real SPIN/workflow-QOS deployment, linking to the existing SPIN database setup guide.
5. **Section CLAUDE.md updated** to reflect new assumptions (SQLite default, daemon optional).
6. **Comparison matrix updated** if it currently references AiiDA's setup complexity in a way that no longer applies.

**Key constraints:**
- aiida-core is pre-installed in the conda environment; attendees just run `verdi presto`
- Don't modify `environment.yml` version pins without Perlmutter testing
- Keep pedagogical placeholder computations (no real science)
- Stay within the 35-minute section time budget

## Acceptance Criteria

### aiida-lowbar-training.AC1: Examples 1-2 run with verdi presto (SQLite, no daemon)
- **aiida-lowbar-training.AC1.1 Success:** After `verdi presto`, `python workflow.py --param 42` completes without error and prints the result PK
- **aiida-lowbar-training.AC1.2 Success:** Provenance nodes are created in SQLite — `verdi process list -a` shows the completed workflow
- **aiida-lowbar-training.AC1.3 Success:** `python query_provenance.py` finds and displays provenance from example 1's run
- **aiida-lowbar-training.AC1.4 Failure:** `query_provenance.py` prints a helpful message when no workflows exist (example 1 not run yet)
- **aiida-lowbar-training.AC1.5 Edge:** Examples work in both interactive sessions and short batch jobs on Perlmutter

### aiida-lowbar-training.AC2: Example 3 has tiered run/submit content
- **aiida-lowbar-training.AC2.1 Success:** Tier 1 (training) visualization commands work with SQLite provenance data from examples 1-2
- **aiida-lowbar-training.AC2.2 Success:** Tier 2 (going further) clearly explains `run()` vs `submit()` differences with code examples
- **aiida-lowbar-training.AC2.3 Success:** Tier 2 links to the production deployment resource doc for full setup instructions

### aiida-lowbar-training.AC3: Section README reflects SQLite-default approach
- **aiida-lowbar-training.AC3.1 Success:** Infrastructure Requirements section presents `verdi presto` (SQLite) as the default training path
- **aiida-lowbar-training.AC3.2 Success:** PostgreSQL + RabbitMQ are documented as production-only, not as prerequisites
- **aiida-lowbar-training.AC3.3 Success:** Quick Start section uses `verdi presto` (not `verdi presto --use-postgres`)
- **aiida-lowbar-training.AC3.4 Success:** No language describes examples as "conceptual" or "pedagogical only" — they're runnable
- **aiida-lowbar-training.AC3.5 Success:** README follows the same structure as sections 00-03 (title, duration, concepts, overview, why, when-to-use, examples, progression)

### aiida-lowbar-training.AC4: Production deployment resource doc exists
- **aiida-lowbar-training.AC4.1 Success:** `resources/aiida-production-deployment.md` explains when to upgrade from SQLite to PostgreSQL
- **aiida-lowbar-training.AC4.2 Success:** Doc covers SPIN deployment and workflow QOS as two production paths
- **aiida-lowbar-training.AC4.3 Success:** Doc links to existing `resources/installation-guides/aiida-database-setup.md` for detailed SPIN instructions
- **aiida-lowbar-training.AC4.4 Success:** Doc is concise — focuses on when/why to upgrade, not a full how-to duplicate

### aiida-lowbar-training.AC5: Section CLAUDE.md updated
- **aiida-lowbar-training.AC5.1 Success:** Expects section reflects SQLite default, daemon optional
- **aiida-lowbar-training.AC5.2 Success:** Guarantees section reflects runnable examples (not just conceptual)

### aiida-lowbar-training.AC6: Comparison matrix updated
- **aiida-lowbar-training.AC6.1 Success:** AiiDA's setup complexity reflects the tiered model (low for training, high for production)
- **aiida-lowbar-training.AC6.2 Success:** NERSC compatibility notes that SQLite mode works on login/compute nodes

## Glossary

- **AiiDA**: A Python framework for managing computational workflows with automatic provenance tracking. Stores every calculation input, output, and linkage in a database.
- **verdi**: The AiiDA command-line interface. Used to manage profiles, inspect provenance, and control the daemon.
- **verdi presto**: An AiiDA subcommand that creates a ready-to-use profile backed by SQLite and a localhost computer in roughly 30 seconds. Intended for quick starts and training environments.
- **SQLite**: A file-based relational database requiring no server process. AiiDA supports it as a storage backend; it covers all QueryBuilder operations used in the tutorial except `has_key` and `contains`.
- **PostgreSQL**: A full client-server relational database. AiiDA's production-recommended backend; required for multi-user or high-throughput deployments.
- **RabbitMQ**: A message broker that AiiDA's daemon uses to queue and distribute calculation jobs. Not needed when using `engine.run()` for synchronous execution.
- **daemon**: A background AiiDA process that picks up submitted calculations from the RabbitMQ queue and sends them to the scheduler. Required for `submit()`; not required for `run()`.
- **engine.run()**: An AiiDA function that executes a workflow synchronously in the calling process. Blocks until completion; no daemon or message broker needed.
- **engine.submit()**: An AiiDA function that hands a workflow off to the daemon asynchronously. Requires a running daemon and RabbitMQ.
- **@calcfunction**: An AiiDA Python decorator that wraps a function so every call creates provenance nodes (inputs, outputs, and the linkage between them) in the database.
- **@task.graph_builder**: An AiiDA decorator for defining workflow graphs — functions that wire together multiple `@calcfunction` calls into a dependency graph.
- **QueryBuilder**: AiiDA's database query API. Used to retrieve provenance nodes and relationships from the storage backend in a backend-agnostic way.
- **provenance graph**: The directed graph AiiDA records of every calculation: what data went in, what came out, and which function produced it. Inspectable via `verdi node graph generate`.
- **PK**: Primary key — AiiDA's integer identifier for any node in the provenance database. Printed after a workflow runs and used to look up results with `verdi` commands.
- **SPIN**: NERSC's container platform, used to host persistent services like the PostgreSQL and RabbitMQ instances that production AiiDA deployments require.
- **workflow QOS**: A Slurm quality-of-service tier at NERSC intended for long-running workflow orchestration jobs, relevant as an alternative to SPIN for hosting the AiiDA daemon.
- **load_profile()**: An AiiDA Python function that must be called in standalone scripts (run directly with `python`, not via `verdi run`) to initialize the database connection before any AiiDA API calls.
- **comparison matrix**: A reference document in `resources/` that grades each tutorial tool on setup complexity, NERSC compatibility, and other dimensions. Updated as part of this refactor to reflect AiiDA's tiered complexity.

## Architecture

The refactor replaces the "full infrastructure required" assumption with a two-tier model:

**Tier 1 (Training default):** `verdi presto` creates a SQLite-backed AiiDA profile with a localhost computer configured automatically. All examples use `engine.run()` for synchronous, in-process execution. No daemon, no RabbitMQ, no PostgreSQL. Attendees get full provenance tracking — every `@calcfunction` call creates nodes in the provenance graph stored in SQLite. Setup takes ~30 seconds.

**Tier 2 (Production upgrade path):** Documented in a separate resource file. Explains when and why to upgrade to PostgreSQL + RabbitMQ + daemon. Links to the existing 801-line SPIN deployment guide for the how-to.

The code changes are minimal. The three `@calcfunction` decorated functions in `workflow.py` already work with SQLite — the decorator handles provenance capture regardless of storage backend. The main change is how the workflow gets executed: replacing implicit `verdi run` context with explicit `engine.run()` calls.

### Data flow

```
verdi presto
  └── creates SQLite profile + localhost computer

python workflow.py --param 42
  └── engine.run(simple_workflow, param=Int(42))
        ├── prepare_data(42)  → Int(84)        [provenance node created]
        ├── compute(84)       → Int(7056)      [provenance node created]
        └── analyze(7056)     → Dict(7156)     [provenance node created]

python query_provenance.py
  └── QueryBuilder queries SQLite for provenance from above

verdi node graph generate <PK>
  └── generates visual provenance graph from SQLite data
```

### What stays the same

- All `@task.calcfunction` decorated functions — unchanged
- `@task.graph_builder` workflow definition — unchanged
- `code_wrapper.py` template — unchanged
- QueryBuilder query patterns — unchanged (SQLite supports all operators used)
- `verdi node graph generate` CLI — unchanged

### What changes

- `workflow.py` main block: explicit `engine.run()` instead of relying on `verdi run`
- `query_provenance.py`: add `load_profile()` call, add "run example 1 first" guidance
- All READMEs: rewritten for SQLite default path
- Section README: infrastructure section restructured
- Section CLAUDE.md: updated contracts

## Existing patterns

Investigation of sections 00-04 shows a consistent structure:

**Section READMEs** all follow: Title with duration → Concepts → Overview → "Why [Tool]?" → Core Concepts → Examples list → "When to Use" with checkmark/cross lists → Official Documentation links → Quick Start.

**Example READMEs** all follow: Learning Objectives → Concepts → Running instructions → Key Concepts → Expected Output → Exercises.

The AiiDA section already follows this structure. The refactor preserves it — only the content within these sections changes, not the structure itself.

**Training reservation pattern:** Only GNU Parallel's example 3 uses `submit.sh` wrappers with `NERSC_TRAINING_RESERVATION`. AiiDA doesn't need this — its examples run locally via `engine.run()`, not through `sbatch`.

**No divergence from existing patterns.** This refactor adjusts content within the established structure.

## Implementation phases

<!-- START_PHASE_1 -->
### Phase 1: Refactor example 1 (workflow-def)

**Goal:** Make the workflow example runnable with `verdi presto` and `engine.run()`.

**Components:**
- `04-aiida/example1-workflow-def/workflow.py` — change `if __name__` block to use `from aiida.engine import run` explicitly, add `load_profile()`, add post-execution output showing PK and suggested `verdi` commands
- `04-aiida/example1-workflow-def/README.md` — rewrite prerequisites (verdi presto, not PostgreSQL), running instructions (python, not verdi run), add Expected Output section

**Dependencies:** None (first phase)

**Done when:** `workflow.py` runs successfully after `verdi presto`, creates provenance nodes, prints result PK. README accurately describes the setup and execution flow.
<!-- END_PHASE_1 -->

<!-- START_PHASE_2 -->
### Phase 2: Refactor example 2 (provenance querying)

**Goal:** Make the provenance query example work against SQLite data from example 1.

**Components:**
- `04-aiida/example2-provenance/query_provenance.py` — add `load_profile()`, add guidance message when no workflows found ("Did you run example 1 first?"), verify all QueryBuilder operations used are SQLite-compatible
- `04-aiida/example2-provenance/README.md` — rewrite for SQLite context, add prerequisite note about running example 1 first, add Expected Output section

**Dependencies:** Phase 1 (example 1 must be updated first so the expected provenance data exists)

**Done when:** `query_provenance.py` successfully queries provenance created by example 1 running against SQLite. README accurately describes the dependency and expected output.
<!-- END_PHASE_2 -->

<!-- START_PHASE_3 -->
### Phase 3: Refactor example 3 (data-graph + tiered submit)

**Goal:** Add two-tier content — default visualization walkthrough plus optional daemon/submit documentation.

**Components:**
- `04-aiida/example3-data-graph/README.md` — restructure into Tier 1 (training: `verdi node graph generate`, ancestor-depth traversal, archive export — all work with SQLite) and Tier 2 (going further: explain `run()` vs `submit()` diff, what daemon provides, link to production deployment doc)

**Dependencies:** Phases 1-2 (visualization references provenance data from earlier examples)

**Done when:** README clearly separates training-default and production-upgrade tiers. Tier 1 commands work with SQLite. Tier 2 explains the upgrade path without requiring attendees to actually run it.
<!-- END_PHASE_3 -->

<!-- START_PHASE_4 -->
### Phase 4: Update section README and CLAUDE.md

**Goal:** Align the section-level documentation with the new SQLite-default approach.

**Components:**
- `04-aiida/README.md` — rewrite Infrastructure Requirements (training: verdi presto / production: PostgreSQL + RabbitMQ), update Quick Start commands, update Database Backend subsection, remove "conceptual/pedagogical" language, keep When to Use section as-is
- `04-aiida/CLAUDE.md` — update Expects (SQLite default, daemon optional), update Guarantees (examples are runnable, not just conceptual), update Key Decisions

**Dependencies:** Phases 1-3 (section docs must reflect the updated examples)

**Done when:** Section README and CLAUDE.md accurately describe the two-tier approach. No references to PostgreSQL or RabbitMQ as required for training.
<!-- END_PHASE_4 -->

<!-- START_PHASE_5 -->
### Phase 5: Create production deployment resource doc

**Goal:** Bridge the training setup to real SPIN/workflow-QOS production deployment.

**Components:**
- `resources/aiida-production-deployment.md` — new file covering: when to upgrade from SQLite (multi-user, high-throughput, daemon-based submission), PostgreSQL setup summary, RabbitMQ + daemon summary, SPIN deployment pointer, workflow QOS alternative pointer. Links to existing `resources/installation-guides/aiida-database-setup.md` for detailed instructions

**Dependencies:** Phase 4 (section README links to this doc)

**Done when:** Resource doc exists, covers when/why to upgrade, links to existing SPIN guide. Concise — focuses on decision-making, not full how-to.
<!-- END_PHASE_5 -->

<!-- START_PHASE_6 -->
### Phase 6: Update comparison matrix

**Goal:** Reflect that AiiDA's setup complexity depends on deployment tier.

**Components:**
- `resources/comparison-matrix.md` — update AiiDA's Setup Complexity rating from "High" to "Low (training) / High (production)", update NERSC Compatibility to note SQLite mode works on login/compute nodes, keep production-scale ratings for context

**Dependencies:** None (can run in parallel with other phases, but logically follows Phase 5)

**Done when:** Comparison matrix accurately reflects the tiered setup complexity. No misleading "High complexity" without qualification.
<!-- END_PHASE_6 -->

## Additional considerations

**SQLite QueryBuilder limitations:** The `has_key` and `contains` operators don't work with SQLite. The current `query_provenance.py` doesn't use either — it uses `filters={'ctime': {'>': '-7d'}}` and `filters={'value': target_value}`, both of which are supported. If future examples need these operators, they'd require PostgreSQL. Worth noting in the README but not a blocker.

**35-minute time budget:** The SQLite approach actually frees up time. Current section spends instructor time explaining infrastructure that attendees can't set up during the seminar. With `verdi presto`, attendees spend ~30 seconds on setup and the remaining time on actual provenance concepts. Net gain.

**Cleanup of `__pycache__` and `.pyc` files:** The `example1-workflow-def/` directory contains `code_wrapper.pyc` and `__pycache__/workflow.cpython-36.pyc` (Python 3.6 artifacts). These should be gitignored or removed, but that's outside the scope of this design.
