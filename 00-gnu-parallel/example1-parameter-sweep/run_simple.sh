#!/bin/bash
# Example 1: Simple Parameter Sweep with GNU Parallel
# Demonstrates basic parallelization on a single node

# IMPORTANT: Load GNU Parallel module if running on compute node
# On Perlmutter compute nodes, you MUST uncomment this line:
# module load parallel
# (Not needed on login nodes where parallel may already be available)

# Make process_task.sh executable
chmod +x process_task.sh

echo "Running 20 tasks with 2 parallel jobs..."
echo "(Using -j 2 for login node safety; use -j \$SLURM_CPUS_ON_NODE on compute nodes)"
echo ""

# Time the execution
start_time=$(date +%s)

# Run 20 tasks in parallel with job limit of 2
# On compute node, replace '-j 2' with '-j $SLURM_CPUS_ON_NODE'
seq 1 20 | parallel -j 2 './process_task.sh {}'

end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo ""
echo "All tasks complete!"
echo "Elapsed time: ${elapsed} seconds"
echo ""
echo "Analysis:"
echo "- Sequential execution: ~40 seconds (20 tasks × 2 seconds)"
echo "- Parallel execution (2 jobs): ~${elapsed} seconds"
echo "- Parallel execution (128 jobs on Perlmutter): <1 second"
