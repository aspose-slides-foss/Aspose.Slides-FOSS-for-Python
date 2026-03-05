from __future__ import annotations
from typing import overload, Optional, TYPE_CHECKING
from .BaseSlide import BaseSlide
from .ILayoutSlide import ILayoutSlide

if TYPE_CHECKING:
    from .IMasterSlide import IMasterSlide
    from .ISlide import ISlide
    from .SlideLayoutType import SlideLayoutType
    from ._internal.pptx.layout_slide_part import LayoutSlidePart
    from ._internal.opc import OpcPackage

class LayoutSlide(BaseSlide, ILayoutSlide):
    """Represents a layout slide."""

    def _init_internal(self, presentation, package: OpcPackage,
                       part_name: str, layout_part: LayoutSlidePart,
                       master_resolver=None) -> None:
        """
        Internal initialization for a layout slide.

        Args:
            presentation: The parent Presentation object.
            package: The OPC package.
            part_name: The part name of this layout slide.
            layout_part: The parsed LayoutSlidePart.
            master_resolver: Callable that resolves a master part name to a MasterSlide.
        """
        super().__init__()
        self._presentation_ref = presentation
        self._package = package
        self._part_name = part_name
        self._layout_part = layout_part
        self._master_resolver = master_resolver
        self._master_slide_cache: Optional[IMasterSlide] = None



    @property
    def master_slide(self) -> IMasterSlide:
        """Returns or sets the master slide for a layout. Read/write ."""
        if hasattr(self, '_master_resolver') and self._master_resolver is not None:
            if self._master_slide_cache is None:
                master_part_name = self._layout_part.master_part_name
                if master_part_name:
                    self._master_slide_cache = self._master_resolver(master_part_name)
            if self._master_slide_cache is not None:
                return self._master_slide_cache
        return None



    @property
    def layout_type(self) -> SlideLayoutType:
        """Returns layout type of this layout slide. Read-only ."""
        if hasattr(self, '_layout_part') and self._layout_part is not None:
            from .SlideLayoutType import SlideLayoutType as SLT
            type_value = self._layout_part.layout_type_value
            try:
                return SLT(type_value)
            except ValueError:
                return SLT.CUSTOM
        return None







