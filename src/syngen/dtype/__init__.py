from .base import *
from .float import *
from .int import *

#@formatter:off
base_type = BaseType()
base_float = BaseFloat()
base_int = BaseInt()
base_bool = BaseBool()
# Float
float32 = Float32()
float64 = Float64()
# Int
int32 = Int32()
int64 = Int64()
#@formatter:on

__all__ = [
    ##### Classes #####
    # Base
    'BaseType',
    'BaseFloat',
    'BaseInt',
    'BaseBool',
    # Float
    'Float32',
    'Float64',
    # Int
    'Int32',
    'Int64',
    ##### Instances #####
    # Base
    'base_type',
    'base_float',
    'base_int',
    'base_bool',
    # Float
    'float32',
    'float64',
    # Int
    'int32',
    'int64',
]
