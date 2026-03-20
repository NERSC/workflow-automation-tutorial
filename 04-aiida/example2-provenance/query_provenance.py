#!/usr/bin/env python
"""Query provenance graph examples."""

from aiida import orm
from aiida.orm import QueryBuilder, WorkflowNode, CalcFunctionNode, Int

def query_recent_workflows():
    """Find recent workflows."""
    qb = QueryBuilder()
    qb.append(WorkflowNode, filters={'ctime': {'>': '-7d'}})
    print(f"Found {qb.count()} workflows in last 7 days")

    for node, in qb.iterall():
        print(f"  {node.pk}: {node.label}")

def query_by_input_value(target_value):
    """Find calculations with specific input value."""
    qb = QueryBuilder()
    qb.append(Int, filters={'value': target_value}, tag='input')
    qb.append(CalcFunctionNode, with_incoming='input')

    print(f"Calculations with input {target_value}:")
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
    query_recent_workflows()
    query_by_input_value(42)
    # trace_provenance(12345)  # Replace with actual PK
