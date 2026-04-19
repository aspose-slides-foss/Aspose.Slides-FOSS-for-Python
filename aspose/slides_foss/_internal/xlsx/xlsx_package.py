"""
High-level facade for XLSX packages.

Provides open/create/save operations for embedded Excel workbooks
used as chart data sources in PPTX presentations.
"""

from __future__ import annotations
import io
from pathlib import Path
from typing import Optional, Union

from ..opc.opc_package import OpcPackage
from ..opc.content_types import ContentTypesManager
from ..opc.relationships import RelationshipsManager
from .constants import XLSX_REL_TYPES, XLSX_CONTENT_TYPES
from .workbook_part import WorkbookPart, SheetInfo
from .worksheet_part import WorksheetPart
from .shared_strings_part import SharedStringsPart
from .table_part import TablePart

_TEMPLATE_PATH = Path(__file__).parent / 'template.xlsx'


class XlsxPackage:
    """
    Facade for reading and writing XLSX packages.

    Wraps an OpcPackage and provides convenient access to workbook,
    worksheets, shared strings, and tables.
    """

    def __init__(self, opc_package: OpcPackage):
        self._opc = opc_package
        self._ct_manager: Optional[ContentTypesManager] = None
        self._workbook: Optional[WorkbookPart] = None
        self._shared_strings: Optional[SharedStringsPart] = None
        self._worksheets: dict[str, WorksheetPart] = {}  # keyed by part_name
        self._tables: dict[str, TablePart] = {}  # keyed by part_name

    @classmethod
    def from_bytes(cls, data: bytes) -> XlsxPackage:
        """Open an XLSX package from raw bytes (e.g., from an embedded part)."""
        stream = io.BytesIO(data)
        opc = OpcPackage.open(stream)
        return cls(opc)

    @classmethod
    def create_new(cls) -> XlsxPackage:
        """Create a new XLSX package from the minimal template."""
        opc = OpcPackage.open(str(_TEMPLATE_PATH))
        return cls(opc)

    def to_bytes(self) -> bytes:
        """Save all parts and return the XLSX as bytes."""
        self.save_all()
        stream = io.BytesIO()
        self._opc.save(stream)
        return stream.getvalue()

    # --- Lazy-init part accessors ---

    @property
    def content_types(self) -> ContentTypesManager:
        if self._ct_manager is None:
            self._ct_manager = ContentTypesManager(self._opc)
        return self._ct_manager

    @property
    def workbook(self) -> WorkbookPart:
        if self._workbook is None:
            self._workbook = WorkbookPart(self._opc)
        return self._workbook

    @property
    def shared_strings(self) -> SharedStringsPart:
        if self._shared_strings is None:
            # Shared strings part may not exist yet (empty workbook)
            if not self._opc.has_part(SharedStringsPart.PART_NAME):
                # Create empty shared strings
                self._shared_strings = SharedStringsPart(self._opc)
                # Register content type
                self.content_types.add_override(
                    SharedStringsPart.PART_NAME,
                    XLSX_CONTENT_TYPES['shared_strings'],
                )
                # Add relationship from workbook
                wb_rels = self.workbook._rels_manager
                # Check if relationship already exists
                existing = wb_rels.get_relationships_by_type(XLSX_REL_TYPES['shared_strings'])
                if not existing:
                    wb_rels.add_relationship(
                        XLSX_REL_TYPES['shared_strings'],
                        'sharedStrings.xml',
                    )
            self._shared_strings = SharedStringsPart(self._opc)
        return self._shared_strings

    # --- Worksheet access ---

    def get_worksheet(self, name_or_index: Union[str, int]) -> Optional[WorksheetPart]:
        """Get a worksheet by name (str) or 0-based index (int)."""
        if isinstance(name_or_index, int):
            info = self.workbook.get_sheet_by_index(name_or_index)
        else:
            info = self.workbook.get_sheet_by_name(name_or_index)
        if info is None:
            return None
        return self._get_or_load_worksheet(info.part_name)

    def _get_or_load_worksheet(self, part_name: str) -> WorksheetPart:
        """Load a worksheet lazily."""
        if part_name not in self._worksheets:
            self._worksheets[part_name] = WorksheetPart(
                self._opc, part_name, self.shared_strings
            )
        return self._worksheets[part_name]

    def add_worksheet(self, name: str) -> WorksheetPart:
        """Add a new empty worksheet and return it."""
        info = self.workbook.add_sheet(name, self.content_types)
        # Create the empty worksheet part in the package
        ws = WorksheetPart(self._opc, info.part_name, self.shared_strings)
        ws.save()  # Persist empty sheet XML
        self._worksheets[info.part_name] = ws
        return ws

    def get_sheet_names(self) -> list[str]:
        """Get names of all sheets in order."""
        return [s.name for s in self.workbook.get_sheets()]

    # --- Table access ---

    def get_table(self, part_name: str) -> TablePart:
        """Get a table part by its part name."""
        if part_name not in self._tables:
            self._tables[part_name] = TablePart(self._opc, part_name)
        return self._tables[part_name]

    def create_table(
        self,
        worksheet: WorksheetPart,
        display_name: str,
        ref: str,
        column_names: list[str],
    ) -> TablePart:
        """
        Create a new table linked to a worksheet.

        Args:
            worksheet: The worksheet to link the table to.
            display_name: Table display name.
            ref: Cell range (e.g., 'A1:D5').
            column_names: Column header names.
        """
        table_id = self._next_table_id()
        part_name = self._next_table_part_name()

        # Create the table part
        table = TablePart.create_new(
            self._opc, part_name, table_id, display_name, ref, column_names
        )

        # Register content type
        self.content_types.add_override(part_name, XLSX_CONTENT_TYPES['table'])

        # Add relationship from worksheet to table
        # Relative path from xl/worksheets/ to xl/tables/
        rel_target = '../tables/' + part_name.rsplit('/', 1)[-1]
        rel_id = worksheet.rels_manager.add_relationship(
            XLSX_REL_TYPES['table'], rel_target
        )

        # Add tablePart reference in worksheet XML
        worksheet.add_table_part_ref(rel_id)

        self._tables[part_name] = table
        return table

    def _next_table_id(self) -> int:
        """Generate next unique table ID."""
        max_id = 0
        for part_name in self._opc.get_part_names():
            if part_name.startswith('xl/tables/table') and part_name.endswith('.xml'):
                try:
                    tp = self.get_table(part_name)
                    max_id = max(max_id, tp.get_table_id())
                except (ValueError, KeyError):
                    pass
        return max_id + 1

    def _next_table_part_name(self) -> str:
        """Generate next available table part name."""
        counter = 1
        while True:
            name = f'xl/tables/table{counter}.xml'
            if not self._opc.has_part(name):
                return name
            counter += 1

    # --- Save ---

    def save_all(self) -> None:
        """Save all modified parts back to the OPC package."""
        if self._shared_strings is not None:
            self._shared_strings.save()
        for ws in self._worksheets.values():
            ws.save()
        for tbl in self._tables.values():
            tbl.save()
        if self._workbook is not None:
            self._workbook.save()
        if self._ct_manager is not None:
            self._ct_manager.save()

    @property
    def opc_package(self) -> OpcPackage:
        """Access the underlying OPC package."""
        return self._opc
