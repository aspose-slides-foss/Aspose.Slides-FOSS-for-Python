from __future__ import annotations
from typing import TYPE_CHECKING
from .BaseOverrideThemeManager import BaseOverrideThemeManager
from .IOverrideThemeManager import IOverrideThemeManager
from .IThemeManager import IThemeManager

if TYPE_CHECKING:
    from .IOverrideTheme import IOverrideTheme


class SlideThemeManager(BaseOverrideThemeManager, IOverrideThemeManager, IThemeManager):
    """Provides access to slide theme overriden."""
