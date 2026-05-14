#!/bin/bash
# cleanup.sh - Remove runtime artifacts from 00-gnu-parallel examples
#
# Restores the directory to its freshly-cloned state by removing files
# generated when example3-slurm-integration is run:
#   example3-slurm-integration/parallel_job.log  (GNU Parallel --joblog)
#   example3-slurm-integration/slurm-*.out       (Slurm batch output)

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

rm -f "$SCRIPT_DIR/example3-slurm-integration/parallel_job.log"
rm -f "$SCRIPT_DIR/example3-slurm-integration/slurm-"*.out

echo "00-gnu-parallel cleaned."
