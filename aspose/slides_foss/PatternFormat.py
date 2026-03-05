from __future__ import annotations
from typing import overload, TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .IPatternFormat import IPatternFormat
from ._internal.pptx.constants import NS, Elements

if TYPE_CHECKING:
    from .IColorFormat import IColorFormat
    from .IImage import IImage
    from .PatternStyle import PatternStyle
    from ._internal.pptx.slide_part import SlidePart

# OOXML prst value -> PatternStyle enum name
_PRST_TO_PATTERN = {
    'pct5': 'PERCENT05', 'pct10': 'PERCENT10', 'pct20': 'PERCENT20',
    'pct25': 'PERCENT25', 'pct30': 'PERCENT30', 'pct40': 'PERCENT40',
    'pct50': 'PERCENT50', 'pct60': 'PERCENT60', 'pct70': 'PERCENT70',
    'pct75': 'PERCENT75', 'pct80': 'PERCENT80', 'pct90': 'PERCENT90',
    'dkHorz': 'DARK_HORIZONTAL', 'dkVert': 'DARK_VERTICAL',
    'dkDnDiag': 'DARK_DOWNWARD_DIAGONAL', 'dkUpDiag': 'DARK_UPWARD_DIAGONAL',
    'smCheck': 'SMALL_CHECKER_BOARD', 'trellis': 'TRELLIS',
    'ltHorz': 'LIGHT_HORIZONTAL', 'ltVert': 'LIGHT_VERTICAL',
    'ltDnDiag': 'LIGHT_DOWNWARD_DIAGONAL', 'ltUpDiag': 'LIGHT_UPWARD_DIAGONAL',
    'smGrid': 'SMALL_GRID', 'dottedDmnd': 'DOTTED_DIAMOND',
    'wdDnDiag': 'WIDE_DOWNWARD_DIAGONAL', 'wdUpDiag': 'WIDE_UPWARD_DIAGONAL',
    'dashDnDiag': 'DASHED_DOWNWARD_DIAGONAL', 'dashUpDiag': 'DASHED_UPWARD_DIAGONAL',
    'narVert': 'NARROW_VERTICAL', 'narHorz': 'NARROW_HORIZONTAL',
    'dashVert': 'DASHED_VERTICAL', 'dashHorz': 'DASHED_HORIZONTAL',
    'lgConfetti': 'LARGE_CONFETTI', 'lgGrid': 'LARGE_GRID',
    'horzBrick': 'HORIZONTAL_BRICK', 'lgCheck': 'LARGE_CHECKER_BOARD',
    'smConfetti': 'SMALL_CONFETTI', 'zigZag': 'ZIGZAG',
    'solidDmnd': 'SOLID_DIAMOND', 'diagBrick': 'DIAGONAL_BRICK',
    'openDmnd': 'OUTLINED_DIAMOND', 'plaid': 'PLAID',
    'sphere': 'SPHERE', 'weave': 'WEAVE', 'dottedGrid': 'DOTTED_GRID',
    'divot': 'DIVOT', 'shingle': 'SHINGLE', 'wave': 'WAVE',
    'horz': 'HORIZONTAL', 'vert': 'VERTICAL', 'cross': 'CROSS',
    'dnDiag': 'DOWNWARD_DIAGONAL', 'upDiag': 'UPWARD_DIAGONAL',
    'diagCross': 'DIAGONAL_CROSS',
}

_PATTERN_TO_PRST = {v: k for k, v in _PRST_TO_PATTERN.items()}


class PatternFormat(PVIObject, ISlideComponent, IPresentationComponent, IPatternFormat):
    """Represents a pattern to fill a shape."""

    def _init_internal(self, patt_fill_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        self._patt_fill = patt_fill_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def pattern_style(self) -> PatternStyle:
        """Returns or sets the pattern style. Read/write."""
        from .PatternStyle import PatternStyle
        prst = self._patt_fill.get('prst')
        if prst is None:
            return PatternStyle.NOT_DEFINED
        name = _PRST_TO_PATTERN.get(prst)
        if name:
            return PatternStyle[name]
        return PatternStyle.UNKNOWN

    @pattern_style.setter
    def pattern_style(self, value: PatternStyle):
        from .PatternStyle import PatternStyle
        if value in (PatternStyle.NOT_DEFINED, PatternStyle.UNKNOWN):
            if 'prst' in self._patt_fill.attrib:
                del self._patt_fill.attrib['prst']
        else:
            prst = _PATTERN_TO_PRST.get(value.name)
            if prst:
                self._patt_fill.set('prst', prst)
        self._save()

    @property
    def fore_color(self) -> IColorFormat:
        """Returns the foreground pattern color. Read-only."""
        from .ColorFormat import ColorFormat
        fg_clr = self._patt_fill.find(Elements.A_FG_CLR)
        if fg_clr is None:
            fg_clr = ET.SubElement(self._patt_fill, Elements.A_FG_CLR)
        cf = ColorFormat()
        cf._init_internal(fg_clr, self._slide_part, self._parent_slide)
        return cf

    @property
    def back_color(self) -> IColorFormat:
        """Returns the background pattern color. Read-only."""
        from .ColorFormat import ColorFormat
        bg_clr = self._patt_fill.find(Elements.A_BG_CLR)
        if bg_clr is None:
            bg_clr = ET.SubElement(self._patt_fill, Elements.A_BG_CLR)
        cf = ColorFormat()
        cf._init_internal(bg_clr, self._slide_part, self._parent_slide)
        return cf



