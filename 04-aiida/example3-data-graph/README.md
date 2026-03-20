# Example 3: Data Lineage Visualization

**Learning Objectives:**
- Visualize provenance graph
- Answer "where did this result come from?"
- Generate publication-grade documentation
- Use WorkGraph GUI

**Concepts:** Data lineage, graph visualization, reproducibility documentation

## Visualizing Provenance

```bash
# Generate graph for workflow
verdi node graph generate <PK> --output lineage.pdf

# View in browser (requires graphviz)
verdi node graph generate <PK> | dot -Tpng > lineage.png

# WorkGraph GUI (interactive)
workgraph web start
# Visit http://localhost:8000/workgraph
```

## Answering Origin Questions

For any result node PK:
```bash
# Show complete provenance
verdi node show <PK>

# Recursive ancestor tree
verdi node graph generate <PK> --ancestor-depth 999
```

## Publication-Ready Export

```bash
# Export with full provenance
verdi archive create --nodes <PK> publication.aiida

# Include all calculations
verdi archive create --all full_study.aiida
```

Publication archives enable reviewers to verify computational results years later.
