# Section 1: signac - Parameter Space Organization

**Duration:** 25 minutes

**Concepts:** Parameter organization, filesystem-based state tracking, job aggregation

## Overview

signac provides parameter space organization and filesystem-based state management for computational experiments, building on GNU Parallel's parallelization with structured data organization.

## When to Use signac

✅ **Good for:**
- Managing experiments with 2-5 dimensional parameter spaces
- Filesystem-based state tracking (no database needed)
- Aggregating results across parameter combinations
- Restart and continuation of parameter sweeps

❌ **Not suitable for:**
- Complex multi-step dependencies (use Maestro)
- Real-time coordination across allocations (use Merlin)
- Full provenance tracking (use AiiDA)

## Examples

This directory contains three examples demonstrating signac's progression:

1. **example1-parameter-space**: 2D parameter space (temperature × pressure) with automatic directory organization. Shows how signac creates unique hash-based directories for each parameter combination without manual tracking.

2. **example2-job-submission**: signac-flow integration for Slurm job submission. Demonstrates how signac-flow generates submission scripts automatically, one per state point.

3. **example3-aggregation**: Query and aggregate results across the parameter space. Shows how to filter jobs by parameters and combine results for analysis.

## Further Reading

- [signac official documentation](https://signac.io/)
- [signac-flow for HPC](https://signac.io/signac-flow/)
