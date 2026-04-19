from __future__ import annotations
from enum import Enum

class TickLabelPositionType(Enum):
    """Represents the position type of tick-mark labels on the specified axis."""
    HIGH = 'High'  # Specifies the axis labels shall be at the high end of the perpendicular axis.
    LOW = 'Low'  # Specifies the axis labels shall be at the low end of the perpendicular axis.
    NEXT_TO = 'NextTo'  # Specifies the axis labels shall be next to the axis.
    NONE = 'None'  # Specifies the axis labels are not drawn.
