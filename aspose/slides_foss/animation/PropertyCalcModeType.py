from __future__ import annotations
from enum import Enum

class PropertyCalcModeType(Enum):
    """Represent calc mode for animation property."""
    NOT_DEFINED = 'NotDefined'
    DISCRETE = 'Discrete'
    LINEAR = 'Linear'
    FORMULA = 'Formula'
