"""
Export functionality for SynGen.

This module provides utilities for exporting generated data
to various formats and databases.
"""

from .formats import DataExporter
from .database import DatabaseExporter

__all__ = [
    'DataExporter',
    'DatabaseExporter',
    'export_data'
]

def export_data(data, format_type: str, **kwargs):
    """Export data to specified format."""
    exporter = DataExporter()
    return exporter.export(data, format_type, **kwargs) 