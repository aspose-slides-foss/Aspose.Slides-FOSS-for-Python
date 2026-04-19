from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from ..IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .IColorScheme import IColorScheme
    from .IFontScheme import IFontScheme
    from .IFormatScheme import IFormatScheme
    from ..IPresentation import IPresentation

class ITheme(IPresentationComponent, ABC):
    """Represents a theme."""
    @property
    @abstractmethod
    def color_scheme(self) -> IColorScheme:
        """Returns the color scheme. Read-only ."""
        ...

    @property
    @abstractmethod
    def font_scheme(self) -> IFontScheme:
        """Returns the font scheme. Read-only ."""
        ...

    @property
    @abstractmethod
    def format_scheme(self) -> IFormatScheme:
        """Returns the shape format scheme. Read-only ."""
        ...

    @property
    @abstractmethod
    def as_i_presentation_component(self) -> IPresentationComponent:
        """Allows to get base IPresentationComponent interface. Read-only ."""
        ...

    @property
    @abstractmethod
    def presentation(self) -> IPresentation:
        ...

