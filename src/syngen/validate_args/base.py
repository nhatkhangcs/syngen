from ..condition import BaseCondition
from ..dtype import BaseType
from pydantic import BaseModel as PyndanticBaseModel
from pydantic import model_validator
from typing import List, Iterable, Tuple, Dict
import pandas as pd


class BaseModel(PyndanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class BaseValidator(BaseModel):
    attributes: List[Tuple[str, BaseType]]
    conditions: Dict[str, List[BaseCondition]]

    @model_validator(mode='after')
    def unique(self):
        names: list[str] = [t for t, _ in self.attributes]
        if len(names) != len(set(names)):
            raise ValueError('Attributes name must be unique!')
        return self

    @model_validator(mode='after')
    def check_len(self):
        att_len = len(self.attributes)
        con_len = len(self.conditions)

        if att_len != con_len:
            raise ValueError(f'{len(self.attributes)} != {len(self.conditions)}')

        return self


    @model_validator(mode='after')
    def check_matching_column_names(self):
        columns_attr = {col: 1 for col, _ in self.attributes}
        undefined_cols = list(filter(lambda col: columns_attr.get(col) is None, self.conditions))
        
        if undefined_cols:
            raise ValueError(f'Column names do not match: {undefined_cols}')
    
        return self
    