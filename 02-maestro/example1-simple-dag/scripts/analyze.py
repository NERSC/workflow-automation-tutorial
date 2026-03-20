#!/usr/bin/env python3
"""Analyze simulation results."""

import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: analyze.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print(f"Analyzing results from {input_file}")

    # Read simulation results
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if not line.startswith('#')]

    # Parse results
    results = []
    for line in lines:
        parts = line.split()
        if len(parts) == 3:
            results.append(int(parts[2]))

    # Calculate statistics
    if results:
        mean = sum(results) / len(results)
        min_val = min(results)
        max_val = max(results)

        # Write summary
        with open(output_file, 'w') as f:
            f.write(f"Analysis Summary\n")
            f.write(f"================\n")
            f.write(f"Count: {len(results)}\n")
            f.write(f"Mean:  {mean:.2f}\n")
            f.write(f"Min:   {min_val}\n")
            f.write(f"Max:   {max_val}\n")

        print(f"Analysis complete. Summary written to {output_file}")
    else:
        print("No results to analyze!")
        sys.exit(1)

if __name__ == "__main__":
    main()
