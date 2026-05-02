# Human Test Plan: AiiDA Low-Barrier Training Refactor

**Implementation plan:** `docs/implementation-plans/2026-05-01-aiida-lowbar-training/`
**Generated:** 2026-05-01
**Coverage:** 21/21 acceptance criteria covered

## Prerequisites

- Perlmutter login node access with conda environment from `environment.yml` active
- `verdi presto` has been run successfully (creates SQLite-backed AiiDA profile)
- Working directory is the repository root

## Phase 1: Core Workflow Execution (AC1.1, AC1.2)

| Step | Action | Expected |
|------|--------|----------|
| 1 | `cd 04-aiida/example1-workflow-def && python workflow.py --param 42` | Exit code 0. Output contains "Running workflow with param=42...", then "Workflow completed! PK: N" where N is an integer, followed by three `verdi` command suggestions. |
| 2 | `verdi process list -a` | At least one row appears. The process label column shows `simple_workflow`. State column shows `Finished [0]`. |
| 3 | Copy the PK from step 2, run `verdi process show <PK>` | Displays workflow inputs (including `param` with value 42), outputs, and called calcfunctions (`prepare_data`, `compute`, `analyze`). |

## Phase 2: Provenance Querying (AC1.3, AC1.4)

| Step | Action | Expected |
|------|--------|----------|
| 1 | `cd 04-aiida/example2-provenance && python query_provenance.py` | Exit code 0. Output shows "Found N workflows in last 7 days" where N >= 1, lists at least one PK with label, and "Calculations with input 42:" with at least one calcfunction PK and label. |
| 2 | `verdi presto --profile-name test-empty` | Creates a new empty profile. |
| 3 | `verdi profile setdefault test-empty` | Switches default profile. |
| 4 | `cd 04-aiida/example2-provenance && python query_provenance.py` | Exit code 0 (no crash). Output shows "Found 0 workflows in last 7 days", "No workflows found. Did you run example 1 first?", and "No calculations found with input value 42." with suggested run command. |
| 5 | `verdi profile setdefault <original-profile-name>` then `verdi profile delete test-empty --force` | Restores original profile and cleans up test profile. |

## Phase 3: Batch Job Execution (AC1.5)

| Step | Action | Expected |
|------|--------|----------|
| 1 | `srun --time=5 --nodes=1 --constraint=cpu --qos=debug --account=ntrain4 python 04-aiida/example1-workflow-def/workflow.py --param 42` | Job completes without error. Output contains "Workflow completed! PK:". |
| 2 | `verdi process list -a` | New workflow entry appears from the batch execution with state `Finished [0]`. |

Note: Requires an active Perlmutter allocation. If `debug` QOS is unavailable, use any `salloc` interactive allocation instead.

## Phase 4: Graph Visualization and Archives (AC2.1)

| Step | Action | Expected |
|------|--------|----------|
| 1 | `verdi process list -a` and note a PK | At least one workflow PK is available. |
| 2 | `verdi node graph generate <PK>` | Exit code 0. Output says "Success: Output written to <PK>.dot.pdf". |
| 3 | `ls <PK>.dot.pdf` | File exists on disk. |
| 4 | `verdi node graph generate <PK> --ancestor-depth 999` | Exit code 0. Generates a graph showing the full ancestor chain back to initial inputs. |
| 5 | `verdi archive create --all test_archive.aiida` | Creates `test_archive.aiida` file. |
| 6 | `verdi archive info test_archive.aiida` | Displays metadata: number of nodes, users, computers, etc. |
| 7 | `rm -f test_archive.aiida *.dot.pdf` | Cleanup successful. |

## Phase 5: Documentation Content Review (AC2.2, AC3.1, AC3.5, AC4.1, AC4.4)

These criteria require human judgment about clarity and structure.

| Step | Action | Expected |
|------|--------|----------|
| 1 | Open `04-aiida/example3-data-graph/README.md` and read the "Tier 2: Going Further" section. | The `run()` vs `submit()` comparison table is clear and covers: execution model, blocking behavior, infrastructure requirements, use case, and fault tolerance. Code examples are syntactically correct. A reader unfamiliar with AiiDA can understand when to use each. |
| 2 | Open `04-aiida/README.md` and read the "Infrastructure Requirements" section. | The training path (SQLite via `verdi presto`) is presented first and prominently. A reader's first impression is that setup is simple. Production infrastructure is described second, clearly labeled as "beyond the seminar." |
| 3 | Compare `04-aiida/README.md` headings against `00-gnu-parallel/README.md` and `02-maestro/README.md`. | All major structural sections are present. No major sections present in other READMEs are missing from the AiiDA README. |
| 4 | Open `resources/aiida-production-deployment.md`. Read the "When to Upgrade from SQLite" section. | Clear trigger conditions are listed. A reader can determine whether their use case warrants upgrading. |
| 5 | Assess overall conciseness of `resources/aiida-production-deployment.md` (85 lines). | Document answers "when" and "why" to upgrade, then links to `aiida-database-setup.md` for "how." Feels like a decision-making bridge document, not a how-to duplicate. |

## End-to-End: Full Attendee Walkthrough

**Purpose:** Validate the complete training experience from zero-state to provenance visualization.

1. Start with a fresh `verdi presto` profile (or use existing one).
2. Read `04-aiida/README.md` Quick Start section. Follow the commands exactly as written:
   - `verdi presto`
   - `cd example1-workflow-def && python workflow.py --param 42`
   - `python ../example2-provenance/query_provenance.py`
   - `verdi node graph generate <PK>` (using PK from step 2)
3. Verify each step completes without error and output matches what the README describes.
4. Read example READMEs and confirm the exercises are achievable with the training setup.
5. From `example3-data-graph/README.md`, follow the link to `resources/aiida-production-deployment.md`. Confirm it loads and is reachable via the relative path.
6. From the production deployment doc, confirm the link to `installation-guides/aiida-database-setup.md` works.

**Expected:** An attendee can complete the entire section in approximately 35 minutes with no infrastructure errors, no confusing "you need PostgreSQL" messages, and a clear understanding of what AiiDA does and when to upgrade.

## End-to-End: Progressive Capability Story

**Purpose:** Validate that the AiiDA section fits into the seminar's progressive narrative.

1. Read the "Progression from Merlin" section in `04-aiida/README.md`. Confirm it explicitly states what Merlin provided and what AiiDA adds.
2. Read `resources/comparison-matrix.md` AiiDA entries. Confirm setup complexity shows "Low (training) / High (production)" and NERSC compatibility notes mention SQLite on login/compute nodes.
3. Read `04-aiida/CLAUDE.md`. Confirm Purpose, Contracts, and Key Decisions align with the training-first, production-optional approach.

## Traceability Matrix

| Acceptance Criterion | Automated Verification | Manual Step |
|----------------------|----------------------|-------------|
| AC1.1 - workflow.py runs, prints PK | Code: `run_get_node()`, prints PK and verdi suggestions | Phase 1, Steps 1-3 |
| AC1.2 - Provenance nodes in SQLite | Code: `@task.calcfunction` + `run_get_node()` creates nodes | Phase 1, Steps 2-3 |
| AC1.3 - query_provenance.py finds provenance | Code: QueryBuilder queries, prints expected format | Phase 2, Step 1 |
| AC1.4 - Helpful message when empty | Code: Two `if count == 0` branches with guidance | Phase 2, Steps 2-5 |
| AC1.5 - Interactive + batch execution | Code: `load_profile()` + synchronous `run_get_node()` | Phase 3, Steps 1-2 |
| AC2.1 - Tier 1 viz commands work | README: Standard `verdi` CLI commands, SQLite-compatible | Phase 4, Steps 1-7 |
| AC2.2 - Tier 2 run() vs submit() | Structural: 5x `run()`, 5x `submit()`, comparison table | Phase 5, Step 1 |
| AC2.3 - Tier 2 links to production doc | Grep: Two links, target exists | End-to-End, Step 5 |
| AC3.1 - verdi presto as default | Grep: Leads Infrastructure Requirements section | Phase 5, Step 2 |
| AC3.2 - PostgreSQL production-only | Grep: No "required" + "postgresql" match | Automated only |
| AC3.3 - No --use-postgres | Grep: Zero matches | Automated only |
| AC3.4 - No conceptual/pedagogical language | Grep: Zero matches | Automated only |
| AC3.5 - README structure alignment | Heading extraction | Phase 5, Step 3 |
| AC4.1 - Upgrade decision guidance | Grep: Heading + trigger table present | Phase 5, Step 4 |
| AC4.2 - SPIN and workflow QOS paths | Grep: Both paths documented | Automated only |
| AC4.3 - Link to aiida-database-setup.md | Grep: Three links, target exists | End-to-End, Step 6 |
| AC4.4 - Concise bridge document | Line count: 85 lines | Phase 5, Step 5 |
| AC5.1 - Expects reflects SQLite default | Grep: verdi presto, no PostgreSQL required | Automated only |
| AC5.2 - Guarantees reflects runnable | Grep: "runnable", zero conceptual/pedagogical | Automated only |
| AC6.1 - Tiered setup complexity | Grep: "Low (training) / High (production)" | Automated only |
| AC6.2 - SQLite on login/compute nodes | Grep: "runs on login and compute nodes" | Automated only |
