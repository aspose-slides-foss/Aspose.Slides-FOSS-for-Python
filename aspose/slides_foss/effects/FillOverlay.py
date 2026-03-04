from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .ImageTransformOperation import ImageTransformOperation
from ..ISlideComponent import ISlideComponent
from ..IPresentationComponent import IPresentationComponent
from .IImageTransformOperation import IImageTransformOperation
from .IFillOverlay import IFillOverlay

if TYPE_CHECKING:
    from ..FillBlendMode import FillBlendMode
    from ..IBaseSlide import IBaseSlide
    from ..IFillFormat import IFillFormat
    from .IFillOverlayEffectiveData import IFillOverlayEffectiveData
    from ..IPresentation import IPresentation
    from .._internal.pptx.slide_part import SlidePart

# OOXML blend mode -> FillBlendMode enum name
_BLEND_MAP = {
    'over': 'OVERLAY', 'mult': 'MULTIPLY', 'screen': 'SCREEN',
    'darken': 'DARKEN', 'lighten': 'LIGHTEN',
}
_BLEND_MAP_REV = {v: k for k, v in _BLEND_MAP.items()}


class FillOverlay(ImageTransformOperation, ISlideComponent, IPresentationComponent, IFillOverlay, IImageTransformOperation):
    """Represents a Fill Overlay effect. A fill overlay may be used to specify an additional fill for an object and blend the two fills together."""

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
    def fill_format(self) -> IFillFormat:
        """Fill format. Read-only ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ..FillFormat import FillFormat
        ff = FillFormat()
        ff._init_internal(self._element, self._slide_part, self._parent_slide)
        return ff

    @property
    def blend(self) -> FillBlendMode:
        """FillBlendMode. Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ..FillBlendMode import FillBlendMode
        val = self._element.get('blend')
        if val is None:
            return FillBlendMode.OVERLAY
        name = _BLEND_MAP.get(val)
        return FillBlendMode[name] if name else FillBlendMode.OVERLAY

    @blend.setter
    def blend(self, value: FillBlendMode):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        ooxml_val = _BLEND_MAP_REV.get(value.name)
        if ooxml_val:
            self._element.set('blend', ooxml_val)
        self._save()

    @property
    def slide(self) -> IBaseSlide:
        if hasattr(self, '_parent_slide'):
            return self._parent_slide
        raise NotImplementedError("This feature is not yet available in this version.")


    @property
    def as_i_image_transform_operation(self) -> IImageTransformOperation:
        return self

