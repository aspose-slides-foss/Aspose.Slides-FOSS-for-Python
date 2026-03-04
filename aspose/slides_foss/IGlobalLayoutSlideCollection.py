from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any
from .ILayoutSlideCollection import ILayoutSlideCollection

if TYPE_CHECKING:
    from .ILayoutSlide import ILayoutSlide

class IGlobalLayoutSlideCollection(ILayoutSlideCollection, ABC):
    """Represents a collection of all layout slides in presentation. Extends ILayoutSlideCollection interface with methods for adding/cloning layout slides in context of uniting of the individual collections of master's layout slides."""
    @property
    def as_i_layout_slide_collection(self) -> ILayoutSlideCollection:
        """Returns ILayoutSlideCollection interface. Read-only ."""
        ...




