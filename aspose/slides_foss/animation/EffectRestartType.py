from __future__ import annotations
from enum import Enum

class EffectRestartType(Enum):
    """Represent restart types for timing."""
    NOT_DEFINED = 'NotDefined'
    ALWAYS = 'Always'
    WHEN_NOT_ACTIVE = 'WhenNotActive'
    NEVER = 'Never'
