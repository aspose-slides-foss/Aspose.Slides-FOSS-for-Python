from __future__ import annotations
from enum import Enum

class AxisPositionType(Enum):
    """Determines a position of axis."""
    BOTTOM = 'Bottom'  # Specifies that the axis shall be displayed at the bottom of the plot area.
    LEFT = 'Left'  # Specifies that the axis shall be displayed at the left of the plot area.
    RIGHT = 'Right'  # Specifies that the axis shall be displayed at the right of the plot area.
    TOP = 'Top'  # Specifies that the axis shall be displayed at the top of the plot area.
