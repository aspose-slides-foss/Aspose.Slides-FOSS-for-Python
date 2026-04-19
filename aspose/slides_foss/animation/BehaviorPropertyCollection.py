from __future__ import annotations
from typing import Any, Optional
import lxml.etree as ET
from .BehaviorProperty import BehaviorProperty
from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
from .._internal.base_collection import BaseCollection
from .._internal.pptx.constants import Elements


class BehaviorPropertyCollection(BaseCollection, IBehaviorPropertyCollection):
    """Represents collection of behavior properties."""

    def _init_internal(self, attr_lst_elem: Optional[ET._Element], cbhvr_elem: Optional[ET._Element]):
        self._attr_lst = attr_lst_elem
        self._cbhvr = cbhvr_elem
        self._items: list = []
        if self._attr_lst is not None:
            from .BehaviorProperty import BehaviorProperty
            for attr_name in self._attr_lst.findall(Elements.P_ATTR_NAME):
                text = attr_name.text or ''
                self._items.append(BehaviorProperty.get_or_create_by_value(text))

    @property
    def as_i_enumerable(self) -> Any:
        return iter(self._items)

    def add(self, property_value) -> None:
        from .BehaviorProperty import BehaviorProperty
        if isinstance(property_value, str):
            bp = BehaviorProperty.get_or_create_by_value(property_value)
        else:
            bp = property_value
        self._items.append(bp)
        if self._attr_lst is not None:
            an = ET.SubElement(self._attr_lst, Elements.P_ATTR_NAME)
            an.text = bp.value

    def index_of(self, property_value) -> int:
        for i, item in enumerate(self._items):
            if item.value == (property_value if isinstance(property_value, str) else property_value.value):
                return i
        return -1

    def __getitem__(self, index: int) -> BehaviorProperty:
        return self._items[index]

    def __len__(self):
        return len(self._items)
