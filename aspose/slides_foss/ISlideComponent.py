from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .IBaseSlide import IBaseSlide

class ISlideComponent(IPresentationComponent, ABC):
    """Represents a component of a slide."""
    @property
    def slide(self) -> IBaseSlide:
        """Returns the base slide. Read-only ."""
        ...

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        """Allows to get base IPresentationComponent interface. Read-only ."""
        ...
