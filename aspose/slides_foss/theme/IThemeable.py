from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from ..ISlideComponent import ISlideComponent
from ..IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from ..IBaseSlide import IBaseSlide
    from ..IPresentation import IPresentation

class IThemeable(ISlideComponent, IPresentationComponent, ABC):
    """Represents objects that can be themed with ."""
    @property
    @abstractmethod
    def as_i_slide_component(self) -> ISlideComponent:
        """Returns ISlideComponent interface. Read-only ."""
        ...

    @property
    @abstractmethod
    def slide(self) -> IBaseSlide:
        ...

    @property
    @abstractmethod
    def as_i_presentation_component(self) -> IPresentationComponent:
        ...

    @property
    @abstractmethod
    def presentation(self) -> IPresentation:
        ...

