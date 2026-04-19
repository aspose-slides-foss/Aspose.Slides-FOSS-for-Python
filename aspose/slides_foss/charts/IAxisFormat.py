from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..IEffectFormat import IEffectFormat
    from ..IFillFormat import IFillFormat
    from ..ILineFormat import ILineFormat

class IAxisFormat(ABC):
    """Represents chart format properties."""
    @property
    def fill(self) -> IFillFormat:
        """Returns fill style properties of an axis. Read-only ."""
        ...

    @property
    def line(self) -> ILineFormat:
        """Returns line style properties of an axis. Read-only ."""
        ...

    @property
    def effect(self) -> IEffectFormat:
        """Returns effects used for an axis. Read-only ."""
        ...

