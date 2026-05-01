#!/usr/bin/env python
"""Query provenance graph examples."""

from aiida import orm
from aiida.orm import QueryBuilder, WorkflowNode, CalcFunctionNode, Int

def query_recent_workflows():
    """Find recent workflows."""
    qb = QueryBuilder()
    qb.append(WorkflowNode, filters={'ctime': {'>': '-7d'}})
    count = qb.count()
    print(f"Found {count} workflows in last 7 days")

    if count == 0:
        print("\n  No workflows found. Did you run example 1 first?")
        print("    cd ../example1-workflow-def")
        print("    python workflow.py --param 42")
        return

    for node, in qb.iterall():
        print(f"  {node.pk}: {node.label}")

def query_by_input_value(target_value):
    """Find calculations with specific input value."""
    qb = QueryBuilder()
    qb.append(Int, filters={'value': target_value}, tag='input')
    qb.append(CalcFunctionNode, with_incoming='input')

    count = qb.count()
    print(f"\nCalculations with input {target_value}:")
    if count == 0:
        print(f"  No calculations found with input value {target_value}.")
        print(f"  Try running: python ../example1-workflow-def/workflow.py --param {target_value}")
        return

    for node, in qb.iterall():
        print(f"  PK {node.pk}: {node.process_label}")

def trace_provenance(pk):
    """Trace provenance of a result."""
    node = orm.load_node(pk)
    print(f"Provenance of PK {pk}:")

    # Walk inputs
    for link in node.base.links.get_incoming():
        print(f"  Input: {link.node.pk} ({link.link_label})")

    # Walk outputs
    for link in node.base.links.get_outgoing():
        print(f"  Output: {link.node.pk} ({link.link_label})")

if __name__ == '__main__':
    from aiida import load_profile
    load_profile()

    query_recent_workflows()
    query_by_input_value(42)
    # Uncomment with an actual PK from example 1:
    # trace_provenance(<PK>)
