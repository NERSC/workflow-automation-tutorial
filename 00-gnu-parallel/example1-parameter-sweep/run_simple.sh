#!/bin/bash
# Example 1: Simple Parameter Sweep with GNU Parallel
# Demonstrates basic parallelization on a single node

# GNU Parallel is available by default on Perlmutter (no module load needed)

# Make process_task.sh executable
chmod +x process_task.sh

# Use all available cores in Slurm job, or default to 2 for login node safety
NJOBS=${SLURM_CPUS_ON_NODE:-2}

echo "Running 20 tasks with $NJOBS parallel jobs..."
echo "(Automatically detects Slurm allocation or defaults to 2 for login nodes)"
echo ""

# Time the execution
start_time=$(date +%s)

# Run 20 tasks in parallel
seq 1 20 | parallel -j $NJOBS './process_task.sh {}'

end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo ""
echo "All tasks complete!"
echo "Elapsed time: ${elapsed} seconds"
echo ""
echo "Analysis:"
echo "- Sequential execution: ~40 seconds (20 tasks × 2 seconds)"
echo "- Parallel execution ($NJOBS jobs): ~${elapsed} seconds (ceiling(20/$NJOBS) batches × 2 seconds)"
echo "- Parallel execution (128 jobs on Perlmutter): ~2 seconds"
echo "  (all 20 tasks run simultaneously, limited by single-task duration)"
echo "  Note: 108 of 128 cores would sit idle - this example is too small for a full node!"
