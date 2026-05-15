# Human Test Plan: Merlin Example 1 Infrastructure Fixes

**Implementation plan:** `docs/implementation-plans/2026-05-14-merlin-ex1-infra-fixes/`
**Generated:** 2026-05-14
**HEAD SHA:** 5ef2b03

---

## Prerequisites

- NERSC Perlmutter account with access to `ntrain4` (or your own account)
- Conda environment `wf-seminar` set up per the top-level README
- All automated checks passing (run the verification script from repo root)
- A compute node allocation via `salloc` (30 minutes minimum recommended)

---

## Phase 1: Environment and Redis Setup

| Step | Action | Expected |
|------|--------|----------|
| 1.1 | Run `salloc --nodes=1 --qos=debug --time=00:30:00 --constraint=cpu --account=ntrain4` | Shell prompt changes to compute node (hostname begins with `nid`) |
| 1.2 | Run `module load python && conda activate wf-seminar` | No errors; prompt shows `(wf-seminar)` |
| 1.3 | Run `merlin --version` | Output: `merlin 1.13.0` |
| 1.4 | Run `redis-server --daemonize yes --loglevel warning` | No error output |
| 1.5 | Run `redis-cli ping` | Output: `PONG` |
| 1.6 | Run `cd 03-merlin/ && merlin info` | Output includes `broker server connection: OK` and `results server connection: OK` |

---

## Phase 2: Workspace Location and errno 524 (AC1.2, AC1.3)

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | Run `rm -rf $PSCRATCH/wf-seminar-merlin/example1-distributed_*` to clean prior runs | No errors (or "no such file" if first run) |
| 2.2 | From `03-merlin/`, run `merlin run example1-distributed/spec.yaml` | Output shows tasks being enqueued to Redis; no errors |
| 2.3 | Run `merlin run-workers example1-distributed/spec.yaml 2>&1 \| tee /tmp/merlin-workers.log` | Workers start, process tasks, and eventually exit. May take 1–3 minutes. |
| 2.4 | Run `ls $PSCRATCH/wf-seminar-merlin/` | At least one directory named `example1-distributed_<timestamp>/` exists |
| 2.5 | Run `grep -i 'errno 524\|error 524\|ENOTSUPP' /tmp/merlin-workers.log` | No output (exit code 1). Zero matches means no DVS/GPFS filelock warnings. |

---

## Phase 3: Per-Step Data Flow (AC2.1, AC2.2, AC2.3, AC2.4)

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | Set workspace variable: `STUDY=$(ls -d $PSCRATCH/wf-seminar-merlin/example1-distributed_* \| head -1) && echo $STUDY` | Prints the full path to the study workspace |
| 3.2 | Run `cat "$STUDY/generate/output.txt"` | File exists. Contains "Generated at" with a date, followed by five lines "Input data for PARAM 1" through "Input data for PARAM 5" |
| 3.3 | Run `for p in 1 2 3 4 5; do echo "--- PARAM.$p ---"; cat "$STUDY/process/PARAM.$p/result.txt"; done` | All five files exist and contain non-empty content. Each file's content should reference its respective PARAM value. |
| 3.4 | Run `cat "$STUDY/aggregate/summary.txt"` | Contains "Aggregating results from all PARAM values" header, followed by content from all five process results, followed by "Aggregation complete" |
| 3.5 | Run `find "$STUDY" -name result.txt -not -path '*/process/PARAM.*/result.txt'` | No output. No stray `result.txt` files exist outside `process/PARAM.N/` directories. |
| 3.6 | Run `for p in 1 2 3 4 5; do echo "PARAM.$p: $(head -1 "$STUDY/process/PARAM.$p/result.txt")"; done` | Each line shows distinct content corresponding to its PARAM value. If all five lines are identical, this indicates a race condition (FAIL). |

---

## Phase 4: Documentation Walkthrough (AC3.1, AC3.2, AC4.1, AC4.2, AC4.3)

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | Open `03-merlin/README.md` and read the "Redis setup" subsection (around lines 64–100) | Instructions say to start Redis on the compute node, not the login node. Includes "Why compute node, not login node?" explanation. Includes `salloc` command with `--nodes=1 --qos=debug --time=00:30:00 --constraint=cpu`. |
| 4.2 | In the same README, verify the localhost explanation is present | The "Why compute node, not login node?" paragraph explains that Redis binds to localhost (127.0.0.1) and is not reachable from other nodes. |
| 4.3 | Verify no instructions tell the user to start Redis on the login node | The README should only reference login nodes in the context of explaining why that approach fails. There should be no imperative instruction like "start Redis on the login node." |
| 4.4 | Open `03-merlin/example1-distributed/README.md` and read the "Running on Perlmutter" section | Instructions reference a single `salloc` allocation. All commands (`merlin run`, `merlin run-workers`) are shown in a single linear sequence, not split across "Terminal 1" / "Terminal 2". |
| 4.5 | Verify the example1 README contains no "login node" references | The phrase "login node" should not appear anywhere in this file. |
| 4.6 | Verify the example1 README contains no claim that Redis on the login node is "reachable from compute nodes" | No such sentence exists. |

---

## End-to-End: Full Tutorial Walkthrough

**Purpose:** Validates that a seminar attendee can follow the documentation from start to finish without encountering incorrect instructions, missing output, or filesystem errors.

**Steps:**

1. Start from a fresh login on Perlmutter (no prior `wf-seminar` state).
2. Follow `03-merlin/README.md` Prerequisites section exactly as written:
   - Set up conda environment
   - Get compute node allocation via `salloc`
   - Start Redis on the compute node
   - Verify with `redis-cli ping` and `merlin info`
3. Follow `03-merlin/example1-distributed/README.md` Running section exactly as written:
   - `cd 03-merlin/`
   - `merlin run example1-distributed/spec.yaml`
   - `merlin run-workers example1-distributed/spec.yaml`
   - `merlin status example1-distributed/spec.yaml`
4. Verify output structure matches the "Expected output structure" shown in the example1 README — all directories and files exist under `$PSCRATCH/wf-seminar-merlin/`.
5. Verify no errno 524 warnings appeared during worker execution.
6. Verify `summary.txt` contains aggregated results from all five parameter values.
7. Clean up with `redis-cli shutdown`.

**Pass criteria:** A user following the documented steps verbatim produces the expected output without errors, warnings, or confusion about which node to use for Redis.

---

## Human Verification Required

| Criterion | Why Manual | Steps |
|-----------|------------|-------|
| AC1.2: Workspace on Lustre | Requires `$PSCRATCH` filesystem and Merlin runtime to create workspace directories | Phase 2, steps 2.1–2.4 |
| AC1.3: No errno 524 | The `[Errno 524]` warning only manifests when `filelock` calls `fcntl.flock()` through DVS on GPFS from a compute node | Phase 2, step 2.5 |
| AC2.1: generate/output.txt exists | Requires Merlin runtime to resolve `$(WORKSPACE)` and execute the generate step | Phase 3, step 3.2 |
| AC2.2: process/PARAM.N/result.txt files | Requires Merlin runtime to distribute tasks via Redis workers and resolve per-parameter workspaces | Phase 3, step 3.3 |
| AC2.3: aggregate/summary.txt content | Requires Merlin runtime to resolve `$(process.workspace)` cross-step reference | Phase 3, step 3.4 |
| AC2.4: No shared-path race condition | Requires parallel Merlin worker execution to verify no race conditions | Phase 3, steps 3.5–3.6 |

---

## Traceability

| Acceptance Criterion | Automated Test | Manual Step |
|----------------------|----------------|-------------|
| AC1.1: OUTPUT_PATH value | grep (automated) | — |
| AC1.2: Workspace on Lustre | — | Phase 2, steps 2.1–2.4 |
| AC1.3: No errno 524 | — | Phase 2, step 2.5 |
| AC2.1: generate output | spec grep (automated) | Phase 3, step 3.2 |
| AC2.2: process outputs | spec grep (automated) | Phase 3, step 3.3 |
| AC2.3: aggregate output | spec grep (automated) | Phase 3, step 3.4 |
| AC2.4: No race condition | spec grep (automated) | Phase 3, steps 3.5–3.6 |
| AC3.1: salloc instructions | grep (automated) | Phase 4, step 4.1 |
| AC3.2: localhost explanation | grep (automated) | Phase 4, step 4.2 |
| AC3.3: No login-node Redis instruction | grep (automated) | Phase 4, step 4.3 |
| AC4.1: Single-allocation workflow | grep (automated) | Phase 4, step 4.4 |
| AC4.2: False reachability claim removed | grep (automated) | Phase 4, steps 4.5–4.6 |
| AC4.3: No two-terminal workflow | grep (automated) | Phase 4, step 4.4 |
