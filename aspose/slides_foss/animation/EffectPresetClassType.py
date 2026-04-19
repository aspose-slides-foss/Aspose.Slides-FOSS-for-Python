from __future__ import annotations
from enum import Enum

class EffectPresetClassType(Enum):
    """Represent effect class types."""
    ENTRANCE = 'Entrance'  # Entrance effects class.Target shape types: All
    EXIT = 'Exit'  # Exit effects class.Target shape types: All
    EMPHASIS = 'Emphasis'  # Emphasis effects class.Target shape types: All
    PATH = 'Path'  # Motion Paths class.Target shape types: All
    MEDIA_CALL = 'MediaCall'  # Media effects class.Target shape types: ,
    OLE_ACTION_VERBS = 'OLEActionVerbs'  # OLE Action Verbs class.Target shape types:
