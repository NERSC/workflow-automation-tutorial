# Example 2: Fault Tolerance with Automatic Retries

**Learning Objectives:**
- Use `$(MERLIN_RETRY)` exit code for automatic retries
- Configure `retry_delay` and `max_retries`
- Use `$(MERLIN_RESTART)` for checkpoint/restart patterns
- Handle transient failures gracefully

**Concepts:** Fault tolerance, retry strategies, persistent state, task restart

## Prerequisites

- Redis broker running (see `resources/installation-guides/merlin-redis-setup.md`)
- `~/.merlin/app.yaml` configured with Redis connection
- Merlin v1.13.0+ installed

## Workflow

- `flaky_task`: Fails randomly (50% chance), retries up to 3 times with 5s delay between attempts
- `checkpoint_task`: Simulates checkpoint/restart by tracking progress in a file, uses restart section to resume

## Running

```bash
# Terminal 1: Submit workflow to queue
merlin run spec.yaml

# Terminal 2: Start workers (in batch allocation)
salloc --nodes=1 --qos=debug --time=00:30:00 --constraint=cpu --account=m4408
merlin run-workers spec.yaml
```

Tasks will fail initially, then retry until success or max_retries exceeded.

**Monitor progress:**
```bash
merlin status spec.yaml
```

## Expected Output

Upon successful completion:
```
output/
├── attempt.log           # Shows final attempt number (1-4)
├── checkpoint.txt        # Final checkpoint value (5)
├── failed_once           # Marker file indicating restart occurred
└── recovered             # Marker file indicating completion
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
