# AiiDA Environment Dependencies Design

## Summary

The design resolves two runtime failures in the `wf-seminar` conda environment that prevent the AiiDA section from functioning on Perlmutter. First, `aiida-workgraph==0.3.16` declares an unbounded dependency on `node-graph>=0.0.12`; pip resolves this to a newer release that broke the package's internal API, so the fix pins `node-graph==0.0.12` in both `environment.yml` and `requirements.txt`. Second, the `graphviz` Python wrapper already present in the environment requires the Graphviz binary suite (`dot`, etc.) to render provenance graphs, but neither the environment spec nor any Perlmutter Lmod module provides it; the fix adds the conda `graphviz` package, which ships the binary suite. Both fixes are config-file-only with no changes to application code, and a documentation pass in Phase 2 updates the example 3 README and the `04-aiida/CLAUDE.md` to reflect the corrected environment state. Four files are changed in total: `environment.yml`, `requirements.txt`, `04-aiida/example3-data-graph/README.md`, and `04-aiida/CLAUDE.md`.

## Definition of Done

The `wf-seminar` conda environment, when created from `environment.yml` (or installed from `requirements.txt`), installs `node-graph==0.0.12` so that `aiida_workgraph==0.3.16` imports successfully. The environment also installs the Graphviz binary suite so that `verdi node graph generate` can render graphs. Example 3's README correctly describes how to get the `graphviz` binary. The `04-aiida/CLAUDE.md` documents the `node-graph` pin constraint so future maintainers understand why it exists.

Out of scope: upgrading `aiida-workgraph` or `aiida-core`, changes to other sections.

## Acceptance Criteria

### aiida-env-deps.AC1: aiida-workgraph imports successfully in the wf-seminar environment
- **aiida-env-deps.AC1.1 Success:** `from aiida_workgraph import task, WorkGraph` completes without error
- **aiida-env-deps.AC1.2 Success:** `pip show node-graph` in the environment reports `Version: 0.0.12`
- **aiida-env-deps.AC1.3 Success:** `@task.calcfunction` and `@task.graph_builder` decorators are importable and callable
- **aiida-env-deps.AC1.4 Failure:** A fresh pip install of `aiida-workgraph==0.3.16` without the pin resolves `node-graph` to a version ≥0.1.0 and fails to import (documents why the pin is necessary)

### aiida-env-deps.AC2: Graphviz binary suite is available in the wf-seminar environment
- **aiida-env-deps.AC2.1 Success:** `dot -V` exits 0 inside the conda environment
- **aiida-env-deps.AC2.2 Success:** `verdi node graph generate <PK>` (after running example 1) produces a `.dot.pdf` file without error

### aiida-env-deps.AC3: Example 3 README correctly describes graphviz setup
- **aiida-env-deps.AC3.1 Success:** README no longer contains the string `module load graphviz`
- **aiida-env-deps.AC3.2 Success:** README states graphviz is included in the `wf-seminar` conda environment
- **aiida-env-deps.AC3.3 Success:** README provides `conda install graphviz -c conda-forge` as the manual fallback

### aiida-env-deps.AC4: 04-aiida/CLAUDE.md documents the node-graph pin constraint
- **aiida-env-deps.AC4.1 Success:** Gotchas section contains a bullet referencing `node-graph==0.0.12`
- **aiida-env-deps.AC4.2 Success:** The bullet explains the incompatibility reason (API rename: `NodeSocket` → `TaskSocket`)

## Glossary

- **node-graph**: A Python library that provides the graph data structures used internally by `aiida-workgraph`. Version `0.0.12` is the release co-shipped with `aiida-workgraph==0.3.16`; later releases (>=0.1.0) renamed key classes, breaking backward compatibility.
- **aiida-workgraph**: An AiiDA plugin (version 0.3.16 in this project) that lets users define workflows as graphs of tasks using Python decorators such as `@task.calcfunction` and `@task.graph_builder`.
- **aiida-core**: The base AiiDA framework package that provides the provenance database, the `verdi` CLI, and the runner infrastructure on which plugins like `aiida-workgraph` depend.
- **verdi**: The command-line interface for AiiDA (installed as part of `aiida-core`). Used to manage profiles, inspect nodes, and render provenance graphs (e.g., `verdi node graph generate`).
- **WorkGraph**: The top-level object in `aiida-workgraph` that represents a workflow as a directed graph of tasks; imported as `from aiida_workgraph import WorkGraph`.
- **dot (binary)**: The primary command-line renderer in the Graphviz binary suite. It reads `.dot` graph description files and produces rendered output (PDF, PNG, SVG, etc.). Required by `verdi node graph generate` at runtime.
- **graphviz (conda vs pip)**: Two distinct installable components share the name "graphviz." The pip package (`graphviz` 0.21) is a pure-Python binding that generates `.dot` syntax but cannot render graphs by itself. The conda package `graphviz` (from `conda-forge`) ships the compiled binary suite including the `dot` executable. Both are needed: the pip package is pulled in transitively by `aiida-core`; the conda package must be added explicitly.
- **wf-seminar**: The name of the project's conda environment (defined in `environment.yml`) used for all five seminar sections. Attendees create it once and it must satisfy the dependency requirements of GNU Parallel, signac, Maestro, Merlin, and AiiDA together.
- **NodeSocket**: The name used in `node-graph==0.0.12` for the class representing a data socket on a graph node. In `node-graph>=0.1.0` this class was renamed to `TaskSocket`, making the older `aiida-workgraph==0.3.16` fail to import.
- **TaskSocket**: The renamed successor to `NodeSocket` introduced in `node-graph>=0.1.0`. Because `aiida-workgraph==0.3.16` still references `NodeSocket`, it is incompatible with any `node-graph` release that completed this rename.
- **conda dependencies**: The list of packages in `environment.yml` under the top-level `dependencies:` key that conda resolves and installs from its channel repositories (e.g., `conda-forge`). Binary tools like `redis` and `graphviz` are listed here.
- **pip subsection**: The nested `- pip:` list inside `environment.yml`'s `dependencies:` block. Packages listed here are installed by pip after conda finishes, and are used for packages not available in conda channels or where a specific version pin is needed (e.g., `aiida-workgraph==0.3.16`, `node-graph==0.0.12`).
- **environment.yml**: The conda environment specification file at the project root. Running `conda env create -f environment.yml` reproduces the full `wf-seminar` environment including both conda and pip packages.
- **requirements.txt**: A pip-only alternative to `environment.yml` for users who prefer a plain virtual environment. It must be kept in sync with the pip subsection of `environment.yml` for the same packages and version pins.

## Architecture

Two runtime bugs in the `wf-seminar` environment spec, fixed by targeted edits to four files:

**`node-graph` pin** — `aiida-workgraph==0.3.16` declares `node-graph>=0.0.12` with no upper bound. Pip resolves this to the latest release (currently `0.6.5`), which renamed `NodeSocket` to `TaskSocket` and restructured `utils`, breaking the import entirely. The fix is to pin `node-graph==0.0.12` — the version co-released with `aiida-workgraph==0.3.16` on August 10, 2024, verified working by direct testing on Perlmutter.

**Graphviz binary** — The `graphviz` Python package (0.21) is already installed as a transitive dependency of `aiida-core`, but it is a pure-Python wrapper that requires the Graphviz binary suite (`dot`, `neato`, etc.) to render graphs. The binary suite is not in the conda environment; there is no `graphviz` Lmod module on Perlmutter. Adding the conda `graphviz` package installs the binary suite alongside the existing Python bindings.

Both fixes are config-file-only. No application code changes.

## Existing Patterns

The project already pins transitive dependencies for reproducibility in `requirements.txt` (signac's `filelock`, `packaging`, `synced-collections`, `tqdm`; Merlin's `celery`, `redis`; AiiDA's `psycopg2-binary`, `pyyaml`). This design follows that same pattern for `node-graph==0.0.12`.

`environment.yml` already provides both a conda binary (`redis`) and a corresponding pip Python package (`redis>=6.0,<7.0`), establishing the precedent for complementary conda/pip entries. Adding conda `graphviz` (binary) alongside the pip-installed `graphviz` Python package (already present via `aiida-core`) follows this same pattern.

## Implementation Phases

<!-- START_PHASE_1 -->
### Phase 1: Pin dependencies in environment spec files

**Goal:** Ensure a fresh conda environment install resolves to `node-graph==0.0.12` and includes the Graphviz binary suite.

**Components:**
- `environment.yml` — add `graphviz` to conda `dependencies:` block (after `redis`, before the pip subsection); add `node-graph==0.0.12` to pip subsection (after `aiida-workgraph==0.3.16`) with inline comment explaining the pin
- `requirements.txt` — add `node-graph==0.0.12` after `aiida-workgraph==0.3.16` with inline comment

**Dependencies:** None (first phase)

**Done when:**
- `conda run -n wf-seminar python -c "from aiida_workgraph import task, WorkGraph"` exits 0
- `conda run -n wf-seminar dot -V` exits 0
- `conda run -n wf-seminar pip show node-graph` reports `Version: 0.0.12`
<!-- END_PHASE_1 -->

<!-- START_PHASE_2 -->
### Phase 2: Update documentation to match environment state

**Goal:** Ensure example 3's prerequisites and the section CLAUDE.md accurately describe the `graphviz` and `node-graph` requirements.

**Components:**
- `04-aiida/example3-data-graph/README.md` — replace the Prerequisites bullet that says `module load graphviz on Perlmutter, or conda install graphviz` with text stating graphviz is included in the `wf-seminar` environment, with a manual fallback (`conda install graphviz -c conda-forge`)
- `04-aiida/CLAUDE.md` — add a Gotchas bullet: `node-graph` must be pinned to `==0.0.12`; `aiida-workgraph==0.3.16` is incompatible with `node-graph>=0.1.0` (API rename: `NodeSocket` → `TaskSocket`). Pinned in both `environment.yml` and `requirements.txt`.

**Dependencies:** Phase 1 (documentation describes the state established in Phase 1)

**Done when:**
- `04-aiida/example3-data-graph/README.md` contains no reference to `module load graphviz`
- `04-aiida/CLAUDE.md` Gotchas section contains a bullet referencing `node-graph==0.0.12`
<!-- END_PHASE_2 -->
