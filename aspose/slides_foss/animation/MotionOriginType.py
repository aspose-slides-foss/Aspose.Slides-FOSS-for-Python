from __future__ import annotations
from enum import Enum

class MotionOriginType(Enum):
    """Specifies what the origin of the motion path is relative to. Such as the layout of the slide, or the parent."""
    NOT_DEFINED = 'NotDefined'
    PARENT = 'Parent'
    LAYOUT = 'Layout'
