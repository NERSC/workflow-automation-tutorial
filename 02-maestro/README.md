# Section 2: Maestro - DAG-Based Workflow Specification

**Duration:** 30 minutes

**Concepts:** Directed Acyclic Graphs (DAG), declarative YAML workflows, dependency resolution

## Overview

Maestro introduces DAG-based workflow specification using declarative YAML, enabling multi-step pipelines with explicit dependencies and Slurm integration.

## When to Use Maestro

✅ **Good for:**
- Multi-step workflows with clear dependencies (prep → simulate → analyze → visualize)
- Declarative workflow definition (YAML, not Python code)
- Parameter sweeps within DAG structure
- Medium-scale workflows (hundreds to low thousands of tasks)

❌ **Not suitable for:**
- Massive scale requiring distributed coordination (use Merlin)
- Real-time task distribution across workers (use Merlin)
- Comprehensive provenance tracking (use AiiDA)

## Examples

This directory will contain three examples:
1. Simple sequential DAG (3-4 steps)
2. Parameter sweeps with DAG structure
3. Perlmutter-specific Slurm configuration

(Examples will be added in Phase 4)

## Further Reading

- [Maestro GitHub repository](https://github.com/LLNL/maestrowf)
- [Maestro documentation](https://maestrowf.readthedocs.io/)
