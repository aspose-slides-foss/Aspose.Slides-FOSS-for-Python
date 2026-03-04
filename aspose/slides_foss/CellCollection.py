from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .ICellCollection import ICellCollection

if TYPE_CHECKING:
    from .Cell import Cell
    from .IBaseSlide import IBaseSlide
    from .IPresentation import IPresentation

from ._internal.base_collection import BaseCollection
class CellCollection(BaseCollection, ICellCollection):
    """Represents a collection of cells."""

    def _init_internal(self, cells, slide_part, parent_slide):
        self._cells = cells
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        return self

    @property
    def slide(self) -> IBaseSlide:
        """Returns the parent slide of a CellCollection. Read-only ."""
        if hasattr(self, '_parent_slide'):
            return self._parent_slide
        raise NotImplementedError("This feature is not yet available in this version.")

    @property
    def presentation(self) -> IPresentation:
        """Returns the parent presentation of a CellCollection. Read-only ."""
        if hasattr(self, '_parent_slide') and self._parent_slide is not None:
            return self._parent_slide.presentation
        raise NotImplementedError("This feature is not yet available in this version.")

    @property
    def as_i_slide_component(self) -> ISlideComponent:
        return self

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        return self

    @property
    def as_i_collection(self) -> list:
        if hasattr(self, '_cells'):
            return list(self._cells)
        raise NotImplementedError("This feature is not yet available in this version.")

    @property
    def as_i_enumerable(self) -> Any:
        if hasattr(self, '_cells'):
            return iter(self._cells)
        raise NotImplementedError("This feature is not yet available in this version.")

    def __getitem__(self, index: int) -> Cell:
        if hasattr(self, '_cells'):
            return self._cells[index]
        raise NotImplementedError("This feature is not yet available in this version.")

    def __len__(self) -> int:
        if hasattr(self, '_cells'):
            return len(self._cells)
        return 0

    def __iter__(self):
        if hasattr(self, '_cells'):
            return iter(self._cells)
        return iter([])
