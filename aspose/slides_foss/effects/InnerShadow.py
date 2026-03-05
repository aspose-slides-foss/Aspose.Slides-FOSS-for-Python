from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .IInnerShadow import IInnerShadow
from .IImageTransformOperation import IImageTransformOperation
from .._internal.pptx.constants import EMU_PER_POINT

if TYPE_CHECKING:
    from ..IColorFormat import IColorFormat
    from .._internal.pptx.slide_part import SlidePart

class InnerShadow(IInnerShadow, IImageTransformOperation):
    """Represents a Inner Shadow effect."""

    def _init_internal(self, element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        self._element = element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def blur_radius(self) -> float:
        """Blur radius. Read/write ."""
        val = self._element.get('blurRad')
        if val is None:
            return 0.0
        return int(val) / EMU_PER_POINT

    @blur_radius.setter
    def blur_radius(self, value: float):
        self._element.set('blurRad', str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def direction(self) -> float:
        """Direction of shadow. Read/write ."""
        val = self._element.get('dir')
        if val is None:
            return 0.0
        return int(val) / 60000.0

    @direction.setter
    def direction(self, value: float):
        self._element.set('dir', str(int(round(value * 60000))))
        self._save()

    @property
    def distance(self) -> float:
        """Distance of shadow. Read/write ."""
        val = self._element.get('dist')
        if val is None:
            return 0.0
        return int(val) / EMU_PER_POINT

    @distance.setter
    def distance(self, value: float):
        self._element.set('dist', str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def shadow_color(self) -> IColorFormat:
        """Color of shadow. Read-only ."""
        from ..ColorFormat import ColorFormat
        cf = ColorFormat()
        cf._init_internal(self._element, self._slide_part, self._parent_slide)
        return cf

    @property
    def as_i_image_transform_operation(self) -> IImageTransformOperation:
        return self

