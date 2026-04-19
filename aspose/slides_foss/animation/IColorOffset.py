from __future__ import annotations
from abc import ABC, abstractmethod

class IColorOffset(ABC):
    """Represent color offset."""
    @property
    @abstractmethod
    def value0(self) -> float:
        """Defines first value of offset. Read/write ."""
        ...
    @value0.setter
    @abstractmethod
    def value0(self, value: float):
        ...
    @property
    @abstractmethod
    def value1(self) -> float:
        """Defines second value of offset. Read/write ."""
        ...
    @value1.setter
    @abstractmethod
    def value1(self, value: float):
        ...
    @property
    @abstractmethod
    def value2(self) -> float:
        """Defines third value of offset. Read/write ."""
        ...
    @value2.setter
    @abstractmethod
    def value2(self, value: float):
        ...