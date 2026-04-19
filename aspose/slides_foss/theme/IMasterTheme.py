from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ITheme import ITheme

if TYPE_CHECKING:
    from ..IPresentationComponent import IPresentationComponent
    from .IColorScheme import IColorScheme
    from .IExtraColorSchemeCollection import IExtraColorSchemeCollection
    from .IFontScheme import IFontScheme
    from .IFormatScheme import IFormatScheme
    from ..IPresentation import IPresentation

class IMasterTheme(ITheme, ABC):
    """Represents a master theme."""
    @property
    @abstractmethod
    def extra_color_schemes(self) -> IExtraColorSchemeCollection:
        """Returns the collection of additional color schemes. These schemes don't affect presentation's look, they can be selected as main color scheme for a slide. Read-only ."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the name of a theme. Read/write ."""
        ...

    @name.setter
    @abstractmethod
    def name(self, value: str):
        ...

    @property
    @abstractmethod
    def as_i_theme(self) -> ITheme:
        """Allows to get base ITheme interface. Read-only ."""
        ...

    @property
    @abstractmethod
    def color_scheme(self) -> IColorScheme:
        ...

    @property
    @abstractmethod
    def font_scheme(self) -> IFontScheme:
        ...

    @property
    @abstractmethod
    def format_scheme(self) -> IFormatScheme:
        ...

    @property
    @abstractmethod
    def as_i_presentation_component(self) -> IPresentationComponent:
        ...

    @property
    @abstractmethod
    def presentation(self) -> IPresentation:
        ...

