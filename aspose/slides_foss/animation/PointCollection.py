from __future__ import annotations
from typing import Any
from .IPointCollection import IPointCollection
from .Point import Point
from .._internal.base_collection import BaseCollection


class PointCollection(BaseCollection, IPointCollection):
    """Represents a collection of animation points."""

    def __init__(self):
        self._items: list = []

    @property
    def count(self) -> int:
        return len(self._items)

    @property
    def as_i_enumerable(self) -> Any:
        return iter(self._items)

    def __getitem__(self, index: int) -> Point:
        return self._items[index]

    def __len__(self):
        return len(self._items)
