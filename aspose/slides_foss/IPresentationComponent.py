from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IPresentation import IPresentation

class IPresentationComponent(ABC):
    """Represents a component of a presentation."""
    @property
    def presentation(self) -> IPresentation:
        """Returns the presentation. Read-only ."""
        ...
