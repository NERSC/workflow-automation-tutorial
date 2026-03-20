#!/bin/bash
# Simulates flaky task that fails 50% of the time

ATTEMPT_LOG="$1"
ATTEMPT=1

if [ -f "$ATTEMPT_LOG" ]; then
  ATTEMPT=$(cat "$ATTEMPT_LOG")
  ATTEMPT=$((ATTEMPT + 1))
fi

echo $ATTEMPT > "$ATTEMPT_LOG"

echo "Attempt $ATTEMPT"

# 50% chance of failure (except on 4th attempt, always succeed)
if [ $ATTEMPT -lt 4 ]; then
  if [ $((RANDOM % 2)) -eq 0 ]; then
    echo "Task failed (transient error)"
    exit $(merlin config | grep MERLIN_RETRY | cut -d'=' -f2)
  fi
fi

echo "Task succeeded on attempt $ATTEMPT"
exit 0
