from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .LayoutSlideCollection import LayoutSlideCollection
from .IMasterLayoutSlideCollection import IMasterLayoutSlideCollection

if TYPE_CHECKING:
    from .ILayoutSlide import ILayoutSlide

from ._internal.base_collection import BaseCollection
class MasterLayoutSlideCollection(LayoutSlideCollection, IMasterLayoutSlideCollection):
    """Represents a collections of all layout slides of defined master slide. Extends LayoutSlideCollection class with methods for adding/inserting/removing/cloning/reordering layout slides in context of the individual collections of master's layout slides."""

    def _init_internal(self, layouts: list) -> None:
        """Internal initialization with list of layout slides."""
        self._layouts = layouts








    def __len__(self) -> int:
        if hasattr(self, '_layouts'):
            return len(self._layouts)
        raise NotImplementedError("This feature is not yet available in this version.")

    def __iter__(self):
        if hasattr(self, '_layouts'):
            return iter(self._layouts)
        raise NotImplementedError("This feature is not yet available in this version.")

