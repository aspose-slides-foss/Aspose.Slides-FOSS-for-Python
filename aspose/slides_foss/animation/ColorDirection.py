from __future__ import annotations
from enum import Enum

class ColorDirection(Enum):
    """Represents color direction for color effect behavior."""
    NOT_DEFINED = 'NotDefined'
    CLOCKWISE = 'Clockwise'
    COUNTER_CLOCKWISE = 'CounterClockwise'
