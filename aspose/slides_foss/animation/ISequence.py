from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IEffect import IEffect
    from ..IShape import IShape

class ISequence(ABC):
    """Represents sequence (collection of effects)."""
    @property
    @abstractmethod
    def count(self) -> int:
        """Returns the number of effects in a sequense. Read-only ."""
        ...
    @property
    @abstractmethod
    def trigger_shape(self) -> IShape:
        """Returns or sets shape target for INTERACTIVE sequence. If sequence is not interactive then returns null. Read/write ."""
        ...
    @trigger_shape.setter
    @abstractmethod
    def trigger_shape(self, value: IShape):
        ...
    @property
    @abstractmethod
    def as_i_enumerable(self) -> Any:
        """Allows to get base IEnumerable interface. Read-only ."""
        ...
    @overload
    @abstractmethod
    def add_effect(self, shape, effect_type, subtype, trigger_type) -> IEffect:
        ...

    @overload
    @abstractmethod
    def add_effect(self, paragraph, effect_type, subtype, trigger_type) -> IEffect:
        ...

    @overload
    @abstractmethod
    def add_effect(self, chart, type, index, effect_type, subtype, trigger_type) -> IEffect:
        ...

    @overload
    @abstractmethod
    def add_effect(self, chart, type, series_index, categories_index, effect_type, subtype, trigger_type) -> IEffect:
        ...

    def add_effect(self, *args, **kwargs) -> IEffect:
        ...
    @abstractmethod
    def remove(self, item) -> None:
        ...
    @abstractmethod
    def remove_at(self, index) -> None:
        ...
    @abstractmethod
    def clear(self) -> None:
        ...
    @abstractmethod
    def remove_by_shape(self, shape) -> None:
        ...
    @abstractmethod
    def get_effects_by_shape(self, shape) -> list[IEffect]:
        ...
    @abstractmethod
    def get_effects_by_paragraph(self, paragraph) -> list[IEffect]:
        ...
    @abstractmethod
    def get_count(self, shape) -> int:
        ...
    @abstractmethod
    def __getitem__(self, index: int) -> IEffect:
        ...