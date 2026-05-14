# Human Test Plan: Merlin Prerequisites & Setup Redesign

**Implementation plan:** `docs/implementation-plans/2026-05-13-merlin-prereqs/`
**Commit:** `136ca2dc974ea2ea5b633c491bdd5a15491bec3c`
**Date:** 2026-05-13

## Prerequisites

- Access to NERSC Perlmutter (login node)
- Repository cloned at the commit above
- `module load python` available
- Automated checks passing (after fixing the 4 grep pattern issues noted below)

## Known Test Script Issues (non-blocking)

| Check | Issue | Fix |
|-------|-------|-----|
| AC1.1 `grep -A 5` window | `merlin --version` at line offset 7 | Widen to `grep -A 8` |
| AC5.1 spec.yaml `queue:` (x3) | Matches `task_queue:` (Merlin routing), not Slurm `queue:` | Exclude `task_queue` from grep |

## Phase 1: Environment Verification (AC2.2)

| Step | Action | Expected |
|------|--------|----------|
| 1 | SSH to Perlmutter: `ssh perlmutter.nersc.gov` | Login node shell |
| 2 | `cd /path/to/workflow_tutorial_research && git checkout 136ca2dc` | HEAD at test commit |
| 3 | `module load python` | Python module loaded |
| 4 | `conda env update -f environment.yml` | Environment installs/updates (may take 2-5 min) |
| 5 | `conda activate wf-seminar` | Prompt changes to `(wf-seminar)` |
| 6 | `which redis-server` | Prints path like `/global/common/.../wf-seminar/bin/redis-server` |
| 7 | `redis-server --version` | Prints `Redis server v=7.x.x` or `v=8.x.x` |
| 8 | `python -c "import redis; print(redis.__version__)"` | Prints version (e.g., `6.x.x`) without ImportError |

**Pass criteria:** Steps 6-8 all produce valid output. redis-server binary and Python redis client coexist without conflict.

## Phase 2: Structural Pattern Verification (AC5.2)

| Step | Action | Expected |
|------|--------|----------|
| 1 | Open `02-maestro/README.md` lines 41-50 (Prerequisites section) | Shows simple conda activate block |
| 2 | Open `03-merlin/README.md` Prerequisites section | Shows two-path structure |
| 3 | Confirm `### If you completed earlier sections` heading present | Exact wording matches |
| 4 | Confirm `### First time? Set up the environment` heading present | Exact wording matches |
| 5 | Verify returning-user path contains: module load, conda activate, merlin --version, skip-ahead link | All four elements present |
| 6 | Verify new-user path contains: link to `../README.md`, module load, conda activate, merlin --version | All four elements present |
| 7 | Verify Redis-specific content (### Redis setup, ### Merlin configuration, ### Cleanup) appears AFTER both paths | These headings are at a lower document position |
| 8 | Confirm no repeated/conflicting instructions between the two paths | Each path gives equivalent outcome via different starting points |

**Pass criteria:** Merlin README follows a two-path convergence pattern. Merlin-specific infrastructure steps appear after the convergence point.

## Phase 3: End-to-End New Attendee Walkthrough (AC6.1)

**Pre-cleanup (start from clean state):**
```bash
rm -f ~/.merlin/app.yaml
redis-cli shutdown 2>/dev/null || true
```

| Step | Action | Expected |
|------|--------|----------|
| 1 | Read the "First time? Set up the environment" section | Directs to `../README.md#setup-instructions` |
| 2 | Follow top-level README setup (if not already done) | conda environment created |
| 3 | Return to 03-merlin/README.md, run: `module load python` | No error |
| 4 | Run: `conda activate wf-seminar` | Prompt shows `(wf-seminar)` |
| 5 | Run: `merlin --version` | Prints `merlin 1.13.0` |
| 6 | Proceed to "Redis setup". Run: `redis-server --daemonize yes --loglevel warning` | No output (daemon started) |
| 7 | Run: `redis-cli ping` | Prints `PONG` |
| 8 | Proceed to "Merlin configuration". Run: `merlin config create` | Creates `~/.merlin/app.yaml` |
| 9 | Run the `cat > ~/.merlin/app.yaml << 'EOF' ... EOF` block (copy-paste from README) | File overwritten with Redis config |
| 10 | Run: `merlin info` | Output includes `broker server connection: OK` and `results server connection: OK` |
| 11 | Proceed to "Cleanup". Run: `redis-cli shutdown` | No output (Redis stopped) |
| 12 | Verify cleanup: Run `redis-cli ping` | Prints `Could not connect to Redis at 127.0.0.1:6379: Connection refused` |

**Pass criteria:** All 12 steps complete without errors. Commands copy-paste directly from the README without modification.

## Path Convergence Verification (AC1.3)

| Step | Action | Expected |
|------|--------|----------|
| 1 | Read the "If you completed earlier sections" path entirely | Contains: activate env, verify version, skip-ahead link |
| 2 | Read the "First time?" path entirely | Contains: setup reference, activate env, verify version |
| 3 | Confirm no conflicting instructions between paths | No contradictions |
| 4 | Confirm both paths result in equivalent state before Redis setup | Both end with Merlin installed and verified |

## Returning User Flow

| Step | Action | Expected |
|------|--------|----------|
| 1 | Assuming environment already exists: `module load python && conda activate wf-seminar` | Environment active |
| 2 | Run: `merlin --version` | Prints `merlin 1.13.0` |
| 3 | Follow the "skip ahead to Redis setup" link | Jumps to `### Redis setup` section |
| 4 | Complete Redis setup and Merlin configuration (Phase 3 steps 6-10) | `merlin info` shows OK |

**Pass criteria:** Returning user reaches working state without re-reading setup instructions or visiting top-level README.

## Example1 Integration Test

| Step | Action | Expected |
|------|--------|----------|
| 1 | Complete all Prerequisites (Redis running, merlin info OK) | Working state |
| 2 | Navigate to `03-merlin/example1-distributed/README.md` | References `../README.md#prerequisites` |
| 3 | Run: `cd 03-merlin/example1-distributed && merlin run spec.yaml` | Tasks submitted to Redis |
| 4 | In separate terminal: `salloc --nodes=1 --qos=debug --time=00:30:00 --constraint=cpu --account=ntrain4` | Allocation granted |
| 5 | Run: `merlin run-workers spec.yaml` | Workers start consuming tasks |
| 6 | Run: `merlin status spec.yaml` | Shows task progress/completion |

**Pass criteria:** Workers connect to login-node Redis. Tasks execute successfully.

## Traceability Matrix

| Acceptance Criterion | Automated Test | Manual Step |
|----------------------|----------------|-------------|
| AC1.1 | grep for heading + version check | -- |
| AC1.2 | grep for heading + README reference | -- |
| AC1.3 | Python position check | Path Convergence steps 1-4 |
| AC2.1 | grep for `redis-server --daemonize yes` | Phase 3 step 6 |
| AC2.2 | redis-server in environment.yml | Phase 1 steps 6-8 |
| AC2.3 | grep for "background" + "redis-cli ping" | Phase 3 step 7 |
| AC2.4 | grep for "cleanup" + "redis-cli shutdown" | Phase 3 steps 11-12 |
| AC3.1 | grep for "merlin config" | Phase 3 step 8 |
| AC3.2 | grep for broker: + results_backend: | Phase 3 step 9 |
| AC3.3 | grep for troubleshooting + error patterns | -- |
| AC4.1 | grep for merlin --version + 1.13.0 | Phase 3 step 5 |
| AC4.2 | grep for merlin info + expected output | Phase 3 step 10 |
| AC4.3 | grep for both failure modes | -- |
| AC5.1 | No m4408; bank: ntrain4 everywhere | -- |
| AC5.2 | -- (human only) | Phase 2 steps 1-8 |
| AC5.3 | grep for ../README.md#prerequisites | -- |
| AC6.1 | -- (human only) | Phase 3 steps 1-12 |
| AC6.2 | grep for merlin-redis-setup.md + "production" | -- |
