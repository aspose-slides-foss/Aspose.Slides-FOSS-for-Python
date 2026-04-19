from __future__ import annotations
from typing import TYPE_CHECKING
from .BaseThemeManager import BaseThemeManager
from .IOverrideThemeManager import IOverrideThemeManager
from .IThemeManager import IThemeManager

if TYPE_CHECKING:
    from .IOverrideTheme import IOverrideTheme


class BaseOverrideThemeManager(BaseThemeManager, IOverrideThemeManager, IThemeManager):
    """Base class for classes that provide access to different types of overriden themes."""

    def _init_internal(self) -> None:
        self._override_theme_obj = None

    @property
    def override_theme(self) -> IOverrideTheme:
        """Returns the overriding theme object. Read/write ."""
        if self._override_theme_obj is None:
            from .OverrideTheme import OverrideTheme
            self._override_theme_obj = OverrideTheme()
            self._override_theme_obj._init_internal()
        return self._override_theme_obj

    @override_theme.setter
    def override_theme(self, value: IOverrideTheme):
        self._override_theme_obj = value

    @property
    def is_override_theme_enabled(self) -> bool:
        """Determines whether OverrideTheme overrides inherited effective theme. Read-only ."""
        if self._override_theme_obj is not None:
            return not self._override_theme_obj.is_empty
        return False

    @property
    def as_i_theme_manager(self) -> IThemeManager:
        return self
