from __future__ import annotations
from typing import overload, TYPE_CHECKING, Any
from .LayoutSlideCollection import LayoutSlideCollection
from .IGlobalLayoutSlideCollection import IGlobalLayoutSlideCollection

if TYPE_CHECKING:
    from .ILayoutSlide import ILayoutSlide

from ._internal.base_collection import BaseCollection
class GlobalLayoutSlideCollection(LayoutSlideCollection, IGlobalLayoutSlideCollection):
    """Represents a collection of all layout slides in presentation. Extends LayoutSlideCollection class with methods for adding/cloning layout slides in context of uniting of the individual collections of master's layout slides."""

    def _init_internal(self, layouts: list) -> None:
        """Internal initialization with list of all layout slides."""
        self._layouts = layouts

    @property
    def as_i_layout_slide_collection(self) -> ILayoutSlideCollection:
        return self





    def __len__(self) -> int:
        if hasattr(self, '_layouts'):
            return len(self._layouts)
        raise NotImplementedError("This feature is not yet available in this version.")

    def __iter__(self):
        if hasattr(self, '_layouts'):
            return iter(self._layouts)
        raise NotImplementedError("This feature is not yet available in this version.")

