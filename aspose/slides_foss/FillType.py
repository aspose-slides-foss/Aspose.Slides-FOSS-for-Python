from __future__ import annotations
from enum import Enum

class FillType(Enum):
    """Specifies the interior fill type of various visual objects."""
    NOT_DEFINED = 'NotDefined'  # The fill type is not defined.
    NO_FILL = 'NoFill'  # No fill applied.
    SOLID = 'Solid'  # Filled with a solid color.
    GRADIENT = 'Gradient'  # The fill is gradient.
    PATTERN = 'Pattern'  # Repeating pattern is used to fill the object.
    PICTURE = 'Picture'  # A single picture is used to fill the object.
    GROUP = 'Group'  # The visual object inherits the fill properties from the group.
