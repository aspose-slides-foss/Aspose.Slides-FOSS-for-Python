from __future__ import annotations
from typing import Any, Optional
import lxml.etree as ET
from .ITextAnimationCollection import ITextAnimationCollection
from .TextAnimation import TextAnimation
from .._internal.base_collection import BaseCollection
from .._internal.pptx.constants import Elements


class TextAnimationCollection(BaseCollection, ITextAnimationCollection):
    """Represents collection of text animations."""

    def __init__(self):
        self._items: list = []
        self._bld_lst_elem = None

    def _init_internal(self, bld_lst_elem: Optional[ET._Element] = None):
        self._bld_lst_elem = bld_lst_elem
        self._items = []
        if bld_lst_elem is not None:
            self._parse()

    def _parse(self):
        from .TextAnimation import TextAnimation
        for bld_p in self._bld_lst_elem.findall(Elements.P_BLD_P):
            ta = TextAnimation()
            ta._init_internal(bld_p)
            self._items.append(ta)

    @property
    def as_i_collection(self) -> list:
        return self._items

    @property
    def as_i_enumerable(self) -> Any:
        return iter(self._items)

    def add(self) -> TextAnimation:
        ta = TextAnimation()
        self._items.append(ta)
        return ta

    def __getitem__(self, index: int) -> TextAnimation:
        return self._items[index]

    def __len__(self):
        return len(self._items)
