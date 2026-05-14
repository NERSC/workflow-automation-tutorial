# Merlin Example 1 Infrastructure Fixes Design

## Summary

This change fixes three interconnected infrastructure bugs in the Merlin example 1 tutorial (`03-merlin/example1-distributed/`). The core issue is that the spec file's `OUTPUT_PATH` points to a local directory on GPFS, a networked filesystem accessed through a forwarding layer (DVS) on compute nodes. When Merlin writes workspace files there, the underlying file-locking call (`fcntl.flock()`) is unsupported through DVS, producing `[Errno 524] ENOTSUPP` warnings that confuse attendees. Relocating `OUTPUT_PATH` to `$PSCRATCH` moves all Merlin workspace I/O onto Lustre, which supports the full POSIX file-locking interface natively.

Beyond the filesystem fix, two related bugs caused silent data-flow failures: per-step output paths used the global `$(OUTPUT_PATH)` variable instead of Merlin's built-in per-step `$(WORKSPACE)`, creating a race condition when multiple parameterized process steps wrote to the same absolute path; and the aggregate step's `find` command used the wrong path base and wrong directory-name separator, so it always returned zero results silently. A companion documentation fix corrects both READMEs, which incorrectly instructed attendees to start Redis on the login node — Redis binds to `localhost` by default and is unreachable from compute nodes. The corrected instructions describe a single-allocation workflow where Redis, `merlin run`, and `merlin run-workers` all execute on the same compute node.

## Definition of Done

1. `03-merlin/example1-distributed/spec.yaml`: `OUTPUT_PATH` changed to `$PSCRATCH/wf-seminar-merlin`; all per-step output references changed from `$(OUTPUT_PATH)/` to `$(WORKSPACE)/`; the aggregate `find` command fixed to navigate via `$(WORKSPACE)/../process/PARAM.$p` (was searching wrong path with wrong name pattern, silently producing empty results).
2. `03-merlin/README.md`: Prerequisites section updated — Redis must be started on the compute node (inside the `salloc` allocation), not the login node.
3. `03-merlin/example1-distributed/README.md`: False claim that login-node Redis is reachable from compute nodes removed; running instructions updated to reflect the working procedure.
4. Scope boundary: examples 2 and 3, and all other sections (00–04), are not touched.

## Acceptance Criteria

### merlin-ex1-infra-fixes.AC1: spec.yaml workspace relocates to $PSCRATCH
- **merlin-ex1-infra-fixes.AC1.1 Success:** `OUTPUT_PATH` in `env.variables` is `$PSCRATCH/wf-seminar-merlin`
- **merlin-ex1-infra-fixes.AC1.2 Success:** Running `merlin run` + `merlin run-workers` on a compute node creates the study workspace under `$PSCRATCH/wf-seminar-merlin/`
- **merlin-ex1-infra-fixes.AC1.3 Success:** No `[Errno 524]` / `Unknown error 524` warnings appear in worker output during a complete run

### merlin-ex1-infra-fixes.AC2: Per-step outputs use $(WORKSPACE) and data flows correctly
- **merlin-ex1-infra-fixes.AC2.1 Success:** `generate` step produces `generate/output.txt` in the study workspace (not in an `output/` subdirectory)
- **merlin-ex1-infra-fixes.AC2.2 Success:** Each `process/PARAM.N/` directory contains `result.txt` with non-empty content after workers complete
- **merlin-ex1-infra-fixes.AC2.3 Success:** `aggregate/summary.txt` contains aggregated content from all five `process/PARAM.N/result.txt` files
- **merlin-ex1-infra-fixes.AC2.4 Failure:** No `result.txt` files are written to a shared absolute path (no race condition between parameterized steps)

### merlin-ex1-infra-fixes.AC3: Section README Redis prerequisites are correct
- **merlin-ex1-infra-fixes.AC3.1 Success:** `03-merlin/README.md` instructs attendees to start Redis inside the `salloc` allocation on the compute node
- **merlin-ex1-infra-fixes.AC3.2 Success:** README includes explanation that Redis binds to `localhost` and is not reachable from compute nodes when started on a login node
- **merlin-ex1-infra-fixes.AC3.3 Failure:** No text in `03-merlin/README.md` instructs starting Redis on the login node

### merlin-ex1-infra-fixes.AC4: example1 README running instructions are correct
- **merlin-ex1-infra-fixes.AC4.1 Success:** `example1-distributed/README.md` shows a single-allocation workflow (Redis + merlin run + merlin run-workers all inside salloc)
- **merlin-ex1-infra-fixes.AC4.2 Failure:** The claim "Redis server you started on the login node is reachable from compute nodes" does not appear in `example1-distributed/README.md`
- **merlin-ex1-infra-fixes.AC4.3 Failure:** No two-terminal workflow (one login-node terminal, one compute-node terminal) appears in the running instructions

## Glossary

- **Merlin**: A Python-based workflow tool built on top of Maestro that adds distributed task dispatch via a message broker (Redis or RabbitMQ). Workers pull tasks from a queue and execute them in parallel across compute nodes.
- **spec.yaml**: The YAML file that defines a Merlin workflow — steps, commands, parameter spaces, environment variables, and the message broker connection.
- **`$(WORKSPACE)`**: A Merlin built-in variable that resolves to the unique per-step directory created by Merlin before the step runs. Distinct from `$(OUTPUT_PATH)`, which is a user-defined variable pointing to a shared root directory.
- **`$(OUTPUT_PATH)`**: A user-defined environment variable in the spec's `env.variables` block, conventionally used as the study workspace root. Not per-step — all parameterized instances of a step share this value, which causes a write race condition if used as an output path inside parameterized steps.
- **`$(SPECROOT)`**: A Merlin built-in variable resolving to the directory containing `spec.yaml`. Not suitable for navigating the runtime workspace tree.
- **`merlin run`**: The Merlin CLI command that sends workflow tasks to the message broker queue without executing them.
- **`merlin run-workers`**: The Merlin CLI command that starts worker processes that pull tasks from the queue and execute them.
- **Redis**: An in-memory key-value store used by Merlin as its default message broker. Binds to `localhost` by default, making it unreachable across node boundaries.
- **`salloc`**: The Slurm command that opens an interactive allocation on one or more compute nodes.
- **GPFS (Global Parallel File System)**: IBM's clustered filesystem used at NERSC for home directories (`$HOME`). Accessed from compute nodes via DVS, which does not support all POSIX file-locking primitives.
- **DVS (Data Virtualization Service)**: A Cray/HPE forwarding layer that proxies filesystem requests from compute nodes to GPFS servers. Does not implement `fcntl.flock()`, causing `[Errno 524] ENOTSUPP` when file-locking code runs on a compute node against a GPFS path.
- **Lustre**: A high-performance parallel filesystem used for scratch storage (`$PSCRATCH`) on Perlmutter. Accessed via native client on compute nodes; supports the full POSIX file-locking interface.
- **`$PSCRATCH`**: The Perlmutter environment variable pointing to a user's scratch directory on Lustre. Set automatically for all users.
- **`filelock`**: A Python library implementing cross-process file locking via `fcntl.flock()`. Used internally by Merlin; fails with errno 524 on GPFS paths accessed through DVS.
- **`fcntl.flock()`**: A POSIX system call for advisory file locking. Not implemented through DVS — the proximate cause of the `[Errno 524]` errors.
- **Race condition**: In the parameterized `process` step, multiple workers writing `result.txt` to the same shared `$(OUTPUT_PATH)/` path causes later writers to overwrite earlier results silently. Using `$(WORKSPACE)` gives each instance its own directory.

## Architecture

Configuration and documentation fix — no new components introduced. Three files change:

- `03-merlin/example1-distributed/spec.yaml`
- `03-merlin/example1-distributed/README.md`
- `03-merlin/README.md`

### spec.yaml: OUTPUT_PATH and workspace layout

`OUTPUT_PATH` changes from `./output` to `$PSCRATCH/wf-seminar-merlin`. Merlin uses this value as the study workspace root, so the workspace relocates from GPFS (accessed via DVS on compute nodes) to Lustre (accessed via native client). This eliminates the `OSError: [Errno 524] ENOTSUPP` warnings Merlin emits when `filelock` calls `fcntl.flock()` through DVS.

Per-step output paths change from `$(OUTPUT_PATH)/filename` to `$(WORKSPACE)/filename`. `$(WORKSPACE)` is Merlin's built-in variable resolving to the current step's unique workspace directory (created by Merlin before the step runs, no `mkdir` needed). This also fixes a pre-existing data-flow bug: the original spec wrote to `$(OUTPUT_PATH)/` subdirectories inside each step workspace, but cross-step references used `$(step.workspace)/filename` — a path mismatch that caused silent failures at every step boundary.

The aggregate step's `find` command changes from a broken `$(SPECROOT)/../example1_distributed_*` pattern (wrong path, wrong separator) to `$(WORKSPACE)/../process/PARAM.$p` — workspace-relative navigation that correctly locates sibling process step directories.

### README: Redis setup

Both READMEs update to reflect that Redis must run on the compute node inside the `salloc` allocation. Redis binds to `localhost` by default; a Redis process on a login node is not reachable from compute nodes (connection reset, errno 104). The fix changes the two-terminal workflow (login node + compute node) to a single-allocation workflow where Redis, `merlin run`, and `merlin run-workers` all execute on the same compute node.

## Existing Patterns

Investigation found 11 existing design plans in `docs/design-plans/` using the same `YYYY-MM-DD-slug.md` structure. This document follows that convention.

No prior Merlin tutorial spec uses `$(WORKSPACE)` — all existing examples use `$(OUTPUT_PATH)/` for step outputs. This design intentionally diverges from that pattern because `$(OUTPUT_PATH)/` with an absolute path creates a race condition across parameterized step instances; `$(WORKSPACE)` is the idiomatic Merlin variable for per-step output isolation.

## Implementation Phases

<!-- START_PHASE_1 -->
### Phase 1: Fix spec.yaml
**Goal:** Move workspace to Lustre and repair silent data-flow failures.

**Components:**
- `03-merlin/example1-distributed/spec.yaml` — `env.variables.OUTPUT_PATH`, `generate` step cmd, `process` step cmd, `aggregate` step cmd and find pattern

**Dependencies:** None

**Done when:** `merlin run` + `merlin run-workers` on a compute node produces `generate/output.txt`, `process/PARAM.{1-5}/result.txt`, and `aggregate/summary.txt` with non-empty content under `$PSCRATCH/wf-seminar-merlin/example1-distributed_*/`; no `[Errno 524]` warnings appear in worker output
<!-- END_PHASE_1 -->

<!-- START_PHASE_2 -->
### Phase 2: Fix section README Redis prerequisites
**Goal:** Correct Redis setup instructions in the section-level README.

**Components:**
- `03-merlin/README.md` — Prerequisites/Redis setup section: replace login-node instructions with compute-node salloc workflow; add explanation of why login-node Redis fails

**Dependencies:** None (documentation only)

**Done when:** README instructs attendees to start Redis inside the salloc allocation; no text refers to starting Redis on the login node
<!-- END_PHASE_2 -->

<!-- START_PHASE_3 -->
### Phase 3: Fix example1 README running instructions
**Goal:** Remove false login-node reachability claim and update running instructions to match working procedure.

**Components:**
- `03-merlin/example1-distributed/README.md` — remove line 25 (false reachability claim); replace two-terminal instructions with single-allocation workflow

**Dependencies:** None (documentation only)

**Done when:** README contains no claim that login-node Redis is reachable from compute nodes; running instructions show single-allocation workflow matching updated section README
<!-- END_PHASE_3 -->

## Additional Considerations

**Examples 2 and 3:** `example2-fault-tolerance/README.md` contains the same false Redis reachability claim (line 15). It is out of scope for this design but should be addressed in a follow-on change.

**`$PSCRATCH` availability:** `$PSCRATCH` is set automatically for all Perlmutter users. No setup required.
