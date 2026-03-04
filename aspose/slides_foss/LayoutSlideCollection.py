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
        if hasattr(self, '_layouts'):
            return list(self._layouts)
        raise NotImplementedError("This feature is not yet available in this version.")

    @property
    def as_i_enumerable(self) -> Any:
        if hasattr(self, '_layouts'):
            return iter(self._layouts)
        raise NotImplementedError("This feature is not yet available in this version.")

    def get_by_type(self, type) -> ILayoutSlide:
        if hasattr(self, '_layouts'):
            for layout in self._layouts:
                if layout.layout_type == type:
                    return layout
            return None
        raise NotImplementedError("This feature is not yet available in this version.")



    def __getitem__(self, index: int) -> GlobalLayoutSlide:
        if hasattr(self, '_layouts'):
            return self._layouts[index]
        raise NotImplementedError("This feature is not yet available in this version.")

