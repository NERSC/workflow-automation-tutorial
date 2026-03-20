# Example 2: Provenance Querying and Workflow Restart

**Learning Objectives:**
- Query provenance graph with QueryBuilder
- Retrieve workflow history from database
- Export workflows for reproducibility
- Understand data lineage

**Concepts:** QueryBuilder, provenance traversal, workflow export, reproducibility

## Running

```bash
# Run query examples
python query_provenance.py

# Export workflow
verdi archive create --all archive.aiida

# Import elsewhere
verdi archive import archive.aiida
```
