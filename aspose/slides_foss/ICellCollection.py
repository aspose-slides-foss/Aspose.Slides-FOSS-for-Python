from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .ICell import ICell

class ICellCollection(ISlideComponent, IPresentationComponent, ABC):
    """Represents a collection of cells."""
    @property
    def as_i_slide_component(self) -> ISlideComponent:
        """Allows to get base ISlideComponent interface. Read-only ."""
        ...

    @property
    def as_i_collection(self) -> list:
        ...

    @property
    def as_i_enumerable(self) -> Any:
        ...
    def __getitem__(self, index: int) -> ICell:
        ...

