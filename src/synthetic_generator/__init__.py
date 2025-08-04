"""
Synthetic Generator - Synthetic Data Generator for Machine Learning Pipelines

A comprehensive library for generating synthetic data with various distributions,
correlations, and constraints for machine learning and data science applications.
"""

from . import attribute
from . import dtype
from . import generators
from . import schemas
from . import privacy
from . import export
from . import utils
from typing import Dict, Any, Optional, Union
import pandas as pd

# Import main classes for easy access
from .schemas import DataSchema, ColumnSchema, DataType, DistributionType

__all__ = [
    'attribute',
    'dtype',
    'generators',
    'schemas',
    'privacy',
    'export',
    'utils',
    'generate_data',
    'infer_schema',
    'load_template',
    'validate_data',
    'DataSchema',
    'ColumnSchema',
    'DataType',
    'DistributionType'
]

__version__ = '0.1.3'

def generate_data(
    schema: Union[Dict[str, Any], 'schemas.DataSchema'],
    n_samples: int,
    seed: Optional[int] = None,
    constraints: Optional[Dict[str, Any]] = None,
    privacy_level: Optional[str] = None
) -> pd.DataFrame:
    """
    Generate synthetic data based on a schema.
    
    Args:
        schema: Data schema defining columns and their properties
        n_samples: Number of samples to generate
        seed: Random seed for reproducibility
        constraints: Additional constraints for data generation
        privacy_level: Privacy level ('none', 'basic', 'differential')
    
    Returns:
        DataFrame with synthetic data
    """
    if seed is not None:
        import numpy as np
        np.random.seed(seed)
    
    # Convert dict to schema if needed
    if isinstance(schema, dict):
        schema = schemas.DataSchema.from_dict(schema)
    
    # Apply privacy if specified
    if privacy_level:
        schema = privacy.apply_privacy_settings(schema, privacy_level)
    
    # Generate data
    generator = generators.DataGenerator(schema, constraints)
    return generator.generate(n_samples)

def infer_schema(
    data: pd.DataFrame,
    sample_size: Optional[int] = None
) -> 'schemas.DataSchema':
    """
    Automatically infer data schema from existing data.
    
    Args:
        data: Input DataFrame
        sample_size: Number of samples to use for inference
    
    Returns:
        Inferred data schema
    """
    return schemas.DataSchema.infer(data, sample_size)

def load_template(template_name: str) -> 'schemas.DataSchema':
    """
    Load a pre-built template for common use cases.
    
    Args:
        template_name: Name of the template
    
    Returns:
        Data schema template
    """
    return schemas.load_template(template_name)

def validate_data(
    data: pd.DataFrame,
    schema: Union[Dict[str, Any], 'schemas.DataSchema']
) -> Dict[str, Any]:
    """
    Validate generated data against schema.
    
    Args:
        data: Generated data
        schema: Data schema
    
    Returns:
        Validation results
    """
    if isinstance(schema, dict):
        schema = schemas.DataSchema.from_dict(schema)
    
    return schema.validate_data(data)
