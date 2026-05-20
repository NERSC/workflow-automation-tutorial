# AiiDA Section (04-aiida)

Last verified: 2026-05-19

## Purpose
Teaches comprehensive provenance tracking as the final capability step beyond Merlin's distributed coordination. Demonstrates why automatic data lineage matters for reproducible, publication-grade computational research.

## Contracts
- **Exposes**: 3 examples progressing from workflow definition to provenance querying to graph visualization
- **Guarantees**: Examples use aiida-workgraph (modern API), not legacy WorkChain. All examples are runnable with `verdi presto` (SQLite, no daemon) — attendees execute them during the seminar.
- **Expects**: AiiDA profile configured with `verdi presto` (SQLite default). No PostgreSQL, RabbitMQ, or daemon required for training. Production deployment is documented separately.

## Dependencies
- **Uses**: aiida-core 2.8.0, aiida-workgraph 0.5.0, aiida-pythonjob 0.1.8 (pinned), node-graph 0.1.27 (pinned), graphviz (conda binary for `verdi node graph generate`), SQLite (training default via `verdi presto`)
- **Production uses**: PostgreSQL, RabbitMQ (documented in resources/aiida-production-deployment.md)
- **Used by**: Root README references this as Section 4; resources/ comparison matrix includes AiiDA
- **Boundary**: Does not import from other sections. Logically builds on Merlin (Section 3) but has no code dependency.

## Key Decisions
- WorkGraph over WorkChain: WorkGraph is the modern, Pythonic API; WorkChain is legacy
- SQLite default for training: `verdi presto` provides zero-setup AiiDA with full provenance tracking. PostgreSQL + RabbitMQ documented as production upgrade path.
- Synchronous execution: Examples use `run()`/`WorkGraph.run()` for synchronous, in-process execution. No daemon needed. `submit()` explained in example 3 as a "going further" topic.

## Key Files
- `README.md` - Section overview, concepts, tiered infrastructure requirements
- `cleanup.sh` - Removes runtime artifacts (*.dot.pdf, *.dot.png, *.aiida, __pycache__/) to restore freshly-cloned state
- `example1-workflow-def/workflow.py` - WorkGraph workflow with standalone execution via load_profile() + WorkGraph.run()
- `example2-provenance/query_provenance.py` - QueryBuilder usage for provenance queries with load_profile()
- `example3-data-graph/README.md` - Graph visualization walkthrough + production upgrade path

## Gotchas
- `load_profile()` must be called before any AiiDA operations in standalone scripts (not needed with `verdi run`)
- SQLite does not support `has_key` or `contains` QueryBuilder operators (not used in current examples)
- Production deployment (PostgreSQL + RabbitMQ + daemon) documented in `resources/aiida-production-deployment.md`
- `verdi process list -a` may show "last state change: not reported" on SQLite profiles (cosmetic only)
- `aiida-pythonjob==0.1.8` must be pinned: 0.2.0+ imports `get_stack_size` which was removed in aiida-core 2.8.0
- `node-graph==0.1.27` must be pinned in both `environment.yml` and `requirements.txt`; must match `aiida-workgraph==0.5.0` requirement exactly
