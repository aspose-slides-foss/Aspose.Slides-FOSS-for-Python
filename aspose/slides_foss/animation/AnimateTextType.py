from __future__ import annotations
from enum import Enum

class AnimateTextType(Enum):
    """Represents the animate text type of an animation effect."""
    ALL_AT_ONCE = 'AllAtOnce'  # Animate all text at once.
    BY_WORD = 'ByWord'  # Animate text by word.
    BY_LETTER = 'ByLetter'  # Animate text by letter.
