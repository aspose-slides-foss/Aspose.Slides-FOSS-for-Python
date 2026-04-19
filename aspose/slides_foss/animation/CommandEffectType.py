from __future__ import annotations
from enum import Enum

class CommandEffectType(Enum):
    """Represents command effect type for command effect behavior."""
    NOT_DEFINED = 'NotDefined'
    EVENT = 'Event'
    CALL = 'Call'
    VERB = 'Verb'
