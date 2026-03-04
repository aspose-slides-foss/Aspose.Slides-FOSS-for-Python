from __future__ import annotations
from typing import overload, TYPE_CHECKING
from .GraphicalObject import GraphicalObject
from .ITable import ITable

if TYPE_CHECKING:
    from .IBulkTextFormattable import IBulkTextFormattable
    from .ICell import ICell
    from .IColumnCollection import IColumnCollection
    from .IGraphicalObject import IGraphicalObject
    from .IGraphicalObjectLock import IGraphicalObjectLock
    from .IRowCollection import IRowCollection
    from .ITableFormat import ITableFormat
    from .TableStylePreset import TableStylePreset

class Table(GraphicalObject, ITable):
    """Represents a table on a slide."""

    def _init_internal(self, xml_element, slide_part, parent_slide) -> None:
        super()._init_internal(xml_element, slide_part, parent_slide)
        from ._internal.pptx.constants import Elements
        # Locate the <a:tbl> element inside the graphicFrame
        self._tbl = xml_element.find(f".//{Elements.A_TBL}")
        if self._tbl is not None:
            self._tbl_pr = self._tbl.find(Elements.A_TBL_PR)
            self._tbl_grid = self._tbl.find(Elements.A_TBL_GRID)

    def _get_tbl_pr(self):
        if hasattr(self, '_tbl_pr') and self._tbl_pr is not None:
            return self._tbl_pr
        return None

    def _ensure_tbl_pr(self):
        import lxml.etree as ET
        from ._internal.pptx.constants import Elements
        if hasattr(self, '_tbl_pr') and self._tbl_pr is not None:
            return self._tbl_pr
        self._tbl_pr = ET.SubElement(self._tbl, Elements.A_TBL_PR)
        # Insert as first child
        self._tbl.insert(0, self._tbl_pr)
        return self._tbl_pr

    @property
    def graphical_object_lock(self) -> IGraphicalObjectLock:
        from .GraphicalObjectLock import GraphicalObjectLock
        return GraphicalObjectLock()

    @property
    def rows(self) -> IRowCollection:
        """Returns the collectoin of rows. Read-only ."""
        if not hasattr(self, '_tbl') or self._tbl is None:
            raise NotImplementedError("This feature is not yet available in this version.")
        from .RowCollection import RowCollection
        rc = RowCollection()
        rc._init_internal(self._tbl, self._slide_part, self._parent_slide, self)
        return rc

    @property
    def columns(self) -> IColumnCollection:
        """Returns the collectoin of columns. Read-only ."""
        if not hasattr(self, '_tbl') or self._tbl is None:
            raise NotImplementedError("This feature is not yet available in this version.")
        from .ColumnCollection import ColumnCollection
        cc = ColumnCollection()
        cc._init_internal(self._tbl, self._tbl_grid, self._slide_part, self._parent_slide, self)
        return cc

    @property
    def table_format(self) -> ITableFormat:
        """Returns the TableFormat object that contains formatting properties for this table. Read-only ."""
        from .TableFormat import TableFormat
        tf = TableFormat()
        tbl_pr = self._ensure_tbl_pr()
        tf._init_internal(tbl_pr, self._slide_part, self._parent_slide)
        return tf

    def _get_bool_attr(self, attr_name: str) -> bool:
        tbl_pr = self._get_tbl_pr()
        if tbl_pr is not None:
            return tbl_pr.get(attr_name, '0') == '1'
        return False

    def _set_bool_attr(self, attr_name: str, value: bool):
        tbl_pr = self._ensure_tbl_pr()
        if value:
            tbl_pr.set(attr_name, '1')
        elif attr_name in tbl_pr.attrib:
            del tbl_pr.attrib[attr_name]
        if self._slide_part:
            self._slide_part.save()

    def _find_style_element(self, tbl_pr):
        """Find the table style element - either <a:tableStyleId> or legacy <a:tblStyle>."""
        from ._internal.pptx.constants import Elements
        el = tbl_pr.find(Elements.A_TABLE_STYLE_ID)
        if el is not None:
            return el
        return tbl_pr.find(Elements.A_TBL_STYLE)

    def _read_style_guid(self, style_el) -> str:
        """Read GUID from either <a:tableStyleId>text</a:tableStyleId> or <a:tblStyle val="..."/>."""
        if style_el is None:
            return ''
        # <a:tableStyleId> stores GUID as text content
        if style_el.text:
            return style_el.text.strip()
        # Legacy <a:tblStyle> stores GUID as val attribute
        return style_el.get('val', '')

    @property
    def style_preset(self) -> TableStylePreset:
        """Gets or sets builtin table style. Read/write ."""
        from .TableStylePreset import TableStylePreset
        from ._internal.pptx.table_style_mapping import GUID_TO_PRESET
        tbl_pr = self._get_tbl_pr()
        if tbl_pr is not None:
            style_el = self._find_style_element(tbl_pr)
            if style_el is not None:
                guid = self._read_style_guid(style_el)
                preset_name = GUID_TO_PRESET.get(guid)
                if preset_name is not None:
                    try:
                        return TableStylePreset[preset_name]
                    except KeyError:
                        return TableStylePreset.CUSTOM
                return TableStylePreset.CUSTOM
        return TableStylePreset.NONE

    @style_preset.setter
    def style_preset(self, value: TableStylePreset):
        from .TableStylePreset import TableStylePreset
        from ._internal.pptx.table_style_mapping import PRESET_TO_GUID
        from ._internal.pptx.constants import Elements
        import lxml.etree as ET
        tbl_pr = self._ensure_tbl_pr()
        style_el = self._find_style_element(tbl_pr)

        if value == TableStylePreset.NONE:
            if style_el is not None:
                tbl_pr.remove(style_el)
        else:
            guid = PRESET_TO_GUID.get(value.name, '')
            if guid:
                if style_el is not None:
                    tbl_pr.remove(style_el)
                style_el = ET.SubElement(tbl_pr, Elements.A_TABLE_STYLE_ID)
                style_el.text = guid
        if self._slide_part:
            self._slide_part.save()

    @property
    def right_to_left(self) -> bool:
        """Determines whether the table has right to left reading order. Read-write ."""
        return self._get_bool_attr('rtl')

    @right_to_left.setter
    def right_to_left(self, value: bool):
        self._set_bool_attr('rtl', value)

    @property
    def first_row(self) -> bool:
        """Determines whether the first row of a table has to be drawn with a special formatting. Read/write ."""
        return self._get_bool_attr('firstRow')

    @first_row.setter
    def first_row(self, value: bool):
        self._set_bool_attr('firstRow', value)

    @property
    def first_col(self) -> bool:
        """Determines whether the first column of a table has to be drawn with a special formatting. Read/write ."""
        return self._get_bool_attr('firstCol')

    @first_col.setter
    def first_col(self, value: bool):
        self._set_bool_attr('firstCol', value)

    @property
    def last_row(self) -> bool:
        """Determines whether the last row of a table has to be drawn with a special formatting. Read/write ."""
        return self._get_bool_attr('lastRow')

    @last_row.setter
    def last_row(self, value: bool):
        self._set_bool_attr('lastRow', value)

    @property
    def last_col(self) -> bool:
        """Determines whether the last column of a table has to be drawn with a special formatting. Read/write ."""
        return self._get_bool_attr('lastCol')

    @last_col.setter
    def last_col(self, value: bool):
        self._set_bool_attr('lastCol', value)

    @property
    def horizontal_banding(self) -> bool:
        """Determines whether the even rows has to be drawn with a different formatting. Read/write ."""
        return self._get_bool_attr('bandRow')

    @horizontal_banding.setter
    def horizontal_banding(self, value: bool):
        self._set_bool_attr('bandRow', value)

    @property
    def vertical_banding(self) -> bool:
        """Determines whether the even columns has to be drawn with a different formatting. Read/write ."""
        return self._get_bool_attr('bandCol')

    @vertical_banding.setter
    def vertical_banding(self, value: bool):
        self._set_bool_attr('bandCol', value)

    @property
    def as_i_graphical_object(self) -> IGraphicalObject:
        return self

    @property
    def as_i_bulk_text_formattable(self) -> IBulkTextFormattable:
        return self




    def set_text_format(self, *args, **kwargs) -> None:
        if len(args) < 1:
            raise NotImplementedError("This feature is not yet available in this version.")
        source = args[0]
        from ._internal.pptx.bulk_text_format import apply_text_format
        cells = []
        for row in self.rows:
            for cell in row:
                cells.append(cell)
        apply_text_format(cells, source, self._slide_part)

    def merge_cells(self, cell1, cell2, allow_splitting) -> ICell:
        if not hasattr(self, '_tbl') or self._tbl is None:
            raise NotImplementedError("This feature is not yet available in this version.")

        r1 = cell1.first_row_index
        c1 = cell1.first_column_index
        r2 = cell2.first_row_index
        c2 = cell2.first_column_index

        # Ensure r1,c1 is top-left and r2,c2 is bottom-right
        top_row = min(r1, r2)
        bot_row = max(r1, r2)
        left_col = min(c1, c2)
        right_col = max(c1, c2)

        row_span = bot_row - top_row + 1
        grid_span = right_col - left_col + 1

        from ._internal.pptx.constants import Elements

        trs = self._tbl.findall(Elements.A_TR)
        for ri in range(top_row, bot_row + 1):
            if ri >= len(trs):
                break
            tcs = trs[ri].findall(Elements.A_TC)
            for ci in range(left_col, right_col + 1):
                if ci >= len(tcs):
                    break
                tc = tcs[ci]
                if ri == top_row and ci == left_col:
                    # Anchor cell
                    if grid_span > 1:
                        tc.set('gridSpan', str(grid_span))
                    if row_span > 1:
                        tc.set('rowSpan', str(row_span))
                else:
                    if ci > left_col:
                        tc.set('hMerge', '1')
                    if ri > top_row:
                        tc.set('vMerge', '1')

        if self._slide_part:
            self._slide_part.save()

        # Return the anchor cell
        from .Cell import Cell
        anchor_tc = trs[top_row].findall(Elements.A_TC)[left_col]
        anchor_cell = Cell()
        anchor_cell._init_internal(anchor_tc, top_row, left_col, self._slide_part, self._parent_slide, self)
        return anchor_cell
