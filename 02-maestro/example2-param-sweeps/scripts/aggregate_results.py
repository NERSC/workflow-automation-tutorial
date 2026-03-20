#!/usr/bin/env python3
"""Aggregate results from all parameter sweep runs."""

import argparse
import glob
import os
import re
import sys

def parse_output_file(filepath):
    """Extract statistics from simulation output file."""
    data = {}
    with open(filepath, 'r') as f:
        for line in f:
            if 'SIZE=' in line:
                match = re.search(r'SIZE=(\d+)', line)
                if match:
                    data['size'] = int(match.group(1))
            elif 'Mean:' in line:
                data['mean'] = float(line.split(':')[1].strip())
            elif 'Min:' in line:
                data['min'] = int(line.split(':')[1].strip())
            elif 'Max:' in line:
                data['max'] = int(line.split(':')[1].strip())
    return data

def main():
    parser = argparse.ArgumentParser(description='Aggregate parameter sweep results')
    parser.add_argument('--workspace', required=True, help='Workspace directory containing run directories')
    parser.add_argument('--pattern', required=True, help='Glob pattern for output files')
    parser.add_argument('--output', required=True, help='Output summary file')
    args = parser.parse_args()

    print(f"Searching for results in {args.workspace}")

    # Find all output files matching pattern
    search_pattern = os.path.join(args.workspace, args.pattern)
    output_files = glob.glob(search_pattern)

    print(f"Found {len(output_files)} result files")

    if not output_files:
        print(f"ERROR: No files matching pattern {search_pattern}")
        sys.exit(1)

    # Parse all results
    all_results = []
    for filepath in sorted(output_files):
        data = parse_output_file(filepath)
        if data:
            all_results.append(data)
            print(f"  Parsed: SIZE={data.get('size', '?')} Mean={data.get('mean', '?'):.2f}")

    # Write aggregated summary
    with open(args.output, 'w') as f:
        f.write("Aggregated Results Across All SIZE Values\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total parameter combinations: {len(all_results)}\n\n")
        f.write("Per-Parameter Results:\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'SIZE':<10} {'Mean':<10} {'Min':<10} {'Max':<10}\n")
        f.write("-" * 50 + "\n")

        for result in sorted(all_results, key=lambda x: x.get('size', 0)):
            f.write(f"{result['size']:<10} {result['mean']:<10.2f} {result['min']:<10} {result['max']:<10}\n")

        # Overall statistics
        if all_results:
            all_means = [r['mean'] for r in all_results]
            overall_mean = sum(all_means) / len(all_means)

            f.write("\n" + "-" * 50 + "\n")
            f.write(f"Overall mean across all SIZE values: {overall_mean:.2f}\n")

    print(f"Aggregation complete. Summary written to {args.output}")

if __name__ == "__main__":
    main()
