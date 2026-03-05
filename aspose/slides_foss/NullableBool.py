from __future__ import annotations
from enum import Enum

class NullableBool(Enum):
    """Represents triple boolean values."""
    NOT_DEFINED = 'NotDefined'  # Boolean value is undefined.
    FALSE = 'False'  # False value.
    TRUE = 'True'  # True value.
