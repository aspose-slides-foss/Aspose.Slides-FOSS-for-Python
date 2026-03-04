from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .IReflection import IReflection
from .IImageTransformOperation import IImageTransformOperation
from .._internal.pptx.constants import EMU_PER_POINT

if TYPE_CHECKING:
    from .IReflectionEffectiveData import IReflectionEffectiveData
    from ..RectangleAlignment import RectangleAlignment
    from .._internal.pptx.slide_part import SlidePart

# OOXML alignment -> RectangleAlignment enum name
_ALGN_MAP = {
    'tl': 'TOP_LEFT', 't': 'TOP', 'tr': 'TOP_RIGHT',
    'l': 'LEFT', 'ctr': 'CENTER', 'r': 'RIGHT',
    'bl': 'BOTTOM_LEFT', 'b': 'BOTTOM', 'br': 'BOTTOM_RIGHT',
}
_ALGN_MAP_REV = {v: k for k, v in _ALGN_MAP.items()}


class Reflection(IReflection, IImageTransformOperation):
    """Represents a Reflection effect."""

    def _init_internal(self, element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        self._element = element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def start_pos_alpha(self) -> float:
        """Specifies the start position (along the alpha gradient ramp) of the start alpha value (percents). Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        val = self._element.get('stPos')
        if val is None:
            return 0.0
        return int(val) / 1000.0

    @start_pos_alpha.setter
    def start_pos_alpha(self, value: float):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._element.set('stPos', str(int(round(value * 1000))))
        self._save()

    @property
    def end_pos_alpha(self) -> float:
        """Specifies the end position (along the alpha gradient ramp) of the end alpha value (percents). Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        val = self._element.get('endPos')
        if val is None:
            return 100.0
        return int(val) / 1000.0

    @end_pos_alpha.setter
    def end_pos_alpha(self, value: float):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._element.set('endPos', str(int(round(value * 1000))))
        self._save()

    @property
    def fade_direction(self) -> float:
        """Specifies the direction to offset the reflection. (angle). Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        val = self._element.get('fadeDir')
        if val is None:
            return 90.0
        return int(val) / 60000.0

    @fade_direction.setter
    def fade_direction(self, value: float):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._element.set('fadeDir', str(int(round(value * 60000))))
        self._save()

    @property
    def start_reflection_opacity(self) -> float:
        """Starting reflection opacity. (percents). Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        val = self._element.get('stA')
        if val is None:
            return 100.0
        return int(val) / 1000.0

    @start_reflection_opacity.setter
    def start_reflection_opacity(self, value: float):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._element.set('stA', str(int(round(value * 1000))))
        self._save()

    @property
    def end_reflection_opacity(self) -> float:
        """End reflection opacity. (percents). Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        val = self._element.get('endA')
        if val is None:
            return 0.0
        return int(val) / 1000.0

    @end_reflection_opacity.setter
    def end_reflection_opacity(self, value: float):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._element.set('endA', str(int(round(value * 1000))))
        self._save()

    @property
    def blur_radius(self) -> float:
        """Blur radius. Read/write ."""
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
        """Direction of reflection. Read/write ."""
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
        """Distance of reflection. Read/write ."""
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
    def rectangle_align(self) -> RectangleAlignment:
        """Rectangle alignment. Read/write ."""
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
        """Specifies the horizontal skew angle. Read/write ."""
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
        """Specifies the vertical skew angle. Read/write ."""
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
        """Specifies whether the reflection should rotate with the shape if the shape is rotated. Read/write ."""
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
        """Specifies the horizontal scaling factor, negative scaling causes a flip. (percents) Read/write ."""
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
        """Specifies the vertical scaling factor, negative scaling causes a flip. (percents) Read/write ."""
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

