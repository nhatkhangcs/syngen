"""
Schema inference for SynGen.

This module provides functionality to automatically infer
data schemas from existing data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from .base import DataSchema, ColumnSchema, DataType, DistributionType


class SchemaInferrer:
    """Class for inferring data schemas from existing data."""
    
    @staticmethod
    def infer(
        data: pd.DataFrame, 
        sample_size: Optional[int] = None
    ) -> DataSchema:
        """
        Infer schema from existing data.
        
        Args:
            data: Input DataFrame
            sample_size: Number of samples to use for inference
            
        Returns:
            Inferred data schema
        """
        # Sample data if specified
        if sample_size and sample_size < len(data):
            data = data.sample(n=sample_size, random_state=42)
        
        columns = []
        
        for col_name in data.columns:
            col_data = data[col_name]
            column_schema = SchemaInferrer._infer_column_schema(col_name, col_data)
            columns.append(column_schema)
        
        return DataSchema(columns=columns)
    
    @staticmethod
    def _infer_column_schema(column_name: str, column_data: pd.Series) -> ColumnSchema:
        """Infer schema for a single column."""
        
        # Determine data type
        data_type = SchemaInferrer._infer_data_type(column_data)
        
        # Determine distribution
        distribution, parameters = SchemaInferrer._infer_distribution(column_data, data_type)
        
        # Determine constraints
        constraints = SchemaInferrer._infer_constraints(column_data, data_type)
        
        return ColumnSchema(
            name=column_name,
            data_type=data_type,
            distribution=distribution,
            parameters=parameters,
            **constraints
        )
    
    @staticmethod
    def _infer_data_type(column_data: pd.Series) -> DataType:
        """Infer data type from column data."""
        
        # Handle missing values
        non_null_data = column_data.dropna()
        
        if len(non_null_data) == 0:
            return DataType.STRING
        
        # Check for boolean first (before numeric)
        if pd.api.types.is_bool_dtype(column_data):
            return DataType.BOOLEAN
        
        # Check for numeric types
        if pd.api.types.is_numeric_dtype(column_data):
            if pd.api.types.is_integer_dtype(column_data):
                return DataType.INTEGER
            else:
                return DataType.FLOAT
        
        # Check for datetime
        if pd.api.types.is_datetime64_any_dtype(column_data):
            return DataType.DATETIME
        
        # Check for date (simplified check)
        try:
            # Try to convert to datetime to see if it's a date
            pd.to_datetime(column_data.iloc[0])
            return DataType.DATE
        except:
            pass
        
        # Check for specific text patterns
        sample_values = non_null_data.head(100).astype(str)
        
        # Check for email pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if sample_values.str.match(email_pattern).mean() > 0.8:
            return DataType.EMAIL
        
        # Check for phone pattern
        phone_pattern = r'^[\+]?[1-9][\d]{0,15}$'
        if sample_values.str.replace(r'[^\d+]', '', regex=True).str.match(phone_pattern).mean() > 0.8:
            return DataType.PHONE
        
        # Check for address pattern (contains street, city, state, zip)
        address_indicators = ['street', 'avenue', 'road', 'drive', 'lane', 'court']
        if any(indicator in ' '.join(sample_values).lower() for indicator in address_indicators):
            return DataType.ADDRESS
        
        # Check for name pattern (first last format)
        name_pattern = r'^[A-Z][a-z]+ [A-Z][a-z]+$'
        if sample_values.str.match(name_pattern).mean() > 0.7:
            return DataType.NAME
        
        # Check for categorical
        unique_ratio = len(non_null_data.unique()) / len(non_null_data)
        if unique_ratio < 0.1:  # Less than 10% unique values
            return DataType.CATEGORICAL
        
        return DataType.STRING
    
    @staticmethod
    def _infer_distribution(
        column_data: pd.Series, 
        data_type: DataType
    ) -> tuple[DistributionType, Dict[str, Any]]:
        """Infer distribution and parameters from column data."""
        
        non_null_data = column_data.dropna()
        
        if len(non_null_data) == 0:
            return DistributionType.CONSTANT, {'value': None}
        
        if data_type in [DataType.INTEGER, DataType.FLOAT]:
            return SchemaInferrer._infer_numeric_distribution(non_null_data)
        elif data_type == DataType.CATEGORICAL:
            return SchemaInferrer._infer_categorical_distribution(non_null_data)
        elif data_type == DataType.BOOLEAN:
            return DistributionType.CATEGORICAL, {
                'categories': [True, False],
                'probabilities': [
                    (non_null_data == True).mean(),
                    (non_null_data == False).mean()
                ]
            }
        else:
            # For text data, use categorical distribution
            unique_values = non_null_data.unique()
            if len(unique_values) <= 20:  # Small number of unique values
                return DistributionType.CATEGORICAL, {
                    'categories': unique_values.tolist()
                }
            else:
                return DistributionType.UNIFORM, {}  # Default for text
    
    @staticmethod
    def _infer_numeric_distribution(column_data: pd.Series) -> tuple[DistributionType, Dict[str, Any]]:
        """Infer distribution for numeric data."""
        
        # Safety check: ensure we have numeric data
        if not pd.api.types.is_numeric_dtype(column_data):
            # If not numeric, treat as categorical
            return DistributionType.CATEGORICAL, {
                'categories': column_data.unique().tolist()
            }
        
        # Check if it's constant
        if column_data.nunique() == 1:
            return DistributionType.CONSTANT, {'value': column_data.iloc[0]}
        
        # Calculate basic statistics
        mean_val = column_data.mean()
        std_val = column_data.std()
        min_val = column_data.min()
        max_val = column_data.max()
        
        # Check for normal distribution
        if std_val > 0:
            # Simple normality test (check if 68% of data is within 1 std)
            within_one_std = ((column_data >= mean_val - std_val) & 
                             (column_data <= mean_val + std_val)).mean()
            
            if 0.6 <= within_one_std <= 0.8:
                return DistributionType.NORMAL, {
                    'mean': mean_val,
                    'std': std_val
                }
        
        # Check for uniform distribution
        range_val = max_val - min_val
        if range_val > 0:
            # Check if data is roughly uniform
            bins = np.linspace(min_val, max_val, 10)
            hist, _ = np.histogram(column_data, bins=bins)
            hist_std = hist.std()
            hist_mean = hist.mean()
            
            if hist_std / hist_mean < 0.5:  # Low variance in histogram
                return DistributionType.UNIFORM, {
                    'low': min_val,
                    'high': max_val
                }
        
        # Check for exponential distribution
        if min_val >= 0:
            # Simple exponential test
            exp_mean = column_data.mean()
            exp_std = column_data.std()
            
            if abs(exp_mean - exp_std) / exp_mean < 0.2:  # Mean ≈ std for exponential
                return DistributionType.EXPONENTIAL, {
                    'scale': exp_mean
                }
        
        # Default to normal distribution
        return DistributionType.NORMAL, {
            'mean': mean_val,
            'std': std_val
        }
    
    @staticmethod
    def _infer_categorical_distribution(column_data: pd.Series) -> tuple[DistributionType, Dict[str, Any]]:
        """Infer distribution for categorical data."""
        
        value_counts = column_data.value_counts()
        categories = value_counts.index.tolist()
        probabilities = (value_counts / len(column_data)).tolist()
        
        return DistributionType.CATEGORICAL, {
            'categories': categories,
            'probabilities': probabilities
        }
    
    @staticmethod
    def _infer_constraints(
        column_data: pd.Series, 
        data_type: DataType
    ) -> Dict[str, Any]:
        """Infer constraints from column data."""
        
        constraints = {}
        
        # Check for uniqueness
        if column_data.nunique() == len(column_data):
            constraints['unique'] = True
        
        # Check for null probability
        null_prob = column_data.isnull().mean()
        if null_prob > 0:
            constraints['null_probability'] = null_prob
            constraints['nullable'] = True
        
        # Check for min/max values for numeric data
        if data_type in [DataType.INTEGER, DataType.FLOAT]:
            non_null_data = column_data.dropna()
            if len(non_null_data) > 0:
                constraints['min_value'] = non_null_data.min()
                constraints['max_value'] = non_null_data.max()
        
        return constraints 