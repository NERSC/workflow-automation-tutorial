#!/bin/bash
# Generate sample input data

OUTPUT_FILE="$1"

echo "Generating input data..."

# Create simple input file with 10 data points
for i in {1..10}; do
  echo "$i $((i * i))" >> "$OUTPUT_FILE"
done

echo "Generated 10 data points in $OUTPUT_FILE"
