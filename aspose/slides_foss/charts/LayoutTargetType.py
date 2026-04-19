from __future__ import annotations
from enum import Enum


class LayoutTargetType(Enum):
    """If layout of the plot area defined manually this property specifies whether
    to layout the plot area by its inside (not including axis and axis labels) or
    outside (including axis and axis labels)."""
    INNER = 'Inner'
    OUTER = 'Outer'
