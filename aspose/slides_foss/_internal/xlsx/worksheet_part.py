"""
Worksheet part for XLSX packages.

Manages xl/worksheets/sheetN.xml — the actual cell data for a single sheet.
"""

from __future__ import annotations
import lxml.etree as ET
from dataclasses import dataclass
from typing import Optional, Union, TYPE_CHECKING

from .constants import SML_NS, R_NS, WORKSHEET_NSMAP, XLSX_REL_TYPES
from .cell_reference import parse_cell_ref, format_cell_ref, parse_range_ref
from ..opc.relationships import RelationshipsManager

if TYPE_CHECKING:
    from ..opc.opc_package import OpcPackage
    from .shared_strings_part import SharedStringsPart

_WORKSHEET_TAG = f'{SML_NS}worksheet'
_SHEET_DATA_TAG = f'{SML_NS}sheetData'
_ROW_TAG = f'{SML_NS}row'
_C_TAG = f'{SML_NS}c'
_V_TAG = f'{SML_NS}v'
_IS_TAG = f'{SML_NS}is'
_T_TAG = f'{SML_NS}t'
_DIMENSION_TAG = f'{SML_NS}dimension'
_TABLE_PARTS_TAG = f'{SML_NS}tableParts'
_TABLE_PART_TAG = f'{SML_NS}tablePart'


@dataclass
class CellValue:
    """Represents a cell's typed value."""
    value: Union[str, float, int, None]
    is_string: bool

    @property
    def is_empty(self) -> bool:
        return self.value is None


class WorksheetPart:
    """Manages cell data in xl/worksheets/sheetN.xml."""

    def __init__(
        self,
        package: OpcPackage,
        part_name: str,
        shared_strings: SharedStringsPart,
    ):
        self._package = package
        self._part_name = part_name
        self._shared_strings = shared_strings
        self._rels_manager = RelationshipsManager(package, part_name)
        self._root: Optional[ET._Element] = None
        self._sheet_data: Optional[ET._Element] = None
        self._rows: dict[int, ET._Element] = {}  # 1-based row number -> <row>
        self._load()

    def _load(self) -> None:
        content = self._package.get_part(self._part_name)
        if content:
            self._root = ET.fromstring(content)
            self._sheet_data = self._root.find(_SHEET_DATA_TAG)
            if self._sheet_data is None:
                self._sheet_data = ET.SubElement(self._root, _SHEET_DATA_TAG)
            self._index_rows()
        else:
            self._create_empty()

    def _create_empty(self) -> None:
        """Build a minimal empty worksheet."""
        self._root = ET.Element(_WORKSHEET_TAG, nsmap=WORKSHEET_NSMAP)
        dim = ET.SubElement(self._root, _DIMENSION_TAG)
        dim.set('ref', 'A1')
        self._sheet_data = ET.SubElement(self._root, _SHEET_DATA_TAG)
        self._rows = {}

    def _index_rows(self) -> None:
        """Build row index from <sheetData>."""
        self._rows.clear()
        for row_elem in self._sheet_data.findall(_ROW_TAG):
            row_num = int(row_elem.get('r', '0'))
            if row_num > 0:
                self._rows[row_num] = row_elem

    def _get_or_create_row(self, row_num: int) -> ET._Element:
        """Get or create a <row> element for the given 1-based row number, maintaining sort order."""
        if row_num in self._rows:
            return self._rows[row_num]
        row_elem = ET.Element(_ROW_TAG)
        row_elem.set('r', str(row_num))
        # Insert in sorted position
        inserted = False
        for existing in self._sheet_data.findall(_ROW_TAG):
            existing_num = int(existing.get('r', '0'))
            if existing_num > row_num:
                self._sheet_data.insert(list(self._sheet_data).index(existing), row_elem)
                inserted = True
                break
        if not inserted:
            self._sheet_data.append(row_elem)
        self._rows[row_num] = row_elem
        return row_elem

    def _find_cell(self, row_elem: ET._Element, ref: str) -> Optional[ET._Element]:
        """Find a <c> element in a row by its reference."""
        for c in row_elem.findall(_C_TAG):
            if c.get('r') == ref:
                return c
        return None

    def _read_cell_value(self, c_elem: ET._Element) -> CellValue:
        """Extract typed value from a <c> element."""
        cell_type = c_elem.get('t', '')
        v_elem = c_elem.find(_V_TAG)

        if cell_type == 's':
            # Shared string reference
            if v_elem is not None and v_elem.text:
                idx = int(v_elem.text)
                return CellValue(value=self._shared_strings.get_string(idx), is_string=True)
            return CellValue(value='', is_string=True)

        if cell_type == 'inlineStr':
            # Inline string
            is_elem = c_elem.find(_IS_TAG)
            if is_elem is not None:
                t_elem = is_elem.find(_T_TAG)
                if t_elem is not None:
                    return CellValue(value=t_elem.text or '', is_string=True)
            return CellValue(value='', is_string=True)

        if cell_type == 'b':
            # Boolean
            if v_elem is not None and v_elem.text:
                return CellValue(value=int(v_elem.text), is_string=False)

        # Numeric (default) or empty
        if v_elem is not None and v_elem.text:
            text = v_elem.text
            try:
                if '.' in text or 'e' in text.lower():
                    return CellValue(value=float(text), is_string=False)
                return CellValue(value=int(text), is_string=False)
            except ValueError:
                return CellValue(value=text, is_string=True)

        return CellValue(value=None, is_string=False)

    # --- Public API ---

    def get_cell(self, ref: str) -> CellValue:
        """
        Get cell value by A1-notation reference.

        Returns CellValue with value=None if cell doesn't exist.
        """
        row_idx, _ = parse_cell_ref(ref)
        row_num = row_idx + 1
        row_elem = self._rows.get(row_num)
        if row_elem is None:
            return CellValue(value=None, is_string=False)
        # Normalize ref (strip $)
        normalized = format_cell_ref(row_idx, parse_cell_ref(ref)[1])
        c_elem = self._find_cell(row_elem, normalized)
        if c_elem is None:
            return CellValue(value=None, is_string=False)
        return self._read_cell_value(c_elem)

    def set_cell(self, ref: str, value: Union[str, float, int, None]) -> None:
        """
        Set cell value. Auto-detects type:
        - str -> shared string (t="s")
        - int/float -> numeric (no t attribute)
        - None -> deletes cell
        """
        if value is None:
            self.delete_cell(ref)
            return

        row_idx, col_idx = parse_cell_ref(ref)
        row_num = row_idx + 1
        normalized = format_cell_ref(row_idx, col_idx)

        row_elem = self._get_or_create_row(row_num)
        c_elem = self._find_cell(row_elem, normalized)

        if c_elem is None:
            c_elem = ET.SubElement(row_elem, _C_TAG)
            c_elem.set('r', normalized)

        # Clear existing children and type
        for child in list(c_elem):
            c_elem.remove(child)
        if 't' in c_elem.attrib:
            del c_elem.attrib['t']

        if isinstance(value, str):
            idx = self._shared_strings.get_or_add_string(value)
            c_elem.set('t', 's')
            v = ET.SubElement(c_elem, _V_TAG)
            v.text = str(idx)
        else:
            v = ET.SubElement(c_elem, _V_TAG)
            # Use repr for floats to avoid precision loss, str for ints
            if isinstance(value, float):
                v.text = repr(value) if value != int(value) else str(int(value))
            else:
                v.text = str(value)

    def delete_cell(self, ref: str) -> bool:
        """Delete a cell by reference. Returns True if cell existed."""
        row_idx, col_idx = parse_cell_ref(ref)
        row_num = row_idx + 1
        row_elem = self._rows.get(row_num)
        if row_elem is None:
            return False
        normalized = format_cell_ref(row_idx, col_idx)
        c_elem = self._find_cell(row_elem, normalized)
        if c_elem is None:
            return False
        row_elem.remove(c_elem)
        # Remove empty row
        if len(row_elem.findall(_C_TAG)) == 0:
            self._sheet_data.remove(row_elem)
            del self._rows[row_num]
        return True

    def get_range(self, range_ref: str) -> list[list[CellValue]]:
        """
        Read a rectangular range of cells as a 2D list (rows x cols).

        Missing cells are returned as CellValue(value=None, is_string=False).
        """
        (r1, c1), (r2, c2) = parse_range_ref(range_ref)
        result = []
        for r in range(r1, r2 + 1):
            row_data = []
            for c in range(c1, c2 + 1):
                ref = format_cell_ref(r, c)
                row_data.append(self.get_cell(ref))
            result.append(row_data)
        return result

    def set_range(self, range_ref: str, values: list[list[Union[str, float, int, None]]]) -> None:
        """
        Write a 2D array of values to a rectangular range.

        The values list must match the dimensions of the range.
        """
        (r1, c1), (r2, c2) = parse_range_ref(range_ref)
        for ri, r in enumerate(range(r1, r2 + 1)):
            for ci, c in enumerate(range(c1, c2 + 1)):
                ref = format_cell_ref(r, c)
                self.set_cell(ref, values[ri][ci])

    def get_dimension(self) -> Optional[str]:
        """Get the worksheet dimension (e.g., 'A1:D5')."""
        dim = self._root.find(_DIMENSION_TAG)
        if dim is not None:
            return dim.get('ref')
        return None

    def set_dimension(self, ref: str) -> None:
        """Set the worksheet dimension."""
        dim = self._root.find(_DIMENSION_TAG)
        if dim is None:
            dim = ET.SubElement(self._root, _DIMENSION_TAG)
            # Move before sheetData
            self._root.remove(dim)
            self._root.insert(0, dim)
        dim.set('ref', ref)

    def get_row_count(self) -> int:
        """Get the number of rows with data."""
        return len(self._rows)

    def delete_row(self, row_index: int) -> bool:
        """Delete a row by 0-based index. Returns True if row existed."""
        row_num = row_index + 1
        row_elem = self._rows.get(row_num)
        if row_elem is None:
            return False
        self._sheet_data.remove(row_elem)
        del self._rows[row_num]
        return True

    def get_table_rel_ids(self) -> list[str]:
        """Get relationship IDs of tables linked to this sheet."""
        tp_elem = self._root.find(_TABLE_PARTS_TAG)
        if tp_elem is None:
            return []
        return [
            tp.get(f'{R_NS}id', '')
            for tp in tp_elem.findall(_TABLE_PART_TAG)
        ]

    def add_table_part_ref(self, rel_id: str) -> None:
        """Add a table part reference to this worksheet."""
        tp_elem = self._root.find(_TABLE_PARTS_TAG)
        if tp_elem is None:
            tp_elem = ET.SubElement(self._root, _TABLE_PARTS_TAG)
        tp = ET.SubElement(tp_elem, _TABLE_PART_TAG)
        tp.set(f'{R_NS}id', rel_id)
        # Update count
        count = len(tp_elem.findall(_TABLE_PART_TAG))
        tp_elem.set('count', str(count))

    def save(self) -> None:
        """Save worksheet XML and relationships back to the package."""
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

    @property
    def rels_manager(self) -> RelationshipsManager:
        return self._rels_manager
