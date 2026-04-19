from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .ILineFormatCollection import ILineFormatCollection
from .._internal.base_collection import BaseCollection
from .._internal.pptx.constants import NS, Elements

if TYPE_CHECKING:
    from ..LineFormat import LineFormat
    from .._internal.pptx.theme_part import ThemePart

import lxml.etree as ET


def _patch_line_format(lf, style_list_elem, index):
    """Monkey-patch a LineFormat to work on a specific index in the list."""

    def _get_ln():
        children = list(style_list_elem)
        if index < len(children):
            return children[index]
        return None

    def _ensure_ln():
        ln = _get_ln()
        if ln is not None:
            return ln
        ln = ET.Element(Elements.A_LN)
        style_list_elem.insert(index, ln)
        return ln

    lf._get_ln = _get_ln
    lf._ensure_ln = _ensure_ln


class LineFormatCollection(BaseCollection, ILineFormatCollection):
    """Represents the collection of line styles."""

    def _init_internal(self, style_list_elem: ET._Element, theme_part: ThemePart) -> None:
        self._style_list_elem = style_list_elem
        self._theme_part = theme_part
        self._items_cache: dict[int, object] = {}

    def __len__(self) -> int:
        return len(list(self._style_list_elem))

    def __getitem__(self, index: int) -> LineFormat:
        if index in self._items_cache:
            return self._items_cache[index]
        children = list(self._style_list_elem)
        if index < 0 or index >= len(children):
            raise IndexError(f"Index {index} out of range")

        from ..LineFormat import LineFormat as LF
        lf = LF()
        lf._init_internal(self._style_list_elem, self._theme_part, None)
        _patch_line_format(lf, self._style_list_elem, index)
        self._items_cache[index] = lf
        return lf

    @property
    def as_i_collection(self) -> list:
        return list(self)

    @property
    def as_i_enumerable(self) -> Any:
        return self
