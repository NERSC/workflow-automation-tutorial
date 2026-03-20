#!/usr/bin/env python3
"""Process task demonstrating distributed execution."""

import argparse
import time
import socket

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--param', type=int, required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    hostname = socket.gethostname()
    print(f"Processing PARAM={args.param} on {hostname}")

    # Simulate work
    time.sleep(2)

    # Read input
    with open(args.input) as f:
        input_data = f.read()

    # Write result
    with open(args.output, 'w') as f:
        f.write(f"PARAM {args.param} Results\n")
        f.write(f"Processed on: {hostname}\n")
        f.write(f"Input received: {len(input_data)} bytes\n")
        f.write(f"Computation result: {args.param * 100}\n")

    print(f"PARAM={args.param} complete")

if __name__ == "__main__":
    main()
