from __future__ import annotations
from typing import overload, Optional, TYPE_CHECKING
from .BaseSlide import BaseSlide
from .IMasterSlide import IMasterSlide

if TYPE_CHECKING:
    from .IMasterLayoutSlideCollection import IMasterLayoutSlideCollection
    from .ISlide import ISlide
    from .theme.IMasterThemeManager import IMasterThemeManager
    from ._internal.pptx.master_slide_part import MasterSlidePart
    from ._internal.opc import OpcPackage

class MasterSlide(BaseSlide, IMasterSlide):
    """Represents a master slide in a presentation."""

    def _init_internal(self, presentation, package: OpcPackage,
                       part_name: str, master_part: MasterSlidePart,
                       layout_slides=None) -> None:
        """
        Internal initialization for a master slide.

        Args:
            presentation: The parent Presentation object.
            package: The OPC package.
            part_name: The part name of this master slide.
            master_part: The parsed MasterSlidePart.
            layout_slides: List of LayoutSlide objects belonging to this master.
        """
        super().__init__()
        self._presentation_ref = presentation
        self._package = package
        self._part_name = part_name
        self._master_part = master_part
        self._layout_slides_list = layout_slides or []





    @property
    def theme_manager(self) -> IMasterThemeManager:
        """Returns the theme manager. Read-only ."""
        if not hasattr(self, '_theme_manager_cache') or self._theme_manager_cache is None:
            from .theme.MasterThemeManager import MasterThemeManager
            mgr = MasterThemeManager()
            mgr._init_internal(
                self._presentation_ref.master_theme,
                self._presentation_ref,
            )
            self._theme_manager_cache = mgr
        return self._theme_manager_cache

    @property
    def layout_slides(self) -> IMasterLayoutSlideCollection:
        """Returns the collection of child layout slides for this master slide. Read-only ."""
        if hasattr(self, '_layout_slides_list') and self._layout_slides_list is not None:
            from .MasterLayoutSlideCollection import MasterLayoutSlideCollection
            collection = MasterLayoutSlideCollection()
            collection._init_internal(self._layout_slides_list)
            return collection
        return None










