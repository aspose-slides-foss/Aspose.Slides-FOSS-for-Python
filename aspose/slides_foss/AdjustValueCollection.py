from __future__ import annotations
from typing import TYPE_CHECKING, Any
import lxml.etree as ET
from .IAdjustValueCollection import IAdjustValueCollection

if TYPE_CHECKING:
    from .AdjustValue import AdjustValue
    from ._internal.pptx.slide_part import SlidePart

from ._internal.base_collection import BaseCollection
class AdjustValueCollection(BaseCollection, IAdjustValueCollection):
    """Reprasents a collection of shape's adjustments."""

    def __init__(self):
        self._av_lst: ET._Element = None
        self._slide_part = None

    def _init_internal(self, av_lst_element: ET._Element, slide_part) -> AdjustValueCollection:
        self._av_lst = av_lst_element
        self._slide_part = slide_part
        return self

    def _get_gd_elements(self) -> list:
        if self._av_lst is None:
            return []
        from ._internal.pptx.constants import NS
        return self._av_lst.findall(f"{NS.A}gd")

    def __len__(self) -> int:
        return len(self._get_gd_elements())

    def __getitem__(self, index: int) -> AdjustValue:
        from .AdjustValue import AdjustValue
        gd_elements = self._get_gd_elements()
        if index < 0 or index >= len(gd_elements):
            raise IndexError(f"Index {index} is out of range")
        gd = gd_elements[index]
        av = AdjustValue()
        av._init_internal(gd, self._slide_part)
        return av

    @property
    def as_i_collection(self) -> list:
        from .AdjustValue import AdjustValue
        result = []
        for gd in self._get_gd_elements():
            av = AdjustValue()
            av._init_internal(gd, self._slide_part)
            result.append(av)
        return result

    @property
    def as_i_enumerable(self) -> Any:
        return self.as_i_collection
