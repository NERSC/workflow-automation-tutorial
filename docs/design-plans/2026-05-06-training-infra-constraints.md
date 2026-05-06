# Training Infrastructure Constraints Design

## Summary

This project delivers a set of HPC workflow management tutorial materials for a hands-on workshop at NERSC Perlmutter. The workshop teaches five tools in progressive order — GNU Parallel, signac, Maestro, Merlin, and AiiDA — where each tool adds exactly one major capability over the previous. The materials consist of numbered example scripts, section READMEs, installation guides, and Slurm submit scripts, all designed to run on Perlmutter without modification once the conda environment is activated.

The central challenge this design addresses is an infrastructure mismatch: training accounts at NERSC have access to standard Slurm QOS queues but not to SPIN or workflow QOS, while the existing Merlin examples assume an external Redis broker that requires one of those two elevated access paths. The solution eliminates that dependency for working examples by running Redis as a background process inside the Slurm allocation itself and switching Merlin's worker dispatch mode from `slurm` to `local`, so that the full queue-based task flow is demonstrated without any external services. SPIN and workflow QOS are retained throughout the documentation but are uniformly reframed as a production tier — described accurately, but explicitly marked as requiring separate account access not available during the workshop.

## Definition of Done

The design removes all working-example dependencies on SPIN and workflow QOS from the workshop materials. Specifically:

1. The Merlin section gains a `setup-merlin-local.sh` script that starts a local `redis-server` within the Slurm allocation and writes `~/.merlin/app.yaml` pointing to `localhost`; all three Merlin example submit scripts use this setup before running `merlin run` and `merlin run-workers`.
2. `environment.yml` adds the `redis` conda package (which provides the `redis-server` binary).
3. All files that reference SPIN are updated so that: (a) working examples use only standard Slurm QOS within the training reservation, and (b) SPIN and workflow QOS are described together in a "production/after this training" tier — never presented as a working example path.
4. `resources/installation-guides/merlin-redis-setup.md` and `resources/installation-guides/aiida-database-setup.md` are restructured to lead with the training approach, with SPIN and workflow QOS as a documented-but-not-runnable production section.

**Out of scope:** Changes to AiiDA working examples (already use `verdi presto` / SQLite), changes to GNU Parallel / signac / Maestro examples, and any changes to version pins.

## Acceptance Criteria

### training-infra-constraints.AC1: Merlin examples run without SPIN or external services
- **training-infra-constraints.AC1.1 Success:** `sbatch submit.sh` in each Merlin example starts Redis, enqueues tasks, and runs workers within a single Slurm allocation using standard QOS
- **training-infra-constraints.AC1.2 Success:** `merlin status spec.yaml` shows all steps completed after the job finishes
- **training-infra-constraints.AC1.3 Success:** `batch.type: local` in spec files causes workers to run in-process rather than submitting new Slurm jobs
- **training-infra-constraints.AC1.4 Failure:** Running without SPIN access produces no connection errors to an external Redis
- **training-infra-constraints.AC1.5 Edge:** `~/.merlin/app.yaml` is backed up before being overwritten by the setup script

### training-infra-constraints.AC2: `redis-server` binary is available in the conda environment
- **training-infra-constraints.AC2.1 Success:** `conda env update` from `environment.yml` succeeds
- **training-infra-constraints.AC2.2 Success:** `redis-server --version` resolves inside the activated `wf-seminar` environment
- **training-infra-constraints.AC2.3 Success:** `redis-cli ping` to a running local Redis returns `PONG`
- **training-infra-constraints.AC2.4 Failure:** Adding the conda-forge `redis` package does not conflict with the existing pip `redis>=6.0,<7.0` Python client

### training-infra-constraints.AC3: All prose SPIN and workflow QOS references use production-tier framing
- **training-infra-constraints.AC3.1 Success:** No file describes SPIN or workflow QOS as a path for working examples run by training attendees
- **training-infra-constraints.AC3.2 Success:** Every section that mentions SPIN or workflow QOS also states that it requires separate account access not available to training accounts
- **training-infra-constraints.AC3.3 Success:** `03-merlin/README.md` Infrastructure Requirements section has two tiers: training (local Redis) and production (SPIN + workflow QOS)
- **training-infra-constraints.AC3.4 Failure:** No file uses "SPIN (recommended)" or "workflow QOS fallback" without the production-only qualification

### training-infra-constraints.AC4: Installation guides lead with the training approach
- **training-infra-constraints.AC4.1 Success:** `merlin-redis-setup.md` Section 1 describes local Redis setup; SPIN is Section 2; workflow QOS is Section 3
- **training-infra-constraints.AC4.2 Success:** `aiida-database-setup.md` Section 1 describes verdi presto / SQLite (training); production PostgreSQL+RabbitMQ is in later sections
- **training-infra-constraints.AC4.3 Success:** Each production section in both guides opens with a sentence noting SPIN access or workflow QOS approval is required

## Glossary

- **AiiDA**: A Python framework for computational science workflows that records full data provenance — inputs, outputs, and the links between them — in a queryable graph database.
- **batch.type**: A field in a Merlin YAML spec that controls how workers are launched. `slurm` submits new Slurm jobs; `local` runs workers in the current allocation without submitting additional jobs.
- **Celery**: A Python distributed task queue library. Merlin uses Celery workers to consume tasks from a message broker (Redis in this context).
- **conda-forge**: A community-maintained channel for the conda package manager that provides a broader set of binary packages than the default Anaconda channel.
- **DAG**: Directed Acyclic Graph. A representation of a workflow as a set of steps connected by directed dependencies, with no cycles, used by tools like Maestro to determine execution order.
- **debug QOS**: A Slurm Quality of Service tier at NERSC with short time limits and small node counts, intended for interactive testing and short jobs.
- **Maestro**: A Python-based workflow tool that executes steps defined as a DAG in a YAML spec file, tracking dependencies and step status.
- **Merlin**: A workflow framework built on Celery and a message broker that is designed for large-scale parameter sweeps by distributing tasks across many workers.
- **message broker**: A service that mediates communication between a task producer and task consumers by maintaining a queue. Merlin requires a live broker (Redis or RabbitMQ) to coordinate workers.
- **`merlin run`**: The Merlin CLI command that reads a spec file and enqueues all tasks into the broker.
- **`merlin run-workers`**: The Merlin CLI command that starts Celery workers that pull tasks from the broker and execute them.
- **NERSC SPIN**: A container orchestration service at NERSC (based on Kubernetes/Rancher) that can host persistent services such as Redis or PostgreSQL outside of a Slurm allocation. Requires a separate SPIN account.
- **`redis-server`**: The Redis server binary. In this design it runs as a daemon inside a Slurm job rather than as a persistent external service.
- **`redis-cli ping`**: A one-shot Redis client command used to test broker connectivity; a healthy server responds with `PONG`.
- **reservation (`--reservation`)**: A Slurm flag that directs a job to a pre-reserved partition created for the training event, reducing queue wait times for attendees.
- **signac**: A Python framework for managing parameter spaces and associated file-based data, giving each parameter combination a unique workspace directory.
- **Slurm**: The workload manager and job scheduler used on NERSC Perlmutter. Jobs are submitted with `sbatch`, interactive allocations with `salloc`.
- **SQLite**: A serverless, file-based relational database. AiiDA's `verdi presto` command configures AiiDA to use SQLite, removing the need for a PostgreSQL server during training.
- **`verdi presto`**: An AiiDA CLI command that sets up a lightweight AiiDA profile backed by SQLite, requiring no external database or message broker. Intended for development and training use.
- **workflow QOS**: A Slurm Quality of Service tier at NERSC designed for long-running workflow jobs that act as persistent brokers or orchestrators. Requires a separate approval process; not available to standard training accounts.
- **`~/.merlin/app.yaml`**: The Merlin broker configuration file. It specifies the URL of the Redis (or RabbitMQ) instance that Merlin's Celery workers connect to.

## Architecture

Training accounts at NERSC have access to standard Slurm QOS queues and a reserved partition for the training event. They do not have SPIN accounts or workflow QOS grants. This design maps that access ceiling onto the workshop materials.

**Working examples** run entirely within a single Slurm allocation using standard or debug QOS, optionally with `--reservation` injected by the existing `submit.sh` wrapper pattern. No external persistent services are required.

**Documentation** describes SPIN and workflow QOS as a paired production tier — two paths that are available after the workshop once attendees have their own project accounts, but neither of which is demonstrated as a working example.

The principal technical change is in the Merlin section. Merlin's distributed queue paradigm requires a live message broker (Redis). Without SPIN or workflow QOS, that broker runs as a background process (`redis-server`) inside the Slurm allocation itself. The spec's `batch.type` is changed from `slurm` to `local` so `merlin run-workers` launches Celery workers in the current allocation rather than submitting new Slurm jobs. Tasks still flow through Redis — the queue concept is fully demonstrated — but workers stay in the same allocation instead of spanning multiple jobs.

AiiDA already uses `verdi presto` (SQLite, no PostgreSQL or RabbitMQ) for training mode and requires no changes to working examples.

```
Training example execution model (Merlin):

  Slurm allocation (standard QOS + optional --reservation)
  ┌──────────────────────────────────────────────────────┐
  │  redis-server --daemonize yes --port 6379            │
  │  merlin run spec.yaml          # enqueue tasks       │
  │  merlin run-workers spec.yaml  # local Celery workers│
  └──────────────────────────────────────────────────────┘

Production model (described, not demonstrated):
  NERSC SPIN: persistent Redis container
  OR
  Workflow QOS: long-lived broker job with minimized allocation cost
  + workers spanning multiple independent allocations
```

## Existing Patterns

Investigation found one established submit script at `00-gnu-parallel/example3-slurm-integration/submit.sh`. That script injects `--reservation` and `--account=ntrain4` from environment variables. Merlin example submit scripts do **not** follow this pattern — they are plain Slurm job scripts without reservation injection. Attendees add `--reservation` and account flags directly to their commands or edit the script header as instructed.

No existing submit scripts exist in Merlin examples (`03-merlin/`). The three spec files (`example1-distributed/spec.yaml`, `example2-fault-tolerance/spec.yaml`, `example3-massive-scale/spec.yaml`) all use `batch.type: slurm`, which will change to `batch.type: local`.

## Implementation Phases

<!-- START_PHASE_1 -->
### Phase 1: Environment — add redis-server binary

**Goal:** Make `redis-server` and `redis-cli` available inside the `wf-seminar` conda environment.

**Components:**
- `environment.yml` — add `redis` to the conda-forge dependencies block (this package provides the server and CLI binaries; it is distinct from the `redis` PyPI package, which provides only the Python client and is already present under `pip`)
- Update the comment at the bottom of `environment.yml` to reflect that local Redis is used for training rather than an external service

**Dependencies:** None (first phase)

**Done when:** `conda env update` succeeds; `redis-server --version` and `redis-cli --version` resolve inside the activated environment
<!-- END_PHASE_1 -->

<!-- START_PHASE_2 -->
### Phase 2: Merlin local-Redis setup script

**Goal:** Provide a reusable script that starts Redis and writes the Merlin broker config, so each Merlin example can source it without duplicating setup logic.

**Components:**
- `03-merlin/setup-merlin-local.sh` (new) — starts `redis-server` in daemon mode on port 6379, polls `redis-cli ping` until ready, writes `~/.merlin/app.yaml` pointing broker and results backend to `localhost:6379`

**Dependencies:** Phase 1 (redis-server binary must exist)

**Done when:** Script runs inside a Slurm allocation; `redis-cli ping` returns `PONG`; `cat ~/.merlin/app.yaml` shows localhost endpoints
<!-- END_PHASE_2 -->

<!-- START_PHASE_3 -->
### Phase 3: Merlin spec files and example infrastructure

**Goal:** Update all three Merlin examples so they run entirely within a single Slurm allocation, and provide plain Slurm job scripts for each example.

**Components:**
- `03-merlin/example1-distributed/spec.yaml` — change `batch.type: slurm` → `batch.type: local`
- `03-merlin/example2-fault-tolerance/spec.yaml` — same change
- `03-merlin/example3-massive-scale/spec.yaml` — same change
- `03-merlin/example1-distributed/submit.sh` (new) — plain Slurm batch script: loads environment, sources `../../setup-merlin-local.sh`, runs `merlin run spec.yaml` and `merlin run-workers spec.yaml`; no reservation injection
- `03-merlin/example2-fault-tolerance/submit.sh` (new) — same structure
- `03-merlin/example3-massive-scale/submit.sh` (new) — same structure
- Each example's `README.md` — replace Terminal 1 / Terminal 2 / separate `salloc` instructions with the single-job `sbatch submit.sh` approach; update Prerequisites to remove SPIN reference; note that `--reservation` and account are added manually when needed

**Dependencies:** Phase 2 (setup script must exist before submit scripts reference it)

**Done when:** Each `sbatch submit.sh` runs end-to-end in a debug allocation; tasks are enqueued and consumed via local Redis; `merlin status spec.yaml` shows completed steps
<!-- END_PHASE_3 -->

<!-- START_PHASE_4 -->
### Phase 4: Merlin section README restructure

**Goal:** Update `03-merlin/README.md` to present local Redis as the training approach and SPIN + workflow QOS as a paired production description.

**Components:**
- `03-merlin/README.md` — restructure the **Infrastructure Requirements** section into two tiers:
  - *Training (this workshop):* local Redis in Slurm allocation
  - *Production (after this workshop):* SPIN (persistent Redis container) or workflow QOS (long-lived broker job); described, not demonstrated
- Update **Perlmutter/NERSC compatibility** to remove "SPIN (recommended)" and "workflow QOS fallback" framing
- Update **Quick Start** prerequisite block

**Dependencies:** Phase 3 (working example approach must be finalized)

**Done when:** `03-merlin/README.md` contains no sentence presenting SPIN or workflow QOS as a path for working examples; production tier section covers both options
<!-- END_PHASE_4 -->

<!-- START_PHASE_5 -->
### Phase 5: Installation guides restructure

**Goal:** Reorder both Merlin and AiiDA installation guides so the training approach is Section 1 and the production tier (SPIN + workflow QOS) is a clearly labelled later section.

**Components:**
- `resources/installation-guides/merlin-redis-setup.md` — add **Section 1: Training setup (local Redis)** before existing SPIN content; rename current Option 1 to **Section 2: Production Option A — NERSC SPIN**; add **Section 3: Production Option B — Workflow QOS**; add brief framing paragraph explaining neither production option is available to training accounts
- `resources/installation-guides/aiida-database-setup.md` — same restructuring: training setup (verdi presto / SQLite, already works) as Section 1; SPIN PostgreSQL+RabbitMQ as Section 2; workflow QOS as Section 3

**Dependencies:** Phase 4 (README framing must be stable before installation guides are aligned to it)

**Done when:** Both guides lead with the training approach; each production section begins with a sentence noting it requires SPIN access or a workflow QOS grant; no production section is labeled "recommended" without qualification
<!-- END_PHASE_5 -->

<!-- START_PHASE_6 -->
### Phase 6: Cross-cutting SPIN and workflow QOS reference audit

**Goal:** Update all remaining files that reference SPIN or workflow QOS to use the production-tier framing established in Phases 4–5.

**Components:**
- `README.md` (root)
- `04-aiida/README.md` and `04-aiida/example3-data-graph/README.md`
- `resources/comparison-matrix.md`, `resources/decision-tree.md`, `resources/nersc-best-practices.md`, `resources/README.md`
- `STATUS-REPORT.md`, `VALIDATION-REPORT.md`
- All files under `docs/implementation-plans/` and `docs/design-plans/` that contain SPIN or workflow QOS references (these are historical; update prose to match new framing)
- `.gitignore` comment referencing SPIN (update to reflect training vs production distinction)

Scope: ~35 files identified by grep. Change is tone and categorization, not content removal — SPIN and workflow QOS remain documented, just labelled as production-only.

**Dependencies:** Phase 5 (canonical framing must be established in installation guides first)

**Done when:** `grep -r "SPIN" .` returns no results where SPIN is described as available to training attendees or as the "recommended" option without a qualification that it requires separate account access
<!-- END_PHASE_6 -->

## Additional Considerations

**Redis lifecycle:** Redis started inside a Slurm allocation dies when the job ends. This is intentional and pedagogically honest — one of the teaching points of Phase 3 is that this is exactly why production deployments use SPIN or workflow QOS. The README should make this explicit.

**~/.merlin/app.yaml clobbering:** The setup script overwrites any existing Merlin config. For training accounts this is safe (no pre-existing config). Add a backup step in the script for safety.

**redis conda package version:** The conda-forge `redis` package version should be pinned only after testing confirms the binary is compatible with the `redis>=6.0,<7.0` Python client already in the pip section. Until tested on Perlmutter, add without a version pin and document the dependency.
