# Example 1: Simple Sequential DAG

**Learning Objectives:**
- Define multi-step workflows with dependencies in YAML
- Understand DAG execution order determined by `depends` keyword
- Use Maestro tokens (`$(SPECROOT)`, `$(WORKSPACE)`, `$(step_name.workspace)`)
- Run workflows on Perlmutter login nodes

**Concepts:** Sequential dependencies, declarative workflow specification, automatic execution ordering

## Workflow Structure

```
prepare → simulate → analyze → visualize
```

Each step depends on the previous:
- `prepare`: Generates input data
- `simulate`: Runs computation using prepared data
- `analyze`: Processes simulation output
- `visualize`: Creates plots from analyzed results

## Files

- `workflow.yaml` - Maestro workflow specification
- `scripts/prepare.sh` - Data preparation script
- `scripts/simulate.py` - Simple simulation (sleeps to simulate work)
- `scripts/analyze.py` - Result analysis
- `scripts/visualize.py` - Plotting (creates dummy plot)

## Running on Perlmutter

**On login node (quick test):**
```bash
module load python
cd /global/u1/w/$USER/workflow_tutorial_research/02-maestro/example1-simple-dag
maestro run workflow.yaml
```

Maestro creates a timestamped directory (e.g., `simple-dag_20260319-143022/`) containing:
- `prepare/` - Logs and outputs from prepare step (including `input.dat`)
- `simulate/` - Logs and outputs from simulate step (including `results.txt`)
- `analyze/` - Logs and outputs from analyze step (including `summary.txt`)
- `visualize/` - Logs and outputs from visualize step (including `plot.txt`)
- `meta/` - Maestro internal state files

**Check status:**
```bash
maestro status simple-dag_20260319-143022
```

**View results:**
```bash
# Prepared data
cat simple-dag_20260319-143022/prepare/input.dat

# Simulation output
cat simple-dag_20260319-143022/simulate/results.txt

# Analysis summary
cat simple-dag_20260319-143022/analyze/summary.txt

# Plot (would be PNG in real workflow)
cat simple-dag_20260319-143022/visualize/plot.txt
```

## Key Concepts Demonstrated

1. **Declarative dependencies:** `depends: [step-name]` ensures execution order
2. **Automatic ordering:** Maestro determines which steps can run in parallel (none here)
3. **Token usage:** `$(SPECROOT)` references workflow directory, `$(WORKSPACE)` writes outputs to each step's subdirectory
4. **Filesystem passing:** Each step reads from previous step's `$(step_name.workspace)`

## Expected Output

```
$ maestro run workflow.yaml
[TIMESTAMP] INFO: Loading specification from workflow.yaml
[TIMESTAMP] INFO: Launching study simple-dag...
[TIMESTAMP] INFO: Study simple-dag launched successfully.

$ maestro status simple-dag_20260319-143022
Step Name       | State     | Run Time | Elapsed Time
----------------|-----------|----------|-------------
prepare         | FINISHED  | 1s       | 1s
simulate        | FINISHED  | 3s       | 3s
analyze         | FINISHED  | 1s       | 1s
visualize       | FINISHED  | 1s       | 1s
```

## Exercises

1. Modify `simulate.py` to sleep longer - observe increased run time
2. Add a 5th step `archive` that depends on `visualize`
3. Break the dependency (remove `depends: [analyze]` from visualize) - what happens?
4. Add a `description` field to each step explaining its purpose
