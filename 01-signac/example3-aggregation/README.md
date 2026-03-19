# Example 3: Result Aggregation Across State Points

## Overview

This example demonstrates **querying and aggregating results across your parameter space**. Once simulations complete, signac's query API lets you:
- Filter jobs by parameters
- Retrieve results from multiple jobs
- Combine data for analysis

## The Aggregation Pattern

Traditional approach (error-prone):
```bash
# Manually find and aggregate results
for d in workspace/T300_*; do
    cat $d/results.txt
done
# Requires manual parameter parsing from directory names
```

With signac:
```python
jobs = project.find_jobs({"temperature": {"$gte": 400}})
for job in jobs:
    result = read_result(job.fn("results.txt"))
    # Access parameters via job.sp.temperature, job.sp.pressure
```

## Components

### generate_fake_data.py

Populates result files so we can demonstrate aggregation without waiting for actual simulations. Creates `results.txt` in each job's directory with a synthetic value that depends on parameters.

Usage:
```bash
python generate_fake_data.py
```

### analyze_results.py

Demonstrates the signac query API:

**Query syntax:**
```python
project.find_jobs({"temperature": {"$gte": 400}})
```

This uses MongoDB-style operators:
- `{"$gte": 400}`: Greater than or equal to 400
- `{"$lt": 100}`: Less than 100
- `{"$in": [1.0, 10.0]}`: In this list
- And others (MongoDB operators)

**Aggregation workflow:**
1. Query jobs by parameters: `project.find_jobs(...)`
2. Check if results exist: `job.isfile("results.txt")`
3. Read and combine: Loop through jobs, extract values
4. Analyze: Use NumPy, pandas, matplotlib, etc.

## Running This Example

### Setup

First, initialize the parameter space:
```bash
cd ../example1-parameter-space
python init_project.py
```

### Generate Results

From example3-aggregation:
```bash
python generate_fake_data.py
```

### Aggregate and Analyze

```bash
python analyze_results.py
```

Output shows:
- Number of jobs matching the query (T >= 400)
- Mean value across these jobs
- Individual results per job

## Query Examples

Modify `analyze_results.py` to try different queries:

```python
# All jobs with pressure = 10.0
jobs = project.find_jobs({"pressure": 10.0})

# All jobs with temperature in [300, 400]
jobs = project.find_jobs({"temperature": {"$in": [300, 400]}})

# All jobs (no filter)
jobs = project.find_jobs()
```

## Filesystem Observations

Unlike GNU Parallel or shell scripts, you never parse directory names or filenames. Parameters come from the job object itself. This makes code:
- **Robust**: No string parsing
- **Maintainable**: Clear intent
- **Flexible**: Easy to change parameter names

## Next Phase

This concludes signac examples. The next workflow tools (Maestro, Merlin, AiiDA) build on this foundation with additional features:
- **Maestro**: DAG dependencies, complex workflows
- **Merlin**: Real-time task coordination
- **AiiDA**: Full provenance tracking and database
