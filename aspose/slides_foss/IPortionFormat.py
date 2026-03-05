from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IBasePortionFormat import IBasePortionFormat
from .IHyperlinkContainer import IHyperlinkContainer
if TYPE_CHECKING:
    from .IPortionFormatEffectiveData import IPortionFormatEffectiveData

class IPortionFormat(IBasePortionFormat, IHyperlinkContainer, ABC):
    pass
