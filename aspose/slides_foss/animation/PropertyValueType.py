from __future__ import annotations
from enum import Enum

class PropertyValueType(Enum):
    """Represent property value types."""
    NOT_DEFINED = 'NotDefined'
    STRING = 'String'
    NUMBER = 'Number'
    COLOR = 'Color'
