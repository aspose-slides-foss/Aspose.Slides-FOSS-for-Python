from __future__ import annotations
from enum import Enum

class TickMarkType(Enum):
    """Represents the tick mark type for the specified axis."""
    CROSS = 'Cross'  # Specifies the tick marks shall cross the axis.
    INSIDE = 'Inside'  # Specifies the tick marks shall be inside the plot area.
    NONE = 'None'  # Specifies there shall be no tick marks.
    OUTSIDE = 'Outside'  # Specifies the tick marks shall be outside the plot area.
