#!/bin/bash
# cleanup.sh - Remove runtime artifacts from 03-merlin examples
#
# Restores the directory to its freshly-cloned state by removing files
# and directories generated when the Merlin examples are run:
#   output/example1-distributed_<timestamp>/   (Merlin study workspace for example 1)
#   output/fault-tolerance-demo_<timestamp>/   (Merlin study workspace for example 2)
#   output/massive-scale_<timestamp>/          (Merlin study workspace for example 3)
#   $PSCRATCH/wf-seminar-merlin/example1-distributed_<timestamp>/  (scratch workspace)
#   $PSCRATCH/wf-seminar-merlin/fault-tolerance-demo_<timestamp>/  (scratch workspace)
#   $PSCRATCH/wf-seminar-merlin/massive-scale_<timestamp>/         (scratch workspace)
#   **/__pycache__/                            (Python bytecode caches)
#
# The $PSCRATCH block only runs when $PSCRATCH is set and non-empty.
# $PSCRATCH is a NERSC-specific variable pointing to the user's scratch filesystem;
# it is absent in non-Perlmutter environments.

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

rm -rf "$SCRIPT_DIR/output/example1-distributed_"*
rm -rf "$SCRIPT_DIR/output/fault-tolerance-demo_"*
rm -rf "$SCRIPT_DIR/output/massive-scale_"*

# Remove scratch workspaces on Perlmutter (OUTPUT_PATH in examples 1, 2, and 3 spec.yaml)
if [ -n "${PSCRATCH:-}" ]; then
    rm -rf "$PSCRATCH/wf-seminar-merlin/example1-distributed_"*
    rm -rf "$PSCRATCH/wf-seminar-merlin/fault-tolerance-demo_"*
    rm -rf "$PSCRATCH/wf-seminar-merlin/massive-scale_"*
fi

# Python bytecode caches
find "$SCRIPT_DIR" -name '__pycache__' -type d -exec rm -rf {} +

echo "03-merlin cleaned."
