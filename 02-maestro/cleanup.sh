#!/bin/bash
# cleanup.sh - Remove runtime artifacts from 02-maestro examples
#
# Restores the directory to its freshly-cloned state by removing files
# and directories generated when the Maestro examples are run:
#   example1-simple-dag/simple-dag_<timestamp>/    (study output + logs + step dirs)
#   example2-param-sweeps/param-sweep_<timestamp>/ (study output + parameterized steps)
#   example3-slurm-config/slurm-config_<timestamp>/ (study output + Slurm step dirs)
#   **/__pycache__/                                (Python bytecode caches)

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

rm -rf "$SCRIPT_DIR/example1-simple-dag/simple-dag_"*
rm -rf "$SCRIPT_DIR/example2-param-sweeps/param-sweep_"*
rm -rf "$SCRIPT_DIR/example3-slurm-config/slurm-config_"*

# Python bytecode caches (created in scripts/ subdirectories)
find "$SCRIPT_DIR" -name '__pycache__' -type d -exec rm -rf {} +

echo "02-maestro cleaned."
