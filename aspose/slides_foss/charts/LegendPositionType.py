from __future__ import annotations
from enum import Enum


class LegendPositionType(Enum):
    """Determines a position of legend on a chart."""
    BOTTOM = 'Bottom'
    LEFT = 'Left'
    RIGHT = 'Right'
    TOP = 'Top'
    TOP_RIGHT = 'TopRight'
