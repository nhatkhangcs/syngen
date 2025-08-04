class BaseType:
    def __init__(self):
        pass
    
    def __str__(self) -> str:
        return self.__class__.__name__
    

class BaseFloat(BaseType):
    def __init__(self):
        super().__init__()


class BaseInt(BaseType):
    def __init__(self):
        super().__init__()


class BaseBool(BaseType):
    def __init__(self):
        super().__init__()
