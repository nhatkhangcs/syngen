from ..validate_args import BaseValidator


class BaseInput:

    def __init__(self, attributes, datatypes, condition):
        o = BaseValidator(attributes=attributes, datatypes=datatypes, condition=condition)
        self.attributes = o.attributes
        self.datatypes = o.datatypes
        self.condition = o.condition
