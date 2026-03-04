from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ._mocks.Guid import Guid
    from .ISectionSlideCollection import ISectionSlideCollection
    from .ISlide import ISlide

class ISection(ABC):
    pass
