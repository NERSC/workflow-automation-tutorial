# AiiDA Production Deployment at NERSC

This guide helps you decide when to upgrade from the training SQLite setup (`verdi presto`) to a production PostgreSQL + RabbitMQ deployment, and which deployment path to choose.

## When to Upgrade from SQLite

The `verdi presto` SQLite setup is sufficient for:
- Learning AiiDA and prototyping workflows
- Single-user, interactive work sessions
- Workflows that complete in minutes
- Small-scale studies (hundreds of provenance nodes)

**Upgrade when any of these apply:**

| Trigger | Why SQLite Falls Short |
|---------|----------------------|
| Multiple users share the database | SQLite handles concurrent writes poorly — "database is locked" errors |
| Workflows take hours or days | You need the daemon to manage jobs asynchronously (`submit()` instead of `run()`) |
| High-throughput studies (thousands of calculations) | SQLite performance degrades at scale; PostgreSQL handles large provenance graphs efficiently |
| You need fault tolerance | The daemon restarts failed calculations automatically; `run()` does not |
| Long-term shared provenance | PostgreSQL supports concurrent access and proper backup strategies |

## What Changes in Production

| Component | Training (`verdi presto`) | Production |
|-----------|--------------------------|------------|
| Storage | SQLite (file-based) | PostgreSQL (client-server) |
| Message broker | None | RabbitMQ |
| Execution | `run()` — synchronous, in-process | `submit()` — asynchronous, daemon-managed |
| Daemon | Not needed | Required (`verdi daemon start`) |
| Setup time | ~30 seconds | Hours (one-time) |
| Maintenance | None | Database backups, service monitoring |

## Deployment Path 1: SPIN Containers (Recommended)

SPIN is NERSC's Kubernetes-based platform for persistent services. It hosts PostgreSQL and RabbitMQ as always-on containers that survive restarts and are accessible from Perlmutter compute nodes.

**Best for:**
- Multi-user deployments (research groups sharing AiiDA)
- Always-on provenance database
- Long-running campaigns spanning weeks or months

**Trade-offs:**
- Requires SPIN account and basic container familiarity
- One-time setup is more involved
- No allocation hours consumed for database hosting

**Detailed instructions:** [AiiDA Database Setup Guide — SPIN Deployment](installation-guides/aiida-database-setup.md#option-1-spin-deployment-recommended)

## Deployment Path 2: Workflow QOS

Run PostgreSQL, RabbitMQ, and the AiiDA daemon in a long-running Slurm job under the `workflow` quality-of-service tier. The `workflow` QOS allows jobs to run for up to 90 days continuously.

**Best for:**
- Single-user campaigns with a defined time window
- Simpler setup (no SPIN account needed)
- Short-term production runs (days to weeks)

**Trade-offs:**
- Uses allocation hours while running
- Services stop when the job ends
- Must restart between campaigns

**Detailed instructions:** [AiiDA Database Setup Guide — Dedicated Allocation](installation-guides/aiida-database-setup.md#option-2-dedicated-allocation-fallback)

## Upgrading Your Profile

To migrate from SQLite to PostgreSQL while keeping your existing provenance data:

1. Set up PostgreSQL (via SPIN or workflow QOS — see links above)
2. Create a new PostgreSQL-backed profile: `verdi profile setup core.psql_dos`
3. Export your SQLite provenance: `verdi archive create --all training_data.aiida`
4. Import into the new profile: `verdi -p <new-profile> archive import training_data.aiida`

Your complete provenance history transfers to the production database.

## Quick Reference

| Question | Answer |
|----------|--------|
| Can I keep using SQLite? | Yes, if you're single-user and workflows are short |
| Will I lose my training data? | No — export with `verdi archive create`, import into production profile |
| Which deployment path is simpler? | Workflow QOS (no SPIN account needed) |
| Which deployment path is more robust? | SPIN (survives job termination, no allocation cost) |
| Where are the full setup instructions? | [AiiDA Database Setup Guide](installation-guides/aiida-database-setup.md) |
