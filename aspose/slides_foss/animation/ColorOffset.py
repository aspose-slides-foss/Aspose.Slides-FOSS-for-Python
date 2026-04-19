from __future__ import annotations
from .IColorOffset import IColorOffset


class ColorOffset(IColorOffset):
    """Represent color offset."""

    def __init__(self):
        self._v0 = 0.0
        self._v1 = 0.0
        self._v2 = 0.0

    @property
    def value0(self) -> float:
        return self._v0

    @value0.setter
    def value0(self, value: float):
        self._v0 = value

    @property
    def value1(self) -> float:
        return self._v1

    @value1.setter
    def value1(self, value: float):
        self._v1 = value

    @property
    def value2(self) -> float:
        return self._v2

    @value2.setter
    def value2(self, value: float):
        self._v2 = value
