from __future__ import annotations
from typing import TYPE_CHECKING
from .ICell import ICell
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .IBaseSlide import IBaseSlide
    from .ICellFormat import ICellFormat
    from .IColumn import IColumn
    from .IPresentation import IPresentation
    from .IRow import IRow
    from .ITable import ITable
    from .ITextFrame import ITextFrame
    from .TextAnchorType import TextAnchorType
    from .TextVerticalType import TextVerticalType

class Cell(ICell, ISlideComponent, IPresentationComponent):
    """Represents a cell of a table."""

    def _init_internal(self, tc_element, row_index, col_index, slide_part, parent_slide, table):
        self._tc_element = tc_element
        self._row_index = row_index
        self._col_index = col_index
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        self._table = table
        return self

    def _get_tc_pr(self):
        """Get or create the <a:tcPr> element."""
        if self._tc_element is None:
            return None
        from ._internal.pptx.constants import Elements
        tc_pr = self._tc_element.find(Elements.A_TC_PR)
        return tc_pr

    def _ensure_tc_pr(self):
        """Get or create the <a:tcPr> element."""
        from ._internal.pptx.constants import Elements
        import lxml.etree as ET
        tc_pr = self._tc_element.find(Elements.A_TC_PR)
        if tc_pr is None:
            tc_pr = ET.SubElement(self._tc_element, Elements.A_TC_PR)
        return tc_pr

    @property
    def offset_x(self) -> float:
        """Returns a distance from left side of a table to left side of a cell. Read-only ."""
        from ._internal.pptx.constants import EMU_PER_POINT
        total = 0.0
        cols = self._table.columns
        for i in range(self._col_index):
            total += cols[i].width
        return total

    @property
    def offset_y(self) -> float:
        """Returns a distance from top side of a table to top side of a cell. Read-only ."""
        total = 0.0
        rows = self._table.rows
        for i in range(self._row_index):
            total += rows[i].height
        return total

    @property
    def first_row_index(self) -> int:
        """Returns an index of first row, covered by the cell. Read-only ."""
        return self._row_index

    @property
    def first_column_index(self) -> int:
        """Returns an index of first column, covered by the cell. Read-only ."""
        return self._col_index

    @property
    def width(self) -> float:
        """Returns the width of the cell. Read-only ."""
        cols = self._table.columns
        span = self.col_span
        total = 0.0
        for i in range(self._col_index, min(self._col_index + span, len(cols))):
            total += cols[i].width
        return total

    @property
    def height(self) -> float:
        """Returns the height of the cell. Read-only ."""
        rows = self._table.rows
        span = self.row_span
        total = 0.0
        for i in range(self._row_index, min(self._row_index + span, len(rows))):
            total += rows[i].height
        return total

    @property
    def minimal_height(self) -> float:
        """Returns the minimum height of a cell. This is a sum of minimal heights of all rows cowered by the cell. Read-only ."""
        rows = self._table.rows
        span = self.row_span
        total = 0.0
        for i in range(self._row_index, min(self._row_index + span, len(rows))):
            total += rows[i].minimal_height
        return total

    @property
    def margin_left(self) -> float:
        """Returns or sets the left margin in a TextFrame. Read/write ."""
        tc_pr = self._get_tc_pr()
        if tc_pr is not None:
            val = tc_pr.get('marL')
            if val is not None:
                from ._internal.pptx.constants import EMU_PER_POINT
                return int(val) / EMU_PER_POINT
        # Default: 91440 EMU
        from ._internal.pptx.constants import EMU_PER_POINT
        return 91440 / EMU_PER_POINT

    @margin_left.setter
    def margin_left(self, value: float):
        from ._internal.pptx.constants import EMU_PER_POINT
        tc_pr = self._ensure_tc_pr()
        tc_pr.set('marL', str(int(round(value * EMU_PER_POINT))))
        if self._slide_part:
            self._slide_part.save()

    @property
    def margin_right(self) -> float:
        """Returns or sets the right margin in a TextFrame. Read/write ."""
        tc_pr = self._get_tc_pr()
        if tc_pr is not None:
            val = tc_pr.get('marR')
            if val is not None:
                from ._internal.pptx.constants import EMU_PER_POINT
                return int(val) / EMU_PER_POINT
        from ._internal.pptx.constants import EMU_PER_POINT
        return 91440 / EMU_PER_POINT

    @margin_right.setter
    def margin_right(self, value: float):
        from ._internal.pptx.constants import EMU_PER_POINT
        tc_pr = self._ensure_tc_pr()
        tc_pr.set('marR', str(int(round(value * EMU_PER_POINT))))
        if self._slide_part:
            self._slide_part.save()

    @property
    def margin_top(self) -> float:
        """Returns or sets the top margin in a TextFrame. Read/write ."""
        tc_pr = self._get_tc_pr()
        if tc_pr is not None:
            val = tc_pr.get('marT')
            if val is not None:
                from ._internal.pptx.constants import EMU_PER_POINT
                return int(val) / EMU_PER_POINT
        from ._internal.pptx.constants import EMU_PER_POINT
        return 45720 / EMU_PER_POINT

    @margin_top.setter
    def margin_top(self, value: float):
        from ._internal.pptx.constants import EMU_PER_POINT
        tc_pr = self._ensure_tc_pr()
        tc_pr.set('marT', str(int(round(value * EMU_PER_POINT))))
        if self._slide_part:
            self._slide_part.save()

    @property
    def margin_bottom(self) -> float:
        """Returns or sets the bottom margin in a TextFrame. Read/write ."""
        tc_pr = self._get_tc_pr()
        if tc_pr is not None:
            val = tc_pr.get('marB')
            if val is not None:
                from ._internal.pptx.constants import EMU_PER_POINT
                return int(val) / EMU_PER_POINT
        from ._internal.pptx.constants import EMU_PER_POINT
        return 45720 / EMU_PER_POINT

    @margin_bottom.setter
    def margin_bottom(self, value: float):
        from ._internal.pptx.constants import EMU_PER_POINT
        tc_pr = self._ensure_tc_pr()
        tc_pr.set('marB', str(int(round(value * EMU_PER_POINT))))
        if self._slide_part:
            self._slide_part.save()

    @property
    def text_vertical_type(self) -> TextVerticalType:
        """Returns or sets the type of vertical text. Read/write ."""
        from .TextVerticalType import TextVerticalType
        _VERT_MAP = {
            'horz': TextVerticalType.HORIZONTAL,
            'vert': TextVerticalType.VERTICAL,
            'vert270': TextVerticalType.VERTICAL270,
            'wordArtVert': TextVerticalType.WORD_ART_VERTICAL,
            'eaVert': TextVerticalType.EAST_ASIAN_VERTICAL,
            'mongolianVert': TextVerticalType.MONGOLIAN_VERTICAL,
            'wordArtVertRtl': TextVerticalType.WORD_ART_VERTICAL_RIGHT_TO_LEFT,
        }
        tc_pr = self._get_tc_pr()
        if tc_pr is not None:
            val = tc_pr.get('vert')
            if val is not None:
                return _VERT_MAP.get(val, TextVerticalType.NOT_DEFINED)
        return TextVerticalType.NOT_DEFINED

    @text_vertical_type.setter
    def text_vertical_type(self, value: TextVerticalType):
        from .TextVerticalType import TextVerticalType
        _VERT_REVERSE = {
            TextVerticalType.HORIZONTAL: 'horz',
            TextVerticalType.VERTICAL: 'vert',
            TextVerticalType.VERTICAL270: 'vert270',
            TextVerticalType.WORD_ART_VERTICAL: 'wordArtVert',
            TextVerticalType.EAST_ASIAN_VERTICAL: 'eaVert',
            TextVerticalType.MONGOLIAN_VERTICAL: 'mongolianVert',
            TextVerticalType.WORD_ART_VERTICAL_RIGHT_TO_LEFT: 'wordArtVertRtl',
        }
        tc_pr = self._ensure_tc_pr()
        ooxml_val = _VERT_REVERSE.get(value)
        if ooxml_val is not None:
            tc_pr.set('vert', ooxml_val)
        elif 'vert' in tc_pr.attrib:
            del tc_pr.attrib['vert']
        if self._slide_part:
            self._slide_part.save()

    @property
    def text_anchor_type(self) -> TextAnchorType:
        """Returns or sets the text anchor type. Read/write ."""
        from .TextAnchorType import TextAnchorType
        _ANCHOR_MAP = {
            't': TextAnchorType.TOP,
            'ctr': TextAnchorType.CENTER,
            'b': TextAnchorType.BOTTOM,
            'just': TextAnchorType.JUSTIFIED,
            'dist': TextAnchorType.DISTRIBUTED,
        }
        tc_pr = self._get_tc_pr()
        if tc_pr is not None:
            val = tc_pr.get('anchor')
            if val is not None:
                return _ANCHOR_MAP.get(val, TextAnchorType.NOT_DEFINED)
        return TextAnchorType.NOT_DEFINED

    @text_anchor_type.setter
    def text_anchor_type(self, value: TextAnchorType):
        from .TextAnchorType import TextAnchorType
        _ANCHOR_REVERSE = {
            TextAnchorType.TOP: 't',
            TextAnchorType.CENTER: 'ctr',
            TextAnchorType.BOTTOM: 'b',
            TextAnchorType.JUSTIFIED: 'just',
            TextAnchorType.DISTRIBUTED: 'dist',
        }
        tc_pr = self._ensure_tc_pr()
        ooxml_val = _ANCHOR_REVERSE.get(value)
        if ooxml_val is not None:
            tc_pr.set('anchor', ooxml_val)
        elif 'anchor' in tc_pr.attrib:
            del tc_pr.attrib['anchor']
        if self._slide_part:
            self._slide_part.save()

    @property
    def anchor_center(self) -> bool:
        """Determines whether or not text box centered inside a cell. Read/write ."""
        tc_pr = self._get_tc_pr()
        if tc_pr is not None:
            return tc_pr.get('anchorCtr', '0') == '1'
        return False

    @anchor_center.setter
    def anchor_center(self, value: bool):
        tc_pr = self._ensure_tc_pr()
        if value:
            tc_pr.set('anchorCtr', '1')
        elif 'anchorCtr' in tc_pr.attrib:
            del tc_pr.attrib['anchorCtr']
        if self._slide_part:
            self._slide_part.save()

    @property
    def first_row(self) -> IRow:
        """Gets first row of cell. Read-only ."""
        return self._table.rows[self._row_index]

    @property
    def first_column(self) -> IColumn:
        """Gets first column of cell. Read-only ."""
        return self._table.columns[self._col_index]

    @property
    def col_span(self) -> int:
        """Returns the number of grid columns in the parent table's table grid which shall be spanned by the current cell. This property allows cells to have the appearance of being merged, as they span vertical boundaries of other cells in the table. Read-only ."""
        if hasattr(self, '_tc_element') and self._tc_element is not None:
            val = self._tc_element.get('gridSpan')
            if val is not None:
                return int(val)
        return 1

    @property
    def row_span(self) -> int:
        """Returns the number of rows that a merged cell spans. This is used in combination with the vMerge attribute on other cells in order to specify the beginning cell of a horizontal merge. Read-only ."""
        if hasattr(self, '_tc_element') and self._tc_element is not None:
            val = self._tc_element.get('rowSpan')
            if val is not None:
                return int(val)
        return 1

    @property
    def text_frame(self) -> ITextFrame:
        """Returns the text frame of a cell. Read-only ."""
        if self._tc_element is None:
            return None
        from .TextFrame import TextFrame
        from ._internal.pptx.constants import Elements
        txbody = self._tc_element.find(Elements.A_TX_BODY)
        if txbody is None:
            return None
        tf = TextFrame()
        tf._init_internal(txbody, self._slide_part, self._parent_slide)
        tf._parent_cell = self
        return tf

    @property
    def table(self) -> ITable:
        """Returns the parent Table object for a cell. Read-only ."""
        return self._table

    @property
    def is_merged_cell(self) -> bool:
        """Returns true if the cell is merged with any adjusted cell, false otherwise. Read-only ."""
        if self._tc_element is None:
            return False
        tc = self._tc_element
        if tc.get('gridSpan') is not None and int(tc.get('gridSpan', '1')) > 1:
            return True
        if tc.get('rowSpan') is not None and int(tc.get('rowSpan', '1')) > 1:
            return True
        if tc.get('hMerge') == '1':
            return True
        if tc.get('vMerge') == '1':
            return True
        return False

    @property
    def cell_format(self) -> ICellFormat:
        """Returns the CellFormat object that contains formatting properties for this cell. Read-only ."""
        from .CellFormat import CellFormat
        cf = CellFormat()
        tc_pr = self._ensure_tc_pr()
        cf._init_internal(tc_pr, self._slide_part, self._parent_slide)
        return cf

    @property
    def slide(self) -> IBaseSlide:
        """Returns the parent slide of a cell. Read-only ."""
        return self._parent_slide

    @property
    def presentation(self) -> IPresentation:
        """Returns the parent presentation of a cell. Read-only ."""
        if hasattr(self, '_parent_slide') and self._parent_slide is not None:
            return self._parent_slide.presentation
        return None

    @property
    def as_i_slide_component(self) -> ISlideComponent:
        return self

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        return self




