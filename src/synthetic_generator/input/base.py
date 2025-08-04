from ..validate_args import BaseValidator


class BaseInput:

    def __init__(self, attributes, datatypes):
        o = BaseValidator(attributes=attributes)
        self.attributes = o.attributes
        self.datatypes = datatypes
