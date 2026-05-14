#!/bin/bash
# cleanup.sh - Remove runtime artifacts from 01-signac examples
#
# Restores the directory to its freshly-cloned state by removing files
# and directories generated when the signac examples are run:
#   example1-parameter-space/.signac/          (signac project config)
#   example1-parameter-space/signac_project_document.json
#   example1-parameter-space/workspace/        (signac job directories + results)
#   example2-job-submission/workspace/         (empty workspace directory)
#   **/__pycache__/                            (Python bytecode caches)

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

rm -rf "$SCRIPT_DIR/example1-parameter-space/.signac"
rm -f  "$SCRIPT_DIR/example1-parameter-space/signac_project_document.json"
rm -rf "$SCRIPT_DIR/example1-parameter-space/workspace"
rm -rf "$SCRIPT_DIR/example2-job-submission/workspace"

# Python bytecode caches (created in multiple subdirectories)
find "$SCRIPT_DIR" -name '__pycache__' -type d -exec rm -rf {} +

echo "01-signac cleaned."
