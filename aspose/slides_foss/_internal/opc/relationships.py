"""
Relationships management for OPC packages.

Handles .rels files that define relationships between parts in the package.
"""

from __future__ import annotations
import lxml.etree as ET
from typing import Optional, NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .opc_package import OpcPackage

# Relationships namespace
RELS_NAMESPACE = "http://schemas.openxmlformats.org/package/2006/relationships"
RELS_NS = f"{{{RELS_NAMESPACE}}}"

# Note: lxml doesn't support registering empty prefix, so we use a workaround
# when creating elements to ensure clean default namespace output

# Common relationship types
REL_TYPES = {
    'office_document': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument',
    'slide': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide',
    'slide_layout': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout',
    'slide_master': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster',
    'notes_slide': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide',
    'notes_master': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster',
    'handout_master': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/handoutMaster',
    'theme': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme',
    'core_properties': 'http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties',
    'extended_properties': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties',
    'thumbnail': 'http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail',
    'image': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image',
    'hyperlink': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',
    'chart': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/chart',
    'oleObject': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/oleObject',
    'package': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/package',
    'audio': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/audio',
    'video': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/video',
    'comments': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments',
    'commentAuthors': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/commentAuthors',
}


class Relationship(NamedTuple):
    """Represents a single relationship in a .rels file."""
    id: str
    type: str
    target: str
    target_mode: Optional[str] = None  # 'External' for external targets


class RelationshipsManager:
    """
    Manages relationships (.rels) files in an OPC package.

    Each part can have an associated .rels file that defines its relationships
    to other parts. This class provides methods to:
    - Load relationships for a part
    - Add/remove relationships
    - Generate unique relationship IDs
    - Serialize back to XML
    """

    def __init__(self, package: OpcPackage, source_part: str = ''):
        """
        Initialize the relationships manager for a specific part.

        Args:
            package: The OPC package.
            source_part: The part path whose relationships to manage.
                        Empty string for root relationships (_rels/.rels).
        """
        self._package = package
        self._source_part = source_part
        self._rels_part_name = self._get_rels_part_name(source_part)
        self._root: Optional[ET._Element] = None
        self._relationships: dict[str, Relationship] = {}
        self._load()

    @staticmethod
    def _get_rels_part_name(source_part: str) -> str:
        """
        Get the .rels file path for a given source part.

        Examples:
            '' -> '_rels/.rels'
            'ppt/presentation.xml' -> 'ppt/_rels/presentation.xml.rels'
            'ppt/slides/slide1.xml' -> 'ppt/slides/_rels/slide1.xml.rels'
        """
        if not source_part:
            return '_rels/.rels'

        # Split into directory and filename
        if '/' in source_part:
            directory, filename = source_part.rsplit('/', 1)
            return f"{directory}/_rels/{filename}.rels"
        else:
            return f"_rels/{source_part}.rels"

    def _load(self) -> None:
        """Load and parse the .rels file from the package."""
        content = self._package.get_part(self._rels_part_name)
        if content:
            self._root = ET.fromstring(content)
            self._parse_relationships()
        else:
            # Create empty relationships structure with default namespace (no prefix)
            self._root = ET.Element(
                f"{RELS_NS}Relationships",
                nsmap={None: RELS_NAMESPACE}
            )

    def _parse_relationships(self) -> None:
        """Parse relationships from the loaded XML."""
        self._relationships.clear()
        for rel_elem in self._root.findall(f"{RELS_NS}Relationship"):
            rel = Relationship(
                id=rel_elem.get('Id', ''),
                type=rel_elem.get('Type', ''),
                target=rel_elem.get('Target', ''),
                target_mode=rel_elem.get('TargetMode')
            )
            self._relationships[rel.id] = rel

    def get_relationship(self, rel_id: str) -> Optional[Relationship]:
        """
        Get a relationship by ID.

        Args:
            rel_id: The relationship ID (e.g., 'rId1').

        Returns:
            Relationship object or None if not found.
        """
        return self._relationships.get(rel_id)

    def get_relationships_by_type(self, rel_type: str) -> list[Relationship]:
        """
        Get all relationships of a specific type.

        Args:
            rel_type: The relationship type URI.

        Returns:
            List of matching relationships.
        """
        return [r for r in self._relationships.values() if r.type == rel_type]

    def get_all_relationships(self) -> list[Relationship]:
        """
        Get all relationships.

        Returns:
            List of all relationships.
        """
        return list(self._relationships.values())

    def _generate_rel_id(self) -> str:
        """Generate a unique relationship ID."""
        existing_ids = set(self._relationships.keys())
        counter = 1
        while True:
            rel_id = f"rId{counter}"
            if rel_id not in existing_ids:
                return rel_id
            counter += 1

    def add_relationship(
        self,
        rel_type: str,
        target: str,
        rel_id: Optional[str] = None,
        target_mode: Optional[str] = None
    ) -> str:
        """
        Add a new relationship.

        Args:
            rel_type: The relationship type URI.
            target: The target part path (relative to source).
            rel_id: Optional specific ID. If None, auto-generated.
            target_mode: Optional target mode ('External' for external links).

        Returns:
            The relationship ID.
        """
        if rel_id is None:
            rel_id = self._generate_rel_id()

        rel = Relationship(
            id=rel_id,
            type=rel_type,
            target=target,
            target_mode=target_mode
        )
        self._relationships[rel_id] = rel

        # Add to XML
        rel_elem = ET.SubElement(self._root, f"{RELS_NS}Relationship")
        rel_elem.set('Id', rel_id)
        rel_elem.set('Type', rel_type)
        rel_elem.set('Target', target)
        if target_mode:
            rel_elem.set('TargetMode', target_mode)

        return rel_id

    def remove_relationship(self, rel_id: str) -> bool:
        """
        Remove a relationship by ID.

        Args:
            rel_id: The relationship ID to remove.

        Returns:
            True if removed, False if not found.
        """
        if rel_id not in self._relationships:
            return False

        del self._relationships[rel_id]

        # Remove from XML
        for rel_elem in self._root.findall(f"{RELS_NS}Relationship"):
            if rel_elem.get('Id') == rel_id:
                self._root.remove(rel_elem)
                return True

        return True

    def save(self) -> None:
        """Save the relationships back to the package."""
        if not self._relationships:
            # Remove empty .rels file
            self._package.delete_part(self._rels_part_name)
            return

        # Re-indent to ensure consistent formatting after adding new elements
        ET.indent(self._root, space='  ')

        xml_bytes = ET.tostring(
            self._root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True
        )
        self._package.set_part(self._rels_part_name, xml_bytes)

    @property
    def part_name(self) -> str:
        """Get the .rels file part name."""
        return self._rels_part_name
