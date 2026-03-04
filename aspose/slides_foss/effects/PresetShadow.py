from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .IPresetShadow import IPresetShadow
from .IImageTransformOperation import IImageTransformOperation
from .._internal.pptx.constants import EMU_PER_POINT

if TYPE_CHECKING:
    from ..IColorFormat import IColorFormat
    from .IPresetShadowEffectiveData import IPresetShadowEffectiveData
    from ..PresetShadowType import PresetShadowType
    from .._internal.pptx.slide_part import SlidePart

# OOXML preset shadow value -> PresetShadowType enum name
_PRST_MAP = {
    'shdw1': 'TOP_LEFT_DROP_SHADOW',
    'shdw2': 'TOP_LEFT_LARGE_DROP_SHADOW',
    'shdw3': 'BACK_LEFT_LONG_PERSPECTIVE_SHADOW',
    'shdw4': 'BACK_RIGHT_LONG_PERSPECTIVE_SHADOW',
    'shdw5': 'TOP_LEFT_DOUBLE_DROP_SHADOW',
    'shdw6': 'BOTTOM_RIGHT_SMALL_DROP_SHADOW',
    'shdw7': 'FRONT_LEFT_LONG_PERSPECTIVE_SHADOW',
    'shdw8': 'FRONT_RIGHT_LONG_PERSPECTIVE_SHADOW',
    'shdw9': 'OUTER_BOX_SHADOW_3D',
    'shdw10': 'INNER_BOX_SHADOW_3D',
    'shdw11': 'BACK_CENTER_PERSPECTIVE_SHADOW',
    'shdw12': 'TOP_RIGHT_DROP_SHADOW',
    'shdw13': 'FRONT_BOTTOM_SHADOW',
    'shdw14': 'BACK_LEFT_PERSPECTIVE_SHADOW',
    'shdw15': 'BACK_RIGHT_PERSPECTIVE_SHADOW',
    'shdw16': 'BOTTOM_LEFT_DROP_SHADOW',
    'shdw17': 'BOTTOM_RIGHT_DROP_SHADOW',
    'shdw18': 'FRONT_LEFT_PERSPECTIVE_SHADOW',
    'shdw19': 'FRONT_RIGHT_PERSPECTIVE_SHADOW',
    'shdw20': 'TOP_LEFT_SMALL_DROP_SHADOW',
}
_PRST_MAP_REV = {v: k for k, v in _PRST_MAP.items()}


class PresetShadow(IPresetShadow, IImageTransformOperation):
    """Represents a Preset Shadow effect."""

    def _init_internal(self, element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        self._element = element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def direction(self) -> float:
        """Direction of shadow. Read/write ."""
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
        """Distance of shadow. Read/write ."""
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
        """Color of shadow. Read-only ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ..ColorFormat import ColorFormat
        cf = ColorFormat()
        cf._init_internal(self._element, self._slide_part, self._parent_slide)
        return cf

    @property
    def preset(self) -> PresetShadowType:
        """Preset. Read/write ."""
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ..PresetShadowType import PresetShadowType
        val = self._element.get('prst')
        if val is None:
            return None
        name = _PRST_MAP.get(val)
        if name is None:
            return None
        return PresetShadowType[name]

    @preset.setter
    def preset(self, value: PresetShadowType):
        if not hasattr(self, '_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        ooxml_val = _PRST_MAP_REV.get(value.name)
        if ooxml_val:
            self._element.set('prst', ooxml_val)
        self._save()

    @property
    def as_i_image_transform_operation(self) -> IImageTransformOperation:
        return self

