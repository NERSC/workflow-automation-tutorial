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

This directory will contain three examples:
1. Parameter space definition and organization
2. Slurm job submission with signac-flow
3. Result aggregation across state points

(Examples will be added in Phase 3)

## Further Reading

- [signac official documentation](https://signac.io/)
- [signac-flow for HPC](https://signac.io/signac-flow/)
