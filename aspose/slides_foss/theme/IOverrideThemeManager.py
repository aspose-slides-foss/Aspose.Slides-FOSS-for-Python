from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IThemeManager import IThemeManager

if TYPE_CHECKING:
    from .IOverrideTheme import IOverrideTheme

class IOverrideThemeManager(IThemeManager, ABC):
    """Provides access to different types of overriden themes."""
    @property
    @abstractmethod
    def is_override_theme_enabled(self) -> bool:
        """Determines whether OverrideTheme overrides inherited effective theme or not. To enable OverrideTheme for overriding use OverrideTheme.Init*() methods. To disable OverrideTheme from overriding use OverrideTheme.Clear() method. Read-only ."""
        ...

    @property
    @abstractmethod
    def override_theme(self) -> IOverrideTheme:
        """Returns the overriding theme object. Read/write ."""
        ...

    @override_theme.setter
    @abstractmethod
    def override_theme(self, value: IOverrideTheme):
        ...

    @property
    @abstractmethod
    def as_i_theme_manager(self) -> IThemeManager:
        """Allows to get base IThemeManager interface. Read-only ."""
        ...

