#!/usr/bin/env python
"""Placeholder simulation script.

This script runs in the job's workspace directory. It has access to the job's
parameters through the signac project API.
"""
import signac

job = signac.get_job()
print(f"Running simulation for job {job.id}")
print(f"Parameters: {job.sp}")
