from __future__ import annotations
from enum import Enum

class ColorType(Enum):
    """Represents different color modes."""
    NOT_DEFINED = 'NotDefined'  # Color is not defined at all.
    RGB = 'RGB'  # Standard 24bit RGB color.
    RGB_PERCENTAGE = 'RGBPercentage'  # High definition RGB color.
    HSL = 'HSL'  # High definition HSL color.
    SCHEME = 'Scheme'  # Scheme color.
    SYSTEM = 'System'  # System color.
    PRESET = 'Preset'  # Preset Color.
