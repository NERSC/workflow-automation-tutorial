#!/usr/bin/env bash
# inspect_workspace.sh - Inspect a signac workspace using CLI tools
#
# Usage: bash inspect_workspace.sh
# Prerequisite: Run python init_project.py first to create the workspace
#
# This script demonstrates signac's built-in command-line tools for
# navigating the workspace without writing Python code.

set -e

if [ ! -d .signac ]; then
    echo "Error: Run this script from the example1-parameter-space directory." >&2
    exit 1
fi

echo "=== 1. Project Parameter Schema ==="
echo "signac schema shows every parameter key and the range of values across all jobs."
echo ""
echo '$ signac schema'
signac schema
echo ""

echo "=== 2. Find Jobs by Parameter Value ==="
echo "signac find filters jobs by parameter values and prints matching job IDs."
echo ""
echo '$ signac find temperature 300'
signac find temperature 300
echo ""

echo "=== 3. Look Up Directory for a Specific Parameter Set ==="
echo "signac job takes a full statepoint as JSON and prints the job ID."
echo "The workspace directory is workspace/<job_id>/."
echo ""
echo '$ signac job '\''{"temperature": 300, "pressure": 1.0}'\'''
JOB_ID=$(signac job '{"temperature": 300, "pressure": 1.0}')
echo "$JOB_ID"
echo ""
echo "Workspace directory: workspace/$JOB_ID/"
echo ""

echo "=== 4. Read the Raw Statepoint File ==="
echo "Each job directory contains signac_statepoint.json -- plain JSON, no special tools required."
echo ""
echo "$ cat workspace/$JOB_ID/signac_statepoint.json"
cat "workspace/$JOB_ID/signac_statepoint.json"
echo ""
