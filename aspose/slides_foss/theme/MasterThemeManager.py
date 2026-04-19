from __future__ import annotations
from typing import TYPE_CHECKING
from .BaseThemeManager import BaseThemeManager
from .IMasterThemeManager import IMasterThemeManager
from .IThemeManager import IThemeManager

if TYPE_CHECKING:
    from .IMasterTheme import IMasterTheme


class MasterThemeManager(BaseThemeManager, IMasterThemeManager, IThemeManager):
    """Provides access to presentation master theme."""

    def _init_internal(self, master_theme, presentation) -> None:
        self._master_theme = master_theme
        self._presentation_ref = presentation
        self._override_theme = None
        self._is_override_enabled = False

    @property
    def override_theme(self) -> IMasterTheme:
        """Returns the overriding theme object. Read/write ."""
        return self._override_theme

    @override_theme.setter
    def override_theme(self, value: IMasterTheme):
        self._override_theme = value

    @property
    def is_override_theme_enabled(self) -> bool:
        """Determines whether OverrideTheme overrides inherited effective theme. Read/write ."""
        return self._is_override_enabled

    @is_override_theme_enabled.setter
    def is_override_theme_enabled(self, value: bool):
        self._is_override_enabled = value

    @property
    def as_i_theme_manager(self) -> IThemeManager:
        return self
