from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IThemeManager import IThemeManager

if TYPE_CHECKING:
    from .IMasterTheme import IMasterTheme

class IMasterThemeManager(IThemeManager, ABC):
    """Provides access to presentation master theme."""
    @property
    @abstractmethod
    def is_override_theme_enabled(self) -> bool:
        """Determines whether OverrideTheme overrides inherited effective theme (Presentation.MasterTheme) or not. Read/write ."""
        ...

    @is_override_theme_enabled.setter
    @abstractmethod
    def is_override_theme_enabled(self, value: bool):
        ...

    @property
    @abstractmethod
    def override_theme(self) -> IMasterTheme:
        """Returns the overriding theme object. Read/write ."""
        ...

    @override_theme.setter
    @abstractmethod
    def override_theme(self, value: IMasterTheme):
        ...

    @property
    @abstractmethod
    def as_i_theme_manager(self) -> IThemeManager:
        """Allows to get base IThemeManager interface. Read-only ."""
        ...

