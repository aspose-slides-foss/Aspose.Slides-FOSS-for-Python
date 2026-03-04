"""
Master slide part handling for PPTX format.

Manages ppt/slideMasters/slideMasterN.xml parts (read-only for now).
"""

from __future__ import annotations
import lxml.etree as ET
from typing import Optional, TYPE_CHECKING

from .constants import NS, Elements, NAMESPACES
from ..opc import RelationshipsManager
from ..opc.relationships import REL_TYPES

if TYPE_CHECKING:
    from ..opc import OpcPackage


class MasterSlidePart:
    """
    Manages a master slide XML part (ppt/slideMasters/slideMasterN.xml).

    Read-only for now; provides access to master slide properties.
    """

    def __init__(self, package: OpcPackage, part_name: str):
        """
        Initialize a master slide part.

        Args:
            package: The OPC package containing the master slide.
            part_name: The part path (e.g., 'ppt/slideMasters/slideMaster1.xml').
        """
        self._package = package
        self._part_name = part_name
        self._root: Optional[ET._Element] = None
        self._rels_manager = RelationshipsManager(package, part_name)
        self._load()

    def _load(self) -> None:
        """Load and parse the master slide XML."""
        content = self._package.get_part(self._part_name)
        if content:
            self._root = ET.fromstring(content)
        else:
            raise ValueError(f"Master slide part not found: {self._part_name}")

    @property
    def part_name(self) -> str:
        """Get the part name of this master slide."""
        return self._part_name

    @property
    def name(self) -> str:
        """Get the master slide name from <p:cSld name='...'>."""
        csld = self._root.find(f".//{Elements.C_SLD}")
        if csld is not None:
            return csld.get('name', '')
        return ''

    @name.setter
    def name(self, value: str) -> None:
        """Set the master slide name on <p:cSld name='...'>."""
        csld = self._root.find(f".//{Elements.C_SLD}")
        if csld is not None:
            csld.set('name', value)

    @property
    def layout_part_names(self) -> list[str]:
        """Get list of layout slide part names from this master's relationships."""
        rels = self._rels_manager.get_relationships_by_type(REL_TYPES['slide_layout'])
        result = []
        for rel in rels:
            resolved = self._resolve_target(rel.target)
            result.append(resolved)
        return result

    def _resolve_target(self, target: str) -> str:
        """Resolve a relative target path to an absolute part name."""
        if target.startswith('/'):
            return target.lstrip('/')
        base_dir = self._part_name.rsplit('/', 1)[0] if '/' in self._part_name else ''
        parts = (base_dir + '/' + target).split('/')
        resolved = []
        for part in parts:
            if part == '..':
                if resolved:
                    resolved.pop()
            elif part and part != '.':
                resolved.append(part)
        return '/'.join(resolved)

    def save(self) -> None:
        """Save the master slide XML back to the package."""
        xml_bytes = ET.tostring(
            self._root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True
        )
        self._package.set_part(self._part_name, xml_bytes)
        self._rels_manager.save()
