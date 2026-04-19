from __future__ import annotations
from enum import Enum

class EffectChartMinorGroupingType(Enum):
    """Represents the type of an animation effect for chart's element in series or category."""
    BY_ELEMENT_IN_SERIES = 'ByElementInSeries'  # Animate chart by element in series
    BY_ELEMENT_IN_CATEGORY = 'ByElementInCategory'  # Animate chart by element in category
