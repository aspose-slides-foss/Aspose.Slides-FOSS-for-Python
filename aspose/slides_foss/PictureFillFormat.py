from __future__ import annotations
from typing import overload, TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .IPictureFillFormat import IPictureFillFormat
from .IFillParamSource import IFillParamSource
from ._internal.pptx.constants import NS, EMU_PER_POINT

if TYPE_CHECKING:
    from .IPPImage import IPPImage
    from .ISlidesPicture import ISlidesPicture
    from .PictureFillMode import PictureFillMode
    from .RectangleAlignment import RectangleAlignment
    from .TileFlip import TileFlip
    from ._internal.pptx.slide_part import SlidePart

_ALIGN_MAP = {
    'tl': 'TOP_LEFT', 't': 'TOP', 'tr': 'TOP_RIGHT',
    'l': 'LEFT', 'ctr': 'CENTER', 'r': 'RIGHT',
    'bl': 'BOTTOM_LEFT', 'b': 'BOTTOM', 'br': 'BOTTOM_RIGHT',
}
_ALIGN_MAP_REV = {v: k for k, v in _ALIGN_MAP.items()}

_FLIP_MAP = {
    'none': 'NO_FLIP', 'x': 'FLIP_X', 'y': 'FLIP_Y', 'xy': 'FLIP_BOTH',
}
_FLIP_MAP_REV = {v: k for k, v in _FLIP_MAP.items()}


class PictureFillFormat(PVIObject, ISlideComponent, IPresentationComponent, IPictureFillFormat, IFillParamSource):
    """Represents a picture fill style."""

    def _init_internal(self, blip_fill_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        """
        Internal initialization with the p:blipFill XML element.

        Args:
            blip_fill_element: The p:blipFill element.
            slide_part: The SlidePart for relationship resolution.
            parent_slide: The parent Slide object.
        """
        self._blip_fill = blip_fill_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _get_blip(self) -> ET._Element:
        """Get the a:blip element."""
        return self._blip_fill.find(f'{NS.A}blip')

    def _get_or_create_src_rect(self) -> ET._Element:
        """Get or create the a:srcRect element for crop values."""
        src_rect = self._blip_fill.find(f'{NS.A}srcRect')
        if src_rect is None:
            src_rect = ET.SubElement(self._blip_fill, f'{NS.A}srcRect')
        return src_rect

    def _get_stretch(self) -> ET._Element:
        """Get the a:stretch element."""
        return self._blip_fill.find(f'{NS.A}stretch')

    def _get_or_create_fill_rect(self) -> ET._Element:
        """Get or create the a:fillRect element under a:stretch."""
        stretch = self._get_stretch()
        if stretch is None:
            stretch = ET.SubElement(self._blip_fill, f'{NS.A}stretch')
        fill_rect = stretch.find(f'{NS.A}fillRect')
        if fill_rect is None:
            fill_rect = ET.SubElement(stretch, f'{NS.A}fillRect')
        return fill_rect

    @property
    def dpi(self) -> int:
        """Returns or sets the dpi which is used to fill a picture. Read/write ."""
        return getattr(self, '_dpi', -1)

    @dpi.setter
    def dpi(self, value: int):
        self._dpi = value

    @property
    def picture_fill_mode(self) -> PictureFillMode:
        """Returns or sets the picture fill mode. Read/write ."""
        from .PictureFillMode import PictureFillMode
        tile = self._blip_fill.find(f'{NS.A}tile')
        if tile is not None:
            return PictureFillMode.TILE
        return PictureFillMode.STRETCH

    @picture_fill_mode.setter
    def picture_fill_mode(self, value: PictureFillMode):
        from .PictureFillMode import PictureFillMode
        if value == PictureFillMode.TILE:
            # Remove stretch, add tile
            stretch = self._blip_fill.find(f'{NS.A}stretch')
            if stretch is not None:
                self._blip_fill.remove(stretch)
            if self._blip_fill.find(f'{NS.A}tile') is None:
                ET.SubElement(self._blip_fill, f'{NS.A}tile')
        else:
            # Remove tile, add stretch
            tile = self._blip_fill.find(f'{NS.A}tile')
            if tile is not None:
                self._blip_fill.remove(tile)
            if self._blip_fill.find(f'{NS.A}stretch') is None:
                stretch = ET.SubElement(self._blip_fill, f'{NS.A}stretch')
                ET.SubElement(stretch, f'{NS.A}fillRect')

    @property
    def picture(self) -> ISlidesPicture:
        """Returns the picture. Read-only ."""
        from .Picture import Picture
        blip = self._get_blip()
        if blip is None:
            return None
        pic = Picture()
        pic._init_internal(blip, self._slide_part, self._parent_slide)
        return pic

    def _get_crop_value(self, attr: str) -> float:
        """Get a crop value from a:srcRect. Returns percentage (e.g., 10.0 for 10%)."""
        src_rect = self._blip_fill.find(f'{NS.A}srcRect')
        if src_rect is None:
            return 0.0
        val = src_rect.get(attr, '0')
        return int(val) / 1000.0

    def _set_crop_value(self, attr: str, value: float) -> None:
        """Set a crop value on a:srcRect. value is percentage (e.g., 10.0 for 10%)."""
        src_rect = self._get_or_create_src_rect()
        src_rect.set(attr, str(int(value * 1000)))

    @property
    def crop_left(self) -> float:
        """Returns or sets the number of percents of real image width that are cropped off the left of the picture. Read/write ."""
        return self._get_crop_value('l')

    @crop_left.setter
    def crop_left(self, value: float):
        self._set_crop_value('l', value)

    @property
    def crop_top(self) -> float:
        """Returns or sets the number of percents of real image height that are cropped off the top of the picture. Read/write ."""
        return self._get_crop_value('t')

    @crop_top.setter
    def crop_top(self, value: float):
        self._set_crop_value('t', value)

    @property
    def crop_right(self) -> float:
        """Returns or sets the number of percents of real image width that are cropped off the right of the picture. Read/write ."""
        return self._get_crop_value('r')

    @crop_right.setter
    def crop_right(self, value: float):
        self._set_crop_value('r', value)

    @property
    def crop_bottom(self) -> float:
        """Returns or sets the number of percents of real image height that are cropped off the bottom of the picture. Read/write ."""
        return self._get_crop_value('b')

    @crop_bottom.setter
    def crop_bottom(self, value: float):
        self._set_crop_value('b', value)

    def _get_stretch_offset(self, attr: str) -> float:
        """Get a stretch offset value from a:fillRect under a:stretch."""
        stretch = self._get_stretch()
        if stretch is None:
            return 0.0
        fill_rect = stretch.find(f'{NS.A}fillRect')
        if fill_rect is None:
            return 0.0
        val = fill_rect.get(attr, '0')
        return int(val) / 1000.0

    def _set_stretch_offset(self, attr: str, value: float) -> None:
        """Set a stretch offset value on a:fillRect under a:stretch."""
        fill_rect = self._get_or_create_fill_rect()
        fill_rect.set(attr, str(int(value * 1000)))

    @property
    def stretch_offset_left(self) -> float:
        """Returns or sets left edge of the fill rectangle that is defined by a percentage offset from the left edge of the shape's bounding box. A positive percentage specifies an inset, while a negative percentage specifies an outset. Read/write ."""
        return self._get_stretch_offset('l')

    @stretch_offset_left.setter
    def stretch_offset_left(self, value: float):
        self._set_stretch_offset('l', value)

    @property
    def stretch_offset_top(self) -> float:
        """Returns or sets top edge of the fill rectangle that is defined by a percentage offset from the top edge of the shape's bounding box. A positive percentage specifies an inset, while a negative percentage specifies an outset. Read/write ."""
        return self._get_stretch_offset('t')

    @stretch_offset_top.setter
    def stretch_offset_top(self, value: float):
        self._set_stretch_offset('t', value)

    @property
    def stretch_offset_right(self) -> float:
        """Returns or sets right edge of the fill rectangle that is defined by a percentage offset from the right edge of the shape's bounding box. A positive percentage specifies an inset, while a negative percentage specifies an outset. Read/write ."""
        return self._get_stretch_offset('r')

    @stretch_offset_right.setter
    def stretch_offset_right(self, value: float):
        self._set_stretch_offset('r', value)

    @property
    def stretch_offset_bottom(self) -> float:
        """Returns or sets bottom edge of the fill rectangle that is defined by a percentage offset from the bottom edge of the shape's bounding box. A positive percentage specifies an inset, while a negative percentage specifies an outset. Read/write ."""
        return self._get_stretch_offset('b')

    @stretch_offset_bottom.setter
    def stretch_offset_bottom(self, value: float):
        self._set_stretch_offset('b', value)

    def _get_tile(self) -> ET._Element | None:
        """Get the a:tile element."""
        return self._blip_fill.find(f'{NS.A}tile')

    def _ensure_tile(self) -> ET._Element:
        """Get or create the a:tile element (switching from stretch to tile mode)."""
        tile = self._get_tile()
        if tile is not None:
            return tile
        # Remove stretch if present
        stretch = self._blip_fill.find(f'{NS.A}stretch')
        if stretch is not None:
            self._blip_fill.remove(stretch)
        return ET.SubElement(self._blip_fill, f'{NS.A}tile')

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def tile_offset_x(self) -> float:
        """Returns or sets the horizontal offset of the texture from the shape's origin in points. A positive value moves the texture to the right, while a negative value moves it to the left. Read/write ."""
        tile = self._get_tile()
        if tile is None:
            return 0.0
        val = tile.get('tx')
        return int(val) / EMU_PER_POINT if val is not None else 0.0

    @tile_offset_x.setter
    def tile_offset_x(self, value: float):
        tile = self._ensure_tile()
        tile.set('tx', str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def tile_offset_y(self) -> float:
        """Returns or sets the vertical offset of the texture from the shape's origin in points. A positive value moves the texture down, while a negative value moves it up. Read/write ."""
        tile = self._get_tile()
        if tile is None:
            return 0.0
        val = tile.get('ty')
        return int(val) / EMU_PER_POINT if val is not None else 0.0

    @tile_offset_y.setter
    def tile_offset_y(self, value: float):
        tile = self._ensure_tile()
        tile.set('ty', str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def tile_scale_x(self) -> float:
        """Returns or sets the horizontal scale for the texture fill as a percentage. Read/write ."""
        tile = self._get_tile()
        if tile is None:
            return 100.0
        val = tile.get('sx')
        return int(val) / 1000.0 if val is not None else 100.0

    @tile_scale_x.setter
    def tile_scale_x(self, value: float):
        tile = self._ensure_tile()
        tile.set('sx', str(int(round(value * 1000))))
        self._save()

    @property
    def tile_scale_y(self) -> float:
        """Returns or sets the vertical scale for the texture fill as a percentage. Read/write ."""
        tile = self._get_tile()
        if tile is None:
            return 100.0
        val = tile.get('sy')
        return int(val) / 1000.0 if val is not None else 100.0

    @tile_scale_y.setter
    def tile_scale_y(self, value: float):
        tile = self._ensure_tile()
        tile.set('sy', str(int(round(value * 1000))))
        self._save()

    @property
    def tile_alignment(self) -> RectangleAlignment:
        """Returns or sets how the texture is aligned within the shape. This setting controls the starting point of the texture pattern and how it repeats across the shape. Read/write ."""
        from .RectangleAlignment import RectangleAlignment
        tile = self._get_tile()
        if tile is None:
            return RectangleAlignment.NOT_DEFINED
        val = tile.get('algn')
        if val is None:
            return RectangleAlignment.NOT_DEFINED
        name = _ALIGN_MAP.get(val)
        return RectangleAlignment[name] if name else RectangleAlignment.NOT_DEFINED

    @tile_alignment.setter
    def tile_alignment(self, value: RectangleAlignment):
        from .RectangleAlignment import RectangleAlignment
        tile = self._ensure_tile()
        if value == RectangleAlignment.NOT_DEFINED:
            if 'algn' in tile.attrib:
                del tile.attrib['algn']
        else:
            ooxml_val = _ALIGN_MAP_REV.get(value.name)
            if ooxml_val:
                tile.set('algn', ooxml_val)
        self._save()

    @property
    def tile_flip(self) -> TileFlip:
        """Flips the texture tile around its horizontal, vertical or both axis. Read/write ."""
        from .TileFlip import TileFlip
        tile = self._get_tile()
        if tile is None:
            return TileFlip.NOT_DEFINED
        val = tile.get('flip')
        if val is None:
            return TileFlip.NOT_DEFINED
        name = _FLIP_MAP.get(val)
        return TileFlip[name] if name else TileFlip.NOT_DEFINED

    @tile_flip.setter
    def tile_flip(self, value: TileFlip):
        from .TileFlip import TileFlip
        tile = self._ensure_tile()
        if value == TileFlip.NOT_DEFINED:
            if 'flip' in tile.attrib:
                del tile.attrib['flip']
        else:
            ooxml_val = _FLIP_MAP_REV.get(value.name)
            if ooxml_val:
                tile.set('flip', ooxml_val)
        self._save()





