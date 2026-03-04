from __future__ import annotations
from typing import overload, Optional, TYPE_CHECKING
from .BaseSlide import BaseSlide
from .IMasterSlide import IMasterSlide

if TYPE_CHECKING:
    from .IDrawingGuidesCollection import IDrawingGuidesCollection
    from .IMasterLayoutSlideCollection import IMasterLayoutSlideCollection
    from .IMasterSlideHeaderFooterManager import IMasterSlideHeaderFooterManager
    from .theme.IMasterThemeManager import IMasterThemeManager
    from .ISlide import ISlide
    from .ITextStyle import ITextStyle
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
    def layout_slides(self) -> IMasterLayoutSlideCollection:
        """Returns the collection of child layout slides for this master slide. Read-only ."""
        if hasattr(self, '_layout_slides_list') and self._layout_slides_list is not None:
            from .MasterLayoutSlideCollection import MasterLayoutSlideCollection
            collection = MasterLayoutSlideCollection()
            collection._init_internal(self._layout_slides_list)
            return collection
        raise NotImplementedError("This feature is not yet available in this version.")










