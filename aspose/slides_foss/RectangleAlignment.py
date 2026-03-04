from __future__ import annotations
from enum import Enum

class RectangleAlignment(Enum):
    """Defines 2-dimension allignment."""
    NOT_DEFINED = 'NotDefined'
    TOP_LEFT = 'TopLeft'
    TOP = 'Top'
    TOP_RIGHT = 'TopRight'
    LEFT = 'Left'
    CENTER = 'Center'
    RIGHT = 'Right'
    BOTTOM_LEFT = 'BottomLeft'
    BOTTOM = 'Bottom'
    BOTTOM_RIGHT = 'BottomRight'
