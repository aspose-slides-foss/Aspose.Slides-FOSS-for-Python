from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .ILayoutSlideCollection import ILayoutSlideCollection

if TYPE_CHECKING:
    from .ILayoutSlide import ILayoutSlide
    from .LayoutSlide import LayoutSlide

from ._internal.base_collection import BaseCollection
class LayoutSlideCollection(BaseCollection, ILayoutSlideCollection):
    """Represents a base class for collection of a layout slides."""
    @property
    def as_i_collection(self) -> list:
        return list(self._layouts)

    @property
    def as_i_enumerable(self) -> Any:
        return iter(self._layouts)

    def get_by_type(self, type) -> ILayoutSlide:
        for layout in self._layouts:
            if layout.layout_type == type:
                return layout
        return None



    def __getitem__(self, index: int) -> GlobalLayoutSlide:
        return self._layouts[index]

