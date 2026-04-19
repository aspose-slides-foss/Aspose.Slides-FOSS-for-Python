from __future__ import annotations
from enum import Enum

class BubbleSizeRepresentationType(Enum):
    """Specifies the possible ways to represent data as bubble chart sizes."""
    AREA = 'Area'  # Specifies the area of the bubbles shall be proportional to the bubble size value.
    WIDTH = 'Width'  # Specifies the radius of the bubbles shall be proportional to the bubble size value.
