# Resources Section

Last verified: 2026-05-01

## Purpose
Provides cross-cutting reference materials that help attendees choose the right tool after the seminar ends. These are take-home decision frameworks, not teaching materials.

## Contracts
- **Exposes**: Comparison matrix, decision tree, troubleshooting guide, installation guides, best practices, further learning links
- **Guarantees**: All 5 tools (GNU Parallel, signac, Maestro, Merlin, AiiDA) are covered in every cross-cutting document. Installation guides are Perlmutter-specific.
- **Expects**: Content stays tool-neutral and factual; no advocacy for a single tool.

## Dependencies
- **Uses**: References official documentation URLs for each tool
- **Used by**: Root README links here; section READMEs reference installation guides
- **Boundary**: Does not contain runnable examples; those belong in section directories

## Key Files
- `comparison-matrix.md` - 5-dimension comparison (interface, infra, deps, scale, use case)
- `decision-tree.md` - Flowchart: problem characteristics -> tool recommendation
- `troubleshooting.md` - Common issues and solutions per tool
- `nersc-best-practices.md` - Perlmutter-specific configuration patterns and anti-patterns
- `further-learning.md` - Curated links to docs, tutorials, community
- `aiida-production-deployment.md` - When/how to upgrade from SQLite training setup to PostgreSQL+RabbitMQ production
- `installation-guides/` - Per-tool setup on Perlmutter (includes SPIN deployment for Merlin/AiiDA)

## Invariants
- Every cross-cutting document must cover all 5 tools, not a subset
- Installation guides must include Perlmutter setup commands (module load where applicable; GNU Parallel is pre-installed and needs none)
- Troubleshooting entries follow pattern: symptom, cause, fix
