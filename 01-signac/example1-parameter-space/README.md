# Example 1: Parameter Space Definition

## Overview

This example demonstrates signac's core feature: **automatic organization of parameter space**. When you define a 2D parameter space (temperature × pressure), signac creates a unique hash-based directory for each combination without requiring manual tracking.

## The State Point Concept

In signac, a **state point** is a dictionary of parameters uniquely identifying an experiment:

```python
{"temperature": 300, "pressure": 1.0}
```

signac computes a hash of this state point and creates a dedicated workspace directory. The hash ensures:
- **Uniqueness**: Different parameters get different directories
- **Determinism**: Same parameters always map to same directory
- **Portability**: Hash is consistent across systems

## Why This Matters

**Compared to GNU Parallel:** Instead of manually creating directory names like `T300_P1.0`, `T300_P10.0`, etc., signac automates this. You define parameter combinations programmatically, and signac handles the filesystem organization.

**Filesystem-based state tracking:** No database needed. The filesystem structure itself encodes your parameter space:
```
workspace/
├── abc12345def6789.../  (T=300, P=1.0)
├── def34567ghi8901.../  (T=300, P=10.0)
├── ghi56789jkl2345.../  (T=300, P=100.0)
└── ... (9 directories total for 3×3 space)
```

## Running This Example

1. Initialize the project:
   ```bash
   python init_project.py
   ```
   Creates 9 job directories (3 temperatures × 3 pressures)

2. Explore the structure:
   ```bash
   python explore_workspace.py
   ```
   Lists all jobs with their parameters and paths

3. Inspect the filesystem:
   ```bash
   ls -d workspace/*
   ```
   Shows auto-generated hash-based directory names

## What Happens Under the Hood

1. `init_project.py` calls `signac.init_project()` to create project infrastructure
2. For each parameter combination, `project.open_job({"temperature": ..., "pressure": ...})` returns a job object
3. `job.init()` creates the corresponding workspace directory
4. `explore_workspace.py` demonstrates querying: `signac.get_project()` loads the project and iteration over jobs works automatically

## Next Steps

See **example2-job-submission** to learn how signac-flow uses this parameter organization to generate Slurm submission scripts automatically.
