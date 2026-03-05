from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
from .ILayoutSlideCollection import ILayoutSlideCollection
if TYPE_CHECKING:
    from .ILayoutSlide import ILayoutSlide

class IMasterLayoutSlideCollection(ILayoutSlideCollection, ABC):
    pass
