from __future__ import annotations
from enum import Enum

class BehaviorAdditiveType(Enum):
    """Represents additive type for effect behavior."""
    NOT_DEFINED = 'NotDefined'
    NONE = 'None'
    BASE = 'Base'
    SUM = 'Sum'
    REPLACE = 'Replace'
    MULTIPLY = 'Multiply'
