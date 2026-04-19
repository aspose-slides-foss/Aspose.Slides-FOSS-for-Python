from __future__ import annotations
from ..BasePortionFormat import BasePortionFormat
from .IChartPortionFormat import IChartPortionFormat


class ChartPortionFormat(IChartPortionFormat, BasePortionFormat):
    """Chart portion formatting — wraps <a:defRPr> inside <c:txPr>.

    Inherits all properties from BasePortionFormat (font_bold, font_italic,
    font_height, latin_font, fill_format, line_format, etc.) since <a:defRPr>
    has the same attribute schema as <a:rPr>.
    """

    def __init__(self):
        # Do NOT call super().__init__() — it creates a detached element.
        # We'll get our element from _init_internal.
        self._rpr_element = None
        self._slide_part = None
        self._parent_slide = None
