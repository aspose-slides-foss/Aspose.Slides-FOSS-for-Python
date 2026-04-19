from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from ..IBasePortionFormat import IBasePortionFormat

if TYPE_CHECKING:
    from ..IColorFormat import IColorFormat
    from ..IEffectFormat import IEffectFormat
    from ..IFillFormat import IFillFormat
    from ..IFontData import IFontData
    from ..ILineFormat import ILineFormat
    from ..NullableBool import NullableBool
    from ..TextCapType import TextCapType
    from ..TextStrikethroughType import TextStrikethroughType
    from ..TextUnderlineType import TextUnderlineType

class IChartPortionFormat(IBasePortionFormat, ABC):
    """Represents the chart portion formatting properties used in charts."""
    pass
