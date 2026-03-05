from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .IGradientFormat import IGradientFormat
from .IFillParamSource import IFillParamSource
from ._internal.pptx.constants import NS, Elements

if TYPE_CHECKING:
    from .GradientDirection import GradientDirection
    from .GradientShape import GradientShape
    from .IGradientStopCollection import IGradientStopCollection
    from .NullableBool import NullableBool
    from .TileFlip import TileFlip
    from ._internal.pptx.slide_part import SlidePart

# Angle in 60000ths of degree -> GradientDirection mapping
_ANGLE_TO_DIRECTION = {
    0: 'FROM_CORNER1',       # top-left
    5400000: 'FROM_CORNER2',  # top-right
    10800000: 'FROM_CORNER4', # bottom-right
    16200000: 'FROM_CORNER3', # bottom-left
}

_DIRECTION_TO_ANGLE = {v: k for k, v in _ANGLE_TO_DIRECTION.items()}

_FLIP_MAP = {
    'none': 'NO_FLIP', 'x': 'FLIP_X', 'y': 'FLIP_Y', 'xy': 'FLIP_BOTH',
}
_FLIP_MAP_REV = {v: k for k, v in _FLIP_MAP.items()}


class GradientFormat(PVIObject, ISlideComponent, IPresentationComponent, IGradientFormat, IFillParamSource):
    """Represent a gradient format."""

    def _init_internal(self, grad_fill_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        self._grad_fill = grad_fill_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def tile_flip(self) -> TileFlip:
        """Returns or sets the flipping mode for a gradient. Read/write."""
        from .TileFlip import TileFlip
        val = self._grad_fill.get('flip')
        if val is None:
            return TileFlip.NOT_DEFINED
        name = _FLIP_MAP.get(val)
        return TileFlip[name] if name else TileFlip.NOT_DEFINED

    @tile_flip.setter
    def tile_flip(self, value: TileFlip):
        from .TileFlip import TileFlip
        if value == TileFlip.NOT_DEFINED:
            if 'flip' in self._grad_fill.attrib:
                del self._grad_fill.attrib['flip']
        else:
            ooxml_val = _FLIP_MAP_REV.get(value.name)
            if ooxml_val:
                self._grad_fill.set('flip', ooxml_val)
        self._save()

    @property
    def gradient_direction(self) -> GradientDirection:
        """Returns or sets the style of a gradient. Read/write."""
        from .GradientDirection import GradientDirection
        lin = self._grad_fill.find(Elements.A_LIN)
        if lin is not None:
            ang = int(lin.get('ang', '0'))
            name = _ANGLE_TO_DIRECTION.get(ang)
            if name:
                return GradientDirection[name]
        path = self._grad_fill.find(Elements.A_PATH)
        if path is not None:
            return GradientDirection.FROM_CENTER
        return GradientDirection.NOT_DEFINED

    @gradient_direction.setter
    def gradient_direction(self, value: GradientDirection):
        from .GradientDirection import GradientDirection
        if value == GradientDirection.NOT_DEFINED:
            return
        if value == GradientDirection.FROM_CENTER:
            # Remove lin, add/update path
            lin = self._grad_fill.find(Elements.A_LIN)
            if lin is not None:
                self._grad_fill.remove(lin)
            path = self._grad_fill.find(Elements.A_PATH)
            if path is None:
                ET.SubElement(self._grad_fill, Elements.A_PATH, path='circle')
        else:
            # Remove path, add/update lin
            path = self._grad_fill.find(Elements.A_PATH)
            if path is not None:
                self._grad_fill.remove(path)
            ang = _DIRECTION_TO_ANGLE.get(value.name, 0)
            lin = self._grad_fill.find(Elements.A_LIN)
            if lin is None:
                lin = ET.SubElement(self._grad_fill, Elements.A_LIN)
            lin.set('ang', str(ang))
        self._save()

    @property
    def linear_gradient_angle(self) -> float:
        """Returns or sets the angle of a gradient. Read/write."""
        lin = self._grad_fill.find(Elements.A_LIN)
        if lin is not None:
            return int(lin.get('ang', '0')) / 60000.0
        return 0.0

    @linear_gradient_angle.setter
    def linear_gradient_angle(self, value: float):
        lin = self._grad_fill.find(Elements.A_LIN)
        if lin is None:
            lin = ET.SubElement(self._grad_fill, Elements.A_LIN)
        lin.set('ang', str(int(round(value * 60000))))
        self._save()

    @property
    def linear_gradient_scaled(self) -> NullableBool:
        """Determines whether a gradient is scaled. Read/write."""
        from .NullableBool import NullableBool
        lin = self._grad_fill.find(Elements.A_LIN)
        if lin is None:
            return NullableBool.NOT_DEFINED
        val = lin.get('scaled')
        if val is None:
            return NullableBool.NOT_DEFINED
        return NullableBool.TRUE if val == '1' else NullableBool.FALSE

    @linear_gradient_scaled.setter
    def linear_gradient_scaled(self, value: NullableBool):
        from .NullableBool import NullableBool
        lin = self._grad_fill.find(Elements.A_LIN)
        if lin is None:
            lin = ET.SubElement(self._grad_fill, Elements.A_LIN)
        if value == NullableBool.NOT_DEFINED:
            if 'scaled' in lin.attrib:
                del lin.attrib['scaled']
        else:
            lin.set('scaled', '1' if value == NullableBool.TRUE else '0')
        self._save()

    @property
    def gradient_shape(self) -> GradientShape:
        """Returns or sets the shape of a gradient. Read/write."""
        from .GradientShape import GradientShape
        lin = self._grad_fill.find(Elements.A_LIN)
        if lin is not None:
            return GradientShape.LINEAR
        path = self._grad_fill.find(Elements.A_PATH)
        if path is not None:
            path_val = path.get('path', '')
            if path_val == 'rect':
                return GradientShape.RECTANGLE
            if path_val == 'circle':
                return GradientShape.RADIAL
            if path_val == 'shape':
                return GradientShape.PATH
        return GradientShape.NOT_DEFINED

    @gradient_shape.setter
    def gradient_shape(self, value: GradientShape):
        from .GradientShape import GradientShape
        if value == GradientShape.NOT_DEFINED:
            return
        # Remove existing lin and path
        for tag in [Elements.A_LIN, Elements.A_PATH]:
            el = self._grad_fill.find(tag)
            if el is not None:
                self._grad_fill.remove(el)
        if value == GradientShape.LINEAR:
            ET.SubElement(self._grad_fill, Elements.A_LIN, ang='0', scaled='1')
        else:
            path_map = {
                GradientShape.RECTANGLE: 'rect',
                GradientShape.RADIAL: 'circle',
                GradientShape.PATH: 'shape',
            }
            ET.SubElement(self._grad_fill, Elements.A_PATH, path=path_map[value])
        self._save()

    @property
    def gradient_stops(self) -> IGradientStopCollection:
        """Returns the collection of gradient stops. Read-only."""
        from .GradientStopCollection import GradientStopCollection
        gs_lst = self._grad_fill.find(Elements.A_GS_LST)
        if gs_lst is None:
            # gsLst must come before lin/path/tileRect in OOXML element order
            gs_lst = ET.Element(Elements.A_GS_LST)
            self._grad_fill.insert(0, gs_lst)
        gsc = GradientStopCollection()
        gsc._init_internal(gs_lst, self._slide_part, self._parent_slide)
        return gsc

