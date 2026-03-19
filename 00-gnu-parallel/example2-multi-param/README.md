# Example 2: Multiple Parameter Combinations

**Concept:** Exploring parameter spaces with Cartesian products

**Duration:** 5 minutes

## What This Demonstrates

- Multiple parameter sources with `::: A B C ::: 1 2 3`
- Generating all combinations (Cartesian product)
- Parameter substitution with `{1}`, `{2}`, `{3}` for positional access
- Systematic parameter space exploration

## The Problem

You need to run experiments across multiple parameter dimensions:
- 3 algorithms: A, B, C
- 3 dataset sizes: small, medium, large
- 2 optimization levels: O2, O3

That's 3 × 3 × 2 = 18 combinations. Writing nested loops is tedious and error-prone.

## The Solution

GNU Parallel generates all combinations automatically:

```bash
parallel ./process_combination.sh {1} {2} {3} \
  ::: A B C \
  ::: small medium large \
  ::: O2 O3
```

## Files in This Example

- `run_combinations.sh` - Main script demonstrating parameter combinations
- `process_combination.sh` - Placeholder task processing each combination

## How to Run

**On Perlmutter (login node - quick test):**

```bash
cd example2-multi-param
bash run_combinations.sh
```

**Expected Output:**

```
Running 18 parameter combinations (3 algorithms × 3 sizes × 2 opts)...
Processing: algorithm=A, size=small, opt=O2
Processing: algorithm=A, size=small, opt=O3
Processing: algorithm=A, size=medium, opt=O2
...
Processing: algorithm=C, size=large, opt=O3
All combinations complete!
```

## Key Concepts

1. **Multiple sources:** Each `:::` introduces a new parameter dimension
2. **Cartesian product:** All possible combinations are generated
3. **Positional parameters:** `{1}` = first source, `{2}` = second source, `{3}` = third source
4. **Scalability:** 3×3×2=18 combinations run in parallel (limited by `-j` flag)

## Parameter Combinations Explained

```bash
parallel echo {1} {2} {3} ::: A B ::: 1 2 ::: X Y
```

Generates:
```
A 1 X
A 1 Y
A 2 X
A 2 Y
B 1 X
B 1 Y
B 2 X
B 2 Y
```

Total: 2 × 2 × 2 = 8 combinations

## Linked vs Unlinked Parameters

**Unlinked (Cartesian product) - use `:::`:**
```bash
parallel echo {1} {2} ::: A B ::: 1 2
# A 1, A 2, B 1, B 2 (4 combinations)
```

**Linked (pairwise) - use `:::+`:**
```bash
parallel echo {1} {2} ::: A B :::+ 1 2
# A 1, B 2 (2 combinations, maintains alignment)
```

This example uses unlinked parameters (full Cartesian product).

## Real-World Use Case

```bash
# Parameter sweep for ML hyperparameter tuning
parallel python train_model.py \
  --lr {1} \
  --batch-size {2} \
  --optimizer {3} \
  ::: 0.001 0.01 0.1 \
  ::: 16 32 64 \
  ::: adam sgd rmsprop
# Total: 3 × 3 × 3 = 27 training runs
```

## Progression

- **Example 1:** Single parameter dimension
- **Example 2:** Multiple parameter dimensions (this example)
- **Example 3:** Batch integration with Slurm
- **Signac (next section):** Persistent parameter space tracking across runs
