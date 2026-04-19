from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IThemeable import IThemeable
from ..ISlideComponent import ISlideComponent
from ..IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from ..IBaseSlide import IBaseSlide
    from .IOverrideThemeManager import IOverrideThemeManager
    from ..IPresentation import IPresentation

class IOverrideThemeable(IThemeable, ISlideComponent, IPresentationComponent, ABC):
    """Represents override theme manager."""
    @property
    @abstractmethod
    def theme_manager(self) -> IOverrideThemeManager:
        """Returns override theme manager. Read-only ."""
        ...

    @property
    @abstractmethod
    def as_i_themeable(self) -> IThemeable:
        """Returns IThemeable interface. Read-only ."""
        ...

    @property
    @abstractmethod
    def as_i_slide_component(self) -> ISlideComponent:
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

