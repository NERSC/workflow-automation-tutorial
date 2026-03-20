"""Utility for wrapping external codes in AiiDA CalcJobs.

This module provides patterns for integrating external computational codes
with AiiDA's provenance system.
"""

from aiida.orm import List, Str, Int, Float, Dict
from aiida.engine import calcfunction


@calcfunction
def wrapped_external_code(code_path, input_file, parameters):
    """
    Example of wrapping an external code execution.

    In a real scenario, this would:
    1. Prepare input files from AiiDA data nodes
    2. Execute external code
    3. Parse outputs into AiiDA data nodes

    Args:
        code_path: Path to external executable
        input_file: Input file content
        parameters: Dictionary of code parameters

    Returns:
        Dictionary with results and metadata
    """
    # This is a template showing how to structure code wrapping
    # Real implementations would execute the external code here
    # and parse results back into AiiDA nodes

    result = {
        'status': 'completed',
        'message': 'Code wrapper template for external code integration',
        'provenance_tracked': True,
    }

    return Dict(result)


def get_code_node(code_label, remote_computer):
    """
    Retrieve or register a code node for use in calculations.

    Code nodes represent installed executables on HPC systems.
    They enable portable workflow definitions across different systems.

    Args:
        code_label: Unique code identifier
        remote_computer: Computer node where code is installed

    Returns:
        Code node for use in calculations
    """
    # This is a helper showing the pattern for code management
    # In practice, codes are registered with:
    # verdi code create-entry core.code.installed ...
    pass
