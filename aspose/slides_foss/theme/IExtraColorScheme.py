from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IColorScheme import IColorScheme

class IExtraColorScheme(ABC):
    """Represents an additional color scheme which can be assigned to a slide."""
    @property
    @abstractmethod
    def name(self) -> str:
        """Returns a name of this scheme. Read-only ."""
        ...

    @property
    @abstractmethod
    def color_scheme(self) -> IColorScheme:
        """Returns a color scheme. Read-only ."""
        ...

