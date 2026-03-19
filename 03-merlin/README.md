# Section 3: Merlin - Distributed Coordination at Massive Scale

**Duration:** 40 minutes

**Concepts:** Distributed task queuing, Celery workers, persistent Redis queues, fault tolerance

## Overview

Merlin extends Maestro's YAML syntax with distributed worker pools and persistent queuing, enabling fault-tolerant execution at massive scale (millions of tasks).

## Infrastructure Requirements

Merlin requires **Redis** for persistent task queuing:
- **Deployment option 1 (recommended):** NERSC SPIN service
- **Deployment option 2:** Dedicated allocation with workflow QOS

See `resources/installation-guides/merlin-redis-setup.md` for deployment instructions.

## When to Use Merlin

✅ **Good for:**
- Massive-scale parameter sweeps (thousands to millions of tasks)
- Distributed coordination across multiple allocations
- Fault tolerance and automatic retry
- Long-running workflows spanning hours to days

❌ **Not suitable for:**
- Simple parameter sweeps (use GNU Parallel or signac)
- Workflows without distributed coordination needs (use Maestro)
- Full provenance tracking beyond task metadata (use AiiDA)

## Examples

This directory will contain three examples:
1. Distributed worker execution with Redis queues
2. Fault tolerance with intentional failures and retry
3. Massive-scale hyperparameter search (1000s of combinations)

(Examples will be added in Phase 5)

## Further Reading

- [Merlin GitHub repository](https://github.com/LLNL/merlin)
- [Merlin documentation](https://merlin.readthedocs.io/)
