from __future__ import annotations
from abc import ABC, abstractmethod

class IPoint(ABC):
    """Represent animation point."""
    @property
    @abstractmethod
    def time(self) -> float:
        """Represents time value. Read/write ."""
        ...
    @time.setter
    @abstractmethod
    def time(self, value: float):
        ...
    @property
    @abstractmethod
    def value(self) -> object:
        """Represents point value. Only: bool, ColorFormat, float, int, string. Read/write ."""
        ...
    @value.setter
    @abstractmethod
    def value(self, value: object):
        ...
    @property
    @abstractmethod
    def formula(self) -> str:
        """Formulas within values, from, to, by attributes can be made up of these: Standard arithmetic operators: ‘+’, ‘-‘, ‘*’, ‘/’, ‘^’, ‘%’ (mod) Constants: ‘pi’ ‘e’ Conditional operators: ‘abs’, ‘min’, ‘max’, ‘?’ (if) Comparison operators: '==', '>=', '', '!=', '!' Trigonometric operators: ‘sin()’, ‘cos()’, ‘tan()’, ‘asin()’, ‘acos()’, ‘atan()’ Natural logarithm ‘ln()’ Property references (host supported properties) for example: "#ppt_x+(cos(-2*pi*(1-$))*-#ppt_x-sin(-2*pi*(1-$))*(1-#ppt_y))*(1-$)" Read/write ."""
        ...
    @formula.setter
    @abstractmethod
    def formula(self, value: str):
        ...