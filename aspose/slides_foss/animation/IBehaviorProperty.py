from __future__ import annotations
from abc import ABC, abstractmethod

class IBehaviorProperty(ABC):
    """Represent property types for animation behavior. Follows the list of properties from https://msdn.microsoft.com/en-us/library/dd949052(v=office.15).aspx and https://msdn.microsoft.com/en-us/library/documentformat.openxml.presentation.attributename(v=office.15).aspx"""
    @property
    @abstractmethod
    def value(self) -> str:
        """Value of the property"""
        ...
    @property
    @abstractmethod
    def is_custom(self) -> bool:
        """Shows if this property does not belong to the predefined properties list in the specification: https://msdn.microsoft.com/en-us/library/dd949052(v=office.15).aspx"""
        ...