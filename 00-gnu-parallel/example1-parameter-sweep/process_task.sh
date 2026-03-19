#!/bin/bash
# Placeholder task simulating 2-second computation
# In real workflow, this would be your analysis script

TASK_ID=$1

echo "Processing input ${TASK_ID}... (simulates 2-second task)"

# Simulate computational work
sleep 2

# In real workflow, produce output:
# ./actual_analysis input_${TASK_ID}.dat > output_${TASK_ID}.txt

echo "Task ${TASK_ID} complete"
