from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ILineParamSource import ILineParamSource

if TYPE_CHECKING:
    from .ILineFillFormat import ILineFillFormat
    from .ILineFormatEffectiveData import ILineFormatEffectiveData
    from .ISketchFormat import ISketchFormat
    from .LineAlignment import LineAlignment
    from .LineArrowheadLength import LineArrowheadLength
    from .LineArrowheadStyle import LineArrowheadStyle
    from .LineArrowheadWidth import LineArrowheadWidth
    from .LineCapStyle import LineCapStyle
    from .LineDashStyle import LineDashStyle
    from .LineJoinStyle import LineJoinStyle
    from .LineStyle import LineStyle

class ILineFormat(ILineParamSource, ABC):
    """Represents format of a line."""
    @property
    def is_format_not_defined(self) -> bool:
        """Returns true if line format is not defined (as just created, default). Read-only ."""
        ...

    @property
    def fill_format(self) -> ILineFillFormat:
        """Returns the fill format of a line. Read-only ."""
        ...


    @property
    def width(self) -> float:
        """Returns or sets the width of a line. Read/write ."""
        ...

    @width.setter
    def width(self, value: float):
        ...

    @property
    def dash_style(self) -> LineDashStyle:
        """Returns or sets the line dash style. Read/write ."""
        ...

    @dash_style.setter
    def dash_style(self, value: LineDashStyle):
        ...

    @property
    def custom_dash_pattern(self) -> list[float]:
        """Returns or sets the custom dash pattern. Read/write []."""
        ...

    @custom_dash_pattern.setter
    def custom_dash_pattern(self, value: list[float]):
        ...

    @property
    def cap_style(self) -> LineCapStyle:
        """Returns or sets the line cap style. Read/write ."""
        ...

    @cap_style.setter
    def cap_style(self, value: LineCapStyle):
        ...

    @property
    def style(self) -> LineStyle:
        """Returns or sets the line style. Read/write ."""
        ...

    @style.setter
    def style(self, value: LineStyle):
        ...

    @property
    def alignment(self) -> LineAlignment:
        """Returns or sets the line alignment. Read/write ."""
        ...

    @alignment.setter
    def alignment(self, value: LineAlignment):
        ...

    @property
    def join_style(self) -> LineJoinStyle:
        """Returns or sets the lines join style. Read/write ."""
        ...

    @join_style.setter
    def join_style(self, value: LineJoinStyle):
        ...

    @property
    def miter_limit(self) -> float:
        """Returns or sets the miter limit of a line. Read/write ."""
        ...

    @miter_limit.setter
    def miter_limit(self, value: float):
        ...

    @property
    def begin_arrowhead_style(self) -> LineArrowheadStyle:
        """Returns or sets the arrowhead style at the beginning of a line. Read/write ."""
        ...

    @begin_arrowhead_style.setter
    def begin_arrowhead_style(self, value: LineArrowheadStyle):
        ...

    @property
    def end_arrowhead_style(self) -> LineArrowheadStyle:
        """Returns or sets the arrowhead style at the end of a line. Read/write ."""
        ...

    @end_arrowhead_style.setter
    def end_arrowhead_style(self, value: LineArrowheadStyle):
        ...

    @property
    def begin_arrowhead_width(self) -> LineArrowheadWidth:
        """Returns or sets the arrowhead width at the beginning of a line. Read/write ."""
        ...

    @begin_arrowhead_width.setter
    def begin_arrowhead_width(self, value: LineArrowheadWidth):
        ...

    @property
    def end_arrowhead_width(self) -> LineArrowheadWidth:
        """Returns or sets the arrowhead width at the end of a line. Read/write ."""
        ...

    @end_arrowhead_width.setter
    def end_arrowhead_width(self, value: LineArrowheadWidth):
        ...

    @property
    def begin_arrowhead_length(self) -> LineArrowheadLength:
        """Returns or sets the arrowhead length at the beginning of a line. Read/write ."""
        ...

    @begin_arrowhead_length.setter
    def begin_arrowhead_length(self, value: LineArrowheadLength):
        ...

    @property
    def end_arrowhead_length(self) -> LineArrowheadLength:
        """Returns or sets the arrowhead length at the end of a line. Read/write ."""
        ...

    @end_arrowhead_length.setter
    def end_arrowhead_length(self, value: LineArrowheadLength):
        ...




