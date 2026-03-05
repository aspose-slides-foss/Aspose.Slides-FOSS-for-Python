from __future__ import annotations
from enum import Enum

class TextAutofitType(Enum):
    """Represents text autofit mode."""
    NOT_DEFINED = 'NotDefined'  # Not defined.
    NONE = 'None'  # No autofit.
    NORMAL = 'Normal'  # Normal autofit. Font size and line spacing will be reduced to fit the shape.
    SHAPE = 'Shape'  # Shape autofit. Shape size will be changed to fit the text.
