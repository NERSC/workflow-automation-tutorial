# HPC Workflow Management Tools Seminar

Last verified: 2026-05-14

## Tech Stack
- Language: Python 3.10, Bash
- Platform: NERSC Perlmutter (Slurm)
- Tools taught: GNU Parallel, signac, Maestro, Merlin, AiiDA
- Environment: conda (environment.yml) or pip (requirements.txt)

## Project Structure
- `00-gnu-parallel/` - Section 0: Baseline parallelization (30 min)
- `01-signac/` - Section 1: Parameter space organization (25 min)
- `02-maestro/` - Section 2: DAG-based workflow specification (30 min)
- `03-merlin/` - Section 3: Distributed coordination at scale (40 min)
- `04-aiida/` - Section 4: Provenance tracking (35 min)
- `resources/` - Comparison frameworks, decision trees, installation guides
- `docs/` - Implementation plans and progress tracking

## Conventions
- Sections are numbered 00-04 in progressive complexity order
- Each section has 3 examples: `example1-*`, `example2-*`, `example3-*`
- Each section has a README.md with: motivation, concepts, when-to-use, examples list
- Examples use placeholder computations (sleep, echo, basic math) not real science
- All examples must run on Perlmutter without modification after env setup
- Slurm account `ntrain4` used in job scripts (attendees change to their own)
- Training event reservation: attendees pass `-A ntrain4 --reservation=<name>` directly as CLI flags to `sbatch`
- Merlin commands must be run from `03-merlin/` so `./app.yaml` is auto-discovered (Merlin checks `./app.yaml` before `~/.merlin/app.yaml`)

## Invariants
- Progressive capability story: each tool adds exactly one major capability over the previous
- GNU Parallel (parallelism) -> signac (parameter organization) -> Maestro (DAG deps) -> Merlin (distributed scale) -> AiiDA (provenance)
- No example should require domain-specific scientific knowledge
- Merlin tutorial uses a local `redis-server` on the login node (bundled in conda env); production deployments use external Redis/RabbitMQ (NERSC SPIN)
- AiiDA training mode uses SQLite via `verdi presto` (no external services); production mode requires PostgreSQL + RabbitMQ (documented in `resources/aiida-production-deployment.md`)
- All Python scripts must work with Python 3.10+

## Boundaries
- Safe to edit: example scripts, READMEs, resources
- Never touch: `requirements.txt` or `environment.yml` version pins without testing on Perlmutter
- Do not add real scientific codes; examples stay pedagogical
