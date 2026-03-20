# Example 2: Parameter Sweeps with Dependencies

**Learning Objectives:**
- Define parameter sweeps using `global.parameters`
- Combine parameter variations with workflow dependencies
- Use wildcard dependencies `[step_*]` to wait for all parameter instances
- Aggregate results across parameter combinations

**Concepts:** Parameter expansion, parameterized workflows, funnel dependencies, result aggregation

## Workflow Structure

```
[run_simulation SIZE=10] ─┐
[run_simulation SIZE=20] ─┼─→ [aggregate_results]
[run_simulation SIZE=30] ─┘
```

Maestro automatically expands parameter combinations:
- 3 `run_simulation` jobs (one per SIZE value)
- 1 `aggregate_results` job (waits for all SIZE runs via wildcard)

## Parameter Sweep Mechanics

**global.parameters block:**
```yaml
global.parameters:
  SIZE:
    values: [10, 20, 30]
    label: SIZE.%%
```

**Effect:**
- Any step referencing `$(SIZE)` runs once per value
- Maestro creates SIZE-specific workspaces automatically
- Label determines directory naming (e.g., `SIZE.10`, `SIZE.20`, `SIZE.30`)

**Wildcard dependencies:**
```yaml
depends: [run_simulation_*]
```
Waits for ALL parameter instances of `run_simulation` before starting.

## Files

- `workflow.yaml` - Maestro workflow with parameter sweep
- `scripts/run_simulation.py` - Parameterized simulation
- `scripts/aggregate_results.py` - Collects results across all SIZE values

## Running on Perlmutter

```bash
module load python
cd /global/u1/w/$USER/workflow_tutorial_research/02-maestro/example2-param-sweeps
maestro run workflow.yaml
```

**Expected directory structure:**
```
workflow_20260319-150000/
├── run_simulation_SIZE.10/
│   └── output.txt
├── run_simulation_SIZE.20/
│   └── output.txt
├── run_simulation_SIZE.30/
│   └── output.txt
└── aggregate_results/
    └── summary.txt
```

**View aggregated results:**
```bash
cat workflow_20260319-150000/aggregate_results/summary.txt
```

## Key Concepts Demonstrated

1. **Parameter expansion:** One step definition creates multiple jobs
2. **Funnel dependency:** `depends: [step_*]` waits for all parameter instances
3. **Workspace isolation:** Each parameter combination gets separate directory
4. **Result aggregation:** Final step collects outputs from all parameter runs

## Expected Output

```
$ maestro run workflow.yaml
[TIMESTAMP] INFO: Loading specification from workflow.yaml
[TIMESTAMP] INFO: Launching study workflow...
[TIMESTAMP] INFO: Study workflow launched successfully.

$ maestro status workflow_20260319-150000
Step Name                    | State     | Run Time | Elapsed Time
-----------------------------|-----------|----------|-------------
run_simulation_SIZE.10       | FINISHED  | 1s       | 1s
run_simulation_SIZE.20       | FINISHED  | 2s       | 2s
run_simulation_SIZE.30       | FINISHED  | 3s       | 3s
aggregate_results            | FINISHED  | 1s       | 1s
```

Note: `run_simulation` jobs run in parallel (if resources available), then `aggregate_results` runs after all complete.

## Exercises

1. Add a second parameter (e.g., `TIMESTEP: [1, 5, 10]`) - how many jobs run?
2. Modify `run_simulation` to use both SIZE and TIMESTEP
3. Remove the wildcard (`depends: [run_simulation]`) - what error occurs?
4. Add a visualization step that depends on `aggregate_results`
5. Change SIZE values to `[100, 200, 300, 400, 500]` - verify scaling

## Comparison to signac

**signac approach:**
```python
# Define parameter space
project.open_job({"size": 10, "timestep": 1}).init()
project.open_job({"size": 20, "timestep": 1}).init()
# ... manual submission for each combination
```

**Maestro approach:**
```yaml
global.parameters:
  SIZE:
    values: [10, 20]
  TIMESTEP:
    values: [1, 5]
# Automatic expansion + dependency management
```

Maestro adds workflow orchestration to parameter organization.

## Known Limitations

**Workspace path construction:** The aggregate_results step uses `$(SPECROOT)/../../$(WORKSPACE)` to construct the path to parameter-specific workspaces. This relative path construction may be fragile depending on Maestro's working directory behavior. In production workflows, consider using absolute paths or environment variables for more robust path handling.
