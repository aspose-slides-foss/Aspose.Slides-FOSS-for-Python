from __future__ import annotations
from enum import Enum

class MotionPathEditMode(Enum):
    """Specifies how the motion path moves when the target shape is moved"""
    NOT_DEFINED = 'NotDefined'
    RELATIVE = 'Relative'
    FIXED = 'Fixed'
