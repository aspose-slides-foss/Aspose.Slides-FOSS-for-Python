"""
Comment authors part handling for PPTX format.

Manages the ppt/commentAuthors.xml part which holds all comment author definitions.
"""

from __future__ import annotations
import lxml.etree as ET
from typing import Optional, List, TYPE_CHECKING

from .constants import NS, NAMESPACES
from ..opc import RelationshipsManager, ContentTypesManager
from ..opc.relationships import REL_TYPES
from ..opc.content_types import CONTENT_TYPES

if TYPE_CHECKING:
    from ..opc import OpcPackage

# Register namespaces for clean XML output
for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)

_P_NS = NAMESPACES['p']
_P = f"{{{_P_NS}}}"

PART_NAME = 'ppt/commentAuthors.xml'


class AuthorData:
    """Raw data for a comment author parsed from XML."""

    def __init__(self, elem: ET._Element):
        self._elem = elem

    @property
    def id(self) -> int:
        return int(self._elem.get('id', '0'))

    @property
    def name(self) -> str:
        return self._elem.get('name', '')

    @name.setter
    def name(self, value: str) -> None:
        self._elem.set('name', value)

    @property
    def initials(self) -> str:
        return self._elem.get('initials', '')

    @initials.setter
    def initials(self, value: str) -> None:
        self._elem.set('initials', value)

    @property
    def last_idx(self) -> int:
        return int(self._elem.get('lastIdx', '0'))

    @last_idx.setter
    def last_idx(self, value: int) -> None:
        self._elem.set('lastIdx', str(value))

    @property
    def clr_idx(self) -> int:
        return int(self._elem.get('clrIdx', '0'))


class CommentAuthorsPart:
    """
    Manages the comment authors XML part (ppt/commentAuthors.xml).

    This part holds all author definitions used across the presentation's comments.
    """

    def __init__(self, package: OpcPackage):
        self._package = package
        self._root: Optional[ET._Element] = None
        self._load()

    def _load(self) -> None:
        content = self._package.get_part(PART_NAME)
        if content:
            self._root = ET.fromstring(content)
        else:
            self._root = ET.Element(
                f"{_P}cmAuthorLst",
                nsmap={'p': _P_NS}
            )

    def get_authors(self) -> List[AuthorData]:
        return [AuthorData(e) for e in self._root.findall(f"{_P}cmAuthor")]

    def find_author_by_id(self, author_id: int) -> Optional[AuthorData]:
        for e in self._root.findall(f"{_P}cmAuthor"):
            if int(e.get('id', '-1')) == author_id:
                return AuthorData(e)
        return None

    def add_author(self, name: str, initials: str) -> AuthorData:
        """Add a new author and return its AuthorData."""
        # Compute next id and clrIdx
        existing = self._root.findall(f"{_P}cmAuthor")
        next_id = len(existing)
        clr_idx = next_id % 10  # Colors cycle 0-9

        elem = ET.SubElement(self._root, f"{_P}cmAuthor")
        elem.set('id', str(next_id))
        elem.set('name', name)
        elem.set('initials', initials)
        elem.set('lastIdx', '0')
        elem.set('clrIdx', str(clr_idx))
        return AuthorData(elem)

    def remove_author(self, author_id: int) -> None:
        for e in self._root.findall(f"{_P}cmAuthor"):
            if int(e.get('id', '-1')) == author_id:
                self._root.remove(e)
                return

    def clear(self) -> None:
        for e in self._root.findall(f"{_P}cmAuthor"):
            self._root.remove(e)

    def next_comment_idx(self, author_id: int) -> int:
        """
        Return the next globally-unique comment index.

        OOXML parentCmId references idx values that must be unique across ALL
        authors within the presentation (not just per-author). We achieve this
        by taking the maximum lastIdx across every author and incrementing from
        there, then updating only the target author's lastIdx.
        """
        global_max = 0
        for e in self._root.findall(f"{_P}cmAuthor"):
            global_max = max(global_max, int(e.get('lastIdx', '0')))
        new_idx = global_max + 1
        data = self.find_author_by_id(author_id)
        if data is not None:
            data.last_idx = new_idx
        return new_idx

    def save(self) -> None:
        """Save the comment authors XML back to the package."""
        ET.indent(self._root, space='  ')
        xml_bytes = ET.tostring(
            self._root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True,
        )
        self._package.set_part(PART_NAME, xml_bytes)

    @staticmethod
    def ensure_registered(package: OpcPackage) -> None:
        """
        Ensure that commentAuthors.xml is registered in content types and
        the presentation has a relationship to it. Call before first save.
        """
        # Add content type override if needed
        ct = ContentTypesManager(package)
        existing_ct = ct.get_content_type(PART_NAME)
        if existing_ct != CONTENT_TYPES['commentAuthors']:
            ct.add_override(PART_NAME, CONTENT_TYPES['commentAuthors'])
            ct.save()

        # Add relationship from presentation to commentAuthors if needed
        from .presentation_part import PresentationPart
        rels = RelationshipsManager(package, PresentationPart.PART_NAME)
        existing = rels.get_relationships_by_type(REL_TYPES['commentAuthors'])
        if not existing:
            rels.add_relationship(REL_TYPES['commentAuthors'], 'commentAuthors.xml')
            rels.save()
