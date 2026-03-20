#!/usr/bin/env python
"""Simple WorkGraph workflow demonstrating provenance capture."""

from aiida import orm
from aiida_workgraph import task, WorkGraph

@task.calcfunction
def prepare_data(param):
    """Prepare input data."""
    return orm.Int(param * 2)

@task.calcfunction
def compute(data):
    """Perform computation."""
    result = data.value ** 2
    return orm.Int(result)

@task.calcfunction
def analyze(result):
    """Analyze result."""
    final = result.value + 100
    return orm.Dict({'final_result': final, 'status': 'complete'})

@task.graph_builder
def simple_workflow(param):
    """
    Simple 3-step workflow with automatic provenance.

    Args:
        param: Input parameter (Int)

    Returns:
        Analysis results (Dict)
    """
    wg = WorkGraph('simple_workflow')

    # Define workflow steps
    prep = wg.tasks.new(prepare_data, name='prepare', param=param)
    comp = wg.tasks.new(compute, name='compute', data=prep.outputs.result)
    anal = wg.tasks.new(analyze, name='analyze', result=comp.outputs.result)

    # Return final result
    wg.add_task(anal)
    return wg

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--param', type=int, default=5)
    args = parser.parse_args()

    # Submit workflow
    result = simple_workflow(orm.Int(args.param))
    print(f"Workflow submitted. Check with: verdi process list")
