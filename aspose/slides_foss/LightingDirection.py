from __future__ import annotations
from enum import Enum

class LightingDirection(Enum):
    """Constants which define light directions."""
    NOT_DEFINED = 'NotDefined'
    TOP_LEFT = 'TopLeft'
    TOP = 'Top'
    TOP_RIGHT = 'TopRight'
    RIGHT = 'Right'
    BOTTOM_RIGHT = 'BottomRight'
    BOTTOM = 'Bottom'
    BOTTOM_LEFT = 'BottomLeft'
    LEFT = 'Left'
