from __future__ import annotations
from enum import Enum

class FillBlendMode(Enum):
    """Determines blend mode."""
    DARKEN = 'Darken'  # Darken blend mode.
    LIGHTEN = 'Lighten'  # Lighten blend mode.
    MULTIPLY = 'Multiply'  # Multiply blend mode.
    OVERLAY = 'Overlay'  # Overlay blend mode.
    SCREEN = 'Screen'  # Screen blend mode.
