from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .ISoftEdge import ISoftEdge
from .IImageTransformOperation import IImageTransformOperation
from .._internal.pptx.constants import EMU_PER_POINT

if TYPE_CHECKING:
    from .._internal.pptx.slide_part import SlidePart

class SoftEdge(ISoftEdge, IImageTransformOperation):
    """Represents a soft edge effect. The edges of the shape are blurred, while the fill is not affected."""

    def _init_internal(self, element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        self._element = element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def radius(self) -> float:
        """Specifies the radius of blur to apply to the edges. Read/write ."""
        val = self._element.get('rad')
        if val is None:
            return 0.0
        return int(val) / EMU_PER_POINT

    @radius.setter
    def radius(self, value: float):
        self._element.set('rad', str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def as_i_image_transform_operation(self) -> IImageTransformOperation:
        return self

