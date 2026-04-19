from __future__ import annotations
from enum import Enum
class TransitionMorphType(Enum):
    """Represent a type of morph transition."""
    BY_OBJECT = 'ByObject'  # Morph transition will be performed considering shapes as indivisible objects.
    BY_WORD = 'ByWord'  # Morph transition will be performed with transferring text by words where possible.
    BY_CHAR = 'ByChar'  # Morph transition will be performed with transferring text by characters where possible.
