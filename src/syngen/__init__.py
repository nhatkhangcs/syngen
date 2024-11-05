from . import attribute
from . import condition
from . import dtype
from . import validate_args
from typing import List, Tuple

import pandas as pd

__all__ = [
    'attribute',
    'condition',
    'dtype',
]

__version__ = '0.0.0'

def gen(
    attributes: List[Tuple[str, dtype.BaseType]],
    conditions: dict[str, List[condition.BaseCondition]],
    n_samples: int,
) -> pd.DataFrame:
    validate_args.BaseValidator(attributes=attributes, conditions=conditions)
    
    data = {col: arr[0](n_samples) for col, arr in conditions.items()}
    df = pd.DataFrame(data)
    
    return df
