from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .IEffectStyleCollection import IEffectStyleCollection
from .._internal.base_collection import BaseCollection
from .._internal.pptx.constants import NS

if TYPE_CHECKING:
    from .EffectStyle import EffectStyle
    from .._internal.pptx.theme_part import ThemePart

import lxml.etree as ET


class EffectStyleCollection(BaseCollection, IEffectStyleCollection):
    """Represents a collection of effect styles."""

    def _init_internal(self, style_list_elem: ET._Element, theme_part: ThemePart) -> None:
        self._style_list_elem = style_list_elem
        self._theme_part = theme_part
        self._items_cache: dict[int, object] = {}

    def __len__(self) -> int:
        return len(list(self._style_list_elem))

    def __getitem__(self, index: int) -> EffectStyle:
        if index in self._items_cache:
            return self._items_cache[index]
        children = list(self._style_list_elem)
        if index < 0 or index >= len(children):
            raise IndexError(f"Index {index} out of range")
        child = children[index]
        from .EffectStyle import EffectStyle as ES
        es = ES()
        es._init_internal(child, self._theme_part)
        self._items_cache[index] = es
        return es

    @property
    def as_i_collection(self) -> list:
        return list(self)

    @property
    def as_i_enumerable(self) -> Any:
        return self
