# Maestro Perlmutter Slurm Fix Design

## Summary

This design document describes a targeted fix to make `example3-slurm-config` actually submittable on Perlmutter without upgrading the maestrowf package. The approach uses two changes to `workflow.yaml`: adding a native `qos: debug` field to the batch block, and embedding `#SBATCH --constraint=cpu` directly in the compute step's `cmd` block as a workaround for the absence of a native constraint field in the Slurm adapter. Deliverables are an updated `workflow.yaml`, a revised `README.md` documenting the constraint workaround and troubleshooting guidance, and a human test plan covering all three examples including actual Slurm submission of example3.

## Definition of Done

1. **example3-slurm-config runs successfully** on Perlmutter debug QOS by adding `qos: debug` to the batch block and `#SBATCH --constraint=cpu` in the compute step cmd
2. **example3-slurm-config README** documents the constraint workaround, correct debug QOS limits, and Perlmutter-specific requirements
3. **Examples 1 and 2 continue to work unchanged** (no regression)
4. **Human test plan** covers running all three examples, including actual Slurm submission of example3

## Acceptance Criteria

### maestro-120-upgrade.AC1: example3-slurm-config runs on Perlmutter debug QOS
- **maestro-120-upgrade.AC1.1 Success:** `maestro run --dry --autoyes workflow.yaml` generates a Slurm script containing `#SBATCH --qos=debug`
- **maestro-120-upgrade.AC1.2 Success:** Generated Slurm script contains `#SBATCH --constraint=cpu` (from embedded cmd directive)
- **maestro-120-upgrade.AC1.3 Success:** `sbatch --test-only` accepts the generated script without "does not match any supported policy" error
- **maestro-120-upgrade.AC1.4 Success:** `bank` field is set to `ntrain4` (training account)
- **maestro-120-upgrade.AC1.5 Failure:** Omitting `#SBATCH --constraint=cpu` from the compute step cmd causes Slurm rejection on Perlmutter

### maestro-120-upgrade.AC2: README documents configuration and workaround
- **maestro-120-upgrade.AC2.1 Success:** README batch block snippets include `qos: debug` field
- **maestro-120-upgrade.AC2.2 Success:** README explains the `#SBATCH --constraint=cpu` workaround and why it's needed on Perlmutter
- **maestro-120-upgrade.AC2.3 Success:** README troubleshooting section includes "Job request does not match any supported policy" error with resolution steps
- **maestro-120-upgrade.AC2.4 Success:** All code snippets in README match the actual workflow.yaml content

### maestro-120-upgrade.AC3: Examples 1 and 2 unchanged
- **maestro-120-upgrade.AC3.1 Success:** example1-simple-dag workflow.yaml has zero diff from current committed version
- **maestro-120-upgrade.AC3.2 Success:** example2-param-sweeps workflow.yaml has zero diff from current committed version
- **maestro-120-upgrade.AC3.3 Success:** `maestro run --dry --autoyes workflow.yaml` succeeds for both examples 1 and 2

### maestro-120-upgrade.AC4: Human test plan
- **maestro-120-upgrade.AC4.1 Success:** Test plan includes dry-run verification for all three examples
- **maestro-120-upgrade.AC4.2 Success:** Test plan includes actual Slurm submission of example3 on Perlmutter debug QOS
- **maestro-120-upgrade.AC4.3 Success:** Test plan verifies generated Slurm scripts contain expected directives
- **maestro-120-upgrade.AC4.4 Success:** All test plan steps completable within 30 minutes total

## Glossary

- **maestrowf**: The Python library that implements the Maestro workflow specification tool; versions 1.1.11 and 1.2.0 are referenced in this document.
- **Slurm adapter**: The maestrowf component (`slurmscriptadapter.py`) that translates the `batch` block in `workflow.yaml` into `#SBATCH` directives in a generated job script.
- **batch block**: The YAML section in a Maestro `workflow.yaml` that specifies scheduler-level job parameters (nodes, walltime, bank, qos, etc.).
- **`#SBATCH` directive embedding**: The workaround of placing `#SBATCH` lines at the top of a step's `cmd` block so they are parsed by Slurm as job directives, used when the adapter has no native field for a given Slurm option.
- **`--constraint=cpu`**: A Perlmutter-specific mandatory Slurm flag that selects CPU nodes; omitting it causes "Job request does not match any supported policy."
- **debug QOS**: A Slurm Quality of Service tier on Perlmutter with a 30-minute walltime limit, used for interactive testing and tutorial exercises.
- **`allocation_args`**: A maestrowf batch parameter that exists only in the Flux adapter, not the Slurm adapter — the original (incorrect) motivation for investigating a 1.2.0 upgrade.
- **`ntrain4`**: The Slurm account used in NERSC training events.

## Architecture

This is a targeted fix to make the existing example3-slurm-config actually submittable on Perlmutter, using capabilities already present in maestrowf 1.1.11.

### Investigation findings

Initial hypothesis was that upgrading maestrowf to 1.2.0 would enable `allocation_args` for passing `--constraint=cpu` and `--qos=debug` to Slurm. Investigation of the 1.2.0 source code revealed:

- `allocation_args` exists **only in the Flux adapter**, not the Slurm adapter
- The Slurm adapter already supports `qos` as a native batch block parameter in 1.1.11
- No native `constraint` field exists in either version

Conclusion: no version upgrade needed. The fix uses existing 1.1.11 capabilities plus a documented workaround for `--constraint`.

### Approach

Two changes to `workflow.yaml`:

1. **Add `qos: debug`** to the `batch` block. The Slurm adapter reads this and generates `#SBATCH --qos=debug`. This is a native, supported feature.

2. **Embed `#SBATCH --constraint=cpu`** as the first line of the compute step's `cmd` block. Maestro inserts a blank line between the generated `#SBATCH` header and the cmd content. Slurm continues parsing `#SBATCH` directives through blank lines (only stops at the first non-comment, non-whitespace line). Verified via `sbatch --test-only` on Perlmutter.

### Why not upgrade to 1.2.0

- The feature that motivated the upgrade (`allocation_args`) is Flux-only
- 1.1.11 already has native `qos` support in the Slurm adapter
- No other 1.2.0 features are needed for this tutorial
- Avoiding an environment rebuild reduces risk and testing burden

## Existing Patterns

The `#SBATCH` embedding workaround follows patterns documented in maestrowf GitHub issues (#340, #436) where users inject custom SBATCH directives directly in the `cmd` block when the Slurm adapter lacks native support.

The `qos` field in the batch block follows the existing `reservation` pattern — both are Slurm-specific fields recognized by the adapter's `__init__` method (`slurmscriptadapter.py:76`).

## Implementation Phases

<!-- START_PHASE_1 -->
### Phase 1: Fix workflow.yaml for Perlmutter submission

**Goal:** Make example3 workflow submittable on Perlmutter debug QOS

**Components:**
- `02-maestro/example3-slurm-config/workflow.yaml` — add `qos: debug` to batch block, add `#SBATCH --constraint=cpu` to compute step cmd, update `bank` to `ntrain4`

**Dependencies:** None

**Done when:** `maestro run --dry --autoyes workflow.yaml` generates a Slurm script with `#SBATCH --qos=debug` and `#SBATCH --constraint=cpu` directives
<!-- END_PHASE_1 -->

<!-- START_PHASE_2 -->
### Phase 2: Update README documentation

**Goal:** Document the Perlmutter-specific configuration and constraint workaround

**Components:**
- `02-maestro/example3-slurm-config/README.md` — update Perlmutter Configuration section with `qos` field and constraint workaround, fix example batch block snippets, update exercises, add troubleshooting for "Job request does not match any supported policy" error

**Dependencies:** Phase 1 (workflow changes inform documentation)

**Done when:** README accurately describes the workflow.yaml configuration including the constraint workaround, and all code snippets match the actual workflow
<!-- END_PHASE_2 -->

## Additional Considerations

**Perlmutter constraint requirement:** `--constraint=cpu` (or `gpu`) is mandatory on Perlmutter. Omitting it produces `"Job request does not match any supported policy"`. This is a Perlmutter-specific policy, not a Slurm default. The README should call this out explicitly.

**Debug QOS is the default:** On Perlmutter, `debug` is the default QOS. Specifying it explicitly in the workflow makes the example self-documenting and avoids confusion if the default changes.

**The `$(PROCS)` token issue:** The current workflow uses `--procs $(PROCS)` in the compute step cmd, but `$(PROCS)` is not resolved by Maestro in the cmd block (only in the `srun` command generated by `$(LAUNCHER)`). This is a pre-existing issue, not introduced by this change. The compute.py script handles it gracefully by accepting the literal string.
