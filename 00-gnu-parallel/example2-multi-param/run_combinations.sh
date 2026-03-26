#!/bin/bash
# Example 2: Multiple Parameter Combinations with GNU Parallel
# Demonstrates Cartesian product parameter exploration

# GNU Parallel is available by default on Perlmutter (no module load needed)

# Make process_combination.sh executable
chmod +x process_combination.sh

# Use all available cores in Slurm job, or default to 2 for login node safety
NJOBS=${SLURM_CPUS_ON_NODE:-2}

echo "Running 18 parameter combinations (3 algorithms × 3 sizes × 2 opts) with $NJOBS parallel jobs..."
echo "(Automatically detects Slurm allocation or defaults to 2 for login nodes)"
echo ""

# Parameter dimensions:
# - Algorithms: A, B, C
# - Dataset sizes: small, medium, large
# - Optimization levels: O2, O3
# Total: 3 × 3 × 2 = 18 combinations

# Run all combinations in parallel
# {1} = algorithm, {2} = size, {3} = optimization
parallel -j $NJOBS './process_combination.sh {1} {2} {3}' \
  ::: A B C \
  ::: small medium large \
  ::: O2 O3

echo ""
echo "All combinations complete!"
echo ""
echo "Analysis:"
echo "- Total combinations: 18"
echo "- If each task takes 2 seconds:"
echo "  - Sequential: 36 seconds"
echo "  - Parallel ($NJOBS jobs): ~$((18 * 2 / NJOBS)) seconds (ceiling(18/$NJOBS) batches × 2 seconds)"
echo "  - Parallel (128 jobs on Perlmutter): ~2 seconds"
echo "    (all 18 tasks run simultaneously, limited by single-task duration)"
echo "    Note: 110 of 128 cores would sit idle - this example is too small for a full node!"
