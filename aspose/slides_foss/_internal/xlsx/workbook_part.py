"""
Workbook part for XLSX packages.

Manages xl/workbook.xml — the root part that defines the sheet list.
"""

from __future__ import annotations
import lxml.etree as ET
from typing import Optional, NamedTuple, TYPE_CHECKING

from .constants import SML_NS, R_NS, XLSX_REL_TYPES, XLSX_CONTENT_TYPES
from ..opc.relationships import RelationshipsManager

if TYPE_CHECKING:
    from ..opc.opc_package import OpcPackage
    from ..opc.content_types import ContentTypesManager

_SHEETS_TAG = f'{SML_NS}sheets'
_SHEET_TAG = f'{SML_NS}sheet'


class SheetInfo(NamedTuple):
    """Information about a worksheet."""
    name: str
    sheet_id: int
    rel_id: str
    part_name: str  # Resolved absolute part name (e.g., 'xl/worksheets/sheet1.xml')


class WorkbookPart:
    """Manages xl/workbook.xml and the workbook-level relationships."""

    PART_NAME = 'xl/workbook.xml'

    def __init__(self, package: OpcPackage, part_name: Optional[str] = None):
        self._package = package
        self._part_name = part_name or self.PART_NAME
        self._root: Optional[ET._Element] = None
        self._rels_manager = RelationshipsManager(package, self._part_name)
        self._load()

    def _load(self) -> None:
        content = self._package.get_part(self._part_name)
        if content:
            self._root = ET.fromstring(content)
        else:
            raise ValueError(f"Workbook part not found: {self._part_name}")

    def _resolve_target(self, target: str) -> str:
        """Resolve a relative target path from the workbook directory."""
        # Workbook is at xl/workbook.xml, so targets are relative to xl/
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

    def get_sheets(self) -> list[SheetInfo]:
        """Get all sheet info, ordered as in the workbook."""
        sheets_elem = self._root.find(_SHEETS_TAG)
        if sheets_elem is None:
            return []
        result = []
        for sheet in sheets_elem.findall(_SHEET_TAG):
            name = sheet.get('name', '')
            sheet_id = int(sheet.get('sheetId', '0'))
            rel_id = sheet.get(f'{R_NS}id', '')
            # Resolve part name from relationship target
            rel = self._rels_manager.get_relationship(rel_id)
            part_name = self._resolve_target(rel.target) if rel else ''
            result.append(SheetInfo(name=name, sheet_id=sheet_id, rel_id=rel_id, part_name=part_name))
        return result

    def get_sheet_by_name(self, name: str) -> Optional[SheetInfo]:
        """Find a sheet by name."""
        for sheet in self.get_sheets():
            if sheet.name == name:
                return sheet
        return None

    def get_sheet_by_index(self, index: int) -> Optional[SheetInfo]:
        """Get sheet by 0-based index."""
        sheets = self.get_sheets()
        if 0 <= index < len(sheets):
            return sheets[index]
        return None

    def _next_sheet_id(self) -> int:
        """Generate next unique sheet ID."""
        sheets = self.get_sheets()
        if not sheets:
            return 1
        return max(s.sheet_id for s in sheets) + 1

    def _next_sheet_part_name(self) -> str:
        """Generate next available worksheet part name."""
        existing = {s.part_name for s in self.get_sheets()}
        counter = 1
        while True:
            part_name = f'xl/worksheets/sheet{counter}.xml'
            if part_name not in existing:
                return part_name
            counter += 1

    def add_sheet(self, name: str, ct_manager: Optional[ContentTypesManager] = None) -> SheetInfo:
        """
        Add a new sheet entry to the workbook.

        Creates the <sheet> element, adds a worksheet relationship, and
        optionally registers the content type.

        Returns SheetInfo with the new sheet's details.
        """
        sheet_id = self._next_sheet_id()
        part_name = self._next_sheet_part_name()

        # Relative target from xl/ to xl/worksheets/sheetN.xml
        target = part_name.replace('xl/', '', 1)

        # Add relationship
        rel_id = self._rels_manager.add_relationship(
            XLSX_REL_TYPES['worksheet'], target
        )

        # Add <sheet> element
        sheets_elem = self._root.find(_SHEETS_TAG)
        if sheets_elem is None:
            sheets_elem = ET.SubElement(self._root, _SHEETS_TAG)
        sheet_elem = ET.SubElement(sheets_elem, _SHEET_TAG)
        sheet_elem.set('name', name)
        sheet_elem.set('sheetId', str(sheet_id))
        sheet_elem.set(f'{R_NS}id', rel_id)

        # Register content type
        if ct_manager:
            ct_manager.add_override(part_name, XLSX_CONTENT_TYPES['worksheet'])

        return SheetInfo(name=name, sheet_id=sheet_id, rel_id=rel_id, part_name=part_name)

    def remove_sheet(self, name: str, ct_manager: Optional[ContentTypesManager] = None) -> bool:
        """Remove a sheet by name. Returns True if removed."""
        sheets_elem = self._root.find(_SHEETS_TAG)
        if sheets_elem is None:
            return False

        for sheet_elem in sheets_elem.findall(_SHEET_TAG):
            if sheet_elem.get('name') == name:
                rel_id = sheet_elem.get(f'{R_NS}id', '')
                rel = self._rels_manager.get_relationship(rel_id)
                part_name = self._resolve_target(rel.target) if rel else ''

                # Remove XML element
                sheets_elem.remove(sheet_elem)
                # Remove relationship
                if rel_id:
                    self._rels_manager.remove_relationship(rel_id)
                # Remove part and content type
                if part_name:
                    self._package.delete_part(part_name)
                    if ct_manager:
                        ct_manager.remove_override(part_name)
                return True
        return False

    def save(self) -> None:
        """Save workbook XML and relationships back to the package."""
        ET.indent(self._root, space='  ')
        xml_bytes = ET.tostring(
            self._root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True,
        )
        self._package.set_part(self._part_name, xml_bytes)
        self._rels_manager.save()
