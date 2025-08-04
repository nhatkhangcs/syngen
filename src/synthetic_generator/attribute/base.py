class BaseAttribute:
    def __init__(self):
        pass


class Attribute(BaseAttribute):
    def __init__(self, name, dtype):
        super().__init__()
        self.name = name
        self.dtype = dtype
