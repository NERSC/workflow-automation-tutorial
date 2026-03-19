#!/bin/bash
# Example 2: Multiple Parameter Combinations with GNU Parallel
# Demonstrates Cartesian product parameter exploration

# Load GNU Parallel (on Perlmutter)
# Uncomment if running on compute node:
# module load parallel

# Make process_combination.sh executable
chmod +x process_combination.sh

echo "Running 18 parameter combinations (3 algorithms × 3 sizes × 2 opts)..."
echo "(Using -j 2 for login node safety)"
echo ""

# Parameter dimensions:
# - Algorithms: A, B, C
# - Dataset sizes: small, medium, large
# - Optimization levels: O2, O3
# Total: 3 × 3 × 2 = 18 combinations

# Run all combinations in parallel
# {1} = algorithm, {2} = size, {3} = optimization
parallel -j 2 './process_combination.sh {1} {2} {3}' \
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
echo "  - Parallel (2 jobs): ~18 seconds"
echo "  - Parallel (128 jobs on Perlmutter): <1 second"
