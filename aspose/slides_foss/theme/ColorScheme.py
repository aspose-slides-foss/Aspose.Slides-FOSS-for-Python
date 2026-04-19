from __future__ import annotations
from typing import TYPE_CHECKING
from .IColorScheme import IColorScheme
from ..ISlideComponent import ISlideComponent
from ..IPresentationComponent import IPresentationComponent
from .._internal.pptx.constants import NS

if TYPE_CHECKING:
    from ..IBaseSlide import IBaseSlide
    from ..IColorFormat import IColorFormat
    from ..IPresentation import IPresentation
    from .._internal.pptx.theme_part import ThemePart

# Maps property names to XML element local names
_COLOR_SLOTS = {
    'dark1': 'dk1',
    'light1': 'lt1',
    'dark2': 'dk2',
    'light2': 'lt2',
    'accent1': 'accent1',
    'accent2': 'accent2',
    'accent3': 'accent3',
    'accent4': 'accent4',
    'accent5': 'accent5',
    'accent6': 'accent6',
    'hyperlink': 'hlink',
    'followed_hyperlink': 'folHlink',
}


class ColorScheme(IColorScheme, ISlideComponent, IPresentationComponent):
    """Stores theme-defined colors."""

    def _init_internal(self, clr_scheme_elem, theme_part: ThemePart, presentation) -> None:
        self._clr_scheme_elem = clr_scheme_elem
        self._theme_part = theme_part
        self._presentation_ref = presentation
        self._color_cache: dict[str, object] = {}

    def _get_color_format(self, slot_name: str) -> IColorFormat:
        if slot_name in self._color_cache:
            return self._color_cache[slot_name]
        xml_tag = _COLOR_SLOTS[slot_name]
        elem = self._clr_scheme_elem.find(f"{NS.A}{xml_tag}")
        if elem is None:
            return None
        from ..ColorFormat import ColorFormat
        cf = ColorFormat()
        cf._init_internal(elem, self._theme_part, None)
        self._color_cache[slot_name] = cf
        return cf

    @property
    def dark1(self) -> IColorFormat:
        """First dark color in the scheme. Read-only ."""
        return self._get_color_format('dark1')

    @property
    def light1(self) -> IColorFormat:
        """First light color in the scheme. Read-only ."""
        return self._get_color_format('light1')

    @property
    def dark2(self) -> IColorFormat:
        """Second dark color in the scheme. Read-only ."""
        return self._get_color_format('dark2')

    @property
    def light2(self) -> IColorFormat:
        """Second light color in the scheme. Read-only ."""
        return self._get_color_format('light2')

    @property
    def accent1(self) -> IColorFormat:
        """First accent color in the scheme. Read-only ."""
        return self._get_color_format('accent1')

    @property
    def accent2(self) -> IColorFormat:
        """Second accent color in the scheme. Read-only ."""
        return self._get_color_format('accent2')

    @property
    def accent3(self) -> IColorFormat:
        """Third accent color in the scheme. Read-only ."""
        return self._get_color_format('accent3')

    @property
    def accent4(self) -> IColorFormat:
        """Fourth accent color in the scheme. Read-only ."""
        return self._get_color_format('accent4')

    @property
    def accent5(self) -> IColorFormat:
        """Fifth accent color in the scheme. Read-only ."""
        return self._get_color_format('accent5')

    @property
    def accent6(self) -> IColorFormat:
        """Sixth accent color in the scheme. Read-only ."""
        return self._get_color_format('accent6')

    @property
    def hyperlink(self) -> IColorFormat:
        """Color for the hyperlinks. Read-only ."""
        return self._get_color_format('hyperlink')

    @property
    def followed_hyperlink(self) -> IColorFormat:
        """Color for the visited hyperlinks. Read-only ."""
        return self._get_color_format('followed_hyperlink')

    @property
    def slide(self) -> IBaseSlide:
        """Returns the parent slide. Read-only ."""
        return None

    @property
    def presentation(self) -> IPresentation:
        """Returns the parent presentation. Read-only ."""
        return self._presentation_ref

    @property
    def as_i_slide_component(self) -> ISlideComponent:
        return self

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        return self
