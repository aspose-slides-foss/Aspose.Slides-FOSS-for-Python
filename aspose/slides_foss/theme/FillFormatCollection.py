from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .IFillFormatCollection import IFillFormatCollection
from .._internal.base_collection import BaseCollection
from .._internal.pptx.constants import NS, Elements

if TYPE_CHECKING:
    from ..FillFormat import FillFormat
    from .._internal.pptx.theme_part import ThemePart

import lxml.etree as ET

# Fill element tags
_FILL_TAGS = {
    Elements.A_NO_FILL, Elements.A_SOLID_FILL, Elements.A_GRAD_FILL,
    Elements.A_BLIP_FILL, Elements.A_PATT_FILL, Elements.A_GRP_FILL,
}


class _ThemeFillFormat:
    """
    Thin wrapper that adapts FillFormat for indexed access within a theme
    fill style list. Overrides element lookup to work on a specific position.
    """

    def __new__(cls, style_list_elem, index, theme_part):
        from ..FillFormat import FillFormat as FF
        obj = FF.__new__(FF)
        obj._parent_element = style_list_elem
        obj._slide_part = theme_part
        obj._parent_slide = None
        obj._fill_index = index
        return obj


def _patch_fill_format(ff, style_list_elem, index):
    """Monkey-patch a FillFormat to work on a specific index in the list."""
    original_find = ff._find_fill_element
    original_remove = ff._remove_fill_elements
    original_insert = ff._insert_fill_element

    def _find_fill_element():
        children = list(style_list_elem)
        if index < len(children):
            return children[index]
        return None

    def _remove_fill_elements():
        children = list(style_list_elem)
        if index < len(children):
            style_list_elem.remove(children[index])

    def _insert_fill_element(tag):
        el = ET.Element(tag)
        style_list_elem.insert(index, el)
        return el

    ff._find_fill_element = _find_fill_element
    ff._remove_fill_elements = _remove_fill_elements
    ff._insert_fill_element = _insert_fill_element


class FillFormatCollection(BaseCollection, IFillFormatCollection):
    """Represents the collection of fill styles."""

    def _init_internal(self, style_list_elem: ET._Element, theme_part: ThemePart) -> None:
        self._style_list_elem = style_list_elem
        self._theme_part = theme_part
        self._items_cache: dict[int, object] = {}

    def __len__(self) -> int:
        return len(list(self._style_list_elem))

    def __getitem__(self, index: int) -> FillFormat:
        if index in self._items_cache:
            return self._items_cache[index]
        children = list(self._style_list_elem)
        if index < 0 or index >= len(children):
            raise IndexError(f"Index {index} out of range")

        from ..FillFormat import FillFormat as FF
        ff = FF()
        ff._init_internal(self._style_list_elem, self._theme_part, None)
        _patch_fill_format(ff, self._style_list_elem, index)
        self._items_cache[index] = ff
        return ff

    @property
    def as_i_collection(self) -> list:
        return list(self)

    @property
    def as_i_enumerable(self) -> Any:
        return self
