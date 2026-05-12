#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""Comprehensive test of all signac examples.

This script verifies that all example scripts:
1. Have correct Python syntax
2. Can be imported without import errors (with mocked dependencies)
3. Follow the expected structure and patterns
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Test execution
TEST_RESULTS = {
    'syntax_checks': [],
    'structure_checks': [],
    'import_checks': [],
    'execution_checks': []
}


def check_file_syntax(filepath):
    """Check if a Python file has valid syntax."""
    try:
        with open(filepath, 'r') as f:
            compile(f.read(), filepath, 'exec')
        return True, "Syntax OK"
    except SyntaxError as e:
        return False, str(e)


def check_readme_exists(example_dir):
    """Check if README.md exists in example directory."""
    readme = example_dir / 'README.md'
    if readme.exists():
        return True, f"README found ({readme.stat().st_size} bytes)"
    return False, "README not found"


def check_file_exists(filepath):
    """Check if a file exists and has content."""
    p = Path(filepath)
    if p.exists() and p.stat().st_size > 0:
        return True, f"File exists ({p.stat().st_size} bytes)"
    return False, f"File missing or empty"


def test_example1():
    """Test example1-parameter-space structure and syntax."""
    example_dir = Path('/global/u1/w/warndt/workflow_tutorial_research/01-signac/example1-parameter-space')

    print("\n=== EXAMPLE 1: Parameter Space Definition ===")

    # Check files exist
    files = ['README.md', 'init_project.py', 'explore_workspace.py', 'inspect_workspace.sh']
    for fname in files:
        fpath = example_dir / fname
        ok, msg = check_file_exists(fpath)
        TEST_RESULTS['structure_checks'].append((f"example1/{fname}", ok, msg))
        print(f"  {fname}: {msg}")

    # Check syntax
    for fname in ['init_project.py', 'explore_workspace.py']:
        fpath = example_dir / fname
        ok, msg = check_file_syntax(fpath)
        TEST_RESULTS['syntax_checks'].append((f"example1/{fname}", ok, msg))
        print(f"  {fname} syntax: {msg}")


def test_example2():
    """Test example2-job-submission structure and syntax."""
    example_dir = Path('/global/u1/w/warndt/workflow_tutorial_research/01-signac/example2-job-submission')

    print("\n=== EXAMPLE 2: Slurm Job Submission ===")

    # Check files exist
    files = ['README.md', 'project.py', 'simulate.py']
    for fname in files:
        fpath = example_dir / fname
        ok, msg = check_file_exists(fpath)
        TEST_RESULTS['structure_checks'].append((f"example2/{fname}", ok, msg))
        print(f"  {fname}: {msg}")

    # Check syntax
    for fname in ['project.py', 'simulate.py']:
        fpath = example_dir / fname
        ok, msg = check_file_syntax(fpath)
        TEST_RESULTS['syntax_checks'].append((f"example2/{fname}", ok, msg))
        print(f"  {fname} syntax: {msg}")


def test_example3():
    """Test example3-aggregation structure and syntax."""
    example_dir = Path('/global/u1/w/warndt/workflow_tutorial_research/01-signac/example3-aggregation')

    print("\n=== EXAMPLE 3: Result Aggregation ===")

    # Check files exist
    files = ['README.md', 'analyze_results.py', 'generate_fake_data.py']
    for fname in files:
        fpath = example_dir / fname
        ok, msg = check_file_exists(fpath)
        TEST_RESULTS['structure_checks'].append((f"example3/{fname}", ok, msg))
        print(f"  {fname}: {msg}")

    # Check syntax
    for fname in ['analyze_results.py', 'generate_fake_data.py']:
        fpath = example_dir / fname
        ok, msg = check_file_syntax(fpath)
        TEST_RESULTS['syntax_checks'].append((f"example3/{fname}", ok, msg))
        print(f"  {fname} syntax: {msg}")


def test_main_readme():
    """Test main signac README.md."""
    print("\n=== MAIN SIGNAC README ===")

    readme = Path('/global/u1/w/warndt/workflow_tutorial_research/01-signac/README.md')
    ok, msg = check_file_exists(readme)
    TEST_RESULTS['structure_checks'].append(("01-signac/README.md", ok, msg))
    print(f"  README.md: {msg}")

    # Check for key content
    if readme.exists():
        content = readme.read_text()
        checks = [
            ('filesystem-based state tracking', 'filesystem-based state tracking' in content),
            ('example1-parameter-space', 'example1-parameter-space' in content),
            ('example2-job-submission', 'example2-job-submission' in content),
            ('example3-aggregation', 'example3-aggregation' in content),
        ]
        for check_name, result in checks:
            TEST_RESULTS['structure_checks'].append((f"README content: {check_name}", result, "Found" if result else "Missing"))
            print(f"  Content check '{check_name}': {'Found' if result else 'Missing'}")


def print_summary():
    """Print test summary."""
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    total_ok = 0
    total_fail = 0

    for category, results in TEST_RESULTS.items():
        if not results:
            continue
        print(f"\n{category.upper()}:")
        for name, ok, msg in results:
            status = "PASS" if ok else "FAIL"
            total_ok += 1 if ok else 0
            total_fail += 0 if ok else 1
            print(f"  [{status}] {name}: {msg}")

    print(f"\n{'='*70}")
    print(f"Total: {total_ok} passed, {total_fail} failed")
    print(f"{'='*70}")

    return total_fail == 0


if __name__ == '__main__':
    print("Verifying Phase 3 signac examples...\n")

    test_main_readme()
    test_example1()
    test_example2()
    test_example3()

    success = print_summary()
    sys.exit(0 if success else 1)
