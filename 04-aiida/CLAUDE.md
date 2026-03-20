# AiiDA Section (04-aiida)

Last verified: 2026-03-20

## Purpose
Teaches comprehensive provenance tracking as the final capability step beyond Merlin's distributed coordination. Demonstrates why automatic data lineage matters for reproducible, publication-grade computational research.

## Contracts
- **Exposes**: 3 examples progressing from workflow definition to provenance querying to graph visualization
- **Guarantees**: Examples use aiida-workgraph (modern API), not legacy WorkChain. All examples are conceptual/pedagogical since AiiDA requires PostgreSQL+RabbitMQ infrastructure.
- **Expects**: PostgreSQL and RabbitMQ deployed (via SPIN or dedicated allocation). AiiDA profile configured with `verdi presto --use-postgres`.

## Dependencies
- **Uses**: aiida-core 2.8.0, aiida-workgraph 0.3.16, PostgreSQL, RabbitMQ
- **Used by**: Root README references this as Section 4; resources/ comparison matrix includes AiiDA
- **Boundary**: Does not import from other sections. Conceptually builds on Merlin (Section 3) but has no code dependency.

## Key Decisions
- WorkGraph over WorkChain: WorkGraph is the modern, Pythonic API; WorkChain is legacy
- Conceptual examples: AiiDA requires database infrastructure so examples are designed to be read/discussed even if infra is unavailable during seminar

## Key Files
- `README.md` - Section overview, concepts, progression from Merlin
- `example1-workflow-def/workflow.py` - WorkGraph workflow with decorator-based tasks
- `example2-provenance/query_provenance.py` - QueryBuilder usage for provenance queries
- `example3-data-graph/README.md` - Graph visualization walkthrough

## Gotchas
- AiiDA requires a running daemon (`verdi daemon start`) for workflow execution
- Database setup is non-trivial; see `resources/installation-guides/aiida-database-setup.md`
- SPIN deployment recommended over local database in allocation
