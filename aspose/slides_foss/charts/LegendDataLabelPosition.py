from __future__ import annotations
from enum import Enum


class LegendDataLabelPosition(Enum):
    """Determines position of data labels."""
    NOT_DEFINED = 'NotDefined'
    BOTTOM = 'Bottom'
    BEST_FIT = 'BestFit'
    CENTER = 'Center'
    INSIDE_BASE = 'InsideBase'
    INSIDE_END = 'InsideEnd'
    LEFT = 'Left'
    OUTSIDE_END = 'OutsideEnd'
    RIGHT = 'Right'
    TOP = 'Top'
