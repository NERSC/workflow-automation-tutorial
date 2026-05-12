#!/usr/bin/env python
"""Explore the auto-generated workspace directory structure."""
import signac

project = signac.get_project()

print(f"Project contains {len(project)} jobs:")
for job in project:
    print(f"Job {job.id[:8]}: temp={job.sp.temperature}, pressure={job.sp.pressure}")
    print(f"  -> Directory: {job.path}")
