from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from ..ISlideComponent import ISlideComponent
from ..IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from ..IBaseSlide import IBaseSlide
    from ..IColorFormat import IColorFormat
    from ..IPresentation import IPresentation

class IColorScheme(ISlideComponent, IPresentationComponent, ABC):
    """Stores theme-defined colors."""
    @property
    @abstractmethod
    def dark1(self) -> IColorFormat:
        """First dark color in the scheme. Read-only ."""
        ...

    @property
    @abstractmethod
    def light1(self) -> IColorFormat:
        """First light color in the scheme. Read-only ."""
        ...

    @property
    @abstractmethod
    def dark2(self) -> IColorFormat:
        """Second dark color in the scheme. Read-only ."""
        ...

    @property
    @abstractmethod
    def light2(self) -> IColorFormat:
        """Second light color in the scheme. Read-only ."""
        ...

    @property
    @abstractmethod
    def accent1(self) -> IColorFormat:
        """First accent color in the scheme. Read-only ."""
        ...

    @property
    @abstractmethod
    def accent2(self) -> IColorFormat:
        """Second accent color in the scheme. Read-only ."""
        ...

    @property
    @abstractmethod
    def accent3(self) -> IColorFormat:
        """Third accent color in the scheme. Read-only ."""
        ...

    @property
    @abstractmethod
    def accent4(self) -> IColorFormat:
        """Fourth accent color in the scheme. Read-only ."""
        ...

    @property
    @abstractmethod
    def accent5(self) -> IColorFormat:
        """Fifth accent color in the scheme. Read-only ."""
        ...

    @property
    @abstractmethod
    def accent6(self) -> IColorFormat:
        """Sixth accent color in the scheme. Read-only ."""
        ...

    @property
    @abstractmethod
    def hyperlink(self) -> IColorFormat:
        """Color for the hyperlinks. Read-only ."""
        ...

    @property
    @abstractmethod
    def followed_hyperlink(self) -> IColorFormat:
        """Color for the visited hyperlinks. Read-only ."""
        ...

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

