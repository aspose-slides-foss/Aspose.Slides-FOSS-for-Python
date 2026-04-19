"""
Shared Strings Table for XLSX packages.

Manages xl/sharedStrings.xml — a deduplication table for string cell values.
Cells with type="s" store an index into this table instead of the string itself.
"""

from __future__ import annotations
import lxml.etree as ET
from typing import Optional, TYPE_CHECKING

from .constants import SML_NS, SST_NSMAP

if TYPE_CHECKING:
    from ..opc.opc_package import OpcPackage

_T_TAG = f'{SML_NS}t'
_SI_TAG = f'{SML_NS}si'
_SST_TAG = f'{SML_NS}sst'
_R_TAG = f'{SML_NS}r'


class SharedStringsPart:
    """Manages the shared strings table (xl/sharedStrings.xml)."""

    PART_NAME = 'xl/sharedStrings.xml'

    def __init__(self, package: OpcPackage, part_name: Optional[str] = None):
        self._package = package
        self._part_name = part_name or self.PART_NAME
        self._strings: list[str] = []
        self._index_map: dict[str, int] = {}
        self._load()

    def _load(self) -> None:
        content = self._package.get_part(self._part_name)
        if content:
            root = ET.fromstring(content)
            for si in root.findall(_SI_TAG):
                text = self._extract_text(si)
                idx = len(self._strings)
                self._strings.append(text)
                # Only store first occurrence for dedup
                if text not in self._index_map:
                    self._index_map[text] = idx

    @staticmethod
    def _extract_text(si_elem: ET._Element) -> str:
        """Extract text from an <si> element, handling both plain <t> and rich text <r> forms."""
        # Plain string: <si><t>text</t></si>
        t_elem = si_elem.find(_T_TAG)
        if t_elem is not None:
            return t_elem.text or ''
        # Rich text: <si><r><t>part1</t></r><r><t>part2</t></r></si>
        parts = []
        for r_elem in si_elem.findall(_R_TAG):
            t = r_elem.find(_T_TAG)
            if t is not None and t.text:
                parts.append(t.text)
        return ''.join(parts)

    def get_string(self, index: int) -> str:
        """Get string by index. Raises IndexError if out of range."""
        return self._strings[index]

    def get_or_add_string(self, value: str) -> int:
        """Return index of value, adding it if not already present."""
        idx = self._index_map.get(value)
        if idx is not None:
            return idx
        idx = len(self._strings)
        self._strings.append(value)
        self._index_map[value] = idx
        return idx

    def get_count(self) -> int:
        """Return total number of strings."""
        return len(self._strings)

    def save(self) -> None:
        """Serialize shared strings table back to the package."""
        count = len(self._strings)
        root = ET.Element(_SST_TAG, nsmap=SST_NSMAP)
        root.set('count', str(count))
        root.set('uniqueCount', str(count))

        for text in self._strings:
            si = ET.SubElement(root, _SI_TAG)
            t = ET.SubElement(si, _T_TAG)
            t.text = text
            # Preserve leading/trailing whitespace
            if text and (text[0] == ' ' or text[-1] == ' ' or '\n' in text):
                t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')

        ET.indent(root, space='  ')
        xml_bytes = ET.tostring(
            root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True,
        )
        self._package.set_part(self._part_name, xml_bytes)
