# Merlin Prerequisites & Setup Redesign

## Summary

This design plan covers the rewrite of the Prerequisites section in the Merlin module README (`03-merlin/README.md`). Merlin is unique among the tools taught in this seminar in that it requires external infrastructure — a running Redis broker — before any examples can execute. The current Prerequisites section is eight lines and does not account for this requirement or for the two types of attendees who arrive at this module: those who have completed earlier sections (and already have the `wf-seminar` conda environment) and those who are starting here directly.

The rewrite introduces a two-path onboarding flow modeled on the pattern already established in the Maestro section: returning users verify their existing environment and skip ahead, while new users follow a standalone setup path; both paths converge at a shared Redis Setup subsection. That subsection walks the user through starting `redis-server` as a background process on the login node, writing a complete `~/.merlin/app.yaml` for a localhost Redis connection, and verifying connectivity with `merlin info`. A corresponding change to `environment.yml` adds the `redis-server` binary to the shared conda environment so the instructions work without requiring users to install anything beyond what the seminar environment already provides.

## Definition of Done
Rewrite the Prerequisites/Setup section in `03-merlin/README.md` so that:

1. Two user paths are handled clearly: (a) users with an existing `wf-seminar` conda environment from earlier sections, and (b) users jumping directly to this module.
2. Redis setup is explicit and step-by-step — `redis-server` installed via conda in `wf-seminar`, run on the login node for basic examples and inside Slurm allocations for Slurm-based examples.
3. `merlin config` and `~/.merlin/app.yaml` configuration for local Redis are covered.
4. Verification steps are included (`merlin --version`, `merlin info`, Redis connectivity).
5. The Maestro README's two-path pattern is followed as structural precedent.
6. Default account is `ntrain4`.

A new attendee can follow the Prerequisites section end-to-end and have Merlin + Redis running, ready for example1, without needing to consult any other document.

Out of scope: long-lived Redis deployments (SPIN, workflow QOS), changes to example spec files, other tutorial sections.

## Acceptance Criteria

### merlin-prereqs.AC1: Two user paths are clearly distinguished
- **merlin-prereqs.AC1.1 Success:** User with existing `wf-seminar` env can verify setup with `merlin --version` and skip to Redis Setup
- **merlin-prereqs.AC1.2 Success:** New user can follow standalone setup instructions to install Merlin and reach the same verification point
- **merlin-prereqs.AC1.3 Success:** Both paths converge at the Redis Setup subsection with no repeated or conflicting instructions

### merlin-prereqs.AC2: Redis setup is explicit and self-contained
- **merlin-prereqs.AC2.1 Success:** User can start `redis-server` on login node using a single copy-pasteable command
- **merlin-prereqs.AC2.2 Success:** `redis-server` binary is available after `conda activate wf-seminar` (via environment.yml)
- **merlin-prereqs.AC2.3 Success:** Instructions explain Redis runs as a background process and how to verify it is running
- **merlin-prereqs.AC2.4 Success:** Cleanup instructions show how to stop redis-server when done with tutorial

### merlin-prereqs.AC3: Merlin broker configuration is complete and correct
- **merlin-prereqs.AC3.1 Success:** `merlin config` step generates `~/.merlin/app.yaml`
- **merlin-prereqs.AC3.2 Success:** Complete `app.yaml` content for localhost Redis is shown (not "edit these fields")
- **merlin-prereqs.AC3.3 Failure:** User who skips `app.yaml` configuration gets a clear error from `merlin info` rather than silent failure

### merlin-prereqs.AC4: Verification steps confirm readiness
- **merlin-prereqs.AC4.1 Success:** `merlin --version` confirms Merlin package is installed (expected: 1.13.0)
- **merlin-prereqs.AC4.2 Success:** `merlin info` confirms broker connectivity after Redis setup
- **merlin-prereqs.AC4.3 Failure:** User whose Redis is not running gets a recognizable connection error from `merlin info`

### merlin-prereqs.AC5: Account and structural conventions followed
- **merlin-prereqs.AC5.1 Success:** Default account is `ntrain4` in all commands and examples
- **merlin-prereqs.AC5.2 Success:** Maestro's two-path structural pattern is followed (section headers, skip-ahead anchors, verification gates)
- **merlin-prereqs.AC5.3 Success:** Example READMEs reference section-level Prerequisites rather than standalone Redis guide

### merlin-prereqs.AC6: Attendee end-to-end success
- **merlin-prereqs.AC6.1 Success:** A new attendee following Prerequisites end-to-end has Merlin + Redis running and can proceed to example1 without consulting other documents
- **merlin-prereqs.AC6.2 Success:** A note at the end points to `merlin-redis-setup.md` for production Redis deployments

## Glossary

- **Merlin**: A Python workflow framework built on Maestro that adds distributed task execution via a message broker. Workers consume tasks from queues rather than executing them directly.
- **Redis / `redis-server`**: An in-memory data store used here as Merlin's message broker. `redis-server` is the server binary, installed via conda and started manually by the attendee.
- **`app.yaml` (`~/.merlin/app.yaml`)**: Merlin's broker configuration file. Tells Merlin where to find the message broker (host, port, protocol). `merlin config` generates a template with RabbitMQ defaults that must be replaced for Redis.
- **`merlin info`**: Merlin CLI command that tests connectivity to the configured broker. Used as the verification gate confirming Redis is running and reachable.
- **`wf-seminar`**: The shared conda environment used across all tutorial sections, defined in `environment.yml`.
- **`ntrain4`**: The Slurm account used by seminar attendees for job submissions.
- **SPIN**: NERSC's container service for persistent Redis deployments. Covered in existing `merlin-redis-setup.md`; explicitly out of scope for this tutorial-focused design.
- **Broker**: In Merlin's architecture, the service (here Redis) that holds the task queue. Workers connect to the broker to receive tasks; Merlin submits tasks to it.

## Architecture

The Merlin module Prerequisites section is a self-contained onboarding flow that handles two entry points (returning users and fresh users) and converges them at a single Redis setup section. Unlike Maestro, which only requires a Python package, Merlin requires external infrastructure (Redis) — so the Prerequisites section must cover both software installation and service setup.

**Document flow:**

```
Prerequisites
├── Path A: "If you completed earlier sections"
│   └── Verify merlin --version → skip to Redis Setup
├── Path B: "First time? Set up the environment"
│   └── Top-level README or standalone pip install → verify merlin --version
└── Redis Setup (both paths converge here)
    ├── Start redis-server (login node, background process)
    ├── Configure ~/.merlin/app.yaml for localhost
    ├── Verify with merlin info
    └── Cleanup instructions (kill redis-server when done)
```

**Key design decisions:**

1. **Inline tutorial Redis path.** The existing `merlin-redis-setup.md` covers SPIN and workflow QOS — production approaches irrelevant to a tutorial. The section README inlines the simple `redis-server` on localhost approach. A brief note at the end points to the existing guide for persistent deployments.

2. **Complete app.yaml content, not "edit these fields."** `merlin config` generates a template with RabbitMQ defaults. Rather than telling users to find and change specific fields, we show the complete localhost Redis config to write. This eliminates YAML editing errors.

3. **Login-node Redis for basic examples.** Redis runs as a background process on the login node for the initial setup and example1. Individual example READMEs document starting Redis inside Slurm allocations where appropriate.

4. **`redis-server` via conda.** The `redis-server` binary is added to `environment.yml` so it's available when users activate `wf-seminar`. Currently only the Python `redis` client library is included.

## Existing Patterns

The Maestro section README (`02-maestro/README.md`, lines 41-65) establishes the two-path Prerequisites pattern used across this tutorial:

- **"If you completed earlier sections"** — short verification block (`module load python`, `conda activate wf-seminar`, tool-specific version check), with explicit "skip ahead to [section]" if successful
- **"First time? Set up the environment"** — reference to top-level README setup instructions, then return to same verification command

The signac section (`01-signac/README.md`) uses a simpler single-path approach (just `module load python` + `conda activate wf-seminar`). The Maestro pattern is the better precedent because Merlin has even more setup complexity.

**New pattern introduced:** Redis Setup as a separate subsection after the two-path convergence. This is unique to Merlin — no other section needs external infrastructure. This subsection is structured as a linear sequence (start server, configure, verify, cleanup) rather than branching paths.

## Implementation Phases

<!-- START_PHASE_1 -->
### Phase 1: Add redis-server to conda environment
**Goal:** Make `redis-server` binary available in the `wf-seminar` conda environment.

**Components:**
- `environment.yml` — add `redis-server` package (conda-forge channel)

**Dependencies:** None

**Done when:** `conda activate wf-seminar && which redis-server` returns a path. Note: per CLAUDE.md, environment.yml changes must be tested on Perlmutter before merging.
<!-- END_PHASE_1 -->

<!-- START_PHASE_2 -->
### Phase 2: Rewrite Prerequisites section in 03-merlin/README.md
**Goal:** Replace the current 8-line Prerequisites section (lines 38-45) with a complete onboarding flow covering two user paths, Redis setup, Merlin configuration, and verification.

**Components:**
- `03-merlin/README.md` — replace the `## Prerequisites` section with:
  - **"If you completed earlier sections"** subsection — activate env, `merlin --version`, skip-ahead anchor
  - **"First time? Set up the environment"** subsection — reference top-level README, standalone pip alternative, `merlin --version` verification
  - **"Redis Setup"** subsection — start `redis-server` on login node, configure `~/.merlin/app.yaml` with complete localhost config, `merlin info` verification
  - **"Cleanup"** subsection — how to stop redis-server when done with tutorial

**Dependencies:** Phase 1 (redis-server must be in env for instructions to work)

**Done when:**
- Two user paths are clearly distinguished with appropriate skip-ahead anchors
- Redis setup is step-by-step with copy-pasteable commands
- Complete `app.yaml` content is shown (not "edit these fields")
- Verification commands (`merlin --version`, `merlin info`) are included with expected output
- Default account is `ntrain4`
- A new attendee can follow the section end-to-end without consulting other documents
<!-- END_PHASE_2 -->

<!-- START_PHASE_3 -->
### Phase 3: Update example READMEs for consistency
**Goal:** Align example-level prerequisites with the new section-level setup, and add allocation-specific Redis instructions where needed.

**Components:**
- `03-merlin/example1-distributed/README.md` — update Prerequisites to reference section-level setup instead of standalone Redis guide
- `03-merlin/example2-fault-tolerance/README.md` — same update; add note about running Redis inside Slurm allocation if applicable
- `03-merlin/example3-massive-scale/README.md` — same update
- All three: update `salloc` commands to use `--account=ntrain4`

**Dependencies:** Phase 2 (section README must be complete before aligning examples)

**Done when:** Example READMEs reference the section Prerequisites for setup, use `ntrain4` as default account, and include allocation-specific Redis instructions where the example uses Slurm.
<!-- END_PHASE_3 -->

## Additional Considerations

**Password-free Redis for tutorial.** The tutorial Redis runs on localhost without authentication. This is appropriate for a short-lived tutorial process but should not be presented as production practice. A brief note after the Redis setup section points users to `resources/installation-guides/merlin-redis-setup.md` for production deployments with authentication.

**Login node etiquette.** The README should include a reminder to stop `redis-server` after the tutorial, since login nodes are shared resources. The Cleanup subsection covers this.

**Existing redis-setup guide unchanged.** The `resources/installation-guides/merlin-redis-setup.md` remains as-is for users who want persistent SPIN or allocation-based deployments. The section README complements it rather than replacing it.
