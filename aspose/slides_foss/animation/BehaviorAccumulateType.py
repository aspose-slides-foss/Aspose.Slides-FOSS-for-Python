from __future__ import annotations
from enum import Enum

class BehaviorAccumulateType(Enum):
    """Represents types of accumulation of effect behaviors."""
    NOT_DEFINED = 'NotDefined'
    ALWAYS = 'Always'
    NONE = 'None'
