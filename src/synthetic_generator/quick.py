from __future__ import annotations

from typing import Optional, Union, Dict, Any
import os
import pandas as pd

from .schemas import DataSchema
from .schemas import load_template as load_template_schema
from .schemas.inference import SchemaInferrer
from . import generate_data


def dataset(
    template: Optional[str] = None,
    schema: Optional[Union[Dict[str, Any], DataSchema]] = None,
    rows: int = 1000,
    seed: Optional[int] = None,
) -> pd.DataFrame:
    """
    Generate a dataset quickly from a template or a minimal schema.

    Args:
        template: Name of a built-in template (e.g., 'customer_data', 'ecommerce_data').
        schema: Minimal schema dict or DataSchema instance.
        rows: Number of rows to generate.
        seed: Optional random seed for reproducibility.

    Returns:
        Generated DataFrame.
    """
    if template is None and schema is None:
        raise ValueError("Provide either template or schema")

    if template is not None:
        schema_obj = load_template_schema(template)
    else:
        if isinstance(schema, dict):
            schema_obj = DataSchema.from_dict(schema)
        elif isinstance(schema, DataSchema):
            schema_obj = schema
        else:
            raise ValueError("schema must be a dict or DataSchema when provided")

    return generate_data(schema_obj, n_samples=rows, seed=seed)


class QuickModel:
    """A simple fitted model wrapper that can sample new synthetic data."""

    def __init__(self, schema: DataSchema):
        self._schema = schema

    def sample(self, rows: int, seed: Optional[int] = None) -> pd.DataFrame:
        return generate_data(self._schema, n_samples=rows, seed=seed)

    def to_dict(self) -> Dict[str, Any]:
        return self._schema.to_dict()


def fit(data: Union[pd.DataFrame, str], sample_size: Optional[int] = None) -> QuickModel:
    """
    Fit a simple model by inferring a schema from real data.

    Args:
        data: A pandas DataFrame or a file path to CSV/JSON/Parquet/Excel.
        sample_size: Optional subsample size used during inference.

    Returns:
        QuickModel that can sample synthetic rows via .sample().
    """
    df = _load_dataframe(data)
    inferred = SchemaInferrer.infer(df, sample_size)
    return QuickModel(inferred)


def _load_dataframe(data: Union[pd.DataFrame, str]) -> pd.DataFrame:
    if isinstance(data, pd.DataFrame):
        return data
    if not isinstance(data, str):
        raise ValueError("data must be a DataFrame or a path string")

    path = data
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return pd.read_csv(path)
    if ext == ".json":
        return pd.read_json(path)
    if ext in (".parquet", ".pq"):
        return pd.read_parquet(path)
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(path)

    # Fallback: try CSV
    return pd.read_csv(path)
