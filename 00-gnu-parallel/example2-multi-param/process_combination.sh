#!/bin/bash
# Process one parameter combination
# In real workflow, this runs your experiment with specific parameters

ALGORITHM=$1
SIZE=$2
OPTIMIZATION=$3

echo "Processing: algorithm=${ALGORITHM}, size=${SIZE}, opt=${OPTIMIZATION}"

# Simulate computational work
sleep 2

# In real workflow:
# ./run_experiment --algorithm $ALGORITHM --dataset data_${SIZE}.dat --opt $OPTIMIZATION > results_${ALGORITHM}_${SIZE}_${OPTIMIZATION}.txt

echo "  -> Complete: ${ALGORITHM}/${SIZE}/${OPTIMIZATION}"
