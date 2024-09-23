from ..condition import BaseCondition
from ..dtype import BaseType
from pydantic import BaseModel as PyndanticBaseModel
from pydantic import model_validator
from typing import List, Iterable
import pandas as pd


class BaseModel(PyndanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class BaseValidator(BaseModel):
    attributes: List[str]
    datatypes: List[BaseType]
    condition: List[BaseCondition]

    @model_validator(mode='after')
    def check_len(self):
        att_len = len(self.attributes)
        dtp_len = len(self.datatypes)
        con_len = len(self.condition)
        print(att_len, con_len, dtp_len)

        if dtp_len == 1:
            self.datatypes = att_len * self.datatypes
            print(self.datatypes)
        if att_len != con_len:
            raise ValueError(f'{len(self.attributes)} != {len(self.condition)}')

        return self
