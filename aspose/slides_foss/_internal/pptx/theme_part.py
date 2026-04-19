"""
Theme part handling for PPTX format.

Manages ppt/theme/themeN.xml parts.
"""

from __future__ import annotations
import lxml.etree as ET
from typing import Optional, TYPE_CHECKING

from .constants import NS, NAMESPACES

if TYPE_CHECKING:
    from ..opc import OpcPackage

# Register namespaces for clean XML output
for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)


class ThemePart:
    """
    Manages a theme XML part (ppt/theme/themeN.xml).

    Provides access to color scheme, font scheme, and format scheme elements.
    """

    def __init__(self, package: OpcPackage, part_name: str):
        """
        Initialize a theme part from an existing part in the package.

        Args:
            package: The OPC package containing the theme.
            part_name: The part path (e.g., 'ppt/theme/theme1.xml').
        """
        self._package = package
        self._part_name = part_name
        self._root: Optional[ET._Element] = None
        self._load()

    def _load(self) -> None:
        """Load and parse the theme XML from the package."""
        content = self._package.get_part(self._part_name)
        if content:
            self._root = ET.fromstring(content)
        else:
            raise ValueError(f"Theme part not found: {self._part_name}")

    @property
    def part_name(self) -> str:
        """Get the part name of this theme."""
        return self._part_name

    @property
    def name(self) -> str:
        """Get the theme name from <a:theme name='...'>."""
        return self._root.get('name', '')

    @name.setter
    def name(self, value: str) -> None:
        """Set the theme name on <a:theme name='...'>."""
        self._root.set('name', value)

    def _get_theme_elements(self) -> Optional[ET._Element]:
        """Get the <a:themeElements> element."""
        return self._root.find(f"{NS.A}themeElements")

    @property
    def color_scheme_element(self) -> Optional[ET._Element]:
        """Get the <a:clrScheme> element."""
        theme_elems = self._get_theme_elements()
        if theme_elems is not None:
            return theme_elems.find(f"{NS.A}clrScheme")
        return None

    @property
    def font_scheme_element(self) -> Optional[ET._Element]:
        """Get the <a:fontScheme> element."""
        theme_elems = self._get_theme_elements()
        if theme_elems is not None:
            return theme_elems.find(f"{NS.A}fontScheme")
        return None

    @property
    def format_scheme_element(self) -> Optional[ET._Element]:
        """Get the <a:fmtScheme> element."""
        theme_elems = self._get_theme_elements()
        if theme_elems is not None:
            return theme_elems.find(f"{NS.A}fmtScheme")
        return None

    @property
    def extra_color_schemes_element(self) -> Optional[ET._Element]:
        """Get the <a:extraClrSchemeLst> element."""
        return self._root.find(f"{NS.A}extraClrSchemeLst")

    def save(self) -> None:
        """Save the theme XML back to the package."""
        xml_bytes = ET.tostring(
            self._root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True
        )
        self._package.set_part(self._part_name, xml_bytes)
