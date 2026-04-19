from __future__ import annotations
from enum import Enum

class CategoryAxisType(Enum):
    """Represents a type of a category axis."""
    TEXT = 'Text'  # Specifies category axis is a text axis.
    DATE = 'Date'  # Specifies category axis is a date axis.
