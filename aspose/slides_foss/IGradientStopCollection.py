from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IGradientStop import IGradientStop

class IGradientStopCollection(ABC):
    """Represnts a collection of gradient stops."""
    @property
    def as_i_collection(self) -> list:
        ...

    @property
    def as_i_enumerable(self) -> Any:
        ...

    @overload
    def add(self, position, color) -> IGradientStop:
        ...

    @overload
    def add(self, position, preset_color) -> IGradientStop:
        ...

    @overload
    def add(self, position, scheme_color) -> IGradientStop:
        ...


    @overload
    def insert(self, index, position, color) -> None:
        ...

    @overload
    def insert(self, index, position, preset_color) -> None:
        ...

    @overload
    def insert(self, index, position, scheme_color) -> None:
        ...
    def remove_at(self, index) -> None:
        ...
    def clear(self) -> None:
        ...
    def __getitem__(self, index: int) -> IGradientStop:
        ...

