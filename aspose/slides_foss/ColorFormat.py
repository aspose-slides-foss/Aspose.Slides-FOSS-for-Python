from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .IColorFormat import IColorFormat
from .IFillParamSource import IFillParamSource
from ._internal.pptx.constants import NS, Elements

if TYPE_CHECKING:
    from .drawing import Color
    from .ColorType import ColorType
    from .IColorOperationCollection import IColorOperationCollection
    from .PresetColor import PresetColor
    from .SchemeColor import SchemeColor
    from .SystemColor import SystemColor
    from ._internal.pptx.slide_part import SlidePart

# Maps OOXML scheme color values to SchemeColor enum member names
_SCHEME_CLR_TO_ENUM = {
    'bg1': 'BACKGROUND1', 'tx1': 'TEXT1', 'bg2': 'BACKGROUND2', 'tx2': 'TEXT2',
    'accent1': 'ACCENT1', 'accent2': 'ACCENT2', 'accent3': 'ACCENT3',
    'accent4': 'ACCENT4', 'accent5': 'ACCENT5', 'accent6': 'ACCENT6',
    'hlink': 'HYPERLINK', 'folHlink': 'FOLLOWED_HYPERLINK',
    'dk1': 'DARK1', 'lt1': 'LIGHT1', 'dk2': 'DARK2', 'lt2': 'LIGHT2',
}

_ENUM_TO_SCHEME_CLR = {v: k for k, v in _SCHEME_CLR_TO_ENUM.items()}

# Color element tags that represent different color types
_COLOR_ELEMENT_TAGS = {
    Elements.A_SRGB_CLR, Elements.A_SCHEME_CLR, Elements.A_PRST_CLR,
    Elements.A_SYS_CLR, Elements.A_HLS_CLR, Elements.A_SCR_GB_CLR,
}


class ColorFormat(PVIObject, ISlideComponent, IPresentationComponent, IColorFormat, IFillParamSource):
    """Represents a color used in a presentation."""

    def _init_internal(self, parent_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        """
        Internal initialization.

        Args:
            parent_element: The XML element that contains the color child
                (e.g., <a:solidFill>, <a:fgClr>, <a:bgClr>, <a:gs>).
            slide_part: The SlidePart for saving changes.
            parent_slide: The parent slide object.
        """
        self._parent_element = parent_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _find_color_element(self) -> ET._Element | None:
        """Find the first color child element in the parent."""
        if not hasattr(self, '_parent_element'):
            return None
        for child in self._parent_element:
            if child.tag in _COLOR_ELEMENT_TAGS:
                return child
        return None

    def _clear_color_elements(self) -> None:
        """Remove all existing color child elements from parent."""
        for child in list(self._parent_element):
            if child.tag in _COLOR_ELEMENT_TAGS:
                self._parent_element.remove(child)

    def _save(self) -> None:
        """Save changes to the underlying slide part."""
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def color_type(self) -> ColorType:
        """Returns or sets the color definition method. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .ColorType import ColorType
        el = self._find_color_element()
        if el is None:
            return ColorType.NOT_DEFINED
        if el.tag == Elements.A_SRGB_CLR:
            return ColorType.RGB
        if el.tag == Elements.A_SCHEME_CLR:
            return ColorType.SCHEME
        if el.tag == Elements.A_PRST_CLR:
            return ColorType.PRESET
        if el.tag == Elements.A_SYS_CLR:
            return ColorType.SYSTEM
        if el.tag == Elements.A_SCR_GB_CLR:
            return ColorType.RGB_PERCENTAGE
        if el.tag == Elements.A_HLS_CLR:
            return ColorType.HSL
        return ColorType.NOT_DEFINED

    @color_type.setter
    def color_type(self, value: ColorType):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .ColorType import ColorType
        if value == self.color_type:
            return
        self._clear_color_elements()
        if value == ColorType.RGB:
            ET.SubElement(self._parent_element, Elements.A_SRGB_CLR, val='000000')
        elif value == ColorType.SCHEME:
            ET.SubElement(self._parent_element, Elements.A_SCHEME_CLR, val='tx1')
        elif value == ColorType.PRESET:
            ET.SubElement(self._parent_element, Elements.A_PRST_CLR, val='black')
        elif value == ColorType.SYSTEM:
            ET.SubElement(self._parent_element, Elements.A_SYS_CLR, val='windowText')
        elif value == ColorType.HSL:
            ET.SubElement(self._parent_element, Elements.A_HLS_CLR,
                          attrib={'hue': '0', 'sat': '0', 'lum': '0'})
        elif value == ColorType.RGB_PERCENTAGE:
            ET.SubElement(self._parent_element, Elements.A_SCR_GB_CLR,
                          attrib={'r': '0', 'g': '0', 'b': '0'})
        # NOT_DEFINED: just clearing is enough
        self._save()

    def _read_alpha(self, color_element: ET._Element) -> int:
        """Read alpha value from <a:alpha> child. Returns 0-255."""
        alpha_el = color_element.find(f"{NS.A}alpha")
        if alpha_el is None:
            return 255
        # OOXML alpha val is in 1/1000ths of percent (100000 = fully opaque)
        val = int(alpha_el.get('val', '100000'))
        return int(round(val * 255 / 100000))

    def _write_alpha(self, color_element: ET._Element, alpha: int) -> None:
        """Write <a:alpha> child if alpha != 255 (fully opaque)."""
        # Remove existing alpha element
        existing = color_element.find(f"{NS.A}alpha")
        if existing is not None:
            color_element.remove(existing)
        if alpha < 255:
            val = int(round(alpha * 100000 / 255))
            ET.SubElement(color_element, f"{NS.A}alpha", val=str(val))

    @property
    def color(self) -> Color:
        """Returns resulting color. Sets RGB colors and clears all color transformations. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .drawing import Color
        el = self._find_color_element()
        if el is None:
            return Color(255, 0, 0, 0)
        if el.tag == Elements.A_SRGB_CLR:
            hex_val = el.get('val', '000000')
            r = int(hex_val[0:2], 16)
            g = int(hex_val[2:4], 16)
            b = int(hex_val[4:6], 16)
            a = self._read_alpha(el)
            return Color(a, r, g, b)
        return Color(255, 0, 0, 0)

    @color.setter
    def color(self, value: Color):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._clear_color_elements()
        hex_val = f"{value.r:02X}{value.g:02X}{value.b:02X}"
        clr_el = ET.SubElement(self._parent_element, Elements.A_SRGB_CLR, val=hex_val)
        self._write_alpha(clr_el, value.a)
        self._save()

    @property
    def preset_color(self) -> PresetColor:
        """Returns or sets the color preset. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .PresetColor import PresetColor
        el = self._find_color_element()
        if el is not None and el.tag == Elements.A_PRST_CLR:
            val = el.get('val', '')
            # OOXML uses camelCase names like "aliceBlue"
            # Convert to UPPER_SNAKE_CASE for enum lookup
            name = _camel_to_upper_snake(val)
            try:
                return PresetColor[name]
            except KeyError:
                pass
        return PresetColor.NOT_DEFINED

    @preset_color.setter
    def preset_color(self, value: PresetColor):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .PresetColor import PresetColor
        if value == PresetColor.NOT_DEFINED:
            return
        self._clear_color_elements()
        # Convert UPPER_SNAKE_CASE to camelCase for OOXML
        ooxml_val = _upper_snake_to_camel(value.name)
        ET.SubElement(self._parent_element, Elements.A_PRST_CLR, val=ooxml_val)
        self._save()



    @property
    def scheme_color(self) -> SchemeColor:
        """Returns or sets the color identified by a color scheme. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .SchemeColor import SchemeColor
        el = self._find_color_element()
        if el is not None and el.tag == Elements.A_SCHEME_CLR:
            val = el.get('val', '')
            enum_name = _SCHEME_CLR_TO_ENUM.get(val)
            if enum_name:
                return SchemeColor[enum_name]
        return SchemeColor.NOT_DEFINED

    @scheme_color.setter
    def scheme_color(self, value: SchemeColor):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .SchemeColor import SchemeColor
        if value == SchemeColor.NOT_DEFINED:
            return
        ooxml_val = _ENUM_TO_SCHEME_CLR.get(value.name)
        if ooxml_val is None:
            return
        self._clear_color_elements()
        ET.SubElement(self._parent_element, Elements.A_SCHEME_CLR, val=ooxml_val)
        self._save()

    @property
    def r(self) -> int:
        """Returns or sets the red component of a color. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return self.color.r

    @r.setter
    def r(self, value: int):
        c = self.color
        from .drawing import Color
        self.color = Color(c.a, value, c.g, c.b)

    @property
    def g(self) -> int:
        """Returns or sets the green component of a color. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return self.color.g

    @g.setter
    def g(self, value: int):
        c = self.color
        from .drawing import Color
        self.color = Color(c.a, c.r, value, c.b)

    @property
    def b(self) -> int:
        """Returns or sets the blue component of a color. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return self.color.b

    @b.setter
    def b(self, value: int):
        c = self.color
        from .drawing import Color
        self.color = Color(c.a, c.r, c.g, value)

    @property
    def float_r(self) -> float:
        """Returns or sets the red component of a color. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return self.r / 255.0

    @float_r.setter
    def float_r(self, value: float):
        self.r = int(round(value * 255))

    @property
    def float_g(self) -> float:
        """Returns or sets the green component of a color. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return self.g / 255.0

    @float_g.setter
    def float_g(self, value: float):
        self.g = int(round(value * 255))

    @property
    def float_b(self) -> float:
        """Returns or sets the blue component of a color. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return self.b / 255.0

    @float_b.setter
    def float_b(self, value: float):
        self.b = int(round(value * 255))












def _camel_to_upper_snake(name: str) -> str:
    """Convert camelCase to UPPER_SNAKE_CASE. E.g., 'aliceBlue' -> 'ALICE_BLUE'."""
    result = []
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0:
            result.append('_')
        result.append(ch.upper())
    return ''.join(result)


def _upper_snake_to_camel(name: str) -> str:
    """Convert UPPER_SNAKE_CASE to camelCase. E.g., 'ALICE_BLUE' -> 'aliceBlue'."""
    parts = name.lower().split('_')
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])
