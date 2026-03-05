from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .IAdjustValue import IAdjustValue

if TYPE_CHECKING:
    from ._internal.pptx.slide_part import SlidePart

class AdjustValue(IAdjustValue):
    """Represents a geometry shape's adjustment value. These values affect shape's form."""

    def __init__(self):
        self._gd_element: ET._Element = None
        self._slide_part = None

    def _init_internal(self, gd_element: ET._Element, slide_part) -> None:
        self._gd_element = gd_element
        self._slide_part = slide_part

    @property
    def name(self) -> str:
        """Returns a name of this adjustment value. Read-only ."""
        if self._gd_element is None:
            return ''
        return self._gd_element.get('name', '')

    @property
    def raw_value(self) -> int:
        """Returns or sets adjustment value "as is". Read/write ."""
        if self._gd_element is None:
            return 0
        fmla = self._gd_element.get('fmla', '')
        if fmla.startswith('val '):
            try:
                return int(fmla[4:])
            except ValueError:
                return 0
        return 0

    @raw_value.setter
    def raw_value(self, value: int):
        if self._gd_element is None:
            return
        self._gd_element.set('fmla', f'val {value}')
        if self._slide_part:
            self._slide_part.save()

    @property
    def angle_value(self) -> float:
        """Returns or sets value, interpreting it as angle in degrees. Read/write ."""
        return self.raw_value / 60000.0

    @angle_value.setter
    def angle_value(self, value: float):
        self.raw_value = int(round(value * 60000.0))

