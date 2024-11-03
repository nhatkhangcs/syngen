import numpy as np
from abc import ABC, abstractmethod


class BaseCondition(ABC):

    def __init__(self):
        pass


class Condition(BaseCondition, ABC):

    def __init__(self):
        super().__init__()
        pass

    @abstractmethod
    def __getitem__(self, item):
        pass
