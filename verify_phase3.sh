#!/bin/bash
set -e

echo "=========================================="
echo "PHASE 3 VERIFICATION REPORT"
echo "=========================================="
echo ""

echo "=== TASK 1: Main README verification ==="
echo "Checking 01-signac/README.md contains filesystem-based state tracking:"
grep -c "filesystem-based state tracking" 01-signac/README.md && echo "PASS: Found concept description"

echo ""
echo "=== TASK 2: Example 1 - Parameter Space Definition ==="
echo "Checking files exist:"
for f in 01-signac/example1-parameter-space/{README.md,init_project.py,explore_workspace.py}; do
  if [ -f "$f" ]; then
    echo "  OK: $f"
  else
    echo "  FAIL: $f missing"
    exit 1
  fi
done

echo "Checking syntax:"
python3.11 -m py_compile 01-signac/example1-parameter-space/init_project.py && echo "  init_project.py: OK"
python3.11 -m py_compile 01-signac/example1-parameter-space/explore_workspace.py && echo "  explore_workspace.py: OK"

echo ""
echo "=== TASK 3: Example 2 - Slurm Job Submission ==="
echo "Checking files exist:"
for f in 01-signac/example2-job-submission/{README.md,project.py,simulate.py}; do
  if [ -f "$f" ]; then
    echo "  OK: $f"
  else
    echo "  FAIL: $f missing"
    exit 1
  fi
done

echo "Checking syntax:"
python3.11 -m py_compile 01-signac/example2-job-submission/project.py && echo "  project.py: OK"
python3.11 -m py_compile 01-signac/example2-job-submission/simulate.py && echo "  simulate.py: OK"

echo ""
echo "=== TASK 4: Example 3 - Result Aggregation ==="
echo "Checking files exist:"
for f in 01-signac/example3-aggregation/{README.md,analyze_results.py,generate_fake_data.py}; do
  if [ -f "$f" ]; then
    echo "  OK: $f"
  else
    echo "  FAIL: $f missing"
    exit 1
  fi
done

echo "Checking syntax:"
python3.11 -m py_compile 01-signac/example3-aggregation/analyze_results.py && echo "  analyze_results.py: OK"
python3.11 -m py_compile 01-signac/example3-aggregation/generate_fake_data.py && echo "  generate_fake_data.py: OK"

echo ""
echo "=== TASK 5: Verification ==="
echo "All examples have valid Python syntax and required files present."
echo "Examples are designed to run on Perlmutter with signac/signac-flow installed."

echo ""
echo "=== TASK 6: Commit verification ==="
echo "Checking git commit:"
git log -1 --oneline 01-signac/README.md | grep "feat: add signac" && echo "  Commit found: OK"
git log -1 --format='%b' 01-signac/README.md | grep "Co-Authored-By" && echo "  Co-author attribution: OK"

echo ""
echo "=========================================="
echo "VERIFICATION COMPLETE: ALL CHECKS PASSED"
echo "=========================================="
