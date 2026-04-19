from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from ..ISlideComponent import ISlideComponent
from ..IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from ..IBaseSlide import IBaseSlide
    from .IEffectStyleCollection import IEffectStyleCollection
    from .IFillFormatCollection import IFillFormatCollection
    from .ILineFormatCollection import ILineFormatCollection
    from ..IPresentation import IPresentation

class IFormatScheme(ISlideComponent, IPresentationComponent, ABC):
    """Stores theme-defined formats for the shapes."""
    @property
    @abstractmethod
    def fill_styles(self) -> IFillFormatCollection:
        """Returns a collection of theme defined fill styles. Read-only ."""
        ...

    @property
    @abstractmethod
    def line_styles(self) -> ILineFormatCollection:
        """Returns a collection of theme defined line styles. Read-only ."""
        ...

    @property
    @abstractmethod
    def effect_styles(self) -> IEffectStyleCollection:
        """Returns a collection of theme defined effect styles. Read-only ."""
        ...

    @property
    @abstractmethod
    def background_fill_styles(self) -> IFillFormatCollection:
        """Returns a collection of theme defined background fill styles. Read-only ."""
        ...

    @property
    @abstractmethod
    def as_i_slide_component(self) -> ISlideComponent:
        """Allows to get base ISlideComponent interface. Read-only ."""
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

