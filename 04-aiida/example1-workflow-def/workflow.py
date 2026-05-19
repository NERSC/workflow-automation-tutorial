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

    return wg

if __name__ == '__main__':
    from aiida import load_profile
    load_profile()

    import argparse
    parser = argparse.ArgumentParser(
        description='Run simple AiiDA workflow with automatic provenance'
    )
    parser.add_argument('--param', type=int, default=5,
                        help='Input parameter value')
    args = parser.parse_args()

    from aiida.engine import run_get_node

    print(f"Running workflow with param={args.param}...")

    # Run workflow synchronously — no daemon or RabbitMQ needed
    result, node = run_get_node(simple_workflow, param=orm.Int(args.param))

    print(f"\nWorkflow completed! PK: {node.pk}")
    print(f"\nExplore the provenance:")
    print(f"  verdi process list -a                  # List all workflows")
    print(f"  verdi process show {node.pk}           # Inspect this workflow")
    print(f"  verdi node graph generate {node.pk}    # Visualize provenance graph")
