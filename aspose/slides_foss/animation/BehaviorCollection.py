from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
import lxml.etree as ET
from .IBehaviorCollection import IBehaviorCollection
from .._internal.base_collection import BaseCollection
from .._internal.pptx.constants import Elements

if TYPE_CHECKING:
    from .Behavior import Behavior


class BehaviorCollection(BaseCollection, IBehaviorCollection):
    """Represents collection of behavior effects."""

    def _init_internal(self, child_tn_lst: Optional[ET._Element], slide_part=None):
        """Initialize from the <p:childTnLst> of an effect's <p:cTn>."""
        self._child_tn_lst = child_tn_lst
        self._slide_part = slide_part
        self._items: list = []
        if child_tn_lst is not None:
            self._parse_behaviors()

    def _parse_behaviors(self):
        """Parse child elements into behavior objects."""
        from .SetEffect import SetEffect
        from .MotionEffect import MotionEffect
        from .ColorEffect import ColorEffect
        from .RotationEffect import RotationEffect
        from .ScaleEffect import ScaleEffect
        from .FilterEffect import FilterEffect
        from .PropertyEffect import PropertyEffect
        from .CommandEffect import CommandEffect

        _TAG_MAP = {
            Elements.P_SET: SetEffect,
            Elements.P_ANIM: PropertyEffect,
            Elements.P_ANIM_EFFECT: FilterEffect,
            Elements.P_ANIM_MOTION: MotionEffect,
            Elements.P_ANIM_CLR: ColorEffect,
            Elements.P_ANIM_ROT: RotationEffect,
            Elements.P_ANIM_SCALE: ScaleEffect,
            Elements.P_CMD: CommandEffect,
        }

        for child in self._child_tn_lst:
            cls = _TAG_MAP.get(child.tag)
            if cls is not None:
                obj = cls()
                obj._init_internal(child)
                self._items.append(obj)

    @property
    def count(self) -> int:
        return len(self._items)

    @property
    def is_read_only(self) -> bool:
        return False

    @property
    def as_i_enumerable(self) -> Any:
        return iter(self._items)

    def add(self, item) -> None:
        self._items.append(item)
        if self._child_tn_lst is not None and hasattr(item, '_elem'):
            self._child_tn_lst.append(item._elem)

    def index_of(self, item) -> int:
        try:
            return self._items.index(item)
        except ValueError:
            return -1

    def insert(self, index, item) -> None:
        self._items.insert(index, item)
        if self._child_tn_lst is not None and hasattr(item, '_elem'):
            self._child_tn_lst.insert(index, item._elem)

    def copy_to(self, array, array_index) -> None:
        for i, item in enumerate(self._items):
            array[array_index + i] = item

    def remove(self, item) -> bool:
        try:
            self._items.remove(item)
            if self._child_tn_lst is not None and hasattr(item, '_elem'):
                self._child_tn_lst.remove(item._elem)
            return True
        except ValueError:
            return False

    def remove_at(self, index) -> None:
        item = self._items.pop(index)
        if self._child_tn_lst is not None and hasattr(item, '_elem'):
            self._child_tn_lst.remove(item._elem)

    def clear(self) -> None:
        for item in self._items:
            if self._child_tn_lst is not None and hasattr(item, '_elem'):
                try:
                    self._child_tn_lst.remove(item._elem)
                except ValueError:
                    pass
        self._items.clear()

    def contains(self, item) -> bool:
        return item in self._items

    def __getitem__(self, index: int) -> Behavior:
        return self._items[index]

    def __len__(self):
        return len(self._items)
