from __future__ import annotations
from enum import Enum

class EffectChartMajorGroupingType(Enum):
    """Represents the type of an animation effect for chart's element."""
    BY_SERIES = 'BySeries'  # Animate chart by series
    BY_CATEGORY = 'ByCategory'  # Animate chart by category
