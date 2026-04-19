from __future__ import annotations
from .IPoint import IPoint


class Point(IPoint):
    """Represents animation point."""

    def __init__(self, time: float = 0.0, value: object = None, formula: str = ''):
        self._time = time
        self._value = value
        self._formula = formula

    @property
    def time(self) -> float:
        return self._time

    @time.setter
    def time(self, value: float):
        self._time = value

    @property
    def value(self) -> object:
        return self._value

    @value.setter
    def value(self, val: object):
        self._value = val

    @property
    def formula(self) -> str:
        return self._formula

    @formula.setter
    def formula(self, value: str):
        self._formula = value
