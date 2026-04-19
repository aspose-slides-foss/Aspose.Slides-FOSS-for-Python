from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IFillParamSource import IFillParamSource

if TYPE_CHECKING:
    from .IEffectFormatEffectiveData import IEffectFormatEffectiveData
    from .IFillFormatEffectiveData import IFillFormatEffectiveData

class IBackgroundEffectiveData(IFillParamSource, ABC):
    """Immutable object which contains effective background properties."""
    @property
    @abstractmethod
    def fill_format(self) -> IFillFormatEffectiveData:
        ...

    @property
    @abstractmethod
    def effect_format(self) -> IEffectFormatEffectiveData:
        ...

    @property
    @abstractmethod
    def as_i_fill_param_source(self) -> IFillParamSource:
        ...
