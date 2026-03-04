from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .ICellFormat import ICellFormat
    from .IColumn import IColumn
    from .IRow import IRow
    from .ITable import ITable
    from .ITextFrame import ITextFrame
    from .TextAnchorType import TextAnchorType
    from .TextVerticalType import TextVerticalType

class ICell(ISlideComponent, IPresentationComponent, ABC):
    """Represents a cell in a table."""
    @property
    def offset_x(self) -> float:
        """Returns a distance from left side of a table to left side of a cell. Read-only ."""
        ...

    @property
    def offset_y(self) -> float:
        """Returns a distance from top side of a table to top side of a cell. Read-only ."""
        ...

    @property
    def first_row_index(self) -> int:
        """Returns an index of first row, covered by the cell. Read-only ."""
        ...

    @property
    def first_column_index(self) -> int:
        """Returns an index of first column, covered by the cell. Read-only ."""
        ...

    @property
    def width(self) -> float:
        """Returns the width of the cell. Read-only ."""
        ...

    @property
    def height(self) -> float:
        """Returns the height of the cell. Read-only ."""
        ...

    @property
    def minimal_height(self) -> float:
        """Returns the minimum height of a cell. This is a sum of minimal heights of all rows cowered by the cell. Read-only ."""
        ...

    @property
    def margin_left(self) -> float:
        """Returns or sets the left margin in a TextFrame. Read/write ."""
        ...

    @margin_left.setter
    def margin_left(self, value: float):
        ...

    @property
    def margin_right(self) -> float:
        """Returns or sets the right margin in a TextFrame. Read/write ."""
        ...

    @margin_right.setter
    def margin_right(self, value: float):
        ...

    @property
    def margin_top(self) -> float:
        """Returns or sets the top margin in a TextFrame. Read/write ."""
        ...

    @margin_top.setter
    def margin_top(self, value: float):
        ...

    @property
    def margin_bottom(self) -> float:
        """Returns or sets the bottom margin in a TextFrame. Read/write ."""
        ...

    @margin_bottom.setter
    def margin_bottom(self, value: float):
        ...

    @property
    def text_vertical_type(self) -> TextVerticalType:
        """Returns or sets the type of vertical text. Read/write ."""
        ...

    @text_vertical_type.setter
    def text_vertical_type(self, value: TextVerticalType):
        ...

    @property
    def text_anchor_type(self) -> TextAnchorType:
        """Returns or sets the text anchor type. Read/write ."""
        ...

    @text_anchor_type.setter
    def text_anchor_type(self, value: TextAnchorType):
        ...

    @property
    def anchor_center(self) -> bool:
        """Determines whether or not text box centered inside a cell. Read/write ."""
        ...

    @anchor_center.setter
    def anchor_center(self, value: bool):
        ...

    @property
    def first_column(self) -> IColumn:
        """Gets first column of cell. Read-only ."""
        ...

    @property
    def first_row(self) -> IRow:
        """Gets first row of cell. Read-only ."""
        ...

    @property
    def col_span(self) -> int:
        """Returns the number of grid columns in the parent table's table grid which shall be spanned by the current cell. This property allows cells to have the appearance of being merged, as they span vertical boundaries of other cells in the table. Read-only ."""
        ...

    @property
    def row_span(self) -> int:
        """Returns the number of rows that a merged cell spans. This is used in combination with the vMerge attribute on other cells in order to specify the beginning cell of a horizontal merge. Read-only ."""
        ...

    @property
    def text_frame(self) -> ITextFrame:
        """Returns the text frame of a cell. Read-only ."""
        ...

    @property
    def table(self) -> ITable:
        """Returns the parent Table object for a cell. Read-only ."""
        ...

    @property
    def is_merged_cell(self) -> bool:
        """Returns true if the cell is merged with any adjusted cell, false otherwise. Read-only ."""
        ...

    @property
    def cell_format(self) -> ICellFormat:
        """Returns the CellFormat object that contains formatting properties for this cell. Read-only ."""
        ...

    @property
    def as_i_slide_component(self) -> ISlideComponent:
        """Allows to get base ISlideComponent interface. Read-only ."""
        ...





