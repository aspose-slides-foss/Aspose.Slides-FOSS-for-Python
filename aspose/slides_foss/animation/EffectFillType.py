from __future__ import annotations
from enum import Enum

class EffectFillType(Enum):
    """Represent fill types."""
    NOT_DEFINED = 'NotDefined'
    REMOVE = 'Remove'
    FREEZE = 'Freeze'
    HOLD = 'Hold'
    TRANSITION = 'Transition'
