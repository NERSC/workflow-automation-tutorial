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

def build_workflow(param):
    """
    Build a 3-step workflow with automatic provenance.

    Args:
        param: Input parameter (Int)

    Returns:
        WorkGraph ready to run
    """
    wg = WorkGraph('simple_workflow')

    # Define workflow steps
    prep = wg.add_task(prepare_data, name='prepare', param=param)
    comp = wg.add_task(compute, name='compute', data=prep.outputs.result)
    wg.add_task(analyze, name='analyze', result=comp.outputs.result)

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

    print(f"Running workflow with param={args.param}...")

    # Build and run workflow synchronously — no daemon or RabbitMQ needed
    wg = build_workflow(param=orm.Int(args.param))
    wg.run()

    pk = wg.process.pk
    print(f"\nWorkflow completed! PK: {pk}")
    print(f"\nExplore the provenance:")
    print(f"  verdi process list -a                  # List all workflows")
    print(f"  verdi process show {pk}           # Inspect this workflow")
    print(f"  verdi node graph generate {pk} --output-format png  # Visualize provenance graph")
