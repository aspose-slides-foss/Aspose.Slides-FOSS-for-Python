from __future__ import annotations
from enum import Enum

class AfterAnimationType(Enum):
    """Represents the after animation type of an animation effect."""
    DO_NOT_DIM = 'DoNotDim'  # Don't Dim after animation type.
    COLOR = 'Color'  # Color after animation type.
    HIDE_AFTER_ANIMATION = 'HideAfterAnimation'  # Hide After Animation type
    HIDE_ON_NEXT_MOUSE_CLICK = 'HideOnNextMouseClick'  # Hide on Next Mouse Click after animation type.
