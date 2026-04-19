"""
Table part for XLSX packages.

Manages xl/tables/tableN.xml — defines named data tables within a worksheet.
"""

from __future__ import annotations
import lxml.etree as ET
from typing import Optional, NamedTuple, TYPE_CHECKING

from .constants import SML_NS, TABLE_NSMAP

if TYPE_CHECKING:
    from ..opc.opc_package import OpcPackage

_TABLE_TAG = f'{SML_NS}table'
_TABLE_COLUMNS_TAG = f'{SML_NS}tableColumns'
_TABLE_COLUMN_TAG = f'{SML_NS}tableColumn'
_TABLE_STYLE_INFO_TAG = f'{SML_NS}tableStyleInfo'
_AUTO_FILTER_TAG = f'{SML_NS}autoFilter'


class TableColumn(NamedTuple):
    """A column in a table definition."""
    id: int
    name: str


class TablePart:
    """Manages a table definition (xl/tables/tableN.xml)."""

    def __init__(self, package: OpcPackage, part_name: str):
        self._package = package
        self._part_name = part_name
        self._root: Optional[ET._Element] = None
        self._load()

    def _load(self) -> None:
        content = self._package.get_part(self._part_name)
        if content:
            self._root = ET.fromstring(content)
        else:
            raise ValueError(f"Table part not found: {self._part_name}")

    def get_ref(self) -> str:
        """Get table range reference (e.g., 'A1:D5')."""
        return self._root.get('ref', '')

    def set_ref(self, ref: str) -> None:
        """Set table range reference."""
        self._root.set('ref', ref)
        # Update autoFilter if present
        af = self._root.find(_AUTO_FILTER_TAG)
        if af is not None:
            af.set('ref', ref)

    def get_display_name(self) -> str:
        """Get table display name."""
        return self._root.get('displayName', '')

    def set_display_name(self, name: str) -> None:
        """Set table display name."""
        self._root.set('displayName', name)
        self._root.set('name', name)

    def get_table_id(self) -> int:
        """Get table ID."""
        return int(self._root.get('id', '0'))

    def get_columns(self) -> list[TableColumn]:
        """Get all table columns."""
        cols_elem = self._root.find(_TABLE_COLUMNS_TAG)
        if cols_elem is None:
            return []
        return [
            TableColumn(
                id=int(col.get('id', '0')),
                name=col.get('name', ''),
            )
            for col in cols_elem.findall(_TABLE_COLUMN_TAG)
        ]

    def set_columns(self, columns: list[TableColumn]) -> None:
        """Replace all table columns."""
        cols_elem = self._root.find(_TABLE_COLUMNS_TAG)
        if cols_elem is not None:
            self._root.remove(cols_elem)
        cols_elem = ET.SubElement(self._root, _TABLE_COLUMNS_TAG)
        cols_elem.set('count', str(len(columns)))
        for tc in columns:
            col_elem = ET.SubElement(cols_elem, _TABLE_COLUMN_TAG)
            col_elem.set('id', str(tc.id))
            col_elem.set('name', tc.name)

    def add_column(self, name: str) -> TableColumn:
        """Add a column. Returns the new TableColumn."""
        cols_elem = self._root.find(_TABLE_COLUMNS_TAG)
        if cols_elem is None:
            cols_elem = ET.SubElement(self._root, _TABLE_COLUMNS_TAG)
        existing = self.get_columns()
        new_id = max((c.id for c in existing), default=0) + 1
        col_elem = ET.SubElement(cols_elem, _TABLE_COLUMN_TAG)
        col_elem.set('id', str(new_id))
        col_elem.set('name', name)
        cols_elem.set('count', str(len(existing) + 1))
        return TableColumn(id=new_id, name=name)

    def remove_column(self, column_id: int) -> bool:
        """Remove a column by ID. Returns True if removed."""
        cols_elem = self._root.find(_TABLE_COLUMNS_TAG)
        if cols_elem is None:
            return False
        for col_elem in cols_elem.findall(_TABLE_COLUMN_TAG):
            if int(col_elem.get('id', '0')) == column_id:
                cols_elem.remove(col_elem)
                count = len(cols_elem.findall(_TABLE_COLUMN_TAG))
                cols_elem.set('count', str(count))
                return True
        return False

    def save(self) -> None:
        """Save table XML back to the package."""
        ET.indent(self._root, space='  ')
        xml_bytes = ET.tostring(
            self._root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True,
        )
        self._package.set_part(self._part_name, xml_bytes)

    @classmethod
    def create_new(
        cls,
        package: OpcPackage,
        part_name: str,
        table_id: int,
        display_name: str,
        ref: str,
        column_names: list[str],
    ) -> TablePart:
        """
        Create a new table part.

        Args:
            package: The OPC package.
            part_name: Part path (e.g., 'xl/tables/table1.xml').
            table_id: Unique table ID within the workbook.
            display_name: Table display name.
            ref: Cell range (e.g., 'A1:D5').
            column_names: List of column header names.
        """
        root = ET.Element(_TABLE_TAG, nsmap=TABLE_NSMAP)
        root.set('id', str(table_id))
        root.set('name', display_name)
        root.set('displayName', display_name)
        root.set('ref', ref)
        root.set('totalsRowShown', '0')

        # Auto filter
        af = ET.SubElement(root, _AUTO_FILTER_TAG)
        af.set('ref', ref)

        # Columns
        cols_elem = ET.SubElement(root, _TABLE_COLUMNS_TAG)
        cols_elem.set('count', str(len(column_names)))
        for i, name in enumerate(column_names, start=1):
            col = ET.SubElement(cols_elem, _TABLE_COLUMN_TAG)
            col.set('id', str(i))
            col.set('name', name)

        # Default table style
        style = ET.SubElement(root, _TABLE_STYLE_INFO_TAG)
        style.set('showFirstColumn', '0')
        style.set('showLastColumn', '0')
        style.set('showRowStripes', '1')
        style.set('showColumnStripes', '0')

        ET.indent(root, space='  ')
        xml_bytes = ET.tostring(
            root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True,
        )
        package.set_part(part_name, xml_bytes)

        return cls(package, part_name)
