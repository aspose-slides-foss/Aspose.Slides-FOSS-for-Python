from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .IShapeBevel import IShapeBevel
from ._internal.pptx.constants import NS, Elements, EMU_PER_POINT

if TYPE_CHECKING:
    from .BevelPresetType import BevelPresetType
    from ._internal.pptx.slide_part import SlidePart

_BEVEL_MAP = {
    'angle': 'ANGLE', 'artDeco': 'ART_DECO', 'circle': 'CIRCLE', 'convex': 'CONVEX',
    'coolSlant': 'COOL_SLANT', 'cross': 'CROSS', 'divot': 'DIVOT', 'hardEdge': 'HARD_EDGE',
    'relaxedInset': 'RELAXED_INSET', 'riblet': 'RIBLET', 'slope': 'SLOPE', 'softRound': 'SOFT_ROUND',
}
_BEVEL_MAP_REV = {v: k for k, v in _BEVEL_MAP.items()}


class ShapeBevel(PVIObject, ISlideComponent, IPresentationComponent, IShapeBevel):
    """Contains the properties of shape's main face relief."""
    def __init__(self, b_is_top_bevel=True):
        self._is_top = b_is_top_bevel

    def _init_internal(self, bevel_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        self._bevel_element = bevel_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def width(self) -> float:
        """Bevel width. Read/write."""
        if not hasattr(self, '_bevel_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        val = self._bevel_element.get('w')
        if val is None:
            return 0.0
        return int(val) / EMU_PER_POINT

    @width.setter
    def width(self, value: float):
        if not hasattr(self, '_bevel_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._bevel_element.set('w', str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def height(self) -> float:
        """Bevel height. Read/write."""
        if not hasattr(self, '_bevel_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        val = self._bevel_element.get('h')
        if val is None:
            return 0.0
        return int(val) / EMU_PER_POINT

    @height.setter
    def height(self, value: float):
        if not hasattr(self, '_bevel_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._bevel_element.set('h', str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def bevel_type(self) -> BevelPresetType:
        """Bevel type. Read/write."""
        if not hasattr(self, '_bevel_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .BevelPresetType import BevelPresetType
        val = self._bevel_element.get('prst')
        if val is None:
            return BevelPresetType.NOT_DEFINED
        name = _BEVEL_MAP.get(val)
        return BevelPresetType[name] if name else BevelPresetType.NOT_DEFINED

    @bevel_type.setter
    def bevel_type(self, value: BevelPresetType):
        if not hasattr(self, '_bevel_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .BevelPresetType import BevelPresetType
        if value == BevelPresetType.NOT_DEFINED:
            if 'prst' in self._bevel_element.attrib:
                del self._bevel_element.attrib['prst']
        else:
            ooxml_val = _BEVEL_MAP_REV.get(value.name)
            if ooxml_val:
                self._bevel_element.set('prst', ooxml_val)
        self._save()
