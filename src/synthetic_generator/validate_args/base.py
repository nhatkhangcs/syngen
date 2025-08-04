from ..dtype import BaseType
from pydantic import BaseModel as PyndanticBaseModel
from pydantic import model_validator
from typing import List, Tuple, Dict


class BaseModel(PyndanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class BaseValidator(BaseModel):
    attributes: List[Tuple[str, BaseType]]

    @model_validator(mode='after')
    def unique(self):
        names: list[str] = [t for t, _ in self.attributes]
        if len(names) != len(set(names)):
            raise ValueError('Attributes name must be unique!')
        return self
    