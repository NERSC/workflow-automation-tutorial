#!/usr/bin/env python3
"""Generate hyperparameter samples for massive-scale sweep."""

import numpy as np
import sys

def main():
    output_file = sys.argv[1]
    n_samples = int(sys.argv[2])

    # Generate combinations
    lr = np.random.uniform(0.0001, 0.01, n_samples)
    batch_size = np.random.choice([16, 32, 64, 128, 256], n_samples)
    epochs = np.random.randint(10, 100, n_samples)

    # Save as 2D array (n_samples, n_features); column names come from spec column_labels
    samples = np.column_stack([lr, batch_size, epochs])
    np.save(output_file, samples)

    print(f"Generated {n_samples} hyperparameter combinations")

if __name__ == "__main__":
    main()
