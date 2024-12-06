from enum import Enum

class OptionalWayOfCommpare(Enum):
    FullCompare = 'FULL'
    BaseConfig = 'Base'
    CustomConfig = 'Custom'

class SupportChannel(Enum):
    Common = 0
    prach = 1
    pucch = 2
    pusch = 3
    srs = 4
