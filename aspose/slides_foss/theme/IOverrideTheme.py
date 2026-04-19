from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ITheme import ITheme

if TYPE_CHECKING:
    from ..IPresentationComponent import IPresentationComponent
    from .IColorScheme import IColorScheme
    from .IFontScheme import IFontScheme
    from .IFormatScheme import IFormatScheme
    from ..IPresentation import IPresentation

class IOverrideTheme(ITheme, ABC):
    """Represents a overriding theme."""
    @property
    @abstractmethod
    def is_empty(self) -> bool:
        """True value means that ColorScheme, FontScheme, FormatScheme is null and any overriding with this theme object are disabled. Read-only ."""
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

    @abstractmethod
    def clear(self) -> None:
        ...

