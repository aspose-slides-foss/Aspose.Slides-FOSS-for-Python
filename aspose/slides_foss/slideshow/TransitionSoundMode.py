from __future__ import annotations
from enum import Enum
class TransitionSoundMode(Enum):
    """Represent sound mode of transition."""
    NOT_DEFINED = 'NotDefined'
    START_SOUND = 'StartSound'
    STOP_PREVOIUS_SOUND = 'StopPrevoiusSound'
