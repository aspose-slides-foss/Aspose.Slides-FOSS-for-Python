from __future__ import annotations
from enum import Enum

class EffectTriggerType(Enum):
    """Represent trigger type of effect."""
    AFTER_PREVIOUS = 'AfterPrevious'
    ON_CLICK = 'OnClick'
    WITH_PREVIOUS = 'WithPrevious'
