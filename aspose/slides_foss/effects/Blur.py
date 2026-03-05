from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .ImageTransformOperation import ImageTransformOperation
from ..ISlideComponent import ISlideComponent
from ..IPresentationComponent import IPresentationComponent
from .IImageTransformOperation import IImageTransformOperation
from .IBlur import IBlur
from .._internal.pptx.constants import EMU_PER_POINT

if TYPE_CHECKING:
    from ..IBaseSlide import IBaseSlide
    from ..IPresentation import IPresentation
    from .._internal.pptx.slide_part import SlidePart

class Blur(ImageTransformOperation, ISlideComponent, IPresentationComponent, IBlur, IImageTransformOperation):
    """Represents a Blur effect that is applied to the entire shape, including its fill. All color channels, including alpha, are affected."""

    def _init_internal(self, element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        self._element = element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        return self

    @property
    def radius(self) -> float:
        """Returns or sets blur radius. Read/write ."""
        val = self._element.get('rad')
        if val is None:
            return 0.0
        return int(val) / EMU_PER_POINT

    @radius.setter
    def radius(self, value: float):
        self._element.set('rad', str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def grow(self) -> bool:
        """Determines whether the bounds of the object should be grown as a result of the blurring. True indicates the bounds are grown while false indicates that they are not. Read/write ."""
        val = self._element.get('grow')
        if val is None:
            return True  # default
        return val == '1'

    @grow.setter
    def grow(self, value: bool):
        self._element.set('grow', '1' if value else '0')
        self._save()

    @property
    def slide(self) -> IBaseSlide:
        return getattr(self, '_parent_slide', None)


    @property
    def as_i_image_transform_operation(self) -> IImageTransformOperation:
        return self

