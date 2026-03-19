# Section 4: AiiDA - Comprehensive Provenance Tracking

**Duration:** 35 minutes

**Concepts:** Automated provenance, data lineage, reproducible workflows, publication-grade documentation

## Overview

AiiDA provides comprehensive provenance tracking and reproducibility for computational research, storing complete execution history in a database to enable publication-grade documentation of how results were generated.

## Infrastructure Requirements

AiiDA requires:
- **PostgreSQL** for provenance database
- **RabbitMQ** for workflow coordination

**Deployment option 1 (recommended):** NERSC SPIN services
**Deployment option 2:** Dedicated allocation with workflow QOS

See `resources/installation-guides/aiida-database-setup.md` for deployment instructions.

## When to Use AiiDA

✅ **Good for:**
- Research requiring full provenance tracking
- Publication-grade reproducibility
- Long-term data management (years)
- Computational materials science, quantum chemistry workflows
- "Where did this result come from?" queries

❌ **Not suitable for:**
- Simple parameter sweeps (overhead not justified - use signac)
- Rapid prototyping (setup complexity - use Maestro)
- Workflows without provenance requirements (use Maestro/Merlin)

## Examples

This directory will contain three examples:
1. AiiDA workgraph with automatic provenance
2. Provenance demonstration: restart from any point, history capture
3. Data lineage visualization and "result origin" queries

(Examples will be added in Phase 6)

## Further Reading

- [AiiDA official documentation](https://aiida.readthedocs.io/)
- [AiiDA tutorials](https://aiida-tutorials.readthedocs.io/)
