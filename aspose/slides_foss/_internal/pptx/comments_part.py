"""
Comments part handling for PPTX format.

Manages individual ppt/comments/slideN.xml parts (one per slide that has comments).
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

# EMU conversion: 1 cm = 360000 EMU. Comment positions are stored in cm in PointF.
_CM_TO_EMU = 360000


def _dt_to_str(dt) -> str:
    """Convert a datetime/date to OOXML datetime string."""
    import datetime
    if isinstance(dt, datetime.datetime):
        ms = dt.microsecond // 1000
        return dt.strftime(f'%Y-%m-%dT%H:%M:%S.{ms:03d}')
    elif isinstance(dt, datetime.date):
        return dt.strftime('%Y-%m-%dT00:00:00.000')
    return str(dt)


def _str_to_dt(s: str):
    """Parse OOXML datetime string to datetime object."""
    import datetime
    if not s:
        return None
    # Try parsing with milliseconds
    for fmt in ('%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


class CommentData:
    """Raw data for a comment parsed from XML."""

    def __init__(self, elem: ET._Element):
        self._elem = elem

    @property
    def author_id(self) -> int:
        return int(self._elem.get('authorId', '0'))

    @property
    def idx(self) -> int:
        return int(self._elem.get('idx', '0'))

    @property
    def dt_str(self) -> str:
        return self._elem.get('dt', '')

    @dt_str.setter
    def dt_str(self, value: str) -> None:
        self._elem.set('dt', value)

    @property
    def parent_cm_id(self) -> Optional[int]:
        val = self._elem.get('parentCmId')
        return int(val) if val is not None else None

    @parent_cm_id.setter
    def parent_cm_id(self, value: Optional[int]) -> None:
        if value is None:
            if 'parentCmId' in self._elem.attrib:
                del self._elem.attrib['parentCmId']
        else:
            self._elem.set('parentCmId', str(value))

    @property
    def text(self) -> str:
        text_elem = self._elem.find(f"{_P}text")
        if text_elem is not None and text_elem.text:
            return text_elem.text
        return ''

    @text.setter
    def text(self, value: str) -> None:
        text_elem = self._elem.find(f"{_P}text")
        if text_elem is None:
            text_elem = ET.SubElement(self._elem, f"{_P}text")
        text_elem.text = value

    @property
    def pos_x(self) -> float:
        """Position x in cm."""
        pos = self._elem.find(f"{_P}pos")
        if pos is not None:
            return int(pos.get('x', '0')) / _CM_TO_EMU
        return 0.0

    @pos_x.setter
    def pos_x(self, value: float) -> None:
        pos = self._elem.find(f"{_P}pos")
        if pos is None:
            pos = ET.SubElement(self._elem, f"{_P}pos")
        pos.set('x', str(round(value * _CM_TO_EMU)))

    @property
    def pos_y(self) -> float:
        """Position y in cm."""
        pos = self._elem.find(f"{_P}pos")
        if pos is not None:
            return int(pos.get('y', '0')) / _CM_TO_EMU
        return 0.0

    @pos_y.setter
    def pos_y(self, value: float) -> None:
        pos = self._elem.find(f"{_P}pos")
        if pos is None:
            pos = ET.SubElement(self._elem, f"{_P}pos")
        pos.set('y', str(round(value * _CM_TO_EMU)))


class CommentsPart:
    """
    Manages a slide comments XML part (ppt/comments/slideN.xml).

    One file exists per slide that has comments.
    """

    def __init__(self, package: OpcPackage, part_name: str):
        self._package = package
        self._part_name = part_name
        self._root: Optional[ET._Element] = None
        self._load()

    @property
    def part_name(self) -> str:
        return self._part_name

    def _load(self) -> None:
        content = self._package.get_part(self._part_name)
        if content:
            self._root = ET.fromstring(content)
        else:
            raise ValueError(f"Comments part not found: {self._part_name}")

    def get_comments(self) -> List[CommentData]:
        return [CommentData(e) for e in self._root.findall(f"{_P}cm")]

    def get_comments_by_author(self, author_id: int) -> List[CommentData]:
        return [
            CommentData(e) for e in self._root.findall(f"{_P}cm")
            if int(e.get('authorId', '-1')) == author_id
        ]

    def find_comment_by_idx(self, author_id: int, idx: int) -> Optional[CommentData]:
        for e in self._root.findall(f"{_P}cm"):
            if (int(e.get('authorId', '-1')) == author_id and
                    int(e.get('idx', '-1')) == idx):
                return CommentData(e)
        return None

    def find_comment_by_idx_all(self, idx: int) -> Optional[CommentData]:
        """Find a comment by idx across all authors (for parentCmId lookup)."""
        for e in self._root.findall(f"{_P}cm"):
            if int(e.get('idx', '-1')) == idx:
                return CommentData(e)
        return None

    def add_comment(self, author_id: int, idx: int, text: str, pos_x: float,
                    pos_y: float, dt_str: str,
                    parent_idx: Optional[int] = None) -> CommentData:
        """Append a new comment element and return its CommentData."""
        elem = ET.SubElement(self._root, f"{_P}cm")
        elem.set('authorId', str(author_id))
        elem.set('dt', dt_str)
        elem.set('idx', str(idx))
        if parent_idx is not None:
            elem.set('parentCmId', str(parent_idx))

        pos = ET.SubElement(elem, f"{_P}pos")
        pos.set('x', str(round(pos_x * _CM_TO_EMU)))
        pos.set('y', str(round(pos_y * _CM_TO_EMU)))

        text_elem = ET.SubElement(elem, f"{_P}text")
        text_elem.text = text

        return CommentData(elem)

    def insert_comment(self, index: int, author_id: int, idx: int, text: str,
                       pos_x: float, pos_y: float, dt_str: str,
                       parent_idx: Optional[int] = None) -> CommentData:
        """Insert a comment at the given index."""
        elem = ET.Element(f"{_P}cm")
        elem.set('authorId', str(author_id))
        elem.set('dt', dt_str)
        elem.set('idx', str(idx))
        if parent_idx is not None:
            elem.set('parentCmId', str(parent_idx))

        pos = ET.SubElement(elem, f"{_P}pos")
        pos.set('x', str(round(pos_x * _CM_TO_EMU)))
        pos.set('y', str(round(pos_y * _CM_TO_EMU)))

        text_elem = ET.SubElement(elem, f"{_P}text")
        text_elem.text = text

        # Insert at position among all cm elements
        all_cm = self._root.findall(f"{_P}cm")
        if index >= len(all_cm):
            self._root.append(elem)
        else:
            ref = all_cm[index]
            ref_pos = list(self._root).index(ref)
            self._root.insert(ref_pos, elem)

        return CommentData(elem)

    def remove_comment(self, author_id: int, idx: int) -> None:
        for e in self._root.findall(f"{_P}cm"):
            if (int(e.get('authorId', '-1')) == author_id and
                    int(e.get('idx', '-1')) == idx):
                self._root.remove(e)
                return

    def remove_comment_elem(self, elem: ET._Element) -> None:
        try:
            self._root.remove(elem)
        except ValueError:
            pass

    def remove_comments_at(self, index: int) -> None:
        all_cm = self._root.findall(f"{_P}cm")
        if 0 <= index < len(all_cm):
            self._root.remove(all_cm[index])

    def clear(self) -> None:
        for e in self._root.findall(f"{_P}cm"):
            self._root.remove(e)

    def count(self) -> int:
        return len(self._root.findall(f"{_P}cm"))

    def is_empty(self) -> bool:
        return self.count() == 0

    def save(self) -> None:
        ET.indent(self._root, space='  ')
        xml_bytes = ET.tostring(
            self._root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True,
        )
        self._package.set_part(self._part_name, xml_bytes)

    @staticmethod
    def create_for_slide(package: OpcPackage, slide_part_name: str,
                         slide_rels_manager=None) -> 'CommentsPart':
        """
        Create a new empty comments part for a slide and register all relationships.

        Args:
            slide_rels_manager: If provided, the SlidePart's existing RelationshipsManager
                is used (so the relationship survives subsequent SlidePart.save() calls).
                If None, a fresh RelationshipsManager is created.
        """
        # Find a unique part name
        num = 1
        while True:
            candidate = f"ppt/comments/slide{num}.xml"
            if not package.has_part(candidate):
                part_name = candidate
                break
            num += 1

        # Build minimal XML
        root = ET.Element(f"{_P}cmLst", nsmap={'p': _P_NS})
        ET.indent(root, space='  ')
        xml_bytes = ET.tostring(
            root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True,
        )
        package.set_part(part_name, xml_bytes)

        # Content type
        ct = ContentTypesManager(package)
        ct.add_override(part_name, CONTENT_TYPES['comments'])
        ct.save()

        # Relationship: slide → comments
        rel_target = CommentsPart._compute_relative_target(slide_part_name, part_name)
        if slide_rels_manager is not None:
            # Use the existing SlidePart rels_manager so the rel persists through save()
            slide_rels_manager.add_relationship(REL_TYPES['comments'], rel_target)
            slide_rels_manager.save()
        else:
            slide_rels = RelationshipsManager(package, slide_part_name)
            slide_rels.add_relationship(REL_TYPES['comments'], rel_target)
            slide_rels.save()

        return CommentsPart(package, part_name)

    @staticmethod
    def load_for_slide(package: OpcPackage, slide_part_name: str) -> Optional['CommentsPart']:
        """
        Load the comments part for a slide, if it exists. Returns None if no comments.
        """
        slide_rels = RelationshipsManager(package, slide_part_name)
        comment_rels = slide_rels.get_relationships_by_type(REL_TYPES['comments'])
        if not comment_rels:
            return None
        rel = comment_rels[0]
        target = rel.target
        part_name = CommentsPart._resolve_target(slide_part_name, target)
        if not package.has_part(part_name):
            return None
        return CommentsPart(package, part_name)

    @staticmethod
    def delete(package: OpcPackage, slide_part_name: str) -> None:
        """Delete the comments part for a slide."""
        slide_rels = RelationshipsManager(package, slide_part_name)
        comment_rels = slide_rels.get_relationships_by_type(REL_TYPES['comments'])
        for rel in comment_rels:
            part_name = CommentsPart._resolve_target(slide_part_name, rel.target)
            package.delete_part(part_name)
            ct = ContentTypesManager(package)
            ct.remove_override(part_name)
            ct.save()
            slide_rels.remove_relationship(rel.id)
        if comment_rels:
            slide_rels.save()

    @staticmethod
    def _resolve_target(from_part: str, target: str) -> str:
        if target.startswith('/'):
            return target.lstrip('/')
        base_dir = from_part.rsplit('/', 1)[0] if '/' in from_part else ''
        parts = (base_dir + '/' + target).split('/')
        resolved = []
        for part in parts:
            if part == '..':
                if resolved:
                    resolved.pop()
            elif part and part != '.':
                resolved.append(part)
        return '/'.join(resolved)

    @staticmethod
    def _compute_relative_target(from_part: str, to_part: str) -> str:
        from_dir = from_part.rsplit('/', 1)[0] if '/' in from_part else ''
        to_dir = to_part.rsplit('/', 1)[0] if '/' in to_part else ''
        to_file = to_part.rsplit('/', 1)[-1]

        if from_dir == to_dir:
            return to_file

        from_parts = from_dir.split('/') if from_dir else []
        to_parts = to_dir.split('/') if to_dir else []

        common_len = 0
        for i in range(min(len(from_parts), len(to_parts))):
            if from_parts[i] == to_parts[i]:
                common_len = i + 1
            else:
                break

        up_count = len(from_parts) - common_len
        down_path = '/'.join(to_parts[common_len:])

        result = '../' * up_count
        if down_path:
            result += down_path + '/'
        result += to_file
        return result
