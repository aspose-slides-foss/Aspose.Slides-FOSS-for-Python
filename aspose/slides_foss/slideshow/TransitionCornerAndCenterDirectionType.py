from __future__ import annotations
from enum import Enum
class TransitionCornerAndCenterDirectionType(Enum):
    """Specifies a direction restricted to the corners and center."""
    LEFT_DOWN = 'LeftDown'
    LEFT_UP = 'LeftUp'
    RIGHT_DOWN = 'RightDown'
    RIGHT_UP = 'RightUp'
    CENTER = 'Center'
