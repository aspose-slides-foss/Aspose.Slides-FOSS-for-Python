from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .IOuterShadow import IOuterShadow
from .IImageTransformOperation import IImageTransformOperation
from .._internal.pptx.constants import EMU_PER_POINT

if TYPE_CHECKING:
    from ..IColorFormat import IColorFormat
    from .IOuterShadowEffectiveData import IOuterShadowEffectiveData
    from ..RectangleAlignment import RectangleAlignment
    from .._internal.pptx.slide_part import SlidePart

# OOXML alignment -> RectangleAlignment enum name
_ALGN_MAP = {
    'tl': 'TOP_LEFT', 't': 'TOP', 'tr': 'TOP_RIGHT',
    'l': 'LEFT', 'ctr': 'CENTER', 'r': 'RIGHT',
    'bl': 'BOTTOM_LEFT', 'b': 'BOTTOM', 'br': 'BOTTOM_RIGHT',
}
_ALGN_MAP_REV = {v: k for k, v in _ALGN_MAP.items()}


class OuterShadow(IOuterShadow, IImageTransformOperation):
    """Represents an Outer Shadow effect."""

    def _init_internal(self, element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        self._element = element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def blur_radius(self) -> float:
        """Blur radius, in points. Default value – 0 pt. Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        val = self._element.get('blurRad')
        if val is None:
            return 0.0
        return int(val) / EMU_PER_POINT

    @blur_radius.setter
    def blur_radius(self, value: float):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._element.set('blurRad', str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def direction(self) -> float:
        """Direction of the shadow, in degrees. Default value – 0 ° (left-to-right). Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        val = self._element.get('dir')
        if val is None:
            return 0.0
        return int(val) / 60000.0

    @direction.setter
    def direction(self, value: float):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._element.set('dir', str(int(round(value * 60000))))
        self._save()

    @property
    def distance(self) -> float:
        """Distance of the shadow from the object, in points. Default value – 0 pt. Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        val = self._element.get('dist')
        if val is None:
            return 0.0
        return int(val) / EMU_PER_POINT

    @distance.setter
    def distance(self, value: float):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._element.set('dist', str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def shadow_color(self) -> IColorFormat:
        """Color of the shadow. Default value – automatic black (theme-dependent). Read-only ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ..ColorFormat import ColorFormat
        cf = ColorFormat()
        cf._init_internal(self._element, self._slide_part, self._parent_slide)
        return cf

    @property
    def rectangle_align(self) -> RectangleAlignment:
        """Rectangle alignment. Default value – . Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ..RectangleAlignment import RectangleAlignment
        val = self._element.get('algn')
        if val is None:
            return RectangleAlignment.BOTTOM
        name = _ALGN_MAP.get(val)
        return RectangleAlignment[name] if name else RectangleAlignment.NOT_DEFINED

    @rectangle_align.setter
    def rectangle_align(self, value: RectangleAlignment):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ..RectangleAlignment import RectangleAlignment
        if value == RectangleAlignment.NOT_DEFINED:
            if 'algn' in self._element.attrib:
                del self._element.attrib['algn']
        else:
            ooxml_val = _ALGN_MAP_REV.get(value.name)
            if ooxml_val:
                self._element.set('algn', ooxml_val)
        self._save()

    @property
    def skew_horizontal(self) -> float:
        """Horizontal skew angle, in degrees. Default value – 0 °. Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        val = self._element.get('kx')
        if val is None:
            return 0.0
        return int(val) / 60000.0

    @skew_horizontal.setter
    def skew_horizontal(self, value: float):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._element.set('kx', str(int(round(value * 60000))))
        self._save()

    @property
    def skew_vertical(self) -> float:
        """Vertical skew angle, in degrees. Default value – 0 °. Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        val = self._element.get('ky')
        if val is None:
            return 0.0
        return int(val) / 60000.0

    @skew_vertical.setter
    def skew_vertical(self, value: float):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._element.set('ky', str(int(round(value * 60000))))
        self._save()

    @property
    def rotate_shadow_with_shape(self) -> bool:
        """Indicates whether the shadow rotates together with the shape. Default value – true. Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        val = self._element.get('rotWithShape')
        if val is None:
            return True
        return val == '1'

    @rotate_shadow_with_shape.setter
    def rotate_shadow_with_shape(self, value: bool):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._element.set('rotWithShape', '1' if value else '0')
        self._save()

    @property
    def scale_horizontal(self) -> float:
        """Horizontal scaling factor, in percent of the original size. Negative scaling causes a flip. Default value – 100 %. Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        val = self._element.get('sx')
        if val is None:
            return 100.0
        return int(val) / 1000.0

    @scale_horizontal.setter
    def scale_horizontal(self, value: float):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._element.set('sx', str(int(round(value * 1000))))
        self._save()

    @property
    def scale_vertical(self) -> float:
        """Vertical scaling factor, in percent of the original size. Negative scaling causes a flip. Default value – 100 %. Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        val = self._element.get('sy')
        if val is None:
            return 100.0
        return int(val) / 1000.0

    @scale_vertical.setter
    def scale_vertical(self, value: float):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._element.set('sy', str(int(round(value * 1000))))
        self._save()

    @property
    def as_i_image_transform_operation(self) -> IImageTransformOperation:
        return self

