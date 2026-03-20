# Example 2: Fault Tolerance with Automatic Retries

**Learning Objectives:**
- Use `$(MERLIN_RETRY)` exit code for automatic retries
- Configure `retry_delay` and `max_retries`
- Use `$(MERLIN_RESTART)` for checkpoint/restart patterns
- Handle transient failures gracefully

**Concepts:** Fault tolerance, retry strategies, persistent state, task restart

## Workflow

- `flaky_task`: Fails randomly, retries up to 3 times with 5s delay
- `checkpoint_task`: Uses restart section to resume from checkpoint

## Running

```bash
merlin run spec.yaml
merlin run-workers spec.yaml
```

Tasks will fail initially, then retry until success or max_retries exceeded.
