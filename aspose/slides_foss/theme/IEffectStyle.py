from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..IEffectFormat import IEffectFormat
    from ..IThreeDFormat import IThreeDFormat

class IEffectStyle(ABC):
    """Represents an effect style."""
    @property
    @abstractmethod
    def effect_format(self) -> IEffectFormat:
        """Returns an effect format. Read-only ."""
        ...

    @property
    @abstractmethod
    def three_d_format(self) -> IThreeDFormat:
        """Returns an 3d format. Read-only ."""
        ...

