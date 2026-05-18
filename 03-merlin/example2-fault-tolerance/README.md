# Example 2: Fault Tolerance with Automatic Retries

**Learning Objectives:**
- Use `$(MERLIN_RETRY)` exit code for automatic retries
- Configure `retry_delay` and `max_retries`
- Use `$(MERLIN_RESTART)` for checkpoint/restart patterns
- Handle transient failures gracefully

**Concepts:** Fault tolerance, retry strategies, persistent state, task restart

## Prerequisites

Complete the [Prerequisites section](../README.md#prerequisites) in the Merlin README before starting this example. You should have a compute node allocation via `salloc`, Redis running on that node, and `merlin info` showing both connections as `OK`.

## Workflow

- `flaky_task`: Fails randomly (50% chance), retries up to 3 times with 5s delay between attempts
- `checkpoint_task`: Simulates checkpoint/restart by tracking progress in a file, uses restart section to resume

## Running

All `merlin` commands must be run from the `03-merlin/` directory so Merlin finds the repo's `app.yaml` config automatically. All commands run inside the same `salloc` allocation where Redis is already running (see [Prerequisites](#prerequisites)).

```bash
cd 03-merlin/
merlin run example2-fault-tolerance/spec.yaml
merlin run-workers example2-fault-tolerance/spec.yaml
```

Tasks will fail initially, then retry until success or max_retries exceeded.

**Monitor progress:**
```bash
merlin status $(ls -td $PSCRATCH/wf-seminar-merlin/fault-tolerance-demo_* | head -1)
```

## Expected Output

Upon successful completion (under `$PSCRATCH/wf-seminar-merlin/fault-tolerance-demo_<timestamp>/`):
```
fault-tolerance-demo_<timestamp>/
├── flaky_task/
│   └── attempt.log       # Shows final attempt number (1-4)
└── checkpoint_task/
    ├── checkpoint.txt    # Final checkpoint value (5)
    ├── failed_once       # Marker file indicating restart occurred
    └── recovered         # Marker file indicating completion
```

## Key Concepts Demonstrated

1. **Automatic retry:** `exit $(MERLIN_RETRY)` in script triggers automatic retry with delay
2. **Retry configuration:** `retry_delay: 5` and `max_retries: 3` control retry behavior
3. **Restart capability:** `exit $(MERLIN_RESTART)` triggers restart section execution
4. **Checkpoint/resume:** Script tracks progress in checkpoint.txt, restart section resumes from checkpoint
5. **Transient failures:** 50% random failure in flaky_task demonstrates handling of transient errors

## Exercises

1. Modify `max_retries` to 1 - observe task failure when retries exhausted
2. Change failure probability in flaky_task.sh to 100% - verify it eventually fails
3. Remove checkpoint.txt manually mid-execution - observe restart from beginning
4. Add custom retry delay logic - implement exponential backoff in script
5. Add `MERLIN_HARD_FAIL` exit code - understand difference from `MERLIN_RETRY`
