#!/usr/bin/env python3
"""Simple simulation that processes input data."""

import sys
import time

def main():
    if len(sys.argv) != 4:
        print("Usage: simulate.py <input_file> <output_file> <sleep_time>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    sleep_time = int(sys.argv[3])

    print(f"Reading input from {input_file}")

    # Read input data
    with open(input_file, 'r') as f:
        data = [line.strip().split() for line in f]

    # Simulate work
    print(f"Simulating work (sleeping {sleep_time}s)...")
    time.sleep(sleep_time)

    # Process data (simple transformation)
    results = []
    for x, y in data:
        x_val = int(x)
        y_val = int(y)
        result = y_val * 2  # Simple transformation
        results.append(f"{x_val} {y_val} {result}")

    # Write results
    with open(output_file, 'w') as f:
        f.write("# x y result\n")
        for line in results:
            f.write(line + '\n')

    print(f"Simulation complete. Results written to {output_file}")

if __name__ == "__main__":
    main()
